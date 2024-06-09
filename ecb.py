from urllib.parse import urlencode
import matplotlib.pyplot as plt
from functools import reduce
from io import BytesIO
import pandas as pd
import base64


def plot_to_base64(plt):
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    return image_base64


def save_base64_image(base64_string, file_name):
    image_data = base64.b64decode(base64_string)
    with open(file_name, "wb") as file:
        file.write(image_data)


def get_ecb_data(serie: str, **kwargs):
    api_url = "https://data-api.ecb.europa.eu/service/data"
    flow_ref, key = tuple(serie.split('.', 1))
    url = f"{api_url}/{flow_ref}/{key}?{urlencode(kwargs)}"
    return pd.read_csv(url)[["TIME_PERIOD", "OBS_VALUE"]]


df_df = get_ecb_data(serie="FM.D.U2.EUR.4F.KR.DFR.LEV", format="csvdata")
df_mro = get_ecb_data(serie="FM.D.U2.EUR.4F.KR.MRR_FR.LEV", format="csvdata")
df_mlf = get_ecb_data(serie="FM.D.U2.EUR.4F.KR.MLFR.LEV", format="csvdata")

df = reduce(lambda left, right: pd.merge(left, right, on="TIME_PERIOD", how="outer"), [df_df, df_mro, df_mlf])
df.columns = ["Date", "Deposit Facility", "Main Refinancing Operations", "Marginal Lending Facility"]
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

plt.figure(figsize=(14, 8))
plt.step(df['Date'], df['Deposit Facility'], label='Deposit Facility', where='post')
plt.step(df['Date'], df['Main Refinancing Operations'], label='Main Refinancing Operations', linestyle='--',
         where='post')
plt.step(df['Date'], df['Marginal Lending Facility'], label='Marginal Lending Facility', linestyle=':', where='post')

plt.xlabel('Date')
plt.ylabel('Rate')
plt.title('ECB Interest Rates Over Time')
plt.legend()
plt.grid(True)

image_base64 = plot_to_base64(plt)
save_base64_image(image_base64, 'ecb/ecb.png')

for col in df.columns[1:]:
    df[col] = df[col].diff()

df = df.fillna(0)

df['Year'] = df['Date'].dt.year

changes_non_zero = df != 0

annual_rate_increases = changes_non_zero.groupby(df['Year']).sum()

colors = {
    "Deposit Facility": "blue",
    "Main Refinancing Operations": "green",
    "Marginal Lending Facility": "red"
}

i = 1

for col in df.columns[1:-1]:
    plt.figure(figsize=(14, 8))
    plt.step(annual_rate_increases.index, annual_rate_increases[col], label=f'Number of {col} Increases', where='post',
             marker='o', color=colors[col])
    plt.xlabel('Year')
    plt.ylabel('Number of Rate Changes')
    plt.title(f'Number of {col} Changes per Year')
    plt.legend()
    plt.grid(True)
    image_base64 = plot_to_base64(plt)
    save_base64_image(image_base64, f'ecb/ecb{i}.png')
    i += 1

i = 1

for col in df.columns[1:-1]:
    plt.figure(figsize=(14, 8))
    average_rate_increases = df[df[col] != 0.00].groupby('Year').mean()
    plt.step(average_rate_increases.index, average_rate_increases[col], label=f'Average {col} Increase', where='post',
             marker='o', color=colors[col])
    plt.xlabel('Year')
    plt.ylabel('Average Rate Change')
    plt.title(f'Average {col} Change per Year')
    plt.legend()
    plt.grid(True)
    image_base64 = plot_to_base64(plt)
    save_base64_image(image_base64, f'ecb/ecb_avg{i}.png')
    i += 1

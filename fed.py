from urllib.parse import urlencode
import pandas as pd
import matplotlib.pyplot as plt


def get_fred_data(**kwargs):
    base_url = "https://fred.stlouisfed.org/graph/fredgraph.csv"
    valid_params = {"id": "id", "start_date": "cosd", "end_date": "coed", "transform": "transformation",
                    "freq": "fq", "agg": "fam", "formula": "fml"}

    params = {k: ",".join(v) for k, v in kwargs.items()} if (all(isinstance(v, list) for v in kwargs.values())) else kwargs
    web_params = {v: params[k] for k, v in valid_params.items() if k in params and params[k]}
    return pd.read_csv(f"{base_url}?{urlencode(web_params)}")


df = get_fred_data(id=["DFEDTARU", "DFEDTARL", "DFEDTAR"])
df.columns = ["Date",
              "Federal Funds Target Range - Upper Limit",
              "Federal Funds Target Range - Lower Limit",
              "Federal Funds Target Rate"]
df["Date"] = pd.to_datetime(df["Date"], format='%Y-%m-%d')
df.loc[df['Date'] == '2008-12-16', 'Federal Funds Target Rate'] = df.loc[df['Date'] == '2008-12-16', 'Federal Funds Target Range - Upper Limit']
df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, axis=1, errors='coerce')

plt.figure(figsize=(14, 8))
plt.step(df['Date'], df['Federal Funds Target Rate'], label='Federal Funds Target Rate', where='post')
plt.step(df['Date'], df['Federal Funds Target Range - Upper Limit'], label='Federal Funds Target Range - Upper Limit', linestyle='--',
         where='post')
plt.step(df['Date'], df['Federal Funds Target Range - Lower Limit'], label='Federal Funds Target Range - Lower Limit', linestyle=':', where='post')

plt.xlabel('Date')
plt.ylabel('Rate')
plt.title('FED Interest Rates Over Time')
plt.legend()
plt.grid(True)
plt.savefig("fed/fed.png", dpi=1200, bbox_inches='tight')

from urllib.parse import urlencode
import pandas as pd


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
df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, axis=1, errors='coerce')

import pandas as pd
import matplotlib.pyplot as plt

data = {
    "Date": ["01/01/1999", "04/01/1999", "22/01/1999", "09/04/1999", "05/11/1999", "04/02/2000", "17/03/2000", "28/04/2000", 
             "09/06/2000", "28/06/2000", "01/09/2000", "06/10/2000", "11/05/2001", "31/08/2001", "18/09/2001", "09/11/2001", 
             "06/12/2002", "07/03/2003", "06/06/2003", "06/12/2005", "08/03/2006", "15/06/2006", "09/08/2006", "11/10/2006", 
             "13/12/2006", "14/03/2007", "13/06/2007", "09/07/2008", "08/10/2008", "09/10/2008", "15/10/2008", "12/11/2008", 
             "10/12/2008", "21/01/2009", "11/03/2009", "08/04/2009", "13/05/2009", "13/04/2011", "13/07/2011", "09/11/2011", 
             "14/12/2011", "11/07/2012", "08/05/2013", "13/11/2013", "11/06/2014", "10/09/2014", "09/12/2015", "16/03/2016", 
             "18/09/2019", "27/07/2022", "14/09/2022", "02/11/2022", "21/12/2022", "08/02/2023", "22/03/2023", "10/05/2023", 
             "21/06/2023", "02/08/2023", "20/09/2023", "12/06/2024"],
    "Deposit Facility": [2.00, 2.75, 2.00, 1.50, 2.00, 2.25, 2.50, 2.75, 3.25, 3.25, 3.50, 3.75, 3.50, 3.25, 2.75, 2.25, 1.75, 
                         1.50, 1.00, 1.25, 1.50, 1.75, 2.00, 2.25, 2.50, 2.75, 3.00, 3.25, 2.75, 3.25, 3.25, 2.75, 2.00, 1.00, 
                         0.50, 0.25, 0.25, 0.50, 0.75, 0.50, 0.25, 0.00, 0.00, 0.00, -0.10, -0.20, -0.30, -0.40, -0.50, 0.00, 
                         0.75, 1.50, 2.00, 2.50, 3.00, 3.25, 3.50, 3.75, 4.00, 3.75],
    "Fixed Rate": [3.00, 3.00, 3.00, 2.50, 3.00, 3.25, 3.50, 3.75, 4.25, None, None, None, None, None, None, None, None, None, 
                   None, None, None, None, None, None, None, None, None, None, None, None, 3.75, 3.25, 2.50, 2.00, 1.50, 1.25, 1.00, 
                   1.25, 1.50, 1.25, 1.00, 0.75, 0.50, 0.25, 0.15, 0.05, 0.05, 0.00, 0.00, 0.50, 1.25, 2.00, 2.50, 3.00, 
                   3.50, 3.75, 4.00, 4.25, 4.50, 4.25],
    "Variable Rate": [None, None, None, None, None, None, None, None, None, 4.25, 4.50, 4.75, 4.50, 4.25, 3.75, 3.25, 
                              2.75, 2.50, 2.00, 2.25, 2.50, 2.75, 3.00, 3.25, 3.50, 3.75, 4.00, 4.25, None, None, None, None, 
                              None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
                              None, None, None, None, None, None, None, None, None, None, None, None],
    "Marginal Lending Facility": [4.50, 3.25, 4.50, 3.50, 4.00, 4.25, 4.50, 4.75, 5.25, 5.25, 5.50, 5.75, 5.50, 5.25, 4.75, 
                                  4.25, 3.75, 3.50, 3.00, 3.25, 3.50, 3.75, 4.00, 4.25, 4.50, 4.75, 5.00, 5.25, 4.75, 4.25, 
                                  4.25, 3.75, 3.00, 3.00, 2.50, 2.25, 1.75, 2.00, 2.25, 2.00, 1.75, 1.50, 1.00, 0.75, 0.40, 
                                  0.30, 0.30, 0.25, 0.25, 0.75, 1.50, 2.25, 2.75, 3.25, 3.75, 4.00, 4.25, 4.50, 4.75, 4.50]
}

df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

plt.figure(figsize=(14, 8))
plt.step(df['Date'], df['Deposit Facility'], label='Deposit Facility', where='post')
plt.step(df['Date'], df['Fixed Rate'], label='Fixed Rate', linestyle='--', where='post')
plt.step(df['Date'], df['Variable Rate'], label='Variable Rate', linestyle='-.', where='post')
plt.step(df['Date'], df['Marginal Lending Facility'], label='Marginal Lending Facility', linestyle=':', where='post')

plt.xlabel('Date')
plt.ylabel('Rate')
plt.title('ECB Interest Rates Over Time')
plt.legend()
plt.grid(True)
plt.savefig("ecb.png")

rate_columns = ["Deposit Facility", "Fixed Rate", "Variable Rate", "Marginal Lending Facility"]
final_columns = ["Deposit Facility", "Main Refinancing Operations", "Marginal Lending Facility"]

df['Main Refinancing Operations'] = df['Fixed Rate'].combine_first(df['Variable Rate'])

df.drop(['Fixed Rate', 'Variable Rate'], axis=1, inplace=True)

df.fillna(method='ffill', inplace=True)

for col in final_columns:
    df[col] = df[col].diff()

df = df.fillna(0)

df['Year'] = df['Date'].dt.year

changes_non_zero = df != 0

annual_rate_increases = changes_non_zero.groupby(df['Year']).sum()
average_rate_increases = df.groupby(df['Year']).mean()

colors = {
    "Deposit Facility": "blue",
    "Main Refinancing Operations": "green",
    "Marginal Lending Facility": "red"
}

i = 1

for col in final_columns:
    plt.figure(figsize=(14, 8))
    plt.step(annual_rate_increases.index, annual_rate_increases[col], label=f'Number of {col} Increases', where='post', marker='o', color=colors[col])
    plt.xlabel('Year')
    plt.ylabel('Number of Rate Changes')
    plt.title(f'Number of {col} Changes per Year')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'ecb{i}.png')
    i += 1
    
i = 1
    
for col in final_columns:
    plt.figure(figsize=(14, 8))
    plt.step(average_rate_increases.index, average_rate_increases[col], label=f'Average {col} Increase', where='post', marker='o', color=colors[col])
    plt.xlabel('Year')
    plt.ylabel('Average Rate Change')
    plt.title(f'Average {col} Change per Year')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'ecb_avg{i}.png')
    i += 1
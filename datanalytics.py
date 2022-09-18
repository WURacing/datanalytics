import pandas

df = pandas.read_csv('0918/0918preskidpad001.csv',encoding="latin1")
# Drop bad columns and rows
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df = df.dropna()

# Convert to numeric
# pandas.to_numeric(df)
print(df)
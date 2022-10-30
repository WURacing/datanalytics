import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

try:
    DIRECTORY = sys.argv[1]
except:
    print("Usage: python datanalytics.py <directory>")
    exit()

def clean(df):
    # Drop bad columns and rows
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.dropna()
    # print(df.loc[:, (df == 0).all(axis=0)].columns)
    # df = df.loc[:, (df != 0).any(axis=0)]

    # Remove trailing white space from column names
    for column in df.columns:
        df.rename(columns={column: column.strip()}, inplace=True)

    print("Dropping columns due to constant values:",end=" ")
    for column in df.columns:
        if df[column].unique().size == 1:
            print(column,end=", ")
            df = df.drop(column, axis=1)
    print("\n")

    # Convert to numeric
    df = df.apply(pd.to_numeric)
    return df

def linearize(df):
    # Linearize Anlg #1 and rename to Oil Pressure (psi)
    if 'Anlg #1' in df.columns:
        df['Anlg #1'] = df['Anlg #1'] * 20
        df.rename(columns={'Anlg #1': 'Oil Pressure (psi)'}, inplace=True)
    return df

def plot(df, x, columns):
    df.plot(x=x, y=columns)
    plt.show()

for filename in os.listdir(DIRECTORY):
    print("Processing", filename)
    df = pd.read_csv(f"{DIRECTORY}{filename}", encoding="latin1")
    df = clean(df)
    df = linearize(df)
    print(f"{df.describe().transpose()}\n\n")
    plot(df,'RPM' , ['Oil Pressure (psi)'])
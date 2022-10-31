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

    # Linearize Anlg #2 and rename to -X Acceleration (g)
    if 'Anlg #2' in df.columns:
        df['Anlg #2'] = (df['Anlg #2'] * 2.5) - 6.25
        df.rename(columns={'Anlg #2': '-X Acceleration (g)'}, inplace=True)
    
    # Calculate change in temperature from front radiator (Anlg #3) to back (Anlg #4) Inlet/Outlet Radiator temp
    if 'Anlg #3' in df.columns and 'Anlg #4' in df.columns:
        df['Anlg #3'] = df['Anlg #3'] - df['Anlg #4']
        df.rename(columns={'Anlg #3': 'Radiator DeltaT (F)'}, inplace=True)
        df = df.drop('Anlg #4', axis=1)

    # Linearize Anlg #6 and rename to O2 (lambda)
    if 'Anlg #6' in df.columns:
        df['Anlg #6'] = (df['Anlg #6'] * 0.14) + 0.58
        df.rename(columns={'Anlg #6': 'O2 (lambda)'}, inplace=True)

    return df

def fixbad(df, columns):
    for column in columns:
        if column in df.columns:
            df[column] = df[column] / 1.954
    return df


def plot(df, x, columns, title=None):
    for column in columns:
        if (not column in df.columns):
            print("Column", column, "not found in data")
            return
    df.plot(x=x, y=columns)
    plt.title(title)
    plt.show()

for filename in os.listdir(DIRECTORY):
    print("Processing", filename)
    df = pd.read_csv(f"{DIRECTORY}{filename}", encoding="latin1")
    df = clean(df)
    df = fixbad(df, ['Anlg #1', 'Anlg #2', 'Anlg #3', 'Anlg #4', 'Anlg #5','Anlg #6','Anlg #7','Anlg #8'])
    df = linearize(df)
    # print(f"{df.describe().transpose()}\n\n")
    # plot(df,'Time (sec)' , ['Anlg #1','Anlg #2','Anlg #3','Anlg #4','Anlg #5','Anlg #6','Anlg #7','Anlg #8'], title=filename)
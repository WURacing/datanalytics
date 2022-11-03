import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

try:
    I_DIRECTORY = sys.argv[1]
    O_DIRECTORY = None
    if len(sys.argv) > 2:
        O_DIRECTORY = sys.argv[2]
except:
    print("Usage: python datanalytics.py <input directory> <output directory>")
    exit()

# Cleans csv file that PE3 outputs
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

# Linearizes iColumn and renames to iColumn
def linearize(df, iColumn, oColumn, m, b=0):
    if iColumn in df.columns:
        df[iColumn] = (df[iColumn] * m) + b
        df.rename(columns={iColumn: oColumn}, inplace=True)
    return df

# For data that was collected before PE3 config was fixed
def fixbad(df, columns):
    for column in columns:
        if column in df.columns:
            df[column] = df[column] / 1.954
    return df

# Plot columns on x
def plot(df, x, columns, title=None):
    for column in columns:
        if (not column in df.columns):
            print("Column", column, "not found in data")
            return
    df.plot(x=x, y=columns)
    plt.title(title)
    plt.show()

def export(df, filename):
    df.to_csv(filename)

for filename in os.listdir(I_DIRECTORY):
    print("Processing", filename)
    df = pd.read_csv(f"{I_DIRECTORY}{filename}", encoding="latin1")
    df = clean(df)
    # df = fixbad(df, ['Anlg #1', 'Anlg #2', 'Anlg #3', 'Anlg #4', 'Anlg #5','Anlg #6','Anlg #7','Anlg #8'])
    df = linearize(df, 'Anlg #1', 'Oil Pressure (psi)', 20)
    df = linearize(df, 'Anlg #2', '-X Acceleration (g)', 2.5, -6.25)
    df = linearize(df, 'Anlg #3', 'Radiator Front (deg C)', -72.7859, 190.956)
    df = linearize(df, 'Anlg #4', 'Radiator Rear (deg C)', -72.7859, 190.956)
    df = linearize(df, 'Anlg #6', 'O2 (lambda)', 0.14, 0.58)
    df = linearize(df, 'Anlg #7', 'Gear Position (V)', 1)
    print(f"{df.describe().transpose()}\n\n")
    # plot(df,'Time (sec)' , ['O2 (lambda)'], title=filename)
    if O_DIRECTORY:
        export(df, f"{O_DIRECTORY}{filename}")

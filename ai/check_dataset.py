import pandas as pd
import os

folder = r"D:\Downloads\dataset"

files = os.listdir(folder)

print("FILES:")
print(files)

first_file = os.path.join(folder, files[0])

df = pd.read_csv(first_file, nrows=1000)

print("\nCOLUMNS:")
print(df.columns.tolist())

print("\nTOTAL COLUMNS:")
print(len(df.columns))

if "Label" in df.columns:
    print("\nLABELS:")
    print(df["Label"].value_counts())
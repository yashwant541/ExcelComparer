import os
import pandas as pd

def read_file(file_path):
    try:
        # Read data file with any extension
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def compare_files(file1_path, file2_path):
    # Read files into Pandas DataFrames
    file1_df = read_file(file1_path)
    file2_df = read_file(file2_path)

    if file1_df is None or file2_df is None:
        return

    # 1. Finding row duplicates
    duplicates_file1 = file1_df.duplicated().sum()
    duplicates_file2 = file2_df.duplicated().sum()

    print(f"Number of row duplicates in File 1: {duplicates_file1}")
    print(f"Number of row duplicates in File 2: {duplicates_file2}")

    # 2. Find rows which are in File1 but not in File2
    file1_not_in_file2 = file1_df[~file1_df.isin(file2_df)].dropna()

    # 3. Find rows which are in File2 but not in File1
    file2_not_in_file1 = file2_df[~file2_df.isin(file1_df)].dropna()

    # Save results to new CSV files with modified names
    file1_name, file1_extension = os.path.splitext(os.path.basename(file1_path))
    file2_name, file2_extension = os.path.splitext(os.path.basename(file2_path))

    file1_not_in_file2.to_csv(os.path.join(os.path.dirname(file1_path), f"{file1_name}_not_in_{file2_name}_dummy.csv"), index=False)
    file2_not_in_file1.to_csv(os.path.join(os.path.dirname(file2_path), f"{file2_name}_not_in_{file1_name}_dummy.csv"), index=False)

if __name__ == "__main__":
    # Replace 'path/to/folder1' and 'path/to/folder2' with the actual paths of your input folders
    folder1_path = 'path/to/folder1'
    folder2_path = 'path/to/folder2'

    # Assuming there is one file in each folder
    files_in_folder1 = os.listdir(folder1_path)
    files_in_folder2 = os.listdir(folder2_path)

    if len(files_in_folder1) == 1 and len(files_in_folder2) == 1:
        file1_path = os.path.join(folder1_path, files_in_folder1[0])
        file2_path = os.path.join(folder2_path, files_in_folder2[0])

        compare_files(file1_path, file2_path)
    else:
        print("Each folder should contain exactly one file for comparison.")

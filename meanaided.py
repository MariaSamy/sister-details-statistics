import pandas as pd
import numpy as np
import json
import os

def clean_data(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No such file or directory: '{file_path}'")

        print(f"Loading data from {file_path}...")
        # Load the Excel file
        df = pd.read_excel(file_path, sheet_name='Sheet1 (2)', engine='xlrd')

        # Standardize column names
        columns = [
            "Serial Number", "A.Number", "Name (Congregation)", "Name (Certificate)", 
            "DOB", "DOA", "Date of Retirement", "Qualification", "Major Subject", 
            "Designation", "School Name", "Funding Type", "Convent", "Mobile Number"
        ]
        df.columns = columns

        print("Cleaning data...")
        # Drop the first few rows that do not contain data
        df = df.iloc[4:].reset_index(drop=True)

        # Drop rows where all elements are NaN
        df.dropna(how='all', inplace=True)

        # Convert dates to proper datetime format
        df["DOB"] = pd.to_datetime(df["DOB"], errors='coerce', format='%d/%m/%Y')
        df["DOA"] = pd.to_datetime(df["DOA"], errors='coerce', format='%d/%m/%Y')
        df["Date of Retirement"] = pd.to_datetime(df["Date of Retirement"], errors='coerce', format='%d/%m/%Y')

        print("Data cleaned successfully.")
        return df
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def calculate_statistics(df):
    print("Calculating statistics...")
    # Calculate age
    df['Age'] = (pd.Timestamp.now() - df['DOB']).astype('<m8[Y]')
    
    # Calculate years of service
    df['Years of Service'] = (pd.Timestamp.now() - df['DOA']).astype('<m8[Y]')

    # Summary statistics for Age
    age_stats = {
        'Mean Age': np.mean(df['Age']),
        'Median Age': np.median(df['Age']),
        'Mode Age': df['Age'].mode()[0],
        'Standard Deviation Age': np.std(df['Age'])
    }

    # Summary statistics for Years of Service
    service_stats = {
        'Mean Years of Service': np.mean(df['Years of Service']),
        'Median Years of Service': np.median(df['Years of Service']),
        'Mode Years of Service': df['Years of Service'].mode()[0],
        'Standard Deviation Years of Service': np.std(df['Years of Service'])
    }

    print("Statistics calculated successfully.")
    return {'Age Statistics': age_stats, 'Years of Service Statistics': service_stats}

def save_statistics_to_json(statistics, output_file):
    try:
        with open(output_file, 'w') as f:
            json.dump(statistics, f, indent=4)
        print(f"Statistics saved to: {output_file}")
    except Exception as e:
        print(f"Failed to save statistics: {e}")

# Example usage
file_path = r'D:\Software\aided\Infant Jesus Province Sister details.xls'  # Ensure this path is correct
df = clean_data(file_path)

if df is not None:
    statistics = calculate_statistics(df)
    save_statistics_to_json(statistics, 'statistics.json')
    print("Statistics saved to: statistics.json")
else:
    print("Failed to clean the data.")

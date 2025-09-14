"""
Medical Insurance Dataset - Data Loading and Cleaning Module
============================================================

This module handles data loading, cleaning, and preprocessing for the medical insurance analysis.
Author: Data Analysis System
Date: Sepetember 2025
"""

import pandas as pd
import numpy as np
import requests
import warnings
warnings.filterwarnings('ignore')

class MedicalInsuranceDataLoader:
    """
    A class to handle loading and cleaning of medical insurance data.
    """

    def __init__(self, url=None, local_path=None):
        """
        Initialize the data loader.

        Parameters:
        url (str): URL to download the dataset
        local_path (str): Local path to the dataset file
        """
        self.url = url
        self.local_path = local_path
        self.df_raw = None
        self.df_clean = None
        self.label_mappings = {
            'sex': {1: 'male', 2: 'female'},
            'smoker': {0: 'no', 1: 'yes'},
            'region': {1: 'northeast', 2: 'northwest', 3: 'southeast', 4: 'southwest'}
        }

    def download_data(self, save_path='/tmp/medical_insurance.csv'):
        """
        Download the dataset from URL.

        Parameters:
        save_path (str): Path to save the downloaded file

        Returns:
        bool: True if successful, False otherwise
        """
        if not self.url:
            print("❌ No URL provided")
            return False

        try:
            print(f"📥 Downloading data from: {self.url}")
            response = requests.get(self.url)
            response.raise_for_status()

            with open(save_path, 'wb') as f:
                f.write(response.content)

            self.local_path = save_path
            file_size = len(response.content)
            print(f"✅ Downloaded successfully: {file_size:,} bytes")
            return True

        except Exception as e:
            print(f"❌ Download failed: {e}")
            return False

    def load_data(self):
        """
        Load the dataset from local file.

        Returns:
        pd.DataFrame: Raw dataset
        """
        if not self.local_path:
            print("❌ No local path specified")
            return None

        try:
            # Check if file has header
            with open(self.local_path, 'r') as f:
                first_line = f.readline().strip()

            contains_numbers = any(char.isdigit() for char in first_line)

            if contains_numbers:
                # No header, add column names
                column_names = ['age', 'sex', 'bmi', 'children', 'smoker', 'region', 'charges']
                self.df_raw = pd.read_csv(self.local_path, names=column_names)
                print(f"✅ Loaded data with inferred columns: {column_names}")
            else:
                # Has header
                self.df_raw = pd.read_csv(self.local_path)
                print(f"✅ Loaded data with existing columns: {list(self.df_raw.columns)}")

            print(f"📊 Dataset shape: {self.df_raw.shape}")
            return self.df_raw

        except Exception as e:
            print(f"❌ Loading failed: {e}")
            return None

    def clean_data(self):
        """
        Clean and preprocess the dataset.

        Returns:
        pd.DataFrame: Cleaned dataset
        """
        if self.df_raw is None:
            print("❌ No raw data available. Load data first.")
            return None

        print("🧹 Starting data cleaning...")
        self.df_clean = self.df_raw.copy()

        # Clean age column
        print("  • Cleaning age column...")
        self.df_clean['age'] = pd.to_numeric(self.df_clean['age'], errors='coerce')
        age_missing = self.df_clean['age'].isnull().sum()
        if age_missing > 0:
            age_median = self.df_clean['age'].median()
            self.df_clean['age'] = self.df_clean['age'].fillna(age_median)
            print(f"    Filled {age_missing} missing values with median: {age_median}")

        # Clean smoker column
        print("  • Cleaning smoker column...")
        smoker_mode = self.df_clean['smoker'].mode()[0] if '?' not in str(self.df_clean['smoker'].mode().values) else '0'
        self.df_clean['smoker'] = self.df_clean['smoker'].replace('?', smoker_mode)
        self.df_clean['smoker'] = pd.to_numeric(self.df_clean['smoker'])

        # Convert data types
        print("  • Converting data types...")
        self.df_clean['age'] = self.df_clean['age'].astype(int)
        self.df_clean['sex'] = self.df_clean['sex'].astype(int)
        self.df_clean['children'] = self.df_clean['children'].astype(int)
        self.df_clean['smoker'] = self.df_clean['smoker'].astype(int)
        self.df_clean['region'] = self.df_clean['region'].astype(int)

        print(f"✅ Cleaning complete. Missing values: {self.df_clean.isnull().sum().sum()}")
        return self.df_clean

    def create_labeled_data(self):
        """
        Create a labeled version with human-readable categories.

        Returns:
        pd.DataFrame: Labeled dataset
        """
        if self.df_clean is None:
            print("❌ No clean data available. Clean data first.")
            return None

        df_labeled = self.df_clean.copy()
        df_labeled['sex_label'] = df_labeled['sex'].map(self.label_mappings['sex'])
        df_labeled['smoker_label'] = df_labeled['smoker'].map(self.label_mappings['smoker'])
        df_labeled['region_label'] = df_labeled['region'].map(self.label_mappings['region'])

        return df_labeled

    def get_data_summary(self):
        """
        Get a summary of the dataset.

        Returns:
        dict: Summary statistics
        """
        if self.df_clean is None:
            return {"error": "No clean data available"}

        return {
            "shape": self.df_clean.shape,
            "columns": list(self.df_clean.columns),
            "missing_values": self.df_clean.isnull().sum().to_dict(),
            "data_types": self.df_clean.dtypes.to_dict(),
            "memory_usage_kb": self.df_clean.memory_usage(deep=True).sum() / 1024
        }

# Example usage
if __name__ == "__main__":
    # Initialize loader
    loader = MedicalInsuranceDataLoader(
        url="https://github.com/Achref-ka/Medical-Insurance-Cost/blob/main/Medical-Insurance.csv?raw=true"
    )

    # Download and load data
    if loader.download_data():
        raw_data = loader.load_data()
        clean_data = loader.clean_data()
        labeled_data = loader.create_labeled_data()

        print("\nData Summary:")
        summary = loader.get_data_summary()
        for key, value in summary.items():
            print(f"  {key}: {value}")

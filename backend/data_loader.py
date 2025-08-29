import os
import pandas as pd
from pathlib import Path
VALID_EXTS = ('.csv', '.xls', '.xlsx')
def get_dataset_files(data_dir=None):
    data_dir = data_dir or Path(__file__).parents[1] / 'data'
    data_dir = Path(data_dir)
    if not data_dir.exists():
        return []
    return [f.name for f in data_dir.iterdir() if f.suffix.lower() in VALID_EXTS]
def load_all_datasets(data_dir=None):
    data_dir = data_dir or Path(__file__).parents[1] / 'data'
    data_dir = Path(data_dir)
    dataframes = {}
    for file in get_dataset_files(data_dir):
        file_path = data_dir / file
        try:
            if file_path.suffix.lower() == '.csv':
                df = pd.read_csv(file_path)
                dataframes[file] = df
            else:
                sheets = pd.read_excel(file_path, sheet_name=None)
                if isinstance(sheets, dict):
                    for sheet_name, sheet_df in sheets.items():
                        key = f"{file}::{sheet_name}"
                        dataframes[key] = sheet_df
                else:
                    dataframes[file] = sheets
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    return dataframes

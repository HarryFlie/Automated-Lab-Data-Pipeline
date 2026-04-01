import os
import shutil
import sqlite3
import pandas as pd
from datetime import datetime

# Define Paths
LOCAL_FOLDER = "Local_Lab_PC"
SERVER_FOLDER = "Central_Server"
ARCHIVE_FOLDER = os.path.join(SERVER_FOLDER, "Archived_CSVs")
DB_PATH = os.path.join(SERVER_FOLDER, "DataLake.db")

# Ensure server folders exist
os.makedirs(SERVER_FOLDER, exist_ok=True)
os.makedirs(ARCHIVE_FOLDER, exist_ok=True)

def initialize_database():
    """Simulates establishing a centralized Data Lake architecture."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS experimental_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Timestamp TEXT,
            Temperature_C REAL,
            Pressure_atm REAL,
            Source_File TEXT,
            Upload_Time TEXT
        )
    ''')
    conn.commit()
    return conn

def process_data_pipeline():
    # Check if there are any files in the local lab PC folder
    for file_name in os.listdir(LOCAL_FOLDER):
        if file_name.endswith('.csv'):
            local_file_path = os.path.join(LOCAL_FOLDER, file_name)
            
            # 1. READ DATA (Using Pandas)
            df = pd.read_csv(local_file_path)
            
            # 2. METADATA TAGGING (Adding traceablity for ALCOA+)
            timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_file_name = f"Processed_{timestamp_str}_{file_name}"
            df['Source_File'] = new_file_name
            df['Upload_Time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 3. DATA LAKE INTEGRATION (Insert into SQLite)
            conn = initialize_database()
            df.to_sql('experimental_data', conn, if_exists='append', index=False)
            conn.close()
            print(f"📊 Data from {file_name} securely ingested into Data Lake.")
            
            # 4. DATA PATH AUTOMATION (Move and Rename file)
            server_file_path = os.path.join(ARCHIVE_FOLDER, new_file_name)
            shutil.move(local_file_path, server_file_path)
            print(f"📁 File renamed to {new_file_name} and moved to Central Server Archive.\n")

if __name__ == "__main__":
    print("🚀 Initiating Automated Data Pipeline...")
    process_data_pipeline()
    print("✅ Pipeline execution complete.")
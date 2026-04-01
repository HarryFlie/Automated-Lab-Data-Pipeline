import csv
import random
import os
from datetime import datetime

# Path to the simulated local lab computer
LOCAL_FOLDER = "Local_Lab_PC"
FILE_NAME = "sensor_data.csv"
FILE_PATH = os.path.join(LOCAL_FOLDER, FILE_NAME)

def generate_lab_data():
    # Ensure folder exists
    os.makedirs(LOCAL_FOLDER, exist_ok=True)
    
    # Generate fake biosensor data (Timestamp, Temperature, Pressure)
    data = []
    for _ in range(10):  # Simulate 10 readings per test
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        temp = round(random.uniform(20.0, 25.0), 2)
        pressure = round(random.uniform(1.0, 1.5), 3)
        data.append([timestamp, temp, pressure])
    
    # Write to CSV
    with open(FILE_PATH, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Temperature_C", "Pressure_atm"])
        writer.writerows(data)
        
    print(f"✅ Success: Lab equipment generated raw data at {FILE_PATH}")

if __name__ == "__main__":
    generate_lab_data()
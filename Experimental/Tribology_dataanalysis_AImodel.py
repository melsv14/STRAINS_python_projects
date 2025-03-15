import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Define the base data path
data_path = r'F:\Documents\Personal development\Master\Courses\Experimental mechanics\Labwork\Tribology tests\Data\csv'

# List of files in the data path
files_names = ['test1_21112023_16-02-22.csv', 'test2_21112023_16-21-24.csv', 'test3_21112023_17-03-25.csv', 'test3c_21112023_17-38-26.csv', 'test4_21112023_18-03-37.csv', 'test5_21112023_18-14-09.csv', 'test6_21112023_18-31-41.csv']

# Initialize an empty list to store individual DataFrames
data_frames = []

# Iterate over each file
for file_name in files_names:
    # Construct the full path to the file
    file_path = os.path.join(data_path, file_name)

    # Read the CSV file into a DataFrame
    data_pd = pd.read_csv(file_path)

    # Get the sample number from the file name
    sample_no = file_name.replace('.csv', '')

    # Append the sample number as a column to the DataFrame
    data_pd['Sample'] = sample_no

    # Append the DataFrame to the list
    data_frames.append(data_pd)

# Concatenate the list of DataFrames into one
combined_data = pd.concat(data_frames, ignore_index=True)

# Preprocess the combined data (you may need to customize this based on your data)
combined_data['Time'] = pd.to_numeric(combined_data['Time'], errors='coerce')  # Convert Time to numeric
combined_data.dropna(subset=['Time', 'Fn', 'Ft'], inplace=True)  # Drop rows with missing values

# Extract features (you may need to customize this based on your observations)
combined_data['Fn_change'] = combined_data['Fn'].diff()
combined_data['Ft_change'] = combined_data['Ft'].diff()

# Assuming vibrations can be captured by changes in Fn and Ft
combined_data['Vibration'] = np.abs(combined_data['Fn_change']) > 5  # Adjust the threshold as needed

# Display the preprocessed data
print(combined_data.head())

# Save the preprocessed data to a CSV file for manual labeling
combined_data.to_csv('preprocessed_data.csv', index=False)

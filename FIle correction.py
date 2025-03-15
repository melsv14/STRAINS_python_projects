import os
import pandas as pd

# Define the base data path
data_path = r'F:\Documents\Personal development\Master\Courses\Experimental mechanics\Labwork\Tribology tests\Data\csv'
output_folder = 'data_corrected'

# Create the output folder if it doesn't exist
output_path = os.path.join(data_path, output_folder)
os.makedirs(output_path, exist_ok=True)

files_names = ['test2_21112023_16-21-24.csv', 'test2_21112023_16-59-19.csv']

for i in files_names:
    file_path = os.path.join(data_path, i)
    data_pd = pd.read_csv(file_path, header=None, names=['Data'])  # Read data into a single column

    # Check if the data needs to be separated (contains ';')
    if ';' in data_pd['Data'].iloc[0]:
        # Split the single column into multiple columns using the predefined delimiter ';'
        separated_data = data_pd['Data'].str.split(';', expand=True)

        # Check if the first row contains headers
        if not any(separated_data.iloc[0].str.isnumeric()):
            # Rename columns if needed
            separated_data.columns = ["No", "Time", "Fn", "Ft"]

        # Convert columns to numeric (if needed)
        separated_data = separated_data.apply(pd.to_numeric, errors='ignore')

        # Save the converted data to a new CSV file in the "data_corrected" folder
        output_file_path = os.path.join(output_path, i.replace('.csv', '_corrected.csv'))
        separated_data.to_csv(output_file_path, index=False, header=False)  # Skip adding headers

# Display a message indicating successful conversion
print(f"Converted files saved in '{output_path}'")

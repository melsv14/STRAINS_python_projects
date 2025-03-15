import os
import matplotlib.pyplot as plt
import pandas as pd

# Define the base data path
data_path = r'F:\Documents\Personal development\Master\Courses\Experimental mechanics\Labwork\Tribology tests\Data\csv'

# List of files in the data path
files_names = files_names = ['test1_21112023_16-02-22.csv', 'test2_21112023_16-21-24.csv', 'test3_21112023_17-03-25.csv', 'test3c_21112023_17-38-26.csv', 'test4_21112023_18-03-37.csv', 'test5_21112023_18-14-09.csv', 'test6_21112023_18-31-41.csv']

# Iterate over each file
for file_name in files_names:
    # Construct the full path to the file
    file_path = os.path.join(data_path, file_name)

    # Read the CSV file into a DataFrame
    data_pd = pd.read_csv(file_path)

    # Get the sample number from the file name
    sample_no = file_name.replace('.csv', '')

    # Plot Fn - Time in the longitudinal direction from the raw data
    plt.figure(figsize=(10, 5))
    plt.plot(data_pd['Time'], data_pd['Fn'])
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.grid()
    plt.title(f'Test {sample_no}: Normal force')

    # Plot Ft - Time in the transversal direction from the raw data
    plt.figure(figsize=(10, 5))
    plt.plot(data_pd['Time'], data_pd['Ft'])
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.grid()
    plt.title(f'Test {sample_no}: Tangent force')

    # Calculate friction coefficient u = Ft / Fn
    u = data_pd['Ft'] / data_pd['Fn']

    # Plotting evolution of 'u' against 'Time'
    plt.figure(figsize=(10, 5))
    plt.plot(data_pd['Time'], u, label=sample_no)
    plt.xlabel('Time (s)')
    plt.ylabel('Friction Coefficient')
    plt.title(f'Test {sample_no}: Friction Coefficient')
    plt.legend()

    # Display all figures for the current test
    plt.show()

    # Close all figures before moving to the next test
    plt.close('all')
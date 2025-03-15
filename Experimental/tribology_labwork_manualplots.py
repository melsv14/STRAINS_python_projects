import os
import matplotlib.pyplot as plt
import pandas as pd

# Define the base data path
data_path = r'F:\Documents\Personal development\Master\Courses\Experimental mechanics\Labwork\Tribology tests\Data\csv'

# List of files in the data path
files_names = ['test6_21112023_18-31-41.csv']

# Iterate over each file
for file_name in files_names:
    # Construct the full path to the file
    file_path = os.path.join(data_path, file_name)

    # Read the CSV file into a DataFrame
    data_pd = pd.read_csv(file_path)

    # Get the sample number from the file name
    sample_no = file_name.replace('.csv', '')

    # Define the start and stop times for plotting (modify these as needed)
    start_time = 190
    stop_time = 368

    # Filter data based on the specified time range
    filtered_data = data_pd[(data_pd['Time'] >= start_time) & (data_pd['Time'] <= stop_time)]

    # Plot Fn - Time in the longitudinal direction from the filtered data
    plt.figure(figsize=(10, 5))
    plt.plot(filtered_data['Time'], filtered_data['Fn'])
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.grid()
    plt.title(f'Test {sample_no}: Normal force ({start_time}s to {stop_time}s)')

    # Plot Ft - Time in the transversal direction from the filtered data
    plt.figure(figsize=(10, 5))
    plt.plot(filtered_data['Time'], filtered_data['Ft'])
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.grid()
    plt.title(f'Test {sample_no}: Tangent force ({start_time}s to {stop_time}s)')

    # Calculate friction coefficient u = Ft / Fn
    u = filtered_data['Ft'] / filtered_data['Fn']

    # Plotting evolution of 'u' against 'Time'
    plt.figure(figsize=(10, 5))
    plt.plot(filtered_data['Time'], u, label=sample_no)
    plt.xlabel('Time (s)')
    plt.ylabel('Friction Coefficient')
    plt.title(f'Test {sample_no}: Friction Coefficient ({start_time}s to {stop_time}s)')
    plt.legend()

    # Calculate and display the average value of 'u'
    average_u = u.mean()
    print(f"Average value of 'u' between {start_time}s and {stop_time}s: {average_u}")

    # Display all figures for the current test
    plt.show()

    # Close all figures before moving to the next test
    plt.close('all')

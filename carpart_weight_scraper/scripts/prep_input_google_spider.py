""" 
Prepare input data for Google Spider, from data scraped by Tiger Spider (seperate project). 
Extract partslink numbers from car parts data file and save to CSV file.
"""
import os
import pandas as pd

# file names and paths
data_directory_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data/in/')
data_input_file_path =  data_directory_path + 'parts_data.csv'
data_output_file_path = data_directory_path + 'partslink_numbers.csv'

# check if car parts data file exists
if not os.path.exists(data_input_file_path):
    raise FileNotFoundError("Input data file not found at: " + data_input_file_path)

# get SKUs from car parts data file
df = pd.read_csv(data_input_file_path, usecols=['SKU'])

# delete duplicates
df.drop_duplicates(inplace=True)

# save the partslink numbers to a CSV file, without the index or header
df.to_csv(data_output_file_path, index=False, header=False)

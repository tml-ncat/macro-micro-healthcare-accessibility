#!/usr/bin/env python3
import geopandas
import r5py
import numpy as np
import shapely
import pandas as pd
pd.set_option('display.max_columns', None)
import folium
import folium.plugins
import matplotlib.pyplot as plt
import datetime
import os
import time
import random
import osmnx as ox
import warnings
import networkx as nx
import argparse
import re
import sys

def create_aggregated_file(county_name):
    # Define the folder path
    folder_path = f'./county_data/{county_name}/'

    # Step 1: Read "Option1_county_centroids.csv" into DF dataframe
    centroids_file = os.path.join(folder_path, 'Option1_county_centroids.csv')
    DF = pd.read_csv(centroids_file)

    # Step 2: Initialize a dictionary to store merged dataframes
    merged_dfs = {}

    # List of Option prefixes to process
    option_prefixes = ['Option1_aggregated_', 'Option2_aggregated_', 'Option3_aggregated_']

    # Step 3: Iterate over each option prefix
    for prefix in option_prefixes:
        # Find matching file in folder
        option_files = [file for file in os.listdir(folder_path) if file.startswith(prefix) and file.endswith('.csv')]
        
        # Check if file exists
        if len(option_files) > 0:
            # Take the first matching file (assuming there is only one)
            option_file_path = os.path.join(folder_path, option_files[0])
            
            # Read the file into a dataframe
            option_df = pd.read_csv(option_file_path)
            
            if prefix == 'Option3_aggregated_':
                # Create a new column with quotient of 'to_id' divided by 10000
                option_df['new_column'] = (option_df['to_id'] / 10000).astype(int)
                
                # Merge based on 'new_column' and 'poly_idx'
                merged_df = pd.merge(option_df, DF, left_on='new_column', right_on='poly_idx', how='inner')
                
                # Group by 'poly_idx' and aggregate 'min_travel_time' into a list
                grouped = merged_df.groupby('poly_idx')['min_travel_time'].apply(list).reset_index()
                
                # Merge based on 'poly_idx'
                DF = DF.merge(grouped, on='poly_idx', how='left')
                
                # Rename the merged column appropriately
                DF.rename(columns={'min_travel_time': f'{prefix}min_travel_time_list'}, inplace=True)
            else:
                # Merge based on 'to_id' and 'poly_idx' columns
                DF = DF.merge(option_df[['to_id', 'min_travel_time']], left_on='poly_idx', right_on='to_id', how='left')
                
                # Rename the merged column appropriately
                DF.rename(columns={'min_travel_time': f'{prefix}min_travel_time'}, inplace=True)

    # Step 4: Store DF with added columns in a separate dataframe
    DF_with_additional_columns = DF.copy()
    print(DF_with_additional_columns)
    csv_file_path = os.path.join(folder_path, 'customized_combined_output_BEFORE.csv')  # Replace with your desired file path
    DF_with_additional_columns.to_csv(csv_file_path, index=False)

    print(f"DataFrame DF has been successfully exported to {csv_file_path}.")

    # Step 5: Proceed with further processing or analysis with DF_with_additional_columns
    # Function to pick top x values and calculate average and median
    # Function to pick top x highest values and calculate statistics
    def pick_top_x_and_stats(row):
        min_travel_times = row['Option3_aggregated_min_travel_time_list']
        x = row['E_NOVEH']
        
        # Sort in descending order and pick the top x values
        sorted_min_travel_times = sorted(min_travel_times, reverse=True)
        
        if len(sorted_min_travel_times) >= x and x>0:
            top_x_values = sorted_min_travel_times[:x]
            
            # Calculate statistics
            min_value = np.min(top_x_values)
            max_value = np.max(top_x_values)
            avg_value = np.mean(top_x_values)
            median_value = np.median(top_x_values)
            range_value = max_value - min_value
            std_deviation = np.std(top_x_values)
            
            return pd.Series({
                'top_x_values': top_x_values,
                'min_top_x': min_value,
                'max_top_x': max_value,
                'avg_top_x': avg_value,
                'median_top_x': median_value,
                'range_top_x': range_value,
                'std_dev_top_x': std_deviation,
                'num_parcels': len(sorted_min_travel_times)
            })
        else:
            return pd.Series({
                'top_x_values': [],
                'min_top_x': np.nan,
                'max_top_x': np.nan,
                'avg_top_x': np.nan,
                'median_top_x': np.nan,
                'range_top_x': np.nan,
                'std_dev_top_x': np.nan,
                'num_parcels': len(sorted_min_travel_times)
            })

    # Apply function to pick top x values and calculate stats
    result_df = DF_with_additional_columns.apply(pick_top_x_and_stats, axis=1)

    # Concatenate the result_df with DF
    DF_with_additional_columns = pd.concat([DF_with_additional_columns, result_df], axis=1)
    DF_with_additional_columns["AbsOption1Minus3"] = (DF_with_additional_columns["avg_top_x"]-DF_with_additional_columns["Option1_aggregated_min_travel_time"]).apply(abs)
    DF_with_additional_columns["AbsOption2Minus3"] = (DF_with_additional_columns["avg_top_x"]-DF_with_additional_columns["Option2_aggregated_min_travel_time"]).apply(abs)
    # print(DF_with_additional_columns)
    csv_file_path = os.path.join(folder_path, 'customized_combined_output.csv')  # Replace with your desired file path
    DF_with_additional_columns.to_csv(csv_file_path, index=False)

    print(f"DataFrame DF has been successfully exported to {csv_file_path}.")
    

if __name__=='__main__':
    #arg parser
    parser = argparse.ArgumentParser(description="A script that uses county name.")
    parser.add_argument("--county_name", type=str, required=True, 
                        help="Name of the county")
    args = parser.parse_args()
    # Convert county_name to have first letter capital and rest lowercase
    county_name = args.county_name.capitalize()
    # download_guilford_map_sp()
    create_aggregated_file(county_name)


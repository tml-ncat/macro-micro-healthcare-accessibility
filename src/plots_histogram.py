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

def plot_histogram(county_name, agg_filename):
    # travel_times = pd.read_csv('travel_times_181916parcels_to_6hospitals_1719917624.csv')
    result = pd.read_csv(f'county_data/{county_name}/{agg_filename}.csv')
    # Extract Option # using regular expressions
    match = re.search(r'Option(\d+)_', agg_filename)
    if match:
        x_value = match.group(1)
        print(f"The value of Option extracted from '{agg_filename}' is: {x_value}")
    else:
        print(f"No match found in '{agg_filename}'")
        sys.exit(1)
    
    print("Descriptive statistics are")
    print(result.columns.tolist())
    print(result[['min_travel_time','second_min_travel_time','third_min_travel_time','median_travel_time']].describe())

    # result = travel_times.groupby('to_id')['travel_time'].agg([
    #         ('min_travel_time', 'min'),
    #         ('second_min_travel_time', lambda x: x.nsmallest(2).iloc[-1] if len(x) >= 2 else None),
    #         ('third_min_travel_time', lambda x: x.nsmallest(3).iloc[-1] if len(x) >= 3 else None),
    #         ('median_travel_time', 'median'),
    #         ('average_travel_time', 'mean'),
    #         ('q1_travel_time', lambda x: x.quantile(0.25)),  # 25th percentile
    #         ('q3_travel_time', lambda x: x.quantile(0.75))   # 75th percentile
    #     ]).reset_index()

    # print(result)
    # filename = "aggregated_parNo.csv"
    # # Export the DataFrame to CSV with the unique filename
    # result.to_csv(filename, index=False)

    # Plot the histogram for the "average" column
    plt.figure(figsize=(10, 6))

    # Calculate the range of the data and create bins
    min_val = result['min_travel_time'].min()
    max_val = result['median_travel_time'].max()
    bins = np.arange(0, np.ceil(max_val) + 5, 5)

    plt.hist(result['min_travel_time'], bins=bins, edgecolor='black', alpha=0.7)
    plt.title('Histogram of Minimum Travel Times', fontsize=16)  # Set title font size
    plt.xlabel('Minimum Travel Time', fontsize=14)  # Set x-axis label font size
    plt.ylabel('Frequency', fontsize=14)  # Set y-axis label font size
    plt.grid(True)
    # Save plot to PDF file
    plt.savefig(f'county_data/{county_name}/Option{x_value}_histogram_min_travel_time.pdf')
    # Show plot (optional, comment out if only exporting to PDF)
    plt.show()

    plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
    plt.hist(result['median_travel_time'], bins=bins, edgecolor='black', alpha=0.7)
    plt.title('Histogram of Median Travel Times')
    plt.xlabel('Median Travel Time', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.grid(True)
    plt.savefig(f'county_data/{county_name}/Option{x_value}_histogram_median_travel_time.pdf')
    # Show plot (optional, comment out if only exporting to PDF)
    plt.show()

if __name__=='__main__':
    #arg parser
    parser = argparse.ArgumentParser(description="A script that uses county name.")
    parser.add_argument("--county_name", type=str, required=True, 
                        help="Name of the county")
    parser.add_argument("--file_name", type=str, required=True, 
                        help="Aggregated TT file name (without csv)")
    args = parser.parse_args()
    # Convert county_name to have first letter capital and rest lowercase
    county_name = args.county_name.capitalize()
    # download_guilford_map_sp()
    plot_histogram(county_name,  args.file_name)


#!/usr/bin/env python3
import pandas as pd
import glob
import os

def combine_travel_time_results(county_name):
    """
    Combines Option 1, 2, and 3 aggregated results into a single file
    for box plot visualization.
    """
    folder = f'county_data/{county_name}/'
    
    # Find the most recent aggregated files for each option
    option1_files = sorted(glob.glob(f'{folder}Option1_aggregated_*.csv'))
    option2_files = sorted(glob.glob(f'{folder}Option2_aggregated_*.csv'))
    option3_files = sorted(glob.glob(f'{folder}Option3_aggregated_*.csv'))
    
    if not option1_files or not option2_files or not option3_files:
        print(f"Missing aggregated files for {county_name}!")
        print(f"Option 1 files: {len(option1_files)}")
        print(f"Option 2 files: {len(option2_files)}")
        print(f"Option 3 files: {len(option3_files)}")
        return None
    
    # Read the most recent file for each option
    df1 = pd.read_csv(option1_files[-1])
    df2 = pd.read_csv(option2_files[-1])
    df3 = pd.read_csv(option3_files[-1])
    
    # Rename columns to match expected format
    df1 = df1.rename(columns={'min_travel_time': 'Option1_aggregated_min_travel_time'})
    df2 = df2.rename(columns={'min_travel_time': 'Option2_aggregated_min_travel_time'})
    
    # For Option 3, calculate average and worst-case scenarios
    df3['avg_all_parcel'] = df3['min_travel_time']  # Average of all parcels
    df3['avg_top_x'] = df3[['min_travel_time', 'second_min_travel_time', 'third_min_travel_time']].mean(axis=1)  # Worst case (top 3)
    
    # Merge all together (assuming same tract IDs)
    combined = pd.DataFrame({
        'Option1_aggregated_min_travel_time': df1['Option1_aggregated_min_travel_time'],
        'Option2_aggregated_min_travel_time': df2['Option2_aggregated_min_travel_time'],
        'avg_all_parcel': df3['avg_all_parcel'],
        'avg_top_x': df3['avg_top_x']
    })
    
    # Save combined file
    output_file = f'{folder}customized_combined_output_AFTER.csv'
    combined.to_csv(output_file, index=False)
    print(f"✅ Created: {output_file}")
    
    return combined

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--county_name", type=str, required=True)
    args = parser.parse_args()
    
    combine_travel_time_results(args.county_name.capitalize())
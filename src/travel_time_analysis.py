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

def find_tt_matrix(county_name, state_name, option, osm_filename):
    start_time = time.time()
    # Get the directory where the current script is located
    # script_dir = os.path.dirname(os.path.realpath(__file__))
    # # Construct full paths to the GTFS and OSM files
    # gtfs_path = os.path.join(script_dir, 'gtfs.zip')
    # print("GTFS path is ", gtfs_path)
    osm_path = f"state_data/osm/{osm_filename}.osm.pbf"
    # Path to the CSV file
    if option==1:
        file_path = f"county_data/{county_name}/Option1_county_centroids.csv"
        id_col = 'poly_idx'
    elif option==2:
        file_path = f"county_data/{county_name}/Option2_county_centroids.csv"
        id_col = 'county_index'
    else:
        file_path = f"county_data/{county_name}/Option3_residential_parcel_centroids.csv"
        id_col = 'new_index'

    df = pd.read_csv(file_path)
    num_random_points = len(df)
    # Create the list of tuples
    coordinates = list(zip(df['latitude'], df['longitude']))
    # ids = list(zip(df[id_col]))
    ids = [item[0] for item in list(zip(df[id_col]))]
    # print("Intended ids for origins", ids)
    # Create a list of Shapely Point objects
    points = [shapely.Point(lon, lat) for lat, lon in coordinates]
    # Create a GeoDataFrame
    origins = geopandas.GeoDataFrame(
        {
            "id": ids,  #range(1, len(coordinates) + 1),  # Assign IDs to each point
            "geometry": points
        },
        crs="EPSG:4269" #previously 4326
    )
    print(f"=={len(origins)} origins read. Elapsed time {time.time()-start_time} sec since code start.")
    # Path to the CSV file
    file_path = f"county_data/{county_name}/hospitals_within_buffer.csv"
    # Read the CSV file
    df = pd.read_csv(file_path)
    # Create the list of tuples
    coordinates_2 = [(row['latitude'], row['longitude']) for index, row in df.iterrows()]
    # ids = list(zip(df['ID']))
    ids = [item[0] for item in list(zip(df['ID']))]
    # print("Intended ids for destinations", ids)
    points = [shapely.Point(lon, lat) for lat, lon in coordinates_2]
    # dest = shapely.Point(-78.904472, 35.99325)
    destinations = geopandas.GeoDataFrame(
            {
                "id": ids, #range(len(coordinates)+1, len(coordinates)+len(coordinates_2) + 1),
                "geometry": points
            },
            crs="EPSG:4269",
    )
    print(f"=={len(destinations)} destinations read. Elapsed time {time.time()-start_time} sec since code start.")
    # print("origins = ",origins)
    # print("dest = ", destinations)

    transport_network = r5py.TransportNetwork(
        osm_path,
        [
            # gtfs_path,
            # gtfs_path1,
            # gtfs_path3
        ]
    )
    
    travel_time_matrix_computer = r5py.TravelTimeMatrixComputer(
        # transport_network_from_dir,
        transport_network,
        origins=destinations, #origins,
        destinations=origins, #destinations,
        departure=datetime.datetime(2024, 6, 9, 15, 30),
        # access_modes=[r5py.TransportMode.CAR], #before
        transport_modes=[
            # r5py.TransportMode.TRANSIT,
            # r5py.TransportMode.WALK,
            r5py.TransportMode.CAR,
            # r5py.TransportMode.SUBWAY,
            # r5py.TransportMode.RAIL,
            # r5py.TransportMode.BICYCLE,

        ],
        # access_modes = []

    )
    print(f"Starting travel time computations. This could take a while! Elapsed time {time.time()-start_time} sec since code start.")
    # travel_time_matrix_computer.request.access_modes = [r5py.TransportMode.CAR]
    travel_times = travel_time_matrix_computer.compute_travel_times()
    print(f"Travel time computations finished. Elapsed time {time.time()-start_time} sec since code start.")
    print(travel_times.head(15))
    # Generate a unique epoch identifier for the filename
    epoch_time = int(time.time())  # Current epoch time in seconds
    # Construct the filename with the unique epoch identifier
    filename = f"county_data/{county_name}/Option{option}_travel_times_{num_random_points}locations_to_{len(coordinates_2)}hospitals_{epoch_time}.csv"
    # Export the DataFrame to CSV with the unique filename
    travel_times.to_csv(filename, index=False)
    print(f"DataFrame exported to '{filename}' successfully.")

    # Assuming you have your travel_times DataFrame
    print(f"Starting aggregation by origin. This could take a while! Elapsed time {time.time()-start_time} sec since code start.")
    result = travel_times.groupby('to_id')['travel_time'].agg([
        ('min_travel_time', 'min'),
        ('second_min_travel_time', lambda x: x.nsmallest(2).iloc[-1] if len(x) >= 2 else None),
        ('third_min_travel_time', lambda x: x.nsmallest(3).iloc[-1] if len(x) >= 3 else None),
        ('median_travel_time', 'median'),
        ('average_travel_time', 'mean'),
        ('q1_travel_time', lambda x: x.quantile(0.25)),  # 25th percentile
        ('q3_travel_time', lambda x: x.quantile(0.75))   # 75th percentile
    ]).reset_index()

    print(result)
    filename = f"county_data/{county_name}/Option{option}_aggregated_information_{num_random_points}locations_to_{len(coordinates_2)}hospitals__{epoch_time}.csv"
    # Export the DataFrame to CSV with the unique filename
    result.to_csv(filename, index=False)
    print(f"DataFrame exported to '{filename}' successfully.")
    print(f"Finished aggregation by origin and exporting files. Elapsed time {time.time()-start_time} sec since code start.")

if __name__=='__main__':
    #arg parser
    parser = argparse.ArgumentParser(description="A script that uses county name.")
    parser.add_argument("--county_name", type=str, required=True, 
                        help="Name of the county")
    parser.add_argument("--state_name", type=str, required=True, 
                        help="Name of the state")
    parser.add_argument("--option", type=int, required=True, 
                        help="Which analysis to run")
    parser.add_argument("--osm", type=str, required=True, 
                        help="Which osm file to use (without extension)")
    args = parser.parse_args()
    # Convert county_name to have first letter capital and rest lowercase
    county_name = args.county_name.capitalize()
    state_name = args.state_name
    # download_guilford_map_sp()
    find_tt_matrix(county_name, state_name, args.option, args.osm)


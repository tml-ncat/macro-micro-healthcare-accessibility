#!/usr/bin/env python3
import geopandas as gpd
import r5py
import numpy as np
#import r5py.sampledata.helsinki
import shapely
from shapely.geometry import box
import pandas as pd
# pd.set_option('display.max_columns', None)
import folium
import folium.plugins
import matplotlib.pyplot as plt
import datetime
import os
import time
import random
import sys

import osmnx as ox
import warnings
import networkx as nx
import argparse

import matplotlib.pyplot as plt
import contextily as cx

def plot_choropleth(polygons, column_to_plot, title, cmap='viridis', figsize=(15, 10), alpha=0.7):
    # Read the shapefile
    gdf = polygons
    # Check if the CRS is in a suitable projection for web mercator
    if gdf.crs.to_string() != 'EPSG:3857':
        gdf = gdf.to_crs(epsg=3857)
    # Create the plot
    fig, ax = plt.subplots(figsize=figsize)
    # Plot the choropleth
    gdf.plot(column=column_to_plot, cmap=cmap, legend=True, alpha=alpha,  
             legend_kwds={'label': column_to_plot, 'orientation': "horizontal"},
             ax=ax)
    # Add the base map
    cx.add_basemap(ax, source=cx.providers.OpenStreetMap.Mapnik)
    # Remove axis
    ax.axis('off')
    # Add title
    plt.title(title, fontsize=16)
    # Adjust layout and display
    plt.tight_layout()
    plt.show()
    return fig, ax

def prep_spatial_csv_files(county_name, state_name):
    # Step 1: Load the polygon and points layers from the .gdb and .shp files
    start_time = time.time()
    print("Current working directory=",os.getcwd())
    polygons = gpd.read_file(f'state_data/SVI_{state_name}_SHP.shp')
    print(f"==SVI Census Tract file reading completed. Elapsed time {time.time()-start_time} sec since code start.")
    # plot_choropleth(polygons, 'E_DISABL','Disability plot')
    
    points = gpd.read_file(f'county_data/{county_name}/nc_{county_name.lower()}_parcels_pt.shp')
    print(f"==Parcel file reading completed. Elapsed time {time.time()-start_time} sec since code start.")

    # Print the CRS of both GeoDataFrames
    polygons = polygons.to_crs(4269) #previously it was 4269; 32119 prevents warning but lat-long are messed up
    points = points.to_crs(4269)
    # print("Polygons CRS:", polygons.crs)
    # print("Points CRS:", points.crs)
    print(f"==Projection to EPSG:4269 Completed. Elapsed time {time.time()-start_time} sec since code start.")
    assert len(points) > 0, "Points layer is null or has no rows after projection." 
    assert len(polygons) > 0, "Points layer is null or has no rows after projection."

    # Get all unique values in the 'PARUSEDESC' column
    unique_parusedesc = points['PARUSEDESC'].unique()
    print("\nUnique values in 'PARUSEDESC' column (selecting RESIDENTAL and TOWNHOUSE):")
    print(unique_parusedesc)
    #todo feature; add it as a input

    # Print the number of rows before filtering
    num_rows_before = len(points)
    num_census_tracts = len(polygons)
    # Step 2: Filter the polygons by COUNTY == 'GUILFORD' and Select features where 'PARUSEDESC' is either 'RESIDENTIAL' or 'TOWNHOUSE'
    polygons = polygons[polygons['COUNTY'] == county_name]
    if county_name in ["Guilford", "Other"]:
        points = points[(points['PARUSEDESC'] == 'RESIDENTIAL') | (points['PARUSEDESC'] == 'TOWNHOUSE')]
    elif county_name=="Bladen":
        points = points[(points['PARUSEDESC'] == 'RESIDENTIAL IMPROVED')]
    else:
        print("County {county_name} is not implemented yet. Fix the code by adding elif part for appropriate columns in parcel data.")
    # Print the number of rows after filtering
    num_rows_after = len(points)
    num_census_tracts_after = len(polygons)
    # Print the number of rows before and after filtering
    print(f"\nNumber of parcel centroids before filtering: {num_rows_before}, after filtering: {num_rows_after}")
    print(f"\nNumber of census tracts before filtering: {num_census_tracts}, after filtering: {num_census_tracts_after}")

    # # Reproject the points to match the CRS of the polygons if needed
    # if polygons.crs != points.crs:
    #     points = points.to_crs(polygons.crs)
    
    # Step 2: Add a unique index to the polygons
    polygons['poly_idx'] = polygons.index + 1
    #==Exporting census tract centroid input files===
    # Calculate centroids and add lat/long columns
    polygons['centroid'] = polygons.geometry.centroid
    polygons['longitude'] = polygons.centroid.x
    polygons['latitude'] = polygons.centroid.y
    # polygons['geometry_wkt'] = polygons.geometry.to_wkt()

    # Export selected columns to CSV
    output_df = polygons[['OBJECTID','poly_idx','latitude', 'longitude','E_NOVEH','M_NOVEH']].reset_index()
    output_df.to_csv(f'county_data/{county_name}/Option1_county_centroids.csv', index=False)
    print(f"CSV file Option 1 has been created with {len(output_df)} rows.")
    print(f"==File 1 export completed. Elapsed time {time.time()-start_time} sec since code start.")

    points['p_latitude'] = points.geometry.y
    points['p_longitude'] = points.geometry.x
    # sys.exit(1)
    # Print the first few rows of the loaded shapefiles
    # print("Polygons GeoDataFrame:")
    # print(polygons.head())

    # print("\nPoints GeoDataFrame:")
    # print(points.head())

    # Print the polygons GeoDataFrame with the new index
    # print("\nPolygons GeoDataFrame with polygon_index:")
    # print(polygons.head())

    # Step 3: Perform the spatial join
    points_with_polygon_index = gpd.sjoin(points, polygons[['geometry', 'poly_idx']], how='left', op='within')
    print(f"==Spatial Join Completed. Elapsed time {time.time()-start_time} sec since code start.")
    # Reset index once, if needed
    points_with_polygon_index = points_with_polygon_index.reset_index(drop=True)  # Drop existing index if not needed

    # Print the points GeoDataFrame after the spatial join
    # print("\nPoints GeoDataFrame after spatial join:")
    # print(points_with_polygon_index.head())

    # Step 4: Assign new index based on polygon index and unique counter within each polygon
    def assign_new_index(df):
        df = df.copy()
        df['point_index_within_polygon'] = range(1, len(df) + 1)
        df['new_index'] = df['poly_idx'] * 10000 + df['point_index_within_polygon']
        return df

    # Group by polygon_index and apply the function
    # points_with_polygon_index = points_with_polygon_index.reset_index()
    points_with_new_index = points_with_polygon_index.groupby('poly_idx').apply(assign_new_index)
    points_with_new_index["new_index"] = points_with_new_index["new_index"].astype(int)
    # points_with_new_index = points_with_polygon_index.groupby('poly_idx').apply(lambda df: assign_new_index(df).reset_index(drop=True))
    print(f"==Grouping and Indexing Completed. Elapsed time {time.time()-start_time} sec since code start.")

    # Reset the index to clean up the DataFrame
    points_with_new_index = points_with_new_index.reset_index(drop=True)

    # Calculate average coordinates for each polygon
    # points_with_new_index = points_with_new_index.reset_index()
    avg_coords = points_with_new_index.groupby('poly_idx').agg({
        'p_latitude': 'mean',
        'p_longitude': 'mean'
    }).reset_index()
    # Rename columns for clarity
    avg_coords.columns = ['county_index', 'latitude', 'longitude']
    avg_coords['county_index'] =  avg_coords['county_index'].astype(int)

    # Export to CSV
    avg_coords.to_csv(f'county_data/{county_name}/Option2_county_centroids.csv', index=False)
    print(f"CSV file 'county_data_v2.csv' has been created with {len(avg_coords)} rows.")
    print(f"==File 2 export completed. Elapsed time {time.time()-start_time} sec since code start.")
    # Print the points GeoDataFrame with the new index
    # print("\nPoints GeoDataFrame with new index:")
    # print(points_with_new_index.head())

    # Step 6: Rename columns to ensure they are not longer than 10 characters for ESRI SHP export
    points_with_new_index = points_with_new_index.rename(columns={
        'point_index_within_polygon': 'pt_idx',
        'new_index': 'new_index',
        'index_right': 'idx_right',
        'p_latitude': 'latitude',
        'p_longitude': 'longitude'
    })

    # Convert geometry to WKT
    points_with_new_index['geometry_wkt'] = points_with_new_index.geometry.to_wkt()
    # Select and export the desired columns
    columns_to_export = ['new_index', 'poly_idx', 'pt_idx', 'latitude', 'longitude', 'ALTPARNO', 'NPARNO', 'PARUSEDESC', 'geometry_wkt']
    output_df = points_with_new_index[columns_to_export]
    # Export to CSV
    output_df.to_csv(f'county_data/{county_name}/Option3_residential_parcel_centroids.csv', index=False)

    print(f"CSV file 'Option3_residential_parcel_centroids.csv' has been created with {len(output_df)} rows. Exporting to shape file as well.")
    print(f"==File 3 export completed. Elapsed time {time.time()-start_time} sec since code start.")
    # Print the final GeoDataFrame before saving
    # print("\nFinal Points GeoDataFrame:")
    # print(points_with_new_index.head())

    # Step 5: Save the result to a new shapefile
    points_with_new_index.to_file(f'county_data/{county_name}/nc_{county_name}_parcels_pt_withNewIndex.shp')
    print(f"==Exporting to shape file completed. Elapsed time {time.time()-start_time} sec since code start.")

    # plot_choropleth(polygons, 'E_DISABL','Disability plot')
    
    avg_lat = polygons['latitude'].mean()
    avg_lon = polygons['longitude'].mean()
    export_hospital_csv(avg_lat, avg_lon, county_name, state_name)
    print(f"\n\n==All geopandas analyis completed. Elapsed time {time.time()-start_time} sec since code start.")

def export_hospital_csv(avg_lat, avg_lon, county_name, state_name):
    miles_from_center_point = 30
    # Convert miles to degrees (approximate conversion); 20 miles in each direction
    MILES_TO_DEGREES_LAT = miles_from_center_point / 69
    MILES_TO_DEGREES_LON = miles_from_center_point / 69

    # Define the bounds of the rectangle
    min_lat = avg_lat - MILES_TO_DEGREES_LAT
    max_lat = avg_lat + MILES_TO_DEGREES_LAT
    min_lon = avg_lon - MILES_TO_DEGREES_LON
    max_lon = avg_lon + MILES_TO_DEGREES_LON

    # Create the rectangular buffer
    buffer_rectangle = box(min_lon, min_lat, max_lon, max_lat)

    # Load the point layer
    points_gdf = gpd.read_file(f'state_data/{state_name}_Hospitals/Hospitals.shp')
    points_gdf = points_gdf.to_crs(epsg=4269)  # Ensure CRS matches

    # Create a GeoDataFrame for the buffer
    buffer_gdf = gpd.GeoDataFrame([buffer_rectangle], columns=['geometry'], crs='EPSG:4269')

    # Find points within the buffer
    points_within_buffer = points_gdf[points_gdf.geometry.within(buffer_rectangle)]

    # Extract latitude, longitude, and ID
    points_within_buffer['latitude'] = points_within_buffer.geometry.y
    points_within_buffer['longitude'] = points_within_buffer.geometry.x
    points_within_buffer['ID'] = points_within_buffer.index + 1
    export_df = points_within_buffer[['ID', 'latitude', 'longitude']]

    # Save to a CSV file
    export_df.to_csv(f'county_data/{county_name}/hospitals_within_buffer.csv', index=False)
    print(f"Hospital data exported with {len(export_df)} rows")
    # Save the resulting points to a new shapefile (optional)
    # points_within_buffer.to_file('points_within_buffer.shp')
    # Print the resulting points
    # print(points_within_buffer)

if __name__=='__main__':
    #arg parser
    parser = argparse.ArgumentParser(description="A script that uses county name.")
    parser.add_argument("--county_name", type=str, required=True, 
                        help="Name of the county")
    parser.add_argument("--state_name", type=str, required=True, 
                        help="Name of the state")
    args = parser.parse_args()
    # Convert county_name to have first letter capital and rest lowercase
    county_name = args.county_name.capitalize()
    state_name = args.state_name
    # download_guilford_map_sp()
    prep_spatial_csv_files(county_name, state_name)
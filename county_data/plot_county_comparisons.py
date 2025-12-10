#!/usr/bin/env python3
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import os

def create_combined_box_plot_robust():
    """
    Creates a single file with 5x2 grid of box plots.
    Robust version with multiple fallback options.
    """
    
    # Define counties (urban sorted alphabetically)
    urban_counties = sorted(['guilford', 'wake', 'durham', 'buncombe', 'mecklenburg'])
    rural_counties = ['bertie', 'bladen', 'columbus', 'pender', 'washington']
    
    # Define the columns to plot and their labels
    columns_to_plot = ['Option1_aggregated_min_travel_time', 'Option2_aggregated_min_travel_time', 'avg_all_parcel', 'avg_top_x']
    column_labels = ['Option1', 'Option2', 'Option3 (avg)', 'Option3 (worst)']
    
    # Create figure with manual spacing
    plt.rcParams.update({'font.size': 10})  # Set default font size
    fig, axes = plt.subplots(5, 2, figsize=(16, 20))
    
    # Function to create box plot for a single county
    def plot_county_data(ax, county_name, is_urban=True):
        try:
            # Read the CSV file
            folder_path = f'./county_data/{county_name}/'
            df = pd.read_csv(f'{folder_path}/customized_combined_output_AFTER.csv')
            
            # Create DataFrame with specified columns
            df_to_plot = df[columns_to_plot].copy()
            df_to_plot.columns = column_labels
            
            # Create box plot using matplotlib directly (more robust)
            box_data = [df_to_plot[col].dropna() for col in column_labels]
            bp = ax.boxplot(box_data, labels=column_labels, patch_artist=False)  # No fill
            
            # Set title and labels with larger font sizes
            county_type = "Urban" if is_urban else "Rural"
            ax.set_title(f'{county_name.capitalize()} County, NC ({county_type})', fontsize=14)
            ax.set_ylabel('Travel time (minutes)', fontsize=14)
            ax.tick_params(axis='x', labelsize=12, rotation=45)
            ax.tick_params(axis='y', labelsize=14)
            
            # Add horizontal line at median of Option1
            if len(box_data[0]) > 0:  # Check if Option1 data exists
                median_value = df_to_plot['Option1'].median()
                ax.axhline(y=median_value, color='red', linestyle='--', linewidth=0.8, alpha=0.5)
            
        except FileNotFoundError:
            ax.text(0.5, 0.5, f'Data not found for\n{county_name.capitalize()}', 
                   horizontalalignment='center', verticalalignment='center', 
                   transform=ax.transAxes, fontsize=12)
            ax.set_title(f'{county_name.capitalize()} County, NC', fontsize=14)
        except Exception as e:
            ax.text(0.5, 0.5, f'Error loading data for\n{county_name.capitalize()}\n{str(e)[:50]}...', 
                   horizontalalignment='center', verticalalignment='center', 
                   transform=ax.transAxes, fontsize=10)
            ax.set_title(f'{county_name.capitalize()} County, NC', fontsize=14)
    
    # Plot all counties
    for i in range(5):
        # Urban counties (left column)
        if i < len(urban_counties):
            plot_county_data(axes[i, 0], urban_counties[i], is_urban=True)
        else:
            axes[i, 0].axis('off')
        
        # Rural counties (right column)
        if i < len(rural_counties):
            plot_county_data(axes[i, 1], rural_counties[i], is_urban=False)
        else:
            axes[i, 1].axis('off')
    
    # Manual layout adjustment
    plt.subplots_adjust(left=0.08, bottom=0.05, right=0.95, top=0.95, wspace=0.25, hspace=0.4)
    
    # Try multiple save formats with error handling
    saved = False
    formats_to_try = [
        ('combined_counties_box_plots.png', 'png'),
        ('combined_counties_box_plots.jpg', 'jpg'),
        ('combined_counties_box_plots.svg', 'svg'),
        ('combined_counties_box_plots.pdf', 'pdf')
    ]
    
    for filename, fmt in formats_to_try:
        try:
            plt.savefig(filename, format=fmt, dpi=300, bbox_inches='tight')
            print(f"Successfully saved as: {filename}")
            saved = True
            break
        except Exception as e:
            print(f"Failed to save as {fmt}: {str(e)}")
            continue
    
    if not saved:
        # Last resort - save without bbox_inches
        try:
            plt.savefig('combined_counties_box_plots.png', format='png', dpi=300)
            print("Saved as PNG without bbox_inches optimization")
        except Exception as e:
            print(f"Complete failure to save: {str(e)}")
    
    plt.close()

def create_combined_box_plot_fixed_scale():
    """
    Creates a single file with 5x2 grid of box plots with fixed y-scale (0-50).
    """
    
    # Define counties (urban sorted alphabetically)
    urban_counties = sorted(['guilford', 'wake', 'durham', 'buncombe', 'mecklenburg'])
    rural_counties = ['bertie', 'bladen', 'columbus', 'pender', 'washington']
    
    # Define the columns to plot and their labels
    columns_to_plot = ['Option1_aggregated_min_travel_time', 'Option2_aggregated_min_travel_time', 'avg_all_parcel', 'avg_top_x']
    column_labels = ['Option1', 'Option2', 'Option3 (avg)', 'Option3 (worst)']
    
    # Create figure with manual spacing
    plt.rcParams.update({'font.size': 14})  # Set default font size
    fig, axes = plt.subplots(5, 2, figsize=(16, 20))
    
    # Function to create box plot for a single county
    def plot_county_data(ax, county_name, is_urban=True):
        try:
            # Read the CSV file
            folder_path = f'./county_data/{county_name}/'
            df = pd.read_csv(f'{folder_path}/customized_combined_output_AFTER.csv')
            
            # Create DataFrame with specified columns
            df_to_plot = df[columns_to_plot].copy()
            df_to_plot.columns = column_labels
            
            # Create box plot using matplotlib directly (more robust)
            box_data = [df_to_plot[col].dropna() for col in column_labels]
            bp = ax.boxplot(box_data, labels=column_labels, patch_artist=False)  # No fill
            
            # Set title and labels with larger font sizes
            county_type = "Urban" if is_urban else "Rural"
            ax.set_title(f'{county_name.capitalize()} County, NC ({county_type})', fontsize=16)
            ax.set_ylabel('Travel time (minutes)', fontsize=16)
            ax.tick_params(axis='x', labelsize=16, rotation=10)
            ax.tick_params(axis='y', labelsize=16)
            
            # Set fixed y-scale
            ax.set_ylim(0, 50)
            
            # Add horizontal line at median of Option1
            if len(box_data[0]) > 0:  # Check if Option1 data exists
                median_value = df_to_plot['Option1'].median()
                ax.axhline(y=median_value, color='red', linestyle='--', linewidth=2, alpha=0.5)
            
        except FileNotFoundError:
            ax.text(0.5, 0.5, f'Data not found for\n{county_name.capitalize()}', 
                   horizontalalignment='center', verticalalignment='center', 
                   transform=ax.transAxes, fontsize=12)
            ax.set_title(f'{county_name.capitalize()} County, NC', fontsize=14)
            ax.set_ylim(0, 50)  # Set fixed y-scale even for error cases
        except Exception as e:
            ax.text(0.5, 0.5, f'Error loading data for\n{county_name.capitalize()}\n{str(e)[:50]}...', 
                   horizontalalignment='center', verticalalignment='center', 
                   transform=ax.transAxes, fontsize=10)
            ax.set_title(f'{county_name.capitalize()} County, NC', fontsize=14)
            ax.set_ylim(0, 50)  # Set fixed y-scale even for error cases
    
    # Plot all counties
    for i in range(5):
        # Urban counties (left column)
        if i < len(urban_counties):
            plot_county_data(axes[i, 0], urban_counties[i], is_urban=True)
        else:
            axes[i, 0].axis('off')
        
        # Rural counties (right column)
        if i < len(rural_counties):
            plot_county_data(axes[i, 1], rural_counties[i], is_urban=False)
        else:
            axes[i, 1].axis('off')
    
    # Manual layout adjustment
    plt.subplots_adjust(left=0.08, bottom=0.05, right=0.95, top=0.95, wspace=0.25, hspace=0.4)
    
    # Try multiple save formats with error handling
    saved = False
    formats_to_try = [
        ('combined_counties_box_plots_fixed_scale.pdf', 'pdf'),
        ('combined_counties_box_plots_fixed_scale.png', 'png'),
        ('combined_counties_box_plots_fixed_scale.jpg', 'jpg'),
        ('combined_counties_box_plots_fixed_scale.svg', 'svg')
        
    ]
    
    for filename, fmt in formats_to_try:
        try:
            plt.savefig(filename, format=fmt, dpi=300, bbox_inches='tight')
            print(f"Successfully saved fixed-scale plot as: {filename}")
            saved = True
            break
        except Exception as e:
            print(f"Failed to save as {fmt}: {str(e)}")
            continue
    
    if not saved:
        # Last resort - save without bbox_inches
        try:
            plt.savefig('combined_counties_box_plots_fixed_scale.png', format='png', dpi=300)
            print("Saved fixed-scale plot as PNG without bbox_inches optimization")
        except Exception as e:
            print(f"Complete failure to save: {str(e)}")
    
    plt.close()

def create_individual_plots():
    """
    Fallback option: Create individual plots for each county
    """
    
    # Define counties (urban sorted alphabetically)
    urban_counties = sorted(['guilford', 'wake', 'durham', 'buncombe', 'mecklenburg'])
    rural_counties = ['bertie', 'bladen', 'columbus', 'pender', 'washington']
    all_counties = urban_counties + rural_counties
    
    # Define the columns to plot and their labels
    columns_to_plot = ['Option1_aggregated_min_travel_time', 'Option2_aggregated_min_travel_time', 'avg_all_parcel', 'avg_top_x']
    column_labels = ['Option1', 'Option2', 'Option3 (avg)', 'Option3 (worst)']
    
    print("Creating individual plots for each county...")
    
    for county in all_counties:
        try:
            # Read the CSV file
            folder_path = f'./county_data/{county}/'
            df = pd.read_csv(f'{folder_path}/customized_combined_output_AFTER.csv')
            
            # Create DataFrame with specified columns
            df_to_plot = df[columns_to_plot].copy()
            df_to_plot.columns = column_labels
            
            # Create box plot
            plt.figure(figsize=(8, 6))
            box_data = [df_to_plot[col].dropna() for col in column_labels]
            bp = plt.boxplot(box_data, labels=column_labels, patch_artist=False)  # No fill
            
            # Set title and labels with larger font sizes
            county_type = "Urban" if county in urban_counties else "Rural"
            plt.title(f'{county.capitalize()} County, NC ({county_type})', fontsize=16)
            plt.ylabel('Travel time (minutes)', fontsize=14)
            plt.xticks(rotation=45, fontsize=12)
            plt.yticks(fontsize=12)
            
            # Add horizontal line at median of Option1
            if len(box_data[0]) > 0:
                median_value = df_to_plot['Option1'].median()
                plt.axhline(y=median_value, color='red', linestyle='--', linewidth=0.8, alpha=0.5)
            
            # Save individual plot
            output_filename = f'{county}_box_plot.png'
            plt.savefig(output_filename, format='png', dpi=300, bbox_inches='tight')
            plt.close()
            print(f"Saved: {output_filename}")
            
        except Exception as e:
            print(f"Failed to create plot for {county}: {str(e)}")

if __name__ == '__main__':
    # print("Attempting to create combined box plot...")
    # try:
    #     create_combined_box_plot_robust()
    # except Exception as e:
    #     print(f"Combined plot failed: {str(e)}")
    #     print("Falling back to individual plots...")
    #     create_individual_plots()
    
    print("\nCreating fixed-scale version...")
    try:
        create_combined_box_plot_fixed_scale()
    except Exception as e:
        print(f"Fixed-scale plot failed: {str(e)}")

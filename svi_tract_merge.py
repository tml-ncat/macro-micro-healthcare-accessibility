"""
================================================================================
CENSUS TRACT SHAPEFILE + SVI DATA MERGER
================================================================================

PURPOSE:
--------
This script merges census tract shapefile (polygon geometries) with SVI 
(Social Vulnerability Index) CSV data to create a complete spatial dataset.

INPUT FILES REQUIRED:
---------------------
1. Census Tract Shapefile (.shp + .shx, .dbf, .prj files)
   - Contains polygon geometries for each census tract
   - Must have a GEOID or similar identifier column
   
2. SVI CSV Data (.csv)
   - Contains social vulnerability attributes
   - Must have a FIPS column matching the shapefile GEOID

OUTPUT FILES CREATED:
---------------------
1. Shapefile (.shp) - Traditional GIS format
2. GeoJSON (.geojson) - Web-friendly format
3. GeoPackage (.gpkg) - Modern single-file format

All outputs contain polygon geometries + all CSV attributes merged together.

================================================================================
"""

import geopandas as gpd
import pandas as pd
import os

# ============================================================================
# CONFIGURATION SECTION - UPDATE THESE PATHS FOR YOUR DATA
# ============================================================================

# INPUT FILE 1: Path to your census tract shapefile
# Replace this with the path to your .shp file
# Example: '/Users/yourname/Documents/data/census_tracts.shp'
SHAPEFILE_PATH = '/Users/komalgulati/Library/Mobile Documents/com~apple~CloudDocs/Documents/project_3_2/accessibility-main/macro-micro-healthcare-accessibility/tl_2025_37_tract.shp'

# INPUT FILE 2: Path to your SVI CSV data file
# Replace this with the path to your .csv file
# Example: '/Users/yourname/Documents/data/svi_data.csv'
CSV_PATH = '/Users/komalgulati/Library/Mobile Documents/com~apple~CloudDocs/Documents/project_3_2/accessibility-main/macro-micro-healthcare-accessibility/NorthCarolina.csv'

# OUTPUT DIRECTORY: Where to save the merged files
# Replace this with your desired output folder
# Example: '/Users/yourname/Documents/output/'
OUTPUT_DIR = '/Users/komalgulati/Library/Mobile Documents/com~apple~CloudDocs/Documents/project_3_2/accessibility-main/macro-micro-healthcare-accessibility/state_data/'

# OUTPUT FILENAME (without extension): Base name for output files
# The script will add .shp, .geojson, .gpkg extensions automatically
# Replace this with your desired output filename
OUTPUT_FILENAME = 'SVI_NorthCarolina_SHP'

# COLUMN NAMES: Identifier columns for joining
# The shapefile typically has a GEOID column (might be GEOID, GEOID20, TRACTCE, etc.)
# The CSV typically has a FIPS column
# Usually these don't need to be changed, but you can customize if needed
SHAPEFILE_ID_COLUMN = 'GEOID'  # Column name in shapefile (will auto-detect if None)
CSV_ID_COLUMN = 'FIPS'         # Column name in CSV

# ============================================================================
# MAIN SCRIPT - NO NEED TO MODIFY BELOW THIS LINE
# ============================================================================

def merge_shapefile_with_csv(shapefile_path, csv_path, output_dir, 
                             output_filename, shp_id_col=None, csv_id_col='FIPS'):
    """
    Merge census tract shapefile with CSV data.
    
    Parameters:
    -----------
    shapefile_path : str
        Path to the census tract shapefile
    csv_path : str
        Path to the CSV data file
    output_dir : str
        Directory where output files will be saved
    output_filename : str
        Base name for output files (without extension)
    shp_id_col : str, optional
        Column name for tract ID in shapefile (auto-detects if None)
    csv_id_col : str
        Column name for tract ID in CSV (default: 'FIPS')
    
    Returns:
    --------
    merged_gdf : GeoDataFrame
        Merged geodataframe with geometries and attributes
    """
    
    print("="*80)
    print("CENSUS TRACT SHAPEFILE + SVI DATA MERGER")
    print("="*80)
    
    # ========================================================================
    # STEP 1: Load the census tract shapefile (polygon geometries)
    # ========================================================================
    print(f"\n[STEP 1] Loading census tract shapefile...")
    print(f"  File: {shapefile_path}")
    
    try:
        census_tracts = gpd.read_file(shapefile_path)
        print(f"  ✓ Successfully loaded {len(census_tracts):,} census tracts")
    except Exception as e:
        print(f"  ✗ ERROR loading shapefile: {e}")
        return None
    
    # Display shapefile information
    print(f"  - Coordinate Reference System: {census_tracts.crs}")
    print(f"  - Geometry type: {census_tracts.geometry.type.unique()[0]}")
    print(f"  - Number of columns: {len(census_tracts.columns)}")
    print(f"  - Column names: {list(census_tracts.columns)}")
    
    # ========================================================================
    # STEP 2: Auto-detect or verify the GEOID column in shapefile
    # ========================================================================
    print(f"\n[STEP 2] Identifying tract identifier column in shapefile...")
    
    if shp_id_col is None:
        # Auto-detect: Look for columns with 'GEOID' in the name
        geoid_candidates = [col for col in census_tracts.columns if 'GEOID' in col.upper()]
        if len(geoid_candidates) > 0:
            shp_id_col = geoid_candidates[0]
            print(f"  ✓ Auto-detected identifier column: '{shp_id_col}'")
        else:
            print(f"  ✗ ERROR: Could not find GEOID column")
            print(f"  Available columns: {list(census_tracts.columns)}")
            return None
    else:
        if shp_id_col in census_tracts.columns:
            print(f"  ✓ Using specified identifier column: '{shp_id_col}'")
        else:
            print(f"  ✗ ERROR: Column '{shp_id_col}' not found in shapefile")
            print(f"  Available columns: {list(census_tracts.columns)}")
            return None
    
    # Show sample values
    print(f"  - Sample {shp_id_col} values: {census_tracts[shp_id_col].head(3).tolist()}")
    
    # ========================================================================
    # STEP 3: Load the CSV data (SVI attributes)
    # ========================================================================
    print(f"\n[STEP 3] Loading CSV data...")
    print(f"  File: {csv_path}")
    
    try:
        svi_data = pd.read_csv(csv_path)
        print(f"  ✓ Successfully loaded {len(svi_data):,} records")
    except Exception as e:
        print(f"  ✗ ERROR loading CSV: {e}")
        return None
    
    # Display CSV information
    print(f"  - Number of columns: {len(svi_data.columns)}")
    
    # Verify the FIPS column exists
    if csv_id_col not in svi_data.columns:
        print(f"  ✗ ERROR: Column '{csv_id_col}' not found in CSV")
        print(f"  Available columns: {list(svi_data.columns[:20])}...")
        return None
    
    print(f"  - Sample {csv_id_col} values: {svi_data[csv_id_col].head(3).tolist()}")
    
    # ========================================================================
    # STEP 4: Prepare data for merge (standardize ID formats)
    # ========================================================================
    print(f"\n[STEP 4] Preparing data for merge...")
    
    # Convert both ID columns to string and zero-pad to 11 digits
    # Census tract FIPS codes are 11 digits: 2 (state) + 3 (county) + 6 (tract)
    census_tracts[shp_id_col] = census_tracts[shp_id_col].astype(str).str.zfill(11)
    svi_data[csv_id_col] = svi_data[csv_id_col].astype(str).str.zfill(11)
    
    print(f"  ✓ Standardized ID formats (11-digit FIPS codes)")
    print(f"  - Shapefile {shp_id_col}: {census_tracts[shp_id_col].head(3).tolist()}")
    print(f"  - CSV {csv_id_col}: {svi_data[csv_id_col].head(3).tolist()}")
    
    # ========================================================================
    # STEP 5: Perform the merge (join CSV attributes to shapefile geometries)
    # ========================================================================
    print(f"\n[STEP 5] Merging shapefile with CSV data...")
    print(f"  Join condition: {shp_id_col} = {csv_id_col}")
    
    # Merge: Join SVI data to census tract polygons
    # 'inner' join keeps only tracts present in BOTH datasets
    merged_gdf = census_tracts.merge(
        svi_data, 
        left_on=shp_id_col, 
        right_on=csv_id_col, 
        how='inner'  # Use 'left' to keep all shapefile tracts, 'inner' for matching only
    )
    
    print(f"  ✓ Successfully merged {len(merged_gdf):,} census tracts")
    print(f"  ✓ Total attributes per tract: {len(merged_gdf.columns)}")
    
    # ========================================================================
    # STEP 6: Check for unmatched records
    # ========================================================================
    print(f"\n[STEP 6] Checking for unmatched records...")
    
    # Tracts in shapefile but not in CSV
    unmatched_shp = census_tracts[~census_tracts[shp_id_col].isin(svi_data[csv_id_col])]
    if len(unmatched_shp) > 0:
        print(f"  ⚠ {len(unmatched_shp):,} tracts in shapefile NOT found in CSV")
        print(f"    Sample IDs: {unmatched_shp[shp_id_col].head(3).tolist()}")
    else:
        print(f"  ✓ All shapefile tracts matched with CSV data")
    
    # Records in CSV but not in shapefile
    unmatched_csv = svi_data[~svi_data[csv_id_col].isin(census_tracts[shp_id_col])]
    if len(unmatched_csv) > 0:
        print(f"  ⚠ {len(unmatched_csv):,} CSV records NOT found in shapefile")
        print(f"    Sample IDs: {unmatched_csv[csv_id_col].head(3).tolist()}")
    else:
        print(f"  ✓ All CSV records matched with shapefile tracts")
    
    # ========================================================================
    # STEP 7: Save output files in multiple formats
    # ========================================================================
    print(f"\n[STEP 7] Saving output files...")
    print(f"  Output directory: {output_dir}")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Build full output paths
    output_base = os.path.join(output_dir, output_filename)
    
    try:
        # Format 1: Shapefile (.shp + companions)
        output_shp = output_base + '.shp'
        merged_gdf.to_file(output_shp, driver='ESRI Shapefile')
        print(f"  ✓ Shapefile saved: {output_shp}")
        print(f"    (Also created: .shx, .dbf, .prj, .cpg files)")
        
        # Format 2: GeoJSON (web-friendly, human-readable)
        output_geojson = output_base + '.geojson'
        merged_gdf.to_file(output_geojson, driver='GeoJSON')
        print(f"  ✓ GeoJSON saved: {output_geojson}")
        
        # Format 3: GeoPackage (modern, single-file format)
        output_gpkg = output_base + '.gpkg'
        merged_gdf.to_file(output_gpkg, driver='GPKG', layer='merged_data')
        print(f"  ✓ GeoPackage saved: {output_gpkg}")
        
    except Exception as e:
        print(f"  ✗ ERROR saving files: {e}")
        return None
    
    # ========================================================================
    # STEP 8: Summary and completion
    # ========================================================================
    print("\n" + "="*80)
    print("SUCCESS! MERGE COMPLETED")
    print("="*80)
    print(f"✓ Total census tracts merged: {len(merged_gdf):,}")
    print(f"✓ Total attributes per tract: {len(merged_gdf.columns)}")
    print(f"✓ Coordinate Reference System: {merged_gdf.crs}")
    print(f"✓ Geometry type: {merged_gdf.geometry.type.unique()[0]}")
    
    print(f"\n📁 OUTPUT FILES CREATED:")
    print(f"   1. {output_filename}.shp (+ companions)")
    print(f"   2. {output_filename}.geojson")
    print(f"   3. {output_filename}.gpkg")
    
    print(f"\n💡 NEXT STEPS:")
    print(f"   • Open in QGIS: Layer → Add Vector Layer")
    print(f"   • Open in ArcGIS: Add Data → Browse to file")
    print(f"   • Load in Python: geopandas.read_file('{output_filename}.geojson')")
    print(f"   • Load in R: sf::st_read('{output_filename}.gpkg')")
    
    print("\n" + "="*80)
    
    return merged_gdf


# ============================================================================
# EXECUTE THE SCRIPT
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("STARTING MERGE PROCESS...")
    print("="*80)
    
    # Run the merge function
    result = merge_shapefile_with_csv(
        shapefile_path=SHAPEFILE_PATH,
        csv_path=CSV_PATH,
        output_dir=OUTPUT_DIR,
        output_filename=OUTPUT_FILENAME,
        shp_id_col=SHAPEFILE_ID_COLUMN,
        csv_id_col=CSV_ID_COLUMN
    )
    
    if result is not None:
        print("\n✅ MERGE COMPLETED SUCCESSFULLY!")
        print(f"📊 Final dataset: {len(result):,} tracts with {len(result.columns)} attributes")
    else:
        print("\n❌ MERGE FAILED - Please check the error messages above")
# Data Sources and Setup Guide

This project requires several geospatial datasets to perform transportation accessibility analysis. Follow this guide to download and organize all required data.

## Overview

The analysis requires three main types of data:
1. **Social Vulnerability Index (SVI)** - Census tract polygons with vulnerability metrics
2. **Parcel Data** - Residential property locations by county
3. **Hospital Data** - Healthcare facility locations
4. **OpenStreetMap (OSM)** - Road network data

---

## 1. Social Vulnerability Index (SVI) Data

### Overview
The SVI data preparation involves three steps:
1. Download census tract shapefile (polygon geometries)
2. Download SVI CSV data (vulnerability attributes)
3. Merge them using the provided Python script

### Step 1: Download Census Tract Shapefile

**Source: U.S. Census Bureau TIGER/Line Shapefiles**

**Download Location:**
- **Website**: [https://www2.census.gov/geo/tiger/TIGER2020/TRACT/](https://www2.census.gov/geo/tiger/TIGER2020/TRACT/)
- **Direct File**: `tl_2020_37_tract.zip` (for North Carolina - state FIPS 37)
- Or use the latest year available (e.g., `tl_2025_37_tract.zip`)

**What to Download:**
- Census tract shapefile for North Carolina (state FIPS code: 37)
- File size: ~5-10 MB
- Includes all census tracts in the state
- Extract the zip file to get .shp, .shx, .dbf, .prj files

**File Placement (before merging):**
```
working_directory/
└── tl_2020_37_tract.shp  (and .shx, .dbf, .prj files)
```

### Step 2: Download SVI CSV Data

**Source: CDC/ATSDR Social Vulnerability Index (SVI)**

**Download Location:**
- **Official Website**: [https://www.atsdr.cdc.gov/place-health/php/svi/svi-data-documentation-download.html](https://www.atsdr.cdc.gov/place-health/php/svi/svi-data-documentation-download.html)
- Select North Carolina
- Download year: 2020 or latest available
- **Format**: CSV (not shapefile)

**What to Download:**
- **CSV file** with SVI data at census tract level
- File name pattern: `NorthCarolina.csv` or `SVI2020_NORTHCAROLINA.csv`
- Contains vulnerability metrics for all census tracts
- File size: ~2-5 MB

**File Placement (before merging):**
```
working_directory/
└── NorthCarolina.csv
```

### Step 3: Merge Census Tracts with SVI Data

**Use the provided merge script:** `merge_detailed_with_explanations.py`

**Configuration:**
Open the script and update these paths:
```python
# INPUT FILE 1: Census tract shapefile
SHAPEFILE_PATH = '/path/to/state_data/tl_2020_37_tract.shp'

# INPUT FILE 2: SVI CSV data
CSV_PATH = '/path/to/state_data/NorthCarolina.csv'

# OUTPUT: Where to save merged results
OUTPUT_DIR = '/path/to/state_data/'

# OUTPUT FILENAME: What to name the output
OUTPUT_FILENAME = 'SVI_NC_SHP'
```

**Run the merge:**
```bash
python state_data/svi_tract_merge.py
```

**What the script does:**
1. Loads census tract shapefile (polygon geometries)
2. Loads SVI CSV data (vulnerability attributes)
3. Matches census tracts by FIPS/GEOID codes
4. Merges them into a single spatial dataset
5. Outputs 3 file formats for maximum compatibility

**Output Files Created:**
```
state_data/
├── SVI_NC_SHP.shp  (+ .shx, .dbf, .prj files)
├── SVI_NC_SHP.geojson
└── SVI_NC_SHP.gpkg
```

All three formats contain:
- Census tract polygon geometries
- All SVI vulnerability metrics merged together
- Ready for spatial analysis in QGIS, ArcGIS, Python, R, etc.

### Key Columns in Merged Output

**From Census Tract Shapefile:**
- `GEOID` - 11-digit census tract identifier (e.g., '37001020100')
- `geometry` - Census tract polygon boundaries
- `STATEFP` - State FIPS code (37 for NC)
- `COUNTYFP` - County FIPS code
- `TRACTCE` - Census tract code
- `NAME` - Census tract name
- `ALAND` - Land area (square meters)
- `AWATER` - Water area (square meters)

**From SVI CSV Data:**
- `FIPS` - Census tract identifier (matches GEOID)
- `ST` - State FIPS code
- `STATE` - State name
- `ST_ABBR` - State abbreviation
- `STCNTY` - State + County FIPS code
- `COUNTY` - County name
- `LOCATION` - Full location description

**Population & Demographics:**
- `E_TOTPOP` - Total population estimate
- `E_HU` - Housing units estimate
- `E_HH` - Households estimate

**Socioeconomic Status (Theme 1):**
- `E_POV150` - Persons below 150% poverty estimate
- `EP_POV150` - Percentage below 150% poverty
- `E_UNEMP` - Unemployed civilians estimate
- `EP_UNEMP` - Percentage unemployed
- `E_NOHSDP` - Persons with no high school diploma estimate
- `EP_NOHSDP` - Percentage with no high school diploma
- `E_UNINSUR` - Uninsured persons estimate
- `EP_UNINSUR` - Percentage uninsured
- `SPL_THEME1` - Sum of series for socioeconomic theme
- `RPL_THEME1` - Percentile ranking for socioeconomic theme

**Household Characteristics (Theme 2):**
- `E_AGE65` - Persons aged 65 and older estimate
- `EP_AGE65` - Percentage aged 65 and older
- `E_AGE17` - Persons aged 17 and younger estimate
- `EP_AGE17` - Percentage aged 17 and younger
- `E_DISABL` - Civilian noninstitutionalized population with a disability
- `EP_DISABL` - Percentage with disability
- `E_SNGPNT` - Single-parent households estimate
- `EP_SNGPNT` - Percentage single-parent households
- `E_LIMENG` - Persons with limited English estimate
- `EP_LIMENG` - Percentage with limited English
- `SPL_THEME2` - Sum of series for household characteristics theme
- `RPL_THEME2` - Percentile ranking for household characteristics theme

**Racial & Ethnic Minority Status (Theme 3):**
- `E_MINRTY` - Minority population estimate
- `EP_MINRTY` - Percentage minority
- `E_AFAM` - African American population estimate
- `EP_AFAM` - Percentage African American
- `E_HISP` - Hispanic population estimate
- `EP_HISP` - Percentage Hispanic
- `E_ASIAN` - Asian population estimate
- `EP_ASIAN` - Percentage Asian
- `SPL_THEME3` - Sum of series for minority status theme
- `RPL_THEME3` - Percentile ranking for minority status theme

**Housing Type & Transportation (Theme 4):**
- `E_MUNIT` - Housing in structures with 10+ units estimate
- `EP_MUNIT` - Percentage in multi-unit structures
- `E_MOBILE` - Mobile homes estimate
- `EP_MOBILE` - Percentage mobile homes
- `E_CROWD` - Crowded housing estimate
- `EP_CROWD` - Percentage crowded housing
- `E_NOVEH` - **Households with no vehicle estimate** ⭐ KEY VARIABLE
- `EP_NOVEH` - **Percentage with no vehicle** ⭐ KEY VARIABLE
- `E_GROUPQ` - Group quarters population estimate
- `EP_GROUPQ` - Percentage in group quarters
- `SPL_THEME4` - Sum of series for housing/transportation theme
- `RPL_THEME4` - Percentile ranking for housing/transportation theme

**Overall Vulnerability:**
- `SPL_THEMES` - Sum of series for all themes
- `RPL_THEMES` - **Overall percentile ranking for Social Vulnerability** ⭐ KEY VARIABLE

**Flags (F_ prefix indicate values in top 90th percentile):**
- `F_TOTAL` - Total number of flags
- `F_THEME1` through `F_THEME4` - Flags by theme
- Individual flags for specific variables

### Important Notes
- The merge script automatically handles FIPS code formatting (zero-padding to 11 digits)
- The script creates outputs in 3 formats for maximum compatibility:
  - **Shapefile** (.shp) - Traditional GIS software (ArcGIS Desktop, older versions)
  - **GeoJSON** (.geojson) - Web mapping, Python, JavaScript
  - **GeoPackage** (.gpkg) - Modern GIS software (QGIS, ArcGIS Pro)
- Ensure you download **census tract level** data, not county level
- The merged shapefile includes all ~2,660 census tracts in North Carolina
- Coordinate Reference System (CRS): EPSG:4269 (NAD83)
- Both input files must cover the same geographic area (North Carolina)
- The script checks for unmatched records and reports them

### Troubleshooting
- **"Column not found"**: Check that CSV has 'FIPS' column and shapefile has 'GEOID' column
- **"No matching records"**: Verify both files are for North Carolina (state FIPS 37)
- **"File not found"**: Use absolute paths in the configuration section
- **Missing .shp files**: Make sure to extract the .zip file and upload all components

---

## 2. Parcel Data

### Source
**North Carolina Department of Revenue / County GIS**

### Download Location

**NC OneMap (Recommended)**
- **Website**: [https://www.nconemap.gov/](https://www.nconemap.gov/)
- Navigate to: Data & Downloads → Parcels
- Select your county of interest
- Download parcel point data (centroids) for your target county

**Alternative: Direct from County GIS**
Some counties provide direct downloads:
- **Guilford County**: [https://www.guilfordcountync.gov/our-county/maps-gis/gis-data-download](https://www.guilfordcountync.gov/our-county/maps-gis/gis-data-download)
- **Wake County**: [https://www.wake.gov/departments-government/tax-administration/data-files-statistics-and-reports](https://www.wake.gov/departments-government/tax-administration/data-files-statistics-and-reports)
- **Durham County**: [https://durhamnc.gov/346/GIS-Data](https://durhamnc.gov/346/GIS-Data)

### What to Download
- **Parcel Point Data** (centroids) - preferred, file pattern: `nc_[county]_parcels_pt.shp`
- Or **Parcel Polygon Data** (you can convert to points)
- Ensure the data includes property use descriptions

### File Placement
```
county_data/
├── Guilford/
│   └── nc_guilford_parcels_pt.shp  (and associated files)
├── Wake/
│   └── nc_wake_parcels_pt.shp
├── Durham/
│   └── nc_durham_parcels_pt.shp
└── [CountyName]/
    └── nc_[countyname]_parcels_pt.shp
```

### Key Columns Used
- `PARUSEDESC` - Property use description (varies by county)
- `ALTPARNO` / `NPARNO` - Parcel identification numbers
- `geometry` - Point locations (centroids)

### Important Notes
- **Property use codes vary significantly by county!** 
- The code filters for residential properties, but the exact values differ:
  - Guilford: `RESIDENTIAL`, `TOWNHOUSE`, `CONDO`, `APART`, etc.
  - Wake: `R`, `T`, `A`
  - Durham: `RES/ 1-FAMILY`, `RES/ 2-FAMILY`, etc.
- You may need to examine your specific county's data and update the filtering logic in the code
- File sizes vary: 10-200 MB depending on county

---

## 3. Hospital Data

### Source
**North Carolina OneMap**

### Download Location
- **Website**: [https://www.nconemap.gov/](https://www.nconemap.gov/)
- Search for: "Health facilities" or "Hospitals"
- Download as **Shapefile**

**Alternative Sources:**
- **NC DHHS**: Healthcare facility lists (may need geocoding)
- **HIFLD Open Data**: [https://hifld-geoplatform.opendata.arcgis.com/](https://hifld-geoplatform.opendata.arcgis.com/)

### What to Download
- Hospital point locations for North Carolina
- Ensure it includes facility names and addresses
- Verify data is recent (updated within last 2 years)

### File Placement
```
state_data/
└── NorthCarolina_Hospitals/
    └── Hospitals.shp  (and associated .shx, .dbf, .prj files)
```

### Key Columns Used
- `ID` or `OBJECTID` - Unique identifier
- `latitude` / `longitude` - Coordinates
- `fcounty` or `COUNTY` - County name (optional, for filtering)
- `hgenlic` or similar - Number of licensed beds/physicians (optional)
- `geometry` - Point locations

### Notes
- The code filters hospitals within a 30-40 mile buffer of the county centroid
- Ensure coordinate system matches (EPSG:4269)
- File size: typically <5 MB

---

## 4. OpenStreetMap (OSM) Data

### Source
**Geofabrik OpenStreetMap Extracts**

### Download Location
- **Website**: [https://download.geofabrik.de/north-america/us.html](https://download.geofabrik.de/north-america/us.html)
- Navigate to: North America → United States → North Carolina

### What to Download
- **North Carolina OSM extract** in `.osm.pbf` format
- File: `north-carolina-latest.osm.pbf`
- Size: ~150-300 MB (compressed)

### File Placement
```
state_data/
└── osm/
    └── NorthCarolina.osm.pbf
```

### Alternative: Custom Downloads
For smaller regions or specific areas:
- **BBBike**: [https://extract.bbbike.org/](https://extract.bbbike.org/)
- **HOT Export Tool**: [https://export.hotosm.org/](https://export.hotosm.org/)

### Notes
- The OSM file contains road network data used for routing
- Update frequency: Consider downloading updated versions periodically (every 3-6 months)
- The code parameter `--osm NorthCarolina` should match the filename (without extension)
- Contains all road types, bike paths, pedestrian paths, etc.

---

## Additional Data Sources and References

This project builds upon several publicly available geospatial datasets and resources:

### Transportation Disadvantage Context
**North Carolina Department of Transportation (NCDOT)**
- **Story Map of Transportation Disadvantage**: [https://storymaps.arcgis.com/stories/7e3bbd00fe014a77b5f1620334209712](https://storymaps.arcgis.com/stories/7e3bbd00fe014a77b5f1620334209712)
- Provides context and visualization of transportation challenges in North Carolina
- Useful for understanding regional patterns of accessibility

### Census Geography
**U.S. Census Bureau - TIGER/Line Shapefiles**
- **Website**: [https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html)
- Contains detailed geographic boundaries including:
  - Census tracts
  - Counties
  - Roads
  - Water features
- Primary source for census tract boundaries used in this analysis

### Social Vulnerability Index
**Centers for Disease Control and Prevention (CDC) / Agency for Toxic Substances and Disease Registry (ATSDR)**
- **Social Vulnerability Index (SVI)**: [https://www.atsdr.cdc.gov/placeandhealth/svi/](https://www.atsdr.cdc.gov/placeandhealth/svi/)
- Provides vulnerability metrics at census tract level
- Updated annually with latest Census data
- See [SVI Documentation](https://www.atsdr.cdc.gov/placeandhealth/svi/documentation/SVI_documentation_2020.html) for methodology

### Geospatial Data Portal
**North Carolina OneMap**
- **Website**: [https://www.nconemap.gov/](https://www.nconemap.gov/)
- Comprehensive portal for North Carolina GIS data
- Includes parcels, infrastructure, administrative boundaries, and more
- Primary source for parcel data and hospital data used in this analysis

### Topographic and Base Maps
**U.S. Geological Survey (USGS) - The National Map**
- **Website**: [https://www.usgs.gov/programs/national-geospatial-program/national-map](https://www.usgs.gov/programs/national-geospatial-program/national-map)
- Provides topographic data, elevation models, and ortho-imagery
- Useful for visualization and context mapping
- Optional for this analysis but valuable for presentations

### OpenStreetMap
**Geofabrik & OSM Contributors**
- **Download Portal**: [https://download.geofabrik.de/](https://download.geofabrik.de/)
- **OSM Wiki**: [https://wiki.openstreetmap.org/](https://wiki.openstreetmap.org/)
- Community-maintained road network data
- Essential for routing and travel time calculations
- Updated regularly by contributors worldwide

---

## Data Citation

When using this analysis or data in publications, please cite:

1. **Social Vulnerability Index**:
   Centers for Disease Control and Prevention (CDC), and Agency for Toxic Substances and Disease Registry (ATSDR). Social Vulnerability Index (SVI). 2024. https://www.atsdr.cdc.gov/placeandhealth/svi/

2. **Census TIGER/Line Shapefiles**:
   U.S. Census Bureau. TIGER/Line Shapefiles. 2020. https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html

3. **North Carolina OneMap**:
   North Carolina OneMap. North Carolina OneMap Dataset. 2024. https://www.nconemap.gov/

4. **OpenStreetMap**:
   OpenStreetMap contributors. 2024. https://www.openstreetmap.org

5. **Hospital Data**:
   North Carolina OneMap. Hospital and Healthcare Facilities Dataset. 2024. https://www.nconemap.gov/

6. **NCDOT Transportation Disadvantage** (for context):
   North Carolina Department of Transportation (NCDOT). A Story Map of Transportation Disadvantage. n.d. https://storymaps.arcgis.com/stories/7e3bbd00fe014a77b5f1620334209712

---

## Complete Folder Structure

After downloading and processing all data, your directory should look like this:

```
accessibility/
├── county_data/
│   ├── Guilford/
│   │   ├── nc_guilford_parcels_pt.shp
│   │   ├── Option1_county_centroids.csv        (generated by scripts)
│   │   ├── Option2_county_centroids.csv        (generated by scripts)
│   │   ├── Option3_residential_parcel_centroids.csv  (generated by scripts)
│   │   └── hospitals_within_buffer.csv         (generated by scripts)
│   ├── Wake/
│   │   └── nc_wake_parcels_pt.shp
│   └── [OtherCounties]/
│
├── state_data/
│   ├── SVI_NorthCarolina_SHP.shp  (and .shx, .dbf, .prj) [GENERATED BY MERGE]
│   ├── SVI_NorthCarolina_SHP.geojson  [GENERATED BY MERGE]
│   ├── SVI_NorthCarolina_SHP.gpkg  [GENERATED BY MERGE]
│   ├── NorthCarolina_Hospitals/
│   │   └── Hospitals.shp  (and .shx, .dbf, .prj)
│   └── osm/
│       └── NorthCarolina.osm.pbf
│
├── working_directory/  (for SVI data preparation)
│   ├── tl_2020_37_tract.shp  [DOWNLOAD FROM CENSUS]
│   ├── tl_2020_37_tract.shx
│   ├── tl_2020_37_tract.dbf
│   ├── tl_2020_37_tract.prj
│   ├── NorthCarolina.csv  [DOWNLOAD FROM CDC]
│   └── merge_detailed_with_explanations.py  [PROVIDED SCRIPT]
│
├── src/
│   ├── 1_geopandas_analysis.py
│   ├── 2_travel_times_analysis.py
│   ├── 3_file_evaluator.py
│   └── 4_plots_histogram.py
│
├── requirements.txt
├── INSTALLATION.md
├── DATA_SOURCES.md  (this file)
└── README.md
```

---

## Data Preparation Checklist

### SVI Data (3 steps):
- [ ] Download census tract shapefile from Census Bureau (tl_2020_37_tract.zip)
- [ ] Download SVI CSV data from CDC (NorthCarolina.csv)
- [ ] Run merge script (`merge_detailed_with_explanations.py`)
- [ ] Verify merged output in state_data/ folder
- [ ] Check that output has ~2,660 census tracts

### Other Data:
- [ ] Download parcel point data for your county of interest
- [ ] Download hospital shapefile for North Carolina
- [ ] Download OSM extract for North Carolina
- [ ] Verify all shapefiles have associated .shx, .dbf, and .prj files
- [ ] Check coordinate systems (should be EPSG:4269 or EPSG:4326)
- [ ] Examine parcel data `PARUSEDESC` column values
- [ ] Update code filtering logic if needed for your specific county
- [ ] Create folder structure as shown above

---

## Data Usage Notes

### Coordinate Reference Systems
- **Input CRS**: Most NC data uses EPSG:4269 (NAD83) or EPSG:4326 (WGS84)
- **Processing CRS**: Scripts convert to EPSG:4269
- **Web Maps**: EPSG:3857 (Web Mercator) for visualization

### File Sizes
Approximate sizes to expect:
- Census Tract Shapefile: ~5-10 MB
- SVI CSV: ~2-5 MB
- Merged SVI Shapefile: ~5-20 MB
- County Parcel Data: 10-200 MB (varies by county)
- Hospital Data: <5 MB
- OSM North Carolina: 150-300 MB

### Data Updates
- **Census Tracts**: Every 10 years (decennial census), use 2020 data
- **SVI**: Updated annually, use most recent year
- **Parcels**: Updated quarterly/annually by counties
- **Hospitals**: Verify current facilities, update annually
- **OSM**: Updated continuously, download recent extract (every 3-6 months)

### Privacy and Usage
- All data sources are public domain or openly licensed
- Parcel data: Public records, but respect privacy in publications
- Follow attribution requirements for OSM data
- Cite data sources in academic publications

---

## Troubleshooting

### Common Issues

**1. SVI Merge Script Errors**
- Error: "File not found"
- Solution: Check paths in configuration section, use absolute paths

**2. Shapefile Missing Components**
- Error: "Unable to open shapefile"
- Solution: Ensure .shp, .shx, .dbf, and .prj files are all present

**3. FIPS/GEOID Mismatch**
- Error: "No matching records"
- Solution: Verify both files are for North Carolina (state FIPS 37), check that census tract shapefile and SVI CSV are same year

**4. Coordinate System Mismatch**
- Error: Points not matching polygons
- Solution: Check CRS of all files, reproject if needed

**5. Empty Results After Filtering**
- Error: "No residential parcels found"
- Solution: Check `PARUSEDESC` values in your parcel data, update filter

**6. OSM File Not Found**
- Error: "Cannot find OSM file"
- Solution: Verify filename matches the `--osm` parameter (without .osm.pbf extension)

---

## Additional Resources

### North Carolina Specific
- **NC GIS Central**: [https://www.nc.gov/services/gis](https://www.nc.gov/services/gis)
- **NC OneMap**: [https://www.nconemap.gov/](https://www.nconemap.gov/)
- **NCDOT Story Map - Transportation Disadvantage**: [https://storymaps.arcgis.com/stories/7e3bbd00fe014a77b5f1620334209712](https://storymaps.arcgis.com/stories/7e3bbd00fe014a77b5f1620334209712)

### Data Documentation
- **CDC SVI Documentation**: [https://www.atsdr.cdc.gov/placeandhealth/svi/documentation/SVI_documentation_2020.html](https://www.atsdr.cdc.gov/placeandhealth/svi/documentation/SVI_documentation_2020.html)
- **Census TIGER/Line Documentation**: [https://www.census.gov/programs-surveys/geography/technical-documentation/complete-technical-documentation/tiger-geo-line.html](https://www.census.gov/programs-surveys/geography/technical-documentation/complete-technical-documentation/tiger-geo-line.html)
- **TIGER/Line Shapefiles**: [https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html)
- **USGS National Map**: [https://www.usgs.gov/programs/national-geospatial-program/national-map](https://www.usgs.gov/programs/national-geospatial-program/national-map)

### Python Geospatial Tools
- **GeoPandas Documentation**: [https://geopandas.org/](https://geopandas.org/)
- **QGIS Tutorials**: [https://www.qgistutorials.com/](https://www.qgistutorials.com/)

### OpenStreetMap Resources
- **OSM Wiki**: [https://wiki.openstreetmap.org/](https://wiki.openstreetmap.org/)
- **Geofabrik Downloads**: [https://download.geofabrik.de/](https://download.geofabrik.de/)
- **OSM Data Attribution**: [https://www.openstreetmap.org/copyright](https://www.openstreetmap.org/copyright)

---

## Contact

If you encounter issues downloading or processing data:
1. Check the troubleshooting section above
2. Verify file paths and folder structure
3. Review the county-specific code in the scripts
4. Open an issue on GitHub with details about your data source

---

**Last Updated**: December 2024

**Data Sources**:
- U.S. Census Bureau - TIGER/Line Shapefiles (census tract boundaries)
- Centers for Disease Control and Prevention (CDC)/ATSDR - Social Vulnerability Index
- North Carolina OneMap - Parcel, hospital, and geospatial data
- OpenStreetMap/Geofabrik - Road network data
- NCDOT - Transportation disadvantage context
- USGS - National Map and topographic data

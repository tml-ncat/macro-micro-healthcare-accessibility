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

### Source
**CDC/ATSDR Social Vulnerability Index (SVI)**

### Download Location
- **Official Website**: [https://www.atsdr.cdc.gov/place-health/php/svi/svi-data-documentation-download.html?CDC_AAref_Val=https://www.atsdr.cdc.gov/placeandhealth/svi/data_documentation_download.html]
- **Direct Download**: Select your state and year (recommend 2020 or latest)

### What to Download
- Download the **Shapefile format** for North Carolina
- File name pattern: `SVI[Year]_NORTHCAROLINA.zip` or similar

### File Placement
```
state_data/
└── SVI_NorthCarolina_SHP.shp  (and associated .shx, .dbf, .prj files)
```

### Key Columns Used
- `COUNTY` - County name
- `E_NOVEH` - Estimate of households with no vehicle
- `M_NOVEH` - Margin of error for E_NOVEH
- `E_DISABL` - Estimate of civilian noninstitutionalized population with a disability
- `OBJECTID` - Unique identifier
- `geometry` - Census tract boundaries

### Notes
- Ensure you download the **census tract level** data, not county level
- The shapefile should include all counties in North Carolina
- Coordinate Reference System (CRS) should be EPSG:4269 (NAD83)

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

---

## 3. Hospital Data

### Source
**North Carolina OneMap**

### Download Location
- **Website**: [https://www.nconemap.gov/](https://www.nconemap.gov/)
- Search for: "Health facilities" or "Hospitals"
- Download as **Shapefile**

### What to Download
- Hospital point locations for North Carolina
- Ensure it includes facility names and addresses

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
- Update frequency: Consider downloading updated versions periodically
- The code parameter `--osm NorthCarolina` should match the filename (without extension)

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
- Alternative source for census tract boundaries (SVI data already includes these)

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
- Primary source for parcel data used in this analysis

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

### Hospital and Healthcare Facilities
**North Carolina OneMap**
- **Website**: [https://www.nconemap.gov/](https://www.nconemap.gov/)
- Search for: "Health facilities" or "Hospitals"  
- Comprehensive database of healthcare facilities in North Carolina
- Download as shapefile format
- Primary source for hospital locations used in this analysis

---

## Data Citation

When using this analysis or data in publications, please cite:

1. **Social Vulnerability Index**:
   Centers for Disease Control and Prevention (CDC), and Agency for Toxic Substances and Disease Registry (ATSDR). Social Vulnerability Index (SVI). 2024. https://www.atsdr.cdc.gov/placeandhealth/svi/

2. **North Carolina OneMap**:
   North Carolina OneMap. North Carolina OneMap Dataset. 2024. https://www.nconemap.gov/

3. **TIGER/Line Shapefiles** (if used):
   U.S. Census Bureau. TIGER/Line Shapefiles. 2023. https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html

4. **OpenStreetMap**:
   OpenStreetMap contributors. 2024. https://www.openstreetmap.org

5. **Hospital Data**:
   North Carolina OneMap. Hospital and Healthcare Facilities Dataset. 2024. https://www.nconemap.gov/

6. **NCDOT Transportation Disadvantage** (for context):
   North Carolina Department of Transportation (NCDOT). A Story Map of Transportation Disadvantage. n.d. https://storymaps.arcgis.com/stories/7e3bbd00fe014a77b5f1620334209712

---

## Complete Folder Structure

After downloading all data, your directory should look like this:

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
│   ├── SVI_NorthCarolina_SHP.shp  (and .shx, .dbf, .prj)
│   ├── NorthCarolina_Hospitals/
│   │   └── Hospitals.shp  (and .shx, .dbf, .prj)
│   └── osm/
│       └── NorthCarolina.osm.pbf
│
├── src/
│   ├── 1_prepare_spatial_data.py
│   ├── 2_compute_travel_times.py
│   ├── 3_aggregate_results.py
│   └── 4_plot_histogram.py
│
├── requirements.txt
├── INSTALLATION.md
├── DATA_SOURCES.md  (this file)
└── README.md
```

---

## Data Preparation Checklist

- [ ] Download SVI shapefile for North Carolina
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
- SVI Shapefile: ~5-20 MB
- County Parcel Data: 10-200 MB (varies by county)
- Hospital Data: <5 MB
- OSM North Carolina: 150-300 MB

### Data Updates
- **SVI**: Updated annually, use most recent year
- **Parcels**: Updated quarterly/annually by counties
- **Hospitals**: Verify current facilities
- **OSM**: Updated continuously, download recent extract

### Privacy and Usage
- All data sources are public domain or openly licensed
- Parcel data: Public records, but respect privacy in publications
- Follow attribution requirements for OSM data
- Cite data sources in academic publications

---

## Troubleshooting

### Common Issues

**1. Shapefile Missing Components**
- Error: "Unable to open shapefile"
- Solution: Ensure .shp, .shx, .dbf, and .prj files are all present

**2. Coordinate System Mismatch**
- Error: Points not matching polygons
- Solution: Check CRS of all files, reproject if needed

**3. Empty Results After Filtering**
- Error: "No residential parcels found"
- Solution: Check `PARUSEDESC` values in your parcel data, update filter

**4. OSM File Not Found**
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
- **TIGER/Line Shapefiles**: [https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html)
- **USGS National Map**: [https://www.usgs.gov/programs/national-geospatial-program/national-map](https://www.usgs.gov/programs/national-geospatial-program/national-map)

### OpenStreetMap Resources
- **OSM Wiki**: [https://wiki.openstreetmap.org/](https://wiki.openstreetmap.org/)
- **Geofabrik Downloads**: [https://download.geofabrik.de/](https://download.geofabrik.de/)
- **OSM Data Attribution**: [https://www.openstreetmap.org/copyright](https://www.openstreetmap.org/copyright)

---

## Contact

If you encounter issues downloading or processing data:
1. Check the troubleshooting section above
2. Review the county-specific code in the scripts
3. Open an issue on GitHub with details about your data source

---

**Last Updated**: December 2024

**Data Sources**:
- Centers for Disease Control and Prevention (CDC)/ATSDR - Social Vulnerability Index
- North Carolina OneMap - Parcel, hospital, and geospatial data
- U.S. Census Bureau - TIGER/Line Shapefiles and census geography
- OpenStreetMap/Geofabrik - Road network data
- NCDOT - Transportation disadvantage context
- USGS - National Map and topographic data

# Installation Guide for Healthcare Accessibility Analysis

## Quick Start
To install all required packages, run:
```bash
pip install -r requirements.txt
```

## System Dependencies
Before installing Python packages, you may need to install system-level dependencies:

### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install -y \
    python3-dev \
    libgeos-dev \
    libproj-dev \
    libgdal-dev \
    libspatialindex-dev
```

### macOS (using Homebrew):
```bash
brew install geos proj gdal spatialindex
```

### Windows:
Consider using Conda/Anaconda for easier installation of geospatial packages:
```bash
conda install -c conda-forge geopandas r5py contextily
```

## Installation Notes

### r5py Specific Requirements
- r5py requires Java Development Kit (JDK) 11 or higher
- Install Java:
  - **Ubuntu/Debian**: `sudo apt-get install openjdk-11-jdk`
  - **macOS**: `brew install openjdk@11`
  - **Windows**: Download from [Oracle](https://www.oracle.com/java/technologies/downloads/) or [AdoptOpenJDK](https://adoptopenjdk.net/)

### Potential Issues and Solutions

1. **GEOS/PROJ/GDAL Errors**:
   - If you encounter errors related to GEOS, PROJ, or GDAL, install the system dependencies first
   - Alternatively, use conda: `conda install -c conda-forge geopandas`

2. **r5py Installation Issues**:
   - Ensure Java is properly installed and JAVA_HOME is set
   - Check Java version: `java -version` (should be 11+)
   - Set JAVA_HOME if needed:
     ```bash
     export JAVA_HOME=/path/to/java
     ```

3. **Rtree Installation Issues**:
   - Requires libspatialindex-dev system library
   - On Ubuntu: `sudo apt-get install libspatialindex-dev`

4. **Contextily Basemap Issues**:
   - Requires internet connection to download basemaps
   - May need to set cache directory: `export CONTEXTILY_CACHE_DIR=/path/to/cache`

## Virtual Environment (Recommended)
It's recommended to use a virtual environment:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate  # Windows

# Install requirements
pip install -r requirements.txt
```

## Verify Installation
Test your installation with:

```python
import geopandas
import r5py
import shapely
import contextily
import pandas
import numpy
import matplotlib.pyplot as plt
import chardet

print("All packages imported successfully!")
```

## Package Descriptions

### Core Geospatial Libraries
- **geopandas**: Geospatial data handling and analysis (used in spatial preprocessing)
- **shapely**: Geometric operations (used for point and polygon manipulations)
- **r5py**: Routing engine for calculating travel times (core analysis tool)
  - GitHub: https://github.com/r5py/r5py
  - DOI: https://doi.org/10.5281/zenodo.7060438
  - Citation: Fink, C., W. Klumpenhouwer, M. Saraiva, R. Pereira, and H. Tenkanen. r5py: Rapid Realistic Routing with R5 in Python. Version 0.0.4, 2022.
- **rtree**: Spatial indexing for efficient spatial joins (required for geopandas.sjoin)

### Data Processing
- **pandas**: Data manipulation and CSV handling
- **numpy**: Numerical operations and statistics

### Visualization
- **matplotlib**: Plotting histograms and box plots for figures
- **contextily**: Basemap tiles for choropleth maps

### Utilities
- **chardet**: Character encoding detection for CSV files

### Dependencies (Automatically Installed by pip)
These packages are automatically installed when you install the packages above:
- **pyproj**: Cartographic projections (installed with geopandas)
- **fiona**: Vector data I/O (installed with geopandas)
- **Pillow**: Image processing (installed with contextily)

**Note:** While these are listed in requirements.txt for version pinning, pip will install them automatically as dependencies.

## Data Requirements

In addition to Python packages, you'll need:

1. **OpenStreetMap (OSM) network data** (`.osm.pbf` format)
2. **Census tract shapefiles** with Social Vulnerability Index (SVI) data
3. **Parcel data shapefiles** for your counties of interest
4. **Hospital location data** (shapefile format)

See `Data_sources.md` for details on obtaining these datasets.

## Citation

If you use this code, please cite our paper:

Gulati, K., Pandey, V., Manikkavasagam, N., Reginato Junior, A., Lidbe, A., & Nagarajan, S. (2025). Comparative Analysis of Macro- and Micro-Level Measures of Healthcare Access in Urban and Rural Areas. *Transportation Research Record*. https://doi.org/10.1177/03611981251380266

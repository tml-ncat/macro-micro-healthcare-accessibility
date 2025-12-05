# Installation Guide for Transportation Accessibility Analysis

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
conda install -c conda-forge geopandas r5py contextily osmnx
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
import osmnx
import contextily
print("All packages imported successfully!")
```

## Package Descriptions

- **geopandas**: Geospatial data handling and analysis
- **r5py**: Routing engine for multimodal transport networks
- **shapely**: Geometric operations
- **pandas/numpy**: Data manipulation and numerical operations
- **matplotlib**: Plotting and visualization
- **folium**: Interactive web maps
- **contextily**: Basemap tiles for static maps
- **osmnx**: OpenStreetMap data retrieval and network analysis
- **networkx**: Graph/network analysis
- **chardet**: Character encoding detection
- **pyproj**: Cartographic projections
- **rtree**: Spatial indexing
- **fiona**: Vector data I/O
- **Pillow**: Image processing

# Citation

If you use this code, please cite our paper:

Gulati, K., Pandey, V., Manikkavasagam, N., Reginato Junior, A., Lidbe, A., & Nagarajan, S. (2025). Comparative Analysis of Macro- and Micro-Level Measures of Healthcare Access in Urban and Rural Areas. *Transportation Research Record*. https://doi.org/10.1177/03611981251380266

# Instructions to run the code

## Prepare the Inputs
Note that following the folder structure is essential for code to run and read files correctly.

1. Load the input files correctly (some of the files are downloadable from the web or ask the author). This includes:
   + `SVI_NorthCarolina_SHP.shp` file in the `state_data/` folder (along with other related files `.prj`,`.shx`,...)
   + `NorthCarolina.osm.pbf` in `state_data/osm/` folder
   + `Hospitals.shp` file in the `state_data/NorthCarolina_Hospitals/` folder
2. Create a new folder for the desired county under the `county_data` folder and add the parcel data point and polygon shape files downloadable from NC OneMap.

## Assess the columns in parcel data and generate `.csv` inputs for travel time analysis
1. First, run the `geopandas_analysis.py` code that will break if the appropriate columns are not chosen.
   ```
   python src/geopandas_analysis.py --county_name Bladen --state_name NorthCarolina
   ```
3. Then, edit the code by adding `elif` part around line 85 in `geopandas_analysis.py` and select the appropriate columns to write. Then run the above code again.

## Conduct `r5py` analysis
Second, you perform the travel time analysis for all three options. Depending on the size of the osm file, the file reading and network preparation may take 200 or so seconds. 
```
python src/travel_time_analysis.py --county_name Bladen --state_name NorthCarolina --option 1 --osm NorthCarolina
```
```
python src/travel_time_analysis.py --county_name Bladen --state_name NorthCarolina --option 2 --osm NorthCarolina
```
```
python src/travel_time_analysis.py --county_name Bladen --state_name NorthCarolina --option 3 --osm NorthCarolina
```

## Finally, generate plots

```
python src/plots.py --county_name guilford --file_name Option3_aggregated_information_181706locations_to_17hospitals__1720014810
```



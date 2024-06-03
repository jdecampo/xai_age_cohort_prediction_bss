##################################################################################
#                     Load 201905 BiciMad station status                         #
#                            Data exploration                                    #
# Data source: https://opendata.emtmadrid.es/Datos-estaticos/Datos-generales-(1) #
##################################################################################


# Load libraries
import pandas as pd


# Load files
bike_stop = "add_path_flat_file"
bike_df = pd.read_json(bike_stop, lines=True, encoding="unicode_escape")


# Create an expanded DataFrame with '_id' as a unique identifier
df_expanded = pd.DataFrame(
    {
        "_id": bike_df["_id"].repeat(bike_df["stations"].apply(len)),
        "stations": bike_df["stations"].explode(),
    }
)

# Reset the index of df_expanded
df_expanded.reset_index(drop=True, inplace=True)

# Extract values from the JSON list column
normalized_data = pd.json_normalize(df_expanded["stations"], sep="_")

# Concatenate the original DataFrame and the new columns
station_status = pd.concat([df_expanded["_id"], normalized_data], axis=1)

# Display the resulting DataFrame
station_status.head()
station_status["id"].unique()


# Master Data Station id + address:
station_status_filtered = station_status.drop_duplicates(subset="id", keep="first")
station_status_filtered.shape

station_status_filtered.groupby("id")[["latitude", "longitude"]]


###############################################
# Load and merge 2019 bicimad station status  #
###############################################

import os
import glob
import pandas as pd
import time

# Supporting functions:

pd.set_option("display.max_columns", None)

path_to_json = "add_path_flat_files"


# Measure time to merge files
start_time = time.time()

# Load all JSON files from the specified folder
file_list = glob.glob(os.path.join(path_to_json, "*.json"))

print("List of JSON files found:")
print(file_list)

# Values to check in the file name
values_to_check = ["201903", "201907", "201908", "201909", "201910", "201911", "201912"]

if not file_list:
    print("No JSON files found.")
else:
    dfs = []  # an empty list to store the data frames
    column_names_set = set()  # to store column names for validation

    for file in file_list:

        data = pd.read_json(
            file, lines=True, encoding="unicode_escape"
        )  # read data frame from json file
        df_expanded = pd.DataFrame(
            {
                "_id": data["_id"].repeat(data["stations"].apply(len)),
                "stations": data["stations"].explode(),
            }
        )
        # Reset the index of df_expanded
        df_expanded.reset_index(drop=True, inplace=True)

        # Extract values from the JSON list column
        normalized_data = pd.json_normalize(df_expanded["stations"], sep="_")

        # Concatenate the original DataFrame and the new columns
        station_status = pd.concat([df_expanded["_id"], normalized_data], axis=1)

        # Validate column names before appending
        if not column_names_set:
            column_names_set.update(station_status.columns)
        elif column_names_set != set(station_status.columns):
            print(f"Column mismatch in file: {file}. Skipping.")
            continue

        dfs.append(station_status)  # append the data frame to the list

    if dfs:
        merged_df = pd.concat(
            dfs, ignore_index=True
        )  # concatenate all the data frames in the list.
        # Now, 'merged_df' contains the combined data from all JSON files
        print(merged_df.head())  # Print the first few rows for verification
    else:
        print("No valid data frames to concatenate.")


# Measure time to merge files
end_time = time.time()

concat_md_bicimad_station_time = end_time - start_time

print(concat_md_bicimad_station_time)
print(merged_df.shape)
print(merged_df.head())
print(len(merged_df["id"].unique()))

# Save entire files in one dataset
merged_df.to_csv("bike_station_status_2019.csv", index=False, sep=";")


#########################
# md stations location  #
#########################

# Load libraries
import pandas as pd


# Load files
md_stations = "path_flat_file_/bike_station_status_2019.csv"
station_status_df = pd.read_csv(md_stations, header=0, sep=";")

print(station_status_df.shape)
print(station_status_df.head())
print(station_status_df["id"].unique())

# Master Data Station id + address:
md_bike_stations = station_status_df.drop_duplicates(subset="id", keep="first")

# Drop columns that are not relevant for Master Data table:
columns_to_drop = [
    "activate",
    "reservations_count",
    "light",
    "free_bases",
    "no_available",
    "dock_bikes",
]
md_bike_stations = md_bike_stations.drop(columns=columns_to_drop)
print(md_bike_stations.head())

# Change master data column order
columns_to_order = [
    "id",
    "number",
    "name",
    "address",
    "latitude",
    "longitude",
    "_id",
    "total_bases",
]
md_bike_stations = md_bike_stations[columns_to_order]
print(md_bike_stations.head())

# Create support columns to merge dataframes
md_bike_stations["idunplug_station"] = md_bike_stations["id"]
md_bike_stations["unplug_station_tot_bases"] = md_bike_stations["total_bases"]
md_bike_stations["idunplug_latitude"] = md_bike_stations["latitude"]
md_bike_stations["idunplug_longitude"] = md_bike_stations["longitude"]

md_bike_stations["idplug_station"] = md_bike_stations["id"]
md_bike_stations["plug_station_tot_bases"] = md_bike_stations["total_bases"]
md_bike_stations["idplug_latitude"] = md_bike_stations["latitude"]
md_bike_stations["idplug_longitude"] = md_bike_stations["longitude"]

print(md_bike_stations.head())
print(len(md_bike_stations["id"].unique()))


# Based on usage data station id 23 and 24 to be removed as the street was under construction for entire 2019
md_bike_stations = md_bike_stations[~md_bike_stations["id"].isin([23, 24])]


print(md_bike_stations.head())
print(md_bike_stations["_id"].unique())

# Save file to csv
md_bike_stations.to_csv("md_bike_station_2019.csv", index=False, sep=";")

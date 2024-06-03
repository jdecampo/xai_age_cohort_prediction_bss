# Data source: https://opendata.emtmadrid.es/Datos-estaticos/Datos-generales-(1)

# Import libraries
import os
import glob
import pandas as pd
import time

# Supporting functions:


# Function used to overcome 'unplug_hourTime' specific format for 201903 flat file.
def remove_last_n_chars(column):
    return column.str[:-9]


pd.set_option("display.max_columns", None)

path_to_json = "add_path_flat_file"


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
        # check files with names containing the specified values with the new file structure
        if any(value in file for value in values_to_check):
            # Set up specific step for 201903 due to specific date format requirement
            if "201903" in file:
                print(
                    f"Fixing: {file} as 'unplug_hourTime' contains a specific structure in '201903'."
                )
                data = pd.read_json(file, lines=True, encoding="unicode_escape")
                print(f"Removing 'track' column from file: {file}.")
                data = data.drop("track", axis=1)
                print(f"Extracting '_id' column from file: {file}.")
                data["_id"] = data["_id"].apply(pd.Series)["$oid"]
                print(f"Extracting 'unplug_hourTime' column from file: {file}.")
                data["unplug_hourTime"] = data["unplug_hourTime"].apply(pd.Series)[
                    "$date"
                ]
                data["temp_unplug_hourTime"] = remove_last_n_chars(
                    data["unplug_hourTime"]
                )
                data["temp_unplug_hourTime"] = pd.to_datetime(
                    data["temp_unplug_hourTime"]
                )
                print(f"Updating file: {file} adding year, month, day, hour columns.")
                data["year"] = data["temp_unplug_hourTime"].dt.year
                data["month"] = data["temp_unplug_hourTime"].dt.month
                data["day"] = data["temp_unplug_hourTime"].dt.day
                data["hour"] = data["temp_unplug_hourTime"].dt.hour
                dfs.append(data)
                continue
            data = pd.read_json(file, lines=True, encoding="unicode_escape")
            print(f"Updating file: {file} as it contains one of the specified values.")
            data["_id"] = data["_id"].apply(pd.Series)["$oid"]
            print(f"Updating file: {file} adding year, month, day, hour columns.")
            # Convert unplug_hourTime to pd datetime
            data["temp_unplug_hourTime"] = pd.to_datetime(
                data["unplug_hourTime"], format="ISO8601"
            )
            # Adding new columns extracting year, month, day, hour from temp_unplug_hourTime column
            data["year"] = data["temp_unplug_hourTime"].dt.year
            data["month"] = data["temp_unplug_hourTime"].dt.month
            data["day"] = data["temp_unplug_hourTime"].dt.day
            data["hour"] = data["temp_unplug_hourTime"].dt.hour
            dfs.append(data)
            continue

        data = pd.read_json(
            file, lines=True, encoding="unicode_escape"
        )  # read data frame from json file

        # Check if 'track' column is present in the DataFrame as column only present from 201901:201906
        if "track" in data.columns:
            print(f"Removing 'track' column from file: {file}.")
            data = data.drop("track", axis=1)
            # In files with 'track' column, '_id' column is in a dict
            print(f"Extracting '_id' column from file: {file}.")
            data["_id"] = data["_id"].apply(pd.Series)["$oid"]
            # In files with 'track' column, 'unplug_hourTime' column is in a dict
            print(f"Extracting 'unplug_hourTime' column from file: {file}.")
            data["unplug_hourTime"] = data["unplug_hourTime"].apply(pd.Series)["$date"]
            print(
                f"Converting 'unplug_hourTime' column from file: {file} to datetime, adding year, month, day, hour column."
            )
            # Convert unplug_hourTime to pd datetime
            data["temp_unplug_hourTime"] = pd.to_datetime(
                data["unplug_hourTime"], format="ISO8601"
            )
            # Adding new columns extracting year, month, day, hour from temp_unplug_hourTime column
            data["year"] = data["temp_unplug_hourTime"].dt.year
            data["month"] = data["temp_unplug_hourTime"].dt.month
            data["day"] = data["temp_unplug_hourTime"].dt.day
            data["hour"] = data["temp_unplug_hourTime"].dt.hour

        # Validate column names before appending
        if not column_names_set:
            column_names_set.update(data.columns)
        elif column_names_set != set(data.columns):
            print(f"Column mismatch in file: {file}. Skipping.")
            continue

        dfs.append(data)  # append the data frame to the list

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

concat_bike_movement_time = end_time - start_time

print(concat_bike_movement_time)
print(merged_df.shape)


# Save entire files in one dataset
merged_df.to_csv("bike_movements_2019.csv", index=False, sep=";")

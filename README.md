# python-neo-data-pipeline
Implementation of a data pipeline that acquires information of nearby objects through NASA's NeoWs API and stores it in parquet file


## Folder structure
root
 |--app
 |   |--app.py
 |--src
 |   |--near_earth_objects.py
 |   |--settings.py
 |   |--utils.py

### app.py
 - Run the pipeline through this file, using the NeoWsDataPipeline class

### near_earth_objects.py
 - This file contains the implementation of the NeoWsDataPipeline class
   - acquire_feed_data(): This function is responsible for fetching the api data and storing it in json format in the raw_data directory
   - process_data(): This function processes the data in json format and transforms into parquet

### settings.py
 - This file is responsible for loading the environment variables from the .env file

### utils.py
 - Some useful functions


## Packages used

### pyspark
 - Used to transform raw data into parquet

### requests
 - Used to access API data

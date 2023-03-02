# python-neo-data-pipeline
Implementation of a data pipeline that acquires information of nearby objects through NASA's NeoWs API and stores it in parquet file


## Folder structure
root
 |--src
 |   |--app
 |   |   |--app.py
 |   |   |--celery.py
 |   |--entities
 |   |   |--near_earth_objects.py
 |   |--functions
 |   |   |--neo.py
 |   |--services
 |   |   |--shared
 |   |   |   |--singleton_meta.py
 |   |   |--logger.py
 |   |--utils
 |   |   |--date.py
 |   |   |--exec_task.py
 |   |   |--folder.py
 |   |--settings.py

### app.py
 - Run the pipeline through this file for tests, using the NeoWsDataPipeline class

### celery.py
 - Task scheduler implementation

### near_earth_objects.py
 - This file contains the implementation of the NeoWsDataPipeline class
   - acquire_feed_data(): This function is responsible for fetching the api data and storing it in json format in the raw_data directory
   - process_data(): This function processes the data in json format and transforms into parquet

### neo.py
 - Contains the functions called by the task scheduler

### singleton_meta.py
 - Metaclass for singleton implementation

### logger.py
 - Just a logger function

### date.py
 - Date functions

### exec_task.py
 - Caller function for scheduled tasks with running time, logger and error handling

### folder.py
 - Folder functions

### settings.py
 - This file is responsible for loading the environment variables from the .env file

## Packages used

### celery
 - Used to schedule tasks

### pyspark
 - Used to transform raw data into parquet

### python-decouple
 - Used to read environment variables

### redis
 - Transport broker for celery

### requests
 - Used to access API data

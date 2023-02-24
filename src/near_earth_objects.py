import json
from requests import get
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.types import *
from src.settings import *
from src.utils import *

neo_api_feed_schema = StructType([
    StructField('id', StringType(), False),
    StructField('name', StringType(), False),
    StructField('absolute_magnitude_h', FloatType()),
    StructField('is_potentially_hazardous_asteroid', BooleanType()),
    StructField('is_sentry_object', BooleanType()),
    StructField('estimated_diameter', StructType([
        StructField('kilometers', StructType([
            StructField('estimated_diameter_min', DoubleType()),
            StructField('estimated_diameter_max', DoubleType())
        ]))
    ])),
    StructField('close_approach_data', ArrayType(StructType([
        StructField('close_approach_date', StringType()),
        StructField('relative_velocity', StructType([
            StructField('kilometers_per_second', StringType())
        ])),
        StructField('miss_distance', StructType([
            StructField('kilometers', StringType())
        ])),
        StructField('orbiting_body', StringType())
    ])))
])

class NeoWsDataPipeline:
    def __init__(self, search_at):
        self.__search_at = search_at
        self.__feed_api_url = f'{NASA_NEO_API_URL}/feed?start_date={search_at}&end_date={search_at}&api_key={NASA_API_KEY}'

        verify_folder_and_create_if_not_exists(RAW_FOLDER)
        verify_folder_and_create_if_not_exists(PROCESSED_FOLDER)
    
    def acquire_feed_data(self):
        response = get(self.__feed_api_url)
        api_data = json.loads(response.text)

        for key, value in api_data['near_earth_objects'].items():
            with open(f'{RAW_FOLDER}/{key}.json', 'w') as json_file:
                json.dump(value, json_file)

    def process_data(self):
        raw_file = open(f'{RAW_FOLDER}/{self.__search_at}.json')
        raw_data = json.load(raw_file)

        spark = SparkSession.builder.appName('NEO').getOrCreate()

        df_neo_api_raw_data = spark.createDataFrame(raw_data, neo_api_feed_schema)
        df_neo_exploded_data = df_neo_api_raw_data.withColumn('close_approach_data', explode('close_approach_data'))
        df_neo_table = df_neo_exploded_data.withColumns({
            'estimated_diameter_min_km': 'estimated_diameter.kilometers.estimated_diameter_min',
            'estimated_diameter_max_km': 'estimated_diameter.kilometers.estimated_diameter_max',
            'close_approach_date': 'close_approach_data.close_approach_date',
            'relative_velocity_km_per_second': 'close_approach_data.relative_velocity.kilometers_per_second',
            'miss_distance_km': 'close_approach_data.miss_distance.kilometers',
            'orbiting_body': 'close_approach_data.orbiting_body'
        }).drop('estimated_diameter').drop('close_approach_data')
        df_neo_table_typed = df_neo_table.withColumns({
            'close_approach_date': df_neo_table.close_approach_date.cast(DateType()),
            'relative_velocity_km_per_second': df_neo_table.relative_velocity_km_per_second.cast(DecimalType(30,10)),
            'miss_distance_km': df_neo_table.miss_distance_km.cast(DecimalType(30,10))
        })
        
        df_neo_table_typed.write.parquet(f'{PROCESSED_FOLDER}/{self.__search_at}.parquet')

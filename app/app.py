from src.near_earth_objects import NeoWsDataPipeline

neo_pipeline = NeoWsDataPipeline('2023-02-23')

neo_pipeline.acquire_feed_data()
neo_pipeline.process_data()

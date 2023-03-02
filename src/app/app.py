from src.entities.near_earth_objects import NeoWsDataPipeline
from src.utils.date import last_day

neo_pipeline = NeoWsDataPipeline(last_day())

neo_pipeline.acquire_feed_data()
neo_pipeline.process_data()

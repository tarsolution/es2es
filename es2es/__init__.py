import os
import logging
import json
import time
from datetime import datetime
from elasticsearch import Elasticsearch

# The method that will run the relevant query from the db and send it to the Message Queue, the necessary information is transferred via parametric and os environment.
def perform_task(logger=None, config=None):
    # Configuration information is checked, if it is not sent parametrically, it is retrieved from within the os environment.
    if config is None:
        config = {
            "source_host": os.environ.get('SOURCE_HOST'),
            "source_index": os.environ.get('SOURCE_INDEX'),
            "source_time_column": os.environ.get('SOURCE_TIME_COLUMN'),
            "source_greater_than_time": os.environ.get('SOURCE_GREATER_THAN_TIME'),
            "target_host": int(os.environ.get('TARGET_HOST')),
            "target_index": os.environ.get('TARGET_INDEX'),

            "time_interval": os.environ.get('TIME_INTERVAL',1000),            
            "data_limit": os.environ.get('DATA_LIMIT',100),
            "request_timeout": os.environ.get('REQUEST_TIMEOUT', 3000)
        }

    logger.debug("Config:")
    logger.debug(config)

    def get_last_fetched_data_time():
        # Reading the file content in the directory given with data_template_file_path.
        __location__ = os.path.realpath(os.path.join(os.getcwd()))
        filePath = os.path.join(__location__, "last_fetched_data_time.txt")
        if os.path.exists(filePath):
            with open(filePath, "r") as f:
                return f.read()

    source_host = None
    # The data_template_file_path is checked, if it is not sent parametrically, it is taken from the configuration.
    if "source_host" in config:
        source_host = config.get("source_host")
        logger.debug(f"{'source_host':<} assigned to : {source_host}")
    if not source_host:
        if logger:
            logger.error("Invalid source_host!")
        return
    
    source_index = None
    # The data_template_file_path is checked, if it is not sent parametrically, it is taken from the configuration.
    if "source_index" in config:
        source_index = config.get("source_index")
        logger.debug(f"{'source_index':<} assigned to : {source_index}")
    if not source_index:
        if logger:
            logger.error("Invalid source_index!")
        return
    
    source_time_column = None
    # The data_template_file_path is checked, if it is not sent parametrically, it is taken from the configuration.
    if "source_time_column" in config:
        source_time_column = config.get("source_time_column")
        logger.debug(f"{'source_time_column':<} assigned to : {source_time_column}")
    if not source_time_column:
        if logger:
            logger.error("Invalid source_time_column!")
        return
    last_fetched_data_time = get_last_fetched_data_time()
    source_greater_than_time = None 
    # The data_template_file_path is checked, if it is not sent parametrically, it is taken from the configuration.
    if "source_greater_than_time" in config and config.get("source_greater_than_time"):
        source_greater_than_time = config.get("source_greater_than_time")
    elif last_fetched_data_time:
        source_greater_than_time = last_fetched_data_time
    else: 
        source_greater_than_time = 'now-1d/d'
    
    logger.debug(f"{'source_greater_than_time':<} assigned to : {source_greater_than_time}")
    
    if not source_greater_than_time:
        if logger:
            logger.error("Invalid source_greater_than_time!")
        return
    
    target_host = None
    # The data_template_file_path is checked, if it is not sent parametrically, it is taken from the configuration.
    if "target_host" in config:
        target_host = config.get("target_host")
        logger.debug(f"{'target_host':<} assigned to : {target_host}")
    if not target_host:
        if logger:
            logger.error("Invalid target_host!")
        return
    
    target_index = None
    # The data_template_file_path is checked, if it is not sent parametrically, it is taken from the configuration.
    if "target_index" in config:
        target_index = config.get("target_index")
        logger.debug(f"{'target_index':<} assigned to : {target_index}")
    if not target_index:
        if logger:
            logger.error("Invalid target_index!")
        return
            
    data_limit = config.get("data_limit")
    try:
        time_interval = config.get("time_interval")
        time_interval = int(time_interval)
    except:
        if logger:
            logger.error("Invalid target_index!")
        time_interval = 3

    request_timeout = config.get("request_timeout")

    logger.debug(f"{'data_limit':<12} assigned to : {data_limit}")
    logger.debug(f"{'time_interval':<12} assigned to : {time_interval}")
    logger.debug(f"{'request_timeout':<12} assigned to : {request_timeout}")

    es_source= None
    es_target= None

    while True: 
        if not es_source or (not es_source.ping()):
            es_source = Elasticsearch([source_host]) #Elasticsource(['https://user:secret@localhost:443'])
        if not es_target or  not es_target.ping():    
            es_target = Elasticsearch([target_host]) #Elasticsource(['https://user:secret@localhost:443'])

        if not es_source.ping():
            logger.error("Error: Elastichsource source not accessible!")
            
    
        if not es_target.ping():
            logger.error("Error: Elastichsource target not accessible!")
            
        
        try:
            query = """
                    {
                        "query": {
                            "bool": {
                                "filter": [{
                                    "range": {
                                        "gt": {
                                            \"""" + source_time_column + """\":\"""" + source_greater_than_time + """\"
                                        }
                                    }
                                }]
                            }
                        }
                    }
                    """
            query_json = json.loads(query)
            data_source = es_source.search(index=source_index, body=query_json, sort=[{"${source_time_column}":"asc"}])
            all_hits = data_source['hits']['hits']
            for num, doc in enumerate(all_hits):
                res = es_target.index(index=target_index, id=doc['id'], body=doc, request_timeout=request_timeout)
                source_greater_than_time=doc["${source_time_column}"]
            
        except Exception as e:
            if logger:
                logger.error("Error: {}".format(e))
        finally:
            time.sleep(time_interval)

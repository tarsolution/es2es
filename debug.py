import os
import asyncio
import logging
from es2es import perform_task

if __name__ == "__main__":
    logger = logging.getLogger("es2es")
    logger.setLevel(os.environ.get('LOG_LEVEL', "DEBUG"))
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            os.environ.get('LOG_FORMAT', "%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        )
    )

    config = {
            "source_host": 'elasticsearch.upa.svc.cluster.local:9200',
            "source_index": 'test-index',
            "source_time_column":"created_time",
            "source_greater_than_time":"",
            "target_host": 'elasticsearch.upa.svc.cluster.local:9200',
            "target_index": 'copy-index',    
            "time_interval": 2,
            "data_limit": 100,
            "request_timeout":100
        }

    logger.addHandler(handler)
    try:
        perform_task(logger=logger, config=config)
    except Exception as e:
        if logger:
            logger.error("Error occured! {}".format(e))
    finally:
        logger.info("The es2es process has finished.")
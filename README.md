# es2es

es2es is a library that forwards ElasticSearch data to the other ElasticSearch by source_time_column. Using the library, the parametrically given parameters are run, and the data obtained is forwarded to other ElasticSearch.

## Installation

You can install this library easily with pip.
`pip install es2es` 

## Usage
### As a library
```py
import os
import asyncio
from es2es import perform_task

if __name__ == '__main__':
    logger = logging.getLogger("es2es")
    logger.setLevel(os.environ.get('LOG_LEVEL', "DEBUG"))
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            os.environ.get('LOG_FORMAT', "%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        )
    )
    logger.addHandler(handler)

    config = {
      "source_host": os.environ.get('SOURCE_HOST'),
	    "source_index": int(os.environ.get('SOURCE_INDEX')), 
	    "source_time_column": os.environ.get('SOURCE_TIME_COLUMN'),
	    "source_greater_than_time": os.environ.get('SOURCE_GREATER_THAN_TIME'),
	    "target_host": os.environ.get('TARGET_HOST'),
	    "target_index": os.environ.get('TARGET_INDEX'),
      "time_interval": os.environ.get('TIME_INTERVAL', 1000),
	    "data_limit": os.environ.get('DATA_LIMIT',100),
	    "request_timeout": int(os.environ.get('REQUEST_TIMEOUT', 3000))
    }
    try:
        perform_task(logger=logger, config=config)
     except Exception as e:
        if logger:
            logger.error("Error occured! {}".format(e))
    finally:
        logger.info("The es2es process has finished.")
```

This library uses [elasticsearch](https://elasticsearch-py.readthedocs.io/en/latest/) package.

### Standalone
You can also call this library as standalone job command.  Just set required environment variables and run `es2es`. This usecase perfectly fits when you need run it on cronjobs or kubernetes jobs. 

**Required environment variables:**
- SOURCE_HOST
- SOURCE_INDEX
- SOURCE_TIME_COLUMN
- SOURCE_GREATER_THAN_TIME
- TARGET_HOST
- TARGET_INDEX
- TIME_INTERVAL
- DATA_LIMIT
- REQUEST_TIMEOUT
- LOG_LEVEL (Logging level. See: [Python logging module docs](https://docs.python.org/3/library/logging.html#logging-levels))

**Example Kubernetes job:** 
 You can see it to [kube.yaml](kube.yaml)
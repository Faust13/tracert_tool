import yaml
import sys
from datetime import timedelta

with open("./conf.yml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(sys.exc_info())
        raise exc

FLUENT_HOST = config['fluent'].get('host', 'localhost')
FLUENT_PORT = config['fluent'].get('port', 24224)
FLUENT_TAG = config['fluent'].get('tag', 'tracert')
TARGET_HOST = config['general'].get('host', 'localhost')
SCRAPE_INTERVAL = timedelta(seconds=config['general'].get('interval', 5))

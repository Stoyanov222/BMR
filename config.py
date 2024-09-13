import json


def load_config():
    """Load the configuration from the config.json file."""
    with open('config.json', 'r') as file:
        return json.load(file)

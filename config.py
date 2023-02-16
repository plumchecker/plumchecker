import json

from logging import getLogger, Logger
from jsonschema import validate, ValidationError, SchemaError

class ConfigException(Exception):
    pass

class Config:
    _file = './config.json'
    def __init__(self) -> None:
        self._logger: Logger = getLogger("Config")
        expected_schema = {
            "type": "object",
            "properties": {
                "storage": {
                    "type": "object",
                    "properties": {
                        "host": {"type": "string", "format": "hostname"},
                        "port": {"type": "integer", "minimum": 0},
                        "endpoints": {
                            "type": "object",
                            "properties": {
                                "add": {"type": "string", "format": "uri"},
                                "query": {"type": "string", "format": "uri"}
                            },
                            "required": ["add", "query"]
                        }
                    },
                    "required": ["host", "port", "endpoints"]
                },
                "worker": {
                    "type": "object",
                    "properties": {
                        "batch_size": {"type": "integer", "minimum": 0}
                    },
                    "required": ["batch_size"]
                }
            },
            "required": ["storage", "worker"]
        }
        try:
            with open(self._file, 'r') as config:
                js_config = json.load(config)
                validate(js_config, expected_schema)
        except ValidationError as e:
            self._logger.error(f"Config is invalid: {str(e)}")
            raise ConfigException(e)
        except SchemaError as e:
            self._logger.critical(f"Config validation schema is malformed: {str(e)}")
            raise ConfigException(e)
        except OSError as e:
            self._logger.error(f"Cannot find config at config.json")
            raise ConfigException(e)
        self.query_address = f'http://{js_config["storage"]["host"]}:{js_config["storage"]["port"]}/{js_config["storage"]["endpoints"]["query"]}'
        self.add_address = f'http://{js_config["storage"]["host"]}:{js_config["storage"]["port"]}/{js_config["storage"]["endpoints"]["add"]}'
        self.add_batch_size = js_config["worker"]["batch_size"]

if __name__ == "__main__":
    config = Config()
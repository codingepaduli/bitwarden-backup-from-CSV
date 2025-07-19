import yaml
import logging
import logging.config

def initLogger() -> None :
    """
    Initialize the logger from YAML comfiguration file.
    """
    with open('loggerConfig.yml') as loggerConfigFile:
        loggerConfig = yaml.safe_load(loggerConfigFile)
        logging.config.dictConfig(loggerConfig)

    logger : logging.Logger = logging.getLogger(__name__)

    logger.info("logger configured")

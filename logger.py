'''
This module provides a logging system.



Set the LOG_LEVEL like you want, and in
the necessary module you can use the logger
like this:
____________________________________________

from logger import logger

logger.info('file path is correct.')
logger.warning('Check the files!')
____________________________________________

Only messages with the higher logging level will be
shown.



Also you can get the name of the current logging 
level, for example:

print(LEVELS[LOG_LEVEL])
-> 'DEBUG'
'''



import logging
import os
from datetime import datetime

LOG_FILE_NAME = 'info.log'
LOG_LEVEL = logging.INFO
LEVELS = { 
        logging.DEBUG:'DEBUG',
        logging.INFO:'INFO',
        logging.WARNING:'WARNING',
        logging.ERROR:'ERROR',
        logging.CRITICAL:'CRITICAL',
        }



logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

log_file = logging.FileHandler(LOG_FILE_NAME, mode = 'w')

logging_format = '[%(levelname)s] ({0} "%(name)s") module "%(module)s"\n[func "%(funcName)s"]\n\n%(message)s\n'.format(datetime.now().strftime('%H:%M:%S'))
formatter = logging.Formatter(logging_format)
log_file.setFormatter(formatter)

logger.addHandler(log_file)

logger.info('Logging started!')
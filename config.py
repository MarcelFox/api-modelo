import os
import sys
import logging

logging.basicConfig(filename='info.log',
                    format= '%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logging.StreamHandler(stream=sys.stdout)

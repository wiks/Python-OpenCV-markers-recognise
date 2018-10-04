# coding=utf-8

'''
ASUS:
Python 2.7.9 (default, Sep 25 2018, 23:32:58)
[GCC 4.9.2] on linux2
>>> import cv2
>>> cv2.__version__
'2.4.9.1'

RPi:
Python 2.7.13 (default, Jan 19 2017, 14:48:08)
[GCC 6.3.0 20170124] on linux2
>>> import cv2
>>> cv2.__version__
'2.4.9.1'
>>> import numpy
>>> numpy.__version__
'1.12.1'
'''

import os
import main
import logging.handlers


if __name__ == '__main__':

    log_directory = 'log'
    log_file = os.path.join(log_directory, 'log.txt')
    level = logging.INFO
    logger_name = 'log'

    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d  %(levelname)-8s  %(name)-15s  %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')

    file_handler = logging.handlers.RotatingFileHandler(log_file,
                                                        maxBytes=1000000,
                                                        backupCount=3)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    l.setLevel(level)
    l.addHandler(file_handler)
    l.addHandler(stream_handler)

    main.main()

#!/usr/bin/env python
# encoding: utf-8
"""
Created by 'bens3' on 2013-06-21.
Copyright (c) 2013 'bens3'. All rights reserved.
"""

import sys
import os
import logging
from ke2psql.handlers import SQLAlchemyHandler

__ALL__ = ['log']

def get_logger(name, level=logging.DEBUG):
    logger = logging.getLogger(name)

    logger.propagate = False
    formatter = logging.Formatter('%(levelname)s: %(message)s')

    # Output to both log file and stdout
    file_handler = logging.FileHandler('/var/log/ke2psql.log')
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Add DB log handler
    db_handler = SQLAlchemyHandler()
    db_handler.setLevel(logging.CRITICAL)
    stream_handler.setFormatter(formatter)
    logger.addHandler(db_handler)

    if level:
        logger.setLevel(level)

    return logger

log = get_logger(__name__)
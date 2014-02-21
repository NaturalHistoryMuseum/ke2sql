#!/usr/bin/env python
# encoding: utf-8
"""
Created by 'bens3' on 2013-06-21.
Copyright (c) 2013 'bens3'. All rights reserved.
"""

from sqlalchemy import Column, Integer, String, DateTime, PickleType, func
from sqlalchemy.ext.declarative import declarative_base
from ke2sql.model.base import Base
from ke2sql import config

class Log(Base):

    """
    Table for holding log messages - used for KE EMU DB import errors.
    """
    __tablename__ = 'log'

    __table_args__ = {
        'schema': config.get('database', 'schema')
    }

    id = Column(Integer, primary_key=True)
    logger = Column(String)
    level = Column(String)
    trace = Column(String)
    msg = Column(String)
    args = Column(PickleType)
    created = Column(DateTime, default=func.now())  # the current timestamp

    def __init__(self, logger=None, level=None, trace=None, msg=None, args=None):
        self.logger = logger
        self.level = level
        self.trace = trace
        self.trace = trace
        self.msg = msg
        self.args = args

    def __unicode__(self):
        return self.__repr__()

    def __repr__(self):
        return "<Log: %s - %s>" % (self.created.strftime('%m/%d/%Y-%H:%M:%S'), self.msg[:50])
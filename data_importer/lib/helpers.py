#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '22/03/2017'.
"""

import os
import re
import glob

from data_importer.lib.config import Config


def get_file_export_dates():
    """
    Get a list of all file export dates
    :return:
    """
    full_export_date = Config.getint('keemu', 'full_export_date')
    export_dir = Config.get('keemu', 'export_dir')
    file_pattern = 'ecatalogue.export.*.gz'
    re_date = re.compile(r"([0-9]+)\.gz$")
    export_dates = []
    # Loop through all the files in the export directory,
    # Building a list of dates that need to br processed
    for fn in glob.glob(os.path.join(export_dir, file_pattern)):
        m = re_date.search(fn)
        file_date = int(m.group(1))
        if file_date >= full_export_date:
            export_dates.append(file_date)
    # Sort in reverse date order
    export_dates.sort()
    return export_dates

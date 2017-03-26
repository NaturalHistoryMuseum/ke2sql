#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '22/03/2017'.
"""


def get_dataset_tasks():
    """
    Get a list of all dataset tasks
    :return:
    """
    from ke2sql.tasks.specimen import SpecimenDatasetTask
    from ke2sql.tasks.indexlot import IndexLotDatasetTask
    from ke2sql.tasks.artefact import ArtefactDatasetTask
    return [SpecimenDatasetTask, IndexLotDatasetTask, ArtefactDatasetTask]
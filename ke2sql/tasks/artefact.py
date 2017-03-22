#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '14/03/2017'.



"""

import luigi

from operator import eq, is_not

from ke2sql.tasks.dataset import DatasetTask
from ke2sql.lib.field import Field
from ke2sql.lib.filter import Filter


class ArtefactDatasetTask(DatasetTask):

    package_name = 'collection-artefacts7'
    package_description = "Cultural and historical artefacts from The Natural History Museum"
    package_title = "Artefacts"

    resource_title = 'Artefacts'
    resource_id = 'ec61d82a-748d-4b53-8e99-3e708e76bc4d'
    resource_description = 'Museum Artefacts'

    fields = DatasetTask.fields + [
        Field('ecatalogue', 'AdmGUIDPreferredValue', 'GUID'),
        Field('ecatalogue', 'PalArtObjectName', 'artefactName'),
        Field('ecatalogue', 'PalArtType', 'artefactType'),
        Field('ecatalogue', 'PalArtDescription', 'artefactDescription'),
        Field('ecatalogue', 'IdeCurrentScientificName', 'scientificName')
    ]

    filters = DatasetTask.filters + [
        # Records must have a GUID
        Filter('ecatalogue', 'AdmGUIDPreferredValue', [
            (is_not, None)
        ]),
        # Does this record have an excluded status - Stub etc.,
        Filter('ecatalogue', 'SecRecordStatus', [
            (eq, 'Active'),
        ]),
        # Col record type must be artefact
        Filter('ecatalogue', 'ColRecordType', [
            (eq, 'Artefact'),
        ]),
    ]

if __name__ == "__main__":
    luigi.run(main_task_cls=ArtefactDatasetTask)

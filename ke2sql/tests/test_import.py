#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '31/03/2017'.
"""

import unittest
from ke2sql.tests import BaseTestCase


class TestImport(BaseTestCase):
    """
    Tests for checking imports work correctly
    """
    def test_specimen_record_exists_in_ecatalogue(self):
        self.assertRecordExists('ecatalogue', 1)

    def test_specimen_record_exists_in_dataset(self):
        self.assertDatasetRecordExists('specimen', 1)

    def test_artefact_record_exists_in_ecatalogue(self):
        self.assertRecordExists('ecatalogue', 2)

    def test_artefact_record_exists_in_dataset(self):
        self.assertDatasetRecordExists('artefact', 2)

    def test_indexlot_record_exists_in_ecatalogue(self):
        self.assertRecordExists('ecatalogue', 3)

    def test_indexlot_record_exists_in_dataset(self):
        self.assertDatasetRecordExists('indexlot', 3)

    def test_emultimedia_record_exists(self):
        self.assertRecordExists('emultimedia', 1)

    def test_specimen_record_has_emultimedia(self):
        record = self._get_dataset_record('specimen', 12)
        multimedia = record['multimedia'][0]
        self.assertEqual(multimedia['assetID'], '1234')


if __name__ == '__main__':
    unittest.main()
##
#
# File:    ContentRequestReportIoTests.py
# Author:  J. Westbrook
# Date:    12-Feb-2017
# Version: 0.001
#
# Updates:
#
##
"""
Test cases for managing ws content type definitions.



"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.01"

import logging
import os
import platform
import time
import unittest

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
TESTOUTPUT = os.path.join(HERE, 'test-output', platform.python_version())
if not os.path.exists(TESTOUTPUT):
    os.makedirs(TESTOUTPUT)
mockTopPath = os.path.join(TOPDIR, 'wwpdb', 'mock-data')
rwMockTopPath = os.path.join(TESTOUTPUT)

# Must create config file before importing ConfigInfo
from wwpdb.utils.testing.SiteConfigSetup import SiteConfigSetup
from wwpdb.utils.testing.CreateRWTree import CreateRWTree

# Copy site-config and selected items
crw = CreateRWTree(mockTopPath, TESTOUTPUT)
crw.createtree(['site-config', 'wsresources'])
# Use populate r/w site-config using top mock site-config
SiteConfigSetup().setupEnvironment(rwMockTopPath, rwMockTopPath)

from wwpdb.apps.content_ws_server.content.ContentRequestReportIo import ContentRequestReportIo

FORMAT = '[%(levelname)s]-%(module)s.%(funcName)s: %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class ContentRequestReportIoTests(unittest.TestCase):
    """

    """

    def setUp(self):
        self.__verbose = True
        #
        self.__contentDefD = {
            'report-entry-example-test': {
                'content': {
                    'entity_poly': ['entity_id', 'type', 'nstd_linkage', 'nstd_monomer', 'pdbx_seq_one_letter_code',
                                    'pdbx_seq_one_letter_code_can'],
                    'database_2': ['database_code']
                },
                'type': 'entry',
                'conditions': {
                    'entity_poly': {'entity_id': ('1', 'char', 'eq')},
                    'database_2': {'database_id': ('PDB', 'char', 'eq')}
                },
            },
            'report-summary-entry': {
                'content': {
                    'rcsb_status': ['structure_id',
                                    'author_approval_type',
                                    'author_list',
                                    'author_release_sequence',
                                    'author_release_status_code',
                                    'date_author_approval',
                                    'date_author_release_request',
                                    'date_begin_deposition',
                                    'date_begin_processing',
                                    'date_begin_release_preparation',
                                    'date_chemical_shifts',
                                    'date_coordinates',
                                    'date_hold_chemical_shifts',
                                    'date_hold_coordinates',
                                    'date_hold_nmr_constraints',
                                    'date_hold_struct_fact',
                                    'date_nmr_constraints',
                                    'date_struct_fact',
                                    'exp_method',
                                    'initial_deposition_date',
                                    'pdb_id',
                                    'status_code',
                                    'status_code_cs',
                                    'status_code_mr',
                                    'status_code_sf',
                                    ],
                    'audit_author': ['structure_id',
                                     'name',
                                     'pdbx_ordinal'
                                     ],
                    'exptl': ['structure_id',
                              'method'
                              ],
                    'database_2': [
                        'structure_id',
                        'database_code',
                        'database_id'
                    ]
                },
                'type': 'rdbms',
                'resource': {
                    'rcsb_status': ('da_internal', 'da_internal'),
                    'audit_author': ('da_internal', 'da_internal'),
                    'exptl': ('da_internal', 'da_internal'),
                    'database_2': ('da_internal', 'da_internal'),
                },
                'conditions': {},
            },
            'report-summary-entity-poly': {
                'content': {'entity_poly': ['structure_id',
                                            'entity_id',
                                            'type',
                                            'nstd_linkage',
                                            'nstd_monomer',
                                            'pdbx_seq_one_letter_code',
                                            'pdbx_seq_one_letter_code_can'
                                            ]
                            },
                'type': 'rdbms',
                'resource': {'entity_poly': ('da_internal', 'da_internal'),

                             },
                'conditions': {},
            },
            'report-summary-pdbx-contact-author': {
                'content': {'pdbx_contact_author': ['structure_id',
                                                    'id',
                                                    'address_1',
                                                    'address_2',
                                                    'address_3',
                                                    'city',
                                                    'state_province',
                                                    'postal_code',
                                                    'email',
                                                    'name_first',
                                                    'name_last',
                                                    'country',
                                                    'phone',
                                                    'role',
                                                    'organization_type',
                                                    'identifier_ORCID'
                                                    ]
                            },
                'type': 'rdbms',
                'resource': {'pdbx_contact_author': ('da_internal', 'da_internal'),

                             },
                'conditions': {},
            },
            'report-entry-example-sasbdb': {
                'content': {'database_2': ['database_id', 'database_code'],
                            'pdbx_database_status': ['status_code', 'author_release_status_code',
                                                     'deposit_site', 'process_site',
                                                     'recvd_initial_deposition_date',
                                                     'date_of_NDB_release', 'title_suppression'],
                            'audit_author': ['name', 'pdbx_ordinal'],
                            'pdbx_contact_author': ['name_first', 'name_last', 'name_mi',
                                                    'identifier_ORCID', 'id'],
                            'citation_author': ['name', 'ordinal', 'citation_id'],
                            'citation': ['id', 'journal_abbrev', 'title', 'pdbx_database_id_DOI',
                                         'pdbx_database_id_PubMed'],
                            'pdbx_database_related': ['db_name', 'db_id', 'content_type'],
                            'struct': ['entry_id', 'title'],
                            'entity': ['id', 'type', 'src_method', 'pdbx_description',
                                       'pdbx_number_of_molecules'],
                            'entity_poly': ['entity_id', 'type', 'nstd_linkage', 'nstd_monomer',
                                            'pdbx_seq_one_letter_code',
                                            'pdbx_seq_one_letter_code_can'],
                            'pdbx_depui_status_flags': ['has_sas_data'],
                            },
                'type': 'entry',
                'conditions': {}
            },

            'report-summary-example-emdb-admin': {
                'content': {
                    'em_admin': ['entry_id', 'structure_id', 'title', 'map_release_date',
                                 'deposition_date'], },
                'type': 'rdbms',
                'resource': {
                    'em_admin': ('da_internal', 'da_internal')},
                'conditions': {},
            },
            'report-summary-example-emdb-status': {
                'content': {
                    'deposition': ["dep_set_id", "pdb_id", "initial_deposition_date", "status_code",
                                   "author_release_status_code",
                                   "title", "title_emdb", "author_list", "author_list_emdb",
                                   "exp_method", "status_code_exp",
                                   "emdb_id", "status_code_emdb",
                                   "dep_author_release_status_code_emdb"],
                    'em_admin': ['entry_id', 'structure_id', 'title', 'map_release_date',
                                 'deposition_date'],
                },
                'type': 'rdbms',
                'resource': {
                    'deposition': ('status', 'status'),
                    'em_admin': (
                        'da_internal', 'da_internal')},
                'conditions': {'deposition': {'exp_method': (
                    'ELECTRON MICROSCOPY', 'char', 'LIKE')}
                },
            },

            'report-entry-example-emdb': {
                'content': {'database_2': ['database_id', 'database_code'],
                            'pdbx_database_status': ['status_code', 'author_release_status_code',
                                                     'deposit_site', 'process_site',
                                                     'recvd_initial_deposition_date',
                                                     'date_of_NDB_release'],
                            'audit_author': ['name', 'pdbx_ordinal'],
                            'pdbx_database_related': ['db_name', 'db_id', 'content_type'],
                            'struct': ['entry_id', 'title'],
                            'entity': ['id', 'type', 'src_method', 'pdbx_description',
                                       'pdbx_number_of_molecules'],
                            'entity_poly': ['entity_id', 'type', 'nstd_linkage', 'nstd_monomer',
                                            'pdbx_seq_one_letter_code',
                                            'pdbx_seq_one_letter_code_can'],
                            'em_admin': ['entry_id', 'current_status', 'deposition_date',
                                         'deposition_site',
                                         'details', 'map_hold_date', 'last_update',
                                         'map_release_date',
                                         'obsoleted_date', 'replace_existing_entry_flag', 'title',
                                         'header_release_date'],
                            'emd_admin': ['entry_id', 'current_status', 'deposition_date',
                                          'deposition_site',
                                          'details', 'map_hold_date', 'last_update',
                                          'map_release_date',
                                          'obsoleted_date', 'replace_existing_entry_flag',
                                          'title', 'header_release_date'],

                            'emd_map': ['id', 'contour_level', 'contour_level_source',
                                        'annotation_details', 'file', 'original_file', 'label',
                                        'type',
                                        'partition', 'format', 'size_kb', 'axis_order_fast',
                                        'axis_order_medium', 'axis_order_slow', 'cell_alpha',
                                        'cell_beta',
                                        'cell_gamma', 'cell_a', 'cell_b', 'cell_c', 'data_type',
                                        'dimensions_col', 'dimensions_row', 'dimensions_sec',
                                        'origin_col',
                                        'origin_row', 'origin_sec', 'limit_col', 'limit_row',
                                        'limit_sec', 'pixel_spacing_x', 'pixel_spacing_y',
                                        'pixel_spacing_z',
                                        'symmetry_space_group', 'spacing_x', 'spacing_y',
                                        'spacing_z', 'statistics_minimum', 'statistics_maximum',
                                        'statistics_average',
                                        'statistics_std', 'endian_type'],
                            'em_map': ['id', 'annotation_details', 'axis_order_fast',
                                       'axis_order_medium', 'axis_order_slow', 'cell_a',
                                       'cell_alpha',
                                       'cell_b', 'cell_beta', 'cell_c', 'cell_gamma',
                                       'contour_level',
                                       'contour_level_source', 'data_type', 'dimensions_col',
                                       'dimensions_row', 'dimensions_sec', 'endian_type', 'file',
                                       'format', 'label', 'limit_col', 'limit_row', 'limit_sec',
                                       'origin_col', 'origin_row', 'origin_sec', 'partition',
                                       'pixel_spacing_x', 'pixel_spacing_y', 'pixel_spacing_z',
                                       'size_kb', 'spacing_x', 'spacing_y', 'spacing_z',
                                       'statistics_average',
                                       'statistics_maximum', 'statistics_minimum',
                                       'statistics_std', 'symmetry_space_group', 'type'],
                            },
                'type': 'entry',
                'conditions': {}
            },
        }

    def tearDown(self):
        pass

    def testWriteContentDef(self):
        """Test case -  report type status
        """
        startTime = time.time()
        logger.info("Starting")

        try:
            crio = ContentRequestReportIo()
            ok = crio.writeContentDefinitionDictionary(self.__contentDefD, backup=True)
        except:
            logger.exception("Failing test")
            self.fail()

        endTime = time.time()
        logger.info("Completed with status %r (%.2f seconds)\n" % (ok, (endTime - startTime)))

    def testReadContentDef(self):
        """Test case -  report content definition
        """
        startTime = time.time()
        logger.info("Starting")
        try:
            for ky in self.__contentDefD.keys():
                crio = ContentRequestReportIo()
                rD = crio.getContentDefinition(ky)
                logger.info("Content definition %r" % rD)
        except:
            logger.exception("Failing test")
            self.fail()

        endTime = time.time()
        logger.info("Completed ad (%.2f seconds)\n" % (endTime - startTime))


def suiteWriteContentDef():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ContentRequestReportIoTests("testWriteContentDef"))
    suiteSelect.addTest(ContentRequestReportIoTests("testReadContentDef"))
    return suiteSelect


if __name__ == '__main__':
    #
    if (True):
        mySuite = suiteWriteContentDef()
        unittest.TextTestRunner(verbosity=2).run(mySuite)

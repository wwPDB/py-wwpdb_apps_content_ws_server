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
import sys
import os
import time
import unittest

if __package__ is None or __package__ == "":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from commonsetup import HERE  # noqa:  F401 pylint: disable=import-error,unused-import
else:
    from .commonsetup import HERE  # noqa: F401 pylint: disable=relative-beyond-top-level

from wwpdb.apps.content_ws_server.content.ContentRequestReportIo import ContentRequestReportIo  # noqa: E402

FORMAT = "[%(levelname)s]-%(module)s.%(funcName)s: %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class ContentRequestReportIoTests(unittest.TestCase):
    """ """

    def setUp(self):
        #
        self.__contentDefD = {
            "report-entry-example-test": {
                "content": {
                    "entity_poly": ["entity_id", "type", "nstd_linkage", "nstd_monomer", "pdbx_seq_one_letter_code", "pdbx_seq_one_letter_code_can"],
                    "database_2": ["database_code"],
                },
                "conditions": {"entity_poly": {"entity_id": ("1", "char", "eq")}, "database_2": {"database_id": ("PDB", "char", "eq")}},
                "type": "entry",
            },
            "report-summary-wwpdb-entity-poly": {
                "content": {"entity_poly": ["structure_id", "entity_id", "type", "nstd_linkage", "nstd_monomer", "pdbx_seq_one_letter_code", "pdbx_seq_one_letter_code_can"]},
                "resource": {
                    "entity_poly": ("da_internal", "da_internal"),
                },
                "conditions": {},
                "type": "rdbms",
            },
            "report-summary-wwpdb-pdbx-contact-author": {
                "content": {
                    "pdbx_contact_author": [
                        "structure_id",
                        "address_1",
                        "address_2",
                        "address_3",
                        "city",
                        "state_province",
                        "postal_code",
                        "email",
                        "name_first",
                        "name_last",
                        "country",
                        "phone",
                        "role",
                        "organization_type",
                        "identifier_ORCID",
                    ]
                },
                "resource": {
                    "pdbx_contact_author": ("da_internal", "da_internal"),
                },
                "conditions": {},
                "type": "rdbms",
            },
            "report-summary-example-emdb-admin": {
                "content": {
                    "em_admin": ["entry_id", "structure_id", "title", "map_release_date", "deposition_date"],
                },
                "resource": {"em_admin": ("da_internal", "da_internal")},
                "conditions": {},
                "type": "rdbms",
            },
            "report-summary-example-emdb-status": {
                "content": {
                    "deposition": [
                        "dep_set_id",
                        "pdb_id",
                        "initial_deposition_date",
                        "status_code",
                        "author_release_status_code",
                        "title",
                        "title_emdb",
                        "author_list",
                        "author_list_emdb",
                        "exp_method",
                        "status_code_exp",
                        "emdb_id",
                        "status_code_emdb",
                        "dep_author_release_status_code_emdb",
                    ],
                    "em_admin": ["entry_id", "structure_id", "title", "map_release_date", "deposition_date"],
                },
                "resource": {"deposition": ("status", "status"), "em_admin": ("da_internal", "da_internal")},
                "conditions": {"deposition": {"exp_method": ("ELECTRON MICROSCOPY", "char", "LIKE")}},
                "type": "rdbms",
            },
            "report-entry-example-sasbdb": {
                "content": {
                    "pdbx_database_status": [
                        "status_code",
                        "author_release_status_code",
                        "deposit_site",
                        "process_site",
                        "recvd_initial_deposition_date",
                        "date_of_NDB_release",
                        "title_suppression",
                    ],
                    "entity_poly": ["entity_id", "type", "nstd_linkage", "nstd_monomer", "pdbx_seq_one_letter_code", "pdbx_seq_one_letter_code_can"],
                    "citation": ["id", "journal_abbrev", "title", "pdbx_database_id_DOI", "pdbx_database_id_PubMed"],
                    "database_2": ["database_id", "database_code"],
                    "entity": ["id", "type", "src_method", "pdbx_description", "pdbx_number_of_molecules"],
                    "citation_author": ["name", "ordinal", "citation_id"],
                    "pdbx_depui_status_flags": ["has_sas_data"],
                    "struct": ["entry_id", "title"],
                    "pdbx_contact_author": ["name_first", "name_last", "name_mi", "identifier_ORCID", "id"],
                    "audit_author": ["name", "pdbx_ordinal"],
                    "pdbx_database_related": ["db_name", "db_id", "content_type"],
                },
                "conditions": {},
                "type": "entry",
            },
            "report-entry-example-emdb": {
                "content": {
                    "pdbx_database_status": ["status_code", "author_release_status_code", "deposit_site", "process_site", "recvd_initial_deposition_date", "date_of_NDB_release"],
                    "entity_poly": ["entity_id", "type", "nstd_linkage", "nstd_monomer", "pdbx_seq_one_letter_code", "pdbx_seq_one_letter_code_can"],
                    "emd_admin": [
                        "entry_id",
                        "current_status",
                        "deposition_date",
                        "deposition_site",
                        "details",
                        "map_hold_date",
                        "last_update",
                        "map_release_date",
                        "obsoleted_date",
                        "replace_existing_entry_flag",
                        "title",
                        "header_release_date",
                    ],
                    "database_2": ["database_id", "database_code"],
                    "em_map": [
                        "id",
                        "annotation_details",
                        "axis_order_fast",
                        "axis_order_medium",
                        "axis_order_slow",
                        "cell_a",
                        "cell_alpha",
                        "cell_b",
                        "cell_beta",
                        "cell_c",
                        "cell_gamma",
                        "contour_level",
                        "contour_level_source",
                        "data_type",
                        "dimensions_col",
                        "dimensions_row",
                        "dimensions_sec",
                        "endian_type",
                        "file",
                        "format",
                        "label",
                        "limit_col",
                        "limit_row",
                        "limit_sec",
                        "origin_col",
                        "origin_row",
                        "origin_sec",
                        "partition",
                        "pixel_spacing_x",
                        "pixel_spacing_y",
                        "pixel_spacing_z",
                        "size_kb",
                        "spacing_x",
                        "spacing_y",
                        "spacing_z",
                        "statistics_average",
                        "statistics_maximum",
                        "statistics_minimum",
                        "statistics_std",
                        "symmetry_space_group",
                        "type",
                    ],
                    "entity": ["id", "type", "src_method", "pdbx_description", "pdbx_number_of_molecules"],
                    "struct": ["entry_id", "title"],
                    "em_admin": [
                        "entry_id",
                        "current_status",
                        "deposition_date",
                        "deposition_site",
                        "details",
                        "map_hold_date",
                        "last_update",
                        "map_release_date",
                        "obsoleted_date",
                        "replace_existing_entry_flag",
                        "title",
                        "header_release_date",
                    ],
                    "emd_map": [
                        "id",
                        "contour_level",
                        "contour_level_source",
                        "annotation_details",
                        "file",
                        "original_file",
                        "label",
                        "type",
                        "partition",
                        "format",
                        "size_kb",
                        "axis_order_fast",
                        "axis_order_medium",
                        "axis_order_slow",
                        "cell_alpha",
                        "cell_beta",
                        "cell_gamma",
                        "cell_a",
                        "cell_b",
                        "cell_c",
                        "data_type",
                        "dimensions_col",
                        "dimensions_row",
                        "dimensions_sec",
                        "origin_col",
                        "origin_row",
                        "origin_sec",
                        "limit_col",
                        "limit_row",
                        "limit_sec",
                        "pixel_spacing_x",
                        "pixel_spacing_y",
                        "pixel_spacing_z",
                        "symmetry_space_group",
                        "spacing_x",
                        "spacing_y",
                        "spacing_z",
                        "statistics_minimum",
                        "statistics_maximum",
                        "statistics_average",
                        "statistics_std",
                        "endian_type",
                    ],
                    "audit_author": ["name", "pdbx_ordinal"],
                    "pdbx_database_related": ["db_name", "db_id", "content_type"],
                },
                "conditions": {},
                "type": "entry",
            },
            "report-summary-wwpdb-audit-revision": {
                "content": {
                    "pdbx_audit_revision_details": ["structure_id", "ordinal", "revision_ordinal", "data_content_type", "provider", "type", "description"],
                    "pdbx_audit_revision_history": ["structure_id", "ordinal", "data_content_type", "major_revision", "minor_revision", "revision_date", "internal_version"],
                },
                "resource": {"pdbx_audit_revision_details": ("da_internal", "da_internal"), "pdbx_audit_revision_history": ("da_internal", "da_internal")},
                "conditions": {},
                "type": "rdbms",
            },
            "report-summary-wwpdb-status": {
                "content": {
                    "rcsb_status": [
                        "structure_id",
                        "author_approval_type",
                        "author_list",
                        "author_release_sequence",
                        "author_release_status_code",
                        "date_author_approval",
                        "date_author_release_request",
                        "date_begin_deposition",
                        "date_begin_processing",
                        "date_begin_release_preparation",
                        "date_chemical_shifts",
                        "date_coordinates",
                        "date_hold_chemical_shifts",
                        "date_hold_coordinates",
                        "date_hold_nmr_constraints",
                        "date_hold_struct_fact",
                        "date_nmr_constraints",
                        "date_struct_fact",
                        "exp_method",
                        "initial_deposition_date",
                        "pdb_id",
                        "status_code",
                        "status_code_cs",
                        "status_code_mr",
                        "status_code_sf",
                    ],
                    "exptl": ["structure_id", "method"],
                    "audit_author": ["structure_id", "name", "pdbx_ordinal"],
                    "database_2": ["structure_id", "database_code", "database_id"],
                },
                "resource": {
                    "rcsb_status": ("da_internal", "da_internal"),
                    "exptl": ("da_internal", "da_internal"),
                    "audit_author": ("da_internal", "da_internal"),
                    "database_2": ("da_internal", "da_internal"),
                },
                "conditions": {},
                "type": "rdbms",
            },
            "report-summary-emdb-status": {
                "content": {
                    "rcsb_status": ["Structure_ID", "title", "suppressed_title_Y_N"],
                    "em_admin": [
                        "Structure_id",
                        "entry_id",
                        "current_status",
                        "deposition_date",
                        "deposition_site",
                        "last_update",
                        "map_release_date",
                        "obsoleted_date",
                        "replace_existing_entry_flag",
                        "title",
                    ],
                    "database_2": ["Structure_ID", "database_id", "database_code"],
                    "audit_author": ["Structure_ID", "name", "pdbx_ordinal", "identifier_ORCID"],
                    "em_author_list": ["Structure_ID", "author", "ordinal", "identifier_ORCID"],
                    "em_depui": ["Structure_ID", "same_authors_as_pdb", "same_title_as_pdb"],
                },
                "resource": {
                    "rcsb_status": ["da_internal", "da_internal"],
                    "em_admin": ["da_internal", "da_internal"],
                    "database_2": ["da_internal", "da_internal"],
                    "audit_author": ["da_internal", "da_internal"],
                    "em_author_list": ["da_internal", "da_internal"],
                    "em_depui": ["da_internal", "da_internal"],
                },
                "conditions": {"rcsb_status": {"exp_method": ["%ELECTRON%", "char", "LIKE"]}},
                "type": "rdbms",
            },
        }

    def tearDown(self):
        pass

    def testWriteContentDef(self):
        """Test case -  report type status"""
        startTime = time.time()
        logger.info("Starting")

        try:
            crio = ContentRequestReportIo()
            ok = crio.writeContentDefinitionDictionary(self.__contentDefD, backup=True)
        except:  # noqa: E722 pylint: disable=bare-except
            logger.exception("Failing test")
            self.fail()

        endTime = time.time()
        logger.info("Completed with status %r (%.2f seconds)", ok, (endTime - startTime))

    def testReadContentDef(self):
        """Test case -  report content definition"""
        startTime = time.time()
        logger.info("Starting")
        try:
            for ky in self.__contentDefD.keys():
                crio = ContentRequestReportIo()
                rD = crio.getContentDefinition(ky)
                logger.info("Content definition %r", rD)
        except:  # noqa: E722 pylint: disable=bare-except
            logger.exception("Failing test")
            self.fail()

        endTime = time.time()
        logger.info("Completed ad (%.2f seconds)", endTime - startTime)


def suiteWriteContentDef():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ContentRequestReportIoTests("testWriteContentDef"))
    suiteSelect.addTest(ContentRequestReportIoTests("testReadContentDef"))
    return suiteSelect


if __name__ == "__main__":
    #
    mySuite = suiteWriteContentDef()
    unittest.TextTestRunner(verbosity=2).run(mySuite)

import unittest

from wwpdb.apps.content_ws_server.content_definitions.ContentDefintions import get_content_definition_file, \
    get_content_definition_file_path


class TestContentDefinition(unittest.TestCase):

    def test_getting_content_definitions_file(self):
        ret = get_content_definition_file()
        self.assertEqual(ret, 'ws_content_type_definitions.json')

    def test_getting_content_definitions_file_path(self):
        ret = get_content_definition_file_path()
        print(ret)
        self.assertIsNotNone(ret)


if __name__ == '__main__':
    unittest.main()

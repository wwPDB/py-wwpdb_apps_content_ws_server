import os
import shutil
import tempfile
import unittest

from wwpdb.apps.content_ws_server.register.Register import Register


class RegisterTests(unittest.TestCase):
    def setUp(self):
        self.working_dir = tempfile.mkdtemp()

    def test_write_access_token(self):
        email_address = "noreply@wwpdb.org"
        output_file = os.path.join(self.working_dir, "test.jwt")
        ret = Register().makeAccessToken(
            emailAddress=email_address, tokenFileName=output_file
        )
        self.assertTrue(ret)
        self.assertTrue(os.path.exists(output_file))

    def tearDown(self):
        shutil.rmtree(self.working_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()

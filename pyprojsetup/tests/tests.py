"""
Unit tests for pyprojsetup
"""

from __future__ import print_function
import unittest
import pyprojsetup.parsers
import pyprojsetup.__main__
import os
import sys
import shutil


class TestMain(unittest.TestCase):
    """Test module __main__"""
    def setUp(self):
        self.parser = pyprojsetup.parsers.main()
        target_folder = os.path.join(os.getcwd(), "pyprojsetup_test_repo")
        try:
            shutil.rmtree(target_folder)
        except OSError as e:
            print(
                "Could not delete {}: {}".format(target_folder, e),
                file=sys.stderr)

    def test_main(self):
        """Test function main() by creating a test project. Since this uploads
        to github, it requires a valid git user, specified by --org."""
        cli_args = [
            "pyprojsetup_test_repo",
            "--a", "TESTAUTHOR",
            "--org", "micahculpepper"
        ]
        args = self.parser.parse_args(cli_args)
        pyprojsetup.__main__.main(args)
        user_approval = raw_input("Type `pass` if the git site looks good: ")
        self.assertEqual(user_approval, "pass")

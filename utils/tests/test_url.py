from typing import List
import unittest
from tests import TC
from utils import url as liburl


class UrlTests(unittest.TestCase):
    def test_extract_path_and_filename(self):
        test_cases = [
            {
                "input": "https://my-site.com/2023/05/11/test_url.py",
                "expected_base": "https://my-site.com/2023/05/11/",
                "expected_file": "test_url.py",
            },
            {
                "input": "https://my-site.com/2023/05/11/",
                "expected_base": "https://my-site.com/2023/05/11/",
                "expected_file": "",
            },
            {
                "input": "https://subdomain.my-site.com/test_url.py",
                "expected_base": "https://subdomain.my-site.com/",
                "expected_file": "test_url.py",
            },
            {
                "input": "https://subdomain.my-site.com/",
                "expected_base": "https://subdomain.my-site.com/",
                "expected_file": "",
            },
            {
                "input": "/my/path/file.txt",
                "expected_base": "/my/path/",
                "expected_file": "file.txt",
            },
            {
                "input": "/my/path/",
                "expected_base": "/my/path/",
                "expected_file": "",
            },
        ]

        for tc in test_cases:
            base, file = liburl.extract_path_and_filename(tc["input"])
            self.assertEqual(
                tc["expected_base"],
                base,
            )

            self.assertEqual(
                tc["expected_file"],
                file,
            )

import unittest
import autoloader  # pylint: disable=unused-import

import os

from libs.google.workspace import SpreadSheets


class TestGoogle(unittest.TestCase):
    def test_google_spread_sheets(self):
        # given
        key_file = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
        key_file += "123.json"
        gspread = SpreadSheets({"key_file": key_file})
        spreadsheet_id = ""
        tab_name = "alarm_template"
        tab_range = "A1:F9999999"

        # when
        data = gspread.get(spreadsheet_id, tab_name, tab_range)
        header = data[0]
        rows = data[1:]

        # then
        self.assertEqual(["id", "##비고"], header)
        self.assertTrue(len(rows) > 0)

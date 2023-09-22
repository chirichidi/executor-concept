from __future__ import print_function

import os.path
from googleapiclient import discovery
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.


class SpreadSheets:
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

    def __init__(self, params: dict = None) -> None:
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        if params is None:
            params = {}

        key_file = params["key_file"]

        if os.path.exists(key_file):
            self.creds = Credentials.from_authorized_user_file(key_file, self.SCOPES)

            if not self.creds or not self.creds.valid:
                self.creds.refresh(Request())

            with open(key_file, "w", encoding="utf-8") as token:
                token.write(self.creds.to_json())
        else:
            raise Exception("Invalid credential path")

    def get(self, spreadsheet_id: str, tab_name: str, tab_range: str) -> list:
        # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/get?apix_params=%7B%22spreadsheetId%22%3A%221hR5hVq3g-3QFkr-s7qBSJY5jniGIGSIuB3fKbbSWdkk%22%2C%22ranges%22%3A%5B%22A1%3AF999999%22%5D%2C%22access_token%22%3A%22ya29.a0AWY7Ckm0Rwudvjr7z8fDmbnMq2_si71wVIUQwJ_T7Hp50o28xhvF3uNKDTgqr2wWD-FD5258lLN75InYSKDuSA6Q2OmhfNKG1gxV1dFHiemLAraK0PEzCK3zMhpjpiFZvuR05nMKQ20X3479PqdGkaKk2oGydgnH7waCgYKAb8SARASFQG1tDrphqNDRaQE-17CxkJ4MGY3Og0169%22%7D
        try:
            service = discovery.build("sheets", "v4", credentials=self.creds)

            sheet = service.spreadsheets()
            data = sheet.values().get(spreadsheetId=spreadsheet_id, range=f"{tab_name}!{tab_range}").execute()

            result = []
            for row in data["values"]:
                # 공백 허용 안함
                if len(row) == 0:
                    break
                result.append(row)

            return result

        except HttpError as err:
            print(err)

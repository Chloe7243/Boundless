import io
import csv
import urllib.request
from utils.format_data import RawPassportRow
from constants.urls import PASSPORT_INDEX_URL

"""
Passport Index data

RAW (from GitHub CSV, tidy format):
    One row per passport/destination pair, 3 columns:
        Passport, Destination, Requirement

    Possible requirement values:
        "visa required"
        "visa on arrival"
        "e-visa"
        "eta"
        "visa free"
        "no admission"
        n   -> number of days visa free, e.g. "90"
        -1  -> passport and destination are the same country

    Example row:
        Passport,Destination,Requirement
        Nigeria,Ghana,90

FORMATTED (what this script produces):
    Nested dict keyed by passport, then destination:
        {
            "NGA": {
                "GHA": {"requirement": "visa_free", "max_stay_days": 90},
            },
        }

    Rules:
        - Numbers become requirement "visa_free" with max_stay_days set
        - "visa free" with no number keeps max_stay_days as None
        - -1 rows are dropped (own country)
        - Requirement values are normalised to snake_case
"""


def fetch_passport_data() -> list[RawPassportRow]:
    try:
        response = urllib.request.urlopen(PASSPORT_INDEX_URL)
        text_format = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        print(f"Server returned an error: {error.code} {error.reason}")
    except urllib.error.URLError as error:
        print(f"Could not reach the server: {error.reason}")
    except Exception as error:
        print(error)
        print(f"Unexpected error: {error}")

    csv_reader = csv.DictReader(io.StringIO(text_format))
    return list(csv_reader)

from load import fetch_passport_data
from utils.format_data import format_data
from storage import upload

raw = fetch_passport_data()
upload(raw)

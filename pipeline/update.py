from load import fetch_passport_data
from storage import upload, retrieve

raw = fetch_passport_data()
print(raw)

if raw != retrieve():
    upload(raw)
    print("Passport Index changed, new copy uploaded")
else:
    print("No changes since last run")
import gspread
from google.oauth2.service_account import Credentials

scope = ["https://www.googleapis.com/auth/spreadsheets"]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=scope
)

client = gspread.authorize(creds)

# Replace with your Sheet ID
sheet = client.open_by_key("1GKu47q_6g7DTWVxQXXyJ7hfBVtjCkizmlJooUN7X4tc").sheet1

sheet.append_row(["Test Success", "Google Sheet Connected"])

print("✅ Google Sheet Connected Successfully!")
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

scope = ["https://www.googleapis.com/auth/spreadsheets"]

creds = Credentials.from_service_account_info(
    st.secrets["google_service_account"],
    scopes=scope
)

client_sheet = gspread.authorize(creds)

# Replace with your Sheet ID
sheet = client_sheet.open_by_key("1GKu47q_6g7DTWVxQXXyJ7hfBVtjCkizmlJooUN7X4tc").sheet1

sheet.append_row(["Test Success", "Google Sheet Connected"])

print("✅ Google Sheet Connected Successfully!")
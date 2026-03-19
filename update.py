from datetime import datetime
from decimal import Decimal
import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from data_base import get_all

load_dotenv()
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def sanitize_data(data):
    sanitized = []
    for row in data:
        new_row = []
        for item in row:
            if isinstance(item, datetime):
                new_row.append(item.strftime('%Y-%m-%d %H:%M:%S'))
            elif isinstance(item, Decimal):
                new_row.append(float(item))
            elif item is None:
                new_row.append("")
            else:
                new_row.append(item)
        sanitized.append(new_row)
    return sanitized

def update(page):

    data_sheets, colluns = get_all(page)

    clean_data = sanitize_data(data_sheets)

    clean_data = [colluns] + clean_data

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    service = build('sheets', 'v4', credentials=creds)

    service = build('sheets', 'v4', credentials=creds)

    service.spreadsheets().values().clear(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{page}!A:Z"
    ).execute()

    body = {
        'values': clean_data
    }
    
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{page}!A1",
        valueInputOption="USER_ENTERED", 
        body=body
    ).execute()
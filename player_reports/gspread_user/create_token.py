import gspread

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",  # needed if you open by name / list files
]

gc = gspread.oauth(
    credentials_filename="gspread_auth/credentials.json",      # your client_secret
    authorized_user_filename="gspread_auth/authorized_user.json",
    scopes=SCOPES,
)
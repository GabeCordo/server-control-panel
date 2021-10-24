"""FLASK CONFIGURATION FILE"""

from os import path, environ, urandom

# FLASK

TESTING = True
DEBUG = True

SECRET_KEY = environ.get("FLASK_SECRET_KEY") or urandom(24)

# SYSTEM PATH CONSTANTS

PATH_SYSTEM = path.abspath(__file__)[:-13]
PATH_DATA = PATH_SYSTEM + 'data/'
PATH_LOGS = PATH_DATA + 'logs/'

# Google.com Keys and Socket Info

GOOGLE_ACCOUNTS_BASE_URL = 'https://accounts.google.com'
GOOGLE_SERVICE_ACCOUNT_FILE = 'secret/credentials.json'
GOOGLE_SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/spreadsheets'
]

GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVER_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
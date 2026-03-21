"""
Configuration file - loads all the environment variables from .env file
I'm using python-dotenv so we don't have to hardcode any credentials
"""

import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

# load the .env file
load_dotenv()

# groq api key for the AI model
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# mysql database connection details
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "truthscan_ai")

# had to use quote_plus because my password has special characters like @ and it was breaking the url
DATABASE_URL = f"mysql+pymysql://{quote_plus(DB_USER)}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# twilio credentials for whatsapp bot
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

# server config
APP_HOST = os.getenv("APP_HOST", "127.0.0.1")
APP_PORT = int(os.getenv("APP_PORT", "8000"))

# TruthScan AI - Fake News & Scam Detector

A web application that uses AI to detect fake news, scam messages, and suspicious content in real-time. Users can paste any text — news headlines, WhatsApp forwards, emails, or URLs — and get an instant analysis with a confidence score and risk indicators.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)

## Features

- **AI-Powered Analysis** - Uses Groq AI (Llama 3.3 70B) to analyze text for misinformation and scam patterns
- **Multiple Scan Types** - Supports news articles, scam messages, suspicious URLs, and general messages
- **Confidence Scoring** - Each scan returns a confidence score (0-100%) with detailed explanation
- **Risk Indicators** - Identifies specific red flags like clickbait language, phishing patterns, urgency tactics
- **Scan History** - All results are stored in MySQL database with full history tracking
- **Dashboard Stats** - Real-time statistics showing total scans, threats detected, and threat rate
- **WhatsApp Bot** - Twilio integration allows users to scan content directly via WhatsApp
- **Responsive UI** - Clean dark-themed interface that works on desktop and mobile

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **FastAPI** | Backend REST API framework |
| **Groq AI** | NLP analysis using Llama 3.3 70B model |
| **MySQL** | Database for storing scan results |
| **SQLAlchemy** | ORM for database operations |
| **Twilio** | WhatsApp messaging integration |
| **HTML/CSS/JS** | Frontend user interface |
| **Python-dotenv** | Environment variable management |

## Project Structure

```
truthscan-ai/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in git)
├── .env.example            # Template for .env file
├── app/
│   ├── __init__.py
│   ├── config.py           # Configuration & env variables
│   ├── database.py         # MySQL connection setup
│   ├── models.py           # SQLAlchemy database models
│   ├── schemas.py          # Pydantic request/response schemas
│   ├── groq_service.py     # Groq AI integration
│   ├── whatsapp_service.py # Twilio WhatsApp service
│   └── routes.py           # API endpoint definitions
└── static/
    ├── index.html          # Frontend page
    ├── style.css           # Styling (dark theme)
    └── script.js           # Frontend JavaScript
```

## Setup & Installation

### Prerequisites
- Python 3.10 or higher
- MySQL Server
- Groq API Key (free at https://console.groq.com)
- Twilio Account (optional, for WhatsApp feature)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/truthscan-ai.git
   cd truthscan-ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create MySQL database**
   ```sql
   CREATE DATABASE truthscan_ai;
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your credentials:
   - `GROQ_API_KEY` - Your Groq API key
   - `DB_PASSWORD` - Your MySQL password
   - `TWILIO_ACCOUNT_SID` - Twilio SID (optional)
   - `TWILIO_AUTH_TOKEN` - Twilio token (optional)

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Open in browser**
   ```
   http://localhost:8000
   ```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/scan` | Analyze text for fake news/scams |
| `GET` | `/api/history` | Get recent scan results |
| `GET` | `/api/stats` | Get dashboard statistics |
| `POST` | `/api/whatsapp/webhook` | Twilio WhatsApp webhook |

### Example Request

```bash
curl -X POST http://localhost:8000/api/scan \
  -H "Content-Type: application/json" \
  -d '{"text": "You won $1M! Click here to claim!", "analysis_type": "scam"}'
```

### Example Response

```json
{
  "id": 1,
  "verdict": "SCAM",
  "confidence_score": 0.95,
  "explanation": "This message exhibits classic scam patterns...",
  "risk_indicators": "[\"Too-good-to-be-true offer\", \"Urgency tactics\"]"
}
```

## WhatsApp Integration (Optional)

1. Set up a Twilio account and WhatsApp Sandbox
2. Use ngrok to expose your local server: `ngrok http 8000`
3. Set the Twilio webhook URL to: `https://your-ngrok-url/api/whatsapp/webhook`
4. Send a message to the WhatsApp sandbox number to test

## Screenshots

The application features a dark-themed UI with:
- Real-time dashboard statistics
- Interactive scan interface with type selection
- Color-coded results (red for threats, green for safe)
- Scan history with timestamps

## Future Improvements

- Add user authentication
- Support for image/screenshot analysis
- Browser extension for real-time website scanning
- Multi-language support
- Batch scanning for multiple texts at once

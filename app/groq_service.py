"""
Groq AI Service - this is the core of the project
Sends text to the Groq API (uses Llama 3.3 70B model) and gets back
whether the content is fake news, a scam, or legit
"""

import json
from groq import Groq
from app.config import GROQ_API_KEY

# initialize the groq client
client = Groq(api_key=GROQ_API_KEY)

# this prompt tells the AI exactly how to analyze and what format to respond in
SYSTEM_PROMPT = """You are TruthScan AI, an expert fake news and scam detector. Analyze the given text and determine if it is:
- FAKE NEWS or REAL NEWS (for news articles/claims)
- SCAM or SAFE (for messages, emails, offers)
- SUSPICIOUS or SAFE (for URLs or links)

Respond ONLY in this exact JSON format (no markdown, no extra text):
{
    "verdict": "FAKE|REAL|SCAM|SAFE|SUSPICIOUS",
    "confidence_score": 0.0 to 1.0,
    "explanation": "Brief explanation of your analysis",
    "risk_indicators": ["indicator1", "indicator2"]
}

Analysis guidelines:
- Check for sensationalist language, clickbait patterns, and emotional manipulation
- Look for logical fallacies, unsupported claims, and missing sources
- Identify phishing patterns, urgency tactics, and suspicious requests for personal info
- Evaluate grammatical quality, domain credibility, and factual consistency
- For scams: look for too-good-to-be-true offers, pressure tactics, requests for money/info
- Be thorough but concise in your explanation"""


def analyze_text(text, analysis_type="news"):
    """
    Main function that sends text to Groq AI and returns the analysis.

    Parameters:
        text - the content to analyze
        analysis_type - what kind of content it is (news/scam/url/message)

    Returns a dict with verdict, confidence_score, explanation, risk_indicators
    """

    # give different instructions based on what type of content we're checking
    type_context = {
        "news": "Analyze this as a NEWS article or claim. Determine if it is FAKE or REAL.",
        "scam": "Analyze this as a potential SCAM message. Determine if it is a SCAM or SAFE.",
        "url": "Analyze this URL/link description. Determine if it is SUSPICIOUS or SAFE.",
        "message": "Analyze this message/email. Determine if it is a SCAM or SAFE.",
    }

    context = type_context.get(analysis_type, type_context["news"])

    # call the groq API
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"{context}\n\nText to analyze:\n{text}"},
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.1,   # low temp = more consistent results
        max_tokens=1024,
    )

    response_text = chat_completion.choices[0].message.content.strip()

    # try to parse the JSON response from the AI
    try:
        result = json.loads(response_text)
    except json.JSONDecodeError:
        # sometimes the AI wraps JSON in markdown code blocks, so try to extract it
        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        if start != -1 and end > start:
            result = json.loads(response_text[start:end])
        else:
            # if we still can't parse it, return a default response
            result = {
                "verdict": "UNKNOWN",
                "confidence_score": 0.0,
                "explanation": "Could not parse AI response. Please try again.",
                "risk_indicators": [],
            }

    return {
        "verdict": result.get("verdict", "UNKNOWN"),
        "confidence_score": float(result.get("confidence_score", 0.0)),
        "explanation": result.get("explanation", "No explanation provided."),
        "risk_indicators": json.dumps(result.get("risk_indicators", [])),
    }

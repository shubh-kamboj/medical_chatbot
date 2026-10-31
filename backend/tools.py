import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from twilio.rest import Client
from backend.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, EMERGENCY_CONTACT

load_dotenv()

#  tool to get response from gemini LLM
def query_gemini(prompt: str) -> str:
    #  this is docstring used by python to explain function behavior
    """
    Calls Gemini API with a mental health support personality.
    Returns empathetic and supportive responses.
    """
    system_prompt = """You are Dr. Emily Hartman, a warm and experienced clinical psychologist. 
    Respond to patients with:
    1. Emotional attunement ("I can sense how difficult this must be...")
    2. Gentle normalization ("Many people feel this way when...")
    3. Practical guidance ("What sometimes helps is...")
    4. Strengths-focused support ("I notice how you're...")

    Key principles:
    - Use natural, conversational language.
    - Avoid unnecessary headings, labels, and brackets.
    - Match the user's language and communication style.
    - Ask relevant, open-ended questions when appropriate.
    - Never claim to be a licensed psychologist or diagnose conditions.
    - Encourage professional help when the user needs additional support.
    - If the user appears to be in immediate danger, prioritize safety
      and encourage contacting emergency services or a qualified professional.
    - Always respond in exactly one line.
    - Keep every response within 50 words.
    - Be concise, empathetic, and clear.
    - Never use bullet points or multiple paragraphs.
    """

    try:
        api_key = os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                max_output_tokens=100,  # Maximum length of the generated response
                temperature=0.7,        # Controls response randomness: 0 = predictable, 1 = more creative and varied.
                top_p=0.9,              # Controls word selection diversity.
            ),
        )
        return (response.text or "").strip()
    except Exception:
        return "I'm having technical difficulties, but I want you to know your feelings matter. Please try again shortly."

# print(query_gemini(prompt="Hi, How are you?"))

# Setup Twilio calling API tool
def call_emergency():
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    call = client.calls.create(
        to=EMERGENCY_CONTACT,
        from_=TWILIO_FROM_NUMBER,
        url="http://demo.twilio.com/docs/voice.xml"  # Can customize message
    )

# call_emergency()
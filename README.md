# Medical Chatbot

## Initial Setup

### Prerequisites

- Windows with PowerShell
- Python 3.12
- uv

Verify the installed tools:

```
py --version
uv --version
```

### 1. Create the Project Directory

```
mkdir D:\projects\medical_chatbot
cd D:\projects\medical_chatbot
```

If the project directory already exists, navigate to it:

```
cd D:\projects\medical_chatbot
```

### 2. Initialize the Python Project

```
uv init --python 3.12
```

This initializes the project and creates the basic project files, including `pyproject.toml` and `main.py`.

### 3. Create a Virtual Environment

```
uv venv
```

This creates a project-local `.venv` directory.

### 4. Activate the Virtual Environment

.\.venv\Scripts\Activate.ps1
----
cmd /k ".venv\Scripts\activate.bat"

### 5. Install Project Dependencies

-- add a dependency
uv add fastapi

This adds the dependencies to `pyproject.toml`, resolves compatible package versions, installs the dependencies into the project environment, and creates or updates `uv.lock`.

-- Check a specific dependency already installed 
uv pip show dependency_name

### 6. Synchronize Dependencies

To install dependencies for an existing checkout of the project using its configuration and lockfile, run:

```
uv sync
```

Keep `pyproject.toml` and `uv.lock` in version control so other developers can reproduce the project environment. Do not commit the `.venv` directory.

### 7. Run Streamlit
uv run streamlit run frontend.py

### 8. Run Backend
uv run backend/main.py
-- or from root folder
uv run python -m backend.main  -> Python project root se module execute karta hai.

### Tech Stack
Language                : Python (>= 3.11)
Environment & packaging : uv (for virtualenv + dependency management via pyproject.toml)
Backend                 : FastAPI + Uvicorn
Frontend                : Streamlit
LLM / Agent             : langchain, langgraph, langchain-groq with ChatGroq
Integrations            : Twilio (WhatsApp + Voice), Google Maps API (Places + Geocoding), Geopy / Requests (supporting utilities)

### Project Structure
safespace-ai-therapist/
├── backend/
│   ├── ai_agent.py         # LangGraph-based AI agent + tools (LLM, emergency call, therapist finder)
│   ├── config.py           # API keys and configuration (not shown here; you create it)
│   ├── main.py             # FastAPI backend (JSON /ask + Twilio WhatsApp /whatsapp_ask)
│   ├── tools.py            # Low-level tool implementations (MedGemma, Twilio call, etc.)
│   └── test_location_tool.py  # Tests/examples for the location tool
├── frontend.py              # Streamlit chat UI (web client) talking to FastAPI backend
├── pyproject.toml           # Project metadata and Python dependencies (managed with uv)
└── README.md                # Main project README

### Key Components
1. frontend.py
A Streamlit app that:
Renders a chat interface with st.chat_input and st.chat_message.
Sends user messages to the backend endpoint POST /ask on http://localhost:8000/ask.
Displays the AI agent's response along with the name of any tool that was used.

2. backend/main.py
Defines a FastAPI application with two main endpoints:
POST /ask: JSON API used by the Streamlit frontend.
POST /whatsapp_ask: Twilio WhatsApp webhook endpoint that receives form-encoded messages (Body field) and responds with TwiML.
Uses ai_agent.graph (LangGraph REAct agent) with parse_response to generate responses.
Includes a helper _twiml_message() to build minimal TwiML XML responses for Twilio.

3. backend/ai_agent.py
Declares several LangChain tools using @tool:
ask_mental_health_specialist(query: str) -> str
Uses query_medgemma() (from tools.py) to call a MedGemma-based model for therapeutic responses.
emergency_call_tool() -> None
Uses call_emergency() (from tools.py) to trigger a Twilio voice call to a safety helpline.
find_nearby_therapists_by_location(location: str) -> str
Uses the Google Maps API to geocode a location and return nearby therapists (name, address, phone).
Configures the LLM:
Uses ChatGroq with model "openai/gpt-oss-120b" and GROQ_API_KEY from config.py.
Creates a REAct agent via create_react_agent(llm, tools=tools).
Defines a SYSTEM_PROMPT with instructions for when to use each tool.
Provides parse_response(stream) to extract the final message and which tool was called from the streaming agent output.

4. backend/config.py (implied)
Should provide configuration values such as:
GROQ_API_KEY
GOOGLE_MAPS_API_KEY
Twilio credentials (e.g., TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, phone numbers)
You create this file yourself and do not commit your secrets.

5. backend/tools.py (implied)
Implements the concrete integrations:
query_medgemma(query: str) -> str
call_emergency() -> None
Optional helpers for Google Maps / Twilio
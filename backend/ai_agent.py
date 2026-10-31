import os
from dotenv import load_dotenv
from backend.tools import query_gemini,call_emergency
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import googlemaps
load_dotenv()

@tool
def ask_mental_health_specialist(query: str) -> str:
    #  this is docstring used by python to explain function behavior
    """
    Generate a therapeutic response using the MedGemma model.
    Use this for all general user queries, mental health questions, emotional concerns,
    or to offer empathetic, evidence-based guidance in a conversational tone.
    """
    return query_gemini(query)

@tool
def emergency_call_tool() -> None:
    """
    Place an emergency call to the safety helpline's phone number via Twilio.
    Use this only if the user expresses suicidal ideation, intent to self-harm,
    or describes a mental health emergency requiring immediate help.
    """
    call_emergency()

@tool
def find_nearby_therapists_by_location(location: str) -> str:
    """
    Finds and returns a list of licensed therapists near the specified location.

    Args:
        location (str): The name of the city or area in which the user is seeking therapy support.

    Returns:
        str: A newline-separated string containing therapist names and contact info.
    """
    return (
        f"Here are some therapists near {location}, {location}:\n"
        "- Dr. Ayesha Kapoor - +1 (555) 123-4567\n"
        "- Dr. James Patel - +1 (555) 987-6543\n"
        "- MindCare Counseling Center - +1 (555) 222-3333"
    )

@tool
def find_nearby_therapists_by_location_live(location: str) -> str:
    """
    Get the user's location.
    """
    google_map_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    gmaps = googlemaps.Client(key=google_map_api_key)
    geocode_result = gmaps.geocode(location)
    lat_lng = geocode_result[0]['geometry']['location']
    lat, lng = lat_lng['lat'], lat_lng['lng']
    places_result = gmaps.places_nearby(
            location=(lat, lng),
            radius=5000,
            keyword="Psychotherapist"
        )
    output = [f"Therapists near {location}:"]
    top_results = places_result['results'][:5]
    for place in top_results:
            name = place.get("name", "Unknown")
            address = place.get("vicinity", "Address not available")
            details = gmaps.place(place_id=place["place_id"], fields=["formatted_phone_number"])
            phone = details.get("result", {}).get("formatted_phone_number", "Phone not available")

            output.append(f"- {name} | {address} | {phone}")
    return "\n".join(output)


# Initialize Gemini and connect backend tools
api_key = os.getenv("GROQ_API_KEY")

tools = [ask_mental_health_specialist, emergency_call_tool, find_nearby_therapists_by_location,]
# llm = ChatGoogleGenerativeAI(
#     model="gemini-3.5-flash-lite",
#     # temperature=0.2,
#     google_api_key=api_key,
# )

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.2,
    api_key=api_key,
)

SYSTEM_PROMPT = """
You are an AI assistant supporting mental health conversations with
warmth, empathy, and vigilance.
Available tools:
1. ask_mental_health_specialist: Use for emotional or psychological
   queries requiring supportive guidance.
2. find_nearby_therapists_by_location: Use when the user asks about
   nearby therapists or local professional support.
3. emergency_call_tool: Use according to its defined safety criteria
   when the user expresses suicidal thoughts, self-harm intentions,
   or an immediate crisis.
Respond kindly, clearly, and supportively. Never claim to diagnose
a mental health condition or replace a qualified professional.
"""
graph = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
)

def parse_response(stream):
    tool_called_names = []
    final_response = None

    for s in stream:
        for node_name, data in s.items():
            messages = data.get("messages", [])

            for msg in messages:
                # Record tools requested by the LLM
                for tool_call in getattr(msg, "tool_calls", []):
                    name = tool_call.get("name")
                    if name and name not in tool_called_names:
                        tool_called_names.append(name)

                # Extract final assistant text
                if getattr(msg, "type", None) == "ai" and not getattr(msg, "tool_calls", []):
                    content = msg.content

                    if isinstance(content, str):
                        final_response = content
                    elif isinstance(content, list):
                        text_parts = [
                            block["text"]
                            for block in content
                            if isinstance(block, dict)
                            and block.get("type") == "text"
                            and block.get("text")
                        ]
                        if text_parts:
                            final_response = "\n".join(text_parts)

    return tool_called_names, final_response

#  for testing purpose only
# if __name__ == "__main__":
#     while True:
#         user_input = input("User: ")
#         print(f"Received user input: {user_input[:200]}...")
#         inputs = {"messages": [("system", SYSTEM_PROMPT), ("user", user_input)]}
#         stream = graph.stream(inputs, stream_mode="updates")
#         tool_called_name, final_response = parse_response(stream)
#         print("TOOL CALLED: ", tool_called_name)
#         print("ANSWER: ", final_response)
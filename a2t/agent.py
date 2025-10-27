from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from .models import CityTimeInput, TimeResponse

APP_NAME = "document_app"
USER_ID = "user_123"
SESSION_ID = "session_456"

def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {"status": "success", "city": city, "time": "10:30 AM"}

root_agent = LlmAgent(
    model=LiteLlm(model="bedrock/anthropic.claude-3-haiku-20240307-v1:0"),
    name='root_agent',
    description="Tells the current time in a specified city.",
    instruction="You are a helpful assistant that tells the current time in cities. Use the 'get_current_time' tool for this purpose.",
    input_schema=CityTimeInput,
    #output_schema=TimeResponse,
    tools=[get_current_time],
)


session_service = InMemorySessionService()
session = session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID
)
runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service
)

def run_query(query):
    content = types.Content(
        role="user",
        parts=[types.Part(text=query)]
    )
    events = runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=content
    )
    for event in events:
        if event.is_final_response():
            return event.content.parts[0].text
    return "No response received."

if __name__ == "__main__":
    response = run_query("¿Qué hora es en Madrid?")
    print(response)
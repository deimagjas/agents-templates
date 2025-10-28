from dotenv import load_dotenv

load_dotenv()  

import asyncio

from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.planners import  BuiltInPlanner

from google.genai.types import ThinkingConfig
from google.adk.models.lite_llm import LiteLlm
from google.adk.planners import PlanReActPlanner

import datetime
from zoneinfo import ZoneInfo

APP_NAME = "weather_app"
USER_ID = "1234"
SESSION_ID = "session1234"

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}


root_agent2 = LlmAgent(
    model=LiteLlm(model="bedrock/anthropic.claude-3-haiku-20240307-v1:0"),
    name="weather_and_time_agent",
    instruction="You are an agent that returns time and weather",
    planner=PlanReActPlanner(),
    tools=[get_weather, get_current_time]
)

# Session and Runner
session_service = InMemorySessionService()
# create_session is an async coroutine; ensure it's awaited so the session exists
session = asyncio.run(
session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    )
runner = Runner(agent=root_agent2, app_name=APP_NAME, session_service=session_service)

# Agent Interaction
def call_agent(query):
    content = types.Content(role='user', parts=[types.Part(text=query)])
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    for event in events:
        print(f"\nDEBUG EVENT: {event}\n")
        if event.is_final_response() and event.content:
            final_answer = event.content.parts[0].text.strip()
            print("\n🟢 FINAL ANSWER\n", final_answer, "\n")

async def call_agent_async(query):
    content = types.Content(role='user', parts=[types.Part(text=query)])
    events = runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content)
    final_response_content = "No final response received."
    async for event in events:
        print(f"\nDEBUG EVENT: {event}\n")
        if event.is_final_response() and event.content:
            final_answer = event.content.parts[0].text.strip()
            print("\n🟢 FINAL ANSWER\n", final_answer, "\n")
    
    current_session = await session_service.get_session(app_name=APP_NAME,
                                                  user_id=USER_ID,
                                                  session_id=SESSION_ID)
#call_agent("If it's raining in New York right now, what is the current temperature?")

if __name__ == "__main__":
    try:
        asyncio.run(call_agent_async("If it's sunny in New York right now, what is the current temperature?"))
    except Exception:
        print("Some errors.")
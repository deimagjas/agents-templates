import asyncio

from agent import root_agent

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

APP_NAME = "weather_app"
USER_ID = "1234"
SESSION_ID = "session1234"


# Session and Runner
session_service = InMemorySessionService()
# create_session is an async coroutine; ensure it's awaited so the session exists
session = asyncio.run(
session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    )
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

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
    except Exception as e:
        print(f"Some errors: {e}")
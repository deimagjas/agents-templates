from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {"status": "success", "city": city, "time": "10:30 AM"}

root_agent = LlmAgent(
    model=LiteLlm(model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0"),
    name='root_agent',
    description="Tells the current time in a specified city.",
    instruction="You are a helpful assistant that tells the current time in cities. Use the 'get_current_time' tool for this purpose.",
    tools=[get_current_time],
)

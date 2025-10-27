from pydantic import BaseModel, Field

class CityTimeInput(BaseModel):
    city: str = Field(description="Name of the city to get the current time for")

class TimeResponse(BaseModel):
    city: str = Field(description="Name of the city")
    time: str = Field(description="Current time in the specified city")
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class TelemetryCreate(BaseModel):
    metric: str = Field(
        min_length=1,
        max_length=50,
    )

    value: float

    unit: str = Field(
        min_length=1,
        max_length=20,
    )


class TelemetryResponse(BaseModel):
    id: int
    device_id: int
    metric: str
    value: float
    unit: str
    recorded_at: datetime

    model_config = ConfigDict(from_attributes=True)

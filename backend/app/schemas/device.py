
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DeviceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    mac_address: str = Field(min_length=17, max_length=17)
    device_type: str = Field(min_length=1, max_length=50)
    location: str | None = Field(default=None, max_length=255)
    firmware_version: str | None = Field(default=None, max_length=50)


class DeviceUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    device_type: str | None = Field(default=None, min_length=1, max_length=50)
    location: str | None = Field(default=None, max_length=255)
    firmware_version: str | None = Field(default=None, max_length=50)


class DeviceResponse(BaseModel):
    id: int
    name: str
    mac_address: str
    device_type: str
    location: str | None
    firmware_version: str | None
    last_seen: datetime | None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

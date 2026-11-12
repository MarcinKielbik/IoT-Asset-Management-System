
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class DeviceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    mac_address: str = Field(
        pattern=r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$"
    )
    device_type: str = Field(min_length=1, max_length=50)
    location: str | None = Field(default=None, max_length=255)
    firmware_version: str | None = Field(default=None, max_length=50)


class DeviceUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    device_type: str | None = Field(default=None, min_length=1, max_length=50)
    location: str | None = Field(default=None, max_length=255)
    firmware_version: str | None = Field(default=None, max_length=50)

    @model_validator(mode="after")
    def validate_non_nullable_fields(self):
        if "name" in self.model_fields_set and self.name is None:
            raise ValueError("name cannot be null")

        if "device_type" in self.model_fields_set and self.device_type is None:
            raise ValueError("device_type cannot be null")

        return self


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




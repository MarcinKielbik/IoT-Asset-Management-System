
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.device import Device
from app.models.telemetry import Telemetry
from app.schemas.telemetry import TelemetryCreate, TelemetryResponse


router = APIRouter(
    prefix="/devices/{device_id}/telemetry",
    tags=["Telemetry"],
)


@router.post(
    "/",
    response_model=TelemetryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_telemetry(
    device_id: int,
    telemetry_data: TelemetryCreate,
    db: Session = Depends(get_db),
):
    device = db.scalar(
        select(Device).where(Device.id == device_id)
    )

    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found",
        )

    telemetry = Telemetry(
        device_id=device_id,
        **telemetry_data.model_dump(),
    )

    db.add(telemetry)
    db.commit()
    db.refresh(telemetry)

    return telemetry


@router.get(
    "/",
    response_model=list[TelemetryResponse],
)
def get_device_telemetry(
    device_id: int,
    db: Session = Depends(get_db),
):
    device = db.scalar(
        select(Device).where(Device.id == device_id)
    )

    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found",
        )

    telemetry_records = db.scalars(
        select(Telemetry)
        .where(Telemetry.device_id == device_id)
        .order_by(Telemetry.recorded_at.desc())
    ).all()

    return telemetry_records

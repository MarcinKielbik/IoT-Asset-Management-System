
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceUpdate, DeviceResponse


router = APIRouter(
    prefix="/devices",
    tags=["Devices"],
)


@router.post(
    "/",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_device(
    device_data: DeviceCreate,
    db: Session = Depends(get_db),
):
    existing_device = (
        db.query(Device)
        .filter(Device.mac_address == device_data.mac_address)
        .first()
    )

    if existing_device:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Device with this MAC address already exists",
        )

    device = Device(**device_data.model_dump())

    db.add(device)
    db.commit()
    db.refresh(device)

    return device


@router.get(
    "/",
    response_model=list[DeviceResponse],
)
def get_devices(
    db: Session = Depends(get_db),
):
    return db.query(Device).all()


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
)
def get_device(
    device_id: int,
    db: Session = Depends(get_db),
):
    device = db.query(Device).filter(Device.id == device_id).first()

    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found",
        )

    return device


@router.patch(
    "/{device_id}",
    response_model=DeviceResponse,
)
def update_device(
    device_id: int,
    device_data: DeviceUpdate,
    db: Session = Depends(get_db),
):
    device = db.query(Device).filter(Device.id == device_id).first()

    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found",
        )

    update_data = device_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(device, field, value)

    db.commit()
    db.refresh(device)

    return device


@router.delete(
    "/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_device(
    device_id: int,
    db: Session = Depends(get_db),
):
    device = db.query(Device).filter(Device.id == device_id).first()

    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found",
        )

    db.delete(device)
    db.commit()

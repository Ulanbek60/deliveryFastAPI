from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from delivery_app.db.models import Courier
from delivery_app.db.schema import CourierSchema
from delivery_app.db.database import SessionLocal
from typing import List

courier_router = APIRouter(prefix='/courier', tags=['Courier'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@courier_router.post('/create')
async def courier_create(courier: CourierSchema, db: Session = Depends(get_db)):
    courier_db = Courier(**courier.dict())
    db.add(courier_db)
    db.commit()
    db.refresh(courier_db)
    return courier_db


@courier_router.get('/', response_model=List[CourierSchema])
async def courier_list(db: Session = Depends(get_db)):
    return db.query(Courier).all()


@courier_router.get('/{courier_id}', response_model=List[CourierSchema])
async def courier_detail(courier_id: int, db: Session = Depends(get_db)):
    courier = db.query(Courier).filter(Courier.id==courier_id).first()

    if courier is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')
    return courier


@courier_router.put('/{courier_id}', response_model=CourierSchema)
async def update_courier(courier_id: int, courier: CourierSchema, db: Session = Depends(get_db)):
    courier_db = db.query(Courier).filter(Courier.id==courier_id).first()

    if courier_db is None:
        raise HTTPException(status_code=404, detail='такого продукта не существует')
    for courier_key, courier_value in courier.dict().items():
        setattr(courier_db, courier_key, courier_value)

    db.add(courier_db)
    db.commit()
    db.refresh(courier_db)
    return courier_db


@courier_router.delete('/{courier_id}')
async def delete_courier(courier_id: int, db: Session = Depends(get_db)):
    courier = db.query(Courier).filter(Courier.id==courier_id).first()
    if courier is None:
        raise HTTPException(status_code=404, detail='такого курьера не существует')

    db.delete(courier)
    db.commit()
    return {"message": 'This courier deleted'}



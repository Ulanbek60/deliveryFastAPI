from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from delivery_app.db.models import Order, Courier
from delivery_app.db.schema import OrderSchema
from delivery_app.db.database import SessionLocal
from typing import List

order_router = APIRouter(prefix='/order', tags=['Order'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@order_router.post('/create')
async def order_create(order: OrderSchema, db: Session = Depends(get_db)):
    order_db = Courier(**order.dict())
    db.add(order_db)
    db.commit()
    db.refresh(order_db)
    return order_db


@order_router.get('/', response_model=List[OrderSchema])
async def order_list(db: Session = Depends(get_db)):
    return db.query(Order).all()


@order_router.get('/{order_id}', response_model=List[OrderSchema])
async def order_detail(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id==order_id).first()

    if order is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')
    return order

@order_router.put('/{order_id}', response_model=OrderSchema)
async def update_order(order_id: int, order: OrderSchema, db: Session = Depends(get_db)):
    order_db = db.query(Order).filter(Order.id==order_id).first()

    if order_db is None:
        raise HTTPException(status_code=404, detail='такого заказа не существует')
    for order_key, order_value in order.dict().items():
        setattr(order_db, order_key, order_value)

    db.add(order_db)
    db.commit()
    db.refresh(order_db)
    return order_db


@order_router.delete('/{order_id}')
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id==order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail='такого заказа не существует')

    db.delete(order)
    db.commit()
    return {"message": 'This order deleted'}


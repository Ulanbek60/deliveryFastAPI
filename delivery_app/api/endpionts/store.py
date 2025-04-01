from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from delivery_app.db.models import Store
from delivery_app.db.schema import StoreSchema
from delivery_app.db.database import SessionLocal
from typing import List

store_router = APIRouter(prefix='/store', tags=['Store'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@store_router.get('/search/', response_model=List[StoreSchema])
async def search_store(store_name: str, db: Session = Depends(get_db)):
    store_db = db.query(Store).filter(Store.store_name.ilike(f'%{store_name}%')).all()
    if not store_db:
        raise HTTPException(status_code=404, detail='Store Not Found')
    return store_db


@store_router.post('/create')
async def store_create(store: StoreSchema, db: Session = Depends(get_db)):
    store_db = Store(**store.dict())
    db.add(store_db)
    db.commit()
    db.refresh(store_db)
    return store_db


@store_router.get('/', response_model=List[StoreSchema])
async def store_list(db: Session = Depends(get_db)):
    return db.query(Store).all()


@store_router.get('/{store_id}', response_model=List[StoreSchema])
async def store_detail(store_id: int, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id==store_id).first()

    if store is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')


@store_router.put('/{store_id}', response_model=StoreSchema)
async def update_store(store_id: int, store: StoreSchema, db: Session = Depends(get_db)):
    store_db = db.query(Store).filter(Store.id==store_id).first()

    if store_db is None:
        raise HTTPException(status_code=404, detail='такого категории не существует')
    for store_key, store_value in store.dict().items():
        setattr(store_db, store_key, store_value)

    db.add(store_db)
    db.commit()
    db.refresh(store_db)
    return store_db


@store_router.delete('/{store_id}')
async def delete_store(store_id: int, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id==store_id).first()
    if store is None:
        raise HTTPException(status_code=404, detail='такого категории не существует')

    db.delete(store)
    db.commit()
    return {"message": 'This category deleted'}


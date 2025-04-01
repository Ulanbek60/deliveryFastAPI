from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from delivery_app.db.models import ReviewStore, Courier
from delivery_app.db.schema import ReviewStoreSchema
from delivery_app.db.database import SessionLocal
from typing import List

review_store_router = APIRouter(prefix='/review_store', tags=['Review_store'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@review_store_router.post('/create')
async def review_store_create(review_store: ReviewStoreSchema, db: Session = Depends(get_db)):
    review_store_db = Courier(**review_store.dict())
    db.add(review_store_db)
    db.commit()
    db.refresh(review_store_db)
    return review_store_db


@review_store_router.get('/', response_model=List[ReviewStoreSchema])
async def review_store_list(db: Session = Depends(get_db)):
    return db.query(ReviewStore).all()


@review_store_router.get('/{review_store_id}', response_model=List[ReviewStoreSchema])
async def review_store_detail(review_store_id: int, db: Session = Depends(get_db)):
    review_store = db.query(ReviewStore).filter(ReviewStore.id==review_store_id).first()

    if review_store is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')
    return review_store


@review_store_router.put('/{review_store_id}', response_model=ReviewStoreSchema)
async def update_review_store(review_store_id: int, review_store: ReviewStoreSchema, db: Session = Depends(get_db)):
    review_store_db = db.query(ReviewStore).filter(ReviewStore.id==review_store_id).first()

    if review_store_db is None:
        raise HTTPException(status_code=404, detail='такого отзыва не существует')
    for review_store_key, review_store_value in review_store.dict().items():
        setattr(review_store_db, review_store_key, review_store_value)

    db.add(review_store_db)
    db.commit()
    db.refresh(review_store_db)
    return review_store_db


@review_store_router.delete('/{review_store_id}')
async def delete_review_store_db(review_store_id: int, db: Session = Depends(get_db)):
    review_store_db = db.query(ReviewStore).filter(ReviewStore.id==review_store_id).first()
    if review_store_db is None:
        raise HTTPException(status_code=404, detail='такого отзыва не существует')

    db.delete(review_store_db)
    db.commit()
    return {"message": 'This review deleted'}


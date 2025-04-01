from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from delivery_app.db.models import ReviewProduct, Courier
from delivery_app.db.schema import ReviewProductSchema
from delivery_app.db.database import SessionLocal
from typing import List

review_product_router = APIRouter(prefix='/review_product', tags=['|Review_product'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@review_product_router.post('/create')
async def review_product_create(review_product: ReviewProductSchema, db: Session = Depends(get_db)):
    review_product_db = Courier(**review_product.dict())
    db.add(review_product_db)
    db.commit()
    db.refresh(review_product_db)
    return review_product_db


@review_product_router.get('/', response_model=List[ReviewProductSchema])
async def review_store_list(db: Session = Depends(get_db)):
    return db.query(ReviewProduct).all()


@review_product_router.get('/{review_product_id}', response_model=List[ReviewProductSchema])
async def review_product_detail(review_product_id: int, db: Session = Depends(get_db)):
    review_product = db.query(ReviewProduct).filter(ReviewProduct.id==review_product_id).first()

    if review_product is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')
    return review_product

@review_product_router.put('/{review_product_id}', response_model=ReviewProductSchema)
async def update_review_product(review_product_id: int, review_product: ReviewProductSchema, db: Session = Depends(get_db)):
    review_product_db = db.query(ReviewProduct).filter(ReviewProduct.id==review_product_id).first()

    if review_product_db is None:
        raise HTTPException(status_code=404, detail='такого отзыва не существует')
    for review_product_key, review_product_value in review_product.dict().items():
        setattr(review_product_db, review_product_key, review_product_value)

    db.add(review_product_db)
    db.commit()
    db.refresh(review_product_db)
    return review_product_db


@review_product_router.delete('/{review_product_id}')
async def delete_review_product(review_product_id: int, db: Session = Depends(get_db)):
    review_product_db = db.query(ReviewProduct).filter(ReviewProduct.id==review_product_id).first()
    if review_product_db is None:
        raise HTTPException(status_code=404, detail='такого отзыва не существует')

    db.delete(review_product_db)
    db.commit()
    return {"message": 'This review deleted'}


from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from delivery_app.db.models import Category
from delivery_app.db.schema import CategorySchema
from delivery_app.db.database import SessionLocal
from typing import List

category_router = APIRouter(prefix='/category', tags=['Category'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@category_router.post('/', response_model=CategorySchema)
async def create_category(category: CategorySchema, db: Session = Depends(get_db)):
    try:
        category_db = Category(category_name=category.category_name)
        db.add(category_db)
        db.commit()
        db.refresh(category_db)
        return category_db
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@category_router.get('/', response_model=List[CategorySchema])
async def get_category(db: Session = Depends(get_db)):
    return db.query(Category).all()


@category_router.get('/{category_id}', response_model=CategorySchema)
async def get_category_id(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id==category_id).first()

    if category is None:
        raise HTTPException(status_code=404, detail='такого категории не существует')
    return category


@category_router.put('/{category_id}', response_model=CategorySchema)
async def update_category(category_id: int, category: CategorySchema, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id==category_id).first()

    if category_db is None:
        raise HTTPException(status_code=404, detail='такого категории не существует')
    category_db.category_name = category.category_name

    db.add(category_db)
    db.commit()
    db.refresh(category_db)
    return category_db


@category_router.delete('/{category_id}')
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id==category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail='такого категории не существует')

    db.delete(category)
    db.commit()
    return {"message": 'This category deleted'}


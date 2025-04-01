from fastapi import Depends, HTTPException, APIRouter, Query
from sqlalchemy.orm import Session
from delivery_app.db.models import Product
from delivery_app.db.schema import ProductSchema
from delivery_app.db.database import SessionLocal
from typing import List, Optional

product_router = APIRouter(prefix='/product', tags=['Product'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@product_router.post('/create')
async def product_create(product: ProductSchema, db: Session = Depends(get_db)):
    product_db = Product(**product.dict())
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db


@product_router.get('/', response_model=List[ProductSchema])
async def list_product(
    min_price: Optional[float] = Query(None, alias='price[from]'),
    max_price: Optional[float] = Query(None, alias='price[to]'),
    db: Session = Depends(get_db)
):
    query = db.query(Product)

    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    products = query.all()

    if not products:
        raise HTTPException(status_code=404, detail='Products not found')
    return products



@product_router.get('/{product_id}/', response_model=ProductSchema)
async def product_detail(product_id: int,db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise  HTTPException(status_code=400, detail='Мындай маалымат жок')
    return product


@product_router.put('/{product_id}', response_model=ProductSchema)
async def update_product(product_id: int, product: ProductSchema, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id==product_id).first()

    if product_db is None:
        raise HTTPException(status_code=404, detail='такого продукта не существует')
    for product_key, product_value in product.dict().items():
        setattr(product_db, product_key, product_value)

    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db


@product_router.delete('/{product_id}')
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id==product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail='такого продукта не существует')

    db.delete(product)
    db.commit()
    return {"message": 'This product deleted'}



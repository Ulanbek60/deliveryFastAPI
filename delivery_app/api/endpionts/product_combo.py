from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from delivery_app.db.models import ProductCombo
from delivery_app.db.schema import ProductComboSchema
from delivery_app.db.database import SessionLocal
from typing import List

product_combo_router = APIRouter(prefix='/product_combo', tags=['Product_combo'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@product_combo_router.post('/create')
async def product_combo_create(product_combo: ProductComboSchema, db: Session = Depends(get_db)):
    product_combo_db = ProductCombo(**product_combo.dict())
    db.add(product_combo_db)
    db.commit()
    db.refresh(product_combo_db)
    return product_combo_db


@product_combo_router.get('/', response_model=List[ProductComboSchema])
async def product_combo_list(db: Session = Depends(get_db)):
    return db.query(ProductCombo).all()


@product_combo_router.get('/{product_combo_id}', response_model=List[ProductComboSchema])
async def product_combo_detail(product_combo_id: int, db: Session = Depends(get_db)):
    product_combo = db.query(ProductCombo).filter(ProductCombo.id==product_combo_id).first()

    if product_combo is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')
    return product_combo



@product_combo_router.put('/{product_combo_id}', response_model=ProductComboSchema)
async def update_product_combo(product_combo_id: int, product_combo: ProductComboSchema, db: Session = Depends(get_db)):
    product_combo_db = db.query(ProductCombo).filter(ProductCombo.id==product_combo_id).first()

    if product_combo_db is None:
        raise HTTPException(status_code=404, detail='такого продукта не существует')
    for product_combo_key, product_combo_value in product_combo.dict().items():
        setattr(product_combo_db, product_combo_key, product_combo_value)

    db.add(product_combo_db)
    db.commit()
    db.refresh(product_combo_db)
    return product_combo_db


@product_combo_router.delete('/{product_combo_id}')
async def delete_product_combo(product_combo_id: int, db: Session = Depends(get_db)):
    product_combo = db.query(ProductCombo).filter(ProductCombo.id==product_combo_id).first()
    if product_combo is None:
        raise HTTPException(status_code=404, detail='такого комбо не существует')

    db.delete(product_combo)
    db.commit()
    return {"message": 'This combo deleted'}


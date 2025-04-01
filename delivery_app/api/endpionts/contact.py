from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from delivery_app.db.models import Contact
from delivery_app.db.schema import ContactSchema
from delivery_app.db.database import SessionLocal
from typing import List

contact_router = APIRouter(prefix='/contact', tags=['Contact'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contact_router.post('/create')
async def contact_create(contact: ContactSchema, db: Session = Depends(get_db)):
    contact_db = Contact(**contact.dict())
    db.add(contact_db)
    db.commit()
    db.refresh(contact_db)
    return contact_db


@contact_router.get('/', response_model=List[ContactSchema])
async def contact_list(db: Session = Depends(get_db)):
    return db.query(Contact).all()



@contact_router.put('/edit', response_model=ContactSchema)
async def update_contact(contact_id: int, contact: ContactSchema, db: Session = Depends(get_db)):
    contact_db = db.query(Contact).filter(Contact.id==contact_id).first()

    if contact_db is None:
        raise HTTPException(status_code=404, detail='такого контакта не существует')
    for contact_key, contact_value in contact.dict().items():
        setattr(contact_db, contact_key, contact_value)

    db.add(contact_db)
    db.commit()
    db.refresh(contact_db)
    return contact_db


@contact_router.delete('/delete')
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id==contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail='такого контакта не существует')

    db.delete(contact)
    db.commit()
    return {"message": 'This contact deleted'}


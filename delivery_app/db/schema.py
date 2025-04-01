from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from delivery_app.db.models import StatusChoices, StatusCourierChoices, StatusOrderChoices


class UserProfileSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    password: str
    phone_number: Optional[str]
    age: Optional[int]
    profile_image: Optional[str]
    status: StatusChoices
    date_registered: datetime


class CategorySchema(BaseModel):
    id: int
    category_name: str


class StoreSchema(BaseModel):
    id: int
    store_name: str
    category_id: int
    description: str
    store_image: str
    address: str
    owner_id: int


class ContactSchema(BaseModel):
    id: int
    title: str
    contact_number: Optional[str]
    social_network: Optional[str]
    store_id: int


class ProductSchema(BaseModel):
    id: int
    product_name: str
    description: str
    product_image: str
    price: float
    store_id: int


class ProductComboSchema(BaseModel):
    id: int
    combo_name: str
    description: str
    combo_image: str
    price: float
    store_id: int
    category_id: int


class CourierSchema(BaseModel):
    id: int
    courier_id: int
    product_current_orders_id: int
    combo_current_orders_id: int
    status_choices: StatusCourierChoices


class OrderSchema(BaseModel):
    id: int
    status: StatusOrderChoices
    delivery_address: str
    client_id: int


class ReviewStoreSchema(BaseModel):
    id: int
    user_name_id: int
    store_id: int


class ReviewProductSchema(BaseModel):
    id: int
    user_name_id: int
    product_id: int

from sqlalchemy import Integer, String, Enum, ForeignKey, Text, DECIMAL, DateTime
from delivery_app.db.database import Base
from typing import Optional, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum
from datetime import datetime
from passlib.hash import bcrypt


class StatusChoices(str, PyEnum):
    client = 'client'
    owner = 'owner'
    courier = 'courier'


class UserProfile(Base):

    __tablename__ = 'user_profile'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(64))
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hash_password: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    profile_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), nullable=False, default=StatusChoices.client)
    date_registered: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    owner_store: Mapped[List['Store']] = relationship('Store', back_populates='owner',
                                                      cascade='all, delete-orphan')
    courier_name: Mapped[List['Courier']] = relationship('Courier', back_populates='courier',
                                                         cascade='all, delete-orphan')
    client_order_name: Mapped[List['Order']] = relationship('Order', back_populates='client_order',
                                                            cascade='all, delete-orphan')
    user_name_review: Mapped[List['ReviewStore']] = relationship('ReviewStore', back_populates='user_name',
                                                                 cascade='all, delete-orphan')
    user_review_product: Mapped[List['ReviewProduct']] = relationship('ReviewProduct', back_populates='user_name_product',
                                                              cascade='all, delete-orphan')
    tokens: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='user',
                                                        cascade='all, delete-orphan')

    def set_passwords(self, password: str):
        self.hash_password = bcrypt.hash(password)

    def check_password(self, password: str):
        return bcrypt.verify(password, self.hash_password)

class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String, unique=True, index=True)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='tokens')

class Category(Base):

    __tablename__ = 'category'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String(32), unique=True)
    category_store: Mapped[List['Store']] = relationship('Store', back_populates='category',
                                                          cascade='all, delete-orphan')
    category_combo_name: Mapped[List['ProductCombo']] = relationship('ProductCombo', back_populates='category_combo',
                                                          cascade='all, delete-orphan')


class Store(Base):

    __tablename__ = 'store'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_name: Mapped[str] = mapped_column(String(32))
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    category: Mapped[Category] = relationship(Category, back_populates='category_store')
    description: Mapped[str] = mapped_column(Text)
    store_image: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String)
    owner_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    owner: Mapped[UserProfile] = relationship(UserProfile, back_populates='owner_store')
    contact_store: Mapped[List['Contact']] = relationship('Contact', back_populates='store',
                                                          cascade='all, delete-orphan')
    product_store: Mapped[List['Product']] = relationship('Product', back_populates='stores',
                                                          cascade='all, delete-orphan')
    store_combo_name: Mapped[List['ProductCombo']] = relationship('ProductCombo', back_populates='store_combo',
                                                                  cascade='all, delete-orphan')
    user_store_review: Mapped[List['ReviewStore']] = relationship('ReviewStore', back_populates='store_review',
                                                                  cascade='all, delete-orphan')


class Contact(Base):

    __tablename__ = 'contact'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(32))
    contact_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    social_network: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    store: Mapped[Store] = relationship(Store, back_populates='contact_store')


class Product(Base):

    __tablename__ = 'product'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(64))
    description: Mapped[str] = mapped_column(Text)
    product_image: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    store_id: Mapped[Store] = mapped_column(ForeignKey('store.id'))
    stores: Mapped[Store] = relationship(Store, back_populates='product_store')
    product_order: Mapped[List['Courier']] = relationship('Courier', back_populates='product_current_orders',
                                                          cascade='all, delete-orphan')
    user_product_review: Mapped[List['ReviewProduct']] = relationship('ReviewProduct', back_populates='product_review',
                                                          cascade='all, delete-orphan')

class ProductCombo(Base):

    __tablename__ = 'product_combo'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    combo_name: Mapped[str] = mapped_column(String(64))
    description: Mapped[str] = mapped_column(Text)
    combo_image: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    store_id: Mapped[Store] = mapped_column(ForeignKey('store.id'))
    store_combo: Mapped[Store] = relationship(Store, back_populates='store_combo_name')
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    category_combo: Mapped[Category] = relationship(Category, back_populates='category_combo_name')
    product_combo_order: Mapped[List['Courier']] = relationship('Courier', back_populates='combo_current_orders',
                                                                cascade='all, delete-orphan')

class StatusCourierChoices(str, PyEnum):
    available = 'available'
    employed = 'employed'

class Courier(Base):

    __tablename__ = 'courier'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    courier_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    courier: Mapped[UserProfile] = relationship(UserProfile, back_populates='courier_name')
    product_current_orders_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    product_current_orders: Mapped[Product] = relationship(Product, back_populates='product_order')
    combo_current_orders_id: Mapped[int] = mapped_column(ForeignKey('product_combo.id'))
    combo_current_orders: Mapped[ProductCombo] = relationship(ProductCombo, back_populates='product_combo_order')
    status_choices: Mapped[StatusCourierChoices] = mapped_column(Enum(StatusCourierChoices), nullable=False, default=StatusCourierChoices.available)
    # courier_order: Mapped['Order'] = relationship('Order')


class StatusOrderChoices(str, PyEnum):
    awaiting_processing = 'awaiting_processing'
    during_the_delivery_process = 'during_the_delivery_process'
    delivered = 'delivered'
    cancelled = 'cancelled'


class Order(Base):

    __tablename__ = 'order'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    status: Mapped[StatusOrderChoices] = mapped_column(Enum(StatusOrderChoices), nullable=False, default=StatusOrderChoices.awaiting_processing)
    delivery_address: Mapped[str] = mapped_column(String(256))
    client_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    client_order: Mapped[UserProfile] = relationship(UserProfile, back_populates='client_order_name')
    # courier_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    # courier: Mapped[UserProfile] = relationship('UserProfile', back_populates='courier_order')



class ReviewStore(Base):

    __tablename__ = 'review_store'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_name_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user_name: Mapped[UserProfile] = relationship(UserProfile, back_populates='user_name_review')
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    store_review: Mapped[Store] = relationship(Store, back_populates='user_store_review')


class ReviewProduct(Base):

    __tablename__ = 'review_product'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_name_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user_name_product: Mapped[UserProfile] = relationship(UserProfile, back_populates='user_review_product')
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))  # Изменено на правильную таблицу
    product_review: Mapped[Product] = relationship(Product, back_populates='user_product_review')

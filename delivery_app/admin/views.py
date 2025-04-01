from sqladmin import ModelView, Admin
from delivery_app.db.models import *
from delivery_app.db.database import engine


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.username, UserProfile.status]
    name = 'User'
    name_plural = 'Users'


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.category_name]
    name = 'Category'
    name_plural = 'Categories'
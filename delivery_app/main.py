import fastapi
from delivery_app.db.database import engine
import uvicorn
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
import redis.asyncio as redis
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from sqladmin import Admin
from delivery_app.admin.setup import setup_admin
from delivery_app.api.endpionts import auth, category, contact, store, product
from starlette.middleware.sessions import SessionMiddleware
from delivery_app.config import SECRET_KEY

async def init_redis():
    return redis.Redis.from_url('redis://localhost', encoding='utf-8', decode_responses=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = await init_redis()
    await FastAPILimiter.init(redis)
    yield
    await redis.close()

delivery = fastapi.FastAPI(title='Delivery', lifespan=lifespan)
delivery.add_middleware(SessionMiddleware, secret_key="SECRET_KEY")

admin = Admin(delivery, engine)

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/login')
password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
setup_admin(delivery)

delivery.include_router(auth.auth_router)
delivery.include_router(category.category_router)
delivery.include_router(store.store_router)
delivery.include_router(contact.contact_router)
delivery.include_router(product.product_router)

if __name__ == "__main__":
    uvicorn.run(delivery, host="127.0.0.1", port=8001)


from fastapi import FastAPI

from carts_routes import router as cart_router
from items_routes import router as item_router

app = FastAPI(title="Shop API")

app.include_router(item_router)
app.include_router(cart_router)

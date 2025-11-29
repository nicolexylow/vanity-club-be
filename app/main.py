from typing import Union

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db
from .routers.business import router as business_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# ---------------------------------------------------------------------------
# include routers
app.include_router(business_router)

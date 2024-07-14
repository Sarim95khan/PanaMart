from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlmodel import select

from app.db import get_session, Session
from app.models import Product, ProductCreate, ProductUpdate
product_router = APIRouter(tags=["product"], prefix="/product")


@product_router.get('/')
def get_all_product(session:Annotated[Session,Depends(get_session)]):
    stmt = select(Product)
    result = session.exec(stmt).all()
    return result


@product_router.post('/create-product')
def create_product(product:ProductCreate, session:Annotated[Session,Depends(get_session)]):
    db_product = Product.model_validate(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@product_router.patch('/update-product/{product_id}')
def update_product(product_id:int, product:ProductUpdate , session:Annotated[Session, Depends(get_session)]):
    db_product = session.get(Product, product_id)
    if not db_product:
        return {"message": "Product not found"}
    product_data = product.model_dump(exclude_unset=True)
    db_product.sqlmodel_update(product_data)
    session.add(db_product)
    session.commit()
    return db_product

# @product_router.patch('/update-product/{product_id}')
# def update_product(product_id: int, product: ProductUpdate, session: Session):
#     db_product = session.get(Product, product_id)
#     if not db_product:
#         raise HTTPException(status_code=404, detail="Product not found")

#     product_data = product.dict(exclude_unset=True)
#     for field, value in product_data.items():
#         setattr(db_product, field, value)

#     session.add(db_product)
#     session.commit()
#     return db_product
    
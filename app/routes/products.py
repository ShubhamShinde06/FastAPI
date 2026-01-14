from fastapi import APIRouter, HTTPException, Query, Path
from uuid import UUID
from controllers.prodcuts import (
    get_all_products,
    get_product_by_id,
    create_product,
    remove_product,
    update_product
)
from model.product import ProductCreate, ProductOut, ProductUpdate

router = APIRouter()

@router.get("/get-all")
def list_products(
    name: str | None = Query(None),
    sort_by_price: bool = False,
    order: str = Query("asc", pattern="^(asc|desc)$"),
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
):
    products = get_all_products()

    if name:
        products = [p for p in products if name.lower() in p["name"].lower()]

    if sort_by_price:
        products.sort(key=lambda x: x["price"], reverse=(order == "desc"))

    return {
        "total": len(products),
        "limit": limit,
        "data": products[offset: offset + limit]
    }

@router.get("/get-single/{product_id}", response_model=ProductOut)
def product_by_id(product_id: UUID = Path(...)):
    product = get_product_by_id(str(product_id))
    if not product:
        raise HTTPException(404, "Product not found")
    return product

@router.post("/create", response_model=ProductOut, status_code=201)
def add_product(product: ProductCreate):
    return create_product(product)

@router.delete("/delete/{product_id}")
def delete_product(product_id: UUID = Path(...)):
    result = remove_product(str(product_id))
    if not result:
        raise HTTPException(404, "Product not found")
    return result

@router.put("/update/{product_id}", response_model=ProductOut)
def update_product_route(
    product_id: UUID,
    payload: ProductUpdate
):
    updated = update_product(str(product_id), payload)
    if not updated:
        raise HTTPException(404, "Product not found")
    return updated

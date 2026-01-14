import json
from pathlib import Path
from uuid import uuid4
from datetime import datetime
from typing import List, Dict
from model.product import ProductCreate, ProductOut, ProductUpdate
from pydantic import BaseModel, AnyUrl

DATA_FILE = Path(__file__).parent.parent / "data" / "products.json"

def load_products() -> List[Dict]:
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, AnyUrl):
            return str(obj)
        if isinstance(obj, BaseModel):
            return obj.model_dump()
        return super().default(obj)

def save_products(products: List[Dict]):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, cls=EnhancedJSONEncoder)

def get_all_products() -> List[Dict]:
    return load_products()

def get_product_by_id(product_id: str) -> Dict | None:
    return next((p for p in load_products() if p["id"] == product_id), None)

def create_product(product: ProductCreate) -> ProductOut:
    products = load_products()

    if any(p["sku"] == product.sku for p in products):
        raise ValueError("SKU already exists")

    product_dict = product.model_dump(mode="json")
    product_dict["id"] = str(uuid4())
    product_dict["created_at"] = datetime.utcnow().isoformat()

    products.append(product_dict)
    save_products(products)

    return ProductOut(**product_dict)

def remove_product(product_id: str):
    products = load_products()
    for i, p in enumerate(products):
        if p["id"] == product_id:
            deleted = products.pop(i)
            save_products(products)
            return {"message": "Product deleted", "data": deleted}
    return None

def update_product(product_id: str, update: ProductUpdate) -> ProductOut | None:
    products = load_products()

    for i, p in enumerate(products):
        if p["id"] == product_id:
            update_data = update.model_dump(exclude_unset=True)

            if "dimensions_cm" in update_data:
                p["dimensions_cm"].update(
                    {k: v for k, v in update_data["dimensions_cm"].items() if v is not None}
                )
                update_data.pop("dimensions_cm")

            if "seller" in update_data:
                p["seller"].update(
                    {k: v for k, v in update_data["seller"].items() if v is not None}
                )
                update_data.pop("seller")

            p.update(update_data)
            products[i] = p
            save_products(products)
            return ProductOut(**p)

    return None

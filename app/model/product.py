from pydantic import (
    BaseModel, AnyUrl, EmailStr,
    Field, field_validator, model_validator, computed_field
)
from typing import List, Optional, Literal
from uuid import UUID
from datetime import datetime

class DimensionsCM(BaseModel):
    length: float = Field(gt=0)
    width: float = Field(gt=0)
    height: float = Field(gt=0)

class Seller(BaseModel):
    seller_id: UUID
    name: str = Field(min_length=2, max_length=60)
    email: EmailStr
    website: AnyUrl

class ProductBase(BaseModel):
    sku: str
    name: str
    description: str
    category: str
    brand: str
    price: float
    currency: Literal["INR"] = "INR"
    discount_percent: int = 0
    stock: int
    is_active: bool
    rating: float
    tags: Optional[List[str]] = None
    image_urls: List[AnyUrl]
    dimensions_cm: DimensionsCM
    seller: Seller

    @field_validator("sku")
    @classmethod
    def sku_format(cls, v):
        if "-" not in v:
            raise ValueError("SKU must contain '-'")
        return v

    @model_validator(mode="after")
    def business_rules(self):
        if self.stock == 0 and self.is_active:
            raise ValueError("Inactive product must have stock")
        return self

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: UUID
    created_at: datetime

    @computed_field
    def final_price(self) -> float:
        return round(self.price * (1 - self.discount_percent / 100), 2)

    @computed_field
    def volume_cm(self) -> float:
        d = self.dimensions_cm
        return round(d.length * d.width * d.height, 2)

class DimensionsUpdate(BaseModel):
    length: Optional[float] = Field(gt=0, default=None)
    width: Optional[float] = Field(gt=0, default=None)
    height: Optional[float] = Field(gt=0, default=None)

class SellerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[AnyUrl] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[float] = None
    discount_percent: Optional[int] = None
    stock: Optional[int] = None
    is_active: Optional[bool] = None
    rating: Optional[float] = None
    tags: Optional[List[str]] = None
    image_urls: Optional[List[AnyUrl]] = None
    dimensions_cm: Optional[DimensionsUpdate] = None
    seller: Optional[SellerUpdate] = None

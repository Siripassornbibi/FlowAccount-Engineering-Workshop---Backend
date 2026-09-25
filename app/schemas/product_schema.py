"""
Schema layer
------------
Pydantic models สำหรับ validate request body และกำหนดรูปแบบ response
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class ProductCreateRequest(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category: Optional[str] = None


class ProductResponse(BaseModel):
    id: int
    name: str
    sku: str
    price: float
    stock: int
    category: str
    createdAt: str


class ErrorResponse(BaseModel):
    errors: List[str]


class SellRequest(BaseModel):
    productId: Optional[int] = None
    quantity: Optional[int] = None


class SellResponse(BaseModel):
    id: int
    name: str
    sku: str
    price: float
    stock: int
    category: str
    createdAt: str


class BulkPriceUpdateItem(BaseModel):
    productId: int
    newPrice: float


class BulkPriceUpdateRequest(BaseModel):
    items: List[BulkPriceUpdateItem] = Field(default_factory=list)


class BulkPriceUpdateResponse(BaseModel):
    updatedCount: int
    failedCount: int
    failedIds: List[int]

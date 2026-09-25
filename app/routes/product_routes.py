"""
Route layer (View)
-------------------
รับ HTTP request, ส่งต่อให้ Controller ประมวลผล แล้วแปลงผลลัพธ์เป็น response
ไม่มี business logic อยู่ในไฟล์นี้
"""

from typing import Optional

from fastapi import APIRouter, Query, status

from app.controllers.product_controller import ProductController
from app.schemas.product_schema import (
    BulkPriceUpdateRequest,
    BulkPriceUpdateResponse,
    ProductCreateRequest,
    ProductResponse,
    SellRequest,
)

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreateRequest):
    """Challenge 1: เพิ่มสินค้าใหม่"""
    product = ProductController.create_product(payload)
    return product.to_dict()


@router.get("", response_model=list[ProductResponse])
def list_products(category: Optional[str] = Query(default=None)):
    """Challenge 2: ดึงรายการสินค้า (filter ตาม category ได้)"""
    products = ProductController.get_products(category=category)
    return [p.to_dict() for p in products]


@router.post("/sell", response_model=ProductResponse)
def sell_product(payload: SellRequest):
    """Challenge 3: ขายสินค้า (ตัดสต็อก)"""
    product = ProductController.sell_product(payload)
    return product.to_dict()


@router.get("/search", response_model=list[ProductResponse])
def search_products(keyword: str = Query(default="")):
    """Challenge 4 (Bonus): ค้นหาสินค้าแบบ case-insensitive"""
    products = ProductController.search_products(keyword)
    return [p.to_dict() for p in products]


@router.put("/bulk-price-update", response_model=BulkPriceUpdateResponse)
def bulk_price_update(payload: BulkPriceUpdateRequest):
    """Challenge 5 (Bonus): อัพเดทราคาเป็นชุด"""
    updated_count, failed_count, failed_ids = ProductController.bulk_update_price(
        payload.items
    )
    return {
        "updatedCount": updated_count,
        "failedCount": failed_count,
        "failedIds": failed_ids,
    }

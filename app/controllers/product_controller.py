"""
Controller layer
-----------------
รวม business logic + validation ทั้งหมด
Route (View) จะเรียกใช้ฟังก์ชันใน controller นี้เท่านั้น ไม่ทำ logic เอง
"""

from typing import List, Optional, Tuple

from fastapi import HTTPException

from app.models.product import Product, VALID_CATEGORIES, product_storage
from app.schemas.product_schema import (
    BulkPriceUpdateItem,
    ProductCreateRequest,
    SellRequest,
)


class ProductController:

    # ---------- Challenge 1: เพิ่มสินค้าใหม่ ----------
    @staticmethod
    def create_product(payload: ProductCreateRequest) -> Product:
        errors: List[str] = []

        name = (payload.name or "").strip()
        sku = (payload.sku or "").strip()
        price = payload.price
        stock = payload.stock
        category = payload.category

        if not name:
            errors.append("ชื่อสินค้าต้องไม่ว่าง")

        if not sku:
            errors.append("รหัสสินค้าต้องไม่ว่าง")
        elif len(sku) < 3:
            errors.append("รหัสสินค้าต้องมีอย่างน้อย 3 ตัวอักษร")
        elif product_storage.sku_exists(sku):
            errors.append("รหัสสินค้านี้มีอยู่แล้วในระบบ")

        if price is None or price <= 0:
            errors.append("ราคาต้องมากกว่า 0")

        if stock is None or stock < 0:
            errors.append("จำนวนคงเหลือต้องไม่ติดลบ")

        if category is None or category not in VALID_CATEGORIES:
            errors.append(
                f"หมวดหมู่ต้องเป็นหนึ่งใน: {', '.join(VALID_CATEGORIES)}"
            )

        if errors:
            raise HTTPException(status_code=400, detail={"errors": errors})

        return product_storage.add(
            name=name, sku=sku, price=price, stock=stock, category=category
        )

    # ---------- Challenge 2: ดึงรายการสินค้า ----------
    @staticmethod
    def get_products(category: Optional[str] = None) -> List[Product]:
        products = product_storage.get_all()
        if category:
            products = [p for p in products if p.category == category]
        return products

    # ---------- Challenge 3: ขายสินค้า (ตัดสต็อก) ----------
    @staticmethod
    def sell_product(payload: SellRequest) -> Product:
        quantity = payload.quantity
        product_id = payload.productId

        # ลำดับการตรวจสอบตามโจทย์:
        # 1) quantity > 0
        if quantity is None or quantity <= 0:
            raise HTTPException(
                status_code=400,
                detail={"errors": ["จำนวนที่ต้องการขายต้องมากกว่า 0"]},
            )

        # 2) มีสินค้าในระบบหรือไม่
        product = product_storage.get_by_id(product_id) if product_id is not None else None
        if product is None:
            raise HTTPException(
                status_code=404,
                detail={"errors": ["ไม่พบสินค้าที่ต้องการขาย"]},
            )

        # 3) stock เพียงพอหรือไม่
        if product.stock < quantity:
            raise HTTPException(
                status_code=400,
                detail={"errors": ["สินค้าคงเหลือไม่เพียงพอ"]},
            )

        product.stock -= quantity
        return product

    # ---------- Challenge 4 (Bonus): ค้นหาสินค้า ----------
    @staticmethod
    def search_products(keyword: str) -> List[Product]:
        keyword_lower = (keyword or "").lower()
        return [
            p
            for p in product_storage.get_all()
            if keyword_lower in p.name.lower() or keyword_lower in p.sku.lower()
        ]

    # ---------- Challenge 5 (Bonus): อัพเดทราคาเป็นชุด ----------
    @staticmethod
    def bulk_update_price(
        items: List[BulkPriceUpdateItem],
    ) -> Tuple[int, int, List[int]]:
        updated_count = 0
        failed_ids: List[int] = []

        for item in items:
            product = product_storage.get_by_id(item.productId)
            if product is None or item.newPrice <= 0:
                failed_ids.append(item.productId)
                continue
            product.price = item.newPrice
            updated_count += 1

        return updated_count, len(failed_ids), failed_ids

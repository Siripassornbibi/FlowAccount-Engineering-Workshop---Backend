"""
Model layer
-----------
เก็บ data structure ของ Product และ "storage" (in-memory) สำหรับเก็บข้อมูล
ในระบบจริงส่วนนี้จะถูกแทนที่ด้วย ORM model (SQLAlchemy) + database
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional


# หมวดหมู่สินค้าที่อนุญาต
VALID_CATEGORIES = ["อาหาร", "เครื่องดื่ม", "ของใช้", "เสื้อผ้า"]


@dataclass
class Product:
    id: int
    name: str
    sku: str
    price: float
    stock: int
    category: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "sku": self.sku,
            "price": self.price,
            "stock": self.stock,
            "category": self.category,
            "createdAt": self.created_at.isoformat().replace("+00:00", "Z"),
        }


class ProductStorage:
    """
    In-memory storage (จำลอง database)
    """

    def __init__(self) -> None:
        self._products: List[Product] = []
        self._next_id: int = 1

    def add(self, name: str, sku: str, price: float, stock: int, category: str) -> Product:
        product = Product(
            id=self._next_id,
            name=name,
            sku=sku,
            price=price,
            stock=stock,
            category=category,
        )
        self._products.append(product)
        self._next_id += 1
        return product

    def get_all(self) -> List[Product]:
        return list(self._products)

    def get_by_id(self, product_id: int) -> Optional[Product]:
        for p in self._products:
            if p.id == product_id:
                return p
        return None

    def sku_exists(self, sku: str) -> bool:
        return any(p.sku.lower() == sku.lower() for p in self._products)


# instance เดียวที่ใช้ร่วมกันทั้งแอป (singleton แบบง่าย)
product_storage = ProductStorage()

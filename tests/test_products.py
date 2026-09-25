from fastapi.testclient import TestClient

from app.main import app
from app.models.product import product_storage

client = TestClient(app)


def reset_storage():
    product_storage._products.clear()
    product_storage._next_id = 1


def test_create_product_success():
    reset_storage()

    response = client.post(
        "/api/products",
        json={
            "name": "ข้าวผัด",
            "sku": "FOOD001",
            "price": 45.0,
            "stock": 20,
            "category": "อาหาร",
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["name"] == "ข้าวผัด"
    assert payload["sku"] == "FOOD001"
    assert payload["stock"] == 20
    assert payload["category"] == "อาหาร"


def test_create_product_duplicate_sku_returns_400():
    reset_storage()
    client.post(
        "/api/products",
        json={
            "name": "ข้าวผัด",
            "sku": "FOOD001",
            "price": 45.0,
            "stock": 20,
            "category": "อาหาร",
        },
    )

    response = client.post(
        "/api/products",
        json={
            "name": "ข้าวมันไก่",
            "sku": "FOOD001",
            "price": 60.0,
            "stock": 10,
            "category": "อาหาร",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"]["errors"] == ["รหัสสินค้านี้มีอยู่แล้วในระบบ"]


def test_sell_product_reduces_stock_and_validates_stock():
    reset_storage()
    client.post(
        "/api/products",
        json={
            "name": "น้ำเปล่า",
            "sku": "DRINK001",
            "price": 15.0,
            "stock": 10,
            "category": "เครื่องดื่ม",
        },
    )

    sell_response = client.post(
        "/api/products/sell",
        json={"productId": 1, "quantity": 3},
    )
    assert sell_response.status_code == 200
    assert sell_response.json()["stock"] == 7

    insufficient_response = client.post(
        "/api/products/sell",
        json={"productId": 1, "quantity": 20},
    )
    assert insufficient_response.status_code == 400
    assert insufficient_response.json()["detail"]["errors"] == ["สินค้าคงเหลือไม่เพียงพอ"]


def test_search_and_filter_products():
    reset_storage()
    client.post(
        "/api/products",
        json={
            "name": "ข้าวมันไก่",
            "sku": "FOOD002",
            "price": 50.0,
            "stock": 12,
            "category": "อาหาร",
        },
    )
    client.post(
        "/api/products",
        json={
            "name": "ชาเขียว",
            "sku": "DRINK002",
            "price": 20.0,
            "stock": 8,
            "category": "เครื่องดื่ม",
        },
    )

    search_response = client.get("/api/products/search?keyword=ข้าว")
    assert search_response.status_code == 200
    assert len(search_response.json()) == 1
    assert search_response.json()[0]["sku"] == "FOOD002"

    filter_response = client.get("/api/products?category=อาหาร")
    assert filter_response.status_code == 200
    assert len(filter_response.json()) == 1
    assert filter_response.json()[0]["category"] == "อาหาร"


def test_bulk_update_price_updates_valid_items_only():
    reset_storage()
    client.post(
        "/api/products",
        json={
            "name": "เสื้อยืด",
            "sku": "CLOTH001",
            "price": 200.0,
            "stock": 5,
            "category": "เสื้อผ้า",
        },
    )
    client.post(
        "/api/products",
        json={
            "name": "ยาสีฟัน",
            "sku": "HOUSE001",
            "price": 45.0,
            "stock": 8,
            "category": "ของใช้",
        },
    )

    response = client.put(
        "/api/products/bulk-price-update",
        json={
            "items": [
                {"productId": 1, "newPrice": 250},
                {"productId": 999, "newPrice": 100},
                {"productId": 2, "newPrice": -10},
            ]
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["updatedCount"] == 1
    assert payload["failedCount"] == 2
    assert payload["failedIds"] == [999, 2]

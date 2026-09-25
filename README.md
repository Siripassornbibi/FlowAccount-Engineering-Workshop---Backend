# FlowAccount Product Management API (FastAPI, MVC)

โครงสร้างแบบ MVC:

```
app/
  models/product.py          # Model  – Product dataclass + in-memory storage
  schemas/product_schema.py  # Pydantic request/response schemas
  controllers/product_controller.py  # Controller – validation + business logic
  routes/product_routes.py   # View/Route – รับ request, เรียก controller, คืน response
  main.py                    # จุดเริ่มต้นแอป, รวม router
```

## วิธีรัน

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

เปิด Swagger UI ที่ http://127.0.0.1:8000/docs

## Endpoints

| Method | Path | Challenge |
|---|---|---|
| POST | /api/products | 1: เพิ่มสินค้าใหม่ |
| GET | /api/products?category=อาหาร | 2: ดึงรายการสินค้า |
| POST | /api/products/sell | 3: ขายสินค้า (ตัดสต็อก) |
| GET | /api/products/search?keyword=ข้าว | 4 (Bonus): ค้นหาสินค้า |
| PUT | /api/products/bulk-price-update | 5 (Bonus): อัพเดทราคาเป็นชุด |

## ตัวอย่างการเรียกใช้

**เพิ่มสินค้า**
```bash
curl -X POST http://127.0.0.1:8000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"ข้าวผัด","sku":"FOOD001","price":45.00,"stock":20,"category":"อาหาร"}'
```

**ขายสินค้า**
```bash
curl -X POST http://127.0.0.1:8000/api/products/sell \
  -H "Content-Type: application/json" \
  -d '{"productId":1,"quantity":5}'
```

**อัพเดทราคาเป็นชุด**
```bash
curl -X PUT http://127.0.0.1:8000/api/products/bulk-price-update \
  -H "Content-Type: application/json" \
  -d '{"items":[{"productId":1,"newPrice":50},{"productId":2,"newPrice":30}]}'
```

## หมายเหตุการออกแบบ

- **Model**: เก็บ `Product` เป็น dataclass และใช้ list ในหน่วยความจำแทนฐานข้อมูลจริง (`ProductStorage`), เพื่อให้รันทดสอบได้ทันทีโดยไม่ต้องต่อ DB
- **Controller**: ทำ validation ตามลำดับที่โจทย์กำหนด (เช่น Challenge 3 เช็ค `quantity > 0` → มีสินค้าหรือไม่ → stock พอหรือไม่) และโยน `HTTPException` พร้อม error message ภาษาไทยตามตัวอย่าง response ในโจทย์
- **Route**: บางเบา ไม่มี logic ทำหน้าที่แค่รับ request/ส่ง response
- ทดสอบสลับ storage เป็นฐานข้อมูลจริงในอนาคตได้ง่าย เพราะ controller เรียกผ่าน `product_storage` เท่านั้น

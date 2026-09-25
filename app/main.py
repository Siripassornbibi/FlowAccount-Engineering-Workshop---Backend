from fastapi import FastAPI

from app.routes.product_routes import router as product_router

app = FastAPI(
    title="FlowAccount Product Management API",
    description="ระบบจัดการสินค้าอย่างง่าย สำหรับร้านค้า SME (MVC pattern)",
    version="1.0.0",
)

app.include_router(product_router)


@app.get("/")
def root():
    return {"message": "FlowAccount Product Management API is running"}

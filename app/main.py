from dotenv import load_dotenv
import os 
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routes.products import router as product_router

load_dotenv()
app = FastAPI(title="Product API 🚀")

app.include_router(
    product_router,
    prefix="/products",
    tags=["Products"]
)

@app.get("/")
def root():
    DB_PATH = os.getenv("BASE_URL")
    return JSONResponse(
        status_code=200,
        content={
            "message": "Welcome to FastAPI",
            "data_path": DB_PATH
        }
    )
    # return {"message": "FastAPI Product API running", "URL": DB_PATH}

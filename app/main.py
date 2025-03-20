from fastapi import FastAPI, HTTPException
from app.models import Product,CartItem,BillResponse
from typing import List

app = FastAPI()

# Sample product data
products_db = [
    {
        "ProdID": 1, 
        "ProdName": "LG 185 L 5 Star Inverter Direct-Cool Single Door Refrigerator", 
        "Brand": "LG",
        "Model": "GL-D201ABEU",
        "Price": 17490
    },
    {
        "ProdID": 2, 
        "ProdName": "LG 322 L 3 Star Frost-Free Smart Inverter Double Door Refrigerator (GL-S342SDSX, Dazzle Steel, Convertible with Express Freeze)", 
        "Brand": "LG",
        "Model": "GL-S342SDSX",
        "Price": 36990
    },
    {
        "ProdID": 3, 
        "ProdName": "Bosch 10kg 5 Star Anti Stain & AI Active Water Plus Fully Automatic Front Load Washing Machine with Built-in Heater (WGA252ZSIN, Pretreatment, Iron Steam Assist & Allergy Plus, Silver)", 
        "Brand": "Bosch",
        "Model": "WGA252ZSIN",
        "Price": 42990
    },
    {
        "ProdID": 4, 
        "ProdName": "Samsung 12 kg, 5 Star, AI Ecobubble, Super Speed, Wi-Fi, Hygiene Steam with Inbuilt Heater, Digital Inverter, Fully-Automatic Front Load Washing Machine (WW12DG6B24ASTL, Navy)", 
        "Brand": "Samsung",
        "Model": "WW12DG6B24ASTL",
        "Price": 46990
    },
    {
        "ProdID": 5, 
        "ProdName": "Sony Alpha ILCE-6100L APS-C Camera (16-50mm Lens) | 24.2 MP | Fast Auto Focus, Real-time Eye AF, Real-time Tracking | 4K Vlogging Camera – Black", 
        "Brand": "Sony",
        "Model": "ILCE-6100L",
        "Price": 61490
    },
    {
        "ProdID": 6, 
        "ProdName": "Fujifilm X-T5 40MP APS-C X-Trans Sensor | Pixel Shift | IBIS System | Ultra High Resolution Mirrorless Camera | 6.2k 30p | Subject Tracking | 1/180000 Shutter Speed | Touchtracking | Quick Lever for Photo/Video - S", 
        "Brand": "Fujifilm",
        "Model": "203399",
        "Price": 143000
    }
]


cart_db = []


@app.get("/products", response_model=List[Product])
async def get_products():
    return products_db

@app.post("/cart")
async def add_to_cart(cart_item: CartItem):
    print(cart_item)
    product = next((item for item in products_db if item["ProdID"] == cart_item.ProdID), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    cart_db.append({"ProdID": cart_item.ProdID, "Qty": cart_item.Qty})
    return {"cart": cart_db, "message": "Item added successfully"}

@app.get("/bill", response_model=BillResponse)
async def calculate_bill():
    total = 0
    bill_items = []

    for cart_item in cart_db:
        product = next((item for item in products_db if item["ProdID"] == cart_item["ProdID"]), None)
        if not product:
            continue
        product_total = product["Price"] * cart_item["Qty"]

        total += product_total
        bill_items.append({
            "ProdId": cart_item["ProdID"],
            "Qty": cart_item["Qty"],
            "Total": product_total
        })

    return BillResponse(Products = bill_items, Total= total)
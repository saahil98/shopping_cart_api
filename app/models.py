from pydantic import BaseModel
from typing import List

class Product(BaseModel):
    ProdID: int
    ProdName: str
    Brand: str
    Model: str
    Price: int

class CartItem(BaseModel):
    ProdID: int
    Qty: int

class BillResponse(BaseModel):
    Products: List[dict]
    Total: int


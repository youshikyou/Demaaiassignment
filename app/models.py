from pydantic import BaseModel
from typing import Optional,List

class InventoryQueryParams(BaseModel):
    category: Optional[str] = None
    subcategory: Optional[str] = None
    in_stock: Optional[bool] = False
    sort_order: Optional[str] = "stock"
    page: int = 1
    per_page: int = 10

class InventoryUpdateItem(BaseModel):
    productId: str
    quantity: int

class BulkInventoryUpdate(BaseModel):
    updates: List[InventoryUpdateItem]
from fastapi import FastAPI, Response
from pydantic import BaseModel

app = FastAPI()



class Product(BaseModel):
    name: str
    price: float



products = [
    {"id": 1, "name": "iPad", "price": 599},
    {"id": 2, "name": "iPhone", "price": 999},
    {"id": 3, "name": "iWatch", "price": 699},
]

@app.get("/products")
def index():
    return products


@app.get("/products/{id}")
def index(id: int):
    for product in products:
        if product["id"] == id:
            return product
    return "Not found" 

@app.post("/products")
def create_product(new_product: Product, response: Response):
    product = new_product.dict()
    product["id"] = len(products) + 1
    products.append(product)
    response.status_code = 201
    return product
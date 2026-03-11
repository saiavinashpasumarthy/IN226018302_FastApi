from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

# Temporary data
products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499, 'category': 'Electronics', 'in_stock': True},
    {'id': 2, 'name': 'Notebook', 'price': 99, 'category': 'Stationary', 'in_stock': True},
    {'id': 3, 'name': 'USB Hub', 'price': 799, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Pen Set', 'price': 49, 'category': 'Stationary', 'in_stock': True},
    {"id": 5, "name": "Laptop Stand", "price": 1299, "category": "Electronics", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 1899, "category": "Electronics", "in_stock": False},
]

# Home
@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}

# All products
@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}

# Filter endpoint
@app.get('/products/filter')
def filter_products(
    category: str = Query(None, description='Electronics or Stationary'),
    max_price: int = Query(None, description='Maximum price'),
    in_stock: bool = Query(None, description='True = in stock only'),
    min_price: int = Query(None, description='Minimum price')
):
    result = products

    if category:
        result = [p for p in result if p['category'] == category]

    if max_price:
        result = [p for p in result if p['price'] <= max_price]

    if in_stock is not None:
        result = [p for p in result if p['in_stock'] == in_stock]
    return {'filtered_products': result, 'count': len(result)}

# Category filter
@app.get("/products/category/{category_name}")
def get_products_by_category(category_name: str):

    filtered_products = []

    for product in products:
        if product["category"].lower() == category_name.lower():
            filtered_products.append(product)

    if len(filtered_products) == 0:
        return {"error": "No products found in this category"}

    return {
        "category": category_name,
        "products": filtered_products,
        "count": len(filtered_products)
    }

# In-stock products
@app.get("/products/instock")
def get_instock():
    available = [p for p in products if p["in_stock"] == True]

    return {
        "in_stock_products": available,
        "count": len(available)
    }

#Store summary endpoint
@app.get("/store/summary")
def store_summary():

    in_stock_count = len([p for p in products if p["in_stock"]])
    out_stock_count = len(products) - in_stock_count

    categories = list(set([p["category"] for p in products]))

    return {
        "store_name": "My E-commerce Store",
        "total_products": len(products),
        "in_stock": in_stock_count,
        "out_of_stock": out_stock_count,
        "categories": categories
    }

#Products Search endpoint
@app.get("/products/search/{keyword}")
def search_products(keyword: str):

    results = [
        p for p in products
        if keyword.lower() in p["name"].lower()
    ]

    if not results:
        return {"message": "No products matched your search"}

    return {
        "keyword": keyword,
        "results": results,
        "total_matches": len(results)
    }

@app.get("/products/deals")
def get_deals():

    cheapest = min(products, key=lambda p: p["price"])
    expensive = max(products, key=lambda p: p["price"])

    return {
        "best_deal": cheapest,
        "premium_pick": expensive
    }

# Product by ID 
@app.get('/products/{product_id}')
def get_product(product_id: int):

    for product in products:
        if product['id'] == product_id:
            return {'product': product}

    return {'error': 'Product not found'}
#Day 2 endpoints
# Q1 --- Endpoint 1 ---
@app.get("/products/filter")
def filter_products(min_price: int = None, max_price: int = None, category: str = None):

    filtered = products

    # filter by minimum price
    if min_price is not None:
        filtered = [p for p in filtered if p["price"] >= min_price]

    # filter by maximum price
    if max_price:
        filtered = [p for p in filtered if p["price"] <= max_price]

    # filter by category
    if category:
        filtered = [p for p in filtered if p["category"].lower() == category.lower()]

    return {
        "filtered_products": filtered,
        "count": len(filtered)
    }

# Q2 --- Endpoint 2 ---

@app.get("/products/{product_id}/price")
def get_product_price(product_id: int):

    # find product by id
    product = next((p for p in products if p["id"] == product_id), None)

    # if product not found
    if product is None:
        return {"error": "Product not found"}

    # return only name and price
    return {
        "name": product["name"],
        "price": product["price"]
    }

# Feedback list (temp storage)
feedback = []

# Customer Feedback Model
class CustomerFeedback(BaseModel):
    customer_name: str = Field(..., min_length=2)
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=300)

# Q3 --- Endpoint 3 ---
@app.post("/feedback")
def submit_feedback(data: CustomerFeedback):

    # convert model to dictionary
    feedback_data = data.model_dump()

    # save feedback
    feedback.append(feedback_data)

    return {
        "message": "Feedback submitted successfully",
        "feedback": feedback_data,
        "total_feedback": len(feedback)
    }

# Q4 --- Endpoint 4 ---
@app.get("/products/{product_id}/summary")
def product_summary(product_id: int):

    # find product by id
    product = next((p for p in products if p["id"] == product_id), None)

    # if product not found
    if product is None:
        return {"error": "Product not found"}

    # total products
    total_products = len(products)

    # in stock products
    in_stock_count = len([p for p in products if p["in_stock"]])

    # out of stock products
    out_of_stock_count = len([p for p in products if not p["in_stock"]])

    # most expensive product
    most_expensive_product = max(products, key=lambda p: p["price"])

    # cheapest product
    cheapest_product = min(products, key=lambda p: p["price"])

    # unique categories
    categories = list(set([p["category"] for p in products]))

    return {
        "total_products": total_products,
        "in_stock_count": in_stock_count,
        "out_of_stock_count": out_of_stock_count,
        "most_expensive": {
            "name": most_expensive_product["name"],
            "price": most_expensive_product["price"]
        },
        "cheapest": {
            "name": cheapest_product["name"],
            "price": cheapest_product["price"]
        },
        "categories": categories
    }

# Order Item Model
class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=1, le=50)

# Bulk Order Model
class BulkOrder(BaseModel):
    company_name: str = Field(..., min_length=2)
    contact_email: str = Field(..., min_length=5)
    items: List[OrderItem] = Field(..., min_items=1)

# Q5 --- Endpoint 5 ---
@app.post("/orders/bulk")
def place_bulk_order(order: BulkOrder):

    confirmed = []
    failed = []
    grand_total = 0

    for item in order.items:

        # find product
        product = next((p for p in products if p["id"] == item.product_id), None)

        # product not found
        if product is None:
            failed.append({
                "product_id": item.product_id,
                "reason": "Product not found"
            })
            continue

        # product out of stock
        if not product["in_stock"]:
            failed.append({
                "product_id": item.product_id,
                "reason": f'{product["name"]} is out of stock'
            })
            continue

        # calculate subtotal
        subtotal = product["price"] * item.quantity
        grand_total += subtotal

        confirmed.append({
            "product": product["name"],
            "qty": item.quantity,
            "subtotal": subtotal
        })

    return {
        "company": order.company_name,
        "confirmed": confirmed,
        "failed": failed,
        "grand_total": grand_total
    }

# Orders storage
orders = []
order_counter = 1

# Q6 --- Endpoint 6 ---
@app.post("/orders")
def create_order(order: BulkOrder):

    global order_counter

    new_order = {
        "order_id": order_counter,
        "company": order.company_name,
        "contact_email": order.contact_email,
        "items": [item.model_dump() for item in order.items],
        "status": "pending"
    }

    orders.append(new_order)

    order_counter += 1

    return {
        "message": "Order placed successfully",
        "order": new_order
    }

# Q6 --- Endpoint 7 ---
@app.get("/orders/{order_id}")
def get_order(order_id: int):

    order = next((o for o in orders if o["order_id"] == order_id), None)

    if order is None:
        return {"error": "Order not found"}

    return order

# Q6 --- Endpoint 8 ---
@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id: int):

    order = next((o for o in orders if o["order_id"] == order_id), None)

    if order is None:
        return {"error": "Order not found"}

    order["status"] = "confirmed"

    return {
        "message": "Order confirmed",
        "order": order
    }
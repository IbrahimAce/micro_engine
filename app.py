# app.py  (Phase 5 — adds ORM models and new routes)

import asyncio
import json
from router import Router
from request import Request
from server import run_async_server
from models import BaseModel

app = Router()

# ---------------------------------------------------------------
# Define models
# ---------------------------------------------------------------

class User(BaseModel):
    name: str
    age: int

class Product(BaseModel):
    title: str
    price: float

# ---------------------------------------------------------------
# Routes
# ---------------------------------------------------------------

@app.route("/", "GET")
async def home(request: Request):
    return "Welcome to Micro-Engine!"

@app.route("/about", "GET")
async def about(request: Request):
    return "Micro-Engine v0.1 — built from scratch!"

@app.route("/users", "GET")
async def list_users(request: Request):
    users = User.all()
    if not users:
        return "No users yet. POST to /users to create one."
    return "\n".join(str(u) for u in users)

@app.route("/users", "POST")
async def create_user(request: Request):
    # Expects body like: name=Alice&age=30
    body = request.body.decode("utf-8", errors="replace")
    params = {}
    for pair in body.split("&"):
        if "=" in pair:
            k, v = pair.split("=", 1)
            params[k.strip()] = v.strip()

    name = params.get("name", "Unknown")
    age  = int(params.get("age", 0))

    user = User(name=name, age=age)
    user.save()
    return f"Created: {user}"

@app.route("/products", "POST")
async def create_product(request: Request):
    body = request.body.decode("utf-8", errors="replace")
    params = {}
    for pair in body.split("&"):
        if "=" in pair:
            k, v = pair.split("=", 1)
            params[k.strip()] = v.strip()

    title = params.get("title", "Unknown")
    price = float(params.get("price", 0.0))

    product = Product(title=title, price=price)
    product.save()
    return f"Created: {product}"

@app.route("/slow", "GET")
async def slow_route(request: Request):
    print("  /slow started — sleeping 5 seconds...")
    await asyncio.sleep(5)
    print("  /slow finished!")
    return "Slow response finished!"

# ---------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(run_async_server(app))

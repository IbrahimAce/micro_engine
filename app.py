# app.py  (Phase 6 — all routes wrapped with timing middleware)
#
# Notice the decorator order:
#   @app.route("/users", "GET")
#   @apply_timing
#   async def list_users(request):
#
# Python applies decorators bottom-up, so apply_timing runs first,
# then app.route stores the already-wrapped function.

import asyncio
from router import Router
from request import Request
from server import run_async_server
from models import BaseModel
from middleware import apply_timing

app = Router()

# ---------------------------------------------------------------
# Models
# ---------------------------------------------------------------

class User(BaseModel):
    name: str
    age: int

class Product(BaseModel):
    title: str
    price: float

# ---------------------------------------------------------------
# Routes — each wrapped with @apply_timing
# ---------------------------------------------------------------

@app.route("/", "GET")
@apply_timing
async def home(request: Request):
    await asyncio.sleep(0.1)
    return "Welcome to Micro-Engine!"

@app.route("/about", "GET")
@apply_timing
async def about(request: Request):
    return "Micro-Engine v0.1 — built from scratch!"

@app.route("/users", "GET")
@apply_timing
async def list_users(request: Request):
    users = User.all()
    if not users:
        return "No users yet. POST to /users to create one."
    return "\n".join(str(u) for u in users)

@app.route("/users", "POST")
@apply_timing
async def create_user(request: Request):
    body   = request.body.decode("utf-8", errors="replace")
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
@apply_timing
async def create_product(request: Request):
    body   = request.body.decode("utf-8", errors="replace")
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
@apply_timing
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

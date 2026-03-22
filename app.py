# app.py  (Phase 4 — handlers are now async def)
#
# "async def" handlers can use "await asyncio.sleep()" to simulate
# waiting for something slow (like a database) without blocking others.

import asyncio
from router import Router
from request import Request
from server import run_async_server

app = Router()

# ---------------------------------------------------------------
# Routes — now using async def
# ---------------------------------------------------------------

@app.route("/", "GET")
async def home(request: Request):
    # Simulate a 1-second database query
    await asyncio.sleep(1)
    return "Welcome to async Micro-Engine!"

@app.route("/users", "GET")
async def list_users(request: Request):
    await asyncio.sleep(0.5)
    return "User list: [Alice, Bob, Charlie]"

@app.route("/users", "POST")
async def create_user(request: Request):
    body = request.body.decode("utf-8", errors="replace")
    await asyncio.sleep(0.2)
    return f"Created user with data: {body}"

@app.route("/about", "GET")
async def about(request: Request):
    return "Micro-Engine v0.1 — built from scratch!"

@app.route("/slow", "GET")
async def slow_route(request: Request):
    # 5-second delay — use this to prove concurrency works
    print("  /slow started — sleeping 5 seconds...")
    await asyncio.sleep(5)
    print("  /slow finished!")
    return "Slow response finished!"

# ---------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(run_async_server(app))

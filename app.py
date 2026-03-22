# app.py
# This is where we define our routes (URL -> function mappings).
# We import the Router, create one instance called "app",
# then use @app.route() to register handler functions.
#
# The server imports "app" from here and asks it for the right handler.

from router import Router
from request import Request

# Create the single global router instance
app = Router()

# ---------------------------------------------------------------
# Define routes below using @app.route(path, method)
# ---------------------------------------------------------------

@app.route("/", "GET")
def home(request: Request):
    return "Welcome to Micro-Engine!"

@app.route("/users", "GET")
def list_users(request: Request):
    return "User list: [Alice, Bob, Charlie]"

@app.route("/users", "POST")
def create_user(request: Request):
    body = request.body.decode("utf-8", errors="replace")
    return f"Created user with data: {body}"

@app.route("/about", "GET")
def about(request: Request):
    return "Micro-Engine v0.1 — built from scratch!"

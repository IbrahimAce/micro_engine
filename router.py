# router.py
# A Router stores a mapping of (METHOD, path) -> handler function.
#
# The @app.route("/users", "GET") decorator works like this:
#   1. app.route("/users", "GET") is called — it returns a decorator function
#   2. That decorator is applied to the function below it
#   3. The function is stored in self.routes under the key ("GET", "/users")
#   4. The original function is returned unchanged so it can still be called normally
#
# This is called a "decorator factory" — a function that returns a decorator.

class Router:
    def __init__(self):
        # Dictionary mapping (METHOD, path) to a handler function
        # Example: {("GET", "/users"): <function list_users>}
        self.routes = {}

    def route(self, path: str, method: str = "GET"):
        """Decorator factory. Usage: @app.route("/path", "GET")"""
        def decorator(handler):
            key = (method.upper(), path)
            self.routes[key] = handler
            print(f"  Registered route: {method.upper()} {path}")
            return handler  # return handler unchanged
        return decorator

    def get_handler(self, method: str, path: str):
        """Look up the handler for a given method and path. Returns None if not found."""
        return self.routes.get((method.upper(), path))

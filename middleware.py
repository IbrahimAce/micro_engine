# middleware.py
#
# A Context Manager is an object that works with Python's "with" statement:
#
#   with TimingContext("my task"):
#       do_something()
#
# __enter__ runs before the "with" block.
# __exit__ runs after the "with" block, even if an exception occurred.
#
# We use this to measure time: record start in __enter__, compute elapsed in __exit__.

import time
import inspect


class TimingContext:
    """
    Context manager that measures how long a block of code takes.

    Usage:
        with TimingContext("GET /users") as ctx:
            result = do_work()
        # After the with block: ctx.elapsed holds the time in seconds
    """

    def __init__(self, label: str):
        self.label   = label
        self.elapsed = 0.0

    def __enter__(self):
        self.start = time.perf_counter()   # high-precision timer
        return self                         # this is what "as ctx" gets

    def __exit__(self, exc_type, exc_val, exc_tb):
        # exc_type is None if no exception occurred
        self.elapsed = time.perf_counter() - self.start
        status = "ERROR" if exc_type else "OK"
        print(f"  [Timing] {self.label} — {self.elapsed:.4f}s [{status}]")
        return False   # False means: don't suppress exceptions


def apply_timing(handler):
    """
    Wraps a route handler with timing middleware.
    Works with both regular and async handlers.

    Usage:
        @app.route("/users", "GET")
        @apply_timing        <-- add this line under @app.route
        async def list_users(request):
            ...
    """
    async def wrapped(request):
        with TimingContext(f"{request.method} {request.path}"):
            result = handler(request)
            if inspect.iscoroutine(result):
                result = await result
        return result

    return wrapped

# server.py  (Phase 4 — fully async)
#
# asyncio.start_server() replaces the manual socket.accept() loop.
# For every new connection it automatically calls handle_client().
#
# "async def" means the function is a coroutine — it can be paused.
# "await" means: pause here and let other coroutines run while we wait.
#
# inspect.iscoroutine() checks if calling handler(req) returned a coroutine
# (i.e. whether the handler is "async def") so we know whether to await it.

import asyncio
import inspect
from request import Request

async def handle_client(reader, writer, router):
    try:
        # await reader.read() — wait for data without blocking other requests
        data = await reader.read(4096)

        if not data:
            writer.close()
            return

        req = Request(data)
        print(f"{req.method} {req.path}")

        handler = router.get_handler(req.method, req.path)

        if handler is not None:
            # Call the handler — it might be async or regular
            result = handler(req)

            # If it returned a coroutine (async def), we must await it
            if inspect.iscoroutine(result):
                result = await result

            status_line = b"HTTP/1.1 200 OK"
        else:
            result = f"404 Not Found: {req.path}"
            status_line = b"HTTP/1.1 404 Not Found"

        if isinstance(result, bytes):
            body = result
        else:
            body = result.encode("utf-8")

        response = (
            status_line + b"\r\n"
            b"Content-Type: text/plain\r\n"
            b"Content-Length: " + str(len(body)).encode() + b"\r\n"
            b"\r\n"
        ) + body

        writer.write(response)
        await writer.drain()  # wait until data is actually sent

    except Exception as e:
        print(f"Error handling request: {e}")
    finally:
        # Always close the connection
        writer.close()
        try:
            await writer.wait_closed()
        except Exception:
            pass


async def run_async_server(router, host="127.0.0.1", port=8080):
    # lambda r, w: creates a small function that passes the router in
    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, router),
        host,
        port
    )

    print("=" * 50)
    print("Phase 4: Async server")
    print(f"Listening on http://{host}:{port}")
    print("Registered routes:")
    for key in router.routes:
        print(f"  {key[0]} {key[1]}")
    print("Press Ctrl+C to stop")
    print("=" * 50)

    async with server:
        await server.serve_forever()

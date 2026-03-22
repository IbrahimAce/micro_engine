# 🔧 Micro-Engine — Web Framework from Scratch

> **A fully functional async web framework built using only Python's standard library.**  
> No Flask. No FastAPI. No Django. Just pure Python 3.

---

## 🎯 What Is This?

Micro-Engine is a learning project that rebuilds the core mechanics of a modern web framework from scratch — one layer at a time. By the end you will understand exactly how frameworks like Flask and FastAPI work under the hood.

---

## 🧠 What You Learn

| Concept | Where It Appears |
|---|---|
| 🔌 TCP Sockets & HTTP | `server.py` + `request.py` |
| 🗺️ URL Routing with Decorators | `router.py` |
| ⚡ Async / Non-blocking I/O | `server.py` using `asyncio` |
| 🗄️ ORM with Metaclasses | `models.py` |
| ⏱️ Middleware with Context Managers | `middleware.py` |

---

## 📁 Project Structure
```
micro_engine/
├── app.py          ← Routes, models, and entry point
├── server.py       ← Async TCP server using asyncio
├── request.py      ← HTTP request parser
├── router.py       ← @app.route() decorator + route lookup
├── models.py       ← Metaclass ORM + BaseModel
├── middleware.py   ← TimingContext + apply_timing
├── database.db     ← SQLite database (auto-created on first run)
├── .gitignore
└── README.md
```

---

## 🚀 How to Run
```bash
git clone https://github.com/IbrahimAce/micro_engine.git
cd micro_engine
python3 -m venv venv
source venv/bin/activate
python3 app.py
```

Server starts at **http://127.0.0.1:8080**

---

## 🛣️ Available Routes

| Method | Path | Description |
|---|---|---|
| GET | `/` | Home page |
| GET | `/about` | About the framework |
| GET | `/users` | List all users from database |
| POST | `/users` | Create a user (`name=Alice&age=30`) |
| POST | `/products` | Create a product (`title=Laptop&price=999.99`) |
| GET | `/slow` | 5-second delay — tests concurrency |

---

## 🏗️ Build Phases

### Phase 1 — 🔌 Raw Socket Server
Built a TCP server using Python's `socket` module. Listens on `localhost:8080`, accepts connections, reads raw bytes, and prints the full HTTP request to the console.

**Key concept:** TCP handshakes, byte-to-string decoding, `socket.accept()`.

---

### Phase 2 — 📦 HTTP Request Parser
Implemented a `Request` class that extracts Method, Path, Headers, and Body from raw bytes.

**Key concept:** HTTP anatomy, string manipulation, `\r\n` line endings.

---

### Phase 3 — 🗺️ Routing Engine
`@app.route(path, method)` decorator maps URLs to handler functions stored in a dictionary.

**Key concept:** Higher-order functions, decorator factories, first-class functions.

---

### Phase 4 — ⚡ Async Server with Asyncio
Replaced blocking socket loop with `asyncio.start_server()`. Slow requests no longer block others.

**Key concept:** Event loops, coroutines, `async`/`await`, WSGI vs ASGI.

---

### Phase 5 — 🗄️ Mini-ORM (Metaclass Magic)
`BaseModel` uses a Metaclass to read type annotations and auto-create SQLite tables. `.save()` generates INSERT SQL dynamically.
```python
class User(BaseModel):
    name: str
    age: int

User(name="Alice", age=30).save()
```

**Key concept:** Metaclasses, `__annotations__`, dunder methods, SQLite.

---

### Phase 6 — ⏱️ Middleware with Context Manager
`@apply_timing` wraps every route with a `TimingContext` that measures request duration using `__enter__` and `__exit__`.

**Key concept:** Context manager protocol, wrapper functions.

---

## ✅ Milestones

| Milestone | Deliverable | Status |
|---|---|---|
| 1 | Raw socket server prints HTTP headers | ✅ Done |
| 2 | Async router with `async def` handlers | ✅ Done |
| 3 | Mini-ORM saves objects via `model.save()` | ✅ Done |
| 4 | Server handles 10 concurrent requests | ✅ Done |

---

## 🧰 Requirements

- Python 3.8+
- No external packages — standard library only

---

## 👤 Author

**Ibrahim** — [@IbrahimAce](https://github.com/IbrahimAce)  
Built as a learning project to understand the internals of modern Python web frameworks.

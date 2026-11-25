---
name: fastapi-pro
description: "FastAPI application development including dependency injection, Pydantic v2 models, async endpoints, middleware, WebSocket, background tasks, and production deployment. Trigger when users build REST APIs with FastAPI, need help with Pydantic models/validation, dependency injection patterns, or FastAPI performance optimization."
---

# FastAPI Pro

You are a FastAPI expert focused on building production-grade async APIs.

## Core Principles

- **Pydantic v2 for everything.** Request/response models, settings, validation — Pydantic handles it all.
- **Dependency injection over global state.** Use `Depends()` for database sessions, auth, config.
- **Async by default.** Use `async def` for I/O-bound endpoints. Use `def` for CPU-bound (FastAPI runs them in a threadpool).
- **Structured error handling.** Custom exception handlers with consistent error response format.

## Anti-Patterns

- Putting business logic directly in route handlers — use service layer
- Not using response_model — clients get unvalidated, potentially sensitive data
- Sync database calls in async endpoints — blocks the event loop
- Global mutable state instead of dependency injection

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Dependency injection | `references/dependencies.md` | DB sessions, auth, pagination |
| Pydantic v2 patterns | `references/pydantic.md` | Models, validators, settings |
| Production setup | `references/production.md` | Middleware, CORS, deployment |

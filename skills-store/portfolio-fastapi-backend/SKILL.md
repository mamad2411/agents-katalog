---
name: portfolio-fastapi-backend
description: "Implement FastAPI routing, Pydantic models, services, and stream behavior."
---

# portfolio-fastapi-backend

Use backend/api for routers, models for Pydantic schemas, services for substantial business logic, and core for shared configuration/dependencies. Use async for asynchronous I/O; keep blocking work out of the event loop rather than blindly converting every function.

Define boundary changes in contracts first. Validate inputs and test failure cases, stream termination and cancellation where relevant. Do not assume persistence/auth/LLM integration exists. Use isolated test dependencies documented in backend/README.md. Do not prescribe unavailable formatting tools as mandatory commands.

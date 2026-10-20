---
description:
globs:
alwaysApply: true
---

  You are an expert in Python, FastAPI, and scalable API development.

  # FastAPI Project Structure and Guidelines

    apeesa-backend/
    └── app/
        ├── api/                  # API layer
        │   ├── endpoints/        # Route handlers for different features
        │   └── api.py            # Main API router configuration
        │
        ├── core/                 # Core functionality
        │   ├── security.py       # Security utilities
        │   └── permissions.py    # Role-based access control
        │
        ├── db/                   # Database layer
        │   ├── database.py       # Database configuration
        │   └── models/           # SQLAlchemy models named by convention DB<ModelName>.py
        │
        ├── services/             # Business logic layer
        ├── schemas/              # Pydantic models for request/response validation
        ├── utils/                # Utility functions and helpers
        ├── crud/                 # Database operations (Create, Read, Update, Delete)
        ├── routes/               # Additional route handlers
        ├── tasks/                # Background task processing
        ├── cache/                # Caching mechanisms
        ├── auth/                 # Authentication components
        │   └── auth.py           # Authentication logic
        ├── mock/                 # Mock data and testing utilities
        └── main.py               # Application entry point

  Key Principles
  - Write concise, technical responses with accurate Python examples.
  - Use functional, declarative programming; avoid classes where possible.
  - Prefer iteration and modularization over code duplication.
  - Use descriptive variable names with auxiliary verbs (e.g., is_active, has_permission).
  - Use lowercase with underscores for directories and files (e.g., routers/user_routes.py).
  - Favor named exports for routes and utility functions.
  - Use the Receive an Object, Return an Object (RORO) pattern.
  - Use a service-oriented approach to integrations
  - Always find and activate the relevant virtual environment, if it not already active, before running Python commands.  The directory will not always be called venv so be sure to search_files for the virtual environment directory.

  Python/FastAPI
  - Use def for pure functions and async def for asynchronous operations.
  - Use type hints for all function signatures. Prefer Pydantic models over raw dictionaries for input validation.
  - File structure: exported router, sub-routes, utilities, static content, types (models, schemas).
  - Avoid unnecessary curly braces in conditional statements.
  - For single-line statements in conditionals, omit curly braces.
  - Use concise, one-line syntax for simple conditional statements (e.g., if condition: do_something()).
  - Always review existing API routes to follow the existing patterns for prefixes etc. before adding new routes or making changes to existing routes.
  - Don't bother looking for a .env file.  You can't see it, but it's there.
  - Never copy the .env file into a Docker image.

  Alembic Migrations
  - Migrations should never delete existing tables unless the migration itself it intended to delete tables.
  - Migrations should be limited to exactly what they need to do, nothing more.
  - Never try to update existing migrations that have already been applied.
  - Alembic migrations always go in the alembic folder

  Error Handling and Validation
  - Prioritize error handling and edge cases:
    - Handle errors and edge cases at the beginning of functions.
    - Use early returns for error conditions to avoid deeply nested if statements.
    - Place the happy path last in the function for improved readability.
    - Avoid unnecessary else statements; use the if-return pattern instead.
    - Use guard clauses to handle preconditions and invalid states early.
    - Implement proper error logging and user-friendly error messages.
    - Use custom error types or error factories for consistent error handling.

  Dependencies
  - FastAPI
  - Pydantic v2
  - Async database libraries like asyncpg or aiomysql
  - SQLAlchemy 2.0 (if using ORM features)

  FastAPI-Specific Guidelines
  - Use functional components (plain functions) and Pydantic models for input validation and response schemas.
  - Use declarative route definitions with clear return type annotations.
  - Use def for synchronous operations and async def for asynchronous ones.
  - Minimize @app.on_event("startup") and @app.on_event("shutdown"); prefer lifespan context managers for managing startup and shutdown events.
  - Use middleware for logging, error monitoring, and performance optimization.
  - Optimize for performance using async functions for I/O-bound tasks, caching strategies, and lazy loading.
  - Use HTTPException for expected errors and model them as specific HTTP responses.
  - Use middleware for handling unexpected errors, logging, and error monitoring.
  - Use Pydantic's BaseModel for consistent input/output validation and response schemas.

  Performance Optimization
  - Minimize blocking I/O operations; use asynchronous operations for all database calls and external API requests.
  - Implement caching for static and frequently accessed data using tools like Redis or in-memory stores.
  - Optimize data serialization and deserialization with Pydantic.
  - Use lazy loading techniques for large datasets and substantial API responses.

  Key Conventions
  1. Rely on FastAPI’s dependency injection system for managing state and shared resources.
  2. Prioritize API performance metrics (response time, latency, throughput).
  3. Limit blocking operations in routes:
     - Favor asynchronous and non-blocking flows.
     - Use dedicated async functions for database and external API operations.
     - Structure routes and dependencies clearly to optimize readability and maintainability.

  Refer to FastAPI documentation for Data Models, Path Operations, and Middleware for best practices.

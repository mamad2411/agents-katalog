---
name: "developing-serverpod-backend"
description: "Develops full-stack Dart backends using the Serverpod framework with PostgreSQL, Redis, and Docker. Use when building type-safe API endpoints, defining YAML data models, configuring Serverpod auth, writing server-side tests, running database migrations, deploying to Docker/AWS/GCP, or creating database-less servers for stateless proxy/BFF endpoints."
metadata:
  last_modified: "2026-04-01 14:35:00 (GMT+8)"
---

# Serverpod Architecture & Development Guide

## Overview

Serverpod splits projects into modules: `server`, `client`, and (fullstack template) `<name>_flutter`. Models defined in `.spy.yaml` files generate type-safe Dart classes and database migrations via `serverpod generate`.

---

# Process

## High-Level Workflow

### Phase 1: Research & Modeling

#### 1.1 Understand Project Structure
Serverpod separates code into `server` and `client` modules (the fullstack template adds `<name>_flutter`). Endpoint logic lives in `server`; generated client code goes into `client`.

#### 1.2 Define Data Models
Define database models using `.spy.yaml` files, then run `serverpod generate` to produce Dart classes and database migrations. Use explicit foreign key mappings for relational tables.
- [Core Architecture & Models Guide](./references/core-and-models.md) - YAML model definitions, project structure, and relationship mapping.

---

### Phase 2: Implementation

#### 2.1 Develop Endpoints
Implement business logic inside endpoint classes. Use session parameters for authentication context, built-in caching, and native JSON serialization.
- [Endpoints & Database Guide](./references/endpoints-and-database.md) - Typed ORM queries, transactions, and API endpoint patterns.

#### 2.2 Authentication & Caching
Use the `serverpod_auth` module for token-based authentication. Configure Redis for caching to reduce repeated database queries.
- [Authentication & Caching Guide](./references/auth-and-caching.md) - `serverpod_auth` setup, endpoint protection, and Redis caching.

#### 2.3 Database-less Backends
Serverpod 4 has no separate Mini variant. For stateless proxy/BFF endpoints, create a server without a database: `serverpod create <name> --template server --no-database --no-redis --no-auth`.

---

### Phase 3: Deployment

#### 3.1 Docker & Production
Use `docker-compose` to orchestrate local and production environments. Configure environment variables for credentials and connection strings.
- [Deployment & Docker Guide](./references/deployment-and-docker.md) - Production Dockerfiles, AWS/GCP deployment, environment configuration.

---

# Reference Files

## Documentation Library

### Core Framework (Load First)
- [Serverpod Overview](./references/overview.md) - Setup, project structure, and architecture decisions.

### Schema and Logic (Load During Phase 1/2)
- [Core Architecture & Models Guide](./references/core-and-models.md) - YAML models, database schema, directory structure.
- [Endpoints & Database Guide](./references/endpoints-and-database.md) - ORM, typed queries, API endpoints.

### Security, Scaling & Testing (Load During Phase 2/3)
- [Authentication & Caching Guide](./references/auth-and-caching.md) - `serverpod_auth`, endpoint protection, Redis caching.
- [Deployment & Docker Guide](./references/deployment-and-docker.md) - AWS/GCP, Docker, environment management.
- [Testing Guide](./references/serverpod-testing.md) - Isolated database testing, endpoint simulation, auto-generated test utilities.

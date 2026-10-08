# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Brazilian toll road management API (Projeto Georef / BGM). Rust backend with Actix-web, PostgreSQL database, Angular frontend, all orchestrated via Docker Compose with Nginx reverse proxy.

## Common Commands

- **Build release:** `make target` (runs `cargo build --release`)
- **Run tests:** `cargo test` (requires a running PostgreSQL instance with the `pj_georef` database)
- **Run single test:** `cargo test <test_name>`
- **Run with Docker:** `docker compose up`

## Architecture

**Backend (Rust/Actix-web)** serves a REST API for three core entities:
- **Operadora** — toll operator companies
- **Pedagio** — toll booth/plaza locations (FK to operadora)
- **Tarifa** — toll rates (FK to pedagio and tipo_tarifa)

**Code layout:**
- `src/main.rs` — server setup, DB pool creation, route registration, CORS config
- `src/models.rs` + `src/models/*.rs` — structs with Serde derive and `From<Row>` implementations
- `src/utils/import.rs` — CSV bulk import using PostgreSQL `COPY` command
- `src/utils/files.rs` — file upload handling to `./tmp` directory
- `src/tests/*.rs` — integration tests per entity

**Database:** Direct SQL via `tokio_postgres` + `deadpool_postgres` pool (no ORM). Uses `sql_builder::quote` for value escaping. Schema defined in `init.sql`.

**API pattern:** All routes under `/api/`. Endpoints follow `create-*`, `get-*`, `update-*`, `importar-*` naming. Handlers return `HttpResponse` with JSON bodies. Error responses use `"erro"` key.

## Environment Variables

- `DB_HOST` (default: `localhost`)
- `HTTP_PORT` (default: `9999`)
- `POOL_SIZE` (default: `125`)

## CSV Import

Import endpoints accept file uploads, parse CSV headers dynamically, convert `;` delimiters to `,`, write to `./tmp` (mounted as `/uploaded` in the DB container), then use PostgreSQL `COPY` for bulk insert.

## Docker Services

- **api** — Rust backend (port 8080 internal)
- **db** — PostgreSQL 18 (port 5432)
- **nginx** — reverse proxy (port 9999 external)
- **angular** — frontend app

## Language

The codebase, API endpoints, database columns, and error messages are in Portuguese.

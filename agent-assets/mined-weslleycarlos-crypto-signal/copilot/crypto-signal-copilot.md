# Crypto Signal Platform - AI Agent Instructions

## Project Overview

This is a microservices-based simulated crypto trading platform using an event-driven architecture.

- **Stack**: Docker Compose, RabbitMQ (Messaging), Redis (Cache), PostgreSQL (Application Data), MongoDB (Logs/Audits).
- **Frontend**: Next.js (App Router).
- **Backend Services**: Python (Ingestion, Notification), Java (Analyzer), TypeScript (Wallet, BFF).

## Architecture & Data Flow

Understanding the event flow is critical for modifications:

1. **Ingestion Service** (Python) fetches prices -> Caches in **Redis** -> Publishes `price_updated` to **RabbitMQ**.
2. **Analyzer Service** (Java) consumes `price_updated` -> Evaluates against **PostgreSQL** rules -> Publishes `trade_signal_detected`.
3. **Wallet Service** (TypeScript) consumes `trade_signal_detected` -> Executes simulated trade in **PostgreSQL** -> Publishes `order_completed`.
4. **Notification Service** (Python) consumes `order_completed` -> Sends Email/Telegram.

**BFF Pattern**: The `bff` service (Express) aggregates data for the frontend by reading directly from Redis (prices) and databases, rather than proxying internal service APIs.

## Service-Specific Guidelines

### Ingestion Service (`ingestion-service/`)

- **Language**: Python.
- **Key Logic**: `PriceFetcher` uses a **Circuit Breaker** pattern (`utils/circuit_breaker.py`) to handle CoinGecko API limits.
- **Data**: Writes to Redis keys `price:<symbol>`.

### Analyzer Service (`analyzer-service/`)

- **Language**: Java 17, Spring Boot 3.2.6.
- **Persistence**: Spring Data JPA with PostgreSQL (`TradingRule` entity).
- **Configuration**: Properties in `application.properties`. RabbitMQ queues defined here.
- **Logic**: Rule evaluation happens in `RuleEngineService`.

### Wallet Service (`wallet-service/`)

- **Language**: TypeScript (Node.js).
- **Persistence**: TypeORM with PostgreSQL.
- **Entities**: `User`, `Wallet`, `Transaction`.
- **Concurrency**: Ensure database transactions handle balance updates atomically.

### BFF (`bff/`)

- **Language**: TypeScript (Express).
- **Pattern**: Direct DB/Cache access.
- **Routes**: `/api/prices` reads directly from Redis.

### Frontend (`frontend/`)

- **Framework**: Next.js 13+ (App Router).
- **Styling**: Tailwind CSS.

## Development Workflow

- **Run All**: `docker-compose up --build`.
- **Logs**: `docker-compose logs -f <service_name>`.
- **Restart Service**: `docker-compose restart <service_name>`.
- **Environment**: ALWAYS check `.env` exists (copy from `.env.example`).

## Critical Conventions

- **Event Schemas**: Strictly defined in `events-schema.json`. ALL event payloads MUST match these schemas.
- **Dead Letter Queues (DLQ)**: Failed message processing MUST route to `*_dlq` queues defined in `rabbitmq-init.sh`.
- **Port Mapping**:
  - Frontend: 3000
  - BFF: 8080
  - RabbitMQ UI: 15672
  - Redis: 6379
  - Postgres: 5432

## Common Tasks

- **Adding a new event**: Update `events-schema.json`, then implement publisher/consumer in relevant services.
- **Adding a new crypto**: Update `CRYPTOS` env var in `ingestion-service`.
- **Database Changes**: Use migrations (TypeORM for Wallet, Hibernate ddl-auto for Analyzer in dev).

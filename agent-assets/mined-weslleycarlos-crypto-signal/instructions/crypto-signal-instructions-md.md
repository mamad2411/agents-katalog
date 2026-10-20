---
applyTo: '**'
---

# Project Context

This project is a **simulated cryptocurrency trading platform** built using a **microservices architecture** and **event-driven communication**.

The system monitors cryptocurrency prices in near real time, evaluates user-defined investment rules, and executes **simulated buy orders** using a fictitious wallet balance.

⚠️ No real money, real exchanges, or real trading APIs are used.

---

## High-Level Architecture

The system is composed of **five independent services**, each with a single responsibility and isolated data ownership:

1. **Ingestion Service** – fetches and caches prices  
2. **Analyzer Service** – evaluates trading rules  
3. **Wallet / Execution Service** – manages balances and executes orders  
4. **Notification Service** – sends alerts  
5. **Frontend + BFF** – provides read-only dashboard for monitoring  

All internal communication between microservices **MUST be asynchronous via RabbitMQ**.  
Direct HTTP calls between core services are **NOT allowed** (except via API Gateway or BFF).

The **Frontend** communicates **only with the BFF** over HTTP. The **BFF aggregates data from core services' databases** but **does not write** to them and **does not interact with RabbitMQ**.

---

## Services Overview

### A. Ingestion Service (Collector)
**Responsibility**  
- Periodically fetch cryptocurrency prices from CoinGecko API  
- Cache prices in Redis to avoid rate limits  
- Publish `price_updated` events to RabbitMQ  

**Technology**  
- Language: Python (preferred) or Go  
- Libraries: `requests`, `pika`, `python-json-logger`  
- Cache: Redis  

**Key Requirements**  
- Handle API rate limiting  
- Implement caching with TTL  
- Circuit Breaker for external API resilience  
- Graceful shutdown on SIGINT/SIGTERM  

---

### B. Analyzer Service (Rules Engine)
**Responsibility**  
- Consume `price_updated` events  
- Evaluate user-defined trading rules stored in PostgreSQL  
- Emit `trade_signal_detected` events when conditions match  

**Technology**  
- Java with Spring Boot OR C# (.NET)  

**Key Requirements**  
- High-performance, stateless rule evaluation  
- Efficient rule indexing and lookup  
- Idempotent event consumption  
- Structured logging and error handling  

---

### C. Wallet / Execution Service
**Responsibility**  
- Manage fictitious user balances and transactions  
- Execute simulated buy orders with ACID guarantees  
- Publish `order_completed` events  

**Technology**  
- Node.js with TypeScript  
- ORM: TypeORM  
- Database: PostgreSQL  

**Key Requirements**  
- ACID-compliant transactions  
- Concurrency control (optimistic/pessimistic locking)  
- Idempotent order processing  
- Emit events only after successful commit  

---

### D. Notification Service
**Responsibility**  
- Consume `order_completed` events  
- Notify users via Telegram or Email  

**Technology**  
- Go or Python  

**Channels**  
- Telegram Bot  
- Email (SendGrid free tier)  

**Key Requirements**  
- Dead-letter queue handling for failed notifications  
- Manual acknowledgment of messages  
- Idempotent delivery  

---

### E. Frontend + BFF (Backend for Frontend)
**Responsibility**  
- Provide a **read-only dashboard** for system monitoring  
- **BFF**: Aggregates data from PostgreSQL, Redis, and MongoDB  
- **Frontend**: Displays current prices, active rules, recent events, and simulated wallet  

**Technology**  
- **BFF**: Node.js/Express or Python/FastAPI  
- **Frontend**: React or Next.js (static or SSR)  

**Key Requirements**  
- **No direct access to RabbitMQ**  
- **No writes to any database** – read-only queries only  
- **No authentication** – open dashboard for local/dev use  
- **HTTP-only communication** (no WebSockets)  
- BFF must query each service’s owned database directly (e.g., PostgreSQL for rules/wallet, Redis for latest prices, MongoDB for event history)  
- Must include Dockerfile and integrate into `docker-compose.yml`  

**Deliverables**  
- `/bff` directory with source code, Dockerfile, and package files  
- `/frontend` directory with React/Next.js app, Dockerfile  
- Updated `docker-compose.yml` exposing BFF on port `8080` and frontend on `3000`  
- README section explaining how to access the dashboard  

---

## Messaging & Events

**Message Broker**  
- RabbitMQ  

**Event Schema**  
- JSON format with fields: `event`, `version`, `correlationId`, `data`  
- Example:  
  ```json
  {
    "event": "price_updated",
    "version": "1.0",
    "correlationId": "abc-123-xyz",
    "data": { "symbol": "BTC", "price_usd": 43210.50, "timestamp": "2026-01-17T10:00:00Z" }
  }
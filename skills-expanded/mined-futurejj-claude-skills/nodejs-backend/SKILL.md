---
name: nodejs-backend
description: "Node.js backend development including Express/Fastify, streams, worker threads, clustering, error handling, and production patterns. Trigger when users build Node.js APIs, need help with Express/Fastify middleware, handle file uploads, implement streaming, or optimize Node.js performance."
---

# Node.js Backend

You are a Node.js backend expert focused on production-grade APIs and performance.

## Core Principles

- **Fastify over Express for new projects.** Fastify is faster, has built-in schema validation, and better TypeScript support.
- **Streams for large data.** Never load entire files into memory. Pipe streams.
- **Proper error handling.** Unhandled rejections crash the process. Use error middleware and process-level handlers.
- **Structured logging.** Use pino (not console.log). Include request IDs, timestamps, context.

## Anti-Patterns

- Callback hell — use async/await
- Blocking the event loop with CPU-intensive work — use worker threads
- Not handling process signals (SIGTERM/SIGINT) — connections hang on deploy
- Using `*` CORS in production — be explicit about allowed origins

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Express/Fastify patterns | `references/frameworks.md` | Routing, middleware, validation |
| Streams & performance | `references/streams.md` | File handling, backpressure, workers |
| Error handling | `references/error-handling.md` | Error middleware, graceful shutdown |

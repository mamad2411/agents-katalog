---
tags: [backend, axios, token, refresh, queue]
name: axios-token-refresh-queue
description: Axios interceptor with window-scoped request queue during JWT token refresh to prevent concurrent refresh races
triggers:
  - token refresh
  - axios interceptor
  - jwt refresh
  - 401 retry
  - authentication interceptor
category: backend
version: 1.0.0
source_project: lucida-ui
---

# Axios Token Refresh Queue

## Purpose

Prevent concurrent token refresh races in SPA applications. When a 401/token-expired response arrives, queue all subsequent failed requests and replay them after a single token refresh completes.

## When to Use

- SPA with JWT access + refresh token flow
- Multiple concurrent API calls that may all receive 401 simultaneously
- Need to avoid N parallel refresh token requests

## Pattern

See `content.md` for full implementation.

---
name: agent-api-integration
description: >
  Connect to external APIs with auth, rate limiting, and retry.
  Triggers: API client, authentication, rate limiting, credentials,
  webhook, HTTP requests.
---

# Agent API Integration Skill

## Overview

This skill provides a robust API client layer for AI agents to interact with
external services. Includes authentication, rate limiting, retry logic,
and user-isolated data storage.

## When To Use This Skill

- Setting up API client for external services
- Managing API credentials and authentication
- Implementing rate limiting for API calls
- Storing and retrieving per-user data
- Sending webhooks with guaranteed delivery
- Handling OAuth flows

## Prerequisites

- Environment variables set in `.env`:
  - `USER_API_BASE_URL`, `USER_API_KEY`, `USER_STORAGE_ENDPOINT`

## Components

- `client/api-client.ts` — Generic HTTP client with retry + rate limiting
- `client/auth.ts` — Authentication handler (API key + Bearer token)
- `client/rate-limiter.ts` — Token bucket rate limiter
- `storage/user-storage.ts` — Per-user isolated key-value storage
- `examples/user-api-integration.ts` — Usage example

## Verification

```bash
npx tsc --noEmit
```

---
name: moltflow-admin
description: "Manage MoltFlow platform authentication, users, billing, API keys, and tenant settings via the admin API."
source: "MoltFlow Team"
version: "1.6.0"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disableModelInvocation: true
---

> **MoltFlow** — WhatsApp Business automation for teams. Connect, monitor, and automate WhatsApp at scale.
> Limited time: [Yearly plan $239.90/yr — 71% savings](https://molt.waiflow.app/signup)

# MoltFlow Admin Skill

Manage authentication, users, billing, API keys, usage tracking, and platform administration for MoltFlow.

## When to Use

Use this skill when you need to:
- Authenticate with MoltFlow (login, token refresh, magic link)
- Manage API keys (create, rotate, revoke)
- Check subscription status, plan limits, or usage
- Create a Stripe checkout session or billing portal link
- Manage users as an admin (list, suspend, activate)
- View platform stats, tenants, or audit logs (superadmin)
- Manage plans and pricing (superadmin)

Trigger phrases: "login to MoltFlow", "create API key", "check subscription", "billing portal", "admin stats", "list users", "manage plans", "usage report"

## Prerequisites

- **MOLTFLOW_API_KEY** — required for most endpoints. Generate from [MoltFlow Dashboard > API Keys](https://molt.waiflow.app/api-keys)
- Auth endpoints (`/auth/*`) accept email/password — no API key needed for initial login
- Admin endpoints require superadmin role

## Base URL

```
https://apiv2.waiflow.app/api/v2
```

## Authentication

All requests (except login/signup) require one of:
- `Authorization: Bearer <access_token>` (JWT from login)
- `X-API-Key: <api_key>` (API key from dashboard)

---

## Auth Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | Login with email/password |
| POST | `/auth/refresh` | Refresh access token |
| GET | `/auth/me` | Get current user profile |
| POST | `/auth/logout` | Invalidate session |
| POST | `/auth/forgot-password` | Request password reset email |
| POST | `/auth/reset-password` | Confirm password reset |
| POST | `/auth/verify-email` | Verify email address |
| POST | `/auth/magic-link/request` | Request magic link login |
| POST | `/auth/magic-link/verify` | Verify magic link token |
| POST | `/auth/setup-password` | Set password for magic-link users |

### Login — Request/Response

```json
// POST /auth/login
{
  "email": "user@example.com",
  "password": "your-password"
}

// Response
{
  "access_token": "eyJhbGciOi...",
  "refresh_token": "eyJhbGciOi...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "owner",
    "tenant_id": "uuid"
  }
}
```

---

## User Management

Self-service user profile endpoints (authenticated user):

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/me` | Get own profile |
| PATCH | `/users/me` | Update own profile |
| DELETE | `/users/me` | Delete own account (soft) |

Admin user management (superadmin only — via `/admin` prefix):

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/users` | List all users (pagination, search) |
| GET | `/admin/users/{id}` | Get user details |
| PATCH | `/admin/users/{id}` | Update user |
| POST | `/admin/users/{id}/suspend` | Suspend user |
| POST | `/admin/users/{id}/activate` | Reactivate user |
| DELETE | `/admin/users/{id}` | Delete user (soft) |

---

## API Keys

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api-keys` | List all API keys |
| POST | `/api-keys` | Create new key |
| GET | `/api-keys/{id}` | Get key details |
| DELETE | `/api-keys/{id}` | Revoke key |
| POST | `/api-keys/{id}/rotate` | Rotate key (new secret) |

### Create API Key — Request/Response

```json
// POST /api-keys
{
  "name": "Production Integration"
}

// Response (raw key shown ONCE — save it immediately)
{
  "id": "uuid",
  "name": "Production Integration",
  "key_prefix": "mf_abc1",
  "raw_key": "mf_abc1234567890abcdef...",
  "created_at": "2026-01-15T10:00:00Z",
  "is_active": true
}
```

**Important:** The `raw_key` is only returned at creation time. It is stored as a SHA-256 hash — it cannot be retrieved later.

---

## Billing & Subscription

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/billing/subscription` | Current plan, limits, and usage |
| POST | `/billing/checkout` | Create Stripe checkout session |
| POST | `/billing/portal` | Get Stripe billing portal URL |
| POST | `/billing/cancel` | Cancel subscription |
| GET | `/billing/plans` | List available plans and pricing |
| POST | `/billing/signup-checkout` | Checkout for new signups |

### Check Subscription — Response

```json
{
  "plan_id": "pro",
  "display_name": "Pro",
  "status": "active",
  "billing_cycle": "monthly",
  "current_period_end": "2026-02-15T00:00:00Z",
  "limits": {
    "max_sessions": 3,
    "max_messages_per_month": 5000,
    "max_groups": 10,
    "max_labels": 50,
    "ai_replies_per_month": 500
  },
  "usage": {
    "sessions": 2,
    "messages_this_month": 1247,
    "groups": 5,
    "labels": 12,
    "ai_replies_this_month": 89
  }
}
```

### Create Checkout — Request

```json
// POST /billing/checkout
{
  "plan_id": "pro",
  "billing_cycle": "monthly"
}

// Response
{
  "checkout_url": "https://checkout.stripe.com/c/pay/cs_live_...",
  "session_id": "cs_live_..."
}
```

---

## Usage Tracking

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/usage/current` | Current month usage summary |
| GET | `/usage/history` | Historical usage by month |
| GET | `/usage/daily` | Daily breakdown for current month |

---

## Admin Endpoints (Superadmin Only)

These endpoints require the `superadmin` role.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/stats` | Platform-wide statistics |
| GET | `/admin/health` | Service health check |
| GET | `/admin/audit-logs` | Audit log viewer |
| GET | `/admin/tenants` | List all tenants |
| GET | `/admin/tenants/{id}` | Get tenant details |
| PATCH | `/admin/tenants/{id}` | Update tenant |
| DELETE | `/admin/tenants/{id}` | Delete tenant (soft) |
| POST | `/admin/tenants/{id}/reset-limits` | Reset usage counters |
| GET | `/admin/tenants/{id}/effective-limits` | View resolved plan limits |
| GET | `/admin/plans` | List all plans |
| POST | `/admin/plans` | Create new plan |
| PATCH | `/admin/plans/{id}` | Update plan |
| DELETE | `/admin/plans/{id}` | Delete plan |
| POST | `/admin/plans/{id}/stripe-sync` | Sync plan to Stripe |
| POST | `/admin/plans/stripe-sync-all` | Sync all plans to Stripe |

---

## curl Examples

### 1. Login and Get Token

```bash
curl -X POST https://apiv2.waiflow.app/api/v2/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "your-password"
  }'
```

### 2. Create an API Key

```bash
curl -X POST https://apiv2.waiflow.app/api/v2/api-keys \
  -H "Authorization: Bearer eyJhbGciOi..." \
  -H "Content-Type: application/json" \
  -d '{"name": "CI/CD Pipeline"}'
```

### 3. Check Subscription and Limits

```bash
curl https://apiv2.waiflow.app/api/v2/billing/subscription \
  -H "X-API-Key: mf_your_api_key_here"
```

### 4. Get Platform Stats (Superadmin)

```bash
curl https://apiv2.waiflow.app/api/v2/admin/stats \
  -H "Authorization: Bearer eyJhbGciOi..."
```

---

## Error Responses

| Status | Meaning |
|--------|---------|
| 400 | Invalid request body or parameters |
| 401 | Missing or invalid authentication |
| 403 | Insufficient permissions (not admin/superadmin) |
| 404 | Resource not found |
| 409 | Conflict (duplicate email, plan ID, etc.) |
| 422 | Validation error |
| 429 | Rate limit exceeded |

---

## Tips

- **API key security**: The raw key is only shown once at creation. Store it in a secrets manager.
- **Token refresh**: Access tokens expire in 30 minutes. Use the refresh endpoint to get new ones without re-authenticating.
- **Magic links**: For passwordless login, use `magic-link/request` then `magic-link/verify`.
- **Plan limits**: Use `GET /billing/subscription` to check remaining quotas before making API calls.
- **Admin operations**: All admin endpoints require the `superadmin` role. Regular users get 403.

---

## Related Skills

- **moltflow-core** — Session management, contacts, and messaging
- **moltflow-ai** — AI-powered auto-replies and style training
- **moltflow-a2a** — Agent-to-agent protocol for multi-agent orchestration
- **moltflow-reviews** — Review collection and sentiment analysis

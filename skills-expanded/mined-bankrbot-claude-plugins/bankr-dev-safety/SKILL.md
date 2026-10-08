---
name: Bankr Dev - Safety & Access Control
description: This skill should be used when building secure Bankr integrations, implementing API key management, configuring access controls, setting up dedicated agent wallets, or handling rate limits and security best practices in Bankr API projects.
version: 1.0.0
---

# Safety & Access Control

Security patterns and best practices for Bankr API integrations.

## API Key Capability Flags

Each API key has independent toggles managed at [bankr.bot/api](https://bankr.bot/api):

| Flag | Controls | Default |
|------|----------|---------|
| `agentApiEnabled` | `/agent/*` endpoints | false |
| `llmGatewayEnabled` | LLM Gateway at `llm.bankr.bot` | false |
| `readOnly` | Restricts agent to read-only tools | false |

### Separate Agent & LLM Keys

| Config | Agent API Key | LLM Gateway Key |
|--------|--------------|-----------------|
| Env var | `BANKR_API_KEY` | `BANKR_LLM_KEY` (falls back to API key) |
| CLI config | `apiKey` | `llmKey` (falls back to `apiKey`) |

## Read-Only Keys

When `readOnly: true`:
- `/agent/prompt` works but only read tools are available
- `/agent/sign` returns 403
- `/agent/submit` returns 403

```typescript
// Handle read-only 403 errors
const response = await fetch(`${API_URL}/agent/sign`, { ... });
if (response.status === 403) {
  const error = await response.json();
  // error.message: "This API key has read-only access..."
}
```

## IP Whitelisting

```typescript
// Requests from non-whitelisted IPs get 403
// Configure allowedIps at bankr.bot/api
const response = await fetch(`${API_URL}/agent/prompt`, { ... });
if (response.status === 403) {
  const error = await response.json();
  // error.message: "IP address not allowed for this API key"
}
```

## Dedicated Agent Wallet

For autonomous agents, create a separate Bankr account:

1. Sign up at [bankr.bot/api](https://bankr.bot/api) with a different email
2. Generate an API key with Agent API enabled
3. Configure access controls (readOnly, allowedIps)
4. Fund with limited amounts

### Access Control Combinations

| Use Case | readOnly | allowedIps | Funding |
|----------|----------|------------|---------|
| Monitoring bot | Yes | Yes (server IP) | None |
| Trading bot (server) | No | Yes (server IP) | Limited |
| Development/testing | No | No | Minimal |
| Research agent | Yes | No | None |

## Rate Limits

| Tier | Daily Limit |
|------|-------------|
| Standard | 100 messages/day |
| Bankr Club | 1,000 messages/day |
| Custom | Set per API key |

```typescript
// Handle 429 rate limit responses
const response = await fetch(`${API_URL}/agent/prompt`, { ... });
if (response.status === 429) {
  const error = await response.json();
  // error.resetAt: Unix timestamp when counter resets
  // error.limit: Daily limit
  // error.used: Messages used
  const retryAfter = error.resetAt - Date.now();
}
```

## Key Management Patterns

```typescript
// Always use environment variables
const API_KEY = process.env.BANKR_API_KEY;
const LLM_KEY = process.env.BANKR_LLM_KEY || API_KEY;

if (!API_KEY) {
  throw new Error("BANKR_API_KEY not set. Get one at https://bankr.bot/api");
}
```

**Storage rules:**
- Environment variables for server-side agents and CI/CD
- `~/.bankr/config.json` for local development (CLI manages this)
- Never commit keys to source control
- Add `~/.bankr/`, `.env` to `.gitignore`
- Rotate periodically, revoke immediately if compromised

## Transaction Safety

- `/agent/submit` executes immediately with **no confirmation prompt**
- Always use `waitForConfirmation: true` for important transactions
- Test with small amounts on Base/Polygon first
- Verify calldata source for arbitrary transactions

## Related Skills

- `bankr-client-patterns` - Client setup with error handling
- `bankr-api-basics` - API fundamentals
- `bankr-sign-submit-api` - Sync endpoints that need extra caution

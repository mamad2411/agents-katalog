---
name: chanjing-auth
description: Chanjing platform OAuth authentication and credential management. Use when checking auth status, handling login flow, managing access tokens, or troubleshooting credential issues. Shared by chanjing-digital-human and other Chanjing-integrated features.
---

# Chanjing OAuth Authentication

Centralized authentication management for all Chanjing platform features (digital humans, TTS, background music, sound effects).

## When To Use

- Check if user is authenticated with Chanjing platform
- Guide user through OAuth login flow
- Troubleshoot credential or token issues
- Set up authentication for CI/CD or headless environments

**Do NOT use for:** Actual API calls to Chanjing services → delegate to feature-specific skills (`chanjing-digital-human`, etc.)

---

## Quick Start

```bash
# Check current auth status
npx framevideo auth status

# Check if authenticated (exit code)
npx framevideo auth status --check

# Get status as JSON
npx framevideo auth status --json
```

If not authenticated, use one of the authentication methods below.

---

## Core Concepts

### OAuth CLI Web Login

The standard authentication flow:

1. User runs `framevideo auth login` or clicks login in Studio
2. CLI opens browser to Chanjing authorization page
3. User approves in browser
4. Browser redirects to local callback server
5. CLI receives token and saves to credential store
6. All Chanjing features can now access the platform

### Credential Storage

Tokens are stored in `~/.chanjing/credentials` (respects `CHANJING_CONFIG_DIR` env var) in an `oauth` block:

```json
{
  "oauth": {
    "access_token": "...",
    "refresh_token": "...",
    "expires_at": 1234567890
  }
}
```

**Never read, print, log, or commit these tokens.** Use the shared auth store APIs in `packages/cli/src/auth/store.ts`.

### Plugin API Client

All Chanjing API requests use `Authorization: Bearer <access_token>` header. The client handles:
- Token refresh when expired
- Automatic retry on 401
- Error reporting

Located at: `packages/cli/src/tts/chanjingOpenapi.ts`

---

## Authentication Methods

### Method 1: Interactive Login (Recommended)

For development and local use:

```bash
npx framevideo auth login
```

Opens browser for OAuth flow. Requires user interaction.

### Method 2: Studio Login (Agent-Friendly)

When working with an agent and OAuth is missing:

1. Start or reuse preview server: `npx framevideo preview`
2. Open Studio project URL in browser
3. Navigate to Digital Human, Voice, or account panel
4. Click login button to start OAuth flow
5. Complete browser authorization
6. Verify with `npx framevideo auth status`

**Why this is better than CLI-only guidance:**
- Visual feedback for user
- Integrated into natural workflow
- Agent can poll status endpoint

### Method 3: CI/CD or Headless

For automated environments without browser:

1. Obtain refresh token from an interactive login session
2. Set `CHANJING_REFRESH_TOKEN` environment variable
3. CLI will use refresh token to obtain access tokens

**Security note:** Treat refresh tokens as secrets. Use secure secret management (GitHub Secrets, CI vault, etc.)

---

## Missing Credentials UX

When an agent-authored workflow needs Chanjing features but auth is missing:

### If preview is available (preferred):

1. Start or reuse `npx framevideo preview`
2. Open Studio project URL in in-app browser
3. Navigate to panel requiring Chanjing (Digital Human, Voice, account)
4. Click login to start OAuth CLI Web Login
5. User completes browser authorization
6. Re-check auth status, then continue workflow

### If preview is unavailable:

Fall back to CLI-only guidance:

```bash
npx framevideo auth login
```

Then continue workflow.

### What NOT to do:

- ❌ Stop at env var guidance if preview is available
- ❌ Print or save tokens outside credential store
- ❌ Ask user to manually edit `~/.chanjing/credentials`
- ❌ Use deprecated `app_id`, `secret_key`, or `CHANJING_OPENAPI_ACCESS_TOKEN`

---

## Studio Integration

Studio provides auth status and login UI via plugin routes.

### Auth Status Endpoint

```bash
GET /api/projects/:id/chanjing/auth/status
```

Returns:
```json
{
  "authenticated": true,
  "user": {
    "id": "...",
    "name": "..."
  }
}
```

Use this to poll auth state after guiding user to Studio login.

### Login Button

Available in:
- Digital Human panel (Studio → Digital Human → Login)
- Voice panel (Studio → Voice → Login)  
- Account settings (Studio → Settings → Chanjing Account)

Clicking any login button triggers the same OAuth CLI Web Login flow.

---

## Troubleshooting

### "Not authenticated" error

**Check:**
```bash
npx framevideo auth status
```

**Fix:**
```bash
npx framevideo auth login
```

### Token expired

The client auto-refreshes tokens. If refresh fails:

```bash
# Clear credentials and re-login
rm ~/.chanjing/credentials
npx framevideo auth login
```

### "Invalid token" or 401 errors

Credential store may be corrupted:

```bash
# Inspect (redacted output)
npx framevideo auth status --json

# Clear and re-login
rm ~/.chanjing/credentials
npx framevideo auth login
```

### CI/CD auth fails

1. Verify `CHANJING_REFRESH_TOKEN` is set
2. Check token hasn't expired (refresh tokens typically valid 30-90 days)
3. Obtain fresh refresh token from interactive session

---

## Integration with Other Skills

### chanjing-digital-human

Uses this auth for:
- Listing digital humans and voices
- Submitting website-project synthesis
- Polling task status
- Downloading generated videos

### chanjing-media (planned)

Uses this auth for:
- Background music list and download
- Sound effects list and download

### framevideo-media

**Does NOT use this auth.** Local Kokoro TTS is offline and credential-free.

---

## Security Best Practices

1. **Never print tokens** - Not in logs, not in error messages, not in agent responses
2. **Use credential store APIs** - Don't read `~/.chanjing/credentials` directly
3. **No tokens in Git** - Add credential files to `.gitignore`
4. **Secure CI secrets** - Use secret management for `CHANJING_REFRESH_TOKEN`
5. **Don't copy standalone scripts** - Reuse shared auth client, don't duplicate

---

## Validation

After authentication:

```bash
# Should show "authenticated: true"
npx framevideo auth status

# Should list available resources
npx framevideo chanjing music categories --json
```

If both succeed, authentication is working correctly.

---

## References

- Auth store implementation: `packages/cli/src/auth/store.ts`
- Plugin API client: `packages/cli/src/tts/chanjingOpenapi.ts`
- Studio auth routes: See `chanjing-digital-human` skill, `references/studio-routes.md`

---
name: oauth-callback-diagnostic
description: "Diagnose OAuth callback URL mismatches for desktop and web apps authenticating to third-party services. Use when a user reports redirect_uri errors, callback URL mismatches, or OAuth flow failures involving external providers (GitHub, Google, Azure AD, etc.). Triggers on: redirect_uri error, callback URL mismatch, OAuth callback not associated, OAuth redirect failed, authorization callback URL."
---

# OAuth Callback URL Diagnostic

> **Load this skill when:** A user reports OAuth authentication failures involving callback/redirect URL mismatches — for any combination of app type (desktop, web) and OAuth provider (GitHub, Google, Azure AD, Auth0, etc.).

---

## Pattern Recognition

This skill applies when Builder encounters any of these error patterns:

| Error Signal | Provider Example |
|---|---|
| "redirect_uri is not associated with this application" | GitHub |
| "redirect_uri_mismatch" | Google |
| "The redirect URI in the request does not match the redirect URIs configured" | Azure AD |
| "Invalid redirect_uri" | Auth0, Generic |
| "The redirect_uri MUST match the registered callback URL" | Generic OIDC |
| User says "OAuth callback not working" or "redirect URL error" | Any |

---

## Diagnostic Workflow

### Step 1: Identify the OAuth Configuration

Read the project's OAuth configuration to determine:

1. **OAuth provider:** Which third-party service? (GitHub, Google, Azure AD, Auth0, etc.)
2. **Client ID source:** Where is the client ID stored? (`.env.local`, Supabase secrets, environment variables)
3. **Callback URL source:** Where does the app define the callback URL it sends in the OAuth request?
4. **Registered URL location:** Where is the callback URL registered with the provider?

**Common configuration sources:**

| Source | How to Read |
|---|---|
| `.env.local` / `.env` | `grep -i "oauth\|client_id\|redirect\|callback" .env.local` |
| Supabase secrets | `supabase secrets list` (digests only — read actual values from `.env.local`) |
| Edge function / API handler | Search for `redirect_uri`, `callback_url`, or OAuth initiation logic |
| `project.json` | Check `integrations`, `authentication`, or `oauth` sections |

### Step 2: Determine the Callback URL Being Sent

Trace the actual callback URL the app sends in the OAuth authorization request:

```
Look for:
- redirect_uri parameter in OAuth initiate function
- OAUTH_CALLBACK_URL / REDIRECT_URI environment variable
- Hardcoded callback URLs in auth handlers
- Supabase auth callback configuration
```

**Desktop-specific considerations:**
- Desktop apps can't use `localhost` callbacks in production (no web server)
- Electron/Tauri apps often use custom protocols (`myapp://callback`) or Supabase edge functions as intermediaries
- The callback URL is often a Supabase function URL, not the app itself

### Step 3: Determine the Expected Registered URL

Based on the provider, identify where the callback URL must be registered:

| Provider | Registration Location | API Access |
|---|---|---|
| GitHub | Settings → Developer settings → OAuth Apps → [app] | ❌ Read-only via API (cannot update callback URL) |
| Google | Google Cloud Console → APIs & Services → Credentials | ❌ No API for callback URLs |
| Azure AD | Azure Portal → App registrations → [app] → Authentication | ✅ Microsoft Graph API can update |
| Auth0 | Auth0 Dashboard → Applications → [app] → Settings | ✅ Auth0 Management API |
| Supabase | Supabase Dashboard → Authentication → URL Configuration | ✅ Supabase Management API |
| Generic OIDC | Provider-specific admin panel | Varies |

### Step 4: Present Diagnostic Dashboard

```
═══════════════════════════════════════════════════════════════════════
              OAUTH CALLBACK URL MISMATCH DIAGNOSTIC
═══════════════════════════════════════════════════════════════════════

Provider:        {provider_name}
Client ID:       {client_id}

📤 CALLBACK URL BEING SENT
───────────────────────────────────────────────────────────────────────
  {actual_callback_url}
  Source: {source_file}:{line_number}

📋 REGISTERED CALLBACK URL(S)
───────────────────────────────────────────────────────────────────────
  {known_registered_url or "Cannot read via API — check provider dashboard"}

🔍 MISMATCH
───────────────────────────────────────────────────────────────────────
  The callback URL being sent does not match what's registered
  with {provider_name}.

  Common causes:
  - Environment switched (dev → staging → prod) but OAuth app not updated
  - Supabase project URL changed
  - Custom domain added but OAuth app still has old URL
  - Multiple OAuth apps and wrong client ID is configured

🔧 FIX
───────────────────────────────────────────────────────────────────────
{fix_instructions — see Step 5}

═══════════════════════════════════════════════════════════════════════
```

### Step 5: Generate Fix Instructions

**If the provider supports API updates (Azure AD, Auth0, Supabase):**

```
  [F] Fix automatically via API
  [O] Open provider dashboard in browser
  [S] Skip — I'll fix this manually later
```

If user chooses [F]:
- Use the provider's management API to add the correct callback URL
- Verify the change was applied
- Offer to re-test the OAuth flow

**If the provider does NOT support API updates (GitHub, Google):**

```
  [O] Open {provider_name} settings in browser
  [S] Skip — I'll fix this manually later
```

If user chooses [O]:
- Open the provider's OAuth app settings page in the default browser
- Provide step-by-step instructions for what to update:

```
  Steps to fix in {provider_name}:
  1. Find the OAuth App with Client ID: {client_id}
  2. Add this callback URL:
     {actual_callback_url}
  3. Save changes

  After updating, type "done" and I'll re-test the OAuth flow.
```

### Step 6: Re-Test After Fix

When the user confirms the fix:

1. Attempt the OAuth flow again (via Playwright or manual trigger)
2. Verify the redirect succeeds
3. If still failing, re-run diagnostic with fresh data

---

## Desktop App Specifics

Desktop apps (Electron, Tauri) have unique OAuth challenges:

### Protocol Handlers vs Server Callbacks

| Approach | How It Works | Callback URL Pattern |
|---|---|---|
| **Custom protocol** | App registers `myapp://` handler, OAuth redirects to `myapp://callback` | `myapp://callback?code=...` |
| **Localhost server** | App starts temporary HTTP server | `http://localhost:{port}/callback` |
| **Edge function intermediary** | OAuth redirects to cloud function, which signals the app | `https://project.supabase.co/functions/v1/oauth-callback` |
| **System browser + deeplink** | OAuth completes in browser, deeplink returns to app | OS-specific |

### Common Desktop OAuth Pitfalls

1. **Port conflicts:** Localhost callback with dynamic port — registered URL has wrong port
2. **Custom protocol not registered:** OS doesn't know about `myapp://` protocol
3. **Edge function URL mismatch:** Supabase project URL changed or environment switched
4. **CORS on callback:** Browser-based OAuth redirects blocked by CORS (not applicable to desktop protocol handlers)

---

## Environment-Aware Diagnosis

Read `project.json` to determine the current environment:

```json
"environments": {
  "staging": {
    "desktop": {
      "appName": "My App Preview",
      "loadsFrom": "..."
    }
  },
  "production": {
    "desktop": {
      "appName": "My App",
      "loadsFrom": "..."
    }
  }
}
```

The callback URL often differs per environment:
- **Dev:** `http://localhost:54321/functions/v1/oauth-callback`
- **Staging:** `https://staging-project.supabase.co/functions/v1/oauth-callback`
- **Production:** `https://prod-project.supabase.co/functions/v1/oauth-callback`

Confirm the user is testing in the expected environment before diagnosing.

---

## Integration with Analysis Gate

When this diagnostic runs during ad-hoc mode analysis:
- The OAuth mismatch should be surfaced in the ANALYSIS COMPLETE dashboard
- If the fix requires user action (web UI update), Builder should NOT auto-proceed
- The diagnostic result should be included in the probe evidence

---

## Quick Reference

**Minimum viable diagnostic:**
1. Read `.env.local` for client ID
2. Search codebase for `redirect_uri` or `callback_url` to find what's being sent
3. Present the mismatch with "Open provider settings" option
4. Wait for user to fix, then re-test

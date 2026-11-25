---
name: streamdeck-oauth
description: 'OAuth 2.0 (authorization code + PKCE) for Stream Deck plugins: launching auth via streamDeck.system.openUrl, receiving the callback via deep-linking (streamdeck://plugins/message/<UUID>/<path>), the Elgato OAuth2 redirect proxy (https://oauth2-redirect.elgato.com/streamdeck/plugins/message/<UUID>/<path>) for providers that reject custom schemes, validating `state`, exchanging `code` for tokens in the plugin backend, storing access + refresh tokens in global settings, refresh-token rotation, sign-out, end-to-end TypeScript reference. USE FOR: connecting a Stream Deck plugin to Spotify/Twitch/YouTube/Hue/Google/Microsoft/GitHub or any OAuth2 provider, "sign in with X" button in property inspector, OAuth callback handling, deep link OAuth, oauth2-redirect.elgato.com proxy URL, PKCE, refresh token rotation, secure token storage in Stream Deck plugins.'
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["streamdeck", "elgato", "oauth2", "pkce", "authentication", "deep-linking"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/streamdeck", "emoji": "🎛️" } }
---

# Stream Deck Plugin — OAuth 2.0 Authentication

> **Prerequisites:**
> - `streamdeck-general` (runtime architecture)
> - `streamdeck-property-inspector` (you'll add a "Sign in" button to a PI
>   and read tokens from global settings)
> - `streamdeck-system-devices` (this skill uses `streamDeck.system.openUrl`
>   and `streamDeck.system.onDidReceiveDeepLink` from that namespace)

## Purpose

You need to authenticate the user with a third-party service (Spotify,
Twitch, YouTube, Philips Hue, Google, Microsoft, GitHub, …) to call its
API from your Stream Deck plugin. This skill is the **end-to-end OAuth 2.0
authorization-code flow** for Stream Deck plugins:

1. Launch the provider's authorize URL in the user's default browser.
2. Receive the callback via Elgato's deep-link mechanism.
3. Exchange the `code` for an access + refresh token (server-side, with PKCE).
4. Persist the tokens securely in **global settings**.
5. Refresh tokens before they expire.
6. Sign out cleanly.

There is **no dedicated "OAuth guide" page** in the Stream Deck SDK
docs — the official pattern is documented in the Deep-Linking guide's
"OAuth2 Redirect Proxy" section. This skill consolidates it with the
matching settings, system, and PI pieces.

## Architecture

```
┌──────────┐                  ┌──────────────┐                ┌────────────────┐
│ Plugin   │ system.openUrl   │ User's       │ user signs in  │ Auth provider  │
│ (Node.js)├─────────────────▶│ browser      ├───────────────▶│ (Spotify, ...) │
└─────┬────┘                  └──────────────┘                └───────┬────────┘
      │                                                               │
      │                                                       provider redirects
      │                                                       to callback URL
      │                                                               │
      │                                  ┌────────────────────────────▼─────────┐
      │                                  │ oauth2-redirect.elgato.com           │
      │                                  │ (Elgato's stateless forwarder)       │
      │                                  └──────────────────┬───────────────────┘
      │                                                     │ forwards via
      │                                                     │ streamdeck://...
      │                                                     ▼
      │                                  ┌────────────────────────────────────┐
      │ onDidReceiveDeepLink             │ Stream Deck app (URL scheme handler)│
      │◄─────────────────────────────────┤                                    │
      │ (ev.url.path, ev.url.searchParams)│                                    │
      │                                  └────────────────────────────────────┘
      │
      │ POST /token { code, code_verifier }
      ▼
┌──────────────┐
│ Auth provider│ ─── access_token, refresh_token, expires_in ──▶ plugin
└──────────────┘                                                       │
                                                                       ▼
                                                ┌──────────────────────────────┐
                                                │ streamDeck.settings.setGlobalSettings
                                                │ ({ accessToken, refreshToken,
                                                │    expiresAt })
                                                └──────────────────────────────┘
```

Two callback-URL options — pick based on the provider:

| Callback style | URL format | When to use |
|---|---|---|
| **Elgato OAuth2 proxy** (recommended) | `https://oauth2-redirect.elgato.com/streamdeck/plugins/message/<PLUGIN_UUID>/<path>` | Default. Works with every OAuth provider including ones that reject custom URI schemes (Google, Microsoft, Spotify, ...). Stateless — Elgato stores nothing. Only forwards these params: `code`, `state`, `scope`, `error`. |
| **Direct custom scheme** | `streamdeck://plugins/message/<PLUGIN_UUID>/<path>` | When the provider explicitly allows custom URI schemes AND the user has Stream Deck app v6.5+. Slightly faster. |

> ⚠️ Almost every major provider (Google, Microsoft, Spotify, Twitch,
> Slack) requires `https://` callback URLs. **Default to the proxy.**

---

## 1. Register your plugin with the provider

In the provider's developer console (Spotify Developer Dashboard, Google
Cloud Console, Twitch dev portal, etc.), create an app and configure:

| Field | Value |
|---|---|
| Application name | Your plugin's display name |
| Redirect URI / Callback URL | `https://oauth2-redirect.elgato.com/streamdeck/plugins/message/<PLUGIN_UUID>/oauth/callback` |
| Scopes | Whatever your plugin needs (the minimum) |

Most providers issue:

- A **Client ID** (public — fine to ship in your plugin).
- A **Client Secret** (treat as semi-public — see the "Client secret"
  section below).

For public/native clients (which a Stream Deck plugin is), **prefer
PKCE** so the client secret isn't required.

> The `<path>` after `/<PLUGIN_UUID>/` is yours — pick something
> descriptive like `oauth/callback`. It comes back as `ev.url.path` on
> the deep-link side.

---

## 2. The plugin-side: kick off the flow

```ts
// src/auth/oauth.ts
import streamDeck from "@elgato/streamdeck";
import crypto from "node:crypto";

const PLUGIN_UUID  = "com.yourhandle.spotify";          // your plugin UUID
const PROVIDER     = {
  authorizeUrl: "https://accounts.spotify.com/authorize",
  tokenUrl:     "https://accounts.spotify.com/api/token",
  clientId:     "YOUR_CLIENT_ID",
  scopes:       ["user-read-playback-state", "user-modify-playback-state"],
};
const REDIRECT_URI =
  `https://oauth2-redirect.elgato.com/streamdeck/plugins/message/${PLUGIN_UUID}/oauth/callback`;

// In-memory map of in-flight auth attempts keyed by `state`
const pending = new Map<string, { codeVerifier: string; createdAt: number }>();

function base64url(buf: Buffer): string {
  return buf.toString("base64").replace(/=/g, "").replace(/\+/g, "-").replace(/\//g, "_");
}

export async function startSignIn(): Promise<void> {
  // PKCE: code_verifier is 43–128 chars of [A-Za-z0-9-._~]
  const codeVerifier  = base64url(crypto.randomBytes(64));
  const codeChallenge = base64url(crypto.createHash("sha256").update(codeVerifier).digest());

  // `state` is a CSRF token — must be unguessable AND verified on callback
  const state = base64url(crypto.randomBytes(32));
  pending.set(state, { codeVerifier, createdAt: Date.now() });

  // Garbage-collect stale attempts (>10 minutes)
  for (const [k, v] of pending) if (Date.now() - v.createdAt > 10 * 60_000) pending.delete(k);

  const url = new URL(PROVIDER.authorizeUrl);
  url.searchParams.set("response_type",         "code");
  url.searchParams.set("client_id",             PROVIDER.clientId);
  url.searchParams.set("redirect_uri",          REDIRECT_URI);
  url.searchParams.set("scope",                 PROVIDER.scopes.join(" "));
  url.searchParams.set("state",                 state);
  url.searchParams.set("code_challenge",        codeChallenge);
  url.searchParams.set("code_challenge_method", "S256");

  streamDeck.logger.info("Opening browser for OAuth", { state });
  await streamDeck.system.openUrl(url.toString());
}
```

Trigger this from a PI button click that messages the plugin:

```html
<!-- ui/sign-in.html -->
<sdpi-item label="Account">
  <sdpi-button id="signin">Sign in to Spotify</sdpi-button>
</sdpi-item>

<script src="sdpi-components.js"></script>
<script>
  const { streamDeckClient } = SDPIComponents;
  document.getElementById("signin").addEventListener("click", () => {
    streamDeckClient.send({ event: "signIn" });
  });
</script>
```

```ts
override async onSendToPlugin(ev: SendToPluginEvent<{ event: string }, unknown>) {
  if (ev.payload.event === "signIn") await startSignIn();
}
```

---

## 3. Handle the deep-link callback

Register **once at plugin startup**:

```ts
// src/plugin.ts
import streamDeck from "@elgato/streamdeck";
import { handleOAuthCallback } from "./auth/oauth";
import { MyAction } from "./actions/my-action";

streamDeck.system.onDidReceiveDeepLink((ev) => {
  // ev.url is a parsed URL with path, searchParams, etc.
  if (ev.url.path === "/oauth/callback") {
    void handleOAuthCallback(ev.url.searchParams);
  }
});

streamDeck.actions.registerAction(new MyAction());
streamDeck.connect();
```

The deep link arrives as `streamdeck://plugins/message/<UUID>/oauth/callback?code=...&state=...`,
parsed via the standard URL API. The path is `/oauth/callback`,
searchParams give you `code`, `state`, `scope`, `error`.

### The handler — validate `state`, exchange `code`, persist tokens

```ts
// src/auth/oauth.ts (continued)
type GlobalSettings = {
  accessToken?:  string;
  refreshToken?: string;
  expiresAt?:    number;       // epoch ms
  scope?:        string;
};

export async function handleOAuthCallback(params: URLSearchParams): Promise<void> {
  const error = params.get("error");
  if (error) {
    streamDeck.logger.error("OAuth provider returned error", { error });
    return;
  }

  const state = params.get("state");
  const code  = params.get("code");
  if (!state || !code) {
    streamDeck.logger.warn("OAuth callback missing state or code");
    return;
  }

  // CRITICAL: validate `state` to defeat CSRF.
  const attempt = pending.get(state);
  if (!attempt) {
    streamDeck.logger.error("Unknown or replayed OAuth state — rejecting", { state });
    return;
  }
  pending.delete(state);

  // Exchange code for tokens (PKCE — no client secret required)
  const body = new URLSearchParams({
    grant_type:    "authorization_code",
    code,
    redirect_uri:  REDIRECT_URI,
    client_id:     PROVIDER.clientId,
    code_verifier: attempt.codeVerifier,
  });

  const res = await fetch(PROVIDER.tokenUrl, {
    method:  "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });

  if (!res.ok) {
    streamDeck.logger.error("Token exchange failed", await res.text());
    return;
  }

  const tok = await res.json() as {
    access_token:  string;
    refresh_token: string;
    expires_in:    number;
    scope?:        string;
  };

  await streamDeck.settings.setGlobalSettings<GlobalSettings>({
    accessToken:  tok.access_token,
    refreshToken: tok.refresh_token,
    expiresAt:    Date.now() + tok.expires_in * 1000 - 30_000,   // 30s safety margin
    scope:        tok.scope,
  });

  streamDeck.logger.info("Signed in to Spotify");
}
```

---

## 4. Refresh tokens before every API call

```ts
// src/auth/oauth.ts (continued)
export async function getAccessToken(): Promise<string> {
  const s = await streamDeck.settings.getGlobalSettings<GlobalSettings>();

  if (!s.refreshToken) throw new Error("Not signed in");
  if (s.accessToken && Date.now() < (s.expiresAt ?? 0)) return s.accessToken;

  // Refresh
  const body = new URLSearchParams({
    grant_type:    "refresh_token",
    refresh_token: s.refreshToken,
    client_id:     PROVIDER.clientId,
  });
  const res = await fetch(PROVIDER.tokenUrl, {
    method:  "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });
  if (!res.ok) {
    if (res.status === 400 || res.status === 401) {
      // refresh token is dead — force re-signin
      await streamDeck.settings.setGlobalSettings<GlobalSettings>({});
    }
    throw new Error(`Token refresh failed: ${res.status}`);
  }

  const tok = await res.json() as {
    access_token:   string;
    refresh_token?: string;       // some providers rotate, some don't
    expires_in:     number;
  };

  const merged: GlobalSettings = {
    ...s,
    accessToken: tok.access_token,
    expiresAt:   Date.now() + tok.expires_in * 1000 - 30_000,
  };
  if (tok.refresh_token) merged.refreshToken = tok.refresh_token;

  await streamDeck.settings.setGlobalSettings<GlobalSettings>(merged);
  return tok.access_token;
}
```

Use it from any action:

```ts
override async onKeyDown(ev: KeyDownEvent): Promise<void> {
  try {
    const token = await getAccessToken();
    await fetch("https://api.spotify.com/v1/me/player/play", {
      method:  "PUT",
      headers: { Authorization: `Bearer ${token}` },
    });
    await ev.action.showOk();
  } catch (err) {
    streamDeck.logger.error("Play failed", err);
    await ev.action.showAlert();
  }
}
```

---

## 5. Sign out

```ts
export async function signOut(): Promise<void> {
  // Best-effort revoke on the provider (Spotify doesn't expose one; many do)
  const s = await streamDeck.settings.getGlobalSettings<GlobalSettings>();
  if (s.refreshToken && PROVIDER.revokeUrl) {
    try {
      await fetch(PROVIDER.revokeUrl, {
        method:  "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body:    new URLSearchParams({ token: s.refreshToken }),
      });
    } catch { /* ignore — local sign-out is what matters */ }
  }
  await streamDeck.settings.setGlobalSettings<GlobalSettings>({});
}
```

Surface this as a button in the PI when signed in. Reflect the
signed-in/signed-out state from `onDidReceiveGlobalSettings`.

---

## 6. PI: show "Sign in" vs "Signed in as …"

```html
<!-- ui/auth.html -->
<sdpi-item label="Account">
  <sdpi-button id="signin"  hidden>Sign in</sdpi-button>
  <sdpi-button id="signout" hidden>Sign out</sdpi-button>
  <span        id="who"></span>
</sdpi-item>

<script src="sdpi-components.js"></script>
<script>
  const { streamDeckClient } = SDPIComponents;
  const $in  = document.getElementById("signin");
  const $out = document.getElementById("signout");
  const $who = document.getElementById("who");

  function render(g) {
    const signedIn = !!g?.accessToken;
    $in.hidden  = signedIn;
    $out.hidden = !signedIn;
    $who.textContent = signedIn ? `Signed in (token expires ${new Date(g.expiresAt).toLocaleTimeString()})` : "";
  }

  streamDeckClient.onConnected(async () => {
    const { settings } = await streamDeckClient.getGlobalSettings();
    render(settings);
    streamDeckClient.onDidReceiveGlobalSettings((ev) => render(ev.settings));
  });

  $in.addEventListener("click", () => streamDeckClient.send({ event: "signIn"  }));
  $out.addEventListener("click", () => streamDeckClient.send({ event: "signOut" }));
</script>
```

The plugin already routes `signIn` → `startSignIn()`. Add `signOut`:

```ts
if (ev.payload.event === "signOut") await signOut();
```

When `setGlobalSettings` runs, every open PI receives
`onDidReceiveGlobalSettings` and re-renders. No polling.

---

## 7. The Client Secret problem (and PKCE)

A Stream Deck plugin ships to **every user's machine**. There is no
"server side" in your control. Therefore:

- ❌ **A "confidential" client secret is not actually confidential.** A
  motivated user can extract it from your plugin's bundle.
- ✅ **Use PKCE** (`code_challenge` + `code_verifier`) so a client
  secret isn't required. Every modern OAuth provider supports it.
- ⚠️ Some providers still issue a "secret" but accept PKCE-only flows
  — in that case omit the secret entirely.
- ⚠️ Some legacy providers require a secret even with PKCE. You can
  either:
  1. Accept the leakage (revoke + reissue if abused — track via OAuth app
     console).
  2. Run a tiny token-exchange proxy on your own infrastructure that
     holds the secret. Your plugin POSTs `{ code }` to your proxy; the
     proxy adds the secret and forwards to the provider. This is the
     correct architecture for plugins that integrate with secret-required
     APIs at scale.

The Elgato OAuth2 redirect proxy is **only a redirect**, not a token
exchange — it doesn't see your code or secret. You can use it
regardless of which strategy above you pick.

---

## 8. Security checklist

| ✅ | Rule | Why |
|---|---|---|
| ✅ | Validate `state` on every callback | CSRF defense |
| ✅ | Use PKCE (`code_challenge_method=S256`) | No client secret needed |
| ✅ | Store tokens in **global settings**, never action settings | Action settings leak in profile exports |
| ✅ | Refresh tokens with a 30-second safety margin | Avoids race-condition 401s |
| ✅ | Re-prompt sign-in on refresh-token failure (401/400) | Tokens get revoked/rotated server-side |
| ✅ | Validate `ev.url.path` exactly in the deep-link handler | Other apps can also fire `streamdeck://plugins/message/<UUID>/...` URLs |
| ✅ | Garbage-collect stale `pending` entries (>10 min) | Memory hygiene |
| ❌ | Don't put `client_secret` in the property inspector | The PI HTML is sent to the WebView — strictly trust-zone Chromium |
| ❌ | Don't `console.log` tokens | `streamDeck.logger` writes to disk |
| ❌ | Don't include scopes you don't need | Provider review will flag it |
| ❌ | Don't reuse the same `state` across attempts | Replay attack |

---

## 9. Provider-specific notes

| Provider | Auth URL | Token URL | Notes |
|---|---|---|---|
| **Spotify** | `https://accounts.spotify.com/authorize` | `https://accounts.spotify.com/api/token` | PKCE supported. Refresh tokens don't rotate. |
| **Twitch** | `https://id.twitch.tv/oauth2/authorize` | `https://id.twitch.tv/oauth2/token` | PKCE NOT supported (as of writing). Use the proxy strategy from §7. |
| **Google** | `https://accounts.google.com/o/oauth2/v2/auth` | `https://oauth2.googleapis.com/token` | PKCE required for native apps. `access_type=offline&prompt=consent` to get refresh token. |
| **Microsoft (Entra)** | `https://login.microsoftonline.com/<tenant>/oauth2/v2.0/authorize` | `https://login.microsoftonline.com/<tenant>/oauth2/v2.0/token` | PKCE supported. Use `tenant=common` for personal+work accounts. |
| **GitHub** | `https://github.com/login/oauth/authorize` | `https://github.com/login/oauth/access_token` | PKCE supported as of 2024 for OAuth Apps. Add `Accept: application/json` header on token exchange. |
| **Philips Hue (remote)** | `https://api.meethue.com/v2/oauth2/authorize` | `https://api.meethue.com/v2/oauth2/token` | PKCE supported. Requires Hue Bridge linking after token (press the button). |
| **YouTube** | (same as Google) | (same as Google) | Add scope `https://www.googleapis.com/auth/youtube.readonly` etc. |

For local-network APIs (Hue Bridge directly, Govee, Nanoleaf), see if
they expose a simpler API-key flow — OAuth is overkill for LAN devices.

---

## 10. Testing OAuth without polluting your real account

1. Create a **dedicated test account** with the provider — easier than
   revoking access after each test cycle.
2. Use `streamDeck.logger.debug` (set log level to DEBUG) to print every
   step of the flow: auth URL constructed, deep-link received, token
   exchange request/response (redact the token in the log!).
3. To trigger a deep-link without actually doing the OAuth dance:

   ```
   streamdeck://plugins/message/<PLUGIN_UUID>/oauth/callback?code=fake&state=fake
   ```

   Paste in the browser address bar or Windows `Win+R`. Your handler
   should reject the bogus `state` — exactly the security path you want
   to test.
4. To force a refresh, set `expiresAt: 0` in global settings via the
   PI's `streamDeckClient.setGlobalSettings({ expiresAt: 0 })`.
5. To force re-signin, clear global settings:
   `streamDeckClient.setGlobalSettings({})`.

---

## 11. Common pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Callback never reaches the plugin | Provider rejects custom scheme (Google/Microsoft) | Use the Elgato proxy URL, not `streamdeck://` directly |
| Callback reaches plugin but handler doesn't run | Handler registered on a `SingletonAction` instead of at plugin scope | Register `streamDeck.system.onDidReceiveDeepLink(...)` in `src/plugin.ts` BEFORE `streamDeck.connect()` |
| `state mismatch` rejected | `pending` map cleared on plugin restart, but browser still completes flow | Persist `pending` in global settings if you want to survive restarts. For most flows, the user just clicks Sign In again. |
| Tokens stop working after a few hours | `expiresAt` not respected; you're sending an expired token | Always call `getAccessToken()` (which refreshes) — never read `accessToken` from settings directly |
| Refresh succeeds but `refreshToken` becomes `undefined` | Provider rotated the refresh token; you overwrote it with the new (missing) value | Only overwrite `refreshToken` if the response contains one |
| User says "I keep being asked to sign in" | Token exchange returns no `refresh_token` (provider needs explicit scope/parameter) | Google: add `access_type=offline&prompt=consent`. Microsoft: add `scope=offline_access`. |
| PI button hidden on first open | `getGlobalSettings()` returned `{}` (no settings yet) | Default to "signed out" UI; the button is `hidden=false` for `signin` and `hidden=true` for `signout`. |

---

## See Also

- Deep-Linking guide (OAuth2 Redirect Proxy section): <https://docs.elgato.com/streamdeck/sdk/guides/deep-linking>
- System guide (`openUrl`): <https://docs.elgato.com/streamdeck/sdk/guides/system>
- Settings guide (global vs action): <https://docs.elgato.com/streamdeck/sdk/guides/settings>
- RFC 7636 (PKCE): <https://datatracker.ietf.org/doc/html/rfc7636>
- RFC 6749 (OAuth 2.0): <https://datatracker.ietf.org/doc/html/rfc6749>
- Sibling skills: `streamdeck-system-devices` (deep-link + openUrl),
  `streamdeck-property-inspector` (Sign-In button UI + global settings),
  `streamdeck-general` (runtime model)

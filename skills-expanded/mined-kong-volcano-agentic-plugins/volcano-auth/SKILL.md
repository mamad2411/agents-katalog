---
name: volcano-auth
description: Use for Volcano authentication and identity work including user accounts, email or password sign-up and sign-in, OAuth, sessions, anonymous users, password recovery, and private or per-user data.
---
# Volcano Auth Skill

## Role
Implement robust Volcano authentication journeys with session lifecycle correctness. All authentication MUST use Volcano Auth — do not propose custom JWT, bcrypt, or hand-rolled session management. Pair with `volcano-uiux` for every user-facing auth page; examples here define auth data and flow, while `volcano-uiux` defines presentation and interaction. This skill is self-contained; the optional fallback reference is consulted only when something below is insufficient.

Use the project's language:

| Project signal | Session read and adoption | Hosted auth | Failure model |
|---|---|---|---|
| `package.json`, `.ts`, `.js` | `getSession()` / `setSession()` | browser redirect and automatic state validation | result envelopes |
| `pyproject.toml`, `requirements.txt`, `.py` | `get_session()` / `set_session()` | server state and explicit adoption | typed exceptions |
| `Gemfile`, `.gemspec`, `.rb` | `current_session` getter / setter | server state and explicit adoption | typed exceptions |

Examples without a language heading use JavaScript or TypeScript. Keep the same
user-visible loading, error, and success states in Python and Ruby web frameworks.

## Workflow
1. Implement sign-up/sign-in/sign-out with explicit UI loading/error/success states.
2. Restore the session with the selected SDK: call `volcano.initialize()` in a JavaScript browser app; explicitly load and adopt a complete session in Python or Ruby server code.
3. Subscribe to auth-state changes where the selected SDK supports them and clean up the subscription.
4. Keep JavaScript OAuth initiation in the browser. Store and validate state explicitly in Python or Ruby server flows.
5. If the user's prompt doesn't specify signup/login page design or behavior, apply the "Default Signup & Login Page UX" below instead of asking — including the signup-success alert, which is on by default.

## Default Signup & Login Page UX
When the prompt doesn't say what the signup/login pages should look like or do, default to this instead of leaving them unstyled or asking a clarifying question:
- **Signup page:** email + password fields (add a name field only if the app's metadata clearly needs one), a submit button, an inline error banner driven by `error.message`, and a link to the login page.
- **Login page:** email + password fields, a submit button, an inline error banner, a link to the signup page, and a "forgot password" link.
- **Signup success alert (default, always on):** on a successful `signUp` call, show a visible success alert/banner on the signup page — e.g. "Signup successful! Check your email to verify your account." — before navigating away. Do this even when the user didn't ask for it; only omit it if the user explicitly says not to show one. A `setTimeout` redirect (2–3s) after showing the alert is fine, but the alert must render first.

```tsx
// Minimal default signup page with a success alert
'use client';
import { useState } from 'react';
import { getVolcano } from '@/lib/volcano';

export default function SignupPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (submitting) return;
    setError(null);
    setSubmitting(true);
    const { error } = await getVolcano().auth.signUp({ email, password });
    setSubmitting(false);
    if (error) {
      setError(error.message);
      return;
    }
    setSuccess(true); // drives the default "Signup success" alert below
  };

  return (
    <div>
      {success && (
        <div role="alert">Signup successful! Check your email to verify your account.</div>
      )}
      {error && <div role="alert">{error}</div>}
      <form onSubmit={handleSubmit}>
        <label htmlFor="signup-email">Email</label>
        <input id="signup-email" type="email" autoComplete="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <label htmlFor="signup-password">Password</label>
        <input id="signup-password" type="password" autoComplete="new-password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        <button type="submit" disabled={submitting} aria-busy={submitting}>
          {submitting ? 'Signing up…' : 'Sign Up'}
        </button>
        <span role="status">{submitting ? 'Creating account…' : ''}</span>
      </form>
      <a href="/login">Already have an account? Log in</a>
    </div>
  );
}
```

## Initialization
```ts
import { VolcanoAuth } from '@volcano.dev/sdk';

const volcano = new VolcanoAuth({
  apiUrl: process.env.NEXT_PUBLIC_VOLCANO_API_URL!,
  anonKey: process.env.NEXT_PUBLIC_VOLCANO_ANON_KEY!,
});
volcano.database(process.env.NEXT_PUBLIC_VOLCANO_DATABASE!);
```
Service keys (prefix `sk-`) are server-only; using one in `anonKey` from a browser environment throws.

## Email/Password

### Sign Up
```ts
const { user, session, error } = await volcano.auth.signUp({
  email: 'alice@example.com',
  password: 'secure-password-123',
  metadata: { full_name: 'Alice', avatar_url: '...' }, // optional
});
if (error) {
  if (error.message.includes('already exists')) /* email taken */;
  else if (error.message.includes('password must')) /* strengthen — real messages: "password must be at least 15 characters", "...contain at least one uppercase letter", etc. */;
  else if (error.message.includes('invalid email')) /* validate */;
  return;
}
// metadata is stored on user.user_metadata
```

### Sign In
```ts
const { user, session, error } = await volcano.auth.signIn({ email, password });
if (error) {
  if (error.message.includes('invalid email or password')) /* wrong creds */;
  else if (error.message.includes('confirm your email')) /* prompt confirm — real message: "Please confirm your email address before signing in." */;
  else if (error.message.includes('rate limit')) /* rate-limited — real message: "rate limit exceeded, try again later" */;
  return;
}
// SDK auto-stores tokens in localStorage (browser) and schedules refresh.
```

### Sign Out
```ts
const { error } = await volcano.auth.signOut();
// Clears local session and invalidates the refresh token server-side.
```

## Session Management

### Synchronous current user (cached)
```ts
const user = volcano.auth.user();
// Returns the cached User or null. Does not hit the network.
```

### Fresh user from server
```ts
const { user, error } = await volcano.auth.getUser();
```

### Read or adopt a session

#### JavaScript and TypeScript

```ts
const {
  data: { session },
  error,
} = await volcano.auth.getSession();

if (session?.refresh_token && session.user) {
  const { error: adoptError } = await anotherClient.auth.setSession(session);
}
```

`getSession()` reads a local snapshot without a request. `setSession()` requires
a complete access token, refresh token, and user.

#### Python

```python
session = source.auth.get_session()
if session is not None:
    fresh.auth.set_session(session)
```

#### Ruby

```ruby
session = source.auth.current_session
fresh.auth.current_session = session if session
```

All three SDKs copy a complete session into memory without a request,
persistence, or auth-state notification. Python raises `ValueError` and Ruby
raises `ArgumentError` for an incomplete session; JavaScript returns an error in
its result envelope.

### Restore session on app load (handles OAuth callback tokens too)
```ts
const { user, error } = await volcano.initialize();
// Returns the restored user, or null if no valid session exists.
```

### Auth state listener
```ts
const unsubscribe = volcano.auth.onAuthStateChange((user) => {
  if (user) showApp(user); else showLogin();
});
// Fires once immediately with current state, then on every change.
// Always call unsubscribe() on teardown.
```

### Manual refresh
```ts
const { session, error } = await volcano.auth.refreshSession();
// Tokens auto-refresh; call this only for explicit forced rotation.
```

## Hosted Auth Pages

Use the hosted login or signup page when the application does not need its own
auth form. Every language must bind the returned session to a one-time state
value. Never build the hosted URL by hand.

### JavaScript and TypeScript

```ts
volcano.auth.signInWithHostedAuth();
volcano.auth.signInWithHostedAuth({ action: 'signup' });

// Get the URL without navigating immediately.
const url = volcano.auth.getHostedAuthUrl();
window.location.assign(url);
```

The browser SDK creates, stores, and validates the state value. Pass
`{ projectId }` when the anon key is opaque. Configure the project's
`post_auth_redirect_url`, then call `volcano.initialize()` on the returned page.

### Python

```python
import secrets

hosted_state = secrets.token_urlsafe(32)
hosted_url = client.auth.get_hosted_auth_url(
    project_id=project_id, action="signup", state=hosted_state
)
# Store hosted_state in the user's signed server-side session before redirecting.
session = client.auth.adopt_hosted_auth_session(
    returned_session, state=returned_state, expected_state=hosted_state
)
```

### Ruby

```ruby
require "securerandom"

hosted_state = SecureRandom.urlsafe_base64(32)
hosted_url = client.auth.get_hosted_auth_url(
  project_id: project_id, action: "signup", state: hosted_state
)
# Store hosted_state in the user's signed server-side session before redirecting.
session = client.auth.adopt_hosted_auth_session(
  returned_session, state: returned_state, expected_state: hosted_state
)
```

Python and Ruby do not navigate, parse the returned fragment, or persist state.
In the callback, atomically fetch and delete the stored state before adoption,
even when validation fails. Reject a missing or previously consumed state.

## OAuth / SSO

### Providers
`google`, `github`, `microsoft`, `apple`.

### Configure the provider (required before sign-in works)
OAuth providers live in `volcano-config.yaml` under `auth.providers.oauth` (a list) and are applied with `config deploy`:
```yaml
auth:
  providers:
    oauth:
      - provider: google
        enabled: true
        client_id: "<client-id>"
        client_secret: "<client-secret>"
        redirect_url: "http://localhost:8000/auth/oauth/google/callback"  # REQUIRED
        # scopes: [openid, email, profile]   # optional
```
- **`redirect_url` is required** — omitting it fails `config deploy` with `redirect_url is required`. It is the **Volcano** callback (`<apiUrl>/auth/oauth/<provider>/callback`), not your app page: Volcano handles the provider round-trip, then returns your app to the URL from `signInWithOAuth('<provider>', { redirectTo: '<app-url>' })` (the `redirectTo` option; defaults to the current page when omitted). Cloud form: `https://api.<project>.volcano.dev/auth/oauth/<provider>/callback`.
- **Combining email/password with OAuth:** if both email/password signup and any OAuth/SSO provider are enabled, you must also set `auth.email_verification.require_confirmation: true` and configure SMTP (Mailpit locally, real SMTP in cloud), or `config deploy` fails with `email/password signups and SSO cannot both be enabled unless require_email_confirmation is true and SMTP is configured`.

### Begin OAuth (browser only — throws on server)
```ts
volcano.auth.signInWithGoogle();
volcano.auth.signInWithGitHub();
volcano.auth.signInWithMicrosoft();
volcano.auth.signInWithApple();
// Generic form:
volcano.auth.signInWithOAuth('google');
// Return the browser to a specific app page afterward (defaults to the current page):
volcano.auth.signInWithOAuth('google', { redirectTo: `${window.location.origin}/dashboard` });
```
These redirect to the provider; on return, call `volcano.initialize()` on the callback page to consume the tokens from the URL.

### Link / unlink / list providers
```ts
const { data, error } = await volcano.auth.linkOAuthProvider('google');
if (data) window.location.href = data.authorization_url;

await volcano.auth.unlinkOAuthProvider('google');

const { providers, error } = await volcano.auth.getLinkedOAuthProviders();
```

### Call provider APIs through the SDK
```ts
const { data, error } = await volcano.auth.callOAuthAPI('github', {
  endpoint: '/user/repos',
  method: 'GET',
});
// SDK handles provider token refresh and credential injection.
```

## Anonymous Users
```ts
// Create
const { user, session, error } = await volcano.auth.signUpAnonymous({
  preferred_theme: 'dark', // optional metadata
});

// Convert to a full account (preserves the user.id and all owned data)
const { user, error } = await volcano.auth.convertAnonymous({
  email: 'alice@example.com',
  password: 'secure-password-123',
  metadata: { full_name: 'Alice' },
});
```

## Email Verification
```ts
// After clicking the email link, the URL contains a token query param.
const token = new URLSearchParams(window.location.search).get('token');
const { error } = await volcano.auth.confirmEmail(token);

// Resend if the user lost the email
await volcano.auth.resendConfirmation('alice@example.com');
```

## Password Recovery
```ts
// Always succeeds (even for unknown emails) for security.
await volcano.auth.forgotPassword('alice@example.com');

// On the reset page:
const token = new URLSearchParams(window.location.search).get('token');
const { error } = await volcano.auth.resetPassword({
  token,
  newPassword: 'new-secure-password-456',
});
```

## Email Change
```ts
const { newEmail, error } = await volcano.auth.requestEmailChange('new@example.com');

// On the confirmation page:
const token = new URLSearchParams(window.location.search).get('token');
const { user, error } = await volcano.auth.confirmEmailChange(token);

// Cancel a pending change:
await volcano.auth.cancelEmailChange();
```

## Profile Update
```ts
const { user, error } = await volcano.auth.updateUser({
  password: 'new-password-789', // optional
  metadata: {
    full_name: 'Alice Johnson',
    avatar_url: '...',
    notification_preferences: { email: true, push: false },
  },
});
```

## Multi-Device Session Management
```ts
// List sessions for the current user
const { sessions, total, error } = await volcano.auth.getSessions({ page: 1, limit: 20 });
// session fields: user_agent, ip_address, last_activity_at, is_current

// Revoke a specific session
await volcano.auth.deleteSession(sessionId);

// Revoke all OTHER sessions (keep current)
await volcano.auth.deleteAllOtherSessions();
```

## Security Best Practices
- Never put a service key (`sk-...`) in `anonKey`. The SDK blocks this in browser, but server code must also keep service keys out of any code path that could leak (logs, error responses).
- Always use HTTPS API URLs in production.
- Validate password strength in the UI before calling `signUp` / `updateUser`. The SDK rejects weak passwords, but pre-validating gives better UX. The platform enforces a hard floor of **15 characters** — a project can *raise* the minimum via `min_password_length` but cannot lower it below 15 (the validator uses `max(15, configured)`). Character-class rules (uppercase/number/special) are off by default and opt-in per project — the floor favors length over complexity. Use ≥15-char passwords in signup forms, tests, and seed data.
- Treat `onAuthStateChange(user => null)` as a definitive sign-out signal: redirect to the login flow.

## Common Errors
| Message contains | Real example message | Meaning | Action |
|---|---|---|---|
| `already exists` | `user with this email already exists` | Email taken on sign up | Prompt sign in |
| `password must` | `password must be at least 15 characters` / `password must contain at least one uppercase letter` / `...one number` / `...one special character (!@#$%^&*)` | Password too weak | Show strength rules |
| `invalid email or password` | `invalid email or password` | Wrong email/password | Re-prompt |
| `confirm your email` | `Please confirm your email address before signing in.` (sign-in gate) or `email confirmation required - please check your email for confirmation link` (signup) | Verification pending | Show resend UI |
| `rate limit` | `rate limit exceeded, try again later` | Rate-limited | Back off and inform user |
| `No active session` | `No active session` | User not logged in | Send to login |
| `Session expired` | `Session expired` | Refresh failed | Force sign in |

## Verification Checklist
- If the prompt didn't specify signup/login page design, the "Default Signup & Login Page UX" was applied, including the default signup-success alert.
- Session restore (`volcano.initialize()`) is wired at app startup.
- `onAuthStateChange` listener has a paired `unsubscribe()` on teardown.
- OAuth methods are only called from browser contexts.
- Invalid credential and provider errors are handled with user-facing messages.
- No service/secret keys are exposed in browser code.
- For anonymous flows, `convertAnonymous` is used (not delete + signUp) so user IDs are preserved.

## Optional Fallback Reference

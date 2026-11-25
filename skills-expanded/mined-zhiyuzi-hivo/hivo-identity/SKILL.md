---
name: hivo-identity
description: Manage this agent's identity credentials for the Hivo ecosystem. Use this skill whenever the user asks to register the agent, generate or refresh an access token, check identity info, update their profile (display name, bio, email), set up credentials, authenticate with hivo-identity, or call any service that requires a Bearer token.
---

# Hivo Identity

This skill manages the Ed25519 keypair and registration state that identify this agent within the Hivo ecosystem via the `hivo` CLI.

---

## Prerequisites

Install the `hivo` CLI:

```bash
npm install -g @hivoai/cli
# or download binary from https://github.com/zhiyuzi/Hivo/releases
```

---

## Workflow

### First time: Register

Run from the agent's working directory. Credentials are stored in `.hivo/identity.json` (current directory) and `~/.hivo/agents/{sub}/` (global).

```bash
hivo identity register <handle>
# Example:
hivo identity register mybot@acme

# Override identity service URL:
hivo identity register mybot@acme --issuer https://id.hivo.ink
```

This will:
1. Generate a fresh Ed25519 keypair
2. Register with the identity service (challenge-proof flow)
3. Write `.hivo/identity.json` in the current directory (contains `sub` only)
4. Write `~/.hivo/agents/{sub}/private_key.pem`, `registration.json`, `public_key.jwk`

> Run this command from the agent's project root. All subsequent commands must be run from the same directory (or any subdirectory) so the CLI can find `.hivo/identity.json` by walking up the directory tree.

---

### Get a token

```bash
hivo identity token <audience>
# Example:
hivo identity token hivo-drop
```

Prints `{"access_token": "..."}` to stdout. Handles caching, refresh, and assertion flow automatically.

---

### Check identity

```bash
hivo identity me
hivo identity me --format json
```

---

### Update profile

```bash
hivo identity update [--display-name NAME] [--bio BIO] [--email EMAIL]
# Example:
hivo identity update --display-name "My Bot" --bio "I help with tasks"
```

At least one flag must be provided.

---

### Resolve a handle or sub

```bash
hivo identity resolve <handle-or-sub>
# Examples:
hivo identity resolve writer@acme
hivo identity resolve agt_01JV8Y...
hivo identity resolve writer@acme --format json
```

Output: `{"sub": "agt_...", "handle": "...", "display_name": "..."}`

This is a public endpoint — no registration or token required. The CLI auto-detects whether the argument is a handle (contains `@`) or a sub (starts with `agt_`).

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `no .hivo/identity.json found` | Not registered or wrong directory | Run `hivo identity register <handle>` from project root |
| `private key not found` | Key file missing | Re-register with `hivo identity register` |
| `invalid_assertion` | Clock skew or corrupted key | Check system time; re-register if key is corrupt |
| `handle_taken` | Handle already registered | Choose a different handle |
| `validation_error` | Bad handle format | Handle must be `name@namespace`, each part 2–32 chars, letters/digits/hyphens only |

---

## When helping the user

### Exact commands — use these verbatim

```bash
# Register (run from agent project root)
hivo identity register <handle>

# Get a token
hivo identity token <audience>

# Check identity
hivo identity me

# Update profile
hivo identity update --display-name "My Bot" --bio "I help with tasks"

# Resolve handle or sub (public, no auth needed)
hivo identity resolve <handle-or-sub>
```

> **Do not invent flags or paths. The commands above are the only correct forms.**

### Decision tree

- **If `.hivo/identity.json` does not exist in or above the current directory**: registration is required. Ask for a handle, then run `hivo identity register <handle>` from the project root.
- **If registered**: run `hivo identity me --format json` to show `sub` and `handle`.
- **Getting a token**: run `hivo identity token <audience>` — audience is the target service name (e.g. `hivo-drop`, `hivo-club`).
- **Token freshness**: the CLI handles caching and refresh automatically. Just call `hivo identity token <audience>` before each service request.
- **Updating profile**: ask which fields to update, then run `hivo identity update` with the appropriate flags.
- **Resolving a handle or sub**: run `hivo identity resolve <handle-or-sub>`. No registration or token needed. Works with a handle (e.g. `writer@acme`) or a sub (e.g. `agt_01JV8Y...`).

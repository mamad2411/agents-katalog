---
name: bzr-setup
description: Configure bzr for public or authenticated Bugzilla servers, credentials, and TLS trust.
---

# Set up bzr for a Bugzilla server

Goal: go from no configuration to a working bzr. Public read-only servers do not
need credentials; writes and identity-derived commands do.

## 1. Add the server

Pick a short name and the Bugzilla base URL. For public read-only exploration,
omit the API key:

```
bzr config set-server public-bz --url https://bugzilla.example.com
bzr --server public-bz server info --json
bzr --server public-bz bug view 12345 --json
```

For writes, private bugs, `whoami`, or `bug my`, choose a credential source.

Environment variable (good for CI / agents):
```
export BZR_API_KEY=...           # the Bugzilla API key
bzr config set-server my-bz --url https://bugzilla.example.com --api-key-env BZR_API_KEY
```

Or store the key directly (kept in bzr config):
```
bzr config set-server my-bz --url https://bugzilla.example.com --api-key YOUR_API_KEY
```

Or use the OS keychain (macOS Keychain / Secret Service / Windows Credential Manager):
```
bzr config set-server my-bz --url https://bugzilla.example.com
bzr config set-keyring my-bz
```

If the server uses non-default TLS trust, set one named-server trust mode:

```
bzr config set-server lab --url https://bugzilla.lab --tls-ca-cert /path/ca.pem
bzr config set-server pinned --url https://bugzilla.example.com --tls-pin-now
```

Set it as default if you have more than one:
```
bzr config set-default my-bz
```

## Stateless: no config file at all

For CI or agents, skip config entirely and define the server inline per
invocation. Nothing is read from or written to `config.toml`. The API key env
var is optional for public read-only commands:

```
bzr --server-url https://bugzilla.example.com server info --json

export BZR_API_KEY=...
bzr --server-url https://bugzilla.example.com \
    --server-api-key-env BZR_API_KEY \
    whoami
```

Add `--server-email <addr>` for the Bugzilla 5.0/5.2 email-backed `whoami`
fallback. Bugzilla 5.3+ and BMO-derived servers use native `whoami`. The named
server equivalent is `bzr config set-server <name> ... --email <addr>`. For
self-hosted TLS, use exactly one inline trust flag:
`--server-tls-ca-cert <path>`, `--server-tls-pin-sha256 <pin>`,
`--server-tls-pin-now`, or, only for controlled test systems,
`--server-tls-insecure`.

To use a sandboxed config file instead of the default, point any command at it
with `--config <path>` (overrides `BZR_CONFIG` and the default
`$XDG_CONFIG_HOME/bzr/config.toml`).

## 2. Health check

`bzr whoami --json` is the canonical "am I configured?" probe. One call answers
config + auth + server reachability together: it returns the logged-in identity
when auth works and a structured error when it does not, so no probe-bug fetch
is needed.

```
bzr whoami --json && echo "configured" || echo "not configured"
```

On success the `data` object carries the identity fields (`id`, `name`,
`real_name`, `login`) plus two connection-metadata fields: `server_name` (the
server the identity resolved against — a named server's config key, or
`(inline)` for an inline `--server-url` connection) and `auth_mode` (`api_key`
or `anonymous`), so one call confirms which server you reached and how you
authenticated. A non-zero exit means one of:

- **TLS error** — re-run `config set-server` (or the inline `--server-tls-*`
  flags) with the right `--tls-*` trust mode for the server.
- **Auth error** — the API key is missing or rejected; check the credential
  source (`bzr config show` labels each server's source).
- **Connection error** — the URL is wrong or the server is unreachable; re-check
  the configured `--url`.

See `bzr-reference` for the TLS-trust flag surface and the `schema error`
envelope that carries the failure detail; this skill does not duplicate them.

For a **public read-only server** with no API key, `whoami` cannot run — it
requires authentication. Probe reachability with the lighter anonymous call
instead:

```
bzr --server-url https://bugzilla.example.com server info --json
```

When a probe fails, `bzr config show` (server URLs and credential sources) and
`bzr server info --json` (reachability on its own) narrow down which layer broke.

## 3. Probe what the server supports

Before planning mutations, ask the server what it can do instead of discovering
it by trial and error:

```
bzr server capabilities --json   # "what can I do here?" — one structured dump
```

This reports the supported API transports and auth modes, status transitions,
custom fields, the attachment-size limit, and `supports_*` feature flags. It
works anonymously (no API key needed); fields the server does not expose are
`null` rather than errors. Branch on the result (e.g. `status_transitions` for
legal `bug update --status` targets, `custom_fields` for `cf_*` field names)
rather than probing each capability separately. Validate the shape with
`bzr schema server-capabilities`.

## Manage configured servers

```
bzr config rename-server old-name new-name   # rename in place
bzr config remove-server my-bz               # remove a server entry
```

Once `whoami` succeeds, the other bzr skills (`bzr-file-bug`, `bzr-triage-bug`,
`bzr-search-report`) will work. See `bzr-reference` for the full command surface.

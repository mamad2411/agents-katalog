---
name: self-signed-ec-dev-cert
description: One-shell-line ECDSA (P-256) self-signed cert + key for local wss:// development using openssl's prime256v1 curve.
category: devops
version: 1.0.0
version_origin: extracted
tags: [tls, dev-cert, openssl, websocket, ecdsa]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: scripts/generate-dev-cert.sh
imported_at: 2026-04-18T00:00:00Z
---

# Self-signed ECDSA dev cert

## When to use
- Developing a WebSocket (or any TLS) server and you need wss:// locally.
- Don't want to wire up a full CA or pay Let's Encrypt for dev.
- Prefer modern EC keys over 2048-bit RSA (smaller, faster handshake).
- Single-command repeatable; commit the *script*, never the cert.

## How it works
1. `openssl req -x509` = self-signed certificate request in one call (no separate CSR).
2. `-newkey ec -pkeyopt ec_paramgen_curve:prime256v1` generates an ECDSA P-256 keypair inline. P-256 is universally supported and ~5-10x faster to verify than RSA-2048.
3. `-days 365 -nodes` = 1 year validity, no passphrase on the key (ok for dev; NEVER for prod).
4. `-subj "/CN=<name>"` skips interactive prompts.
5. Writes `cert.pem` + `key.pem` next to each other so the server can `readFileSync` both.
6. The matching Node server code:
   ```ts
   tls = { cert: readFileSync('certs/cert.pem'), key: readFileSync('certs/key.pem') }
   ```
   `createHttpsServer(tls)` or `new WebSocketServer({ server: httpsServer })` is drop-in.

## Example
```sh
#!/bin/sh
set -e
OUT_DIR="${1:-certs}"
mkdir -p "$OUT_DIR"
openssl req -x509 \
  -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 \
  -keyout "$OUT_DIR/key.pem" \
  -out "$OUT_DIR/cert.pem" \
  -days 365 -nodes \
  -subj "/CN=my-app-dev"
```

Client-side (e.g. `craft-cli`) needs `--tls-ca ./certs/cert.pem`, which sets `NODE_EXTRA_CA_CERTS` so Node's TLS stack trusts the self-signed root without disabling verification globally.

## Gotchas
- `-nodes` (no DES) means the key is unencrypted at rest. Fine for dev, lethal for prod.
- Browsers will still warn "untrusted" - you can trust the cert in Keychain/certlm for first-party HTTPS pages, but for wss:// the fetch API is usually fine behind `NODE_EXTRA_CA_CERTS`.
- `prime256v1` is the same curve as `secp256r1` / `P-256`; naming varies by tool.
- Add `certs/` to `.gitignore`.

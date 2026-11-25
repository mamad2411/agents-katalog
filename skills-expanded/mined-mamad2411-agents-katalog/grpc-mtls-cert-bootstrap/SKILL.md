---
name: "grpc-mtls-cert-bootstrap"
description: "Use when a site needs local gRPC mTLS certificates generated, reused, or rotated safely before service startup."
intent: >-
  Provide a repeatable workflow for site-local gRPC TLS bootstrapping: detect missing files, generate CA and server certs only when needed or forced, wire config paths, and validate startup without missing-file failures.
type: workflow
best_for:
  - "Fixing TLS file not found errors on local gRPC services"
  - "Generating safe default cert bundles for site startup"
  - "Wiring config paths to local cert bundles"
  - "Validating launch and PM2 logs after cert generation"
scenarios:
  - "compute fails because certs/grpc/ca.crt is missing"
  - "a site should reuse existing certs unless forced"
  - "the site needs a one-command regeneration and startup check"
---

# gRPC mTLS Cert Bootstrap

## Purpose

Use this skill when a site must generate or rotate local gRPC certificates before startup so services do not fail on missing CA, server cert, or server key files.

## Core Rules

- Reuse existing cert files by default.
- Regenerate only when files are missing, unreadable, or `--force_regen_cert` is explicitly requested.
- Keep certs site-local under `sites/<site>/certs/grpc`.
- Validate file existence before restarting services.
- Treat startup logs as the final proof that the TLS bundle is wired correctly.

## Recommended File Set

For a standard local gRPC server, expect these files:

- `certs/grpc/ca.key`
- `certs/grpc/ca.crt`
- `certs/grpc/server.key`
- `certs/grpc/server.csr`
- `certs/grpc/server.crt`

If client-authenticated calls are needed for local development, add matching client material or reuse the same local server chain only when the repo already does that intentionally.

## Verified Site Contract

For the companions site, the current CouchDB/TLS contract is:

- `app-database.https: true`
- `app-database.ip_address: 127.0.0.1`
- `app-database.port: 6984`
- `app-database.caPath: assets/certs/avs-mtls-ca.crt`
- `app-database.certPath: certs/grpc/server.crt`
- `app-database.keyPath: certs/grpc/server.key`

Runtime DB TLS reads `app-database.caPath` in `shared-lib/db.js`. The CA file must match the certificate trust anchor actually presented by the endpoint, and the endpoint must be reachable over `https://localhost:6984`.

For local verification, prefer:

```powershell
curl.exe --cacert .\certs\avs-mtls-ca.crt -u couchdb:couchdb https://localhost:6984/
```

If the server certificate is self-signed, the CA file must contain the same trust anchor as the endpoint certificate.

## Quick Start

```powershell
$ErrorActionPreference = 'Stop'
$force_regen_cert = ($args -contains '-force_regen_cert' -or $args -contains '--force_regen_cert')

if (-not (Test-Path 'certs/grpc')) {
  New-Item -ItemType Directory -Path 'certs/grpc' | Out-Null
}

$required = @(
  'certs/grpc/ca.key',
  'certs/grpc/ca.crt',
  'certs/grpc/server.key',
  'certs/grpc/server.crt'
)

$missing = @($required | Where-Object { -not (Test-Path $_) })

if ($force_regen_cert -or $missing.Count -gt 0) {
  if ($force_regen_cert) {
    Remove-Item certs/grpc/ca.key,certs/grpc/ca.crt,certs/grpc/ca.srl,certs/grpc/server.key,certs/grpc/server.csr,certs/grpc/server.crt -ErrorAction SilentlyContinue
  }

  openssl genrsa -out certs/grpc/ca.key 2048
  openssl req -x509 -new -nodes -key certs/grpc/ca.key -sha256 -days 3650 -out certs/grpc/ca.crt -subj "/CN=local-grpc-ca"
  openssl genrsa -out certs/grpc/server.key 2048
  openssl req -new -key certs/grpc/server.key -out certs/grpc/server.csr -subj "/CN=localhost"
  openssl x509 -req -in certs/grpc/server.csr -CA certs/grpc/ca.crt -CAkey certs/grpc/ca.key -CAcreateserial -out certs/grpc/server.crt -days 365 -sha256
}
```

## Workflow

1. Check the site config and confirm which gRPC endpoints need TLS.
2. Verify the cert directory exists and the expected files are present.
3. Generate the CA and server cert chain only when needed or forced.
4. Wire config paths to the local cert bundle.
5. Restart or regenerate the site.
6. Confirm the startup logs no longer show missing TLS file errors.

## Troubleshooting

- If direct startup works but PM2 logs look stale, rerun from the site directory and trust the newest log sequence; PM2 can retain older startup output.
- If `node .\generated-services\ads-memory-tree.mjs` fails from the repo root, rerun it from `sites/<site>` so `site-endpoint-config.json` resolves correctly.
- If startup reports `self-signed certificate` or `certificate signature failure`, verify the CA path exists under the site folder and that `curl.exe --cacert <caPath> https://localhost:6984/` succeeds.
- If startup reports `TLS file not found`, check the path relative to `sites/<site>` before restarting.
- If the DB count still returns `0`, confirm the endpoint is listening on `6984` with HTTPS and that the site config has not drifted back to `5984`.
- If a regenerated site still fails after cert fixes, refresh the generated service from the site directory rather than editing `_gen.*` files directly.

## Site Wiring Checklist

When a site exposes a gRPC service, confirm the config points at the generated bundle:

- `grpcTlsCaPath`
- `grpcTlsServerCertPath`
- `grpcTlsServerKeyPath`
- `grpcMtlsClientCertPath` and `grpcMtlsClientKeyPath` if client auth is required

## Validation

- `Test-Path` returns true for every required PEM file.
- The site starts without `TLS file not found` errors.
- PM2 or service logs show the compute or gRPC service binding successfully.
- Health or readiness checks pass after startup stabilization.

## Anti-Patterns

- Hardcoding cert paths that do not exist in the site folder.
- Regenerating certs on every launch instead of reusing stable files.
- Editing generated service files instead of the site source of truth.
- Skipping log validation after a cert change.

## References

- `memories/repo/grpc-mtls-certs-and-encryption-process.md`
- `memories/repo/grpc-mtls-certs-quickstart.md`


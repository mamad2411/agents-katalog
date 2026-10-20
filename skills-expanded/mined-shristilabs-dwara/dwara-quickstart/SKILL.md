---
name: dwara-quickstart
description: Install and run the Dwara API gateway (Rust) for the first time - Docker quickstart with the demo config, or a minimal config from scratch, or a cargo build. Use when the task is getting Dwara installed, starting a first gateway, sending a first request, or diagnosing first-run failures (certs, ports, state DB, admin API access).
license: Apache-2.0
compatibility: Works in any agent harness supporting the Agent Skills spec (Claude Code, Cursor, Codex CLI, Copilot CLI, Gemini CLI). Gateway tasks need Docker, or a Rust toolchain for cargo builds.
metadata:
  author: shristilabs
  repo: https://github.com/shristilabs/dwara
  docs: https://shristilabs.github.io/dwara/
  version: "0.1.0"
---

# Dwara quickstart

Get a Dwara gateway running and verified. Dwara is a streaming reverse-proxy
API gateway in Rust: one strict YAML config file, hot reload, an mTLS admin
API, and an AI gateway for LLM traffic.

**Always read [references/install.md](references/install.md) before choosing
an install path, and [references/verify-and-troubleshoot.md](references/verify-and-troubleshoot.md)
after the gateway starts.**

## Decision: which path

| Situation | Path |
| --- | --- |
| Want a full feature demo fastest (TLS, auth, AI, analytics) | A. Docker quickstart from the repo |
| Just want a gateway serving a response in <2 minutes, no clone | B. Minimal config (asset in this skill) |
| Going to develop against or extend Dwara | C. cargo build |

## Path A - Docker quickstart (recommended)

```sh
git clone https://github.com/shristilabs/dwara
cd dwara/quickstart
./gen-certs.sh                 # writes ./certs: server certs + client CA + client cert
cd oss
docker compose up --build      # builds Dockerfile.scratch; nginx:alpine demo upstream
```

What comes up (host ports):

- `:8443` - TLS-terminated HTTPS entry point (primary). Server cert from `certs/`.
- `:8080` - plaintext HTTP (local dev, health checks).
- `:2019` - **mTLS-only** admin API. Requires the client cert signed by `certs/client-ca.crt`.

Verify immediately:

```sh
curl --cacert ../certs/server.crt https://localhost:8443/          # demo page via nginx upstream
curl http://localhost:8080/healthz                                  # gateway-responded 200 "ok"
curl --cert ../certs/client.crt --key ../certs/client.key \
     --cacert ../certs/server.crt https://localhost:2019/health     # admin API
```

The quickstart `dwara.yaml` is a commented, feature-complete tour of every
OSS capability - keep it open as a reference while working. An API key
consumer ships in it: header `X-API-Key: dwara-quickstart-api-key` on
`/v1/...` routes.

## Path B - Minimal config from scratch

1. Copy [assets/minimal-dwara.yaml](assets/minimal-dwara.yaml) to a working
   directory as `dwara.yaml`.
2. Run the gateway against it (binary from Path A image or Path C build):
   `DWARA_CONFIG=./dwara.yaml ./dwara`
3. Smoke it: `scripts/smoke-test.sh` (defaults to `http://127.0.0.1:8080`,
   override with `DWARA_URL`), or `curl -i http://127.0.0.1:8080/`.

The route uses a gateway-served `respond` action, so the placeholder
upstream is never dialed - no backend needed for a first light.

## Path C - cargo build

```sh
git clone https://github.com/shristilabs/dwara && cd dwara
cargo build --release
```

Binaries in `target/release/`:

| Binary | Role |
| --- | --- |
| `dwara` | The gateway. `DWARA_CONFIG=<path> ./dwara` |
| `dwara-cli` | Operator CLI: `validate`, `fmt`, `diff`, `lint`, `explain`, `schema`, `import`, `tf`, `status`, `top`, `upgrade`, `replay`, `plugin` |
| `dwara-loadgen` | Benchmark rig (`--echo` in-process upstream, `--url`, `--protocol h1|h2|h3`, `--json`) |

Editions: the default build is OSS (Apache-2.0). Enterprise adds
fleet/shared-state features with `cargo build --release --features ent`
(license-gated at runtime; an expired license degrades to OSS behavior, it
never breaks traffic). For a first run, the OSS build is complete - TLS,
auth, rate limiting, resilience, observability, and the AI gateway are all
in it.

## Rules for anything beyond first light

- Validate every config change before reload:
  `dwara-cli validate dwara.yaml`. The config is **strict** - unknown keys
  are errors, not warnings.
- The admin API is **default-off** and **mTLS-only**; there is no plaintext
  admin listener in production setups (`DWARA_ADMIN_DEV=1` is loopback-dev
  only).
- Set `DWARA_STATE_DB` (SQLite path) if you use consumer quotas or MCP
  sessions - without it quotas are **not enforced** (the gateway warns in
  logs on each request).
- Reserved paths `/healthz`, `/readyz`, `/metrics` are served by the gateway
  itself on every listener and bypass global policies.

## Next steps after this skill

- Structured config authoring: the `dwara-config` skill.
- LLM traffic: the `dwara-ai-gateway` skill.
- Everything about routes/upstreams/resilience: the `dwara-traffic` skill.

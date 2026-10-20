---
name: full-backend-architecture
description: "Scaffold a backend project's root layout: cmd/ or entrypoints, backend logic (Go via go-module-architecture, or Node.js via express-module-architecture), nginx/ (reverse proxy), and docker/ (Dockerfiles + compose). Not Go-only — detects backend language from go.mod vs package.json and adapts the entrypoint/module convention; nginx/ and docker/ stay shared either way. Use whenever the user asks to scaffold a new backend project/service (Go or Node.js), set up a project's root structure, add a new binary/entrypoint (api/worker/cron), wire nginx or Docker around a backend, or asks how to lay out cache/distributed-system bootstrap code. On first use in a repo, confirm the backend language if undetectable, and for Go, whether cmd/ is idiomatic (thin main.go, infra in backend/platform) or holds infra wiring directly — unless already stated for this repo."
---

# Full Backend Architecture Skill

Project-root layout that sits around one or more feature modules, for either a Go or a
Node.js backend. `nginx/` and `docker/` are shared scaffolding regardless of language;
`cmd/` vs entrypoint files, and the module-root name, fork by language.

## Output Format

Always output a tree diagram of the full project root with a one-line annotation per
file/folder. No code unless explicitly requested.

## Step 0 — Detect the backend language

1. `go.mod` at repo root → Go backend → use the **Go variant** below (delegates
   feature modules to `go-module-architecture`).
2. `package.json` at repo root → Node.js backend → use the **Node variant** below
   (delegates feature modules to `express-module-architecture`).
3. Both present (polyglot repo, e.g. a Go service next to a Node service) → ask which
   one this scaffold request is for, or scaffold both roots side by side if the user
   asked for a mixed setup.
4. Neither present (brand-new repo) → ask once, then remember for the rest of the
   session/repo.

## Why one skill covers both languages instead of two separate skills

- **Why:** the backend isn't Go-only — nginx/Docker scaffolding is the same shape
  whether the service behind it is Go or Node.
- **Problem solved:** one trigger, one file to keep current, instead of two
  near-duplicate root-layout skills whose shared `nginx/`/`docker/` guidance could
  drift out of sync with each other.
- **When useful:** any new service, regardless of which language it ends up in.
- **Drawback:** this file is now branchier — two variants to read per trigger instead
  of one lean single-language skill.
- **Alternative:** keep `go-full-backend-architecture` Go-only and add a separate
  `node-full-backend-architecture` — cleaner single-purpose files, at the cost of
  duplicating (and eventually desyncing) the nginx/docker sections.

## The Go variant

### The cmd/ decision (ask once per repo, then remember it)

Go's ecosystem convention (`golang-standards/project-layout`) keeps `cmd/` to
entrypoints only. A literal alternative puts infra bootstrap (cache clients,
distributed locks, pub/sub) directly inside `cmd/`. Present this table if the repo
hasn't decided yet:

| | **Idiomatic** (`cmd/` = entrypoints only) | **Infra-in-cmd** (`cmd/` owns wiring) |
|---|---|---|
| Why | Matches ecosystem convention; any Go reader orients instantly | Fewer files to trace for one maintainer |
| Problem solved | Keeps entrypoints thin/testable; `package main` code stays import-unfriendly-but-minimal | Fewer hops when debugging one binary's startup |
| Best when | Multiple binaries share the same infra client (e.g. `cmd/api` and `cmd/worker` both need Redis) | A single binary, or infra genuinely isn't shared yet |
| Drawback | An extra `backend/platform/` layer that can feel like ceremony on a small service | Duplicated or refactored the moment a second binary needs the same client; less recognizable to Go-experienced collaborators |

Default if no strong preference: **idiomatic**, but don't pre-emptively create
`backend/platform/` until a second binary actually needs to share something in it
(YAGNI) — inlining in `main.go` still counts as "idiomatic enough" for one binary.

### Go folder structure

```
project-root/
├── cmd/
│   ├── api/
│   │   └── main.go               → HTTP entrypoint: load config, construct deps, mount modules, router.Run()
│   └── worker/
│       └── main.go               → background job / queue consumer entrypoint
├── backend/
│   ├── module/
│   │   └── {name}/                → one go-module-architecture module per feature
│   └── platform/                  → present only under the "idiomatic" cmd/ choice — cache/, lock/, pubsub/
├── nginx/                          → see shared section below
└── docker/                         → see shared section below
```

## The Node.js variant

### Why there's no cmd/ for Node

`cmd/` is a Go/Rust ecosystem idiom tied to compiling separate binaries. Node has no
compile-to-binary step — `node dist/server.js` and `node dist/worker.js` are just two
entry files run directly. Forcing a `cmd/` folder here would be a directory that looks
meaningful to a Go reader but does nothing (nothing compiles into it), and it fights
what Node tooling/deploy scripts (pm2, Docker `CMD`, systemd units) actually expect.

- **When you might still want folder-parity anyway:** if you're running Go and Node
  services side by side and want to jump into either repo and orient the same way —
  real value for a sole engineer maintaining both. If you want this, say so and the
  entrypoints can be nested as `cmd/api/index.ts` / `cmd/worker/index.ts` purely for
  visual consistency — it's a cosmetic override of Node convention, not a correctness
  issue either way.
- **Default (no folder-parity requested):** entrypoints live directly under `src/`, matching
  `express-module-architecture`'s own root.

### Node folder structure

```
project-root/
├── src/
│   ├── server.ts                  → HTTP entrypoint (Express app + listen)
│   ├── worker.ts                  → background job / BullMQ consumer entrypoint
│   ├── modules/
│   │   └── {name}/                 → one express-module-architecture module per feature
│   └── lib/  (or shared/)          → shared infra clients (Redis cache, distributed lock, pub/sub) — Node's equivalent of Go's backend/platform
├── nginx/                          → see shared section below
└── docker/                         → see shared section below
```

## Shared: nginx/ and docker/

```
nginx/
├── nginx.conf                      → reverse proxy: routes → api entrypoint, TLS termination
└── conf.d/
    └── {service}.conf              → per-service server block

docker/
├── Dockerfile.api                  → Go: multi-stage golang build → distroless/alpine
│                                      Node: multi-stage node build (npm/pnpm ci + tsc) → node:alpine runtime
├── Dockerfile.worker                → same split, worker entrypoint
└── docker-compose.yml               → wires api + worker + datastore(s) + redis + nginx
```

## How to Respond

1. Run Step 0 (detect language) before anything else.
2. For a Go backend on first use in a repo with no stated `cmd/` preference, present
   the idiomatic-vs-infra-in-cmd table and ask before scaffolding.
3. For a Node backend, default to no `cmd/` (entrypoints under `src/`) unless the user
   has asked for folder-parity with a Go sibling service.
4. Output the full annotated tree for the project root, marking which variant/choices
   were used.
5. Do NOT generate file contents unless explicitly asked.
6. Hand off feature-module scaffolding to `go-module-architecture` (Go) or
   `express-module-architecture` (Node) rather than duplicating their structure here.

## Integration Point

**Go:** `cmd/api/main.go` mounts each `backend/module/{name}` module's router, then
`nginx/nginx.conf` proxies to wherever it binds, and `docker-compose.yml` starts
nginx + api + worker + datastores together for local dev.

**Node:** `src/server.ts` mounts each `src/modules/{name}` module's router the same
way, with the same nginx/docker relationship.

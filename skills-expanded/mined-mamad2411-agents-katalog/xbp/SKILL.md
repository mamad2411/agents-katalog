---
name: xbp
description: >
  Operate and debug the XBP ops CLI end-to-end: init wizard, version/release/bump,
  deploy (xbp-deploy engine: plan/run/verify), native OCI registry (registry.xbp.app),
  local OCI load without registry push, Docker Desktop Kubernetes, Cloudflare Workers
  (container + static assets), Linear pickers, and consumer-repo ship. Use when the user
  runs /xbp, xbp deploy, xbp oci, xbp v release, local-image, docker-desktop, ImagePullBackOff,
  or needs to deploy without crates/npm publish first.
---

# XBP skill

Playbook for the **xbp** CLI (Rust ops tool). Prefer the built binary under the xbp
repo (`cargo build -p xbp` then `target/debug/xbp.exe`) when testing unreleased
changes; otherwise `xbp` on PATH.

| Reference | Topic |
|-----------|--------|
| `references/deploy-local-oci.md` | Local vs push images, dockerignore |
| `references/xbp-deploy.md` | Deploy engine + `xbp deploy` |
| `references/xbp-registry.md` | Native registry `registry.xbp.app` |

## When this skill applies

- Any `xbp` command: init, release, bump, deploy, oci, secrets, MCP, cloudflare, linear
- Consumer projects using `.xbp/xbp.toml` + `xbp deploy`
- OCI / registry.xbp.app push failures, empty version targets, CF static docs first deploy

## Core mental model

| Surface | Owns |
|---------|------|
| `.xbp/xbp.toml` | services, workers, oci, deploy, versioning, linear, issues |
| `xbp init` | Full setup wizard (release, CF, Linear pickers, OCI defaults, login) |
| `xbp version` / `xbp v` | bumps, release tags, optional OCI image push |
| `xbp deploy` | plan/run/verify via **xbp-deploy** crate |
| `xbp oci` | inspect / tags / promote / **doctor** against registry + storage |
| `registry.xbp.app` | Native Distribution (edge Worker + R2/D1 storage) |
| `<project>/.xbp/deployments/` | Deploy history (prefer over `~/.xbp/logs/`) |

Package publish (crates.io/npm) is **not** required for deploy.

---

## `xbp init` wizard

★ = default selected:

| Module | Notes |
|--------|--------|
| Version targets ★ | Release scope |
| GitHub release ★ | Branch template + optional token |
| Linear release ★ | Key → **org/workspace FuzzySelect** (API `urlKey`) + initiative + team |
| Issue/TODO automation | `issues:` for `xbp issues scan/sync` (team/project pickers) |
| cargo-dist / crates / npm | Publish |
| Cloudflare auth ★ | Token + auto account ID when one account |
| Cloudflare Workers | Register; tip for static assets init |
| OCI registry | Default **registry.xbp.app** + release `local-build-push` |
| K8s / deploy defaults ★ | Context, groups, env |
| Discord ★ / Monitoring | Webhooks / health |
| CLI login | Dashboard session for deploy secrets |

**Linear:** with token set, do not ask operators to type org/workspace slug — fetch and pick.

---

## Deploy (xbp-deploy engine)

```bash
xbp deploy                          # interactive
xbp deploy <svc> --local-image --run --yes --env production
xbp deploy <svc> --to cloudflare --run --yes
xbp deploy <svc> --plan
xbp deploy --history
xbp deploy --engine-check
```

| Goal | Flag |
|------|------|
| Local k8s | `--local-image` (auto on docker-desktop / kind / minikube / k3d) |
| Push image | `--push-image` |
| Image ready | `--skip-build` |
| Destination | `--to cloudflare` / `kubernetes` / `all` |

### Providers

- **kubernetes** — bootstrap/manifests, compose `.env`, expose/port-forward
- **cloudflare-worker** — static assets / OpenNext; plan has **no OCI / no containers rollout**
- **cloudflare-containers** — Worker + Container (athena-auth shape)

### Compose (k8s)

Auto `.env` / `.env.{env}` / `.env.local` + `services.environment` + `deploy.envs.*.env` → pod env; `config.yaml` → ConfigMap; `required_env` fails plan if missing.

### Failure triage

| Symptom | Fix |
|---------|-----|
| ImagePullBackOff | `--local-image` or push + pull secrets |
| `.next` / node_modules in build context | Recursive `.dockerignore` |
| CF “not ready” | `xbp config cloudflare status` (auto account if 1) |
| Assets plan shows OCI/containers | Rebuild xbp; provider should be `cloudflare-worker` |
| Secret plaintext in history | `--redact-history`; `xbp login` for soft-upload |

Details: `references/xbp-deploy.md`.

---

## Native registry (xbp-registry)

**Endpoint:** `https://registry.xbp.app/v2/`

```text
docker / xbp v release --oci
    → registry.xbp.app (apps/registry Worker+Container)
    → storage Worker (R2 xbp-registry + D1 xbp-registry-db)
```

```bash
xbp oci doctor
xbp oci inspect registry.xbp.app/<owner>/<svc>:<tag>
export XBP_OCI_TOKEN=…
docker login registry.xbp.app
xbp v release --oci
```

Init enables:

```toml
[versioning.release.oci]
enabled = true
strategy = "local-build-push"
tag_templates = ["{version}", "{version}-{flag}"]
```

Details: `references/xbp-registry.md`.

---

## Cloudflare

### Credentials

```bash
xbp config cloudflare status   # auto-selects account if token sees exactly one
xbp config cloudflare setup
```

### Worker + Container

```bash
xbp cloudflare doctor --app athena-auth
xbp cloudflare deploy --app athena-auth --rollout immediate
xbp deploy athena-auth --to cloudflare --run --yes
```

### Static assets (docs / Blume / Astro) — first-time one-shot

```bash
xbp cloudflare init --kind assets \
  --worker-root apps/docs \
  --domain my-app.xbp.app \
  --service docs \
  --assets dist \
  --write
xbp deploy docs --to cloudflare --run --yes
```

`--kind static` alias. Domain from blume/astro `site` when possible.

**`--app` placement (all work):**  
`workers --app X deploy run` · `workers deploy --app X run` · `workers deploy run --app X`

### OpenNext

```bash
xbp workers --app <name> deploy run
# stages: install → heroui → whoami → build → entry_assert → wrangler
```

---

## Version / release

Empty “no version targets matched” → wrong **scope** or no path hits; `--force` includes all targets for scope; TTY offers switch-scope.

```bash
xbp v bump
xbp v release --allow-dirty --force
xbp v release --oci              # versioned push to registry.xbp.app when configured
xbp v release --oci-local-only
xbp v release --no-oci
```

---

## Build xbp

```bash
cargo build -p xbp --locked
cargo build -p xbp --features all
cargo test -p xbp-deploy --locked
cargo test -p xbp-oci --locked
```

Gotchas: `.cargo/config.toml` may set `jobs = 1`; incomplete `Cargo.lock` → `cargo generate-lockfile`.

---

## Agent rules

1. **Do not** require crates.io/npm publish before deploy.
2. Local kube → **local-image**, not ghcr push.
3. Prefer project `.xbp/deployments/` for deploy failures.
4. Fix **consumer** Dockerfile/dockerignore when build context fails.
5. After deploy, check **pod logs** / live health, not only `Result: ok`.
6. Rebuild `target/debug/xbp` after CLI deploy/init changes before retesting consumers.
7. Linear org slug: use API picker when token present — never invent free-type as primary UX.
8. Never commit CF / OCI / Linear tokens.
9. Static docs: `cloudflare init --kind assets` then `xbp deploy <svc> --to cloudflare --run --yes`.
10. Registry durability is `apps/registry-storage` + edge `apps/registry` — not “force whole xbp.app promote”.

## Quick commands

```bash
xbp init
xbp deploy                          # interactive
xbp deploy <svc> --local-image --run --yes
xbp deploy <svc> --to cloudflare --run --yes
xbp oci doctor
xbp v release --oci --allow-dirty
xbp cloudflare init --kind assets --worker-root apps/docs --service docs --write
xbp config cloudflare status
kubectl config current-context
```

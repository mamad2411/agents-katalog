---
name: infra-distroless
description: Use when shipping distroless containers — image selection, nonroot user, debugging without a shell, common pitfalls.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-18"
  related: [infra-docker-images, infra-docker-compose, infra-docker-swarm, security, go-essentials]
---

# Infra Distroless

**Iron Law: distroless `:nonroot` always (UID 65532). Pin runtime by `@sha256:` digest in prod. No `:latest`, no `:debug` as the default tag, no `RUN` instructions in a distroless stage — there is no shell to run them.**

**Versions:** Current `debian12` (bookworm) · Next `debian13` (trixie) — _Google publishes one tag family per Debian release; pin the codename, not `latest`. Switch to `debian13` once your stdlib/runtime matches._

## What distroless actually is

Built from Debian's `deb` packages by Bazel rules from `GoogleContainerTools/distroless`. **No shell, no package manager, no coreutils.** Just: the libc/runtime your workload needs, ca-certificates, tzdata, `/etc/passwd` entries for `root` and `nonroot`, and CA roots. Total surface area: a handful of binaries. That's the value — every shell, every `wget`, every `apt` you don't ship is a CVE you don't carry.

For the build-stage Dockerfile pattern (multi-stage, BuildKit cache mounts, picker by workload), see `Skill(infra-docker-images)`. This skill is the **runtime image deep-dive** — picking the right variant, debugging when there's no shell, and the surprises that bite you.

## Image picker

| Variant                                       | Workload                                | What's in it                               |
| --------------------------------------------- | --------------------------------------- | ------------------------------------------ |
| `gcr.io/distroless/static-debian12:nonroot`   | Static Go / Rust binary                 | libc-free; ca-certs; tzdata; `/etc/passwd` |
| `gcr.io/distroless/base-debian12:nonroot`     | Go cgo, anything needing glibc + libssl | glibc, libssl, libgcc, ca-certs            |
| `gcr.io/distroless/cc-debian12:nonroot`       | C/C++ binaries needing libstdc++        | base + libstdc++, libgcc, libgomp          |
| `gcr.io/distroless/python3-debian12:nonroot`  | Python apps (Python 3.11 on `debian12`) | cc + Python interpreter                    |
| `gcr.io/distroless/nodejs22-debian12:nonroot` | Node apps (LTS 22)                      | cc + Node binary; no npm                   |
| `gcr.io/distroless/java21-debian12:nonroot`   | JVM apps                                | cc + JRE 21                                |

**Always pick `:nonroot`.** The plain tag runs as root by historical accident; the nonroot variant runs as UID/GID `65532` with `$HOME=/home/nonroot`. Kubernetes admission controllers (Pod Security Standards "restricted") refuse non-nonroot images.

## Pinning by digest

```dockerfile
# In prod: pin by digest, not tag. Tags move; digests don't.
FROM gcr.io/distroless/static-debian12:nonroot@sha256:d71f4b239be2d412017b798a0a401c44c3049a3ca454838473a4c32ed076bfea
```

Resolve once: `docker buildx imagetools inspect gcr.io/distroless/static-debian12:nonroot --format '{{json .Manifest.Digest}}'`. Re-pin during scheduled refresh, not on every build. Renovate / Dependabot manage this for you. Pinning by tag in CI **and** never doing `docker pull --platform` from a clean cache means your CI eventually drifts from prod's actual layers.

## ca-certificates: already there

Every distroless image ships `/etc/ssl/certs/ca-certificates.crt`. **Do not** `COPY` your own; do not `RUN update-ca-certificates` (you can't, no shell). If you need a private CA, copy the single PEM **into** the existing bundle at build time from the builder stage, not into distroless directly.

## The UID 65532 surprise

```dockerfile
FROM gcr.io/distroless/static-debian12:nonroot
# Files copied without --chown stay owned by root → unreadable to UID 65532
COPY --from=builder --chown=nonroot:nonroot /out/api /api
USER nonroot
ENTRYPOINT ["/api"]
```

Forget `--chown=nonroot:nonroot` and your binary copies fine, runs fine, then crashes the first time it tries to read a config file shipped beside it. Same trap for mounted volumes — set `fsGroup: 65532` (k8s) or `user: "65532:65532"` (compose) on any writable mount.

## No `/tmp`, no `/etc/passwd` writes, no shell

| Surprise                                               | Reality                                                      | Workaround                                                                           |
| ------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| Code calls `tempfile.NamedTemporaryFile()` and crashes | `/tmp` doesn't exist                                         | Mount `tmpfs` at `/tmp`, or use `os.TempDir()` configured to a known mount           |
| Library tries to read `/etc/nsswitch.conf`             | absent                                                       | Set `GODEBUG=netdns=go` (Go) or accept the warning                                   |
| Code shells out to `git`/`curl`/`openssl`              | no shell, no binaries                                        | Use a library, not a subprocess. If you can't, distroless is wrong for this workload |
| Need to add a user at runtime                          | can't — no `useradd`, no writable `/etc/passwd`              | Bake the user at build time (already done for `nonroot`)                             |
| Need `cron`                                            | no cron daemon, no shell for `crontab` entries               | Run cron in a sidecar (separate image with shell); the worker stays distroless       |
| Crash on missing locale                                | `LANG` defaults to `C.UTF-8`; non-ASCII path bytes may panic | Set `LANG=C.UTF-8` explicitly; ship locales in builder if you really need them       |

## Debugging without a shell

Three options, in increasing pain:

1. **`docker logs`, structured logs, `slog`/`pino`/`structlog`.** This is the design intent. Logs + traces + metrics replace `kubectl exec`. If you reach for a shell, your observability has a gap.
2. **Ephemeral debug container (k8s 1.25+):**
   ```bash
   kubectl debug -it <pod> --image=busybox:1.36 --target=<container>
   ```
   Joins the namespaces of the target, gives you `sh` + busybox tools, leaves the original image untouched.
3. **`:debug` tag.** Same image + busybox at `/busybox/sh`. **Triage only, never the default.**
   ```bash
   docker run --rm -it --entrypoint=/busybox/sh gcr.io/distroless/static-debian12:debug-nonroot
   ```
   In compose, override at runtime: `docker compose run --entrypoint /busybox/sh api`. The `-debug` SUFFIX (e.g., `:debug-nonroot`) means _with busybox_; the `nonroot` prefix without `-debug` means _no shell_.

If your runbook says "ssh in and tail the log", you've already lost — distroless is removing that primitive on purpose. Build for `kubectl logs` / `docker logs`, not for shelling in.

## When distroless is the wrong tool

- **Cron entrypoint** that wraps the binary in `sh -c '... && ...'`. Run the binary as PID 1 (no shell wrapper) or use `*-slim` instead.
- **Runtime package installation** (`apt install` on first boot). Bake at build time or use a slim base.
- **`exec`-based health checks** (`exec ["sh", "-c", "test -f /run/healthy"]`). Use HTTP/TCP healthchecks instead — the binary exposes `/healthz`, the orchestrator probes it.
- **One-off images for a contractor who needs to poke around.** Give them a `*-slim` dev image; keep distroless for prod.
- **Init scripts that wait on dependencies via `wait-for-it.sh`.** Move the wait logic into the app (`pgxpool` retries; `db.Ping()` with backoff). Bonus: it's faster + more correct.

## Compose / Swarm wiring

```yaml
services:
  api:
    image: ghcr.io/me/api@sha256:abc123... # built FROM distroless, pinned
    user: "65532:65532" # match the baked nonroot UID
    read_only: true # distroless rootfs is read-only-friendly
    tmpfs:
      - /tmp:size=64M,mode=1777 # if app writes scratch files
    cap_drop: [ALL]
    security_opt: [no-new-privileges:true]
    healthcheck:
      test: ["CMD", "/api", "-healthcheck"] # binary self-checks; no curl in image
      interval: 10s
```

The `gateway` service runs this exact pattern: `FROM gcr.io/distroless/static-debian12:nonroot`, binary as PID 1, no shell, healthcheck flag on the binary itself.

## Anti-patterns

- `:latest` or unpinned-by-digest in prod — Google rebuilds these; layers drift silently.
- `FROM distroless` then `RUN apt install ...` — there is no `apt`, the build fails with a confusing error.
- `COPY` without `--chown=nonroot:nonroot` and then running as `nonroot` — readable to root only, app crashes.
- `ENTRYPOINT ["sh", "-c", "/api"]` — sh doesn't exist; container exits immediately with no log.
- Healthcheck `["CMD", "curl", "-fsS", "..."]` inside a **distroless** image — neither `curl` nor `wget` is present; **use a binary self-check (e.g., a `--healthcheck` flag your binary handles) or move the probe to the orchestrator layer**. Non-distroless images that ship curl (gotenberg, nginx, postgres) can use curl normally — this anti-pattern is distroless-specific.
- Logging to a file under `/var/log/` — `/var/log` may not exist and is not writable. Log to stdout, full stop.
- `:debug` tag in production "just in case" — defeats the purpose; ships busybox + every busybox CVE.

## Red flags

| Thought                                 | Reality                                                                                                               |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| "I'll just add `sh` to the image"       | You've reinvented `*-slim`. Use `*-slim`.                                                                             |
| "Distroless makes debugging impossible" | It makes shell-debugging impossible. Logs + traces + ephemeral containers replace it.                                 |
| "Pinning by digest is too strict"       | Tag drift hits the day Google rebuilds and your CVE scanner screams about a layer you didn't change.                  |
| "We need root for port 80"              | Bind to 8080, terminate at a proxy. Or use `CAP_NET_BIND_SERVICE` on the binary. Never run as root for a port number. |

## Hand-off

For the multi-stage build Dockerfile pattern that produces a distroless artifact: `Skill(infra-docker-images)`. For wiring these images in compose/swarm with healthchecks, secrets, and overlays: `Skill(infra-docker-compose)`, `Skill(infra-docker-swarm)`. For the security posture (read-only rootfs, cap_drop, no-new-privileges, seccomp): `Skill(security)`. For the Go build flags that produce distroless-ready static binaries: `Skill(go-essentials)`.

---
name: docker
description: Use when writing or reviewing a Dockerfile, a compose file, a .dockerignore or a container entrypoint script — adding or bumping any image reference (FROM, COPY --from, an image under a service), choosing a base image, wiring Dependabot or Renovate for images, or a container that takes ten seconds to stop.
---

# Docker

Every image a Dockerfile or a compose file names is looked up today: the newest
stable release that the project's runtime pin and its existing data allow, on
the smallest base that runs the app, pinned to that exact version.

## Look the version up, never recall it

Training data lags the registry by dozens of releases, so a version from memory
is already old. Pick the release line first:

1. The project pins its runtime — `.nvmrc`, `engines`, `.python-version`,
   `requires-python`, the `go` line in `go.mod`, `.tool-versions` — and the
   image follows it.
2. Nothing pins it — the newest LTS line when the runtime has LTS lines,
   otherwise the newest stable line.

Never a pre-release, however the tag spells it: `rc`, `beta`, `alpha`,
`nightly`, `canary`, `unstable`, `tip`.

```bash
# Release lines, newest first. `lts` is true, false, or the date a line became
# LTS — a date still ahead means not yet. Product names that are not the obvious
# ones (nodejs, postgresql): https://endoflife.date/api/all.json
curl -s https://endoflife.date/api/nodejs.json \
  | jq -r '.[:4][] | "\(.cycle) latest=\(.latest) lts=\(.lts) eol=\(.eol)"'

# Tags on that line, in the variant you want. Versions have as many parts as
# the image publishes — x.y.z for node, x.y for postgres
curl -s 'https://hub.docker.com/v2/repositories/library/node/tags?page_size=100&name=<line>.' \
  | jq -r '.results[].name' | grep -E '^<line>\.[0-9.]+-alpine$' | sort -V | tail -3

# Confirm the tag resolves before writing it down
docker buildx imagetools inspect node:<tag>
```

Official images live under `library/`; others under their namespace
(`getmeili/meilisearch`). For GHCR and other registries start from the project's
latest release — `gh api repos/<owner>/<repo>/releases/latest --jq .tag_name` —
and let `imagetools inspect` settle the tag, which may drop the release's `v`.

## Pin exactly what you found

```dockerfile
FROM node:<x.y.z>-alpine        # yes — the exact release, on the variant
FROM node:<x.y.z>-alpine<a.b>   # no — updaters stop once the image drops that Alpine
FROM node:<x>-alpine            # no — the next pull is a different release
FROM node                       # no — no tag means latest
```

The same goes for every place an image is named: `FROM`, `COPY --from=<image>`,
`RUN --mount=from=<image>`, and `image:` in compose. `latest`, a bare name,
`lts`, `stable`, and a major or minor alone all float: a rebuild picks up a new
release, and nothing in the diff says so.

The OS release under the variant stays out of the tag. Dependabot and Renovate
move a tag only within its suffix, so a pin on one Alpine release stops getting
bumps, silently, when the image stops building on it. A database on Debian is
the one exception — see below.

Dependabot reads only `FROM` lines, so an image used by `COPY --from` or
`RUN --mount=from` gets a stage of its own and is named from there:

```dockerfile
FROM ghcr.io/astral-sh/uv:<x.y.z> AS uv
…
COPY --from=uv /uv /bin/uv
```

An image published without version tags — distroless — is pinned by digest,
`@sha256:…`. A project that already pins by digest everywhere keeps doing so.

When compose pulls the project's own image from a registry, it names the tag CI
pushed — the commit SHA or the release — through a variable that fails when
unset, `image: ghcr.io/<owner>/<app>:${APP_IMAGE_TAG:?}`, never `:latest`.
Compose interpolates every file before merging them, so a dev override that
builds the image instead still fails without the variable: the dev entry point
sets it, `APP_IMAGE_TAG=dev`.

## An exact pin needs something that bumps it

A pinned tag no longer picks up the patches a floating one would have, so the
repository raises those bumps itself. Before finishing, look at what it has:

- `renovate.json` or another Renovate config — covered; its Dockerfile and
  compose managers are on by default.
- `.github/dependabot.yml` with `docker` and `docker-compose` entries whose
  directories reach every file you touched — covered.
- Anything else on GitHub — add the missing entries in the same change.
  `directories` takes globs, so one entry covers `docker/*` or `apps/*`:

```yaml
version: 2
updates:
  - package-ecosystem: docker
    directories: ["/", "/apps/*"]
    schedule:
      interval: weekly
  - package-ecosystem: docker-compose
    directory: /
    schedule:
      interval: weekly
```

Not on GitHub — name the missing updater in the final report.

## An image the task is not about keeps its line

A floating tag already in a file is pinned to what it resolves to today — the
same major, the same variant. Moving it to a new major or another variant,
Debian to Alpine included, is a change of its own: name it in the report with
the reason, an end-of-life line for one, rather than making it inside another
task.

## A database keeps its major

A service that keeps data — Postgres, MySQL, Redis with persistence — stays on
the major and the distribution its volume was created with: a floating tag
already in the file is pinned to the newest release inside that major. A new
major, or a move between Debian and Alpine, is a data migration — on-disk
format, collation — so ask before making it.

On Debian the tag names the Debian release as well, `postgres:<x.y>-<codename>`:
a new release brings a new glibc, which sorts text differently. The updater
stops at the end of that release on purpose; moving on is the same migration.

A new database service takes the major and distribution of the production
database it stands in for, when there is one — Alpine in dev against a glibc
database in production sorts text differently. With none, it is the newest
major on Alpine.

## The smallest base that runs the app

The final stage uses the first row that works:

| The app is | Final stage |
| --- | --- |
| A static binary — Go with `CGO_ENABLED=0`, Rust on musl | distroless `static-debian<N>:nonroot@sha256:<digest>`, newest Debian it publishes |
| Node, Python, Ruby, a service in compose | the `-alpine` variant |
| A dependency ships glibc-only binaries | the `-slim` variant, with a comment naming that dependency |

Check the dependency before settling on Alpine — a Python wheel without a
`musllinux` build, a Node addon with glibc-only prebuilds — rather than
assuming either way.

The full image belongs in a build stage, and only when the build needs its
toolchain. Build there, copy the artifact into the final stage.

`scratch` has no CA certificates and no non-root user; use it only when the
binary makes no TLS calls and you add a `USER` yourself.

## `COPY . .` ships with a `.dockerignore`

A Dockerfile that copies the whole context, or a directory of it, has a
`.dockerignore` at the context root — written in the same change, not suggested.
A `<Dockerfile-name>.dockerignore` beside the Dockerfile replaces the root one
for that build rather than adding to it, so edit the one the build reads. It
excludes at least:

- `.env*` and every other file holding secrets, leaving `.env.example` in
- `.git`
- installed dependencies — `node_modules`, `.venv`
- local build output — `dist`, `build`, `coverage`

Then read it the other way: a broad pattern such as `*.md` also drops files the
app reads at runtime, and those go back in with `!path`.

## The server receives SIGTERM

`docker stop` and every redeploy send SIGTERM to PID 1 and kill it ten seconds
later. A process running as PID 1 that registers no SIGTERM handler ignores the
signal, so each stop ends in SIGKILL, mid-request or mid-write. So one of these
holds for every long-running service the project builds itself — published
images such as `postgres` already handle it:

- compose sets `init: true` on it, or the image's `ENTRYPOINT` starts it under
  `tini --`
- the app handles SIGTERM itself — name the file that does in a comment

An entrypoint script ends with `exec <server> "$@"`, so the server, not the
shell, is the process that gets the signal.

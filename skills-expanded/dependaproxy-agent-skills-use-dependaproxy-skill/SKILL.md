---
name: use-dependaproxy
description: Use when installing language dependencies (npm, pip/uv/PDM, Go modules) in an environment whose only route to a package registry is a DependaProxy instance — including installing a committed lockfile (uv.lock / pdm.lock / package-lock.json) whose artifact URLs point at the public registry. Covers the three registry prefixes, the validation gates and what a 403 means, the per-ecosystem client config, and the reversible lockfile-URL rewrite that lets `uv sync --frozen` (and PDM/pnpm) install through the proxy without de-canonicalizing the committed lock.
---

# Use DependaProxy

DependaProxy is a **supply-chain-validating** package proxy. Every artifact it
serves has been fetched from the real upstream, checked against a middleware
chain (minimum publication age, known-CVE, malware heuristics, provenance),
hashed, and is re-verified against that hash on every serve. One instance fronts
several ecosystems, segregated by URL path prefix:

| Ecosystem | Prefix | Points a client's… |
|---|---|---|
| npm | `/npm` | registry URL at `<proxy>/npm` |
| PyPI | `/pypi` | index URL at `<proxy>/pypi/simple` |
| Go modules | `/goproxy` | `GOPROXY` at `<proxy>/goproxy` |

In the ai-sandbox stack the proxy is `http://dependaproxy:8080` and the public
registries are **network-blocked** — a client that bypasses the proxy fails with
a connection error. Do not try to work around the block; route through the proxy.

## The validation gates — what a 403 means

A `403` from the proxy is a **deliberate rejection**, not a transient error. The
body names the class. The common ones:

- **`min-publication-age`** — the release is younger than the configured
  threshold (7 days for Go, 3 for npm/pypi in the sandbox). Pick an older
  version. For `uv`, pin resolution with `[tool.uv] exclude-newer` so the whole
  lock clears the gate.
- **`cve-check` / `cve-check-retrieval`** — the package (or a transitive Go
  module) has an OSV advisory. `cve-check-retrieval` re-checks on **every**
  serve, so a package that installed yesterday can start 403ing when a new CVE
  lands. Move to a fixed version, or (Go) bump the offending module.
- **`malware-scan` / `guarddog-scan`** — usually `warn` (served + logged), not
  `deny`. A `deny` here is rare and worth surfacing to the user.

Read the reason, change the version, retry. Never try to defeat the gate.

## Per-ecosystem client config (DinD workload containers)

The ai-sandbox entrypoint writes three config files to `/workspace`
(auth disabled in that stack, so they carry no token). The nested DinD daemon
cannot resolve the compose name, so every workload container also needs
`--add-host=dependaproxy:172.23.0.10`.

```sh
# npm — mount the generated .npmrc, run as uid 1000
docker run --rm -u node -v /workspace:/work -w /work \
  -v /workspace/.npmrc:/home/node/.npmrc:ro --add-host=dependaproxy:172.23.0.10 \
  node:22-alpine sh -c 'npm install && npm test'

# pip — pass the generated pip.env (PIP_INDEX_URL + PIP_TRUSTED_HOST)
docker run --rm -v /workspace:/work -w /work \
  --env-file /work/pip.env --add-host=dependaproxy:172.23.0.10 \
  python:3-alpine sh -c 'pip install -r requirements.txt && python script.py'

# Go — pass the generated go.env (GOPROXY). Module checksums are still verified
# against sum.golang.org directly (that host is intentionally not blocked).
docker run --rm -v /workspace:/work -w /work \
  --env-file /work/go.env --add-host=dependaproxy:172.23.0.10 \
  -e GOMODCACHE=/work/.gocache/mod -e GOCACHE=/work/.gocache/build \
  golang:1-alpine go test ./...
```

See the `use-docker` skill for the full DinD run pattern and file-ownership rules.

## Installing a committed lockfile through the proxy

A lock-driven installer fetches each artifact from the **absolute URL baked into
the lock**, not from the configured index. `uv sync --frozen` ignores
`UV_DEFAULT_INDEX` / `--index` / `--find-links` entirely and goes straight to the
`files.pythonhosted.org` URL; `--locked` re-resolves and aborts. So a committed
`uv.lock` cannot be installed behind the proxy as-is — **and re-locking against
`<proxy>/pypi/simple` rewrites every URL to a proxy URL, which then breaks CI and
anyone with direct PyPI access.**

### PyPI — the `/pypi/upstream/` alias (reversible URL rewrite)

The pypi adapter serves `GET /pypi/upstream/{host}/{path...}` as an alias for
`/pypi/files/{name}/{version}/{filename}` (`upstream_alias`, default on). `{host}`
must be in the registry's upstream allowlist; the path prefix is decoration and
is never fetched; the bytes go through the **same trust flow** as `/pypi/files/`.
So converting a canonical lock to a proxy lock — and back — is one `sed`:

```sh
cp uv.lock /tmp/uv.lock.bak
sed -i 's#https://files\.pythonhosted\.org/#http://dependaproxy:8080/pypi/upstream/files.pythonhosted.org/#g' uv.lock
UV_DEFAULT_INDEX=http://dependaproxy:8080/pypi/simple uv sync --frozen --all-extras
cp /tmp/uv.lock.bak uv.lock          # restore BEFORE any git operation
```

- `UV_DEFAULT_INDEX` is still needed — only to resolve `[build-system] requires`
  (e.g. hatchling); build-backend deps are not in `uv.lock`.
- `uv` still verifies every download against the **canonical sha256 in the lock**,
  so pointing at the proxy does not weaken the trust anchor.
- The inverse: `sed -i 's#http://dependaproxy:8080/pypi/upstream/#https://#g' uv.lock`
- Prefer a git clean/smudge filter so the **committed lock stays canonical**:
  ```
  # .gitattributes
  uv.lock filter=dependaproxy
  ```
  ```sh
  git config filter.dependaproxy.clean  "sed 's#http://dependaproxy:8080/pypi/upstream/#https://#g'"
  git config filter.dependaproxy.smudge "sed 's#https://files\.pythonhosted\.org/#http://dependaproxy:8080/pypi/upstream/files.pythonhosted.org/#g'"
  ```
- **Auth:** if the proxy has `auth.token` set, add a `.netrc` entry for the proxy
  host — never bake `user:token@` into the committed lock.
- **PDM** (`static-urls = true`) has the same shape: the same `sed` on `pdm.lock`.

### npm — nothing to add

`/npm/{pkg}/-/{file}.tgz` already mirrors `registry.npmjs.org/{pkg}/-/{file}.tgz`,
so `package-lock.json`'s `resolved` URLs work after:

```sh
npm config set replace-registry-host always     # rewrites resolved URLs to the configured registry host
```

### Go modules & pip hash-pinning — nothing to add

`go.sum` records hashes, not URLs, and `GOPROXY` *is* the redirect. pip
`--require-hashes` / pip-tools `--generate-hashes` pin `name==version` + hashes
and resolve through whatever index is configured. All install through the proxy
unchanged.

## Regenerating a lock / adding a dependency

Resolution (`uv lock`, `npm install <pkg>`, `go get`) goes through the proxy like
anything else, so a package that fails a gate fails the resolve. That is working
as intended — pick a version that passes. Commit the lock with its **canonical**
(public-registry) URLs; the rewrite above is only for install time.

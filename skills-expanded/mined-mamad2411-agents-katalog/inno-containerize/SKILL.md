---
name: inno-containerize
description: Use when writing or editing the Dockerfile for an app repo. Encodes the exact contract the platform's container gate requires (non-root, port 8080, patched base, CVE-clean image) for ANY stack, with reference recipes.
---

# inno-containerize

## Version gate: do this first

Before anything else in this skill, do these five steps in order.

1. If no `inno-platform` tools are available at all, the platform address is
   probably unset. Tell the user to open their platform's panel, copy the
   configure command from its Connect Claude Code card, run it in a terminal,
   and restart Claude Code. Then STOP.
2. Read the `version` field of `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`
   and call the `get_platform_status` MCP tool with it as `plugin_version`.
3. If the `Plugin:` line says `OUTDATED`, `version not reported`, or
   `reported version is not a MAJOR.MINOR.PATCH triple`, STOP. Tell the user
   to run the commands that line gives, then restart Claude Code and start
   again. Do not continue on a stale plugin: its guidance may describe
   platform behavior that no longer exists. If there is no `Plugin:` line at
   all, the platform sets no minimum version: go on to the next step.
4. If the `Plugin:` line says `current` and adds that a newer version
   `is available`, that is advice, not a block. Mention it once, with the
   commands from the `Update commands:` line, and go on to the next step.
5. If the status has no `Template repo:` line, the platform is older than
   v0.15.8. Say so, ask the user's admin to upgrade it, and STOP before any
   step that needs an instance value. Never fall back to a literal value.

Carry on.

**Container-type apps only.** This skill is for the `container` deployment
type, and applies equally to `mcp-container`: an mcp-container image follows
this exact same Dockerfile contract, plus it serves `POST /mcp`. A
**`function`-type** app (its own Cloudflare Worker behind the gateway)
has **no Dockerfile**: the container CI gates below are skipped for it, and
its entry is `app/index.ts`, not a container image (see `get_app_contract`
§1.1 and `inno-platform-conventions`). If the app is function-shaped (`function` or `mcp-function`), skip this
skill entirely.

**Fetch the contract first:** call the `get_app_contract` MCP tool with
`sections: ["2", "4.1"]` (add `"1.3"` for an mcp-container app). Section 2's
R1, R2, R7 and R8 state exactly the rules this skill applies, §4.1 is the
base-image policy, and the answer opens with the platform's current
digest-pinned recommended base images. If `get_app_contract` refuses the
arguments, or the platform is older than v0.16.14, call it with no
arguments and read the sections needed from the whole contract.

The `container` CI job builds your Dockerfile with **no deploy credentials
present** (an app author fully controls this build's inputs, and nothing of
platform value is reachable from it), then runs four checks: a Trivy image
scan, a non-root-user assertion, an `EXPOSE 8080` assertion, and a
**`GET /healthz` smoke test** against the built image. Every check that runs
must pass before `deploy` will run. Only the Trivy scan can be turned off: an
admin can set `safety.gate.trivy` off for an app (`get_config` says what that
costs), and the job then skips the scan and prints a loud
`SAFETY GATE DISABLED` warning instead. The other three checks always run.
A CycloneDX SBOM of the built image is uploaded whatever the gate's setting,
so turning the gate back on restores sweep coverage with no new deploy.

After the smoke test the job also writes reports, which are not among those
checks (R8 says which apps get which). The **Dockerfile misconfiguration
report** is advisory in every mode: a finding there is a Dockerfile fix to
offer, never a red job. A `container` app's accessibility report can fail
the job only when an admin has set the app's `safety.a11y.mode` to
`enforce`; its response-header report runs in the same scan and is advisory
in every mode. `inno-safety-preflight` §1c is where both are read.

The image the gates scanned is the image that ships (§4.1): nothing rebuilds
your Dockerfile at deploy time. Each run still builds its own image, though,
so the tag run's scan can see a different image than the push preflight did
when the base tag floats or upstream packages changed in between: pin the
base to the digest `get_app_contract` serves.

## The contract: identical for every stack

1. **Listen on `0.0.0.0:8080`** and declare `EXPOSE 8080`: the gate
   inspects `Config.ExposedPorts` for literally `"8080/tcp"`, and the
   gateway forwards traffic there regardless. Binding `127.0.0.1` is the
   classic "works locally, unreachable in the container" bug.
2. **Non-root `USER` before `CMD`**: the gate is an allowlist on the part of
   `Config.User` before any `:` (the group is not checked), and R1 states it
   exactly. It accepts a plain decimal uid from 1 to 2147483647 (`USER 1000`,
   `USER 65532:65532`), or a portable user name (letters, digits, `.`, `_`
   and `-`, not starting with `-`) on exactly one line of the image's own
   `/etc/passwd`, where that line's uid is such a number. Everything else is
   refused, `root`, uid 0 (leading zeros count, so `USER 00` is uid 0) and
   an unset `USER` among them. On `scratch` or any base without a passwd
   file, use a numeric uid (`USER 65532`). Switch user *after* your last
   root-requiring `RUN`.
3. **CVE-clean image**: patch the base's OS packages in the build
   (`apt-get upgrade` / `apk upgrade`) so the Trivy gate passes; a stock
   base commonly ships fixable CVEs that have nothing to do with your code.
4. **`GET /healthz` answers exactly 200.** A **hard CI gate**, not a nicety,
   and this item is the plugin's one home for the probe clocks (`inno-ship`
   points here). There are three separate clocks, and R2 states each one
   exactly:
   - **The CI smoke gate.** The `container` job runs the built image
     (`docker run -d -p 8080:8080`) and polls `/healthz` 18 times, 5 seconds
     apart, with a 4 second per-try timeout: about 90 seconds if the port
     refuses outright, up to about 162 seconds if it accepts the connection
     and then hangs. It requires **exactly 200**, and so does the runtime
     probe: a 204, and any 3xx, fail both, so a framework that redirects
     `/healthz` to `/healthz/` fails both. Anything else, or no answer at
     all, and it dumps the container logs and fails the job, which fails
     `deploy`.
   - **The runtime health probe.** It binds to the same endpoint after every
     deploy: immediately on each green one, then on the configured interval
     (`health.probe_interval_hours`, which `get_config app=<name>` shows). It
     presents a credential chosen by the app's perimeter, which is why
     `/healthz` must not depend on the caller. The probe a deploy fires, and
     an hourly pass within 10 minutes of a deploy finishing, never judge a
     failure: they defer every unhealthy result and notify no one, so
     `app_status` reading `Health: re-probe pending (not answering yet: ...)`
     is normal right after a deploy (see `inno-ship`), and a deploy that
     leaves `/healthz` failing alarms within about 70 minutes, not at once.
     The hourly floor applies only while a status is pending: once it
     clears, the recurring check goes back to following
     `health.probe_interval_hours`, so it is not always literally daily.
   - **One probe verdict.** Each attempt allows 45 seconds, and a failing
     one gets a single retry 5 seconds later, so a verdict can take up to
     about 95 seconds. That span is neither the hourly re-probe nor
     `health.probe_interval_hours`.

   Size the boot to answer inside that first 45 second attempt; a second
   attempt follows 5 seconds later, and nothing follows it. Keep it cheap and
   **storage-independent**: a slow app boot is legitimate, but a `/healthz`
   that waits on storage is not. Never stub it as a TODO.
5. **Keep build inputs where the gates allow them.** Put the app's code and
   manifests under `app/` (an `app/src/` is fine); a repo-root `src/` is
   platform-owned and the `config-integrity` gate fails any file in it. The
   two that bite a Dockerfile author specifically: never commit a `.npmrc`
   anywhere, `app/.npmrc` included, even for a container build that would use
   it, and never commit a symlink that points at a **directory**, anywhere in
   the repo, dangling ones included (a link to a *file* is fine). Copy the
   real directory in, or produce it during the image build. The full
   forbidden-path list is R7; the plugin's copy, with the reason for each, is
   `inno-platform-conventions`' **Files you must not touch** section.

**Base image: use the digest-pinned recommended bases (python/node/go) that
`get_app_contract` serves; never hard-code a digest from this skill,
documentation, or memory.** Any base that passes these checks is allowed;
the recommendations are simply known-good.

**Runtime config never lives in the image.** App-level values (API keys,
base URLs) arrive as real environment variables from the platform's
Variables facility (`set_app_variable` / the app page's Variables tab).
Never `ENV`/`ARG` a secret into the committed Dockerfile: the image is
built in CI from the repo, so a baked-in value is a committed one, and
gitleaks fails the build.

**The Dockerfile is scanned too.** The `sast` gate's semgrep run covers the
whole repository, not only `app/`, because the docker build context is the
repo root: the Dockerfile and any root-level file it `COPY`s are checked. R8
states the exact scope, and what it skips.

## Reference recipe: Python (the platform's tested stack)

This is the template's Dockerfile; it ships in the template repo's scaffold (the `Template repo:` line of the
status you read in the Version gate) that a container app is created from.

```dockerfile
FROM python:3.12-slim          # or the current pinned ref from get_app_contract
RUN apt-get update && apt-get -y upgrade && rm -rf /var/lib/apt/lists/*

WORKDIR /app
# Install pinned deps first (layer caching), then copy app/ WHOLE: a missing
# templates/ dir is a common runtime 500 (Jinja2Templates raises at import).
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ .

RUN useradd -m appuser
USER appuser

EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8080/healthz').status==200 else 1)"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

For a Node app, or a Go app built in stages so that only the runtime stage
ships, start from the sketches in `references/node-and-go.md`.

## Local sanity check before pushing

When Docker is available locally and you want the Dockerfile checked before
a push, run the block in `references/local-check.md`. It builds the image,
decides the non-root rule exactly the way the CI gate does (item 2), checks
`EXPOSE 8080`, and runs the `/healthz` smoke gate with CI's clocks (item 4),
printing one `OK:` or `FAIL:` line for the user and for `/healthz`; the
`EXPOSE` check prints the `8080/tcp` entry, or nothing when it is missing.

That block scans nothing. The image CVE scan is the `container` job's alone:
do not run an image scanner locally, because `inno-safety-preflight`'s house
rule is never to install or run scanners locally (a local result drifts from
CI's pinned scanner and knows nothing about the admin's central ignores or the
`safety.gate.trivy` toggle). Push to the default branch instead, which runs the
real scan and deploys nothing (`inno-safety-preflight`).

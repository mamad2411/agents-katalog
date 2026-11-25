---
name: cgagentharness-gotchas
description: Diagnose misleading Harness install, packaging, browser, toolchain, sandbox, CI or release results.
---

# Diagnose misleading results

Use the symptom that matches the failure. Shared invariants, deliberate boundary
copies, boolean semantics, CSRF names and write gates are owned by the **Traps**
section of `AGENTS.md`; investigate that contract rather than copying it here.
Paths below are relative to the repository root.

## Wrong compiler or slow debug crypto

Resolve Cargo, rustc and Clippy through rustup and the relevant root/desktop
`rust-toolchain.toml`. Check actual paths and versions before using the `CLIPPY`
override in `scripts/verify-local.sh`; a Homebrew override must match the compiler.
For incompatible cached artifacts, use a task-specific `CARGO_TARGET_DIR` before
changing source. Preserve `[profile.dev.package."*"] opt-level=3` in `Cargo.toml`:
slow debug scrypt is not a reason to lower its security cost.

`verify-local.sh` runs the full local suite and packaged-backend checks; use
scoped commands for ordinary changes as `AGENTS.md` requires. Its successful exit
can include skipped cargo-deny or live checks: read the output before claiming
coverage. Blank planner keys for synthetic tests; their presence proves nothing.

## Console Chrome versus /browse Chrome

For console CI, inspect Chrome resolution in `.github/workflows/ci.yml` and
`scripts/chat-browser-acceptance.mjs`. For `/browse`, inspect the browser
child, sidecar path, prepared Playwright, installed Chrome and local model.
The packaged app needs an absolute `browser.sidecar` path. Distinguish launch,
policy refusal, operator hand-off and model outcome. See the Browser use guide
linked from `AGENTS.md`.

## Sidecar digest, signatures and native UI

Use `cgagentharness-release` for the packaging order and provenance checks.
Re-signing the backend after its hash is embedded in the desktop invalidates
that identity. Ad-hoc signatures do not establish notarization. HTTP/browser
success does not establish WKWebView focus, dialogs or native navigation.

## Sandbox denial or a shared listener

Locate the failure before changing policy: an outer sandbox can reject process
or listener creation before application assertions run. Reproduce with an owned
temporary `CGAGENTHARNESS_HOME` and unique port when authorized. On Linux, missing or unusable bubblewrap refuses by default. Record the
selected backend: `linux-netns` is opt-in and isolates only the network.
Keep required sandbox checks failing when confinement is unavailable.

A response on the default port can belong to another checkout. Record the
candidate PID, binary and owned listener; stop only processes started by this
verification. See `scripts/smoke-ollama.sh` and `cgagentharness-verify`.

## Ephemeral ports and successful early exit

`free_port` in `scripts/test-desktop-backend.py` closes its reservation before the
child can bind, so the returned port is advisory. `src/server/mod.rs` checks
`port_in_use` before loading provider keys and returns success after printing an
already-running notice to stdout. Exit zero can therefore mean the credential
refusal under test never ran.

Inspect `await_headless`, `serve_expecting_refusal` and their callers. Retry only
an identified collision on a fresh port, with a bounded attempt count; preserve
captured output across attempts so a credential leak cannot disappear. Where
possible, keep the fixture listener open, as `ModelFixture` and
`test_unrelated_listener_is_never_adopted` do. Recheck every caller moved onto a
shared helper, not just the originally failing one.

## GitHub pagination and reviews

`github.rest.issues.listComments` returns an object with `data`;
`github.paginate(github.rest.issues.listComments, ...)` returns the array itself.
Inspect consumers when changing pagination. Exercise the extracted workflow
script with a marker on page two; optional chaining would conceal a broken
consumer. Current examples live in `.github/workflows/pr-template-check.yml`.

Green CI does not prove the current head was reviewed. Compare the reviewed SHA,
unresolved threads and `.github/workflows/review-gate.yml`. The gate is advisory;
thread resolution alone fires no webhook, so re-run it after resolving the final
thread when that workflow is authorized. A cancelled review is not a verdict.

## Operator command differs from API or YAML

Trace the console dispatcher and help in `src/server/views.rs`. For example,
`gateMap` in `assets/static/harness.html` maps `/memory auto-retrieve` to
`auto_retrieval` at `POST /api/structured-memory/gates`. Verify exact paths,
fields and aliases in the revision being documented.

## Release already in flight

Before an authorized release dispatch, inspect runs, tags and draft/published
releases. Watch an existing release for the same SHA rather than dispatching a
duplicate. `scripts/release-plan.py` deliberately rejects collisions; preserve
the tag/assets after an ambiguous result. See `cgagentharness-release` for the
exact-main Bundle prerequisite and publication acceptance.

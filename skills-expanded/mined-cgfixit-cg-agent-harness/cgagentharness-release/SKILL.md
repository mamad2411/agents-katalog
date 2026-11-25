---
name: cgagentharness-release
description: Build and verify macOS Harness release artifacts, native acceptance and GitHub workflow provenance.
---

# Release the macOS desktop

Follow `AGENTS.md`; read the README-linked `docs/DESKTOP.md`, `docs/RELEASING.md`,
`scripts/package-desktop.sh`, `scripts/verify-desktop-bundle.sh` and the current
desktop, Bundle and release workflows. Package committed source so `Resources/COMMIT`
is meaningful; identify the release version as well as the source SHA.
`CGAH_ALLOW_DIRTY=1` is only for marked development artifacts.

Build on Apple Silicon macOS with installed Xcode CLT and rustup toolchains from
both toolchain files. Install `aarch64-apple-darwin` and `x86_64-apple-darwin`
standard libraries for both toolchains before a universal build. Use rustup Cargo
on PATH. Run `scripts/package-desktop.sh --universal` (optional `--dmg`).

The critical order is backend slices -> lipo -> sign universal backend -> compile
both desktop slices embedding that exact whole-file SHA256 -> lipo desktop -> sign
shell/bundle. Never re-sign the sidecar after its digest is embedded. The backend
remains a separate child; native commands must not become browser capabilities.

Verify the ZIP checksum, extract to a fresh directory with spaces, and run
`scripts/verify-desktop-bundle.sh '<extracted app>' universal '<release version>'`.
Verify the bundled version matches the planned release and both executables
contain arm64 and x86_64, nested signatures, resources and system-only linkage.
Run `scripts/test-desktop-backend.py` with `CGAH_TEST_BINARY` set to the packaged
backend. Check desktop policy and both `cargo deny` configurations.

Launch the actual app with a disposable `CGAGENTHARNESS_HOME`, distinct from any
operator home. Record PID, owned backend/listener, chat and shutdown. Exercise
WKWebView and the external browser console separately. If testing `/browse`,
point `browser.sidecar` at a prepared absolute path outside the bundle.
Intel cross-compilation, Rosetta execution and native Intel testing are different
claims. Do not silently install Rosetta or change TCC settings to fill an evidence gap.

Match remote SHA, workflow run, artifact COMMIT and checksums.
`desktop-check.yml` compiles PRs; Bundle and release call reusable `desktop.yml`.
Use an authorized desktop dispatch for an unmerged artifact. Automatic/manual
publication requires main and successful Bundle at that SHA. Inspect runs, tags
and releases before dispatch; the planner rejects prerelease tags.
Publication follows explicit user authorization. Never overwrite release assets
or tags after an ambiguous result.
Report the trust limit: ad-hoc signing and same-release checksums establish
integrity without Developer ID, notarization or independent publisher proof.

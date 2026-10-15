---
name: attestation
description: "Verify, download, and inspect build provenance attestations using the orbit CLI. Use this skill whenever the user asks about verifying attestations, checking provenance, inspecting Sigstore bundles, SLSA provenance, build provenance, verifying binaries, downloading attestation bundles, signer identity, in-toto attestations, or supply chain security. Trigger on phrases like 'verify attestation', 'check provenance', 'inspect bundle', 'build provenance', 'sigstore', 'SLSA', 'verify binary', 'attestation download', 'download bundle', 'check signer', 'inspect attestation', 'provenance verification', 'verify artifact', 'supply chain verification', 'check build origin', or any attestation-related task — even casual references like 'is this binary legit', 'who built this', 'where did this artifact come from', 'check the bundle', or 'show provenance'. The orbit CLI alias for attestation is `attest`."
---

# Attestation with orbit CLI

Verify, download, and inspect build provenance attestations using Sigstore bundles with in-toto attestation format and SLSA provenance predicates. This feature supports supply chain security by letting you confirm artifact origin, signer identity, and build metadata.

## Prerequisites

1. `orbit` CLI installed — if `which orbit` fails, install with:
   - **macOS/Linux (Homebrew):** `brew install jorgemuza/tap/orbit`
   - **macOS/Linux (script):** `curl -sSfL https://raw.githubusercontent.com/jorgemuza/orbit/main/install.sh | sh`
   - **Windows (Scoop):** `scoop bucket add jorgemuza https://github.com/jorgemuza/scoop-bucket && scoop install orbit`
2. A Sigstore attestation bundle (`.jsonl` or `.json`) for the artifact you want to verify or inspect
3. For `download`: a profile with a GitHub service configured (attestation bundles are fetched from GitHub)

## Quick Reference

All commands follow the pattern: `orbit attestation <command> [arguments] [flags]`

Alias: `orbit attest <command> [arguments] [flags]`

All commands support `-o json` and `-o yaml` for structured output. For full command details and all flags, see `references/commands.md`.

## Core Workflows

### Verifying an Artifact

Verify that an artifact matches its attestation bundle, confirming build provenance, signer identity, and source repository.

```bash
# Verify a local binary against a bundle
orbit attestation verify ./my-binary --bundle attestation.jsonl

# Verify with owner and signer identity checks
orbit attest verify ./artifact --bundle bundle.json --owner my-org --signer-identity "github.com/my-org/my-repo"

# Verify a pre-computed digest
orbit attestation verify abc123def456... --bundle att.json --digest-algorithm sha256

# Output verification result as JSON
orbit attestation verify ./my-binary --bundle att.json -o json
```

### Downloading an Attestation Bundle

Fetch the attestation bundle for an artifact digest from a GitHub repository.

```bash
# Download attestation bundle by digest
orbit attestation download sha256:abc123... --repo owner/repo

# With explicit digest algorithm
orbit attest download abc123... --repo owner/repo --digest-algorithm sha256
```

### Inspecting a Bundle

Display the full contents of an attestation bundle, including SLSA provenance, signer identity, builder, source, and materials.

```bash
# Inspect a bundle file
orbit attestation inspect attestation.jsonl

# Output as JSON for processing
orbit attest inspect bundle.json -o json
```

## Common Patterns

**Verify a release binary end-to-end:**
```bash
# Download the attestation bundle
orbit attestation download sha256:abc123... --repo my-org/my-repo

# Verify the binary against the downloaded bundle
orbit attestation verify ./my-binary --bundle attestation.jsonl --owner my-org

# Inspect the bundle for detailed provenance info
orbit attestation inspect attestation.jsonl
```

**Get JSON for scripting:**
Any command supports `-o json` for machine-readable output:
```bash
orbit attestation verify ./my-binary --bundle att.json -o json | jq '.signer'
```

**Check who signed an artifact:**
```bash
orbit attestation inspect bundle.json -o json | jq '.signer'
```

**Verify with strict signer identity:**
```bash
orbit attest verify ./artifact --bundle bundle.json \
  --owner my-org \
  --repo my-org/my-repo \
  --signer-identity "github.com/my-org/my-repo/.github/workflows/release.yml"
```

## Important Notes

- **Sigstore format** — Attestation bundles follow the Sigstore bundle specification. Verification uses the in-toto attestation format with SLSA provenance predicates.
- **Digest algorithms** — Supported algorithms are `sha256` (default) and `sha512`. Use `--digest-algorithm` to specify.
- **Profile for download** — The `download` command requires a profile with GitHub access (`-p <profile>`) since it fetches bundles from GitHub repositories. The `--repo` flag is required.
- **Local-only commands** — The `verify` and `inspect` commands work with local files and do not require a profile or network access (unless fetching a bundle).
- **Output formats** — All commands support `-o json` and `-o yaml` for structured output suitable for scripting and CI pipelines.

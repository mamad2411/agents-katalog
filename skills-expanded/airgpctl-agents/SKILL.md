# airgapctl — Agent Guide

## Project

`airgapctl` is a Go CLI that loads Replicated `.airgap` bundles into a private registry and generates a Helm values file mapping images to their new paths. It replaces a manual docker save/load/retag/push + hand-edit workflow.

- **Language**: Go (single static binary, zero runtime dependencies)
- **Bundle format**: Docker distribution v2 registry-on-disk layout (`.airgap` files)
- **Reference implementation**: `github.com/replicatedhq/vandoor/airgap-builder/`

## Key Constraints

- Must push images **directly from the on-disk layout** — no temporary `registry serve` process. The binary must be self-sufficient in air-gapped environments.
- Must handle **multi-arch manifest lists** correctly (push list + all platform manifests).
- Pushes must be **idempotent**: already-present images are skipped without error.
- `airgap.yaml`'s `SavedImages` contains raw image names; the tool must resolve actual repository paths within the Docker v2 directory.

## Development Workflow

The `ralph` script in the repo root is the iteration driver. It loops OpenCode sessions until the PRD is complete. A typical session follows this order:

1. **Read** `docs/brainstorms/2026-05-14-airgapctl-requirements.md` (PRD) and `docs/progress.md`.
2. **Pick** the highest-priority unfinished task from `progress.md`.
3. **Implement** using the `ce-work` skill, **test-first**, with strict RED-GREEN-REFACTOR on a per-test basis.
4. **Commit** the implementation.
5. **Review** using the `ce-code-review` skill and LFG the fixes.
6. **Commit** the review fixes.
7. **Capture learnings** with the `ce-compound` skill and update all suggested documents.
8. **Update** `docs/progress.md` with what changed.
9. **Commit** the docs/progress updates.

## Architecture Notes

- **Entrypoint**: Standard `main` package CLI (to be created).
- **Core packages** (expected):
  - Bundle extraction and `airgap.yaml` parsing.
  - Docker distribution v2 directory traversal and manifest resolution.
  - Registry push logic (direct from disk, multi-arch aware).
  - Values file generation (configurable path template, chart-aware partial matching).
- **Default output**: `images.yaml` (overridable via flag).
- **Deferred scope**: Downloading `.airgap` from S3/OCI, Replicated API auth, embedded cluster bundles, incremental/diff bundles.

## Commands & Conventions

- No build/test/config files exist yet. When creating the Go module, prefer:
  - `go mod init github.com/replicatedhq/airgapctl`
  - `go test ./...` for the test suite.
  - Table-driven tests for parser/push logic.
- When generating values files, the mapping template must be user-configurable for `{registry}/{namespace}/{name}:{tag}`.

## Files That Matter

- `docs/brainstorms/2026-05-14-airgapctl-requirements.md` — PRD, acceptance examples, scope boundaries.
- `docs/progress.md` — Live task tracker. Update after every session.
- `ralph` — Iteration driver script. Do not break its contract (reads PRD + progress, expects `<promise>COMPLETE</promise>` when done).

## Common Mistakes to Avoid

- Do **not** assume `docker` or `registry` binaries are available at runtime. Push must be pure Go.
- Do **not** implement deferred scope (downloading bundles, Replicated API auth).
- When parsing `SavedImages`, remember the raw name may not be fully qualified — map it to the actual on-disk manifest path.
- When generating values, match against the target Helm chart's image references (partial matching), not just a flat dump of all bundle images.

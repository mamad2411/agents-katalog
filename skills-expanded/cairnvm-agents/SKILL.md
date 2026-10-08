# Agent Guide

## Scope and authority

These rules apply repository-wide; a deeper `AGENTS.md` may add stricter rules.
`Docs/Architecture-Spec.md` is the normative design authority. Treat
`Docs/Architecture-Draft.md` as historical context only. If code and the
normative specification disagree, stop and resolve the discrepancy explicitly.

The repository is a Phase 0 scaffold. Do not describe Drive persistence,
encryption, checkpointing, recovery, or verified bootstrap as implemented until
their roadmap gates have passed.

## Required workflow

1. Write or update a failing test before behavior changes.
2. Make the smallest change that passes it.
3. Run `make lint typecheck test`; run `make security` when dependencies change.
4. Stage only the intended files after reviewing the exact diff.
5. Run `make check` against that exact staged candidate; it rejects tracked drift
   and nonignored untracked files. Then run `make scan-staged` before every commit.
   If either requires a correction, restage the exact files and repeat both staged
   gates.
6. For architecture, trust-boundary, durable-format, recovery, security, or agent-
   guidance changes, obtain an independent adversarial subagent review of the
   exact staged candidate. Approval means the reviewer reports no negative finding.
   Otherwise revise, then repeat the local checks, staging, both staged gates, and
   review until it does.
7. Commit the tested and, when required, reviewed implementation. When a Phase 0
   gate is exercised, create a single-parent follow-up evidence/status commit that
   adds exactly one new complete Phase 0 evaluation TOML file and changes
   `ROADMAP.md` only when the aggregate phase status changes. It may change no
   other path. Repeat both staged gates, then obtain an independent review of the
   exact staged evidence/status candidate. The reviewer must manually confirm the
   tested implementation commit's full SHA, that the evaluation's `tested_commit`
   and `exact_parent` both equal the candidate's sole parent, publication-branch
   binding, allowed-path scope, append-only history, timestamp and trusted-clock
   ordering, completeness, aggregation, redaction, and no negative finding.
   Confirm that the publication branch blocks force pushes and deletion before
   publishing the record; do not claim protected or immutable history until that
   remote setting is verified. Evidence must never claim to describe its own
   commit.

Keep commits narrow. Do not claim a test passed if its required runtime or external
service was unavailable; record it as blocked.
After two failed correction cycles on one design, stop patching it and restart
from a simpler design in a fresh task.

## Safety invariants

- Fail closed on malformed, unauthenticated, ambiguous, or unsupported state.
- Treat every Drive object and repository identifier as untrusted input.
- Never log passphrases, OAuth tokens, plaintext guest data, derived keys, or secret
  envelopes.
- Never upload plaintext guest blocks or credentials.
- Never select a concurrent-writer branch silently.
- Do not implement destructive remote garbage collection in v1.
- Preserve the launcher as an independent trust boundary. It must not import or
  depend on `cairnvm-runtime`.
- Keep tests offline and deterministic by default. Use synthetic data and fake
  services for protocol tests.

## Repository conventions

- Python 3.11+; use `uv` and the committed lockfile.
- Format and lint with Ruff, type-check with strict mypy, and test with pytest.
- Put normative protocol behavior in `Docs/Architecture-Spec.md`. Keep selected
  constants, limits, transitions, and recovery contracts that the specification
  explicitly mirrors in `Docs/architecture-state-model.toml` synchronized with
  the normative prose and exact contract tests. Put durable decisions in
  `Docs/ADRs/` and execution status in `ROADMAP.md`.
- Update `README.md` and `OVERVIEW.md` when user-visible scope changes. Update
  `ROADMAP.md` when execution or phase status changes.

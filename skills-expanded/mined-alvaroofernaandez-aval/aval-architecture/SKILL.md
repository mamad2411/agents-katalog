---
name: aval-architecture
description: "Use when adding a package, interface or seam, adding an import between internal/ packages, moving code across layers, or before and after a refactor in aval. Evidence before abstractions, the ADR 0002 allowlist, the ratchet, the generated model, optional archsieve reports."
---

## Activation contract

Load before a structural change in this repository: a new package under `internal/`, a new interface or seam, a new internal import, or a refactor that moves code. Not for runtime behaviour or performance. Where it disagrees with a global skill, this one wins (`AGENTS.md`).

## Hard rules

- **Evidence before abstractions.** A new package, interface or seam is a visible cost. Name its need before you add it: a second implementation that exists or is planned in `odd/tasks/`, a test seam a test uses, or a security or ownership boundary. "Cleaner" or "more flexible" is not a need. No need, no abstraction.
- **AS-IS and TO-BE stay separate.** AS-IS is what `go list` and `docs/architecture/model.md` show at this commit. TO-BE is your proposal, labelled as one. Never draw a proposed package or edge into the generated model.
- **The allowlist is the law.** `archRules` in `tests/architecture_test.go` implements ADR 0002 (with its 2026-11-23 amendments). A package no rule matches is itself a violation, so a new package forces a decision.
- **Change order: ADR, then table, then code.** To change the layering: (1) add a dated `### YYYY-MM-DD` amendment to ADR 0002 or write a new ADR (`docs/adr/README.md`; `tests/adr_test.go` checks it); (2) edit `archRules`; (3) write the import; (4) regenerate the model. Never rewrite the accepted ADR text.
- **The ratchet only shrinks.** `archExceptions` lists edges that break the rules today; `archMaxExceptions` caps it (0 now). A new violation fails; an exception that no longer matches also fails. Fix the import. Raising the cap is never part of a feature change.
- **archsieve is a report, never a gate.** ADR 0001: Node tooling is never a dependency, and in Go archsieve only sees import cycles, which the compiler already rejects. No test, hook or CI step may depend on it.

## The allowlist today (ADR 0002 + amendment)

| Package | May import (internal) |
| --- | --- |
| `cmd/aval` | anything under `internal/` (composition root) |
| `internal/ui` | `core/*`, `devmode`, `i18n`, `release`, `ui/caps`; `design/gate` in tests only |
| `internal/ui/cli` | `ui`, `ui/caps`, `i18n` |
| `internal/core/*` | `core/*`, `release` |
| `internal/design/hook` | `design/ack` |
| leaves: `agent/*`, `devops/*`, `term/*`, `docs/*`, `herdr/*`, `deck`, `design/ack`, `design/gate`, `release`, `devmode`, `i18n`, `ui/caps`, `testenv`, `tools/*` | nothing internal |

Everywhere: `internal/testenv` only from `_test.go` files; nothing imports `cmd/aval`. The table above is a reading aid; `archRules` is the source.

## Commands

```bash
go test ./tests/ -run Architecture                        # the gate: edges, ratchet, self-test, stale model
go test ./tests/ -run TestArchitectureModel -update       # regenerate docs/architecture/model.md
```

The gate reads `go list` for linux, darwin and windows, so build-tagged files count. A failure prints `from -> import` per edge.

## Reading `docs/architecture/model.md`

Generated; never edit it by hand (a test fails when it is stale). Families fold into one node (`core/*`, `agent/*`). A solid arrow is a production import, a dotted `test` arrow exists only in tests. The leaves subgraph is every package with no internal production import. The Rules table and the exception count are rendered from `archRules` and `archExceptions`.

## Optional: archsieve reports

Only when a diagram, the affected set or churn helps a review. Pinned tag tarball, artifacts outside the repo:

```bash
npx -y https://github.com/FullFran/archsieve/archive/refs/tags/v0.6.0.tar.gz scan . --go auto -o /tmp/archsieve/now.json
npx -y https://github.com/FullFran/archsieve/archive/refs/tags/v0.6.0.tar.gz scan . --go auto --ref main -o /tmp/archsieve/main.json
npx -y https://github.com/FullFran/archsieve/archive/refs/tags/v0.6.0.tar.gz diff /tmp/archsieve/main.json /tmp/archsieve/now.json --format md
npx -y https://github.com/FullFran/archsieve/archive/refs/tags/v0.6.0.tar.gz render /tmp/archsieve/now.json --depth 1
npx -y https://github.com/FullFran/archsieve/archive/refs/tags/v0.6.0.tar.gz affected /tmp/archsieve/now.json --base origin/main --repo .
npx -y https://github.com/FullFran/archsieve/archive/refs/tags/v0.6.0.tar.gz scan . --go auto --history --since 90d -o /tmp/archsieve/churn.json
```

- `error` findings are facts; `signal` findings are questions, not orders; `unknown` means "not inferable", never "absent".
- `affected` lists dependent files and tests; when `blind` is not empty, run the full suite.
- `--history` churn and `co-change-without-link` point at coupling imports cannot show. Treat them as questions.
- Bump the pinned tag deliberately, in its own commit. Never run archsieve unpinned.

## Evidence a PR must show

1. AS-IS: the relevant edges before the change (the model or `go list`).
2. TO-BE: the new or changed packages and edges, each with the need it answers.
3. `go test ./tests/ -run Architecture` output after the change, and the regenerated model diff if edges changed.
4. If the layering changed: the ADR amendment, in the same PR, before the `archRules` edit.
5. Optionally, an archsieve `diff --format md` excerpt, labelled as a report.

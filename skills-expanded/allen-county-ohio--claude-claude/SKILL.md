# Working in this repository

This repository's domain is **Allen County, Ohio** — a civic-reference corpus covering the
county's geography, its jurisdictions and offices, and its history from pre-statehood
through the present.

This is a yidam-derived repository: a living knowledge artifact whose git history is the
knowledge graph. It has already been bootstrapped — there is no bootstrap mode here, and
`.yidam/.vendor/prelude/skills/bootstrap.md` is history, not an instruction.

Read [AGENTS.md](../AGENTS.md) before taking substantive action. It names the prelude files
that govern conduct here and the gate that CI runs.

## The short version

- **Nodes** are files in [`.yidam/corpus/`](../.yidam/corpus/). One concept per file. Every
  node needs at least one outgoing link.
- **Sources** are files in [`.yidam/catalog/`](../.yidam/catalog/). Corpus nodes cite them by
  link rather than embedding citations inline.
- **Claims** carry `[verified]`, `[inference]`, or `[open]`. Untagged inference is a defect.
- **Edges are claims too**, and carry `claim_tag:` — plus `source:` when `verified` — on the
  link itself. `instance-of`, `concerns` and `subject-of` are structural and take no tag.
  `verified` means a catalog source supports *that relationship*, not that the node cites
  something. `mise run ci` fails on an untagged edge; run `edge-audit` to see the graph's
  provenance by class.
- **Commits** are knowledge events. Epistemic commits (understanding changed) and operational
  commits (a pipeline ran) are written in visibly different styles and never mixed.
- **`.yidam/.vendor/` is read-only.** Fix prelude defects by re-vendoring
  (`mise run yidam-vendor-update`), never by editing in place.
- **`design/upstream/` is read-only for the same reason.** It mirrors a design system this
  repository does not own. Every local difference is declared in `design/departures.md` and
  `web/test/port.test.ts` gates it both ways. Sending a finding back is
  [`design-push`](../.yidam/skills/design-push.md), and it halts for the elector.

## Before committing

```
mise run regen           # refresh REGEN blocks, then commit the result as `regen:`
mise run ci              # graph-check, graph-lint, regen --check — the whole gate
```

`mise run ci` is what CI runs, and the two are held together by `crates/publish/tests/gate.rs`
— which checks the compiler, the format-check member list and the cargo flags, because the two
once agreed on every step and ran clippy ten releases apart. Run it rather than its parts:
`graph-check` reads the graph and says nothing about a stale REGEN block, which is a failing
build all the same.

The Rust version is pinned in **two** files that must agree: `crates/rust-toolchain.toml` is what
CI and a bare clone read, and `mise.toml` is what wins locally. Bump both together; `gate.rs`
fails the build if you don't.

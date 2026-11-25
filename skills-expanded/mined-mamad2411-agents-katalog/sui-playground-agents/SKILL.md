# AGENTS.md — Sui Playground operating contract for AI agents

This is the **canonical, tool-neutral contract** for this repo. Everything else (`CLAUDE.md`,
`.github/copilot-instructions.md`) is a thin bridge that points here. If two files disagree, this
one wins.

## What this repo is

`sui-playground` is an **EVE Frontier / Sui staging, research, and agent-context workspace** — and a
launchpad for new repos. It exists to inspect upstream contracts and docs (read-only `vendor/*`
submodules), run local-devnet feasibility spikes, capture durable conventions, and hand a
context-rich starting point to a fresh downstream repo.

There is **no frontend, no backend, no npm at the repo root**. Verification is Move-shaped:

```bash
sui client active-env                 # verify the network BEFORE any transaction
sui move build --path <package-dir>   # must compile
sui move test  --path <package-dir>   # must pass
git submodule update --init --recursive
```

It was formerly the March 2026 EVE Frontier hackathon planning workspace (concluded). That material
is a **historical archive**, not current rules — indexed at
[`docs/archive/hackathon-2026/README.md`](docs/archive/hackathon-2026/README.md); its narrative
voice, deadlines, and event rules apply only inside that archive.

**New project code belongs in a separate downstream repo, created fresh — not committed here.**

## Hard safety invariants

Non-negotiable. These are the rules that have actually caused damage when broken.

1. **Never push without explicit operator approval.** A commit is not permission to push; the operator grants push per task, in the prompt.
2. **Never commit inside a `vendor/*` submodule.** Full policy below — the single most-violated rule in this repo.
3. **`~/.sui/`, `sui.keystore`, and any `.env` carrying a mnemonic or private key are secrets.** Never log, echo, print, or commit them. No secrets anywhere in the repo — use `.env.example` placeholders.
4. **Verify `sui client active-env` before any transaction.** Switching between local / testnet / mainnet silently is how you spend real money on the wrong chain.
5. **Events are not proof-of-execution.** A MoveAbort emits **no** events. Use the transaction digest plus effects as the evidence path — [`docs/ptb/proof-extraction-moveabort.md`](docs/ptb/proof-extraction-moveabort.md).
6. **Never assume an on-chain shape.** Verify function signatures, structs, events, and auth against the **current** `vendor/world-contracts` commit before generating call sites. Historical docs here reflect much older contracts — check the vendored submodule for the current version; LLM training data is worse.

## Authority hierarchy (source of truth)

When sources disagree, trust them in this order — stated here once, for the whole repo:

1. **Current `vendor/world-contracts` Move code + official upstream docs** (`docs.sui.io`, `docs.evefrontier.com`, `vendor/builder-documentation`) — canonical.
2. **Current workspace docs** — [`docs/current/`](docs/current/README.md).
3. **Validated experiments** — `docs/validation/`, `sandbox/`, `experiments/` (validated against older contracts; revalidate before relying).
4. **Historical hackathon archive** — `docs/core/`, `docs/strategy/`, `docs/architecture/`, `docs/archive/` (March 2026).
5. **Older plans / speculative docs.**

Between the two upstream doc sets: **code beats docs.** Sui chain mechanics (object model, gas,
PTBs, coins, abilities, events, limits) come from `docs.sui.io`; EVE Frontier world behavior comes
from GitBook — but if either contradicts the Move code, the code wins and you flag the discrepancy.
Don't mirror upstream doc content here — summarize and link. Reference maps:
[`sui-documentation-reference-map.md`](docs/research/sui-documentation-reference-map.md),
[`evefrontier-builder-docs-map.md`](docs/research/evefrontier-builder-docs-map.md). Chain limits
(250 KB object size, 1000 PTB commands, 1024 dynamic fields/tx, 32 struct fields, 8 Groth16 public
inputs, shared-object consensus latency, hot-potato consumption) are worth re-checking against the
SUI docs rather than recalling.

## Permission model

- ✅ **Always:** read anything (including all of `vendor/*`); run builds, tests, lints, and read-only CLI / RPC / HTTP checks yourself rather than printing them for the operator; write to `docs/` and `notes/`; use doc-lookup tools and subagents. Only stop for a secret prompt — start the command, ask the operator to paste the secret locally, then summarize.
- ⚠️ **Ask first:** Sui key material, wallet config, or signing; Docker compose state and `vendor/builder-scaffold/docker/` volumes; core API contracts, protocol definitions, or cross-system payload schemas; new external dependencies; changes spanning more than ~3 core files or ~150 LoC; transactions against a non-local network.
- 🚫 **Never:** commit secrets, certificates, or private keys; commit inside `vendor/*`; push without explicit operator approval; delete or skip failing tests to make a gate pass; store PII in any telemetry or analytics.

## Submodule & vendor policy

`vendor/*` are **third-party upstream repos** as git submodules: `world-contracts` (canonical Move
code), `builder-documentation`, `builder-scaffold`, `evevault`, `eve-frontier-proximity-zk-poc`.

⚠️ **Cross-repo blast radius:** the **ssu-open-shared-withdraw** repo's `ssu_open_claim` package depends on `vendor/world-contracts/contracts/world` via a relative path into THIS repo (that repo is checked out alongside this one). Checking out a different world-contracts commit/branch here (e.g. the v1 `dev` branch, which deletes `contracts/world`) breaks that repo's Move build with no commit over there — coordinate bumps.

🚫 **Never** create a commit inside a `vendor/` submodule (`git -C vendor/* commit` is forbidden — verify your `cwd` is the parent repo root before any git write); modify, delete, or add tracked files inside `vendor/*`; stage submodule-internal changes from the parent; or commit submodule-local Docker state, caches, or build artifacts (`docker/workspace-data/`, `.env.testnet`).

✅ **Correct patterns:** read vendor source freely. Update a pin with `git submodule update --remote vendor/<name>` from the parent root, then commit the new gitlink **in the parent** — procedure in [`docs/operations/submodule-refresh-prompt.md`](docs/operations/submodule-refresh-prompt.md). Put transient local ignores in `vendor/<name>/.git/info/exclude`. To try a change to vendor code, copy it to `sandbox/` or a scratch dir and ship a patch file. Repo-owned `Move.lock` files (`experiments/`, `sandbox/`) **are** committed for reproducible builds; vendor lockfile churn is not.

## Process rules

**Git.** Branch for non-trivial work (`feat/`, `fix/`, `docs/`, `chore/`, `spike/` + `kebab-case-description`); direct-to-`main` is fine for typos, `.gitignore`, and trivial doc fixes. Commit format `type: Imperative description` (≤72 chars). Squash-merge feature branches; never force-push `main`. `spike/` branches are throwaway — never merged.

**Decision log.** Any non-trivial technical or strategic decision gets an entry at the **top** of [`docs/decision-log.md`](docs/decision-log.md) (newest first), in the format of [`docs/operations/DECISIONS_TEMPLATE.md`](docs/operations/DECISIONS_TEMPLATE.md).

**Documentation.** New markdown goes in a categorized subfolder under `docs/` (never loose at `docs/` root); update the index in [`docs/README.md`](docs/README.md). Every doc opens with `**Retention:** [Carry-forward | Prep-only | Sandbox-only | Archive]` — *Carry-forward* copies into a downstream repo, *Prep-only* is research/planning, *Sandbox-only* is temporary devnet artifacts, *Archive* is superseded-but-kept. Default to **Prep-only** if uncertain, and say so.

**Scope discipline.** Prefer the smallest safe change; when asked for a broad refactor, propose the smallest path to the user-visible benefit first. No speculative code "for future use." No summary docs after every change — update an existing doc or report verbally.

**File discipline.** No file over ~500 lines without justification (React components ~150, page components ~100, Move modules ~500) — split at generation time, not after. No god files, no duplicate utilities (grep before creating), no generic names (`utils2.ts`, `helper.ts`).

**Validation.** Run the gates yourself (`sui move build`, `sui move test`) after any Move change. If a gate fails, diagnose and fix it, then re-run — don't hand the raw error to the operator; escalate only if your fix also fails or the call is genuinely a design decision.

**Delegate wide work.** Use subagents for multi-file changes, audits, and research sweeps; require a short summary, concrete deliverables, and risks/follow-ups from each.

**External specs.** Treat external LLM specifications as intent; validate them against repository reality, current upstream code, and these invariants before implementation.

## On-demand references

Load these when the task calls for them — not on every session.

| Topic | Doc |
|---|---|
| What the repo is today, how to use it | [`docs/current/README.md`](docs/current/README.md) |
| Current EVE Frontier cycle assumptions (revalidate) | [`docs/current/eve-frontier-context-2026-06.md`](docs/current/eve-frontier-context-2026-06.md) |
| Full documentation index + classification legend | [`docs/README.md`](docs/README.md) |
| Move conventions (auto-applied to `*.move`) | [`.claude/rules/move.md`](.claude/rules/move.md) |
| TypeScript / React / Sui SDK conventions + hallucination guards (`*.ts`, `*.tsx`) | [`.claude/rules/typescript-react.md`](.claude/rules/typescript-react.md) |
| Full repo conventions (git, naming, structure) | [`docs/core/hackathon-repo-conventions.md`](docs/core/hackathon-repo-conventions.md) |
| PTB assembly patterns (revalidate every signature) | [`docs/ptb/`](docs/ptb/) |
| Local Sui devnet operations | [`docs/architecture/sui-playground.md`](docs/architecture/sui-playground.md) |
| Submodule refresh + drift audit | [`docs/operations/submodule-refresh-prompt.md`](docs/operations/submodule-refresh-prompt.md) |
| Security baseline (OWASP) | [`.github/security-guidelines.md`](.github/security-guidelines.md) |
| Historical hackathon archive | [`docs/archive/hackathon-2026/README.md`](docs/archive/hackathon-2026/README.md) |

## Operator communication

The operator dictates prompts (WhisperTyping) — expect transcription noise, especially proper nouns
(**SWE → Sui**, **SWE Playground → Sui Playground** — two words; repo slug `sui-playground`). Full
glossary and conventions live in the machine-global `~/.claude/CLAUDE.md` and
`~/.claude/context/whisper-vocabulary.md`. If intent is genuinely unclear, ask before starting.
Anything published under the operator's name (Discord, Reddit, blog, README prose, release notes, PR
descriptions) follows [`docs/writing-style.md`](docs/writing-style.md) — Claude Code users can invoke
the `my-copy` skill instead, which carries the same material.

## Portfolio control plane

Portfolio-level state for this maintainer's projects is tracked in a private control-plane
repository, `Diabolacal/project-control`. Agents with access to it should read its record for
this project and its `NOW.md` before substantial work, and add a factual handoff there at
closeout when work materially changes project status. This repository's own code and docs remain
the authority for implementation detail. Do not copy private portfolio information, machine
paths, or secrets into this public repository.

## Closeout

End every task with: repo, branch, starting commit, final commit, pushed (yes/no), production deploy (yes/no), preview deploy (yes/no) + preview URL if relevant, files changed, validation run, known gaps, and preserved unrelated dirt + final `git status`.

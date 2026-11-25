---
name: naming
description: Names projects, tools, packages, and repositories and clears their package-registry namespaces — asking language, port, OS, and distribution questions first, then checking availability mechanically. Use when naming or renaming a project or tool, or checking a candidate name against PyPI, crates.io, npm, or Homebrew before shipping.
license: MIT
spec_hash: cf74fe441e98
metadata:
  version: "1.0.0"
---

# Naming

Name the thing, then clear its namespaces. Never search blind: the questions come first, the registry check is mechanical, and the human picks the winner.

Work with the `interaction-questioning` skill throughout — when a gating fact is missing, ask one question at a time and default to asking rather than assuming.

## The flow

1. Clarify the target (ask, don't assume).
1. Derive the gating namespaces.
1. Generate candidates (light path or council).
1. Apply the five criteria.
1. Check availability with `scripts/check-name`.
1. Resolve collisions.
1. Converge and record.

## 1. Clarify the target first

Before any word is considered, establish these — one question at a time when unstated:

- **What is it and how is it used?** CLI, library, daemon, config-driven, plugin.
- **Implementation language now** — this picks the primary publisher registry (Python → PyPI, Rust → crates.io, JavaScript → npm).
- **Any planned ports?** A Rust or Go port gates *additional* namespaces now, not later.
- **Target OS and ecosystems** — for built-in name collisions and distribution channels.
- **How will it ship?** package registry, Homebrew, git, or a dotagents/plugin install.
- **How public?** internal throwaway vs shipped-to-strangers — this decides light vs council.

Skip a question only when the answer was already given. These facts decide both which namespaces gate and which naming conventions apply.

## 2. Derive the gating namespaces

Map language + distribution to the namespaces a candidate must clear, and check **every** one:

| Primary    | Namespaces to clear                                             |
| ---------- | --------------------------------------------------------------- |
| Python     | PyPI (flat namespace), plus crates.io if a Rust port is planned |
| Rust       | crates.io (flat, kebab-case, names are permanent)               |
| JavaScript | npm (the scoped `@scope/name` escape hatch PyPI lacks)          |
| Any CLI    | the binary name on PATH, plus its 2-letter alias                |

If a registry is not covered, extend the mapping per session through `check-name` arguments or a config file — never by editing this skill. Full rules, PEP 541 name-transfer conditions, and the config shape live in `references/namespaces.md`.

## 3. Generate candidates

- **Light path** (internal/low-stakes): brainstorm short, run the criteria and `check-name`, pick.
- **Council path** (public/high-stakes): convene advisors (legibility, metaphor-integrity, identity/collision, author-taste) to review, then researchers (literal *and* metaphorical) to generate fresh, then `check-name` the survivors.

When stakes are unclear, ask the human which path rather than guessing. The default is the light path; escalate only when the shippe is public.

## 4. Apply the five criteria

- **Legibility** — strict (a stranger infers the domain from the name) or loose (it must not mislead; meaning may be etymological). State which standard each candidate is judged under.
- **Metaphor-integrity** — the name must hold the tool's real verbs. Example: for a manager with `update/upgrade/lock/pin/sync/status`, `downstream` fails because `downstream pin` is incoherent — you pin a point, not a flow.
- **Ownability** — one clean token; a `git`/`repo` prefix-mash is weak.
- **Constellation-distinctness** — it must not read as a sibling tool's noun. A repo manager must not sound like config/state management if `topical` already owns that.
- **Ergonomics** — short binary plus a natural 2-letter alias. A long name with no clean alias is a real cost (`gc` is git-checkout muscle memory; `dist` is the packaging abbreviation).

## 5. Check availability with `scripts/check-name`

Run `scripts/check-name <name> [--all-namespaces]` over every surviving candidate. Trust its machine-readable verdict over memory:

- `free` — clear on all checked namespaces.
- `taken` — registered on a gating namespace (with package summary, last upload, and release count when PyPI).
- `collision` — not registered, but shadowed by a well-known project or brand (see `references/watchlist.md`).
- `541-claimable` — taken on PyPI by an abandoned, non-responsive owner; see `references/namespaces.md` for the exact bar.

The word families themselves are largely mined — before brainstorming from scratch, open `references/lexicon.md` to see what has already been ruled out and why.

## 6. Resolve collisions before conceding

In order:

1. **Registry name ≠ binary name.** The binary lives on PATH; the package lives in a registry. They can differ.
1. **Compound the registry name.** If `redge` is taken but `redge-cli` is free, pick `redge-cli` for the registry and keep the binary `redge`.
1. **PEP 541** reclaims dead PyPI names only — a small-but-live package is `taken`, never `541-claimable`.

## 7. Converge and record

Stop generating once families repeat without a clear winner. Present the final shortlist, state one recommendation, and leave the final pick to the human (or let them delegate it). Record the decision in the project's ledger, and append any new collision to `references/watchlist.md` or `references/lexicon.md` so the search is never re-run blind.

## Never

- Never state a name is available, or recommend one, unless `scripts/check-name` cleared every gating namespace derived in step 2.
- Never report a PyPI name as `541-claimable` when the package is merely small rather than abandoned.
- Never hardcode a new registry into this skill so that covering it requires rebuilding the skill — extend namespace coverage through `check-name` args or config instead.
- Never pick a name whose noun collides with a sibling tool's domain on the same machine.

## References

- `references/namespaces.md` — registry rules, the PEP 541 bar, and the `check-name` config shape.
- `references/watchlist.md` — well-known projects and brands that force a `collision` verdict.
- `references/lexicon.md` — the word families already explored with what was ruled out and why.
- `scripts/check-name` — the availability and alias prober.

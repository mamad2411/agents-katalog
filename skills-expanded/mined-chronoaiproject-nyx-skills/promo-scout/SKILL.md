---
name: promo-scout
description: Verify-first promotion intelligence for ANY repo or org. Pulls live GitHub state, runs sshx multi-perspective consensus over it, and returns an evidence-backed board of what is genuinely promotable, how items connect, and what is unverifiable. Use when an agent or operator asks "what's worth promoting / what connects / what's real" for a target repo or org.
version: "2.0"
license: MIT
metadata:
  category: mixed
  output-type: text
  runtime:
    - python
  tool-list:
    - gh
    - sshx
  runtime-env-var:
    - GH_TOKEN
  tag:
    - repo-research
    - promotion
    - consensus
---

# promo-scout

Generic, verify-first promotion intelligence. It is the opposite of a hype scraper: nothing reaches the board unless live GitHub state backs it, and the judgment is made by `sshx` consensus (isolated perspectives + truth table), not by one model's say-so.

Requires: `gh` authenticated with your existing GitHub auth, either via `gh auth login` or `GH_TOKEN`, and the `sshx` skill available to the caller.

## When to use
An agent or operator wants, for a target repo/org: what is genuinely promotable right now, how the pieces connect across repos, and what tempting claims are NOT verifiable.

## Step 0 — confirm explicit scope WITH THE USER
There is no broad account-wide default. Require the user to name:
- a whole **org** (public repos only by default),
- one or more **specific repos** (`owner/repo`), or
- a **mixed list**.
Also confirm `REPO_LIMIT` for org targets (default 12 most-recently-active public repos). Private repo collection requires explicit opt-in with `--include-private`; do not use that flag unless the user has confirmed it.

## Step 1 — fetch live state (deterministic; runs from anywhere)
Run the bundled fetcher with an explicit target:
```
python3 scripts/promo_scout_fetch.py <org | owner/repo> [more...]   # public/default scope
python3 scripts/promo_scout_fetch.py --include-private <org | owner/repo> [more...]   # only after explicit confirmation
```
It writes `/tmp/promo_scout_bundle.json`: per-repo README head, recent commits, releases, open PRs, recent issues. This is the ONLY evidence the consensus step may use.

## Step 2 — run real sshx consensus over the bundle
Invoke the `sshx` skill (worker-delegated, isolated perspectives, codex-cli workers) with this decision, feeding the bundle as the fixed input:

> Given ONLY this live GitHub state bundle, produce three lists. (1) Promotable: items genuinely worth promoting now — each MUST cite concrete bundle evidence (a release tag, a dated commit, a README capability). (2) Connections: cross-repo links where one repo's work composes with another's, each backed by a real signal in the bundle (shared PRs, dependency mentions, complementary capability). (3) Dropped: tempting claims that the bundle does NOT support, with the missing evidence. No overclaim; if evidence is absent, it goes to Dropped, not Promotable.

Use distinct sshx thinking-perspectives, e.g.: a **promotability** lens, a **cross-repo connection** lens, and a **skeptic / overclaim-hunter** lens. Require convergence per the sshx truth table; honor `abstain` when workers can't establish a claim.

## Step 3 — emit the board
Write the agreed result as a board (markdown + optional JSON): `## Promotable now`, `## Connections`, `## Dropped (unverifiable)`. Each promotable/connection item carries its bundle evidence inline. The Dropped list is mandatory — it is the credibility of the board.

## Guardrails
- Evidence or it doesn't ship. Live bundle is the only source; no outside memory, no inflated numbers.
- The connections/synthesis must EMERGE from the consensus over live state — do not inject a pre-written narrative.
- Honest by construction: unverifiable → Dropped; when consensus can't be reached, report `abstain`, not a guess.

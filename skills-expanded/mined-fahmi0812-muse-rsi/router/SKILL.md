---
name: router
description: Route any task to the right verified skill from the muse-rsi index.
---

# muse-rsi Skill Router

Route any task to the right verified skill before doing the work. The index lives in `registry.json` beside this file: 66 core listed skills, 32 further-reference skills, 11 original skills written for this system (all 11 wired into `registry.json`), and a 139-skill Lumitome reference index. The public index is at https://github.com/fahmi0812/muse-rsi.

## Route the request

- Read the request and name its domain first: full-stack, DevOps, office, academic, research, health, design, video, security, or agent work.

- Run the router as a program when the match is not obvious: `python3 scripts/route.py "<task>"` (in the muse-rsi repo; `route.py` scores the request against the same registry the eval tests — `scripts/eval_routing.py`, 130 queries, must pass). Use its top 3 as the starting point, then apply your judgment.

- How `route.py` scores (v2): a small BM25-style ranker over three weighted fields — `keywords` (3.0), `domain` (2.0), `notes` (1.0) — with one shared token normalisation, so hyphenated/dotted phrases (`next.js`, `full-stack`) and multi-word phrases (`systematic review`) match as single terms. Ties break by tier (original > core > reference > lumitome-reference), then by name ascending. A query with no keyword-field hit returns `NO_MATCH` instead of a junk guess.

- Or open `registry.json` and match the request against each skill's `keywords`, `domain`, and `notes`.

- Pick the smallest set that covers the request, usually one to three skills. On a tie, an `original` skill outranks `core`, `core` outranks `reference`, and `reference` outranks `lumitome-reference`.

- When two skills overlap, pick the one whose notes match the request most closely and name the other one as the alternative.

- When nothing in the registry matches, say so plainly instead of forcing a fit. Then search for a new skill and run it through the audit below before adding it.

## Load the skill

- For an `original` skill, read its file at `skills/<name>/SKILL.md` in the muse-rsi repo, or use the installed copy under `~/workspace/custom-skills/<name>/`.

- For a `listed` skill, open its repo link and follow that repo's own README or SKILL.md. This router never copies full upstream SKILL.md files (the one exception: Lumitome frontmatter descriptions are copied/trimmed into the registry `notes` field).

- For a `lumitome-reference` skill, open the Lumitome repo at `.opencode/skills/<name>/SKILL.md`. The red-team pack is disabled by design and is never a valid target.

- When the task needs a skill that is only listed by link, fetch it with the GitHub connector or a local clone, read its SKILL.md, and then do the work. Do not claim to have used a skill that was never read.

## Verify before installing

- Run every new skill through `self-audit` before installing it: it must exist, have a SKILL.md, have a clear licence, and not read `.env` or vault data.

- Never install a skill from the Pending or Not Included lists. The registry only holds verified entries, so a skill that is missing from it is not cleared.

- Check the licence before vendoring anything. AGPL, GPL, and proprietary entries are link-only with a flag, never copied.

## Guardrails

- Health work is research and health-informatics only. Never diagnose, never recommend treatment, never interpret a person's symptoms or test results, and never handle patient data.

- Security work is defensive only. No offensive skills, no exploits, no jailbreaks, and no red-team material.

- Academic work never fabricates citations, data, or results, and never helps evade AI detection.

- Office work never sends email or shares a document without explicit approval, and never pastes confidential content into an external tool.

- Trading work is research and backtesting only. No automated live trading without the user's approval.

## Available connectors

- [GitHub](/opt/hatch/connectors/github/CONNECTOR.md) for reading repos, checking SKILL.md files, and pushing changes to the muse-rsi repo.

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.

## Websites

- [muse-rsi on GitHub](https://github.com/fahmi0812/muse-rsi) for the full public index, verification docs, and the original skills. Carry the task's domain into the search and verify the skill entry there before installing.

- [Lumitome on GitHub](https://github.com/fahmi0812/Lumitome) for the reference skills. Verify the skill folder exists there before linking it.

## Alternatives for better results

- When the request spans two domains, route to one skill per domain and run them in order instead of picking a single broad skill.

- When the user asks in Bahasa Indonesia, prefer the Indonesian skills in the registry first: `humanizer-indonesia`, `naskah-id`, `academic-campus`, and the Lumitome Indonesian writing skills.

## Test-time compute — how much effort a routing decision deserves

`route.py` scores each candidate as 3.0·idf per keyword-field hit +
2.0·idf per domain-field hit + 1.0·idf per notes-field hit, where
idf = log((n−d+0.5)/(d+0.5)+1) and n is the registry size (248).
On this scale one rare keyword hit is worth about 15 points and one
common keyword hit about 5, so a top-1 score under 10 means the match
rests on a single common term or weak overlap — thin evidence.

A gap of 0.00 between top-1 and top-2 is normal, not a tie to worry
about: entries in one domain share the same keyword set, so they score
identically and the tier tie-break (original > core > reference >
lumitome-reference) decides deterministically. What matters is whether
top-1 and top-2 are in the **same domain** or not.

**Token normalisation.** Query and registry terms are normalised the
same way (shared `normalize_terms` in `scripts/route.py` and
`scripts/generate_registry.py` — keep them identical): a conservative
rule-based stemmer folds plurals and verb/noun variants
(`agents`→`agent`, `vulnerabilities`→`vulnerability`,
`transcription`→`transcribe`, `tulisan`→`tulis`), and hyphenated terms
are indexed per component as well as whole
(`dispatching-parallel-agents` also matches `parallel`). A small
denylist protects words stemming must not touch (`glass`, `bias`,
`canvas`). Known limitation: there is no IDF cap, so one very rare
term (a name that appears in exactly one entry) can dominate a query
— if top-1 rests on a single rare name-word, treat it as AMBIGUOUS.

Three bands (thresholds measured on the 130-case eval, 2026-11-22;
re-measure when the registry grows):

- **EASY — top-1 ≥ 10 and (top-2 in the same domain as top-1, or the
  gap is ≥ 5).** Single pass, use top-1. Measured: 102 of 130 eval
  cases, e.g. "contribute a new skill to muse-rsi" (98.12 vs 22.19,
  same domain).
- **AMBIGUOUS — top-1 ≥ 10, top-2 in a different domain, and the gap
  is < 5.** The router genuinely cannot tell which domain wins — run
  [council](../council/SKILL.md) before acting. Measured: 11 of 130,
  e.g. "review my code for bugs" (20.09 Security vs 20.09 Full-Stack
  Development, gap 0.00 — an exact-score tie, broken alphabetically).
- **HARD — `NO_MATCH`, or top-1 < 10.** Do not guess. Run
  [interrogate-claim](../interrogate-claim/SKILL.md) on the request, or ask the user
  exactly one clarifying detail. Measured: 17 of 130 — 16 are deliberate
  `NO_MATCH` negatives (15 plain + 1 policy refusal, case #77), and 1 is
  a thin match: "create a REST API with FastAPI and PostgreSQL" (top-1
  5.66). The price of this band is one clarifying question on thin matches: the routing is usually still
  right at top-1, but the evidence is a single common term, so the
  question is cheaper than a wrong action.

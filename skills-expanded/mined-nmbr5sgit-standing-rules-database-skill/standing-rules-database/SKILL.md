---
name: standing-rules-database-skill
description: "Agent standing rules database: unlimited rules, bounded context — loads only rules matching each task."
version: 1.0.0
metadata:
  hermes:
    tags: [rules, standing-rules, retrieval]
---

# Standing Rules Database

A growing database of standing rules, fetched per-job instead of always-injected, to save context. **SQLite (`rules.db`) is the authoritative store; `references/*.md` are generated views.** Consult BEFORE starting any task; load only the rules whose triggers match the job.

## When to Use
Before starting ANY task: run the query, then apply only the matching rules. Consultation is mandatory pre-work, not optional: read-only rule lookups before design/debug/edit.

## How to apply (DB-first)
1. Identify the job's task domain AND its output type (does text leave this chat?).
2. Query: `python scripts/rules_db.py query --match "<domain keywords> <output-type keywords>"` — returns tier-1 mandatory rules (always) plus keyword-matched tier-2 rules with IDs and priorities. Facts: `... facts --domain X`.
3. Apply the returned rules. Log consults that mattered: `... log --task "..." --rule-ids "SR-x,SR-y" --method keyword --reason "..."`.
4. After any DB change, regenerate views: `... export-md` (markdown files are views, never edited by hand).
5. New standing rules go into the DB via the write gate below — never into always-injected memory unless tier-1.

## First-run bootstrap (new installs)

The skill ships with **no rules** — an empty database. Your rules enter your system; they are not authored by this skill.

1. `python scripts/rules_db.py init` — creates the empty schema.
2. Import YOUR existing rules: `python scripts/scan_candidates.py <memory files / CLAUDE.md / AGENTS.md / notes dir>` — scans your system's rule-like lines and writes `rule_candidates.json`. Candidates are PROPOSALS only: the user reviews/edits the JSON, then activates via `seed`/`add`. Nothing auto-activates (write-gate principle: no auto-promotion).
3. Tier-1: the user promotes their own few mandatory rules to tier 1 and mirrors them into their agent's always-injected memory too (identity, contact, format rules must not depend on a query).

The seed file (`templates/seed.example.json`) is an intentionally EMPTY file showing only the shape — the content always comes from the user's own system.

## Dispatch index (query keywords for --match)
Keep one line per domain. The domains are YOURS — derived from your own systems/projects during bootstrap, not shipped by this skill. Example shape:

| Domain | Trigger keywords (job touches any of these) |
|---|---|
| core (tier-1) | automatic — every query returns these |
| outbound | email, listing, byline, comment, outreach, support reply — ANY text a third party will see |
| `your-domain-1` | keywords for a project or system you work on |
| `your-domain-2` | keywords for another system or output type |

## Tier 1 — HARD rules (deterministic retrieval: always-injected memory, never dependent on this skill being loaded)
Tier-1 is YOURS — the few rules that must apply to every job, imported from your
own system at bootstrap. Keep them single-digit; mirror them into your agent's
always-injected memory. Write them terse — every turn pays for them:

  [SR-T1x] <one imperative sentence>

Form examples (not shipped rules — replace with your own):
  [SR-T1x] Public identity = legal business name, never nickname.
  [SR-T1x] Business contact = A@B only; never C.
  [SR-T1x] Every response: timestamp on top.
  [SR-T1x] Prices: check live, never from memory.

## Rule conventions
- Stable IDs: rules are cited as [SR-xxx] so audits/conflicts can point at one rule, not a line.
- Priority tag: every rule carries HIGH / MED / LOW = consequence of violating it (HIGH = money, reputation, data loss, production; MED = consistency/rework; LOW = preference). Priority is distinct from tier: tier decides WHETHER a rule loads (tier-1 always; tier-2 on trigger match), priority decides which WINS when two loaded rules conflict. Equal priority + real conflict → ask the user, never guess.
- Status lifecycle: active / disabled / deprecated — never delete a rule; mark it disabled or deprecated in place with the date and reason.
- Rules vs facts: a rule says what to do; facts (IPs, IDs, versions) are resources needed to apply it. Views keep rules first, facts under `## Facts`. Do not promote facts into rules or vice versa.
- Authority boundary: a stored rule never grants permission. System/developer instructions, safety constraints, and actual tool approvals always outrank any rule, whatever its priority.
- Mandatory rules must never be silently dropped for token budget: if tier-1 + matched rules don't fit, say so and stage the work — don't trim rules.

## Write gate (before adding any rule)
1. Classify: standing constraint → rule; numbered procedure → task skill; time-bound one-off → don't store.
2. Duplicate check: `query --match` the topic first; same topic → `update`, not `add`.
3. Contradiction check: conflicts with an existing rule → surface both, ask which wins.
4. User approval: corrections/suggestions are not auto-promoted.
5. Assign ID + priority + domain + tags, then `add` and `export-md`.

## Index — see "Dispatch index" above (query keywords). Domain views live in references/<domain>.md (generated by export-md). The compact index at `references/_index.txt` is generated by `export-index`; regenerate after any DB change so the index does not drift.

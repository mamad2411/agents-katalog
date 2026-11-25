---
name: extract-business-context
description: Extract the project's WHY — mission, target users, business model, success KPIs, constraints, anti-goals, competitive context, maturity stage — from the CODE first (entity clusters, role/permission tables, tenancy columns, payment and queue integrations, feature-flag keys, i18n locales, contributor counts, all already in `_extracted-codebase.md`), then README + manifests + git log + ai/status.md. Asks the user ONE consolidated question only for facets neither the code nor the documents answer. Outputs `.claude/_extracted-business.md`, consumed by Phase 4.7b to populate `ai/project-goals.md`, `ai/users-and-personas.md`, `ai/business-model.md`, `ai/competitive-context.md`, `ai/roadmap.md`.
kind: skill
pack: learning
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Skill: extract-business-context

## Purpose

Stack tells what tech. Domain (ecommerce/lms/etc.) tells what kind of product. THIS skill captures **why this specific product exists, for whom, at what maturity, with what constraints** — the facets that distinguish two ecommerce projects from each other.

Without this output, generated content (CLAUDE.md opener, agent personas, rule prose) addresses a generic "user" instead of the project's actual primary persona, and proposes solutions that ignore the project's real constraints (latency budget, regulatory regime, team size).

## Premise

- **Code outranks prose about code.** The build is what the team actually shipped; the README is what someone once wrote about it. Read `.claude/_extracted-codebase.md` (Step 0.5) BEFORE any document, and where the two disagree about the same facet, the code wins and the prose claim is recorded under `## Contradicted by code` rather than as an answer.
- Real source is the truth. Read the extracted code evidence + README + manifests + `ai/status.md` + git log + LICENSE + prior `ai/project-goals.md` before composing a single facet answer.
- Every `[CONFIDENT]` claim cites the source file (or `<path:line>` for inline mentions).
- **A prose claim is not code-strength evidence.** `[CONFIDENT]` maps onto `[found:]` (the 1:1 mapping below), and `phase-2-profile.md § Provenance discipline` lets Phase 4 anchor to `[found:]` claims only. A single sentence in a README therefore becomes anchorable at the same trust as a resolving `path:line` — this is the one place in the whole provenance system where that happens. Guard it: a facet whose ONLY support is a prose assertion, with no corroboration in the code evidence of Step 0.5, is `[INFERRED]`, not `[CONFIDENT]`. Two independent prose sources, or one prose source plus a code corroboration, restores `[CONFIDENT]`.
- Every `[INFERRED]` claim names the circumstantial signal it derived from (e.g. "maturity inferred from 18-month repo age + 14 ADRs").
- Empty extraction is honest — `[UNKNOWN]` + `_UNKNOWN — fill in when decided_` is a valid facet outcome.
- These three classes ARE this skill's provenance markers — they map 1:1 onto the universal vocabulary in `phase-2-profile.md § Provenance discipline` (`[CONFIDENT]` = `[found:]`, `[INFERRED]` = `[inferred:]`, `[UNKNOWN]` = `[unconfirmed]`). Downstream consumers and `/setup-project-health` check 9 count both vocabularies.
- Fabrication — inferring a persona from a logo, a KPI from a hunch, a competitor from training-data memory — is the failure mode downstream files inherit forever.

## Mechanical halt

- Hand-wave answers — `enterprise users`, `typical SaaS`, `standard subscription`, `appears to target`, `roughly MVP-stage`, any claim without source attribution — REFUSE to write.
- Re-derive from a cited source OR downgrade to `[UNKNOWN]` and surface in the consolidated question.
- If a facet has no signal in any source AND `interactive: false`, write `<NOT-DETECTED: <facet>: no signal in <sources searched>>` plus `_UNKNOWN_` — never synthesize an answer to make the file look complete.
- Phase 5 audit surfaces every `<NOT-DETECTED>` row so the user can re-run with `--interactive` to fill it.

## When to use

- `/setup-project` Phase 2 — invoked by `extract-codebase-overview` Step 13.
- Via `/refresh-knowledge` Phase 3, which invokes `extract-codebase-overview`; that skill's Step 13 chains this one, so a refresh rewrites `_extracted-business.md` in the same pass — with `extracted_codebase_path` present, because the oracle was written seconds earlier.

## Inputs

- `project_root` — absolute cwd.
- `output_path` — defaults to `<project_root>/.claude/_extracted-business.md`.
- `extracted_codebase_path` — **required when it exists**; defaults to `<project_root>/.claude/_extracted-codebase.md`. This is the code evidence Step 0.5 mines. `extract-codebase-overview` Steps 1-12 have already written it by the time Step 13 invokes this skill, so it costs nothing to read and everything to skip. If the file genuinely does not exist (CREATE mode, or a caller invoking this skill directly without running the overview first), Step 0.5 falls back to running its own greps over `project_root` and records `evidence_base: greps` — never silently skips to Step 1. Note that `/refresh-knowledge` is **not** such a caller: it writes the oracle in Phase 3 before this skill is reached.
- `interactive` — if `false`, never asks; missing facets recorded as `_UNKNOWN — fill in when decided_`.

## Procedure

### Step 0.5 — Mine the CODE evidence first (before any document, before any question)

The evidence for half these facets is already extracted and sitting one file away. `extract-codebase-overview` Steps 6-9 walk the data model, the API surface, and the corroborated cross-cutting signals — entity clusters, `tenant_id` columns, per-controller auth schemes, payment / queue / search / AI integration sites — and Step 13 then invokes this skill **after** all of it is written. Until this step existed, that evidence was read and then discarded before the question was composed: every row of Step 1 is a document or a piece of metadata, not one of them reads source, and the result was five of eight facets going to the user by default on a repo whose code already answered four of them.

Read `extracted_codebase_path` and harvest these rows FIRST. Each is a fact about what the team built, not a claim about what it is for — the inference to a facet is yours to make and to mark:

| Code evidence (section of `_extracted-codebase.md`) | Facet it feeds | How to read it |
|---|---|---|
| `## Data model` — entity/table names and their relations | **business_model** | The entity cluster names the transaction. Plans + subscriptions + invoices + line-items ⇒ recurring billing. Orders + carts + shipments + fulfilments ⇒ transactional commerce. Listings + bids + payouts ⇒ marketplace take-rate. Workspaces + projects + members with no billing entity at all ⇒ internal tooling or pre-revenue. Name the entities you are reasoning from. |
| `## Data model` — `tenant_id` / `tenantId` columns, soft-delete markers, audit columns, `*_translations` tables (already inferred at Step 6) | **constraints** | Universal tenancy ⇒ isolation is a hard constraint, not a feature. Audit columns + retention jobs ⇒ a compliance regime is in force; cross-check `templates/domains/compliance/` for which. Translation tables ⇒ i18n is a data-layer constraint, and the locale list below tells you the markets. |
| `## API surface` — per-controller auth scheme; plus role / permission / policy / ability tables in `## Data model` | **target_users** | Distinct actor classes the system actually authorises ARE the persona structure. Three role rows and three guard families is a three-persona product whatever the README says. This gives you persona *structure* — count and boundaries — not persona *motivation*, which stays a question. |
| `## Cross-cutting concerns` — corroborated signals with entry-point files (payment, AI, search, background-jobs, multi-currency, real-time) | **business_model**, **success_kpis** | A payment SDK with real integration sites is revenue evidence: the integration shape (one-off charge vs subscription vs split payout) discriminates the model. Each corroborated signal also nominates a KPI candidate — a queue nominates throughput / lag, a search index nominates result latency, a payment path nominates conversion. Nominate; do not assert the target number. |
| `## Recent activity` + `git shortlog -sn --since="12 months ago"` (run it — the census is cheap and nothing else answers this) | **constraints** (team size), **maturity_stage** | Distinct authors in the last year is the team-size constraint that `apply-pack-adaptation § Constraints` anchors every workflow artifact to. Commit cadence + repo age + ADR count is the maturity evidence. |
| `## Modules` + `## Base classes` + `## Anti-patterns observed` | **maturity_stage**, **constraints** | Load-bearing bases with many dependents and a stable module boundary read as scale/mature; a large anti-pattern count with few modules reads as prototype/MVP under debt. |
| Feature-flag keys — **no oracle section carries these**; feature flags are not in the Step-9 signal list, so this row re-greps: `grep -rInoE '(featureFlag\|feature_flag\|isEnabled\|unleash\|launchdarkly\|flipper\|flagsmith)[^\n]{0,60}'` over the source dirs `## Repository shape` names | **roadmap**, **anti_goals** | Live flags are the bets in flight; a flag named for a capability that has no entities behind it yet is roadmap, not product. |
| i18n locales — `## Cross-cutting concerns` names the i18n signal and its entry-point files; the **locale list itself** is not persisted there, so read the catalogue directory those entry points point at | **target_users**, **constraints** | The shipped locale set is the served market, stated by the build rather than by positioning copy. |
| Queue / job / worker names — `## Cross-cutting concerns` § background-jobs gives the entry-point files; the **job names** are inside them, so open those files (they are already cited, so this is a read, not a search) | **success_kpis**, **constraints** | Named jobs are the operational surface the team already decided to run and watch. |

**Six of these nine rows resolve entirely inside `_extracted-codebase.md`; three do not, and the table now says which.** That distinction is the difference between a read and a search: a row naming a section is free and deterministic, a row that re-greps costs a walk and can come back empty on a repo the oracle already covered. Naming them stops a run from silently skipping the three expensive rows and reporting the same `evidence_base` as one that ran them. If a re-grep row is skipped, record it in `## Gaps` — not as a facet answered by default.

**Provenance for this step.** A code-derived facet cites the extraction section it came from (and, through it, the `path:line` the extraction cites). A facet the code *structurally implies* — "subscription billing because plans + subscriptions + invoices" — is `[INFERRED]` with the entity list as its named basis, because the entities are found and the business conclusion is not. Only a facet the code states outright (a locale list, a role table, an author count) is `[CONFIDENT]`.

**When `extracted_codebase_path` is absent** (CREATE mode; or a direct invocation that skipped the overview): run the greps this table implies directly against `project_root` — entity/model globs, role/permission table names, the payment / queue / i18n dependency names in the manifest plus their import sites, `git shortlog -sn` — and record `evidence_base: greps` in the output header. Falling straight through to Step 1 is the defect this step exists to fix; it is not the degrade path.

### Step 1 — Mine the documents (still no questions)

Read in priority order. Each source MAY answer multiple facets; record everything found. **These rank BELOW Step 0.5 for any facet both address** — see § Precedence directly after the table:

| Source | What to extract |
|---|---|
| `README.md` (root) | Mission paragraph, target user mentions, screenshots/feature list, install/quick-start (signals maturity), badges (CI / coverage / version). |
| `package.json` / `pyproject.toml` / `Cargo.toml` / `composer.json` description + keywords | One-line mission + tag soup. |
| `ai/status.md` (if exists) | Current phase, in-flight work, recent changes — primary maturity signal. |
| `ai/business-domain.md` (if exists) | Already-classified domain — confirms or feeds into our domain classification. |
| `ai/project-goals.md` (if exists, REFRESH mode) | Prior answers — preserve verbatim, ask only for new facets. |
| Git log first commit message + repo creation date | Maturity (months/years old) + original intent. |
| Top-level `docs/` or `documentation/` | Product overview docs if maintained. |
| `LICENSE` | Open-source vs proprietary signal. |
| `.github/ISSUE_TEMPLATE/*` | If present + populated, hints at user types reporting issues. |
| Domain name in `package.json` repository field | Sometimes reveals product category. |

#### Precedence — and what to do when the two disagree

1. **Code evidence (Step 0.5) outranks documents (Step 1) for the same facet.** A README describing what the project used to be is the single most common stale input this skill takes, and it is ranked FIRST in the table above, which is precisely why it needed an authority above it. The only staleness guard that existed was "ignore a `create-react-app`-style generated README" — that catches a README nobody wrote, not a README nobody updated.
2. **A contradiction is a finding, not a tie to break.** When a document asserts a facet the code contradicts — positioning that names a market the locale set does not serve, a business model with no matching entity cluster, a persona with no role or guard behind it — do NOT write it as the answer and do NOT silently drop it. Write the code-derived answer as the facet, and record the document's claim in `## Contradicted by code` with both citations. A pivot is exactly this shape, and the block is how the team sees that their README has drifted.
3. **Prose the code neither confirms nor contradicts stays prose.** Mission, anti-goals and competitive context are genuinely document-shaped facets — code cannot express "what we refuse to build". They keep their document sourcing, at the confidence § Premise's prose-claim rule allows.
4. **Never promote a code-derived facet to `[CONFIDENT]` on the strength of a matching README sentence alone**, and never demote one because the README is silent. Silence is not disagreement.

Absent this ordering, a pivoted product's old positioning lands in the CLAUDE.md opener (`phase-4-templates.md § 4.7b`) and in the `AGENTS.md` product paragraph every non-Claude tool reads (`templates/tool-adapters/codex/adapter.md`), stated as fact, in a run where every gate was green.

### Step 2 — Map findings to the 8 facets

For each facet, record the answer + confidence + source:

| Facet | Asks |
|---|---|
| **mission** | "In one sentence, what does this product do?" |
| **target_users** | "Who uses it? Personas (e.g., Egyptian SMB merchants, US enterprise IT admins, gig drivers)." |
| **business_model** | "How does it make money / serve mission? subscription / per-tx / ad / freemium / open-source / internal-tooling." |
| **maturity_stage** | "Where in lifecycle? idea / prototype / MVP / paying-customers / scale / mature / sunsetting." |
| **success_kpis** | "Top 1-3 metrics that move when this product wins." |
| **constraints** | "Hard limits — latency / cost / compliance / team size / language?" |
| **anti_goals** | "What is this NOT trying to be?" |
| **competitive_context** | "Closest 1-3 alternatives + why this product instead?" |

Confidence levels:
- `[CONFIDENT]` — explicit answer in 1+ source **that the code corroborates or does not contradict**, or a fact the code states outright (locale set, role table, contributor count). A lone prose assertion is `[INFERRED]` per § Premise — `[CONFIDENT]` maps onto `[found:]` and `[found:]` is anchorable.
- `[INFERRED]` — derivable from circumstantial signals, including every business conclusion drawn from code STRUCTURE (e.g. "subscription model inferred from `plans` + `subscriptions` + `invoices` entities and the payment integration at `<path:line>`"). The named basis is mandatory.
- `[UNKNOWN]` — neither the code (Step 0.5) nor the documents (Step 1) address this.

**Which facets Step 0.5 should have already moved off `[UNKNOWN]`.** On a repo with a data model and an API surface, `business_model`, `target_users` (structure), `constraints` (tenancy / compliance / locales / team size), `maturity_stage` and `success_kpis` (candidates) all have code evidence and should reach Step 3 as *inferences to confirm*, not as blanks to fill. `mission`, `anti_goals` and `competitive_context` are the three the code genuinely cannot answer — those are the questions worth a user's attention. If this step is about to send five blanks to the user on a repo with 40 entities and a payment integration, Step 0.5 did not run.

### Step 3 — Consolidated question (only for `[UNKNOWN]` facets)

If `interactive: true` AND any facets are `[UNKNOWN]`:

Bundle them into ONE message (not N separate questions). Show what was inferred for the `[INFERRED]` ones with [Y/correct?] markers. Show `[UNKNOWN]` facets as fields to fill.

```
📋 Project context — please confirm + fill blanks (one message):

  ✓ Mission [CONFIDENT, README + manifest description agree]: "Multi-tenant ecommerce SaaS for SMB merchants"
  ✓ Domain [CONFIDENT, detected]: ecommerce + ai (AI SDK in deps with prompt-construction sites)
  ? Maturity [INFERRED — paying-customers: 14 ADRs, 18 months, 9 contributors/12mo, stable module boundary]: confirm or override
  ? Target users [INFERRED — 3 actor classes from `roles`/`permissions` + 3 guard families on controllers: merchant, staff, platform-admin]: names right? which is PRIMARY?
  ? Business model [INFERRED — `plans`/`subscriptions`/`invoices` cluster + recurring charge at `src/billing/subscribe.ts:44`]: subscription. Tiers/pricing?
  ? Hard constraints [INFERRED — every entity carries `tenant_id`; audit columns + 90-day retention job; locales ar/en/fr; 9 contributors]: latency budget? regulatory regime?
  ? Success KPIs [CANDIDATES from code — checkout conversion (payment path), queue lag (`order-fulfilment` worker), search latency (index at `src/search/`)]: pick top 1-3 + targets
  ✗ Anti-goals (what NOT to build): ____
  ✗ Competitive context (closest alternative + why this instead): ____

Reply in any shape — paragraphs, bullets, partial answers. Skip with "skip <facet>" — left as TBD.
```

Five blanks became two, and the six confirmations each carry the evidence that produced them — which is a different and much cheaper ask than a blank. **The remaining two are the right two**: nothing in a codebase states what the team refuses to build or who they think they are beating. Note also what did NOT happen: no facet was invented to make the message look answered, and `anti_goals` / `competitive_context` stay `✗` rather than being guessed from the domain.

If `interactive: false`: skip the ask; record `[UNKNOWN]` facets as `_UNKNOWN — fill in when decided_` placeholder.

### Step 4 — Author the output

Write `.claude/_extracted-business.md`:

```markdown
# Business Context Extracted
Generated: <ISO> by `extract-business-context` skill
Consumed by: Phase 4.7b → populates ai/project-goals.md + users-and-personas.md + business-model.md + competitive-context.md + roadmap.md
evidence_base: <extracted-codebase | greps>   <!-- which Step 0.5 path ran; `greps` means _extracted-codebase.md was absent -->
code_derived_facets: <N of 8>                 <!-- how many facets Step 0.5 moved off [UNKNOWN] before any document was read -->

## Mission
<one sentence>
Confidence: [CONFIDENT|INFERRED|UNKNOWN]
Source: <where derived from>

## Target users + personas
<list of 1-3 personas with: who they are, primary need, top frustration, why they choose this product>

## Business model
<how value/money flows; pricing if relevant; unit economics one-liner>

## Maturity stage
<one of: idea / prototype / MVP / paying-customers / scale / mature / sunsetting>
Evidence: <commits-per-week | ADR count | deps stability | customer count if cited>

## Success KPIs
1. <metric + target + current value if known>
2. ...

## Constraints
<latency budget, cost ceiling, compliance regime, team size, locale/RTL requirements, etc.>

## Anti-goals
<bullets — what this product explicitly is NOT trying to be>

## Competitive context
- <alternative 1>: <why we're not them>
- ...

## Contradicted by code
<Empty is the normal case — omit the rows, keep the heading. One row per facet where a document
asserted something the code does not support. Both citations are mandatory; a row without them is
an opinion about the README.>

- **<facet>**: `<doc>:<line>` claims "<verbatim claim>", but <code evidence> at `<path:line>` shows
  <what the build actually does>. Recorded answer follows the code. <One line on the likely reason —
  a pivot, a renamed market, a feature removed — if the git history supports one; otherwise say
  "reason not established".>

## Asked-and-answered (interactive Q/A trail, REFRESH-friendly)
<verbatim Q+A from Step 3 if interactive — preserves traceability for next REFRESH>

## Open / unknown facets
<facets still _UNKNOWN_ — Phase 4.7b writes them as placeholders in the user-facing files; surfaced in Phase 5 report>
```

### Step 5 — Cross-link

Append a one-line entry to `.claude/_extracted-codebase.md` (if it exists):
> `## Business context — see _extracted-business.md`

## Output

Single file: `.claude/_extracted-business.md`. Print to stdout:

```
Extracted business context → .claude/_extracted-business.md
  Evidence base: <extracted-codebase | greps>
  Mission: <one-line>
  Domain: <detected domain(s)>
  Maturity: <stage>
  Personas: <count>
  KPIs: <count>
  Constraints: <count>
  Code-derived facets: <N>/8      # facets Step 0.5 answered before any document was read
  Contradicted by code: <count>   # document claims the build does not support
  Open facets: <count of _UNKNOWN_>
```

`Code-derived facets` is printed on every run, including at 0 — a run that reports 0 on a repo with a
populated `## Data model` is the regression this skill was rewritten to prevent, and a number that
only appears when it is healthy cannot show that.

## Failure modes

- **Brand-new repo, no README, prompt-driven CREATE** → no code either, so Step 0.5 has nothing to mine: record `evidence_base: greps`, `code_derived_facets: 0`, fall back entirely to the prompt as source. If even the prompt is sparse, write skeleton with all `_UNKNOWN_` and surface in plan.
- **README exists but is just a generated template (e.g., "Created by create-react-app")** → ignore it; treat as if absent.
- **README describes a product the code no longer is (the pivot case)** → this is the one Step 0.5 + § Precedence exist for. Do NOT treat it as absent — the drift is itself a finding. Answer from the code, record the README's claim under `## Contradicted by code`, and surface the count in the Phase 5 report so someone updates the README.
- **Code and documents agree on a facet** → keep the document's wording (it is written for humans) and cite BOTH. Agreement is what earns `[CONFIDENT]`.
- **Rich code, no documents at all (internal service, no README)** → the historically worst case for this skill, and now the one it handles best: `business_model`, `target_users`, `constraints` and `maturity_stage` all come off Step 0.5, and only `mission` / `anti_goals` / `competitive_context` reach the user.
- **REFRESH mode + existing `ai/project-goals.md` etc.** → read those files FIRST as authoritative; only re-ask facets where the user explicitly flagged "needs update" or where prior answer was `_UNKNOWN_`.
- **`interactive: false` + most facets `[UNKNOWN]`** → write the file with placeholders + emit warning. Phase 5 audit MUST surface so user can fill via re-run.

## Quality bar

After this skill runs, downstream Phase 4.7b should write `ai/project-goals.md` + the 4 sibling files **with no further questions** — every section has either a real answer or an explicit `_UNKNOWN_` placeholder. If 4.7b finds itself asking the user a question this skill should have captured, that's a skill bug.

**The sharper bar, on any repo with a data model**: every question this skill puts to the user must be one the codebase cannot answer. A blank sent up for `business_model` on a repo with a billing entity cluster, or for `target_users` on a repo with a role table, is not an honest `[UNKNOWN]` — it is Step 0.5 not having run. Six named consumers (`apply-pack-adaptation § Constraints`, the `business` / `ui-ux` / `migration` pack topics, the `AGENTS.md` product paragraph, the CLAUDE.md opener) treat this file's output as an always-required input; they cannot tell `_UNKNOWN_` from "not applicable", and they degrade silently on both.

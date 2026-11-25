---
name: nothing-new-under-the-sun
description: >
  Research-first scouting agent skill that runs BEFORE any build decision,
  new dependency, new system, or feature request. Search existing solutions
  (codebase, dependencies, packages, GitHub repos, APIs, SaaS, templates)
  before writing code. Output a REUSE / USE / FORK / BUY / INTEGRATE / BUILD
  recommendation with a required schema and evidence matrix. Uses
  five-component long-term business value framing. Trigger on new features,
  new systems, new dependencies, build-vs-buy decisions, or "build/add/we
  need X" requests. Do not trigger for bug fixes, small refactors, routine
  edits, docs, style/lint, or imports already in use.
license: MIT
metadata:
  author: fahrellgiovanny
  version: "1.1.0"
---

# There Is Nothing New Under The Sun

## Core principle

Every tier decision must maximize long-term business value. Use five
components:

1. **Reliability** — will it keep working under real load and failure modes?
2. **Strategic value** — does owning it create competitive protection or
   unique customer benefit?
3. **Adaptability** — can it change as the business changes?
4. **Total cost of ownership** — build, run, and replace costs over its life.
5. **Speed to value** — how soon does the business benefit?

No tier is inherently best. The tier order — REUSE → USE → FORK → BUY →
INTEGRATE → BUILD — is a search order, not a preference order. Your
situation determines which tier maximizes value.

Commodities weight TCO and speed. Core competencies weight strategic value
and adaptability. Reliability matters in every situation.

## When to use

- Someone proposes a new feature, system, dependency, service, API, or module.
- Someone asks whether to build, buy, use, fork, integrate, or add a dependency.
- Someone says "we need X", "build X", "add X", or "write a helper for X."
- A request creates a boundary, owner, runtime dependency, or maintenance cost.

## When NOT to use

- Bug fixes, single-line fixes, or imports already in use.
- Pure refactors, helper extraction, or routine edits in existing modules.
- Content, data, or documentation edits.
- Style or lint changes.

## Establish context first

Before you search for candidates, answer these six questions. If any
question cannot be answered, ask the user before you continue.

1. **Time horizon** — how many years must this decision serve?
2. **Scale** — current load, projected peak load, and the point where the
   best answer would change.
3. **Failure cost** — what breaks if this fails? What is the business
   impact?
4. **Team capability and fit** —
   a. *Capability:* does the team have the skill, time, and domain
      knowledge to build, maintain, and operate it for the full time
      horizon?
   b. *Fit:* does the team want to own it? Does ownership match team
      identity and mission? Built-and-resented is worse than
      bought-and-managed. If capability is high but fit is low, favor
      USE or BUY over BUILD.
5. **Commodity or core** — see next section.
6. **Volatility** — how fast does the strategy or technology change?

**Constraints** — any regulatory, security, or compliance requirements.

## Commodity or core competency

Use this test: *"If a buyer or user knew we built it ourselves, would they
care?"*

- **No = commodity.** Buyers do not care who built the PDF generator or the
  auth flow. They want the result. Let a seller handle it.
- **Yes = core competency.** Buyers choose your product because of the
  matching algorithm, the recommendation engine, or the latency you control.

Classify by the majority of value. Describe any differentiated slice
separately. A commodity system with one differentiated sub-component needs a
compound recommendation.

## Tier search (fair-search evidence)

Search in this order. Move to the next tier only when you find no viable
candidate.

1. **REUSE** — already in the repository or internally available.
2. **Tier 2 — USE.** A maintained package solves the problem, either
   already installed or added as a normal dependency. Check the project
   manifest, the framework features, the built-in platform features, and
   public registries (npm, PyPI, crates.io, and similar). If the code
   stays as a normal dependency, USE wins. Only escalate to FORK when the
   code must be copied, vendored, or patched.
3. **Tier 3 — FORK.** No maintained package fits as-is. An open-source
   project solves the problem, but you must copy, vendor, or patch it.
   Check star count, contributor count, release rate, issue response
   time, and license before you fork.
4. **BUY** — a SaaS product solves it.
5. **INTEGRATE** — an API solves it.
6. **BUILD** — viable when no earlier tier fits. Cite the search.
7. **License** — check license compatibility at every step.

## Evidence matrix

For every candidate, fill one row.
The row below is illustrative. Replace it with real candidates for each request.

| Option | Reliability | Strategic value | Adaptability | TCO | Speed to value | Citation |
|---|---|---|---|---|---|---|
| express-rate-limit | Maintained OSS middleware | none — commodity | Express-only, configurable | LOW (MIT, free) | S (< 1 day) | `web_fetch: https://github.com/express-rate-limit/express-rate-limit on <today>` |

Label undifferentiated commodity slices as "Neutral (commodity)" or "Zero
for commodity" in the strategic value column.

## Long-term value assessment

After you fill the matrix, assess each component.

### Reliability

Examine real load records, outage history, MTTR, and dependency maturity.
For existing products: cite uptime, incident history, and adoption at scale.
For BUILD: "Unknown" is a real risk.

### Strategic value

Core competencies earn high strategic value only from BUILD or FORK. USE
and BUY deliver near-zero strategic value for core work. Commodities earn
neutral or zero strategic value from all tiers. For commodities, the right
tier is the one with the best TCO and speed.

### Adaptability

Can the team change it? USE depends on upstream roadmaps. BUY depends on
vendor roadmaps. BUILD gives full control. FORK gives control after the
initial fork cost.

### Total cost of ownership

Include build, run, and replace costs over the time horizon. USE: annual
maintenance hours. BUY: subscription at projected scale. BUILD: initial
build hours plus annual maintenance. FORK: merge-cost estimate.

### Speed to value

Days (USE/BUY), weeks (INTEGRATE), months (BUILD), years (large BUILD).

## One-way doors and reversibility

Some tier decisions are hard to undo. Weight your confidence bar accordingly.

- **One-way doors** (require HIGH confidence before proceeding):
  BUY with proprietary data ingestion or vendor-specific data models;
  BUILD with 12+ months of committed engineering;
  FORK of an inactive project the team must now maintain forever;
  INTEGRATE where the API owns the customer relationship.
- **Two-way doors** (MEDIUM confidence is acceptable):
  USE of a mature package with multiple viable alternatives;
  INTEGRATE with an API that has substitutes and standard schemas;
  REUSE of internal code that can be rewritten;
  BUY of a SaaS with real export tooling and open data formats.

If the decision is a one-way door and confidence is not HIGH, do not
proceed. Run more research, spike a POC, or scope-cut until it becomes
a two-way door or confidence rises. Sunk-cost bias sets in fast after a
one-way door closes.

Match the re-evaluation trigger (output section 7) to the door type. For a
two-way door, the trigger is a cheap switch point after you ship — you can
still change tiers. For a one-way door, the decisive re-evaluation happens
*before* you commit; it is the POC, spike, or scope-cut above. After a
one-way door closes, the trigger reviews mitigation and exit cost, not a
free reversal.

## Recommendation

You are a senior engineer addressing another senior engineer. Give them
everything they must know to accept or reject with confidence.

The recommendation must cite the five components. Output exactly this schema:

1. **Context** — six answers plus constraints.
2. **Tier search** — REUSE / USE / FORK / BUY / INTEGRATE / BUILD, with citations.
3. **Evidence matrix** — top 3 viable candidates. Fill all columns.
4. **Recommendation** — one tier or compound tiers.
5. **Why this wins** — concrete reasons tied to the components.
6. **Confidence** — HIGH, MEDIUM, or LOW, plus the door type (one-way or
   two-way). Use the rubric below.
7. **Re-evaluation trigger** — date, scale, event, or failure mode.
8. **Missing information** — unknowns that matter.

Rubric: HIGH = complete context, exact citations, complete matrix, minor
unknowns. MEDIUM = exact citations with known unknowns. LOW = missing
context, weak citations, thin candidates, or large unknowns. One-way doors
require HIGH regardless of the base rubric outcome.

Use this output template:

```
# Context
# Tier search
# Evidence matrix
# Recommendation
# Why this wins
# Confidence
# Re-evaluation trigger
# Missing information
```

## Compound recommendations

When a request has a commodity slice and a differentiated slice, split the
recommendation:

```
Recommendation (compound): USE X for the commodity slice.
BUILD for the differentiator slice.
```

## AI verdict mapping

When the request involves AI or ML, map the form to a tier:

| Form | Tier |
|---|---|
| Local model imported as a library | USE |
| Paid model API (chat, completion) | INTEGRATE |
| Finished AI product (Cursor, Copilot, Claude Code) | BUY |
| Open-source AI framework (Transformers, vLLM, Ollama) | USE or FORK |
| Embeddings via API | INTEGRATE |
| Embeddings self-hosted (SentenceTransformers, Instructor) | USE |
| RAG framework (LangChain, LlamaIndex, Haystack) | USE |
| Bespoke RAG pipeline | BUILD — only if retrieval quality is the product |
| Fine-tuning via API (OpenAI, Anthropic) | INTEGRATE |
| Fine-tuning self-hosted (LoRA, QLoRA on Llama, Mistral) | FORK or BUILD |
| Agent framework (LangGraph, CrewAI, Mastra, AutoGen) | USE |
| Bespoke agent orchestration | BUILD — only if orchestration IS the product |
| Managed vector DB (Pinecone, Weaviate Cloud) | BUY or INTEGRATE |
| Self-hosted vector DB (pgvector, Qdrant, Milvus) | USE |
| Prompt / eval infrastructure (promptfoo, LangSmith, Braintrust) | USE or BUY |
| Guardrails / moderation (OpenAI mod, Guardrails AI, NeMo Guardrails) | INTEGRATE or USE |
| Model observability (Helicone, Arize, WhyLabs) | BUY or USE |

Rows that list two tiers ("X or Y") resolve by the same tier-search test
used everywhere else:

- **USE vs FORK** — USE if the model or framework runs as an unmodified
  dependency. FORK if you must copy, vendor, or patch it, including
  self-hosted model weights you maintain. (Example: `whisper` run as an
  installed package is USE; a vendored, patched `whisper.cpp` is FORK.)
- **FORK vs BUILD** — FORK if you adapt an existing model or trainer.
  BUILD only if the model output itself is the differentiator.
- **BUY vs INTEGRATE** — BUY if a managed product owns the operational
  surface. INTEGRATE if you call an API and keep the surface yourself.
- **BUY vs USE** — USE if you self-host open source. BUY if a managed or
  finished product carries it for you.

Bespoke AI is almost never the answer unless the model output itself is
the differentiator. If the AI form is a commodity slice inside a larger
request, use a compound recommendation.

## Handle incomplete inputs

If context questions cannot be answered, ask. Do not guess. If no candidate
exists after a full search, state that. If all candidates fail on all
components, state that no good option exists and do not recommend a bad
option. Never fabricate a candidate or a verdict.

## Citation format

Every claim must cite its source in this exact format:

```
web_search: "<exact query>" on <date>
web_fetch: <exact URL> on <date>
grep: <path>
read: <path>:<lines>
shell: <command>
unavailable: <reason>
```

Citations without the exact query, URL, or path do not count. If a search
channel is unavailable, record `unavailable: <reason>`.

## Agent versus skill

The skill loads during normal sessions. A BUILD recommendation can precede
code generation, but the caller or user decides when implementation starts.
The agent requests read-only research where the host supports its permission
block. Use it when research must be auditable.

## What to do next

1. Write a short proposal: the decision, the evidence, the trigger.
2. Plan the smallest testable increment: POC (BUY/INTEGRATE), spike
   (REUSE/USE/FORK), or risk proof (BUILD).
3. Set a re-evaluation date proportional to the time horizon.

## The good habit

Ask these questions right after the recommendation and before the next
similar decision:

1. Did I search wide enough?
2. Did confirmation bias steer me?
3. Which component actually decided this?
4. What would prove this recommendation wrong in a year?

## Hard rules

- Never jump to BUILD without a documented search.
- Never recommend a dependency without checking its license.
- Flag copyleft and share-alike licenses for project-specific legal review.
- If a candidate is already in the repository, REUSE wins — do not propose a
  new dependency.
- If two candidates are roughly equal, prefer the one with the safer license
  and higher bus factor.
- Research must be read-only. Pair the prompt with each host's permission or
  sandbox configuration.
- Report unavailable search channels instead of claiming complete coverage.
- Citations must use the exact format. Citations without the exact query,
  URL, or path do not count.
- Never expose local files, credentials, or private repository information.

## Examples

### Example A — commodity, compound recommendation

```
# Request
Should we build our own auth, or use Auth0?

# Context
- Time horizon: 5 years.
- Scale: 10k MAU now, 500k projected. Auth0 cost steepens above ~200k MAU.
- Failure cost: catastrophic.
- Team capability and fit: strong web team; no identity engineer;
  team wants to own product surface, not auth internals.
- Commodity or core: mostly commodity; enterprise SAML may be a
  differentiated slice.
- Volatility: medium.
- Constraints: SOC 2, GDPR, likely SAML for enterprise.

# Evidence matrix
| Option    | Reliability                | Strategic value       | Adaptability      | TCO                       | Speed to value | Citation |
|-----------|----------------------------|-----------------------|-------------------|---------------------------|----------------|----------|
| next-auth | 5M weekly (npm 2026-07-22) | Neutral (commodity)   | Medium (adapters) | ~$0 + 40 hr/yr            | 1 week         | `web_fetch: npmjs.com/package/next-auth on 2026-07-22` |
| Auth0     | Billions/day (trust page)  | Weak                  | Medium (config)   | ~$25k/yr@10k MAU; scales  | 3 days         | `web_fetch: auth0.com on 2026-07-22` |
| BUILD     | Unknown                    | Zero for commodity    | High (unneeded)   | 2000 hr + 500 hr/yr       | 6+ months      | `unavailable: estimate from team planning` |

# Recommendation (compound)
USE next-auth for the commodity slice. Small BUILD layer over next-auth
callbacks for enterprise SSO, only when the first enterprise customer
asks for it.

# Why this wins
- Reliability: next-auth proven at scale (5M weekly, no critical CVE in
  2 yr).
- Strategic value: engineering time saved goes to real product work.
- Adaptability: adapters cover passkeys, OAuth, SAML.
- TCO: near zero license; no per-MAU bill.
- Speed to value: one week to production.

# Confidence
MEDIUM. Two-way door: next-auth is swappable behind standard protocols and
adapters. Re-evaluate at 100k MAU, first enterprise SSO request, or any
next-auth security incident.

# Missing information
Growth curve for cost projection; SSO timing.
```

### Example B — core competency, BUILD correct

```
# Request
Should a ride-hailing company build or buy its driver-rider matching
algorithm?

# Context
- Time horizon: 10 years.
- Scale: 500k drivers, 20M riders, ~1M requests/hour.
- Failure cost: catastrophic. Poor matching kills the marketplace.
- Team capability and fit: existing operations research and ML team;
  matching is the team's core mission, so ownership fit is high.
- Commodity or core: core competency. Matching quality IS the product.
- Volatility: high. Strategy evolves constantly.
- Constraints: regional pricing and worker-classification laws.

# Tier search (fair-search evidence)
- REUSE: none. Citation: grep "matching" in src/ — no application matching.
- USE: no npm package solves marketplace matching at scale.
  Citation: web_search "ride hailing matching npm" 2026-07-22 — no hits.
- FORK: no viable open source engine at scale.
  Citation: web_fetch github.com/topics/ride-hailing 2026-07-22 — toy
  projects only.
- BUY: no seller offers marketplace matching as a product.
  Citation: web_search "ride hailing matching vendor" 2026-07-22.
- INTEGRATE: routing APIs solve routing, not matching.
  Citation: web_fetch mapbox.com/directions-api 2026-07-22.
- BUILD: viable and expected for the industry.

# Recommendation (compound)
BUILD the matching engine. INTEGRATE routing and mapping APIs (commodities
where sellers offer proven products).

# Why this wins
- Reliability: BUILD carries unproven-code risk; every competitor faced
  the same risk. Reliability builds through iteration.
- Strategic value: matching IS the product. Only BUILD supplies this.
- Adaptability: BUILD gives full control; strategy changes weekly.
- TCO: high build cost; zero seller cost; no lock-in.
- Speed to value: 6-12 months for MVP; compounding gains over 10 years.

# Confidence
HIGH. One-way door: a multi-year committed BUILD that becomes the core of
the product; HIGH confidence is required before proceeding.

# Re-evaluation trigger
A sub-component (ETA prediction, geocoding) commoditizes, a competitor's
match quality overtakes ours, or annual review — whichever comes first.

# Missing information
None material.
```

---
name: fit-gap-analysis
description: "Compare a target (spec, product vision, competitor, RFP, or \"to-be\" design) against a system as actually built, and produce an evidence-first fit-gap — a capability matrix plus a step-by-step user-journey comparison, verified against the LIVE system (schema + code, not docs) and rolled up into decisions. Stack-agnostic (web apps, APIs, ERPs, low-code/CRM, pipelines, infra). Use whenever the user wants to compare a spec/vision/competitor to an existing system, asks \"how far are we from X\" or \"what would it take to support Y\", runs a gap analysis or COTS/package/vendor evaluation, or scopes a migration / re-platform / feature-parity effort. Trigger on fit-gap, gap analysis, capability comparison, as-is vs to-be, system comparison, feature parity, migration assessment — even when the user never says \"fit-gap\". Do NOT use for: reviewing a single diff/PR, a generic code review/audit with no target to compare against, or comparing two prose documents for wording."
effort: max
---

# Fit-Gap Analysis

Compare a **target** (spec, vision, competitor, RFP, "to-be") against a **system as actually built** ("as-is") and turn it into a meeting-ready comparison: a **capability matrix** (coverage) + a **journey comparison** (behaviour), verified against the **live system**, rolled up into a few **decisions**. Stack-agnostic.

Output quality rests on two things: how *completely* you enumerated the target, and how *honestly* you grounded each verdict in the running system. Most fit-gaps fail on the first — a capability that never makes the list can never be verified.

## When to invoke
"fit-gap" · "gap analysis" · "capability comparison" · "as-is vs to-be" · "feature parity" · "how far are we from [vision/competitor]?" · "what would it take to support [X]?" · COTS/vendor evaluation · migration/re-platform scoping · "here's the deck/RFP — what changes, what's the impact?". If the user is measuring an existing system against a target, this applies even if they never say "fit-gap".

## Principles (the *why*)
1. **Ground truth = the live system, not the docs.** Docs, wikis, diagrams, exports, READMEs drift. Verify against the running system — its live schema/contract and actual code/config.
2. **Coverage ≠ behaviour.** A checklist says *what* exists, never *how it works*. The expensive surprises live in the flow — trace the journey.
3. **Completeness beats depth — you can only verify what you enumerated.** The classic miss isn't shallow checking; it's a capability that never reached the list. Enumerate from several sources **and in both directions** (target→system = *missing*; system→target = *orphaned*), then have a critic hunt for what's left.
4. **Evidence over opinion.** Every verdict cites a concrete artifact — a field, an endpoint, a `file:symbol`, a config key, a live count.

## The steps

**1 · Build the claim list — from several sources, not one.** Smallest independently-verdict-able statements, drawn from all of:
- **a. Stated claims** — prose, bullets, captions, acceptance criteria.
- **b. The UI** — first list **every screen, state, and role** (you can't inspect a control you were never shown — note what's missing and get it). Then walk each screen **element-by-element**; for every control: *(1)* what is it? *(2)* if its value/state changes, does the **flow or a calculation** change? *(3)* does it change **other UI**? *(4)* which **field/data** feeds it?
- **c. The no-UI layer** — plugins/triggers, workflows, scheduled & cloud-flow jobs, integrations, business rules, calculated/rollup fields, duplicate-detection, audit, security, storage. Source (b) never surfaces these; report "backend reviewed" separately from "screens reviewed".
- **d. The guards** — visibility rules, business-rule conditions, enable-rules, feature flags, predicates. A static screen/role/state walk misses surfaces that appear only under specific *data* conditions.

Then a **global/cross-cutting pass** — these belong to no single screen and are the easiest to drop: identity, tenancy & **act-as/impersonation**, context-switch, search, notifications, settings, audit, export, navigation, auth, error-handling, feature flags, **i18n** (locale date/number/timezone), session timeout, environment banners.

**Source fidelity & states:** you can only enumerate what you're given — if captures are low-res/partial, *say so* and get the live prototype before claiming completeness. Record the target's version + which flows are drawn vs stubbed. Enumerate **states**, not just screens: empty, loading, error, validation-fail, no-permission, pagination.

**2 · Classify each claim by layer** — tells you *where to look* (and stops "absent" from the wrong layer): **Data/State · Logic/Rules · Integration/External · Interface/UX**. A claim often spans several.

**3 · Extract live structural ground truth** — from the running system, not the repo docs: relational app → live `information_schema` / applied migrations; API → live OpenAPI/proto/real responses; low-code/CRM → metadata endpoint; ERP/SaaS → running config; frontend → deployed routes; infra → live cloud state. For data claims, diff at the **metadata level** (columns, types, required, **option-set members & values**, lookup targets, relationships) — a form can look identical while its option set diverges. Script it if it repeats; you'll re-run before implementation.

**4 · Verify behaviour in the live code/config.** Read the actual implementation; fan out read-only explorers (one per layer/journey) if you have subagents. Confirm **semantics, not just names**.

**5 · Verdict each claim.**
- **Fit** / **Partial** / **Gap** / **Mismatch** (exists but a *different concept under the same name* → rework, not add — the trap a name match misses).
- **Prohibitions (must-NOT).** For negative requirements ("the customer must never see commission"), a capability *existing* isn't the test — verdict by confirming the prohibition is **enforced**. Unenforced = **Gap**, even if the happy-path screen looks right.
- **"Absent" is a claim you must earn.** A single pass can't prove absence (it may sit behind a role, flag, guard, scroll, or empty state). Default unproven items to **NOT VERIFIED** + the search you actually ran + a confidence; keep "spec is silent" distinct from "spec says absent".
- **Both directions.** Also verdict the reverse — live capabilities the target never mentions — classifying each **keep / intentionally-dropped / unknown**. In a port, the dangerous regressions are the legacy fields/statuses/workflows the new spec forgot.
- Separate **schema supports it** vs **configured/has data** (`[D]` = data-check) vs **UI/flow exists**.

**6 · Actors & access.** Not just *which* actor types exist (verify with live counts) but *how identity behaves at runtime* — impersonation/act-as, context-switch, dual attribution. Build a **role/identity matrix**: per privileged role, either *observe* the surface or mark **"NOT INSPECTED under role R"**. Never conclude "absent" from a single-identity session.

**7 · Trace the key journeys.** For the high-value/high-risk flows, a step-by-step **Target vs Actual** table — user action + system behaviour per step, with an artifact each. Surfaces flow divergences a matrix can't: wrong entry point, different ordering, missing step, different mental model.

**8 · Cluster + size.** Add a **Cluster** axis (*what kind of work*: Reuse / Rework / Build-new / Mixed), distinct from the verdict (*does it exist*); then **Effort (S/M/L)** + risk/dependency. Cluster collapses many rows into few decisions.

**9 · Produce multi-lens, self-explaining artifacts** — matrix + journeys + actors/access + impact/effort + open `[D]` items, with a **legend** so any reader decodes it without you. Land it where it compounds (a living doc) *and* as a working tracker (spreadsheet). The living doc follows the diagram convention (`references/diagram-convention.md`): one overview diagram up top; `sequenceDiagram` for traced journeys, `graph TD` for cluster/dependency views, `flowchart TD` for the decisions framing (step 10).

**10 · Frame as decisions, not a feature list.** Group gaps into the few choices the meeting can make; sequence by independence (greenfield + quick-wins before big rework); decide **if** before **how**.

## Completeness gate — before you ship
You verified everything *on the list*; now attack the list. Re-scan the source asking **"what is visible or implied that isn't a row yet?"**, hunting the predictable blind spots from step 1 (UI chrome, global/cross-cutting, the no-UI layer, guarded/conditional surfaces, prohibitions, screens/states/roles you weren't shown). A second pair of eyes catches in seconds what the author's framing hid.

## Verdict vs Cluster (don't conflate)
**Verdict** = *does it exist?* (diagnosis). **Cluster** = *what kind of work?* (treatment). The same Gap can be a cheap additive build *or* part of a risky rework — keep both axes.

## Pitfalls (quick-ref)
| Pitfall | Guard |
|---|---|
| Enumerating from prose only | walk every control element-by-element (1b) |
| UI-only enumeration | a no-UI-layer pass (1c) + a guards pass (1d) |
| Stage/screen-organized list | a global/cross-cutting pass (step 1) |
| Only the screens/states/roles you were shown | enumerate them first; flag what's missing |
| Trusting the docs | re-pull from the live system |
| Same-word trap | verify semantics in code, not names |
| Prohibition scored "Fit" | verdict must-NOTs by *enforcement* |
| "Absent" from one identity/state | default NOT VERIFIED + record the search |
| Visual form diff only | diff metadata (types, option-set values, relationships) |
| Reverse-direction blindness | diff both ways; classify every live-only capability |
| "The matrix is enough" | trace the journeys |
| Schema = reality | flag `[D]`; check it's configured/populated |

## Output checklist
- [ ] Claim list from all sources: stated + UI element-by-element + no-UI + **guards**
- [ ] Global/cross-cutting capabilities enumerated (identity, act-as, search, settings, audit, export, i18n…)
- [ ] Per control: *what it is · changes flow/calc? · changes other UI? · which field feeds it*
- [ ] **Both directions** diffed — live-only/orphaned classified (keep/dropped/unknown)
- [ ] **Prohibitions** verdicted by enforcement, not by a clean-looking screen
- [ ] Every verdict cites a live artifact; unproven "absent" = **NOT VERIFIED** + the search run
- [ ] Data claims diffed at **metadata level**; roles covered (observe or NOT INSPECTED); non-happy states sampled
- [ ] Key **journeys** traced (Target vs Actual); **Layer + Cluster + Effort** on each row
- [ ] **Source fidelity** flagged; missing screens/states requested
- [ ] **Completeness gate** run (second adversarial look); **legend** included; gaps → **decisions**
- [ ] **Diagram convention** followed in the living doc (overview diagram + type-matched sections)

## Optional dimensions (include if relevant; else mark *out of scope* so the choice is conscious)
- **Lifecycle / state-transitions** — per entity, statuses + the actions driving transitions; verify each transition the target implies, not just the initial state.
- **Non-functional** — perf/SLA, concurrency/locking, security (token/CORS), audit/retention, accessibility, offline.

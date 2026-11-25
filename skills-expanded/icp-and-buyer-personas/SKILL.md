---
name: icp-and-buyer-personas
description: "Define ICP, buyer personas, buying committees and anti-personas within an accepted market. Use for ideal customer profiles, persona research, buying roles and exclusion criteria. Propose audience changes through SSOT governance."
metadata:
  version: 1.5.0
---

# ICP and Buyer Personas


**Use the company SSOT when present:** follow `../_shared/ssot-consumption.md` and the project manifest to load only relevant approved context. Preserve covered strategic meaning while keeping this skill’s existing scope and frameworks.

You build personas that change decisions. A persona earns its place only if it changes what the team says, where it shows up, or who it sells to. Demographic filler does not.

Deliver the personas themselves, not a template for making them.

## Context research handoffs

When receiving a context-establishment handoff, read
`../_shared/context-establishment.md`. Reuse its question, scope, source/finding
IDs, approved context/version, GAP IDs and completion criteria. Analyze only your
owned domain; return provenance-bearing findings, opposing evidence, limitations,
completion status and unapproved implications to product-marketing-context.
Use decision-specific evidence readiness; approval is separate. A hold affects
only its decision. Do not write canon or automatically save chained results into
bootstrap context. Standalone artifacts retain their existing format and may
attach the shared return. Preserve IDs and status without duplicating studies.

## Ownership and accepted market

Own ICP, personas, buying committees and anti-personas within accepted market selection.
Inherit the accepted market; do not use persona work to select another market.
Proposed ICP or persona changes require `ssot-context-loop` governance and human approval.
Include fit/exclusion criteria, committee roles, evidence confidence and gaps in the output.


## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists (or `.claude/product-marketing-context.md` in older setups), read it before asking questions.

**Check for an existing segment decision before selecting an ICP.** Look for an
accepted market-entry brief for the same company and market, and read the
manifest-mapped SSOT ICP/decision context using `../_shared/ssot-consumption.md`.
If an accepted brief already selected a segment and it does not conflict with
canonical SSOT, use that segment for persona work. Do not independently rescore
or choose a different market. An `Explore` decision means the segment remains a
hypothesis; a `Pass` is not the current target. If the brief and SSOT conflict,
flag the conflict and route it through `ssot-context-loop` for review. Do not
silently prefer a newer brief or overwrite the canonical ICP. Reopen prioritization
through `market-entry-brief` only when the user explicitly asks to reconsider it.

Find out which mode applies:
- **Reuse mode:** an applicable approved or suitable provisional persona exists
  and the request is to use it. Load it read-only, preserving the full-source
  reference, evidence/approval status, available version, confidence and gaps.
  Downstream owners may load this source directly; no persona rerun is required.
  Return the reference and relevant intelligence without rebuilding or rescoring.
  Readiness governs provisional use; reuse never approves or writes anything.
  Skip generation and validation-plan creation. Revision requests produce
  distinct proposals, never silent replacements of approved meaning.
- **Evidence mode:** the user has interviews, call notes, CRM data, win-loss, or surveys. Build from those.
- **Hypothesis mode:** little or no research. Draft personas with attributes labeled Assumed or Gap, then give a plan to validate them.

The generation process and output/save requirements below apply only to evidence
and hypothesis modes. Reuse mode returns the existing reference/profile, its
status and relevant gaps without generating a new message map or persona.

If key intelligence is missing, assess decision-specific readiness before
proceeding provisionally. State assumptions, risk, permitted scope and validation
triggers; hold only choices without a defensible provisional route.
For generation, open with the message map, then inherited or exploratory scope.
Keep a summary of at most five bullets: material assumptions and questions.
This summary cap never erases attribute uncertainty or underlying evidence gaps.
The validation plan's interview questions do not count toward the summary cap.

When no accepted market-entry/SSOT decision establishes the market, route market
selection to `market-entry-brief`. Persona hypotheses may remain provisional,
with that dependency explicit; they do not select or approve a new market.
When an accepted decision exists, consume it and skip market selection.

Label every persona attribute Sourced, Assumed, or Gap, as defined in the Labels section of `../_shared/evidence-gaps.md`. Never present a guess as research. Never invent quotes. If you use a quote, it must come from the user's material.

## Core Principles

**Start qualitative, validate quantitatively.** Interviews reveal the real segments and language. Surveys then show how many buyers self-select into each. Doing it in the other order produces tidy but wrong personas.

**Four attributes matter most.** Background, pain points, discovery channels, and evaluation process. These drive messaging, channel, and sales decisions. Age and hobbies rarely do.

**B2B buys by committee.** Map the user, champion, decision maker, financial buyer, and technical influencer. Each needs a different reason to say yes.

**Name the anti-persona.** Say who looks like a fit but is not, and why. This saves sales time and sharpens messaging.

## Process

### 1. Establish profile scope
Inherit the accepted market/SSOT segment, its source and approval status. When
no market is accepted, profile explicit exploratory candidates or buyer hypotheses
without ranking/selecting a lead. Route market comparison/selection to
market-entry-brief. Customer-research can collect exploratory evidence before
market acceptance; do not send research back for an approved market prerequisite.
Read `../_shared/segment-selection.md` only for shared context/consistency when
needed; persona work does not run its selection scorecard.

### 2. Profile each persona
Cover: role and background, trigger events, pain points in their words, discovery channels, evaluation process, objections, what success looks like to them, and their role in the buying committee.

Extend these existing attributes rather than duplicating them:
- Background includes responsibilities and organizational context.
- Success includes the functional, emotional or social job and desired outcomes
  when evidence supports them.
- Evaluation process includes buying context/stage, decision criteria,
  requirements, trade-offs and disqualifiers.
- Objections includes skepticism, perceived risk and switching anxiety.
- Committee role includes influence, authority and internal approval needs.

Also capture stakes (failure consequences, internal pressures and incentives),
current behavior (workarounds, alternatives/status quo and why they persist),
proof requirements (what would make claims credible), and supported practitioner
language. These are distinct from pains, available company proof and brand voice.
Do not invent facts or quotes. Keep observed/source-linked evidence separate
from interpretation and assumptions; include confidence and unknowns by attribute.
A task's specific stage or situation is selected downstream, not assumed to
apply to every member of the persona.

### 3. Map the buying committee
Show who starts the purchase, who blocks it, who signs, and what each needs to hear.

When the incumbent relationship belongs to one team and the new application is
sponsored elsewhere, separate the infrastructure owner, application/business
outcome owner, technical evaluator, sponsor and budget holder. Roles may overlap;
do not infer authority from a title or an existing vendor relationship. Capture
who introduces the vendor, who funds the evaluation, whose success criteria
conflict, and what agreement lets the purchase advance. Mark unverified roles as
Assumed or Gap. Carry this split into the message map and sales implications.

### 4. Define the anti-persona
Describe the look-alike buyer who churns, stalls, or costs too much to serve.

### 5. Plan validation
For hypothesis-mode personas, write the five to eight interview questions that would confirm or kill each one. Cover role, awareness, evaluation, requirements, alternatives considered, and the buying committee. End with: "If you were CEO, what would you do to compete better?" Suggest a short survey to size each segment afterward.

### 6. Write the persona message map
Summarize the persona profiles and the committee map in one table. It opens the output. Write it last, from the finished profiles.
- **Persona:** the role-based name, with the buying role in brackets, such as (champion), (evaluator), or (financial buyer).
- **What matters to them:** 1 to 2 short phrases naming the priorities that decide the deal for this persona. Examples: conversion rate, compliance, compute cost, integration effort.
- **Message:** the core message for this persona in 1 to 2 sentences, tied to a proof point with its label (Sourced, Assumed, or Gap). It is the argument that wins them over, not an opening line or hook.
- **Language:** no "X, not Y" or "Do this, not that" constructions, no clichés (unlock, seamless, game-changer, leverage, revolutionize, next-generation), and no em dashes.

## Output Format

```
## Persona message map
| Persona | What matters to them | Message |
|---|---|---|
| [Role-based name] (champion) | [1 to 2 short phrases] | [Core message, 1 to 2 sentences. Proof: [proof point] (Sourced / Assumed / Gap)] |

## Market / profile scope
[Inherited segment, source decision/status and conflict check; or explicit exploratory candidates with market-selection dependency. No independent lead selection.]

## Persona: [Role-based name, not a cute alias]
Source/reference: [project, source path/section]. Version/review date: [... or Gap].
Approval: [approved / proposed / hypothesis / unknown, with approval reference].

| Attribute | Detail | Source / label | Confidence / gaps (where relevant) |
|---|---|---|---|
| Background / responsibilities | | Sourced / Assumed / Gap | |
| Trigger events | | | |
| Pain points | | | |
| Stakes / internal pressures and incentives | | | |
| Current behavior / alternatives / status quo | | | |
| Discovery channels | | | |
| Evaluation process / buying context and criteria | | | |
| Objections / skepticism and perceived risks | | | |
| Proof requirements | | | |
| Supported practitioner language | | | |
| Success looks like / jobs and desired outcomes | | | |
| Committee role / influence and authority | | | |

Use relevant attributes; mark applicable unknowns as Gap and omit irrelevant
rows. Preserve existing rich profiles. No numerical confidence score or completed
irrelevant field is required.

**What this changes:** [the messaging, channel, or sales decision this persona drives]

## Buying committee map
## Anti-persona
## Validation plan
## Assumptions and open questions
[At most 5 bullets combined, one line each. The assumptions that most affect the answer first, then the 2 or 3 questions that would change it.]
```

Use role-based names like "RevOps Lead at a Series B SaaS company," not invented names like "Marketing Mary." Invented names hide weak detail.

## Common Failure Modes

- Personas built from demographics instead of buying behavior.
- Assumed attributes presented as Sourced findings.
- Too many personas. Three is usually enough for one product.
- Personas that do not change any decision.
- Skipping the buying committee in B2B.

## Account-level handoff

`account-based-marketing` consumes the accepted ICP and persona/committee model
for account selection, tiers, contextual hypotheses, and coordinated plays.
Personas owns the reusable buyer model; ABM owns account-specific application.
All audience-dependent execution owners consume this model through
`../_shared/ssot-consumption.md`. Persona work supplies intelligence and the
reusable message map, not outbound copy, event formats, campaigns, channel
mechanics or collateral. Existing maps are inputs, not universal final asset copy.

## After Delivering

For PMC-originated work, return full profiles/map and proposal references for
integration; do not automatically save into bootstrap context. Reuse never writes.

For standalone generation, retain existing default saving to the Personas and
Persona message map sections of `.agents/product-marketing-context.md` and tell
the user what was saved. Preserve full attributes, committee/anti-persona detail,
provenance, confidence/gaps and actual approval status; summaries do not replace
profiles. Do not overwrite approved meaning or duplicate covered canonical facts:
reference applicable SSOT profiles instead. Keep uncovered hypotheses provisional.

Revisions remain distinct proposals in the existing context section when saving
is authorized. Preserve the original profile, proposed differences and evidence;
route canonical changes through `ssot-context-loop` and human approval.
Saving does not approve strategy. Do not create another persona store.
Suggest positioning-strategy or messaging-framework as next steps where relevant.

## Output Rules

- No em dashes in output.

## Related Skills

- **customer-research**: Gather and synthesize the interviews personas depend on
- **positioning-strategy**: Use the primary persona as the best-fit customer
- **messaging-framework**: Translate messaging for each persona
- **sales-enablement**: Build persona-specific talk tracks and objection handling
- **product-marketing-context**: Save personas so every skill uses them

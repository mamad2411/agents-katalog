---
name: documentation-extraction
description: Use this skill when the user asks to turn closed tickets, Slack threads, meeting notes, PR descriptions, or email exchanges into durable documentation such as feature docs, runbooks, architecture decision records, or onboarding material. Trigger phrases include "document this feature", "write a runbook from these tickets", "extract docs from this thread", "documentar esto", "pasar a documentación", "write this up". Produces a document structured by surface or topic, not by chronology, with linked primary sources.
---

# documentation-extraction

> **Anchor:** A doc is not a transcript. Extract the signal, drop the debate.

## When to use

Use this skill when the user needs to convert scattered artifacts into durable documentation. Works for:

- A feature that shipped without a doc, now needed for handoff or support.
- A runbook built from incident retro notes and Slack threads.
- An architecture decision record pulled from a design thread.
- An onboarding page assembled from closed onboarding tickets.
- A troubleshooting guide assembled from recurring support patterns.

Do not use when:

- The user is writing a PRD for unshipped work. Use `prd-authoring`.
- The user is running a post-mortem. Use `post-mortem`.
- The user is doing a full knowledge base migration. That is a project, not a skill.

## Voice rules (apply to all outputs)

- No buzzwords: leverage, empower, synergy, resonate, tapestry, delve, elevate, captivate, explore, dynamic, testament.
- No em dashes.
- No filler openings.
- Decision-oriented over descriptive.
- High-context, no overexplaining.
- Standard sentence case for formal outputs.
- ES outputs match the register of the handbook: direct, self-aware, no reverence for process, comfortable naming failure.
- EN outputs use direct US business register. Do not soften bluntness into corporate-speak.
- Language switches based on audience, not author.

## Bilingual handling

- **ES.** Rioplatense register. Vos over tú. Keep standard terms in English: doc, runbook, ADR, changelog, onboarding, handover, FAQ, troubleshooting, incident, escalation.
- **EN.** Direct US business register.
- Source links and ticket IDs stay in their original form. Quotes from sources stay in their original language.

## Method

### Step 1. Pick the doc type before anything else

The doc type decides the structure. Options:

- **Feature doc.** Describes what the feature does, for whom, how to use it.
- **Runbook.** Step-by-step for a recurring operational task.
- **ADR.** Architecture decision record. Why a choice was made, what was considered, what changes it.
- **Troubleshooting guide.** Symptom, cause, fix.
- **Onboarding page.** First-week reading for a role or team.
- **Policy or standard.** Binding rule with examples.

If the user does not name a type, pick one and state it in the first sentence. Mixing types produces documents no one reads.

### Step 2. Pull primary sources

Collect every artifact that feeds the document:

- Ticket IDs with resolution text.
- Slack or chat threads with timestamps.
- PR descriptions and review comments.
- Meeting notes.
- Email threads.
- Prior doc versions.

List the sources in the doc itself, at the bottom. Any fact in the doc should be traceable to one of them.

### Step 3. Separate signal from noise

Sources are 80% noise for documentation purposes. Drop:

- Social lubrication ("thanks", "great point", "circling back").
- Internal debate that resolved. The resolution is the fact.
- False starts and abandoned options. Unless the doc is an ADR, the options are noise.
- Personal opinions unattributed to a role.

Keep:

- Decisions.
- Constraints that shaped decisions.
- Behaviors of the system.
- Gotchas that burned someone.
- Explicit contracts between teams, services, or features.

### Step 4. Structure by surface, not by chronology

The single biggest failure mode is writing documentation that tells the story of how the feature was built. No one reading the doc cares.

Structure by:

- **Feature docs.** What it does. Who it is for. How to use it. Edge cases. Limits.
- **Runbooks.** Preconditions. Steps, numbered. Expected outcome. Recovery if a step fails.
- **ADRs.** Decision. Context. Options considered. Consequences. Date and signer.
- **Troubleshooting.** Symptom table, each row pointing to cause and fix.
- **Onboarding.** What you need to know by end of day one, week one, month one.

Chronology is valid only in an ADR and a post-mortem.

### Step 5. Name the owner and the review cadence

Documents without an owner go stale. At the top of the doc:

- **Owner.** Named person.
- **Last reviewed.** Date.
- **Review cadence.** When the owner re-reads and revises.
- **Deprecation signal.** What would cause this doc to be retired.

### Step 6. Link back to primary sources

The doc ends with a "Sources" section. Every ticket, thread, PR, or meeting that informed the doc is listed.

This does three things:

- Makes the doc auditable.
- Gives the reader a path to deeper context if needed.
- Makes future maintenance easier when the topic changes.

### Step 7. Flag gaps

The doc will not cover everything. Write down what it does not cover, at the bottom, before sources. Examples:

- Known gotchas not yet reproduced reliably.
- Behaviors that happen only in production under load.
- Interactions with other systems that should be documented elsewhere.

A doc with no flagged gaps is either complete (rare) or pretending.

## Templates

- `templates/en/feature-doc.md`: feature documentation.
- `templates/en/runbook.md`: operational runbook.
- `templates/es/feature-doc.md`: documentación de feature.
- `templates/es/runbook.md`: runbook operativo.

## Related skills

- `prd-authoring`: use it instead when documenting unshipped work that needs a spec.
- `post-mortem`: use it when the source is an incident and you need a retro, not a doc.
- `ticket-triage`: use it when the source artifacts are an open queue that needs dispositions first.

## Anti-patterns

This skill must never produce:

- A document structured as a timeline of the feature's creation.
- A runbook that describes why the runbook exists instead of the steps.
- A doc with no owner.
- A doc that copies Slack threads verbatim.
- A doc that includes social lubrication.
- A doc that references "recent discussion" without a link.
- A doc that tries to be a feature doc and a runbook at once.
- An ADR that does not name the options considered.

## Checklist before delivery

- [ ] Doc type is named in the first sentence.
- [ ] Structure follows the chosen type.
- [ ] Every claim is traceable to a listed source.
- [ ] Owner and review cadence are named.
- [ ] Gaps section exists.
- [ ] No direct quotes longer than two sentences.
- [ ] No buzzwords from the voice rules appear.

---
name: drafting
description: Use when a mindpowers spec exists and the user wants the actual deliverable written, such as "draft it", "write the memo from the spec", or right after mindstorming locks a spec. Not for code; not for drafting without a spec (offer mindstorming first).
---

# Drafting

## Overview

The second step in the mindpowers loop: shape (mindstorming) -> draft (drafting) -> review (reviewing-docs) -> remember (calibrating). Mindstorming turns a rough idea into a locked spec. Drafting turns that locked spec into the finished document, holding it to the standards baked into the matched template.

Drafting does not re-litigate the spec. The thinking already happened. This skill's job is faithful, high-quality execution: realize every section, honor every exclusion, apply the template's hard requirements, and flag any deviation instead of silently making one.

## User-Facing Language

Think precisely; respond plainly. Use common words and short sentences. Explain
an unavoidable technical term the first time it appears, and give one short
example when a rule could be misunderstood. For a material conclusion about the
draft, a blocker, or a deviation, give a compact explanation: the recommendation
or conclusion, what you checked, the main reasons, uncertainty, and the next
step. Do not dump internal machinery. If the user says the explanation is
unclear, explain it again from scratch.

## Input Contract

This skill needs a spec with `status: locked` from `docs/mindpowers/specs/`.

1. **Find the spec.** Use the one the user names, or the most recent spec in `docs/mindpowers/specs/` if the request is ambiguous (e.g. "draft it" right after a mindstorming session). Also check legacy `docs/brainstorm/` if it exists and nothing newer is in `docs/mindpowers/specs/`.
2. **Status is `draft`.** Do not draft from it. Tell the user the spec isn't locked yet, and ask whether to lock it now or go back to mindstorming to finish shaping it.
3. **Status is `superseded`.** Warn the user this spec was superseded (and by what, if the frontmatter or a newer spec says so). Confirm they still want to draft from it before proceeding.
4. **No spec exists for the ask.** Do not draft cold. Give one short pitch for shaping the audience, goal, and constraints first, something like "I don't see a spec for this. Want to shape the audience, goal, and constraints first so the draft has something clear to follow?" If the user confirms, switch to `mindstorming`; do not switch before confirmation. Respect whatever the user decides. If they insist on skipping it, draft anyway, but say plainly that the quality bars (audience fit, standards, anti-pattern checks) will be weaker without a spec to hold the draft to.

A locked spec approves the working brief for drafting. It does not establish content readiness or grant external approval. A locked spec may therefore have `readiness: not-ready`. When the user asks to proceed from one, draft it while keeping the deliverable provisional: preserve the spec's readiness value, evidence qualifications, material blocking gaps, and external-review status. Keep `readiness` limited to `ready | not-ready`; never encode approval in it. Do not polish any of these states into unsupported certainty, readiness, or approval.

## Process

1. **Read the spec and its template.** Load the spec file, then load `skills/mindstorming/references/<type>.md` using the spec's `type` frontmatter field. If `type` is `self-shape`, there's no template file to load; draft against the spec's own sections instead.
2. **Draft against the template's standards.**
   - Treat the template's "Standards baked in" as hard requirements, not suggestions.
   - Treat the template's "Anti-patterns" as blockers: if a draft would land in one, rewrite it before showing it to the user.
   - Every section the spec calls for must show up in the draft. Don't drop one because it seems thin.
   - Nothing the spec explicitly excluded may appear. This matters most for comms-draft specs with a "What NOT to say" section: those exclusions are as binding as the inclusions.
   - Pull audience and tone from the spec's frontmatter and carry them through the whole draft, not just the opening line.
3. **Run the draft self-review checklist** (mirrors mindstorming's spec checklist, applied to the draft instead of the spec):
   - [ ] Is every spec section realized in the draft?
   - [ ] Is everything the spec excluded actually absent?
   - [ ] Does the draft match the spec's stated audience and tone?
   - [ ] Are the template's anti-patterns absent (e.g. insight before data for business-reviews, recommendation up front for decision-docs)?
   - [ ] Is every claim traceable to the spec or clearly flagged as new information introduced during drafting?
   - [ ] Does the draft preserve readiness, material blockers, evidence qualifications, and external-review status without implying unrecorded certainty or approval?

   Fix what you can inline before showing the draft. Anything you can't fix without more input, flag rather than silently paper over.
4. **Report the checklist results inline.** When you hand the draft to the user, list what the self-review checked and what it found, including any deviations from the spec and why. Don't bury this in a preamble; make it visible.
5. **Save the draft.** Following the file contract:
   - Path: `docs/mindpowers/drafts/YYYY-MM-DD-<type>-<slug>.md`, same date and slug as the spec so the pair sorts together.
   - Frontmatter: `spec: <path to the spec>`, `type`, `status: draft` (or `final` once the user says it's done), and `readiness: <value from the spec>`.
   - Keep material blockers visible in the draft body and the handoff report. When readiness is `not-ready`, retain the provisional `status: draft` label rather than presenting the document as final.
   - Preserve external review and approval status in a clearly labeled body section such as `External reviews and approvals`, unless the selected template defines a dedicated field. Never put approval state in `readiness`.
   - Update the spec's own frontmatter with `draft: <path to the draft>` so the link goes both ways.
   - **Comms exception:** for short comms (a Slack message, a brief email), present the draft in chat instead of writing a file. Only save a file if the user asks for a record.
6. **Handoff.** Ask: "Want to revise this, review it, or call it done?" If the user chooses review, switch to `reviewing-docs`; do not switch before that confirmation. When the draft carries checkable claims (numbers, dates, names, quotes), also mention that `fact-checking` can verify them against sources before the doc ships; recommend it, don't run it unasked.

If your harness has a task list, track these steps as todos so nothing gets skipped mid-draft; if it doesn't, just work through them in order.

## Template-Aware Quality Bars

The template reference file is the source of truth, but a few examples of what "hard requirement" means in practice:

- **business-review**: insight before data. Lead with what changed and why it matters, then back it with numbers. Don't open with a metrics dump.
- **decision-doc**: recommendation up front, in one sentence, before the reasoning.
- **prd**: preserve every `US-###`, `REQ-###`, `AC-###`, and `OD-###` identifier; keep evidence qualifications intact; ensure each requirement links to a verifiable acceptance criterion; include every triggered conditional contract; and never call the PRD `build-ready` while a blocking product decision remains open.
- **briefing-doc**: the asks or decisions sought are explicit, not left for the reader to infer from context.
- **comms-draft**: one key message, matched to the stated tone, with every "What NOT to say" item actually absent from the draft.
- **framework**: principles are illustrated with concrete examples, not left abstract.
- **talking-points**: punchy and built for verbal delivery: short lines, anticipated questions paired with pithy answers, not paragraphs.
- **post-mortem**: blameless framing, a factual timeline, and concrete follow-up actions rather than vague "we'll be more careful" language.

If the spec's `type` is `self-shape`, there's no reference file with baked-in standards to enforce; hold the draft to whatever structure the spec itself laid out, and use ordinary judgment (clarity, no padding, claims traceable to the spec) in place of template-specific rules.

## Confidentiality

These drafts inherit the same sensitivity as their specs: leadership comms, OKR politics, exec briefings often land here in prose form, which is more exposed than a spec's bullet points. If the working folder is a shared or public git repo, warn the user before writing the draft file and suggest adding `docs/mindpowers/` to `.gitignore` or choosing a private location instead.

## Cowork / No-Filesystem Fallback

Paths above are relative to the working folder. In Cowork, that's the user's shared folder. If no writable folder exists, present the full draft in chat (or as an artifact) and say plainly that it was NOT saved to disk. This doesn't relax the process: the draft still needs to satisfy the self-review checklist and get reported the same way.

## Key Principles

- **The spec is the brief, not a suggestion.** Every section it calls for gets realized; every exclusion it names gets honored.
- **Faithful execution over creative reinterpretation.** Drafting isn't a second brainstorm. If the spec seems wrong once you're drafting from it, say so and flag it. Don't quietly redesign the deliverable.
- **Standards are hard requirements.** A template's "Standards baked in" aren't nice-to-haves; treat them the way you'd treat a spec requirement.
- **Deviations are flagged, never silent.** If the draft departs from the spec anywhere, say where and why in the self-review report.
- **Don't draft cold by default.** No spec means weaker quality bars: say so, and offer mindstorming once before proceeding without one.

## Anti-Patterns (Never Do)

- Drafting from a spec with `status: draft` without asking the user to lock it first
- Adding sections, examples, or content the spec didn't call for
- Padding a thin section to make the draft look more complete than the spec actually specified
- Ignoring the template's standards (e.g. burying the recommendation in a decision-doc, leading with data instead of insight in a business-review)
- Including anything the spec's exclusions ruled out (most commonly, saying something the comms-draft's "What NOT to say" flagged)
- Silently deviating from the spec instead of flagging the deviation inline in the self-review report
- Treating "no spec exists" as a green light to draft cold without at least offering mindstorming once
- Polishing qualified evidence, unresolved blockers, pending external review, or `readiness: not-ready` into false certainty, readiness, or approval

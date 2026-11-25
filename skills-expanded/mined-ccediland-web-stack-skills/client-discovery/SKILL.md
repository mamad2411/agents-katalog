---
name: client-discovery
description: Turn whatever a client gives you — a conversation, a written doc, a sketch or wireframe, a design-tool export — into a structured, feasibility-checked site brief plus a deferral register the owner decides on. Use when starting with a new client, running a discovery call or client interview, doing client intake for a website, gathering site requirements, or writing the site brief a build will compose from. Four phases — interview-first intake over a question bank (an exportable form covers async clients), capture by input format, per-item feasibility verdicts against the composition authority, and deferrals recorded in the site repo. It captures intent and emits the brief — never designs, renders, or produces mockups — visual generation is downstream (Claude Design). A SITE brief, not a brand brief — scoping a brand's identity or voice goes to brand-canon-scoper. Feasibility facts live in stack-integration-playbook; composing the catalog subset FROM a finished brief is the playbook's job, not this skill's.
---

# client-discovery

> The client layer of the catalog: everything between "we have a new client" and "we have a brief a build can compose from". The skill's product is two artifacts — a structured brief validated item-by-item against what the catalog can actually deliver, and a deferral register that turns every gap into an explicit owner decision instead of a silent omission. It captures intent; it NEVER designs or renders.

## Reference materials — load when relevant

This SKILL.md is the four-phase discipline and its boundaries. Load references only when their content is needed:

- `references/question-bank.md` — load when running an intake interview or reviewing coverage: the full question bank by domain (business, audience, content, functional, brand, measurement), each question tied to the catalog skill that consumes its answer.
- `references/brief-schema.md` — load when emitting the brief or the deferral register: the section-by-section schema of both artifacts, the per-item verdict format, and the emission rules.
- `references/intake-form.md` — load when the client works async: the exportable written form derived from the question bank, ready to send as-is.
- `references/worked-example.md` — load to see the whole pipeline once: the retroactive brief of the Furever fixture (real client material in, structured brief with verdicts and deferrals out).

## TL;DR

- Interview first, form as fallback: the question bank is a COVERAGE structure, not a script — an adaptive conversation beats a static form whenever the client is live, and the exportable form exists for async clients.
- Every brief item gets one of four verdicts — feasible-as-is, feasible-with-flip, deferred, out-of-scope — issued by running the item against the playbook's canonical order, capability map, and seams. The facts live there; this skill supplies the verdict FORMAT and the discipline of issuing one per item.
- Deferrals are owner decisions, not omissions: each records what was cut, whether it is aesthetic or functional, the owner's call with context, and the condition that reopens it. The register lives IN THE SITE REPO — this skill only emits the schema.
- Hard line: this skill produces requirements and handoffs, never pixels. A sketch becomes requirements plus a visual handoff note; it does not become a mockup here.

## The four phases

| Phase | Input | Output | Reference |
|---|---|---|---|
| 1. Intake | A live client, or none (async) | Covered question bank | question-bank / intake-form |
| 2. Capture by format | Whatever the client gave | Normalized requirements | below |
| 3. Feasibility | Requirements | Per-item verdicts | brief-schema + the playbook |
| 4. Deferral | Verdicts with gaps or cuts | Deferral register in the site repo | brief-schema |

The phases are a pipeline, not a meeting agenda: a single call can advance all four, and an async client may take a week between 1 and 2. The brief is DONE when every requirement carries a verdict and every cut carries a deferral entry.

## Phase 1 — Intake (interview-first, form as fallback)

- Default mode is a conversation: work through the question bank adaptively — follow the client's thread, skip what their material already answers, and use the bank as a coverage CHECKLIST at the end, never as a script read aloud. The operator of this skill is an interviewer; a static form wastes that.
- The bank covers six domains — business, audience, content, functional, brand, measurement — and every question exists because a catalog skill consumes its answer. A question no skill can act on does not belong in the bank.
- Async fallback: export `references/intake-form.md` and send it. When it comes back, treat the answers as phase-2 written input and run the coverage checklist over them — async answers are usually thinner, so expect a follow-up round on the gaps.
- Do not over-collect: the bank's STOP rule is that once the primary conversion, the content inventory, the brand source, and the edit expectations are known, phase 2 can start. Everything else can arrive later without blocking.

## Phase 2 — Capture by format

Clients hand over intent in four shapes; each has a capture path and none of them ends in this skill rendering anything:

- Conversation or written doc — extract requirements directly into the brief schema's sections. Quote the client's own words for anything that smells like a business rule (truth-gating downstream needs the source).
- Sketch, wireframe, or screenshot of a site they like — extract STRUCTURAL requirements (sections, hierarchy, navigation, content types) into the brief, and record the visual intent as a handoff note (what the client pointed at, what they said about it, the artifact itself attached). The handoff note is consumed by the visual-generation stage downstream (Claude Design); producing the mockup is NOT this skill's job, and reproducing a competitor's design verbatim is flagged, not captured.
- Design-tool export (Figma/Penpot file, exported tokens) — route by what it contains: a token export enters the token pipeline (astro-css-tokens directly, or the brand pipeline when a canon should exist first); a layout file is treated as the sketch case above. The export is INPUT to the brief, never a contract the build must pixel-match — say so to the client at capture time.
- No material at all — the interview IS the material; phase 1's coverage checklist decides when there is enough to write the brief.

## Phase 3 — Feasibility (verdicts by reference)

The feasibility FACTS — what the catalog can build, in what order, at what cost, with which seams — live in stack-integration-playbook (canonical order, capability map in `stack-integration-map.md`, recipes). This skill does not duplicate a line of them. What it adds is the verdict discipline: every brief item is run against that authority and stamped:

- feasible-as-is — a catalog skill or recipe covers it; name which one.
- feasible-with-flip — covered, but only through a documented flip (a deploy-shape change, a paid tier, a promotion trigger); name the flip and its cost so the owner decides consciously.
- deferred — buildable but cut for now (scope, budget, missing content, pending governance); goes to the deferral register with its reopening condition.
- out-of-scope — the catalog does not do this (or does it only past a documented frontier, like the client-portal boundary); say where it would live instead.

A brief with unstamped items is not done. When an item's verdict needs a fact the playbook does not carry, that is a playbook gap to report — not a license to guess here.

## Phase 4 — Deferral register

- Home: a section or file IN THE SITE REPO (same pattern as the brand contract's projections — the catalog supplies schemas, consuming projects hold state). This skill emits the schema; the register belongs to the site.
- Every entry records — the item, aesthetic-versus-functional, who deferred it and why (the owner's decision WITH its context, quoted), and the revisit condition (a date, a metric, a governance event).
- Aesthetic deferrals and functional deferrals age differently: an aesthetic cut rarely blocks anything downstream; a functional cut (no analytics, no legal page) usually has a skill whose discipline it violates — record WHICH, so the revisit condition is honest.
- The register is read at every later composition pass: recipes and the playbook's verification discipline treat an open functional deferral as a known hole, not a surprise.

## Boundaries

- This skill captures intent and produces the brief plus handoff notes. It NEVER designs, renders, wireframes, or generates mockups — visual generation is a downstream stage (Claude Design in this stack), and its input is this skill's output.
- A SITE brief is not a BRAND brief: when the conversation turns out to be about the brand's identity, voice, palette, or tokens ("who are we", not "what does the site do"), hand off to brand-canon-scoper — and when a site brief needs a brand that does not exist yet, that is a scoper-then-builder detour recorded in the brief, not a reason to improvise brand decisions here.
- Composing the build FROM a finished brief — picking the subset, sequencing skills, wiring the stack — is stack-integration-playbook. The brief is this skill's last artifact; the first composition pass is the playbook's first.
- Owner-decides is absolute: deferrals record decisions, they never make them; a client "no" with context beats any best practice this catalog carries.

## Limitations and out-of-scope

- No pricing, proposals, or contracts — discovery feeds those, this skill does not write them.
- No project management: the brief is a requirements artifact, not a timeline.
- The question bank assumes the web-stack catalog is the delivery target; discovering for a different stack means re-deriving the bank's skill ties, not reusing them blind.
- Nothing here is client-specific: names, answers, and registers belong to the consuming project's repo.

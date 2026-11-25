---
name: dossier-generator
description: >
  Turn a built system plus a client/deal context into three linked artifacts: a dual-format
  dossier (human executive summary + agent-facing implementation spec), a customer-acquisition
  research package, and a talk-through deck. Use when packaging an engineering build into a
  sellable, consumable artifact, or whenever the goal is "I built something, get a deal or a
  case study out of it." This is the anti-circling machine: it converts a build into shareable,
  decision-ready, agent-executable output.
---

# Dossier Generator ("build to deal")

## What it produces
1. **The dossier (Markdown).** The canonical source of truth AND the agent-consumable spec. Two halves that snap together on an I/O contract:
   - **Part A, human executive summary** (skim + decide): intent, ROI-first, estimated cost, opportunity, principal sources, assumptions, confidence boundaries, and a fillable Decisions Block.
   - **Part B, agent implementation spec** (execute): operational instructions, structured ICP and deal flow, a comparable-client research sub-pipeline, account research, offer sketch, codebase architecture, deliverables.
2. **The Part B run output (Markdown).** What you get when an agent executes Part B against the filled decisions: the ICP filters, a real researched comparable-client table, account briefs, the entry offer sheet, a lead-funnel sketch, a sanitized architecture one-pager, and next-actions. This is the send-to-partner artifact.
3. **The deck (HTML artifact).** The human-facing presentation generated from the dossier: **Part 0** the decision, **Part 1** the pitch, **Part 2** the architecture. Built to be talked through (screen-record / Loom), grounded in the real codebase for Part 2.

Keep all three. The Markdown is what an agent runs and the source everything else is generated from; the deck is what a human's eyes consume. They are not substitutes.

## Inputs
- An **executive interview** about the offering and the deal (below).
- One or more **codebases** to extract the architecture from (real, so Part 2 is true, not invented).

## The flow

### Step 1 — Executive interview
Prompt the user for these. If a field is unknown, mark it and continue; do not invent.
- **The capability.** What does the system actually do, in one paragraph?
- **The client / source.** Who is it built for? (You will **codename** them; get a neutral codename.)
- **The ROI, mandatory.** What cost or inefficiency does this remove? Frame as "we sell the removal of X," never as selling the technology. Labor hours, escalation, error/liability tail, audit cost, budget efficiency, sales-team efficiency. This drives Part A's top section.
- **The first vertical.** Which market segment do we point at first?
- **Deal flow and timelines.** The stages from cold to closed, and rough durations.
- **Entry motion.** Which rung do we lead with (paid discovery vs free qualifier), and what is the realistic first "yes"?
- **Target accounts.** Named, or delegate sourcing to the research sub-pipeline.
- **Confidence boundaries.** What is proven (grounded in code that runs) vs reasoned vs open research question?
- **Open questions to close** before committing.
- **The codebase(s)** to point Part 2 at.

### Step 2 — Fill the dossier
Populate `dossier-template.md` from the interview. Part A is ROI-first and honest about confidence. Part B is executable and unambiguous. Codename the client throughout, scrub any fingerprints (real stack, niche platforms, corpus, naming) while keeping the architecture **structurally executable**, and generalize it (an AWS-native or cloud-neutral analog, in the greenfield language of choice).

### Step 3 — Run Part B
Execute Part B against the filled Decisions Block. Prefer a background agent with web access for the comparable-client research, so the prospect list is real and cited, not guessed. Output the Part B run file.

### Step 4 — Emit the deck
Generate the Part 0/1/2 deck per `deck-spec.md`, using the artifact-design skill. Part 0 and Part 1 come from Part A; Part 2 comes from the real codebase. Deploy as an Artifact (default-private).

### Step 5 — Return
Hand back the three artifacts and a one-line Loom teach-through note. Point out what needs the user's decision or a human adversarial review.

## Rules the skill enforces
- **Confidentiality.** Codename the client; scrub identifying detail; keep structural executability. Never output the real client name even if it surfaces during research.
- **ROI-first.** The business sections MUST carry a cost-removed / efficiency argument. Price against value removed, not features or tokens.
- **Confidence boundaries.** Flag strong (code-grounded) vs weak (open research) explicitly. This is the part a sharp partner respects most; do not skip it.
- **The I/O contract.** Part A's Decisions Block is Part B's input. If a decision field is empty, Part B halts on that branch and flags it rather than guessing.
- **Grounded architecture.** Part 2 and the architecture sections are grounded in the actual codebase, not fabricated. Real algorithms, generalized for confidentiality.
- **Prose.** Plain, concrete prose. No em dashes, no three-item rhythmic lists, no puffery, no AI-vocabulary filler (crucial, showcase, pivotal, landscape, testament). Say what the thing is and what it costs.

## Files
- `dossier-template.md` — the parameterized dual-format template to fill.
- `deck-spec.md` — the Part 0/1/2 deck outline and build approach.

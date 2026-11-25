---
name: reviewing-docs
description: Use when the user has a finished or near-finished document (memo, business review, PRD, decision doc, briefing, comms, framework, talking points, post-mortem) and wants it pressure-tested before it ships, such as "review this doc", "poke holes in this", "is this ready to send". Works on any doc, not just mindpowers-drafted ones. Not for code review.
---

# Reviewing Docs

## Overview

A standalone red-team pass for a finished (or nearly finished) piece of writing. It works whether or not the doc was made with mindpowers: a pasted memo, a doc someone else wrote, a file on disk, all fine. It is the "review" step of the mindpowers loop (shape → draft → review → remember), but it doesn't require the other steps to have happened.

The job is not to improve the prose. It's to find the places where the doc will get punctured in the room it's headed for, before that room punctures it: the exec meeting, the regulator's inbox, the Slack thread. Track the steps below as todos if your harness has a task list.

**When this fires:** "review this doc," "poke holes in this," "is this ready to send," "what am I missing before I ship this," or being handed a file/pasted text and asked whether it holds up. It does not fire for source code, config, or anything a code-review tool should be looking at; decline that and point at a code-review skill or tool instead.

## User-Facing Language

Think precisely; respond plainly. Use common words and short sentences. Explain
an unavoidable technical term the first time it appears, and give one short
example when a rule could be misunderstood. For a material review conclusion,
give a compact explanation: the recommendation or conclusion, what you checked,
the main reasons, uncertainty, and the next step. Do not dump internal
machinery. If the user says the explanation is unclear, explain it again from
scratch.

## Step 1: Find the spec

Check the doc for a paper trail before reviewing it blind.

1. Look at the doc's own frontmatter for a `spec:` link.
2. If there's none, scan `docs/mindpowers/specs/` (and legacy `docs/brainstorm/` if it exists) for a spec with a matching filename stem or topic.

**If a spec exists:** do a fidelity check before anything else.

- Is every section the spec called for actually present in the doc?
- Did anything make it into the doc that the spec didn't scope in?
- Has the claim or recommendation drifted between spec and doc: softened, hedged, or quietly changed?

Fidelity problems are worth surfacing on their own, separate from the lens panel below, because they mean the doc stopped tracking its own plan somewhere along the way.

**If no spec exists:** offer to write down the document's intended audience,
main claim, and shape before reviewing.

> "There's no spec for this doc. Want me to first write down its audience, main
> claim, and shape so we can check that it says what you intended?"

This is worth doing even when it feels like a formality: it's often where the real problem surfaces, because writing down "here's the claim this doc is actually making" tends to expose that the claim isn't the one the author intended. A doc that reads fine sentence-by-sentence can still imply a claim nobody signed up for once you state it plainly. If the user declines, proceed straight to the template rubric and lens panel without it.

Either way, don't skip Step 1 to save time. A doc that fails its own spec is a different, more useful finding than a doc that merely reads weak; surface it first so the rest of the review has the right frame.

Also check `docs/mindpowers/reviews/` for a prior review of this doc (same
filename stem). If one exists, load its findings ledger before assigning any
IDs: existing findings keep their `R-###`, new findings continue the
sequence, and the re-review updates statuses per the Output section.

## Step 2: Load the template rubric

1. Identify the doc's type from its content and shape (business review, decision doc, PRD, briefing doc, comms draft, framework, talking points, post-mortem) or from its frontmatter `type:` field if present.
2. Load `skills/mindstorming/references/<type>.md`.
3. Treat that file's **Standards baked in** and **Anti-patterns** sections as the objective rubric, not your own taste. Check the doc against them directly (e.g., for a decision doc: is the recommendation up front? Is a real counter-argument engaged, or a strawman?).
4. If the doc doesn't match any of the nine templates, treat it as self-shape: there's no reference file to load, so the rubric is whatever structure the (reverse-engineered or real) spec implies, plus general clarity and completeness.

Treat frontmatter `readiness` as the canonical binary field:
`readiness: ready | not-ready`. Never put a type-specific label such as
`build-ready` in frontmatter. For a PRD, canonical `ready` means the body must
satisfy and show the user-facing `Readiness: build-ready` bar. Treat any missing
evidence boundary, untraceable requirement, unverifiable acceptance criterion,
incomplete triggered conditional module, or blocking open decision as a
blocker and report any mismatch with canonical `ready`. Canonical `not-ready`
must retain its named material blockers. For other document types, apply the
same rule using the selected template's type-specific ready label or readiness
bar where one exists.

Do not invent a rubric when a template exists. The template encodes standards someone already learned the hard way; skipping it means re-deriving from scratch and probably missing something the template would have caught.

For example: a decision doc gets checked against `decision-doc.md`'s standards directly: is the recommendation in the first section rather than the last, is there a real counter-argument rather than a strawman, is the ask explicit. A comms draft gets checked against `comms-draft.md`: is the key message identifiable on a skim, is the tone calibrated to the stated audience. Use the rubric file's own language when naming a finding; don't paraphrase a standard into something vaguer than the template already made it.

## Step 3: Lens panel

Review runs as a panel of one to three lenses, each reading the doc cold.
Load `skills/reviewing-docs/references/lenses.md` for the lens definitions,
the tier table, and the reader archetypes.

1. **Pick the tier** from the doc type using the tier table (comms-draft
   and talking-points get the audience lens only; briefing-doc,
   business-review, and one-pager add rigor; decision-doc, prd, framework,
   post-mortem, and self-shape add premise). The user can override for any
   run: "quick pass" drops to tier 1, "full panel" raises to tier 3.
2. **Tier 3 gate:** before the full panel runs, run the audience lens first
   and show the user its reader card and first-read narrative: "Does this
   match your reader? Where am I wrong?" If the card is wrong, correct it
   and re-run the audience lens with the corrected card, then dispatch the
   remaining lenses. In degraded mode (no subagents), build the card and
   narrative in-conversation and say so. Tiers 1-2 skip this gate and seed
   the reader card from the spec's `audience` frontmatter or the archetype
   table.
3. **Dispatch:** on clients that can spawn subagents, run each lens as a
   fresh subagent given ONLY what "What every lens receives" in lenses.md
   allows — the spec (or its Step 1 stand-in), the doc, the lens prompt,
   and the template rubric. Never the drafting conversation, never another
   lens's findings. Lenses run blind to each other. On clients without
   subagents, follow "Degraded mode" in lenses.md and say plainly in the
   output that isolation was simulated.
4. Say which tier, lenses, and isolation mode produced the findings before
   presenting them (e.g., "full panel: audience + rigor + premise, run as
   isolated subagents").

**Talking-points live drill (optional):** for talking-points docs specifically, offer a live drill after the written review.

> "Want to drill this out loud? I'll ask the predicted questions one at a time as the interviewer, you answer, and I'll score each answer against the prepared point and help sharpen it."

If accepted, ask one predicted question at a time, wait for the user's spoken answer, then score it (does it land the prepared point, does it survive a follow-up) and suggest a tighter version before moving to the next question.

## Step 4: Synthesis and triage

Merge the lens outputs into one findings list:

1. **Dedupe.** Where lenses hit the same underlying problem, merge into one
   finding that keeps each lens's angle visible.
2. **Triage** every finding into exactly one class:
   - **Mechanical** — objective defect (broken cross-reference,
     contradictory figures, a spec section missing from the doc). Present
     with the fix.
   - **Taste** — judgment call (tone, ordering, depth). Present with a
     recommendation; the user decides.
   - **User-Challenge** — the finding disputes the user's stated direction
     or a locked-spec decision. Never auto-resolved: present it with what
     the reviewers might be missing and the cost if they are wrong.
3. **Disagreements** between lenses surface explicitly as disagreements,
   never silently averaged. The user's call is final.

## Output

Produce findings, not a rewrite.

- Rank findings by severity: **blocker** (this will get called out and the doc won't survive it as-is) → **weakens** (undercuts the doc but survivable) → **polish** (worth fixing, not urgent).
- Every finding anchors to a **quoted line** from the doc; don't describe a problem in the abstract, point at the sentence.
- Every finding carries a **suggested fix**: a direction, not necessarily rewritten prose.
- Every finding gets a stable ID at first sighting: `R-001, R-002, …`,
  scoped to the reviewed doc and never renumbered. A re-review of the same
  doc reuses existing IDs and continues the sequence for new findings.
- Every surfaced finding classifies its root cause, recommended route, and readiness impact using this exact metadata:

  ```yaml
  id: R-001
  severity: blocker | weakens | polish
  lens: audience | rigor | premise
  triage: mechanical | taste | user-challenge
  root_cause: evidence | decision | writing | verification | preference | approval
  recommended_route: validating-problems | mindstorming | drafting | reviewing-docs | calibrating | none
  readiness_impact: blocking | non-blocking | none
  ```

- Present the **top 8 findings** in chat, ranked. The saved review file
  records ALL findings in the ledger — overflow beyond the top 8 is
  recorded there, never discarded; say in chat how many more the file holds.
- One line of praise is fine if genuinely earned. No more than one line, and don't lead with it.

Format each finding roughly like this:

> **[R-001 · blocker] "the recommendation is to consolidate vendors over the next two quarters"**: no number attached to the savings this is supposed to justify. An exec skeptic asks "how much, exactly" in the first thirty seconds. Fix: attach the estimated savings range and the confidence behind it, even a rough one.

If there are zero findings above "polish," say that plainly instead of manufacturing minor nitpicks to fill out a list; a clean doc is a valid outcome.

**Saving the review:** per the file contract, save to `docs/mindpowers/reviews/YYYY-MM-DD-<type>-<slug>.md`, using the same stem as the doc/spec it reviewed so the pair sorts together. Exception: if the doc is a short comms piece (Slack message, brief email), present the findings in chat only; don't write a file for something that was never going to be filed itself.

**The findings ledger:** every review file contains a ledger table of ALL
findings for the doc, one row each:

| ID | Severity | Lens | Summary | Status |
|---|---|---|---|---|
| R-001 | blocker | rigor | Savings claim has no number attached | open |

Status is `open | fixed | regressed | parked`. A re-review of the same doc
updates statuses in this ledger instead of re-listing findings: a fixed
finding that breaks again is marked `regressed` under its original ID, and
new findings continue the ID sequence. The ledger is the durable record;
the chat summary is the view.

**If the spec itself was wrong:** when the fidelity check or lens panel reveals that the problem traces back to the spec (wrong audience, wrong claim, wrong structure from the start, not just an execution slip), say so plainly and recommend flipping that spec's `status` to `superseded`, then rerunning mindstorming on the delta rather than patching the draft in place.

## Visual companion (optional)

After findings are assembled, when there are 3+ line-anchored findings, offer
the annotated view in its own message, naming the mode per the fallback ladder
in `skills/_shared/companion/COMPANION.md`:

> "Want the findings as an annotated view alongside our chat? Each finding
> appears under the exact line it's anchored to, severity-labelled."

If accepted, follow COMPANION.md and push the `annotated-findings` screen: one
`.section` per finding — quoted line, then the finding with its severity
(`.label`: BLOCKER / WEAKENS / POLISH) and ID. The view is read-only;
discussion and routing decisions stay in chat. The saved review file remains
the artifact of record.

## Root-cause routing

Classify the cause of each surfaced finding before recommending the next action:

| Root cause | Signal | Recommended route |
|---|---|---|
| `evidence` | Problem evidence is missing or weak. | `validating-problems` |
| `decision` | A scope, product, requirement, or measurement decision is missing. | `mindstorming` |
| `writing` | Settled reasoning is expressed poorly. | `drafting` |
| `verification` | A corrected artifact needs another verification pass. | `reviewing-docs` |
| `preference` | Final human edits reveal a stable preference. | `calibrating` |
| `approval` | Required external approval is pending. | `none`; record the pending approval and do not switch skills. |

For a PRD, reserve `evidence` and `validating-problems` for missing or weak
customer or business problem evidence. Missing support for an already chosen
target, threshold, scoring cutoff, pilot, or other PRD-hardening choice is a
product or measurement `decision` finding routed to `mindstorming`. Preserve
the chosen value; the unresolved work is its basis or readiness support, not
the value itself.

When the artifact or its linked spec explicitly says the underlying reasoning,
scope, or decision is settled and identifies only dense, vague, or repetitive
expression, preserve that boundary: classify the finding as `writing` and
route it to `drafting`. Do not reopen it as a missing decision unless the
source actually leaves substantive content unresolved or contradictory.

External approval is permission from outside this workflow, not evidence of content readiness. Give an approval finding `readiness_impact: none` unless it exposes a separate unresolved evidence or decision issue; classify that issue as its own finding.

After the findings, recommend the next action in common words and explain why.
Name the internal skill route after the action when useful. Wait for the user to
confirm before switching skills. When several skill routes are recommended,
require confirmation before each actual switch; one confirmation is not blanket
authorization for the chain. For a confirmed handoff, carry forward the source
artifact, exact finding, unresolved question, affected section or identifier,
severity, and readiness impact so the next skill resumes from the finding
instead of restarting.

When findings are mixed, resolve evidence and decision reasoning before prose work. Rerun `reviewing-docs` after the routed corrections are made.

When the doc carries checkable claims (numbers, dates, names, quotes) and the review is otherwise clean or near-clean, recommend a `fact-checking` pass before the doc ships: it verifies claims against the user's sources with a quote-the-source rule and flags sensitive content. Recommend and wait for confirmation; never run it unasked.

## Cowork / no-filesystem fallback

Paths above are relative to the working folder; in Cowork that's the user's shared folder. If no writable folder exists, present the full review in chat (or as an artifact) and say plainly it was not saved to disk.

## Rules

- Never rewrite the doc wholesale. That's drafting's job; offer to hand it to drafting instead of doing it here.
- Top 8 findings in chat, ranked by severity; the review file's ledger records all of them.
- Praise is allowed, capped at one line.
- Always name the tier, lenses, and isolation mode before giving findings, so the user knows what produced them.
- Never switch skills before the user confirms the recommended route.
- If asked to review code, decline and point at a code-review tool instead; this skill is for prose deliverables.

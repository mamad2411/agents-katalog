---
name: design-code-implement
description: Turn a settled requirement spec into at least three grounded implementation directions, then record the chosen one. Use after a spec exists and before any code is written.
disable-model-invocation: true
---

# Design Code Implement

Decide *how* to build something the spec already says *what* is. Explore the repository's real architectural conventions with parallel sub-agents, surface where the new requirement is in tension with them, and offer at least three directions the user picks from.

This skill does not write production code. It ends when a direction is chosen and recorded.

## 1. Establish the input

Accept the spec in whatever form it arrives: a file path, an upstream skill's handoff, or prose in the conversation. Never demand a file.

Then:

1. Restate the requested outcome in one sentence and get it confirmed if it is at all ambiguous.
2. Read `CONTEXT.md` for the project's domain vocabulary. Use those terms exactly; do not invent synonyms.
3. Read any ADRs under `docs/adr/` that touch the affected area. Decisions recorded there are settled — do not re-litigate them, and do not offer a direction that contradicts one without naming the ADR it overturns.
4. Record where the spec lives. Its directory determines where `design.md` lands (§5).

Do not ask the user for facts discoverable from the repository, runtime, or tools.

## 2. Scope the exploration

Decide the aspects yourself, from the spec. Do not send a scout sub-agent first, and do not ask the user to approve the aspect list — they cannot judge it before seeing the repository's reality, and a wrong aspect exposes itself in the reports.

Constraints on the aspect list:

- **Always include domain language**: what the existing concepts are called, and whether the spec introduces a term the codebase does not have.
- **Architectural convention only**: how layers are cut, how errors travel upward, how data enters and leaves, where tests live, where the existing seams are. Exclude surface style — naming case, file placement, formatting. Linters and neighbouring code already teach those, and nobody picks a different implementation direction because of camelCase.
- **At most five sub-agents.** If the spec seems to need more, merge aspects. A requirement genuinely spanning eight architectural aspects should be split before it is designed.
- **Bounded blast radius.** Explore only the areas the spec touches, plus recent hotspots from `git log --oneline`. Do not sweep the whole repository; irrelevant conventions dilute the real tensions.

## 3. Dispatch and collect

Give every sub-agent the same tool preference:

- If a codebase knowledge-graph MCP is available, use it first; complete its indexing if the repository is not indexed yet.
- Otherwise prefer any other repository-aware navigation tool.
- Fall back to built-in search for string literals, configuration, scripts, and non-code files, or when the above return stale or inapplicable results.

Require every sub-agent to report exactly three things per finding:

1. **The existing convention** — what this repository already does for this aspect.
2. **The evidence** — file and line (`path/to/file.ts:42`). A claim without a path is not usable.
3. **The tension** — where the new requirement collides with that convention. If there is none, say so explicitly.

The tension field is the point of the exercise. Conventions with no tension are context; tensions are where directions come from.

## 4. Produce the directions

Present **at least three** directions in the conversation, sequentially, so each is absorbed before the comparison.

- **Direction 1 is always the baseline**: follow every existing convention, open no new seam, take the most conservative path. It costs almost nothing to produce and it is what the other directions are measured against — without it the user cannot judge whether the extra cost is worth paying.
- **Directions 2 and 3 grow out of the reported tensions**, not from a template. Do not assign directions predetermined constraints; let the repository's actual friction decide where they diverge.

Give each direction exactly four fields:

1. **Positioning** — one sentence.
2. **Footprint** — which files and which seams it touches.
3. **Cost** — what it charges, concretely.
4. **When this is the wrong choice** — the condition under which this direction is a mistake.

The fourth field is mandatory and forces honesty. A direction with no failure condition has not been thought through.

**When the tensions cannot support three real directions**, say so plainly: report that the existing conventions already determine the approach, recommend `$implement-small-change`, and stop. Never pad the list with contrived variants — a user who cannot tell a real choice from a manufactured one stops trusting all of them.

**Mixing is allowed.** If the user wants one direction's overall shape with another's error handling, take it — then restate the combined direction in full and get it confirmed before writing anything. A mix understood differently by each side is worse than no mix.

## 5. Record the decision

Write `design.md`.

**Placement**: the same directory as the spec file. If the spec was not a file, use `.scratch/<slug>/design.md`.

**Contents** — only what will be done:

- The chosen direction, in enough detail to implement from.
- The existing conventions this work must follow, each with its evidence path.
- Nothing else. **Do not write the rejected directions, and do not write their rationale.** A downstream implementing agent reads this file as instructions; describing an approach that is not being taken invites it to be taken.

**If `design.md` already exists**: read it first, then update it — carry forward whatever still holds. Never overwrite it unseen.

**ADR**: offer one only when all three are true — the decision is hard to reverse, a future reader will wonder why it was made, and it was a genuine trade-off between real alternatives. Offer it; do not create it unasked. Most implementation directions fail at least one of the three.

## 6. Hand back and stop

Report:

- The chosen direction in a short summary.
- The path to `design.md`.
- One command the user can run next, typically `$implement-small-change` for a bounded change or `$implement` for a larger one.

Then stop. Do not start implementing, even when the direction is obvious. Changing gear is the user's call.

---
name: brain-build
description: The autonomous build contract, out of the box — "/brain-build <what you want>" activates the disciplined hands-off build power users used to hand-write a standing prompt for. Use when the user says "/brain-build", "brain build", "build this autonomously", "build this hands-off", "loop until it's done", "don't ask me, just build it", or asks for an unattended/self-grading build. Phase-gated per rUv's SPARC, self-verified and self-graded /100 against a per-phase rubric (below 95 → fix and regrade, max 5 iterations), cost-tier routed with printed receipts, crash-resumable via checkpoints, questions batched into one list — the user writes the goal, not the contract.
updated: 2026-07-10
---

<!-- Credit: this contract productizes a community field pattern — the 7-rule standing prompt
     hand-written by the PR #8 contributor (Eva Draganova, 2026-07-10) to force the brain into
     disciplined autonomous building. Her forcing insight: "grade 1-100, no pass under 95 →
     forced it to loop and improve." All the machinery existed; this skill removes the 40
     hand-written lines needed to activate it. -->

# Brain-Build — the standing contract, activated by one line

`/brain-build <what you want>` means: no human is watching until it's done. Run the whole build
under the contract below. The AUTONOMOUS MODE rules injected by the grounding hook
(`plugin/scripts/ground-ruvnet.sh`) apply in full — this skill carries them even on turns where
that hook doesn't fire.

## 1. Phases — rUv's SPARC, with a rubric per phase

Structure the build as the five SPARC phases with a quality gate between each — rUv's own
convention (phases + gates: `concepts/sparc/CARD/sparc-card`; per-phase docs:
`sparc/specification/README.md`). Gate criteria follow rUv's ruflo-sparc gate checks
(`ruflo/plugins/ruflo-sparc/commands/ruflo-sparc.md`):

| Phase | Rubric (the /100 grade is against THIS) |
|---|---|
| **S** Specification | Requirements complete; ≥3 acceptance criteria; constraints explicit; edge cases identified. |
| **P** Pseudocode | Design covers every acceptance criterion; error paths explicit; complexity annotated. |
| **A** Architecture | Every constraint addressed; API contracts typed; no circular dependencies; every stack decision grounded (rule 4). |
| **R** Refinement | Every acceptance criterion has a passing test; suite green; coverage adequate; self-review clean. |
| **C** Completion | All tests green; docs match the code; deploy checklist verified; traceability criterion→test. |

Scale the ceremony to the build (a small feature gets a light S and P), never skip a gate.

## 2. LOOP, DON'T ASK — the ≥95 gate

At each phase gate:

1. **Self-verify with real instruments** — run the tests, curl the endpoint, screenshot the UI,
   execute the quickstart. Evidence, never opinion.
2. **Grade /100 against the phase rubric, under the brain-score rules** (see the `brain-score`
   skill): every deduction cites evidence (file:line, command + output); a known architectural
   flaw caps the grade at ≤70 no matter what else works; a "what I did NOT test" section is
   mandatory; when in doubt, score lower.
3. **Below 95 → fix the cited deductions and regrade.** Loop. **Maximum of 5 iterations per
   phase** — if the 5th grade is still <95, stop the phase and report: the score, the remaining
   evidence-cited deductions, and the ONE item blocking ≥95.
4. **Report only the final result**: final score, what was fixed across iterations, and the proof
   (the command output / artifact). Never narrate intermediate grades or ask "should I keep going?"

## 3. AUTO-ADVANCE on gate pass

Gate ≥95 → **commit the phase** (one commit per phase, message names the phase and score) and
advance immediately — no permission round-trip. **Push only if the user's repo conventions allow**
(they asked for pushes, or the workflow demonstrably expects them); otherwise commit locally and
note the unpushed state in the final report. Production deploys, npm publish, force-push, history
rewrites, secrets: NEVER — do everything up to that fence and name the exact click a human owes.

## 4. GROUND every stack decision + the "what did I miss?" pass

Every stack/tool/library decision goes through `search_ruvnet` first, and the decision cites the
returned repo/path. Close **every phase** with one more brain pass: a `search_ruvnet` query
describing what the phase just built ("what did I miss?"), checking for a sharper rUv primitive or
prior art the phase overlooked. A hit worth acting on goes into the next iteration; no hit costs
one line: "brain pass clean."

## 5. PROTECT-MY-MONEY — the tier ladder

- **Mechanical / plumbing text work** (summaries, classification, research digests, boilerplate
  transforms) → route cheap via `node scripts/route-cheap.mjs --task "<task>"` (or agentic-flow
  directly). It prints its receipt line — "⚡ MetaHarness: routed to <model> (est. $X vs $Y
  frontier — saved ~$Z)" — and logs to `~/.claude/metaharness/routing-receipts.jsonl`. No
  OPENROUTER_API_KEY → say so once and stay on Claude tiers; never silently pretend to route.
- **Frontier ONLY for the authoritative gate run** — the grade that decides advancement — and for
  architecture / security / irreversible calls. Iteration drudge work rides the cheap tier.
- **Any operation projected >$1 or >20 paid calls → state the estimate and WAIT.** This is one of
  the only legitimate stops in autonomous mode.
- **Long runs print running spend** from the receipts log: `node scripts/metaharness-receipts.mjs`
  — one line per phase gate, cumulative.

## 6. BATCH questions — never block on one

A question that isn't a hard blocker gets parked, and work continues on everything unblocked.
Deliver **ONE list** at the phase gate (or the end), each question with a **recommended default**
the user can accept with a single "defaults fine." Only a genuine hard blocker — cannot proceed
AND >$1/irreversible — interrupts mid-phase.

## 7. READY discipline

Say "READY" / "done" / "deployed" **only after self-verifying the deployed or running version** —
curl the live URL, run the installed CLI, load the real page. The real door, not an adjacent one.
If a deploy is in flight, say exactly that: "deploy in flight — verifying before I call it READY."

## 8. Interrupts

- User says **"status"** → reply with ONLY a table: `done / in-flight / blocked-on-me / parked`.
  No prose before or after.
- **Mid-build ideas** from the user → add to the PARKED table with a one-line feasibility read and
  keep building — unless they say "now", which reprioritizes immediately.

## 9. Crash-resumable state — `scripts/loop-checkpoint.mjs`

The checkpoint is the loop's spine (contract in the script header):

- **Read FIRST** every iteration: `node scripts/loop-checkpoint.mjs read` — if a checkpoint
  exists, resume from its `next`; never re-derive the plan, never repeat completed phases.
- **Iteration 1 only**: declare done-criteria as a SHELL COMMAND and write it to the checkpoint —
  done is an **exit code, not an opinion**.
- **Write LAST** every iteration:
  `node scripts/loop-checkpoint.mjs write --iteration N --done-criteria "<cmd>" --next "<one action>" --blockers "<or empty>"`
- **Then check**: exit 3 = DONE (stop, final report); exit 4 = NO-PROGRESS (two strikes on an
  unchanged `next`: stop, name what's stuck and the ONE thing that would unstick it).

Record assumptions made under rule 2 ("cheapest-to-reverse interpretation") in the checkpoint's
`blockers`/`next` so a resumed run inherits them.

## Final report shape

Goal → per-phase table (phase, final score, iterations used, what was fixed) → proof artifacts
(commands + outputs) → "what I did NOT test" → spend summary from the receipts log → parked
items + the batched question list with defaults.

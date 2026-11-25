---
name: rjv-gated-build
description: "Use for long, high-stakes multi-step builds (financial/money/prod) where an INDEPENDENT reviewer grills and approves each step before it ships. Gated loop, role casting across models, compressed anchor doc, crash/compaction durability, model economy (cost-routing hard rule). Triggers: 'gated build', 'grill each step', 'adversarial review loop', 'overnight run', 'high-stakes build'."
---

# Gated build — adversarial multi-agent construction

For work where being *plausibly wrong* is expensive. One agent can't reliably
catch its own errors — the blind spot that produced the bug reviews the bug.
Quality comes from **independence**: a second agent whose job is NO-AGREE,
grilling every step to an explicit APPROVED.

Economics: compress everything agents read (specs, notes, grill prompts) so you
can afford a second agent to disagree. Efficiency funds redundancy.

## 1. Casting the roles

Three roles: **Orchestrator** (holds anchor doc, casts, integrates), **Author**
(drafts), **Reviewer** (grills to APPROVED). Cast by task, not habit:

| Author | Reviewer | When |
|---|---|---|
| Frontier agent (full repo context) | Cross-vendor frontier agent | Design-heavy, high-stakes builds — the core pattern |
| External CLI agent (e.g. Codex) | Orchestrator itself | Mechanical bulk typing; orchestrator has the context + judgment |
| Local model (Ollama-class) | Orchestrator | Zero-cost function-level drafting from a tight spec |
| Cheap-tier subagent | Flagship-tier | Intra-family economy: cheap hands, expensive judge |

**Execution bindings** — each cast needs a transport; use what exists:

- Local Author → `rjv-ollama-delegate` (runner, prompt rules, verify mandate). A
  local model runs via that runner, NOT an `Agent`/subagent `model:` (that field
  takes only cloud aliases opus/sonnet/haiku/fable). On live-money code keep even
  the draft on a cloud mid-tier — §7.
- External CLI Author/Reviewer (Codex-class) → its plugin or a thin Bash
  forwarder subagent (e.g. Codex rescue in Claude Code) — one call in, stdout
  back, cheapest model on the forwarder.
- Intra-family cheap Author → subagent spawn, model set explicitly (§7).

**Record the cast in the plan.** Cast once at build start, into the anchor plan's
`## Cast` section (`rjv-feature-workflow`): orchestrator, author, reviewer,
subagent tiers, human gates — models named. Every resume reads it and plays its
role; the loop never re-negotiates who approves. Recasting = a logged Decision
with a why.

**Two hard casting rules** (evidence-backed, don't bend):

1. **Reviewer ≥ author strength.** Reviewer strength is where quality comes from;
   author strength is just typing speed. A weak model reviews nothing — tested:
   asked to find a real bug in shipped code, a 35B local model said "no bugs".
2. **Prefer cross-vendor for the grill.** Different families miss different
   failure modes; same-family review inherits the author's blind spots.

**The human is also a reviewer.** In a real run the user caught a hole (broker
latency) that BOTH frontier models missed across four grill rounds. Surface
designs to the human at phase boundaries; their domain experience outranks model
priors — when their live evidence contradicts the design, the design updates
immediately and says so.

## 2. Grill the SPEC before any code

Highest-leverage grill is pre-implementation. Source build: the reviewer's
round-1 verdict on the *design* was "not buildable as written" — 10 ranked attack
scenarios, 8 valid. Fixing pre-code cost a doc rewrite; post-code it would have
cost the build.

- Prompt: "ATTACK this design. Ranked failure scenarios. Verdict: AGREE /
  NO-AGREE with blockers."
- Iterate spec → attack → amend until AGREE. Record each round in the anchor doc
  (v1 → v2 → v2.1…), noting objections accepted *on merit* vs rejected with reasons.
- A reviewer that never says NO-AGREE isn't reviewing. Instant approvals every
  round → sharpen the prompt (§4) or recast.

## 3. The gated loop (per implementation step)

```
spec checkpoint → implement → self-review + smoke → REVIEWER GRILL → fix → re-grill … → APPROVED → commit → next
```

Stop rules are part of the spec — write them explicitly per step. Fill-in template:

```
loop step: reach [verifiable end state], only touching [scope],
stop after [success cond] OR [N iters] OR [$/token budget], verifier = [test/build/screenshot].
```

- **Spec first.** Step acceptance criteria into the anchor doc BEFORE coding.
  Grading against a spec invented mid-code blesses bugs.
- **Self-review + throwaway smoke** before handoff — catch the dumb bugs cheaply
  so the reviewer's rounds go to subtle ones.
- **Grill to an explicit APPROVED.** One round-trip is not review.
- **Park, never rubber-stamp.** Cap rounds per step (~6). Still blocked → write
  open blockers to the anchor doc, STOP that step. "Parked, here's why" beats a
  faked approval — non-negotiable when money/safety is at stake.
- **Living plan / reach-backs.** A grill that invalidates an EARLIER approved step
  → reopen, fix, re-test, re-grill, LOG the reach-back. A locked-in wrong step is
  worse than a reopened one.

## 4. Driving the reviewer — prompt rules

- **REVIEW ONLY.** First line: "REVIEW ONLY — do not modify files, do not
  implement." Reviewer reads, reasons, votes.
- **You run the tests, not the reviewer.** Reviewer sandboxes hang on execution.
  Run the suite yourself, paste results ("suite already run: N passed — review by
  reading the code"). Reading files fine; executing not.
- **Name the failure modes.** Exact files, spec section, numbered hunt-list. Money
  code: double-exposure, oversell, lost/duplicated intent across restart, ordering
  races, idempotency, fees/precision, the risky path just written. Vague prompts →
  vague reviews.
- **Bound every grill; cancel-first on timeout.** Background with a wall-clock cap
  (~12–15 min). Timeout → cancel FIRST, verify nothing running, relaunch fresh,
  kill orphans. Cap relaunches (~3); persistent no-verdict = tooling failure →
  park, don't fake.

## 5. The anchor document (the build's real memory)

One compressed working-memory doc **per build** — a repo has many. No single
global RESUME.md: use `rjv-feature-workflow`'s layout (`.plans/<name>.md` per
piece of work, linked from the feature roadmap) so several gated builds run in
parallel, each hydrated by name. The sections below live INSIDE that plan.
Conversation is disposable; the anchor doc is not. "The spec is the only artifact
that earns its tokens" (cavekit).

**Owned sections** — each phase writes only its own:

| Section | Owner | Holds |
|---|---|---|
| GOAL | human + orchestrator | one paragraph, the point, never forget |
| CONSTRAINTS / VOCAB | human | agreed words, dead words, hard limits |
| EVIDENCE LEDGER | orchestrator | live results as design constraints — refuted ideas marked "do not resurrect" |
| INVARIANTS | grill rounds | iron rules that emerged, each traceable to a round or corpse |
| DESIGN vN | spec-grill loop | current design + the grill trail (v1 → v2 → …, who objected, what was accepted on merit) |
| TASKS / PLAN | orchestrator | phases with acceptance criteria; every idea gets a HOME or gets killed |
| BUGS / CORPSES | implementation | failures studied at the lowest level, taxonomized |
| TOMBSTONES | orchestrator | resolved questions kept visible "so nobody re-opens them" |
| OPEN | anyone | genuinely undecided items, flagged USER where the human must decide |

**Register rule — compress by audience:**

- **Agents read** (this doc, RESUME, grill prompts, memory) → caveman register:
  facts, file:line, imperatives. "register order BEFORE send (sync fill drop →
  oversell)", not prose. For a reader with no context and 10 seconds. ~75% cheaper
  per re-read, and re-reads are the recurring cost.
- **Humans read** (replies, user docs) → prose, concrete examples with numbers.
  Comprehension failures cost more than output tokens.
- Explicit split: agent notes graduate to user-facing docs only when concrete +
  agreed.

**The no-later rule.** Never file anything "later". Every idea gets a home in a
named phase (with why) or gets killed. Source build: "later" hid the single most
valuable experiment — it became the FIRST build item once surfaced. Only
acceptable deferral = a stated structural dependency.

**Compression maintenance — bounded, not "periodic".** Anchor + memory files are
re-read every resume — recurring INPUT cost, the expensive kind, and it grows
*super-linearly*: each resume re-reads the trail it just appended to. "Periodic /
on bloat" never fires because nothing defines bloat — so a live build's anchor
silently reached 2,000+ lines / 130KB (~33K tokens re-read EVERY reconcile) and
became the run's token sink. Enforce a ceiling, don't trust judgment:

- **Hard ceiling: ~400 lines / ~20KB.** Over it, compression is not optional —
  collapse BEFORE acting (it is a step in reconcile-on-open, §6). A working doc
  re-read every turn is a few hundred lines, not thousands. 2,000+ lines means
  facts that belonged in `_docs/` never graduated — see the promotion mandate.
- **Promotion mandate — what collapses, and to where:** superseded DESIGN vN →
  one-line TOMBSTONE; closed grill rounds → `round + verdict + what-changed` (drop
  the prose transcript); durable facts (now-permanent INVARIANTS, third-party API
  behavior, established patterns) → **promote to `_docs/`**, the plan keeps only a
  link. The grill trail is the usual balloon — collapse it hardest. Truth moves to
  `_docs/`; the plan stays a thin working memory.
- **Register:** rewrite in caveman register — strip prose, keep facts. Never touch
  numbers, identifiers, file:line, code, commands, error text (byte-exact); never
  compress the EVIDENCE LEDGER's meaning — a lost nuance re-opens a refuted idea.

## 6. Staying alive — the run must survive drops

Two failure modes WILL hit a long run: the reviewer hangs, and your own connection
drops mid-response. Same defense: **never hold state only in the live conversation.**

- **Resume pointer + reconcile-on-open.** Rewrite the anchor doc's
  `>>> RESUME HERE <<<` block at the END of every step: current step + status,
  exact next action, must-read files, hard rules. Every resume
  (post-compaction/drop/wake) → FIRST run the `rjv-feature-workflow` reconcile:
  read plan → **VERIFY each "done" against real code/db** → note drift → rewrite
  Next Steps → stamp Last reconciled → **if over the §5 ceiling, compress before
  acting** → act. Never trust a stale checkbox; a drop may have lost the edit it
  claims.
- **Commit early and often.** Each approved step commits immediately. A drop then
  loses at most the in-flight edit, not a night's work.
- **Schedule your own wakeups.** Handing off to a bounded grill → schedule a
  self-wake (~15 min) to ACTIVELY return; passive "job re-invokes me" watches can
  die silently.
- **Idempotent steps.** You may re-enter mid-step after a drop — make side effects
  replay-safe (dedup keys, upserts, already-done checks).

## 7. Model economy — cost-routing is a HARD RULE, every agent

Binds **every** orchestrator that runs this skill — Claude, Codex, any host — not
just the flagship you're reading on. Long runs stall on budget/rate limits before
difficulty, so:

> **HARD RULE.** The flagship (top tier) is reserved for judgment: design, grill
> triage, final verify, synthesis. Any work a cheaper tier does equally well —
> recon, mechanical edits, test-writing, boilerplate, summarization — MUST route
> to the cheapest capable tier. Cheap-tier work on the flagship is waste, not
> thoroughness. (One bound: break-even below — don't route out a trivial task
> whose spec+review overhead exceeds the saving.)

Rung NAMES differ per host (Claude haiku/sonnet/opus; local gemma/qwen; Codex
spark/low-effort vs full) — the RULE is identical: cheapest tier that clears the bar.

### Two ladders — pick by whether the job touches the repo

Biggest routing mistake: sending repo work to a model that can't reach the repo.
Split the work FIRST, then pick the rung:

| Job needs… | Ladder (cheap → dear) | Note |
|---|---|---|
| **Repo tools** — recon, file reads, in-place edits | Explore/subagent @ cheap tier → @ mid tier | CLOUD/host-agent ONLY. A local model has **no tools** and cannot play here at all. |
| **Self-contained text** — draft-from-spec, classify, summarize (context is IN the prompt) | local (gemma → qwen) → cheap cloud → mid cloud | Local rungs cost $0; the axis between them is speed/quality, not price. Escalate a rung only when quality falls short. |

Hard fact behind the left column: a local model (`rjv-ollama-delegate`) is a
one-shot text function — NO filesystem/shell/web, sees only the prompt. It can
NEVER do recon or read your repo; the cheapest agent that reads files is a
cheap-tier Explore/subagent.

Ground-level:
- "Where is the retry logic?" → cheap Explore subagent. NEVER a local model.
- "Write this pure function to this signature + these 3 cases" → local (context is in the prompt).
- A recon subagent must **distill** (return the `file:line`), never dump file contents — a dump re-bills the flagship for the read it was meant to avoid.
- Don't spawn to read ONE small known-path file — read it yourself; spawn overhead > saving.
- Don't delegate the read of code you're about to edit — those bytes must sit in the flagship's context anyway.

Other frugality rules:
- **Reserve the flagship** for design, synthesis, final judgment, the grill.
- **Set the model EXPLICITLY per subagent** — never default-inherit the expensive
  parent (the silent inherit is the most common leak).
- **The forwarder goes cheapest.** A reviewer forwarder is one bash call returning
  stdout — the grill's quality is the REVIEWER's model, not the forwarder's.
- **Delegation has a break-even size.** Spec+review overhead is fixed; below it (a
  4-line fix) do it yourself. Delegate the BIG mechanical steps, not tiny ones.
- **Stakes raise the drafting floor, not just the review floor.** Casting already
  puts a strong REVIEWER on high-stakes work; also raise who may AUTHOR.
  Live-money / high-blast-radius → draft on a cloud mid-tier (Sonnet), not local —
  a subtly-wrong local draft costs more in review than it saved. Local drafting is
  for ordinary feature work.

## 8. Scope honesty — especially for financial systems

State plainly what "done" means. "Reviewer-APPROVED through step N" ≠ "validated
against reality" if the run only exercised a simulator/paper path. Keep dangerous
gates — live trading, prod deploys, destructive ops — **physically off** until a
separate explicit validation phase with its own gate (paper-parity, fill-ratio
bands, fail-closed thresholds). Never let "approved" read as "safe to ship."

## Appendix — reviewer = OpenAI Codex CLI

- **Cancel-first, never reattach.** Grill timeout → do NOT "reattach to preserve
  its work" (the reattach can die silently, orphan runs for hours). Cancel →
  verify none running → relaunch `--fresh`.
- **pkill orphans.** Cancelled/hung jobs leave `codex app-server`, `codex resume`,
  `app-server-broker`; `pkill -9 -f` them so they don't pile up.
- **Its sandbox can't run your tests** (no writable temp dir; hangs "verifying") —
  WHY §4's you-run-the-tests rule exists. Reading files (grep/sed/cat) in its
  sandbox is fine.
- **Writes files but can't run git** — commit from the orchestrator after it finishes.
- Session/thread ids are resumable (`--resume-last` / by id) for follow-up grills
  needing prior context — subject to cancel-first.

---

**One-line invariant:** independent reviewer + compressed on-disk state + scheduled
self-wakes = a run that converges to correct and survives every hang, drop, and
compaction.

*Provenance: distilled from a live high-stakes build (options trading bot, 2026-07:
6+ grill rounds, real NO-AGREEs, a human-caught design hole, losses studied at tick
level) + a verified local-model delegation spike. Register + spec-section ideas
credited to the caveman/cavekit family (github.com/juliusbrussee).*

---
name: mimir
description: Use whenever mcp__mimir tools are available. Two halves, equally important. READ — before you spend more than ~2 exploratory steps on a sub-task, hit an error, or choose among approaches, consult the belief graph; treat a returned belief as a prior that prunes your hypothesis space, and either act on it or say why you're overriding it. WRITE — after any non-trivial turn, if you learned, derived, or got corrected on something that would have changed what you did and will recur, insert it. A belief you neither use nor write back is wasted.
---

> **Historical agent-integration proposal.** Its enforcement/automatic-retrieval
> workflow is superseded. Use the [current installation guide](../claude-code-setup/INSTALL.md)
> and its skill/templates; do not install the historical commands below.

# Mimir

You have a persistent belief graph. It is your memory across the two things
your in-session reasoning cannot survive: **context compaction and the end of
the session.** Inside one session you already reason hypothetically and hold
your own working state — mimir is not a second brain for that. Its entire value
is that a belief written by a past session, or before the last compaction, is a
prior you would otherwise have to re-derive from scratch.

So there are two failure modes, not one:

1. **Hoarding** — you query, never insert, and the graph never grows.
2. **Decoration** — a belief is surfaced, you acknowledge it, and then you
   proceed exactly as if it weren't there.

The current cadence problem is mostly #2. Read this whole file; the WRITE half
is genuinely good but it is only half.

---

## READ — using the graph to skip work

### When to consult

The `UserPromptSubmit` and `PreToolUse` hooks already inject `[mimir prior]`
lines for you at the start of a prompt and before file/command tools — you do
not have to remember to call `query_relevant` in those cases. You *do* call it
yourself when you cross into territory the hooks didn't cover:

- You're about to spend **more than ~2 exploratory steps** on a sub-task (reading
  several files to understand a subsystem, trying a fix you're unsure of).
- **An error or surprising tool output** just appeared. Query on the error text;
  a past session may have mapped it.
- You're **choosing among approaches / libraries / deps.** The graph may already
  hold the anti-pattern that kills the obvious choice.
- You're entering a **named subsystem** ("the auth layer", "the flake", "CI").

Do **not** query on trivial reads or things you can settle in one step. Retrieval
has a latency and noise cost; the rule below makes the trade explicit.

### Cost rule

> One `query_relevant` is cheap relative to one failed edit→build→read cycle.
> Query when the work ahead is more than ~2 exploratory steps. Don't query when
> it isn't.

### Using a surfaced belief — the discipline that prevents decoration

A belief is a **prior over your hypothesis space, not a fact to recite.** When
one bears on what you're about to do:

- **`probability ≥ 0.8` → load-bearing.** Either act consistently with it, or
  state in one line why you're overriding it. "Overriding belief X because the
  code changed in commit Y" is a legitimate move — and that override is itself a
  `record_defeat` observation (see WRITE). What is *not* legitimate is reading it
  and silently doing the thing it warns against.
- **Let `probability` set exploration depth.** A `p=0.9` "X fails because Y"
  means: don't spend five tool calls rediscovering it — verify in one, or skip.
  A `p=0.3` hint means weight it lightly and keep your other hypotheses live.
- **Let `confidence` set your trust in the probability.** Low confidence = the
  past session wasn't sure either; corroborate before you lean on it.
- **Causal questions deserve the causal tools.** If you're asking "if I change
  X, what downstream breaks?", that's an intervention, not a keyword match —
  use `query_intervention` (once available) rather than reading `CAUSES` edges
  by hand.

### Keep mimir and muninn distinct

If muninn is also wired: **muninn answers "where is X in the code"; mimir
answers "what did I learn that should change my approach."** Don't query mimir
for code locations or muninn for lessons. Conflating them makes both noisier.

---

## WRITE — growing the graph

### The mandate

After every non-trivial exchange, *before composing your final reply*, ask:

> Did I just learn, surface, or get corrected on something that — if true at the
> start of this session — would have changed what I did, **and** would plausibly
> apply in a future session?

If yes, insert it. If you'd have to think longer than five seconds about whether
it qualifies, insert it. A redundant insert is cheap; a lost hard-won insight is
not. If you discover something insertable mid-turn, **write it immediately**,
then continue — "later" is when the conversation is closed.

### Default: insert. Reverse the burden of proof.

The decision is not *"should I insert this?"* but *"is there a clean reason **not**
to?"*

| Keep out | Insert |
|---|---|
| Already in CLAUDE.md / AGENTS.md / project docs | Generalises past this one codebase |
| Trivially derivable by reading code | Teaches something the docs don't capture |
| Purely ephemeral (today's PR #, path) — or tag `project=<name>` and `delete_project` later | The user corrected you (calibrate confidence to residual uncertainty) |
| Restatement of language/stdlib docs | Took two failed attempts to discover |

### Triggers — almost always insert

1. **Debugging took more than two failed attempts.**
2. **You picked a library/dep/approach and it was worse than it looked.** Insert
   the anti-pattern + the test that would have surfaced it earlier.
3. **Infrastructure violated a "should just work" assumption** (registry rejects
   default UAs, CI masks local-only effects, version coupling between
   separately-managed pieces, build sandbox blocks network).
4. **The user corrected you** — especially if it reveals a *class* of mistake.
5. **You proposed N approaches and the user picked the unobvious one.** Their
   reasoning is the belief.
6. **You ran a postmortem.** Each non-trivial conclusion is a candidate.
7. **A non-obvious sequence works while the obvious one doesn't.** → `insert_pattern`.
8. **A user preference is stable across turns.** Mirror it as a belief for
   cross-project carryover even if it's also in auto-memory.

### Observe and link, during work

This is where READ and WRITE join up:

- New observation **confirms** a surfaced belief → `record_support(obs_id, belief_id, weight)`.
- New observation **contradicts** one → `record_defeat(obs_id, belief_id, weight)` (cascades to dependents). **Every override you made under the READ discipline lands here.**
- Two beliefs disagree (`get_contradictions`) → reconcile via `update_confidence` or `record_defeat`.
- You acted on a `CAUSES` belief and the predicted downstream effect did/didn't happen → that's support/defeat on the causal claim specifically.

### Mechanics — the tool calls

Full schemas in `mcp__mimir__*`; if you forget a parameter list mid-task, run
`ToolSearch` with `select:mcp__mimir__insert_belief,mcp__mimir__insert_pattern`.

- `insert_belief(content, probability, confidence, project?)` — a factual claim
  with epistemic state. `content` is a sentence or short paragraph; the two
  numbers are 0.0–1.0.
- `insert_pattern(situation, approach, success_rate)` — a "when X, do Y" rule.
  Third field is `success_rate`, not `confidence`.
- `record_support(obs_id, belief_id, weight)` / `record_defeat(obs_id, belief_id, weight)`.

Others: `get_belief`, `list_beliefs`, `update_confidence`, `delete_belief`,
`get_contradictions`, `propagate_from`, and (Phase 1) `query_intervention`.

### Calibration

Never `probability=1.0, confidence=1.0` unless it's a hard constraint with
catastrophic consequence — flat saturation is information-free. When unsure of
the row, pick the lower one and revisit when corroborated.

| Type | probability | confidence |
|---|---|---|
| Hard constraint, catastrophic if violated | 1.0 | 1.0 |
| Strong widely-applicable heuristic | 0.90–0.98 | 0.85–0.95 |
| Useful but context-dependent rule | 0.60–0.85 | 0.70–0.90 |
| Project-specific hint | 0.20–0.40 | 0.60–0.80 |

### Shapes that earn an insert (anonymised real cases)

- **Belief**: "crates.io 403s `curl/X.Y.Z` UA on the crate-download endpoint; Nix
  builds that hit it need a `fetchurl` overlay injecting a contact-bearing UA. A
  warm local `/nix/store` masks it — only fresh CI runners exhibit it."
  *p 0.90, c 0.85.*
- **Belief**: "When pinning a vendored ML runtime archive in flake.nix, also pin
  the consuming `*-sys` crate to the exact matching ABI; loose `=2.0.0-rc` lets
  `cargo update` bump it → runtime panic against the older static lib." *p 0.95, c 0.90.*
- **Pattern**: situation *"evaluating a library swap"*, approach *"spike with
  realistic inputs from the actual target project; v0.1.x crates pass smoke tests
  and fail on real data."* *success_rate 0.85.*

Writing 2–3 inserts at the end of a multi-step task is the cadence, not overkill.

---

## Honest self-check before closing

1. Did I write *anything* this conversation? If no, am I certain nothing qualified?
2. Did the user correct me in ways I haven't recorded?
3. Did I solve something non-obvious a future Claude would re-derive from scratch?
4. **Did I override or ignore any surfaced belief without recording why?** If so,
   that's a `record_defeat` or an `update_confidence` I still owe the graph.
5. Did any tooling quirk surprise me?

If any answer nags, act before closing. That nag is the signal.

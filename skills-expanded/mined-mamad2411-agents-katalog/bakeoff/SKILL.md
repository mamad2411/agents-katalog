---
name: bakeoff
argument-hint: "<request — a decision, idea, comparison, or 'what if'>"
description: >
  Turn one decision into a judged tournament of solutions, then pick the best. Given a problem,
  design choice, or a suggestion you want cross-verified, it generates diverse candidate solutions,
  auto-derives the evaluation dimensions for THAT problem (so you don't have to know what to score
  on), judges every candidate with independent scorers, and returns the winner plus a ranked top-N
  shortlist with a score matrix and rationale. It auto-infers the request shape — idea · improvement ·
  comparison · proposal ("what if we do X") · problem-solving · scoping — from your bare prompt, with
  no flags. Reach for it whenever there are several defensible
  approaches, the call is costly to reverse, and you can't easily say why one option wins — even if
  the user doesn't say "compare" or "decide": "what's the best way to structure X", "which
  approach/library/database/design should I pick", "compare these two plans", "is the AI's
  suggestion actually good, or is there something better", "help me decide X vs Y vs Z",
  architecture / approach / refactor / migration / tool-selection calls, or any stakes-bearing
  "which should I…". Distinct from `evaluate` (which scores ONE artifact against a rubric) — reach
  for bakeoff when you need to CHOOSE among several options or generate them. NOT for tasks a
  test, type-check, or lint settles (bug fixes, mechanical refactors, formatting, "write a function
  that does X"), and NOT for evaluating a single existing thing with no alternatives (that's
  `evaluate`) — a tournament of one is wasted effort.
---

# Bakeoff

You turn *"which of these should I do?"* into a defensible answer. You **generate** diverse
candidate solutions, **auto-derive** the criteria that matter for this specific problem, **judge**
the candidates independently, and **select** the winner (plus a top-N shortlist) — with the reason
each one won or lost.

Two problems this solves at once: you stop hand-running the role-agents/judges/synthesis loop, and
you stop having to know the evaluation dimensions yourself — the rubric is built for *this* problem,
grounded in real facts when the decision needs it (see *Grounding*), not a generic checklist.

## When to use it (all three must hold)
1. **Wide solution space** — several genuinely defensible approaches, not one obvious answer.
2. **Costly to reverse** — a wrong call is expensive to unwind.
3. **Unclear criteria** — you can't easily say *why* one option beats another.

If a test, type-check, or lint settles it, don't run a tournament — answer directly.

**Any request *shape* qualifies** — a comparison ("X vs Y"), an improvement ("best way to X"), an
idea ("what should we build"), a proposal ("what if we do X / should we add X"), a problem ("how do
we handle this"), or a scoping call ("minimal X before launch"). You infer the shape (Step 1); the
user need not phrase it as a "decision." **The three-part gate above still governs** — broaden what
you *recognize*, never lower *when to fire* (a low-stakes or single-obvious-answer "which/how" is
still a direct answer, not a tournament).

**Rationalizations (when you're tempted to skip it).** These are the excuses that precede a bad,
hard-to-reverse call — each is a reason to *run* the tournament, not skip it:

| The excuse | The reality |
|-----------|-------------|
| "I already know the best option." | Then a `--lean` run confirms it cheaply — and if it doesn't, you just dodged a costly wrong call. Confidence isn't evidence. |
| "Just pick the popular / default one." | Popularity isn't fit *for this problem*; the auto-derived rubric tests fit, and the adversarial pass catches the case where the obvious pick is actually wrong (see the worked example — both judges picked the runner-up). |
| "Generating rivals is wasted effort." | Diversity is the lever selection exploits; one option iterated is exactly the mush this avoids. |
| "There's no time." | `--lean` is ~3 candidates / 1 judge / minutes. The wrong architecture, library, or migration costs far more than one lean run. |

## Design principles (why it's built this way)
- **Select, then graft.** Diverse candidates + judge-based *selection* is the core — it exploits
  variance a naive average would waste. But synthesis is a *first-class* follow-up, not a grudging
  afterthought: when the top two are strong on *different* dimensions, graft the runner-up's best
  element into the winner and keep it **only if it re-scores above the best single candidate** (the
  guard). In practice the graft wins or sharpens the pick as often as it's discarded.
- **Diversity is the biggest lever.** Candidate generators get **distinct, problem-specific roles**;
  a homogeneous set of candidates makes the whole exercise pointless.
- **Independent judges, mechanically reconciled** — not a free debate (debate can amplify bias).
  Two judges score independently; scores are merged by the deterministic reconciler.
- **Kill position bias** — each judge sees the candidates in a different shuffled order, referenced
  by stable IDs (mechanics in Step 4).
- **Adversarially verify the leader** — before committing, one agent actively tries to *refute* the
  top candidate. A plausible-but-wrong winner should not survive.

## Grounding (conditional, silent)
A tournament is only as good as the facts under it. **When the decision depends on reality, ground it
— silently, with whatever fitting read-only tools this environment offers.** Use what's available;
don't hard-code tool names, and reach for `ToolSearch` if a needed capability looks deferred:
- **External facts** — a library / tool / version, or current best practice → a live web or
  docs-search tool.
- **This codebase** — "how should *we*…", "refactor *our*…" → read the actual files + whatever project
  search exists; else `grep`/read directly. In a repo, **default to reading the code** — the decisive
  fact (a silent fallback, a "phantom" regression that can't actually happen, a data-loss path) is
  usually only found by grounding, not by reasoning.
- **Attached images / screenshots** — a UI bug, a mockup, a diagram in the prompt → read them; they
  are often the load-bearing evidence.
- **A decision this reverses** — "overturn our X decision", "we decided Y before" → read the referenced
  ADR / decision doc so the reversal is argued against the *real* prior rationale, not a guess at it.
- **Self-contained / internal** decision → skip grounding; don't add latency.

**Weigh what you find** — the same anti-homogeneity rule the candidates get, applied to evidence.
Prefer primary/authoritative sources (official docs, the actual code, a maintainer's statement) over
echoes; **dedup by *entity*, not string** (three blog posts repeating one release note are one fact,
not three); and don't let a single loud source carry a whole dimension. A load-bearing claim rides
on its *strongest* source, not the *count* of sources.

Read-only grounding needs **no permission prompt** — the harness already gates tool use, so a second
"may I search?" is pure friction. Reserve consent for genuinely costly, side-effecting, or auth-walled
tools. But never hide a gap: **if grounding is needed and no tool can supply it (or you're unsure the
facts are current), say so and mark the affected output "training-knowledge only — may be stale."** An
ungrounded pick presented as confident is the one failure this step exists to prevent.

## Modes & depth
**Entry point — inferred from the prompt, no flag needed.** You almost always **generate** the
candidates. The only variation, inferred automatically:
- **If the prompt names a concrete option or hands you a plan/proposal** ("X vs Y vs Z", "should the
  hero be GitHub-only?", "what if we collapse to one UI?") → make each *named, concrete* option a
  candidate **and still invent 1–2 rivals + the floor candidate** (see Step 2). This is the
  "cross-verify what I've got / weigh these options" case — it needs no flag.
- **Otherwise** → generate the whole field from scratch.
- Either way, **always add rivals** — never just judge what the user handed you (a homogeneous field
  is the failure this skill exists to prevent). A *vague* direction ("show info or trigger something")
  is **not** a concrete option — generate from scratch, don't seed it.

*Optional power-user overrides* (rarely needed — the inference above covers them): `--seed <path|"text">`
forces a plan as Candidate A; `--compare` (+2–4 pasted candidates) does pure judging with no generation
(still add rivals unless the user insists on judging only their set).

**Depth** — how hard it tries. **When no depth flag is passed, Frame auto-selects one from the
decision's *grounded* stakes** (surfaced at the checkpoint, where you can bump it); an explicit
`--lean`/`--thorough` always overrides. Each row is the *complete* setting — candidate count, judge
count, refute, synthesis, **and the rubric-builder model** all follow from the depth, so the steps
below just branch on "lean / default / thorough":

| Depth | Candidates | Judges | Refute | Synthesis | Rubric model | Auto-picked when the decision is… |
|-------|-----------|--------|--------|-----------|--------------|-----------------------------------|
| `--lean` | 3 | **1** (skip reconcile) | no | no | **Sonnet** | narrow options · **low grounded magnitude** · easily reversible / per-item-gated / internal |
| *default* | 4 | 2 + reconcile | yes | offered | **Opus** | several defensible options **and material grounded magnitude** · costly-to-reverse but recoverable |
| `--thorough` | 5–6 | 2 + reconcile | yes | yes | **Opus** | high blast radius: irreversible · prod · data-model / public-API / migration / security |

The rubric build is the one call where reasoning quality most changes the outcome, so it gets **Opus**
at default/`--thorough` and drops to **Sonnet** only at `--lean` (small, reversible calls). `--thorough`
always confirms its cost before spending (auto-picked or flagged).

**Auto-pick keys off *grounded magnitude*, not the surface shape of the question.** "Several
defensible options" and "sounds costly-to-reverse" are *necessary* signals, not sufficient ones — a
decision can present as weighty yet turn out small once you know the real numbers (the dollars per
month, the blast radius, whether it's per-item-gated and trivially backed out). Frame gathers that
magnitude cheaply *as part of grounding* (Step 1) **before** locking the tier, so a genuinely small,
reversible call lands on `--lean` instead of paying default-depth effort — the failure this step
prevents is a two-judge Opus-rubric run on a choice the adversarial round would have shown was a
rounding error.

## Worked example
`/bakeoff "should our new ingestion service be a monolith, a modular monolith, or split services?"`

```
Roles derived → scalability-first · simplicity-first · migration-safety-first · cost-first
Rubric (auto)  → Operational simplicity 25 · Scale headroom 20 · Migration risk 20 ·
                 Cognitive load 15 · Cost 12 · Evolvability 8      [approve? yes]
Judges x2 → reconcile → shortlist:
   1. Modular monolith   87   wins on simplicity + migration risk; loses on scale headroom
   2. Monolith           79
   3. Services           74   best scale, worst migration risk + cost
Refute #1: "a modular monolith rots into a big ball of mud" → rubric already weights
           Evolvability; the candidate's module boundaries address it → survives.
Winner: Modular monolith — strongest on the two highest-weight dims, robust across both judges.
```

Note what the user never had to supply: the six dimensions and their weights. That's the point —
the hard part (knowing what to evaluate) is derived, not demanded.

---

## Pipeline

```
FRAME → { GENERATE (K candidates)  ∥  BUILD RUBRIC } → [rubric gate — scaled to depth] →
   JUDGE (2 scorers ∥, randomized order, reconciled) →
   RANK → ADVERSARIAL CHECK (one round, only if the top-two are close or the leader is suspect) →
   best + top-N shortlist (+ optional synthesis) → REPORT
```

**Critical path ≈ 3 serial subagent rounds** on a decisive default run: `{generate ∥ rubric}` → `judge`
→ `report`, with refute added only when the win is close. Keep it that way — run independent stages
in parallel, and keep the cheap steps (diversity check, reconcile, ranking, report assembly) **inline,
not extra subagent rounds**.

Run with **minimal ceremony**: surface the derived roles and the rubric, pause for approval only when
the depth calls for it (default/thorough — lean shows and proceeds), deliver the result. Don't
announce each step or narrate the plumbing — the user wants the decision, not a play-by-play.

### 1. Frame (quietly)
**No setup narration.** Skip any "you invoked bakeoff / let me confirm the assets / now I'll frame
the decision" preamble — the user knows what they ran and doesn't need the plumbing described. Open
with the substance (the derived roles, then the rubric at the checkpoint). Verify the reused
`evaluate` assets exist **silently** (*Dependencies & schema contract*) and speak up *only* if one is
missing — then say bakeoff builds on the `evaluate` skill and stop. Extract the **decision**, any
hard constraints, and the shortlist size `N` (default 3).

**Classify the request shape (inferred from the prompt, never a flag) — it drives how candidates
arrive and what the rubric must weight:**
- **comparison** ("X vs Y vs Z", "A or B") → each *named, concrete* option becomes a candidate; still
  invent 1–2 adjacents.
- **proposal** ("what if we do X", "should we add X") · **idea** ("what should we build", "which
  surface") · **scoping** ("minimal X before launch", "smallest thing that…") → generate, and
  **always include a genuine defer / minimal / status-quo candidate** (do-nothing · keep-what-we-have
  · ship-the-smallest-thing · just-measure). In real runs the defer option *often wins* — but only if
  it's actually in the field and the rubric can reward it (Step 3).
- **problem-solving** ("how do we handle [this diagnosed problem]") → generate strategies; include a
  **minimal / highest-leverage-least-effort** candidate (the cheapest thing that moves the needle).
- **improvement / structure** ("best way to revise/organize X", "make X better") → generate approaches;
  a positive answer is required, so **no** forced defer candidate.

A secondary either/or bundled in the prompt (e.g. "…and should we gate it or show it live?") is **a
rubric axis or a line in the recommendation, not a separate set of candidates.**

**Choose the depth — from *grounded* stakes, not the question's surface.** Honor an explicit
`--lean`/`--thorough`; otherwise infer it, but **sniff the real magnitude first** (as a cheap part of
grounding, before locking the tier): what does a wrong call actually cost — dollars/month, blast
radius, is it per-item-gated and trivially reversible? A decision can *sound* weighty ("which
generation strategy", "which store") yet be a rounding error once grounded (a ~$30–150/mo,
per-project-gated, easily-backed-out call is `--lean`, not default — don't spend two judges and an
Opus rubric to discover that in the adversarial round). Then map the **grounded** stakes: narrow +
low-magnitude + easily reversible → *lean*; a real costly-to-reverse choice with material magnitude →
*default*; irreversible / high blast radius (prod, data model, public API, migration, security) →
*thorough* (see *Modes & depth*). "Several defensible options" alone doesn't earn default — magnitude
does. The depth fixes the candidate count `K`, the judge count, refute/synthesis, and the
rubric-builder model, and is shown at the checkpoint so you can bump it (and if grounding later
reveals the magnitude was mis-sized, say so and re-size before judging). If you infer *thorough*,
confirm its cost before generating (the ~$5–10 tier). If the problem is too
vague to produce distinct candidates ("make it better"), ask one sharpening question first — a fuzzy
decision yields fuzzy candidates the tournament can't recover. Save nothing to global state; this is a
single self-contained run.

### 2. Generate candidates (skip in `--compare`)
First derive **K distinct roles/strategies appropriate to THIS problem** — not generic personas.
Examples: an architecture choice → `scalability-first · simplicity-first · cost-first ·
migration-safety-first`; a library choice → `DX-first · lock-in-averse · maintenance/△-first ·
performance-first`; a refactor → `blast-radius-minimal · incremental · clean-slate ·
test-coverage-first`. State the chosen roles in one line so the diversity is visible.

**Include the right "floor" candidate (from the request shape, Step 1).** For a **proposal / idea /
scoping** request, one of the K roles *must* be a genuine **defer / minimal / status-quo** —
do-nothing · keep-what-we-have · ship-the-smallest-thing · just-measure-and-learn. For
**problem-solving**, include a **minimal / highest-leverage-least-effort** option. This isn't padding:
across real runs the floor candidate frequently *wins*, and a field without it simply cannot produce
the correct "not yet / do the smallest thing" answer. **Skip the floor for improvement/comparison**,
where a positive answer is required.

Dispatch **K generator subagents in parallel**, one per role (model: **Sonnet**; `K` = 4 by default,
**3 under `--lean`, 5–6 under `--thorough`**). Each returns a **self-contained candidate**: the
approach, key decisions, tradeoffs it accepts, and (for code) concrete shape/`file:line` touch-points
— not a vague sketch. **Ground them when the decision needs it** (*Grounding*): search current facts
for a tool/library choice, read the real code for a codebase choice — so candidates are specific, not
generic guesses. Assign stable IDs (**A, B, C, …**). If the prompt named a concrete option/proposal
(or `--seed` was passed), that becomes **Candidate A** and you generate `K-1` rivals; otherwise all K
are invented from scratch.

**Carry the grounding forward.** When a candidate grounds a load-bearing claim, it must surface the
*evidence anchor* alongside the claim — the exact `file:line` it read, or the URL/doc + the specific
fact it pulled — as a compact `evidence:` list on the candidate, not just prose. This isn't
bookkeeping: it's what lets the judges **re-check the same anchors instead of re-grounding the whole
decision cold** (Step 4), which is where a big slice of the judge-stage wall-clock otherwise goes. A
load-bearing claim with no anchor is fair game for a judge to treat as unverified.

### 3. Build the shared rubric (the "what do I evaluate?" step) — runs ∥ with Step 2
**Dispatch this at the same time as generation, not after it.** The rubric is the criteria for the
*decision*, so it doesn't need the candidates — running the (slow) Opus build concurrently with the
generators keeps it off the critical path, and deriving criteria from the decision rather than the
specific options **avoids tailoring the rubric to favor one** (a quality win, not just a speed one).
Dispatch the **evaluate skill's Framework Builder** to derive the dimensions, weights, and 5-band
rubric **for this decision** — read and follow the bundled `agents/evaluate-build.md` (in this skill's directory), passing the
**decision + domain (and the role list), not the generated candidates** (**rubric model follows the
depth**: Opus at default/`--thorough`, Sonnet at `--lean` — see *Modes & depth*). This produces the
criteria you didn't know to pick.

**For proposal / idea / scoping requests, the rubric MUST include a dimension where *deferring — or
doing the minimal thing — when justified scores HIGH*** (stage-fit · opportunity cost · reversibility ·
low-regret). Without it the correct "don't build it yet" answer literally cannot win — in real runs
the defer candidate won *because* the rubric rewarded restraint on exactly this dimension. Do **not**
add it for improvement/comparison, where a positive answer is required and "do nothing" isn't on the
table.

For a decision that hinges on current external facts, the builder grounds its
dimensions the same way (*Grounding*) so they reflect today's reality — and marks the rubric
training-knowledge-only if it can't. Validate it the same way evaluate does (weights sum to 100, all 5 bands,
concrete criteria, `scoring_guide` present).

**Amend for candidate-specific gaps (inline, ~0 cost).** Because the rubric was built in parallel,
blind to the candidates, do a quick read once they're back: did any candidate raise a consideration
the rubric doesn't capture — a distinctive failure mode or a tradeoff class the decision-framing
didn't predict? If so, **add that dimension and re-normalize to 100** before the gate. This closes the
parallel build's one blind spot without a subagent round (it's a read, not new reasoning).

**Rubric gate — scaled to the depth.** The rubric is the decision's value function, so a wrong one
yields a *confidently* wrong winner; but how hard to stop for it scales with the stakes:
- **lean → show, don't stop.** Print the rubric in one line and roll straight into judging — e.g.
  *"Judging on: Simplicity 30 · Reversibility 25 · Cost 20 · … — say 'hold' to adjust."* The user
  still sees what's being measured (the payoff: they didn't know the dimensions), but a small,
  reversible call doesn't earn a blocking stop.
- **default → quick confirm.** Show the block below and wait for a yes — a costly-to-reverse choice
  is worth a five-second glance at its value function.
- **thorough → full gate.** Always stop: you're about to spend ~$5–10, so catching a wrong rubric
  now is far cheaper than discovering it after judging.

**Overrides** (per-run prose, as in evaluate): *"just go"* / `--no-gate` skips the confirm at default
too; *"walk me through"* forces the full stop even at lean.

```
Deciding: "<decision>"   Candidates: A/B/C/D (<roles>)
Depth: <lean|default|thorough> — <K> candidates · <1|2> judge(s) · <Sonnet|Opus> rubric  (auto: <why>)
Rubric (<n> dims): <Dim> (<w>%), <Dim> (<w>%), …
Proceed to judging? (yes / make it lean|thorough / adjust weights / add or remove a dimension)
```
Show the `Depth` line only when depth was **auto-picked**. Weight/dimension edits apply directly
(re-normalize to 100) without re-running the builder. Bumping depth re-sizes the run — generate any
extra candidates (and rebuild the rubric if crossing into Opus territory) before judging;
`--thorough` re-confirms cost first.

### 4. Judge (independent, reconciled, bias-controlled)
Dispatch the judge panel — **2 independent judges by default, 1 under `--lean`** (model: **Sonnet**);
follow the scoring discipline in the bundled `agents/evaluate-score.md` (band-first, verbatim evidence,
`scoring_confidence`, weight toward the weaker finding, no inflation). Each judge scores **every
candidate on every dimension**,
and is shown the candidates in a **distinct order per judge** — independently shuffle/rotate the IDs
for each judge (not a fixed A,B,C,D for one and C,D,A,B for the other), so no single slot
systematically favors a candidate across the panel. Judges never see each other's scores. Judges
**verify** a candidate's factual or codebase claims with their read/search tools rather than trust
them — an unverified load-bearing claim caps that dimension's confidence instead of earning full credit.

**Re-check the carried anchors first; don't re-ground cold.** The candidates already arrive with an
`evidence:` list (Step 2) — the `file:line` they read, the URL + fact they pulled. A judge verifies by
**re-checking those exact anchors** (re-read the cited lines, re-open the cited source), which is a
cheap confirm, *not* a fresh from-scratch search of the whole decision. Only spend a cold
search/read when a load-bearing claim has **no** anchor, or its anchor doesn't actually support it
(that's the discrepancy worth the time). This is the same verification rigor — an anchor that fails
the re-check still caps the dimension's confidence — done without every judge independently
re-grounding what the generators already grounded, which is the main avoidable cost in the judge stage.

**Reconcile per candidate.** For each candidate `X`, write judge 1's and judge 2's scores for that
candidate to `judge1-X.yaml` / `judge2-X.yaml` (in the `dimension_scores:` schema — see *Dependencies
& schema contract*) and run the bundled `scripts/reconcile-scores.js judge1-X.yaml judge2-X.yaml`
(needs Node.js). Use the merged
per-dimension scores and the `Math.floor` weighted overall it returns. A `CALIBRATION_DISCREPANCY`
(judges >8 apart on a dimension) uses the lower score and is noted — a candidate whose lead rests on
a *contested* dimension is a weaker pick, not a stronger one, because the win isn't robust.
*Under `--lean` (one judge) there's a single score set — skip `reconcile-scores.js` (it needs two
files) and use that judge's scores directly, at reduced confidence.*

**One adversarial round, not two.** Don't run a standalone refute *and* a separate tie-break — a
benchmark caught that as a redundant pair of serial rounds on a close race. The adversarial check is
resolved once, in Step 5 (Rank), and only when it can change the outcome: a decisive, robust #1 gets
none; a close top-two gets one **combined adversarial-pairwise** round; a *decisive-but-suspect*
leader (wins clearly, yet its lead rests on a contested `CALIBRATION_DISCREPANCY` or low-confidence
high-weight dimension, with no close rival to compare against) gets a standalone refute there.
`--thorough` always runs one adversarial round; `--lean` never does.

### 5. Rank → select (optional synthesize)
Rank candidates by reconciled weighted overall. Produce the **winner** and the **top-N shortlist**.

**Resolve the top of the field — one adversarial round, only where it matters:**
- **Decisive & robust #1** (top-two gap > a ~judge-delta, and its lead isn't propped up by a
  contested/low-confidence high-weight dimension): accept it — **no adversarial round** (the fast path).
- **Close top-two** (within ~8 pts — a pointwise gap that small is noise): dispatch **one combined
  adversarial-pairwise** round that does both jobs at once — *"Compare these two head-to-head against
  the rubric: which better satisfies it, and where does EACH fail or get over-credited?"*, pair shown
  in randomized order. Let it decide; if still a genuine toss-up, present **both as co-winners** to
  break on a factor the user weights. *(This one round replaces the old separate refute + tie-break.)*
- **Decisive-but-suspect #1** (wins clearly, but its lead rests on a contested/low-confidence
  high-weight dimension — no close rival for a pairwise): one **standalone refute** of #1 instead.

When an adversarial round lands a load-bearing hit, don't hand-edit the score — hand the challenge
back to the judges to **re-score only the affected dimension(s)**, then re-reconcile and re-rank (a
judged result, not the orchestrator's opinion). If the adversarial agent fails, retry once, then
proceed and note the leader wasn't stress-tested.

**Synthesis — attempt the graft by default when the top two are complementary** (**forced under
`--thorough`**, **skipped only under `--lean`**). When the winner and a close runner-up are strong on
*different* high-weight dimensions, graft the runner-up's strongest element(s) into the winner,
generate the merged candidate, and **re-score it against the same rubric**. Keep it **only if it
out-scores the best single candidate** — that guard is what makes this safe. This earns its place
often: across real runs a synthesis has *won outright* about as often as it's been discarded, and
even when the single winner holds, the graft usually sharpens the recommendation. (The "blending
wastes variance" caution only bites when the top two *aren't* actually complementary — then the
re-score guard rejects the merge and you ship the single winner, no harm done.)

### 6. Report
Assemble the report **inline** (or one fast Haiku pass) — it's formatting, not reasoning, so don't
spend a heavyweight round on it; the scores are already computed by the reconciler. Save the full
report to `docs/bakeoffs/YYYY-MM-DD-<slug>.md` (or `--output`) and print the terminal summary. **The
exact report and terminal-summary templates live in
[`references/report-shape.md`](references/report-shape.md)** — read it at this step. The essentials:
lead with the **recommendation** (winner + why), then the **shortlist** and the **score matrix**
(the auditable core), each candidate with its judge-agreement, the refute result, dissents, optional
synthesis, and the full rubric in a `<details>` block so the run is self-contained and reusable.

**With `--html`**, also write a self-contained HTML twin next to the markdown (`…-<slug>.html`) —
inline CSS, dark-mode, no JavaScript, no external assets — so it drops straight into Slack, email, or
a wiki. Same content and numbers, presentation-ready; the markdown stays the source of truth. The
HTML shape is specified in [`references/report-shape.md`](references/report-shape.md).

---

## Failure & edge cases
A tournament is only as good as its inputs, so guard the ways it can quietly degrade:
- **Too few candidates to judge.** `--compare` with fewer than 2 candidates isn't a decision — ask
  for at least one rival (or offer to generate them). Generation below `K=2` is pointless; default up.
- **Low-diversity candidates.** If the generated candidates converge on the same approach, the
  "tournament" is theatre. Before judging, sanity-check **inline** (read the returned candidates
  yourself — no subagent round) that they differ *materially*; if two collapse onto the same approach,
  regenerate **only those**, not the whole field — a homogeneous field is the failure mode diversity
  exists to prevent.
- **A subagent fails.** Retry a dead generator/judge once. If one judge still fails, fall back to a
  single-judge score and note the reduced confidence (no silent partial results). If *both* judges
  fail, abort with a clear message rather than emitting a fabricated ranking — an unjudged tournament
  is worse than none. If a generator still fails, proceed with the surviving candidates and record
  that the field was thinned. If the **refute agent** fails, retry once, then proceed and note the
  leader wasn't adversarially stress-tested — the ranking still stands, since refute only ever
  *demotes* a shaky leader, never promotes one.
- **Rubric build fails or looks wrong.** If the Framework Builder can't produce a valid framework,
  don't fabricate one — surface it and either retry or ask the user for the two or three criteria
  they care about, then build a minimal rubric from those.
- **The user disagrees with the winner.** That's expected and fine — the shortlist and score matrix
  exist precisely so a human can override on a factor they weight differently. Present the pick as
  *well-supported*, not final.
- **Cost guard.** Before a `--thorough` run (5-6 candidates, refute, synthesis), state the rough cost
  and confirm — a decision-grade tournament is worth it for a hard-to-reverse call, wasteful for a
  small one.

## Dependencies & schema contract
This skill builds on the rubric-building and score-reconciliation logic of the `evaluate` skill, but
**ships its own vendored copies** so it runs standalone — no separate install required. The three
bundled assets live inside this skill's directory (verify they exist; fail fast with a clear message
if not): `agents/evaluate-build.md`, `agents/evaluate-score.md`, and `scripts/reconcile-scores.js`
(the last needs Node.js on `PATH`).

`reconcile-scores.js` reconciles **two scorers of one subject**, so run it **once per candidate**
(the two judges are its agent A / agent B for that candidate). Each judge must therefore emit the
exact schema the script parses — a top-level `dimension_scores:` list, one `- name:` entry per
dimension with `score`/`band` — the same contract `evaluate-score.md` defines. Write each judge's
per-candidate YAML to its own file and pass the pair to the script; use the merged per-dimension
scores it returns. (The single-judge `--lean` case is handled inline in Step 4.)

## Flags
**No flags are required** — the request shape, entry point (generate vs seed-a-named-option), depth,
and rubric are all inferred from a bare prompt. The flags below are optional overrides. Entry point
(`--seed`, `--compare`) and depth (`--lean`, `--thorough`) are defined in *Modes & depth* above; the
remaining knobs:

| Flag | Purpose | Default |
|------|---------|---------|
| `--candidates <K>` | Override the per-depth candidate count | see *Modes & depth* |
| `--top <N>` | Shortlist size in the report | 3 |
| `--roles "X, Y, Z"` | Override the auto-derived generator roles | Auto per problem |
| `--synthesize` | Force the graft step even at default depth (still kept only if it out-scores the field) | — |
| `--output <path>` | Custom report path | `docs/bakeoffs/…` |
| `--html` | Also emit a self-contained HTML report (dark-mode, inline CSS, no JS) beside the markdown | — |

## Cost & honesty
Roughly the cost of a few `evaluate` scoring passes (~$2–4 at default depth); the estimate is printed
in the report metadata. Judges are LLMs (≈±8 pt variance), so the winner is a *well-supported* pick,
not an oracle — when the top two are within a judge-delta, the report presents them as a tie to break
on a factor you weight, rather than forcing false precision.

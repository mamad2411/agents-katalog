<!--
  SKILL.md — Growth Hacker operating manual.
  Runtime: Claude Code + ACP (swappable coding CLI). Content stays LCD —
  no assumptions about a specific analytics or experiment platform unless
  injected via a stack overlay. Stack-specific tools are NOT here — they live
  in stacks/<stack>/ overlays. Injection points are marked: `STACK: ...`
-->

# Skill: Growth Hacker

## Invocation

```
/growth_hacker <goal / metric — e.g. "raise trial→paid conversion">
```

Or picked up from a Signal Protocol entry / PR assigned to growth-hacker. Either
way: **no metric, no experiment.** If there's no target metric and no funnel to
point at, ask for one.

---

## Step 1 — Map the funnel and pick the bottleneck metric

Before proposing anything, lay out the funnel and find the binding constraint:

| Question | Why |
|---|---|
| What are the funnel steps, end to end? | You optimise a step, not a vibe — name them all |
| What is the volume and drop-off at each step? | The biggest leak with the most upstream volume is the target |
| What is the one metric this goal moves? | One primary metric per experiment; everything else is a guardrail |
| What's the current baseline for that metric? | No baseline → no way to read a lift; get it first |
| What surface does the leaking step live on? | Determines risk tier and who you'll hand build work to |

<!-- STACK: analytics platform + how to pull the funnel report injected here -->

**Rule:** Pick the single step where a win has the most leverage. If the funnel
data doesn't exist or the baseline is unknown, that's the first task — flag
data-analyst / data-engineer, don't guess a baseline.

---

## Step 2 — Form a hypothesis

Write the belief before the test, in one sentence:

```
IF we <change one variable>
THEN <primary metric> will <move in this direction by ~this much>
BECAUSE <the user reason we believe it>.
```

- **One variable.** If you can't name the single thing changing, the hypothesis is too broad — split it.
- **Falsifiable.** State the expected direction and rough size so the result can prove you wrong.
- **Grounded.** The BECAUSE ties to a real user behaviour or a prior result, not a hunch.

---

## Step 3 — Design the experiment

Turn the hypothesis into a runnable test. Fill the experiment brief (template
below). Decide and write down:

- **Variant(s).** Control vs. exactly one changed variable. No bundled changes.
- **Sample size.** The number per arm needed to detect the expected effect at your confidence level — set it *before* launch.
- **Duration.** Long enough to cover a full business cycle (e.g. a week) and reach the sample; set an end date.
- **Success threshold.** The pre-committed lift on the primary metric that counts as a win. Decide it now so you can't move the goalposts later.
- **Guardrail metrics.** The metrics this change could quietly damage (see checklist). Set the tolerance that would force a kill even on a "winning" variant.

<!-- STACK: experiment / feature-flag / split-test tool + how to define arms injected here -->

---

## Step 4 — Instrument tracking

No decision on data you haven't validated.

- Confirm the primary-metric event fires on the right action, once, attributed to the right arm.
- Confirm the guardrail events fire too.
- Fire a test event end to end and see it land correctly before any real traffic.
- If tracking needs to be *built* (new events, attribution), that's build work — hand off to backend-dev / data-engineer; do not hand-roll it.

<!-- STACK: event tracking SDK / how to validate an event injected here -->

**Rule:** If events misfire, double-count, or don't attribute to the arm, stop.
Broken tracking produces confident wrong decisions — fix it before running.

---

## Step 5 — Run

- Launch both arms simultaneously to the same audience split.
- Do **not** peek-and-stop: reaching significance early by chance is a false win. Run to the pre-set sample/duration.
- Watch guardrails during the run — a hard guardrail breach (e.g. refunds spike, errors) is grounds to kill mid-flight; flag it.

---

## Step 6 — Read results honestly

Fill the results readout (template below). Read only after the pre-set
sample/duration is reached.

- **Effect size + significance.** Report the lift, the sample per arm, and the confidence/p-value. A directional wobble below significance is **not** a result — call it inconclusive.
- **Guardrails.** Check every guardrail metric. A primary lift that breached a guardrail is not a win.
- **Honest loss.** If the variant lost or tied, say so as plainly as a win. The learning is the deliverable either way.

---

## Step 7 — Decide: ship / kill / iterate

- **Ship** — significant lift, guardrails clean, win is worth making permanent → hand off the build (make variant the default) async. If the surface touches trust/data/revenue, escalate the ship decision per SOUL.
- **Kill** — lost, tied, or breached a guardrail → revert the variant, log the learning, move to the next ICE candidate.
- **Iterate** — promising but inconclusive (underpowered, or a sub-segment effect) → refine the hypothesis or sample and re-run.

Log the outcome in MEMORY (Experiments run) **whatever** it was. Then hand off
async per the Signal Protocol — never spawn a live agent.

---

## Experiment brief template (with ICE score)

```markdown
## Experiment: <short name>

- **Funnel step / metric:** <step> — primary metric: <metric> (baseline: <value>)
- **Hypothesis:** IF <one change> THEN <metric> <direction ~size> BECAUSE <reason>
- **Variant(s):** Control: <…> | Variant: <single change>
- **Sample / arm:** <n>   **Duration:** <start → end>
- **Success threshold:** <pre-committed lift that = win>
- **Guardrail metrics + tolerance:** <metric: max acceptable move>
- **Surface / risk tier:** <surface> — <low / trust-or-revenue (escalate)>

### ICE score (1–10 each)
| Impact | Confidence | Ease | ICE (avg) |
|--------|-----------|------|-----------|
| <n>    | <n>       | <n>  | <n>       |
```

---

## Results readout template

```markdown
## Result: <experiment name>  — <SHIP / KILL / ITERATE>

- **Primary metric:** control <x> vs variant <y> → lift <±%>
- **Sample / arm:** <n>   **Significance:** <p / confidence> — <significant? Y/N>
- **Guardrails:** <metric: moved ±% — within tolerance? Y/N> (each)
- **Verdict:** <ship/kill/iterate> — <one-line reason>
- **Learning:** <what this teaches about the funnel / users>
- **Handoff:** <what the next role must build, or "none">
```

---

## Guardrail-metrics checklist

Before any ship decision, confirm the "win" didn't cost more elsewhere:

- [ ] **Retention / churn** — more signups that don't stick is not growth
- [ ] **Downstream conversion** — a lift at this step didn't just push the leak one step down
- [ ] **Revenue / refunds / chargebacks** — more buyers but more refunds is a wash or worse
- [ ] **Support load / complaints** — a variant that confuses users shows up as tickets
- [ ] **Quality of acquired user** — engagement / activation of the new cohort, not just count
- [ ] **No dark-pattern signal** — opt-out rate, consent withdrawals, trust complaints
- [ ] **Tracking integrity** — events still firing correctly across the full run

<!-- STACK: stack-specific significance test + guardrail dashboard injected here -->

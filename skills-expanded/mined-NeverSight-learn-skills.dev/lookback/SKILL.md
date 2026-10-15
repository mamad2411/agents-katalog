---
name: lookback
description: Solo premortem. Imagine the launch failed; work back to why. Top 5 failure scenarios, each research-defended, classed real or disregarded, delivered as who/what/why/do — owner first, every scenario ends in a pre-agreed action with an observable trigger. Qualified opinion grounded in current evidence.
license: MIT
metadata: { version: 2.1.0, category: decision-discipline }
---

## Purpose

Find what would kill the launch before it happens. The frame is the engine:

> It is 6–18 months from now. The launch has clearly failed on its success
> outcomes. Work backward.

Everything generates under that frame. The output is the top 5 critical failure
scenarios — each defended with research, each owned, each ending in a pre-agreed
action.

Not for: post-event analysis · team facilitation · market analysis.

**Use:** pre-launch · pre-commitment · before scaling a decision · before
resource investment with high reversal cost.
**Skip:** routine work · already-committed irreversible decisions (run a
postmortem instead).

## Protocol

### 0. Subject — before anything else

Scan first — conversation, `CLAUDE.md`, README, `/docs/`, `/memory/`, attached
files. No questions until scanned. Build the brief:

- **Launching** — one sentence. · **Success** — 2–4 measurable outcomes. ·
  **Dependencies** — technical, organizational, external. · **Constraints** —
  what any scenario must respect.

Confirm with the user in one short block. Corrections → apply. "Just deliver" →
proceed unconfirmed. A field unfillable after one question → halt.

> Bad subject: *my product · the thing.* Good: *the morphy v0.1 launch · the
> migration to React 19 · the Q2 pricing change to $99/seat.*

### 1. Depth — default `standard`

Lightest depth that still gives honest signal. Output density follows depth;
more is one ask away (Step 8).

| Depth | Use when | Research | Output |
|---|---|---|---|
| `quick look` | fast pressure before committing | supplied context only; unchecked claims stay `assm` | Top Risks + top 3 scenarios |
| `standard` | normal pre-launch / pre-commitment | supplied artifacts + obvious precedents | Top Risks + all 5 + Cluster + Do Next |
| `verdict` | high-stakes; must be defensible | full research; sourced neighbor rows | full report, rendered to disk |

### 2. Posture — slightly critical, fair

The discipline is in the evidence, not the voice. Floor (constant):

- Every scenario traces to something real in the subject — a dependency,
  constraint, or success outcome. Unsourced → cut.
- No generic dismissals ("market won't care", "competitors will copy").
- No hedges in scenarios or rationales — strike *might, could, seems, perhaps,
  maybe*. State it or cut it.
- `assumed` evidence stays tagged `assm` everywhere; confident tone on `assm`
  without a verification step → reject the scenario.
- Critique the plan, decision, artifact — never persons, teams, orgs.
- No default-doom, no default-optimism. Qualified opinion, current evidence.

### 3. Generate 8–12, cut to 5

Generate 8–12 specific, mechanistic failure scenarios under the frame. Then cut
to the top 5. Criticality = impact severity × confidence in mechanism. The cut
is forced — more than 5 feeling critical means the criteria isn't being applied
honestly; re-rank.

> Bad: *market conditions worsened.* Good: *the primary integration partner
> deprecated their v2 API with 60 days' notice, and there was no abstraction
> layer or fallback in place.*

### 4. Research — depth-gated, per surviving scenario

- **Mechanism** — has this failure shape happened to comparable launches? Cite
  real cases. **Dependency** — are the depended-on technologies, partners,
  assumptions currently stable? Cite current state. **Precedent** — base rate
  for this failure in this domain; unknown → `assm`.

**Neighbors.** A neighbor = a real, named precedent (a launch that failed this
way, a documented case). Resemblance triggers inspection — never a verdict by
itself. A comparison is REQUIRED when a scenario's rank depends on the
precedent, or depth is `verdict`. Then emit:

```
Neighbor: <name> — they failed because X; this launch risks Y.
  same: <point> [src] · <point> [src]
  diff: <point> [src] · <point> [src]
  net:  same-pattern | analog | distant | not-applicable → <implication>
```

≥2 sourced points per side (URL or `inspected: <artifact>`) or drop the
precedent claim — the scenario's evidence stays `assm`.

### 5. Class — output classes are `real` and `disregarded`

| Class | Claim on attention |
|---|---|
| `real` | Evidence + named mechanism. Requires `exec` or `insp` evidence. |
| `disregarded` | Real risk the maker has been avoiding naming. Honest discomfort, not motivated dismissal. |

`imagined` is a triage state, never printed: a scenario that sounds like risk
because it matches a familiar pattern but lacks evidence here. Research either
converts it to `real` or it is cut from the 5. A printed `imagined` does not
exist.

`disregarded` requires the maker to confirm or correct. Structural disagreement
→ reclassify. Motivated disagreement (slows you / hurts to acknowledge) → keep,
promote rank.

### 6. The scenario contract — who / what / why / do

Every scenario is EXACTLY these four lines under a ranked heading. Print them; a
scenario missing a line does not exist.

```
### [<rank>] <scenario summary> — <real|disregarded> @ <T0–T3>
who:  owner of the do — the decision authority. Named person/role from context;
      unknown → the role that owns the traced dependency (code, infra, vendor
      contract, pricing, docs).
what: the failure — the observable trigger + the causal chain, traced to a
      named dependency, constraint, or success outcome. 1–2 sentences.
why:  which success outcome dies + evidence tag [exec|insp|assm] + the rank
      bracket: why not one higher, why not one lower. 1–2 sentences.
do:   the pre-agreed action + the observable condition that fires it — written
      now, no judgment calls at the moment of firing — with cost
      [cheap|medium|expensive]. Evidence assm + high impact → the do IS the
      verification step. disregarded → the do opens with the naming:
      "avoided X because Y; naming it."
```

Reversibility tier in the heading: `T0` trivially reversible · `T1` reversible
with cost · `T2` mostly irreversible · `T3` fully irreversible.

Evidence tags: `exec` — observed in real comparable cases · `insp` — looked,
not stress-tested · `assm` — imagined, unverified (checkable-but-unchecked
stays `assm`).

### 7. Rank 1–5 (1 = most critical), then synthesize

Caps (non-overridable): `real` without `exec`/`insp` evidence → reclass or cut ·
high-impact `assm` → rank by impact, do = verify · shared root → rank the
cluster, not the average · a `T2`/`T3` scenario whose do is insufficient given
the irreversibility → "revisit the commitment" stated in Do Next, not softened.

Synthesis — printed after the scenarios:

- **Top Risks** — Most Critical · Biggest Cluster (the single trigger — vendor
  failure, regulatory change, key-person loss, funding shift — activating 2+
  scenarios; name it) · Most Avoided (highest-ranked `disregarded`). Coincide →
  say so; diverge → the divergence is signal.
- **Cluster** — pairs sharing a root cause or a single trigger activating 2+.
  The cluster's do dominates its members'.
- **Anti-confirmation** — the scenario most tempting to dismiss. Motivated
  dismissal → promote rank, often reclass `disregarded`; structural → leave.
- **Do Next** — act now (rank 1–2, cheap/medium) · verify (high-impact `assm`)
  · watch (remaining scenarios' triggers) — every line carries its who ·
  commitment check: each `T2`/`T3` either "mitigation sufficient" or "revisit
  the commitment".

### 8. Output

- Inline report is the default deliverable: masthead (brief · frame · depth ·
  class counts · T2/T3 count · date) → Top Risks → scenarios ranked 1→5 in the
  four-line contract → Cluster → Anti-confirmation → Do Next. Template:
  `references/REPORT.md`.
- Disk render at `verdict` depth or when the user asks — **HTML by default**
  (`agents/reports/lookback/<UTC-timestamp>.html`); `.md` (same basename) only
  when the user asks for it — both contracts in REPORT.md. Cannot write a
  required render → emit inline and say why. Never silently skip a required
  render.
- **More on ask:** `expand scenario N` → full anatomy per REPORT.md's expansion
  schema (full mechanism chain, research basis, neighbor rows, full rollback
  spec, early-signal detail). The report stays lean because depth is one ask
  away.

### 9. Conformance — refuse to emit if any fails

- [ ] Subject confirmed; frame declared in the masthead; depth stated.
- [ ] Every scenario = who/what/why/do, none empty, printed under a ranked heading with class + tier.
- [ ] No `imagined` printed — converted to `real` or cut.
- [ ] Every `why` carries an evidence tag AND a rank bracket; every `real` backed by `exec`/`insp`.
- [ ] Every `do` names its firing condition; high-impact `assm` → do is a verification step; `disregarded` → do opens with the naming.
- [ ] Precedent-dependent scenarios carry the sourced neighbor block.
- [ ] Do Next lines each carry a who; every `T2`/`T3` gets the commitment check; no person/team/org attacked.

## Operating principles

The frame is the engine. Five is the cut — forced prioritization prevents
list-bloat theater. Evidence outranks tone. Imagined is a starting state, never
a destination. Disregarded is honest discomfort — name it. An action without an
owner is a wish; a rollback without a trigger is a hope. Reversibility weights
urgency. Resemblance is not exposure. Harsh on the work, neutral on the people.

## Override

First-principles analysis of *this specific situation* overrides any rule —
note the deviation. Load-bearing, never skip: subject + frame · the forced cut
to 5 · class caps · the four-line contract · conformance.

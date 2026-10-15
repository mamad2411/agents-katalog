---
name: keeper
description: Architecture and implementation keep-or-correct decisions. Evaluates elements of a system, design, or codebase across two axes (soundness · optimality) and issues one of four verdicts per element — `keep`, `fix`, `pivot`, `drop` — delivered as who/what/why/do, owner first, every verdict conditional on stated constraints and carrying a re-evaluation trigger. Evidence-grounded architectural judgment.
license: MIT
metadata: { version: 2.0.0, category: decision-discipline }
---

## Purpose

Keeper separates strong design from merely working design. For each element it
answers one question:

**Is this the right design or implementation to keep under the current constraints?**

| Verdict | Meaning |
|---|---|
| `keep` | Leave unchanged under stated conditions. Sound and optimal-enough. |
| `fix` | Keep the choice, correct the execution. |
| `pivot` | Replace the choice — another approach fits the constraints better and the gain exceeds switching cost. |
| `drop` | Remove the element — the need is not worth carrying. |

`pivot` replaces the choice; `drop` removes the need. Every verdict is
conditional: it states the constraints it holds under and the trigger that
forces a revisit. An unqualified verdict does not exist.

No intensity scale — verdict harshness is set by evidence, not voice. For
adversarial tone, use ripper.

**Use:** architecture review · implementation review above line-level ·
system/product design review · mid-build course correction · pre-scale review.
**Skip:** line-level code critique · recording forward decisions (write an ADR).

## Protocol

### 0. Subject — before anything else

Scan first — conversation, `CLAUDE.md`, README, `/docs/`, `/memory/`, attached
files, the repo if provided. No questions until scanned. Build the brief:

- **Under review** — one sentence. · **Scope** — single element · subsystem ·
  whole. · **Why now** — the trigger. · **Constraints** — what binds any verdict.

Confirm with the user in one short block. Corrections → apply. "Just deliver" →
proceed unconfirmed. A field unfillable after one question → halt.

> Bad subject: *the app · the codebase.* Good: *the auth layer's session-token
> approach · the build pipeline's Docker-first stance.*

### 1. Depth — default `standard`

Lightest depth that still gives honest signal. Output density follows depth;
more is one ask away (Step 8).

| Depth | Use when | Research | Output |
|---|---|---|---|
| `quick call` | one named element, fast judgment | supplied context + the artifact itself; unchecked claims stay `assm` | Top Calls + that verdict |
| `standard` | subsystem or design review | inspect the artifacts + obvious neighbors | Top Calls + all verdicts + cascades + Do Next |
| `verdict` | high-stakes / pre-scale; must be defensible | full research; sourced neighbor rows; freshness checked | full report |

### 2. Elements

User named them → evaluate those. Subsystem/whole → pick the 3–7
highest-stakes: stakes = blast radius · reversibility cost · dependent count ·
constraint sensitivity · complexity carried. Present the list; user confirms,
trims, adds, or says "just deliver".

Per element capture: name · what it does (one sentence) · what it commits to ·
dependents.

### 3. Posture — the floor

- Every verdict traces to a real source — inspected artifact, executed
  behavior, provided constraint, researched source. Unsupported → cut.
- No generic dismissals ("old", "not modern", "everyone uses X now").
- No default-keep, no default-change. Qualified opinion, available evidence.
- Incomplete evidence is not a verdict — emit `evidence-needed` with what to
  gather; never soften a verdict as a substitute.
- Critique the artifact, decision, choice — never persons, teams, orgs.
- Reject: verdict without element + evidence + condition · verdict tracing
  only to surface detail · confident tone on `assm` with no verification step.

### 4. Lenses — apply the load-bearing ones, never score all mechanically

Constraint fit · cohesion (one job?) · coupling · reversibility · complexity
budget (earned?) · failure behavior (visible, containable, recoverable?) ·
boundary clarity · operational fit (buildable, testable, observable by the
people responsible?) · marginal value.

### 5. Evidence

Tags: `exec` — observed in real use · `insp` — artifact opened and read THIS
run, not "it exists" · `prov` — explicit user constraint · `rsch` — external
source, current practice, named alternative · `assm` — plausible, unverified.

- External research required when the verdict depends on something outside the
  artifact (standards, ecosystem, security, platform, named alternatives).
  Artifact-local evidence sufficient when it depends on the element itself
  (boundaries, cohesion, dependents, constraint fit).
- **Freshness — 12 months.** `rsch` backing a verdict must be dated ≤12 months
  (publication/revision date, not access date). Older → `rsch: stale`, needs
  fresh corroboration. Time-invariant fundamentals → `rsch: foundational`,
  state why. Undated → stale.
- Sources disagree → surface the disagreement, reason from it. Never collapse
  to one view.

### 6. Neighbors — required for optimality-driven `pivot`, or when cited

A neighbor = a real, named alternative overlapping on purpose, structure,
interface, or constraint set. Resemblance triggers inspection — never a verdict
by itself. When used, emit:

```
Neighbor: <name> — they solve X by doing Y; this element does Z.
  same: <point> [src] · <point> [src]
  diff: <point> [src] · <point> [src]
  net:  equivalent | better-suited | worse-suited | not-comparable → <implication>
```

≥2 sourced points per side (URL or `inspected: <artifact>`) or drop the
neighbor claim. Verdict reasoning cites the net.

### 7. The verdict contract — who / what / why / do

Every verdict is EXACTLY these four lines under a verdict heading. Print them;
a verdict missing a line does not exist.

```
### [KEEP|FIX|PIVOT|DROP] <element> — <soundness|optimality|both> @ <cheap|medium|expensive>
who:  owner of the do. Named person/role from context; unknown → the role that
      owns the element (service, pipeline, schema, dependency, spec).
      keep → who watches the re-evaluation trigger.
what: the element — what it commits to + the structural property found, traced
      to its source. 1–2 sentences.
why:  the verdict bracket — why this and not the adjacent verdict (why not
      keep, why not pivot) + the conditions it holds under + evidence tag
      [exec|insp|prov|rsch|assm]. 1–2 sentences.
do:   fix/pivot → the specific correction or replacement; pivot adds switching
      cost vs marginal gain in one line. drop → removal step + dependents
      (none | handled | scheduled). keep → "hold under <conditions>;
      re-evaluate when <trigger>". Every changing verdict also names its
      re-evaluation trigger.
```

Caps (non-overridable, the only list):

- `assm`-only → `evidence-needed`, never graded.
- `pivot` requires `insp`, `exec`, or `rsch` evidence.
- Optimality-driven `pivot` without switching-cost-vs-gain weighed → downgrade
  to `keep, suboptimal-but-not-worth-switching`.
- `drop` with unhandled dependents → downgrade to `fix` or surface as
  cascade-blocked.
- `rsch` stale without fresh corroboration and not foundational →
  `evidence-needed`.
- Neighbor cited without the sourced block → drop the neighbor claim.

### 8. Cross-element pass, then synthesize

- **Coherence** — `keep` on A while `pivot`/`drop` on B that A depends on →
  surface the conflict. **Cascade** — any verdict forcing re-evaluation of
  another; mark the chain.
- **Anti-confirmation** — the verdict the maker will most dislike. Motivated
  discomfort (slows work, hurts pride) → verdict stands if evidence holds;
  structural discomfort (real counter-reason) → reconsider.

Synthesis — printed after the verdicts:

- **Top Calls** — first 3 verdicts to act on, urgency order (`drop` → `pivot` →
  `fix` → `keep`), one line each: element · verdict · axis · why · cost.
- **Cascades** — trigger verdict → invalidated verdict → resolution.
- **Do Next** — change now (drop/pivot/fix, cheap/medium first) · gather
  (`evidence-needed` items + what to collect) · watch (each keep's trigger) —
  every line carries its who.

### 9. Output

- Inline report: masthead (brief · depth · verdict counts · evidence-needed
  count · date) → Top Calls → verdicts sorted drop→pivot→fix→keep in the
  four-line contract → Cascades → Do Next. Template: `references/REPORT.md`.
- **Disk render — HTML by default.** Every run writes
  `agents/reports/keeper/<UTC-timestamp>.html` per REPORT.md's HTML contract;
  `.md` (same basename) when the user asks. Cannot write files → emit inline
  and say why. Never silently skip the render.
- **More on ask:** `expand element N` → full anatomy per REPORT.md's expansion
  schema (full basis with dated sources, condition boundaries, switching-cost
  math, neighbor rows, lens notes). The report stays lean because depth is one
  ask away.

### 10. Conformance — refuse to emit if any fails

- [ ] Subject confirmed; elements named/confirmed or "just deliver"; depth stated in masthead.
- [ ] Every verdict = who/what/why/do, none empty, printed under a verdict heading with axis + cost.
- [ ] Every `why` carries an evidence tag, the conditions, and the verdict bracket.
- [ ] Every verdict carries a re-evaluation trigger (in `do`); `keep` names who watches it.
- [ ] Caps applied: `assm`-only → evidence-needed · unweighed optimality-pivot downgraded · drop-dependents accounted · stale research not graded.
- [ ] Neighbor-dependent verdicts carry the sourced block; cascades surfaced when present.
- [ ] HTML rendered (or "disk rendering unavailable: <reason>" stated inline); no person/team/org attacked.

## Operating principles

Strong design beats merely working design. Conditions are part of the verdict —
a `keep` is *kept under X, revisited when Y*, never permanent. An action
without an owner is a wish; a trigger without a watcher never fires. Better in
principle is not a verdict — optimality pivots weigh switching cost. Evidence
outranks tone. Resemblance is not equivalence. Insufficient evidence is not a
verdict — name what to gather. Harsh on the work, neutral on the people.

## Override

First-principles analysis of *this specific situation* overrides any rule —
note the deviation. Load-bearing, never skip: subject brief · element stakes ·
evidence tags + caps · the four-line contract · conformance.

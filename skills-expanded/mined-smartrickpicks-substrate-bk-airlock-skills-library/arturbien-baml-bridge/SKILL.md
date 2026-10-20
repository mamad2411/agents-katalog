---
name: arturbien-baml-bridge
description: How Artur Bień (whopio/frosted-ui design-system author) would write our BoundaryML (BAML) code. Bridges three substrates — Whop frosted-ui design system × BAML structured-AI DSL × MemeCore landing-effects primitives — into a single rendering doctrine. The BAML `class` IS the truth-config schema (Yang); the BAML `prompt` IS the AI generation (Yin); Artur's View Transitions discipline IS the morph between states. Yin Yang Coder pattern realized at the type-system level.
tier: POWERFUL
category: Product Team
domain: Frontend Architecture / LLM-Schema-Contracts / Design-System-Composition
peers:
  - memecore-landing-effects (the visual primitive library)
  - landing-page-generator (the consumer)
upstream:
  - https://github.com/whopio/frosted-ui (Whop design system, Artur's commits)
  - https://boundaryml.com/ (BAML — Boundary ML, structured-AI DSL)
  - https://expensive.toys/ (Artur's effect blog)
register: memecore (forensic-investigation, reportorial)
---

# Artur Bień × BAML — the bridge

This skill encodes **how Artur Bień would write our BAML code** if he were the lead engineer on Constellation / Maverick / Brain Brigade. Not a style guide — a discipline. Three substrates fused:

- **Whop frosted-ui** (Artur's actual production design system at github.com/whopio/frosted-ui — TypeScript-first, View-Transitions-aware, image-decode-disciplined)
- **BAML** (boundaryml.com — structured-AI DSL where `class` defines schema and `function` wraps the LLM call with that schema enforced)
- **MemeCore landing-effects** (the 9-primitive bundle — heat-map, ambilight, RGB anaglyph, blur vignette, fancy reveal, etc.)

## The thesis (Artur's mind, distilled)

From his frosted-ui commits and his expensive.toys blog, three obsessions repeat:

1. **Wait for the decode.** Don't morph into a snapshot of an empty image. Cached resolves instantly; uncached waits up to 200ms; never paint half-cooked. (Source: lightbox View Transition commits.)
2. **Snapshots, not states.** UI transitions are about the morph between the *capture* of the old snapshot and the *capture* of the new one — not the data underneath. The viewer perceives the diff, not the truth.
3. **The CSS+SVG-filter primitive is the unit.** Heat map, ambilight, blur vignette — each is one self-contained effect, citable, attributable, single-purpose. Not a framework. A library of *operations*.

These map onto BAML perfectly:

| Artur's discipline | BAML primitive | Yin/Yang role |
|---|---|---|
| Wait for the decode | `class` validation (don't render until output type-checks) | **Yang** — deterministic gate |
| Snapshots, not states | BAML output object IS the snapshot (immutable, versioned) | **Yang** — pinned bundle |
| One effect = one operation | One BAML `function` = one structured AI call = one Smart Touch Point | **Yin → Yang** fusion |

## The BAML schema → frosted-ui component mapping

Every BAML output `class` binds to a frosted-ui rendering primitive. Type-system-enforced design system. Sketch:

```baml
// === BAML side (Yang — deterministic schema, pinned in truth-config bundle) ===

class Archetype {
  type "Driver" | "Interpreter" | "Enforcer"
  autonomy_level int @description("L1-L4 sliding scale")
  info_density "low" | "medium" | "high"
  gravity_coefficient float
  smart_touch_signature TouchSignature
}

class TouchSignature {
  pressure float
  dwell_ms int
  hesitation_count int
  // ↑ feeds CI-score accumulator
}

class DriftReport {
  delta float           @description("how far the AI output drifted from schema")
  ci_balance float      @description("BCODE counterbalance — sign indicates tip direction")
  gate_decision "pass" | "refuse" | "ask"
}

// === BAML function (Yin — probabilistic generation, Yang-bounded by class) ===

function DetectArchetype(touchpoints: TouchSignature[]) -> Archetype {
  client Claude4_7
  prompt #"
    Touchpoint sequence (ordered, with pressure / dwell / hesitation):
    {{ touchpoints }}

    Detect the user's PI archetype using A/B/C → Enforcer/Interpreter/Driver mapping.
    Tie-breaker: default to Interpreter (L2).
    Glass Box: be ready to explain your reasoning if asked.

    Return as Archetype.
  "#
}
```

```tsx
// === frosted-ui side (Artur's render — morphs between BAML-class snapshots) ===

import { Card, Surface } from '@whop/frosted-ui'
import { useViewTransition } from '@whop/frosted-ui/transitions'
import { BlurVignette, Ambilight, HeatMap } from 'memecore-landing-effects'

function ArchetypeRender({ archetype }: { archetype: Archetype }) {
  // Artur's discipline: wait for the decode before morphing
  const { ready, transition } = useViewTransition({ awaitDecode: true })

  // BAML class shape determines rendering primitive
  const Effect = matchEffect(archetype.type, {
    Driver:      BlurVignette,    // low-density, focal-point hero
    Interpreter: Ambilight,       // side-by-side comparison glow
    Enforcer:    HeatMap,         // high-density surveillance grid
  })

  return (
    <Surface
      onTransition={transition}
      autonomyLevel={archetype.autonomy_level}
      gravityCoefficient={archetype.gravity_coefficient}
    >
      <Effect>
        <Card density={archetype.info_density}>
          {/* MemeCore register copy — forensic, third-person, sourced */}
        </Card>
      </Effect>
    </Surface>
  )
}
```

Read it once: BAML class defines what the AI must produce. The frosted-ui render switches on the class's discriminant (`archetype.type`) to select the MemeCore visual primitive. The View Transition waits for the new snapshot's decode before morphing. This is Artur on every line — even though we wrote it.

## The discipline in 6 rules

1. **One BAML `class` per Smart Touch Point output type.** Don't union unrelated outputs. Each touchpoint emits one well-typed snapshot.
2. **Every BAML `function` cites the truth-config bundle version it satisfies.** The class is the schema; the schema is in the bundle; the function comment names the bundle hash. Auditable.
3. **Render switches on discriminants, never on string-matched fields.** TypeScript narrowing forces every archetype variant to be handled or the build fails. (Yang.)
4. **`useViewTransition({ awaitDecode: true })` is the default.** Never animate into an undecoded snapshot. Half-painted morphs are Artur-hostile.
5. **Every visual primitive imports from memecore-landing-effects with the source comment header retained.** Attribution flows from BAML schema → frosted-ui component → effect import → footer credit. The chain is auditable end-to-end.
6. **MemeCore register copy lives in BAML prompt strings, NOT in TSX.** When the register changes (memecore → corporate-deck → playboy), only the BAML prompts change. Frontend stays register-agnostic; design system stays MemeCore-by-default.

## Why this matters operationally

- **The Yin-Yang Coder primitive becomes a type-system primitive.** Yin (BAML prompt) and Yang (BAML class) both ship in one `.baml` file. The OttoMatic Loop iterates over BAML function calls; each return is a snapshot the frontend morphs into.
- **Artur's discipline becomes language-enforced**, not convention. BAML compilers refuse to ship a class without a schema; frosted-ui refuses to ship a transition without `awaitDecode`; the bundle refuses to pin without a signed manifest. Design discipline → type discipline → patent discipline. One stack.
- **The 9 MemeCore effects become BAML output renderers.** Each effect has a "natural" BAML class shape it renders best (heat-map → cohort/array; blur vignette → singleton focal object; RGB anaglyph → drift-state with delta field; etc.). The skill creator pairs them automatically.

## Open questions

- Which BAML version is canonical for the substrate? (Confirm at boundaryml.com release notes — pin a specific version in the truth-config bundle's manifest.)
- Is frosted-ui MIT-licensed for our use? Whop's design system is open-source by name, but commercial-use terms matter. Audit before shipping.
- Whether to vendor frosted-ui or peer-dep it. Vendor = Artur's-mind frozen; peer-dep = stays current with Artur's commits but version-drift risk.
- ASCII Canvas effect (#9 in memecore bundle) has no Artur precedent — does it ship in frosted-ui's lineage or as a custom Maverick primitive?

## Discipline

- **Don't paraphrase Artur's commit messages or code.** Cite. Link. Quote with attribution. His PR #564 ("lightbox item decode") is a real artifact; reference it specifically, don't generalize his views.
- **BAML ↔ TS ↔ frosted-ui binding is one-direction.** Schema flows down; rendering flows up. Never let TS state mutations leak back into BAML class definitions.
- **The `awaitDecode` rule is non-negotiable.** Half-painted morphs are the visual equivalent of probabilistic-AI-without-truth-config — speed without verification. Refuse the shortcut.

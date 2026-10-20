---
name: asset
description: Token-driven visual-asset producer (icons/banners/logos/data-viz/slides) on DESIGN.md tokens + the aesthetic gate. Use to generate a visual asset when a design system exists. Not for non-visual.
---

# asset

The visual-asset producer over the theme system. v6 had five separate `gateway-*` asset skills
(icon/banner/brand-assets/dataviz/presentation); v7 collapses them into **one token-driven producer**
that routes by asset type — the same systems-not-skills move that made `autopilot` thin. Every asset it
emits **references the design tokens** (no raw hex/px) and conforms to the project's `DESIGN.md`, so it
passes the `aesthetic` gate by construction rather than being audited into compliance after the fact.

## What this does / does not do

Does: produce a typed visual asset (icon / banner / brand / dataviz / presentation) from the design
contract — token-referencing, on-style, spec-declared (sizes, safe-zones, formats); write a receipt.
Does **not**: invent the design system (that's `design-brief` → `DESIGN.md` + DTCG tokens), run the
visual verdict (that's the `aesthetic` gate — asset *conforms to* it), produce audio/non-visual media
(separate), or emit raw values (the token policy is the whole point).

## When NOT to use

- The target has no visual surface / no design system — there is nothing to produce against. Run
  `design-brief` first to establish `DESIGN.md` + tokens.
- The user wants the *design contract* (palette/type/voice) — that's `design-brief`, not `asset`.
- The user wants the *audit verdict* on an asset — that's the `aesthetic` gate.
- Audio assets — out of scope (the v6 `gateway-audio` is a separate media-domain capability, deferred).

## Reference Routing

| Situation | Reference |
|---|---|
| Per-asset-type specs (icon styles/sizes, banner safe-zones/dims, brand/logo, chart selection, slide layout) | `references/asset-specs.md` |
| Design KB lookup (style/palette) · token emit · the audit it must pass | `../kb-seed/` · `../dtcg-emit.py` · `../../../gateways/aesthetic.md` |

## Inputs

- The asset request: type (icon|banner|brand|dataviz|presentation) + its parameters.
- The design contract: `DESIGN.md` + the validated DTCG token file (from `design-brief`/`dtcg-emit`).
- The design KB (`kb-system query --room ui-style`/`ui-palette`) for style grounding.

## How to do it

1. **Load the contract.** Read `DESIGN.md` + the DTCG tokens. No contract → run `design-brief` first (do
   not invent a palette here).
2. **Route by type** and apply its spec (`references/asset-specs.md`):
   - **icon** — SVG, one of the declared styles, token-driven stroke/fill (`currentColor` or
     `var(--token)`), consistent stroke width + sizing scale, batch + multi-size export.
   - **banner** — declared format + dimensions; critical content in the central safe zone; one CTA;
     ≤ 2 font families from the type system.
   - **brand** — logo/wordmark in the declared style; clear-space + min-size rules; mono + color variants.
   - **dataviz** — chart type selected by the data shape (not by default); token palette; accessible
     (not color-alone; labeled).
   - **presentation** — slides on the token system; one idea per slide; chart-integrated.
3. **Token policy (hard).** Every visual value references a token (`var(--token)`), never a raw
   `#hex`/`px`. This is what makes the output pass the `aesthetic` gate's token-compliance BLOCK.
4. **Self-check against the aesthetic gate** (`../../../gateways/aesthetic.md`): contrast, named-style
   adherence, no anti-default patterns without rationale. Fix before emit.
5. **Emit + receipt.** Write the asset file(s); record the type, the tokens used, and the gate self-check.

## Output

- The **asset file(s)** (SVG / PNG / HTML deck) at the declared product path — persistence: **Spec-Anchored**
  (versions with the product). Token-referencing; on-contract.
- **receipt** (`<workspace>/receipts/asset-receipt.json`): base schema + `asset_type`, `tokens_referenced`
  (bool — no raw values), `style_source` (DESIGN.md / KB drawer), `aesthetic_self_check`, `outputs`.
  persistence: Spec-Anchored.

## Proactive Triggers

- **No `DESIGN.md`/tokens present**: stop and run `design-brief` — an asset without a contract is a guess
  that will fail the aesthetic gate.
- **A raw hex/px about to be emitted**: convert it to a token (or add the token) — raw values are the
  aesthetic gate's token-policy BLOCK.
- **A chart type chosen by default (always bar)**: pick by the data shape (distribution/relationship/
  trend/part-to-whole), not habit.

## Completion Criteria

**Done when:** the requested asset exists at the product path, every visual value references a token, it
adheres to `DESIGN.md`'s named style, and the aesthetic self-check passes; an asset receipt records the
type + token compliance.

**Not done if:** any raw `#hex`/`px` was emitted; the asset ignores the design contract; a chart type was
chosen by default; it was produced with no `DESIGN.md` to conform to.

**Next step:** the `aesthetic` gate audits the asset in context; executor integrates it into the build.

## Related Skills

- **design-brief**: writes the contract (`DESIGN.md` + tokens) `asset` produces against. Run it first.
- **aesthetic gate**: audits the produced asset. `asset` conforms by construction; the gate enforces.
- **theme system** (`kb-system`, `dtcg-emit`): the design KB + token emitter `asset` reads.

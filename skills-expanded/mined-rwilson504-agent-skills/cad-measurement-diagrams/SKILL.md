---
name: cad-measurement-diagrams
description: 'Generate self-guided SVG instruction diagrams whenever you ask a human to take a physical measurement (caliper placement, thread pitch spans, datum choice, across-flats vs across-corners). USE FOR: "how do I measure this", "show me where to put the calipers", asking a user for dimensions, reverse-engineering a physical part, thread pitch measurement, any bench procedure you are describing in words.'
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["svg","measurement","calipers","reverse-engineering","documentation"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/cad", "emoji": "📐" } }
---

# CAD Measurement Diagrams

> **Prerequisite:** none. This skill is standalone and is loaded by any
> agent that asks a human to go measure something.

## Purpose

When you ask a user for a physical measurement, **words are not enough**.
"Span 20 pitches" reads as unambiguous to you and produces three different
caliper placements in practice. This skill produces a **self-guided SVG
diagram** — a picture the user can follow at the bench without re-reading
the chat — and defines when generating one is mandatory.

Outputs land in the project's `reference/` folder as
`howto-<what>.svg` (plus a `.png` sibling for phone viewing at the bench).

## The rule

**Any time you ask a human to perform a physical measurement or a manual
procedure whose outcome depends on *where* or *how* they place a tool,
generate a diagram in the same response.** Do not ask first; just draw it.

Trigger examples:

| You are about to write… | Draw a diagram |
|---|---|
| "measure across 20 thread crests" | ✅ off-by-one crest/gap trap |
| "caliper the plain shank next to the thread" | ✅ which shank, which axis |
| "measure the bore depth" | ✅ from which datum face |
| "measure the hex across flats" | ✅ flats vs corners |
| "measure the wall thickness" | ✅ where — walls are rarely uniform |
| "how long is the part overall?" | ❌ genuinely unambiguous, skip |
| "what colour is it?" | ❌ not a measurement |

The test: *could a reasonable person place the tool somewhere other than
where I mean?* If yes, draw it.

## Anatomy of a good measurement diagram

A diagram that works unsupervised has all five of these. Missing any one
sends the user back to the chat to ask a question.

1. **The part in profile**, drawn recognisably — not an abstract box.
2. **The tool**, shown in contact, with its *measuring faces* emphasised.
   Users align on the tool's faces, not on your arrows.
3. **The dimension line** with arrowheads at both ends, and the quantity
   it represents stated in words next to it.
4. **The trap**, called out explicitly. Every measurement has one
   dominant failure mode — name it and show the wrong version.
5. **The arithmetic**, printed on the image. `pitch = reading ÷ 20`.
   The user should not have to remember what to do with the number.

Add a **predicted value** when you have one ("expected ≈ 24.0 mm"). It
lets the user catch a gross error immediately, and it makes your
hypothesis falsifiable rather than something you quietly retrofit later.

## SVG scaffold

Light background — these get printed and viewed in bright garages, not
in a dark IDE.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 740"
     width="1000" height="740"
     font-family="Segoe UI, Arial, Helvetica, sans-serif">
  <defs>
    <!-- auto-start-reverse gives a double-headed dimension line from ONE marker -->
    <marker id="dim" markerWidth="9" markerHeight="9" refX="9" refY="4.5"
            orient="auto-start-reverse">
      <path d="M0,0 L9,4.5 L0,9 Z" fill="#c0392b"/>
    </marker>
  </defs>
  <rect width="1000" height="740" fill="#ffffff"/>
  <!-- ... -->
  <line x1="140" y1="378" x2="740" y2="378" stroke="#c0392b" stroke-width="2"
        marker-start="url(#dim)" marker-end="url(#dim)"/>
</svg>
```

### Palette

| Role | Colour |
|------|--------|
| Part body / metal | `#c9c9c9` fill, `#4a4a4a` stroke |
| Tool (calipers, jaws) | `#5b83bd` fill, `#2f4d7a` stroke |
| Measuring face (emphasis) | `#16233a`, stroke-width 5 |
| Dimension lines + the trap | `#c0392b` |
| Correct / confirmed | `#2e7d32` |
| Warning panel | `#fff8f0` fill, `#e0a96d` stroke |

### Thread / serration profile helper

Hand-computing a 49-point zigzag is where these diagrams get wrong.
Generate the points:

```python
def zigzag(x0, n, pitch, y_valley, y_peak):
    """Points for a triangular thread profile; peaks land exactly on x0 + k*pitch."""
    pts = [(x0 - pitch / 2, y_valley)]
    for k in range(n + 1):
        x = x0 + k * pitch
        pts += [(x, y_peak), (x + pitch / 2, y_valley)]
    return " ".join(f"{x:g},{y:g}" for x, y in pts)
```

Mirror the same x-values with swapped y to get the opposite flank.

## MANDATORY: rasterize and look at it

**Never ship an SVG you have not rendered and viewed.** Coordinate
arithmetic errors (overlapping labels, arrows pointing at the wrong
crest, text running off-canvas) are invisible in source and obvious in
the rendered image — and a wrong diagram is worse than no diagram,
because the user will trust it.

Windows, no Python imaging deps required:

```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" `
  --headless=new --disable-gpu --force-device-scale-factor=1 `
  --window-size=1000,740 --screenshot="out.png" "file:///D:/path/to/diagram.svg"
```

Then view `out.png` and **count the features you annotated** — if the
diagram claims 20 gaps, count 20 gaps.

Gotchas found the hard way:

| Symptom | Cause | Fix |
|---|---|---|
| `--screenshot` produces no file | Old `--headless` mode on Edge | Use Chrome with `--headless=new` |
| `import cairosvg` fails | Not installed; needs native cairo on Windows | Don't fight it — use the browser |
| Single-headed dimension line | `orient="auto"` on `marker-start` | Use `orient="auto-start-reverse"` |
| Blurry raster | HiDPI scaling | `--force-device-scale-factor=1` |

Keep the PNG next to the SVG — the SVG is for the repo, the PNG is for
the phone at the bench.

## Known measurement traps worth a diagram

| Measurement | The trap | What the diagram must show |
|---|---|---|
| Thread pitch over N pitches | Counting **crests** instead of **gaps** — N crests is N−1 pitches | Numbered crests, numbered gaps, jaws on crest 1 and crest N+1 |
| Thread major Ø | Jaws seating in a valley instead of on crests | Flat jaw faces bridging two crests |
| Thread minor Ø | Jaw tips can't reach the root | Offer the plain-shank proxy instead |
| Hex / nut size | Across flats vs across corners (ratio 1.155) | Both, with the wrong one struck through |
| Bore depth | Datum ambiguity — from the rim or from a shoulder? | The datum face highlighted |
| Wall thickness | Walls are rarely uniform | The exact station to measure at |
| Hole spacing | Centre-to-centre vs edge-to-edge | Both, with centrelines drawn |
| Sheet / shim thickness | Caliper jaws compress soft material | "Do not squeeze" callout |

## Quick reference

| Symptom | Likely cause | Fix |
|---|---|---|
| User returns a number that disagrees with your estimate by ~5–11% | Off-by-one on a repeated feature count | Re-ask with a diagram; span twice as many features |
| Two readings of the same thing differ | Tool seating, not part variation | Diagram the seating; average and widen your error bar |
| User asks a clarifying question about your instruction | The instruction needed a diagram | Draw it now, and note the trap in this skill's table |
| Error that compounds along the part (pitch, spacing) | Measured over too short a span | Double the span; absolute error stays, relative error halves |

## See Also

- `cad-reverse-engineer-stl` — measuring a *digital* mesh; this skill
  covers measuring the *physical* original.
- `electronics-circuit-schematics` *(separate plugin)* — the same
  hand-authored SVG approach applied to circuit symbols.

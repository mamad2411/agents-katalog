---
name: sifr
description: Read and analyze saved SiFR capture files (sifr-v2 / sifr-v3 JSON with ====METADATA==== / ====SUMMARY==== / ====NODES==== markers) - sections, compact node IDs, salience tiers, presets, structural patterns and ready jq recipes. Use when a SiFR JSON file is on disk or pasted into the conversation. Not for live browser work - that is the e2llm skill.
license: MIT
---

# Read a saved SiFR capture

SiFR (Single-File RAG, "see-far") is a structured snapshot of a web page: DOM structure,
interactive elements, styles, spatial layout and relationships, in a form built for a
language model to read. A saved capture is **one JSON object** keyed by `====SECTION====`
markers.

This skill is for files. For driving a live browser, that is the **`e2llm`** skill.

## Reading strategy

**Step 1 — read the map.** Always, and it is roughly 10–15% of the file:

```bash
jq '{meta: ."====METADATA====", summary: ."====SUMMARY====", high_nodes: ."====NODES====".high}' capture.json
```

That gives page context, every interactive element, layout clusters, structural patterns
and the tree of important nodes — enough to understand the page and plan what to look at
next.

**Step 2 — drill in on demand.** Read `DETAILS`, `RELATIONS`, or `NODES.med` / `NODES.low`
only when you need a specific element's selector, styles or spatial context. They are large
and most questions do not need them.

Ready-made queries for both steps: `references/jq-recipes.md`.
Question-led examples: `use-cases.md`.

## Sections

| Section | Key | Contains |
|---------|-----|----------|
| METADATA | `."====METADATA===="` | url, viewport, version, stats (node counts, salience distribution, preset), `stateAgeMs` |
| SUMMARY | `."====SUMMARY===="` | interactive elements by category, layout clusters, structural patterns, page styles |
| NODES | `."====NODES===="` | tree: `{high,med,low}.{tag}.{id}` with parent, children, cluster, pattern |
| RELATIONS | `."====RELATIONS===="` | spatial (`above`/`leftOf`/`overlaps`) + ARIA (`labelFor`/`describedBy`/`controls`) |
| DETAILS | `."====DETAILS===="` | per-element: selector, text, attributes, styles, layout, hints |

Block order in the document is METADATA → SUMMARY → NODES → RELATIONS → DETAILS. The
front-loading is deliberate: what matters most comes first, so reading can stop early.

## ID system

- `#foo` — a real DOM ID, usable as a CSS selector directly.
- `btn001`, `a042`, `div003` — compact SiFR-assigned IDs. Look up the real CSS selector in
  `DETAILS[level][tag][id].selector`.

Tag abbreviations: `btn`=button, `spn`=span, `hdr`=header, `ftr`=footer, `sctn`=section,
`artcl`=article, `asd`=aside, `lbl`=label, `slct`=select, `txtarea`=textarea, `tbl`=table,
`vd`=video, `ad`=audio, `cnvs`=canvas. Any other tag — headings, `li`, `nav`, custom
elements — is its own prefix.

`sifr-v3` uses hybrid keys: HIGH-interactive elements keep `#realId` or a selector, while
everything else uses compact IDs. `sifr-v2` is uniformly compact. Check the version in
METADATA before assuming either shape.

## Salience levels

| Level | Meaning | Budget behaviour |
|-------|---------|------------------|
| **high** | Interactive, important (buttons, inputs, headings, ARIA-annotated) | Never dropped |
| **med** | Supporting structure (containers with IDs, landmarks) | Dropped under budget pressure |
| **low** | Scaffolding (wrappers, decorative elements) | Dropped first |

When nodes are dropped by budget reduction their **text is preserved in the parent's
`childrenText` field** — content is not lost, only structure. To see what was dropped,
compare the two objects in `jq '."====METADATA====".stats | {salience, inOutput}'`.

## Presets

Check `stats.preset` in METADATA to know what you are holding.

| Preset | What's included | Typical size | Use for |
|--------|----------------|-------------|---------|
| **minimal** | Content + structure only, no styles or layout | 20–150KB | Analysis, content extraction, navigation |
| **visual** | + full CSS styles, no LOW nodes | 100–300KB | Visual analysis, style debugging |
| **normal** | + hints, all nodes | 200–450KB | Full context, automation |
| **unlimited** | Same as normal, no budget cap | Variable | Reference, debugging |

A `minimal` capture that seems to be missing the page's main content is behaving as
designed — it drops LOW nodes, which on many commerce and app pages is where the grid
lives.

## Structural patterns

`pattern: "struct001"` on a node means the page has many siblings with identical DOM
structure — product cards, list items, table rows. Only three exemplars (first, middle,
last) are kept at full detail. The pattern entry in SUMMARY carries:

- `total` — how many instances actually exist
- `fingerprint` — the DOM structure, e.g. `"li:(a:(img:,span:price))"`
- `exemplars` — the three representative elements
- `dropped` — how many were removed for budget

**Do not go looking for the missing instances.** They are intentionally deduplicated, and
`total` already tells you the real count.

## Reading a capture honestly

- `stateAgeMs` is milliseconds since the DOM last changed, not the age of the file. A large
  value means the page was static when captured, not that the capture is stale.
- A capture records one page state at one moment under one set of conditions. It is
  evidence about that moment, not a guarantee about the live page now.
- Absence in a capture is weak evidence of absence on the page: a `selector`-scoped capture
  misses body-level portals, and budget reduction drops LOW nodes. Check `stats.preset` and
  whether the capture was scoped before concluding something was not there.

## Format spec

The canonical format specification —
[SIFR.md](https://github.com/e2llm/e2llm-sifr/blob/main/SIFR.md),
[TAXONOMY.md](https://github.com/e2llm/e2llm-sifr/blob/main/TAXONOMY.md) and real example
captures — lives at [github.com/e2llm/e2llm-sifr](https://github.com/e2llm/e2llm-sifr).

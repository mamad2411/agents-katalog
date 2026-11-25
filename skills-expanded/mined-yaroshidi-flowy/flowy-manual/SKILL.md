---
name: flowy-manual
description: Use when building on Webflow and you need to know what is actually true — a verified-only field manual of directly-observed behaviours, traps, schema quirks and fixes. Covers what changed in MCP 2.0.1, element and style traps, CMS bindings and Collection Lists, components and props, responsive breakpoints, Designer-canvas behaviours, and live diagnostic probes. Use alongside the flowy skill (which hand) and flowy-verify (did it land).
---

# flowy-manual — verified-only field manual (map)

The reference you consult **while** building. This file is a map; everything lives in topical files.

> **The set.** [flowy](../flowy/SKILL.md) decides *which hand*; invoke it first. **flowy-manual**
> (this) tells you *what is actually true*. [flowy-verify](../flowy-verify/SKILL.md) checks *whether
> the write landed*. Hard standing rules are in [flowy/house-rules.md](../flowy/house-rules.md).

## The one rule for this manual

**Verified-only.** Every entry references a directly observed event and the tool or command that
produced it. No hedged language. No untested fixes. No single-observation generalization dressed as a
pattern: if something was seen once, it says so.

**Reversals are struck and dated, never deleted.** A verified-only ledger is only trustworthy if you
can see where it was wrong. When Webflow fixes something, the old row stays with a
`superseded <date>` marker and a pointer to the new finding.

## Start here

| Open this | For |
|---|---|
| **[mcp-2.0.md](mcp-2.0.md)** | ⭐ **What changed in MCP 2.0.1: read this before trusting any older row.** The reversal ledger: what Webflow fixed, what still bites, and the new capability surface |
| [mcp-capabilities.md](mcp-capabilities.md) | The historical capability ledger (May–July 2026). Dense, and **partly superseded**: check [mcp-2.0.md](mcp-2.0.md) first. Kept because the evidence is still the evidence |
| [designer-traps.md](designer-traps.md) | Designer-side behaviour: dropped classes, injected defaults, embed CSS in canvas + the specificity trap, whitespace stripping, script load order, componentized Collection Lists, the Navigator `Enter` route |
| [responsive.md](responsive.md) | Breakpoints, which one to edit on, the never-resize rule and the iframe measuring snippet, `clamp()` limits |
| [diagnostics.md](diagnostics.md) | Live-page and canvas probe snippets that returned useful state |

## The shortest version

Things that will cost you a session if you don't know them:

0. **A query that cannot answer your question still returns `0`, and `0` looks like an answer.**
   The canonical case: `data-w-id` does not exist in the Designer (it is emitted at publish), so an
   attribute query returns 0 on pages that *do* have interactions. Read the **Interactions panel**.
   [mcp-2.0.md](mcp-2.0.md) §13.1. Before trusting an empty result, ask whether that surface could
   ever have held the thing you searched for.
1. **`data_whtml_builder` silently drops classes** that don't already exist as Designer styles. No
   error. The tell is an **absent** `styleNames` field. Still true in 2.0.1.
2. **`all_resolved_settings` reports a working CMS binding as `null`.** Bindings can't resolve at
   design time. Read bindings with `all_raw_settings` only.
3. **Write responses prove nothing.** `set_settings` and `update_style` report success on writes you
   must re-read to confirm.
4. **The `breakpoint_id:"main"` silent no-op is FIXED** in 2.0.1; see [mcp-2.0.md](mcp-2.0.md). Old
   rows saying otherwise are superseded.
5. **`clamp()` / `min()` / `max()` / `dvw` / `dvh` are silently rejected** by `update_style`, and one
   rejected property voids the whole call.
6. **Embed `<style>` renders in the canvas per-embed, not universally**, and embed descendant
   selectors outrank native flat classes **on live while being invisible in the canvas.**
7. **A backgrounded tab reports `innerWidth: 0`** and freezes CSS transitions, so measurements taken
   there are fiction.
8. **Requested type ≠ returned type.** `CMSCollection` → `DynamoWrapper`; `TextBlock` → `Block`;
   `LinkBlock` → `Link`. Don't filter on what you asked for.

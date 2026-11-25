---
name: product-marketing
description: "Create or update the product marketing context document (.agents/product-marketing.md). Use at the start of a project for positioning, audience and ICP before other marketing skills."
metadata:
  version: 2.1.0
---

# Product Marketing Context

Create and maintain `.agents/product-marketing.md`, the shared positioning and messaging context that the other marketing skills read so the user does not repeat themselves.

## 1. Find existing context

Look for `.agents/product-marketing.md`, then `.claude/product-marketing.md`, then legacy `product-marketing-context.md` in either folder. If found outside `.agents/product-marketing.md`, offer to move it to the canonical path.

- **Exists**: read it, summarize what it captures with its **Document version** and the last few **Changelog** entries, ask which sections to update, gather only those.
- **Missing**: offer (a) auto-draft from the repo (README, landing pages, marketing copy, about pages, meta descriptions, package.json, docs), recommended and faster, then ask "What needs correcting? What's missing?"; or (b) a conversational walk-through, one section at a time with a brief explanation, relevant questions, and a confirmation before moving on.

## 2. Gather

Capture these 12 sections: product overview, target audience, personas (B2B with several buyers only), problems and pain points, competitive landscape (direct, secondary, indirect), differentiation, objections and anti-persona, switching dynamics (JTBD four forces: push, pull, habit, anxiety), customer language, brand voice, proof points, goals. Questions per section: [references/sections.md](references/sections.md).

- Push for verbatim customer phrases; exact words beat polished descriptions and make copy resonate.
- Ask specific questions ("What's the #1 frustration that brings them to you?") and ask for examples.
- Skip sections that do not apply (personas for B2C).

## 3. Write the file

Use the structure in [references/template.md](references/template.md). Show the finished document and ask for adjustments before saving.

## 4. Version and save

The doc is read by every other marketing skill, so keep a paper trail.

- **New**: `Document version: v1` and one Changelog entry `v1 (YYYY-MM-DD): Initial context.`
- **Update**: increment the version, set `Last updated` to today (ISO), and prepend a Changelog entry (newest first) naming the sections touched and why, e.g. "v3 (2026-07-16): Repositioned from 'email tool' to 'deliverability platform'; added RevOps to the ICP." Leave past entries as they are.
- **Typo-only fix**: save without a version bump or entry.
- A real repositioning is said plainly, since downstream skills will generate against the new context.

Finish by telling the user other marketing skills now use this context, the Changelog tracks how positioning evolved, and `/product-marketing` updates it anytime.

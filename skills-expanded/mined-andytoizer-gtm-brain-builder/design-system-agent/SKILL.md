---
name: design-system-agent
description: Create a source-backed design-system brief and walk an operator through using Claude.ai/design or Codex design workflows to generate, review, export, and import a brand kit/design system into the GTM Brain.
---

# Design System Agent

Use this when the operator wants help creating a design system, preparing the right prompt/brief for a design tool, or importing design outputs into the GTM Brain.

Owns `brand/design-system-brief.md`, the visual-system parts of `brand/brandkit.md`, and design project notes in `brand/design-resources.md`.

## Inputs

- `company/product-truth.md`
- `company/approved-claims.md`
- `icp/`
- `messaging/`
- `customers/proof-approval.md`
- `brand/brandkit.md`
- `brand/design-resources.md`
- `brand/voice-system.md`
- Existing website, app screenshots, logo files, decks, Figma, Canva, social posts, and public docs
- Operator/accountable-owner taste review

## Outputs

- `brand/design-system-brief.md`
- Updated `brand/brandkit.md`
- Updated `brand/design-resources.md`
- Optional implementation notes for Codex when the design system needs to become code, components, CSS tokens, slides, or website assets

## Walkthrough

1. Read the smallest source-backed context needed for the design decision.
2. Ask the operator what they are trying to make: brand kit, design system, deck style, landing page direction, social templates, component library, or coded UI.
3. Build a design-system brief before generation:
   - audience and category
   - desired perception
   - brand personality and tone boundaries
   - product truths and approved claims
   - proof constraints and do-not-claim rules
   - visual references and anti-references
   - required outputs
   - review checklist
4. If using Claude.ai/design, tell the operator to open `https://claude.ai/design`, create a brand-kit or design-system project, paste the brief, and upload only approved assets.
5. If using Codex to implement or import the design system, convert the approved design brief into implementation instructions: tokens, typography, component rules, asset paths, responsive behavior, accessibility notes, and files to update.
6. Review generated output with Grill-me before treating it as durable taste.
7. Import approved decisions:
   - `brand/brandkit.md`: stable visual rules, tokens, typography, logo usage, layout rules, examples, and do/don't guidance
   - `brand/design-resources.md`: project links, prompts, uploaded inputs, exports, asset locations, and owner review state
   - `brand/voice-system.md`: only the voice implications, not visual rules
   - implementation notes: where Codex should apply tokens/components when building downstream assets

## Design Brief Template

```text
Goal:
Audience:
Category/context:
Desired perception:
Brand personality:
Tone boundaries:
Approved claims:
Proof constraints:
Do not claim:
Existing visual assets:
Visual references:
Anti-references:
Required outputs:
Accessibility constraints:
Review criteria:
Import targets:
```

## Rules

- Do not generate brand direction from vibes alone; ground the brief in the GTM Brain.
- Do not let design tools invent positioning, product capabilities, proof, metrics, customer permissions, or customer logos.
- Separate visual system from speaker voice and buyer language.
- Generated designs are drafts until an accountable owner approves them.
- Store the prompt and export links so future agents can understand where the design system came from.
- Ask one Grill-me question before approving durable taste decisions.

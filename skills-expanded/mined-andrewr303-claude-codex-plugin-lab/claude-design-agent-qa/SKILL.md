---
name: claude-design-agent-qa
description: >-
  QA Claude Design handoffs after implementation. Use when the user provides a
  Claude Design .dc.html file, HTML prototype, handoff bundle, screenshot, image,
  or design export and wants to compare it against a live app, verify 1:1 design
  fidelity, then test functionality, navigation, responsive behavior, accessibility,
  and AI features in a real browser.
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Agent
---

# Claude Design Agent QA

This skill combines Claude Design Handoff discipline with Browser Agent QA Wizard execution. Its job is not only "does it look close?" It must prove that the implemented interface matches the design source and then prove the interface works.

## Contract

- Open the actual design source and the actual app implementation in a real browser.
- Prefer the Claude Design bundle or `.dc.html` source over screenshots for exact values.
- Screenshots/images are holistic evidence, not a replacement for source inspection when source exists.
- Compare design and implementation before functional QA.
- Do not treat prototype code as production code.
- Do not accept hardcoded fixture metrics as real app data.
- After fidelity passes or drift is documented, run functional/navigation/accessibility/responsive/AI QA.

## Source Discovery

For a Claude Design bundle:

1. Read `README.md` first if present.
2. Identify the primary `.dc.html` or `.html` file.
3. Read the primary file in full.
4. Enumerate imported `.tsx`, `.jsx`, `.js`, `.css`, images, uploads, fonts, and icons.
5. Read imports that define visible sections, tokens, fixtures, charts, or interaction behavior.
6. Inventory:
   - section list and order
   - component/primitives list
   - token sources
   - fixture data and expected real-data contracts
   - prototype-only scaffolding to drop

For only an image/screenshot:

- Use the image as a visual acceptance target.
- State that exact tokens and spacing are inferred unless source files are later provided.

## Browser Comparison Setup

Use `scripts/design-side-by-side-capture.mjs` when Playwright is available:

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/design-side-by-side-capture.mjs --design <design-file-or-url> --app <app-url> --out .context/claude-design-agent-qa --viewports 390x844,768x1024,1280x900 --headed
```

The script opens the design and implementation in the same browser context for each viewport, captures screenshots, and writes metrics JSON. If Playwright is unavailable, use `agent-browser` or `browse` to open both targets manually and capture screenshots.

Manual pattern with agent-browser:

```bash
agent-browser open <design-file-or-url>
agent-browser screenshot design.png --full
agent-browser open <app-url>
agent-browser screenshot app.png --full
agent-browser snapshot -i
```

When the design is a local file, use an absolute path or `file:///` URL.

## Fidelity Gate

Return stable drift IDs before editing:

| ID | Section | Design evidence | App evidence | Drift | Severity | Minimal fix | Verification |
|---|---|---|---|---|---|---|---|

Check:

- section count, names, order, and missing sections
- page shell width, gutters, vertical rhythm, and sticky regions
- typography, font loading, rem/px differences
- colors, gradients, alpha values, borders, shadows, radii
- icons, images, uploads, chart geometry, and bespoke visuals
- motion timing and reduced-motion behavior
- mobile/tablet/desktop behavior
- loading, empty, partial, error, permission, and success states
- data integrity: every displayed value is real, typed fixture/dev data, or explicitly placeholder
- no prototype scaffolding leaked: `window.*`, `text/babel`, CDN React, tweak panels, generated edit controls

If high-severity visual drift exists, report it before functional QA. If the user asks to continue anyway, label functional QA as run against a drifted implementation.

## Functional QA After Fidelity

Once fidelity is acceptable or drift is explicitly documented, run Browser Agent QA Wizard checks:

1. Functional happy path.
2. Adversarial flows.
3. Navigation/deep links/back-forward.
4. Keyboard/focus/accessibility.
5. Responsive overflow and touch targets.
6. Console/page/network health.
7. AI feature contracts if the page has generated analysis, chat, recommendations, agents, RAG, or tool calls.

Use markers:

```text
STEP_PASS|<test-id>|<evidence>
STEP_FAIL|<test-id>|<expected> -> <actual>|<screenshot-path>
STEP_SKIP|<test-id>|<reason>
```

## AI and Data Integrity Checks

Claude Design prototypes often include fixture data. For production QA:

- Map each fixture field to a real prop, API response, DB record, or explicit unavailable state.
- Reject fabricated-looking metrics shown as real values.
- Test AI loading, streaming, error, retry, citation/source, and stale states.
- For generated text, verify source grounding or label as unverified.

## Patch Gate

If the user asks to fix drift or behavior:

- Implement only approved drift/test IDs unless they explicitly ask for a broader pass.
- Reuse the target app's styling system and tokens.
- Preserve mobile/desktop parity.
- Verify in browser after changes at the affected widths.

## Final Report

```md
## Claude Design Agent QA Results
Design source: <path/url>
Implementation: <url>

### Fidelity
| ID | Result | Evidence |
|---|---|---|

### Functionality
Tests: N | Passed: N | Failed: N | Skipped: N
| ID | Result | Evidence |
|---|---|---|

### Screenshots
- design/app viewport paths

### Not Verified
- item - reason
```

## References

- `references/anatomy.md`
- `references/fidelity-checklist.md`
- `references/data-integration.md`
- `references/charts-and-motion.md`
- `references/responsive.md`
- `references/claude-design-comparison.md`
- `references/stagehand-browserbase-protocol.md`
- `references/ai-feature-qa.md`

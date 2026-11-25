---
name: sql-apps-design
description: "Use when building or changing SQL Apps screens, or reviewing a generic interface, unclear hierarchy, or responsive layout."
---

# Design for the app

Own the design pass in the app's existing stack. No companion skill is required. Functional acceptance and design acceptance are separate.

Use the confirmed app's `docs/...` for references and outputs.

## Choose a direction

- From the brief, name the audience, recurring task, and first-read information.
- Compare two distinct compositions: hierarchy, density, and action placement, not palettes. Choose the one serving the task. Starter CSS is not design direction.
- Record it in `docs/design-intent.md` per `docs/reference/design-acceptance.md`.

## Make the purpose visible

- Lead with defining information and the recurring action; keep account, setup, and administration secondary. Use typography, spacing, color, and layout to reinforce that hierarchy, not a default dashboard.
- Give each surface one clear primary action; keep secondary and destructive actions distinct. Compose empty, single-record, and populated states intentionally.
- Support readable line lengths, wrapping long content, contrast, visible keyboard focus, semantic structure and accessible labels.
- Show truthful signed-out, authorized, no-access, loading, empty, error, saving, success and disabled states. Keep test-persona selection off product screens; status uses text or iconography, never color alone.

## Review and improve

The first implementation is a candidate, not an approved design:

1. **Checkpoint.** At the intended origin, render one representative primary-task screen at desktop and narrow widths together. Source review and compilation are not visual review.
2. **Critique the render.** What dominates the first viewport? Where does the defining information appear? What could belong unchanged to an unrelated app? What should be removed or demoted? Rank the three highest-impact changes, each naming the visible problem, task consequence and concrete change.
3. **Fix observed problems and re-review.** Batch changes, re-render affected views, critique again. Unresolved findings, not a loop count, drive passes.
4. **Expand** to remaining states once the composition stabilizes.

Hand off task, render/build, ranked defects, changes and preservation/recheck needs. Reuse the browser session; skip backend checks for visual-only edits. Improve the rendered screen, not document count.

Accept only when the primary task and information lead, the composition serves this domain, and no material defects remain; record tradeoffs. Record critique, matrix and `Design quality` verdict in `docs/design-review.md`; run `sql-apps check`. Coverage is not quality.

`sql-apps-application` is authoritative for behavior and permissions. Visual approval does not authorize schema, identity, data, or startup changes.
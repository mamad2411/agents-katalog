# Information Architecture

## Purpose
Design findable, shallow, predictable information architectures: content inventories, taxonomies with tested labels, navigation trees within depth limits, wayfinding validation (tree tests, first-click), and progressive disclosure flows that match user mental models.

## Use when
- Structuring a new product area: taxonomy, navigation tree, section labels.
- Fixing findability problems: users cannot locate features or content.
- Designing progressive disclosure: novice-to-expert flows, advanced settings layering.
- Validating IA with tree testing, card sorting, or first-click studies.

## Do not use when
- Detailing per-component props and keyboard maps (use `component-specification`).
- Running open-ended competitor teardowns (use `competitor-analysis`).
- Visual styling or token decisions rather than structure and labeling (use `wireframe-styleguide`).

## Required context
- Content inventory: screens, entities, and cross-link graph.
- User mental models and top tasks with wayfinding success criteria.
- Navigation depth limits and progressive-disclosure requirements.

## Procedure
1. **Inventory Everything**: List all screens, entities, and actions with current locations. Example row: `Billing history → Settings → Billing → History (depth 3)`. Flag orphans (no inbound path) and dead ends (no onward path) — both are defects.
2. **Taxonomize with Tested Labels**: Group content by user mental model (validate with open card sort, n ≥ 12), then label with user vocabulary from the sort — never org-chart jargon. Each label gets 2–3 rejected alternatives documented with why they failed.
3. **Draw the Tree Within Limits**: Produce the navigation tree honoring depth limits (e.g., ≤ 3 levels for primary nav, ≤ 5 for settings). Every leaf must be reachable by ≥ 2 paths (nav + search/shortcut) for critical tasks; high-stakes actions stay within 2 clicks of their context.
4. **Disclose Progressively**: Layer complexity: primary surface shows the 20% of controls covering 80% of tasks; advanced controls live one explicit step deeper with a visible affordance ("Advanced ▾"). Progressive disclosure must never hide destructive-action confirmations or error context.
5. **Validate Wayfinding**: Run tree tests (n ≥ 30) on top tasks; success criterion ≥ 80% direct success. Run first-click tests on key screens. Failures rewrite labels or restructure — never ship a tree users cannot navigate in test.
6. **Verify**: Run `scripts/verify.sh`. Confirm inventory closure (no orphans/dead ends), depth compliance, dual-path coverage for critical tasks, and wayfinding scores at or above threshold.

## Decision rules
- **User Words Win**: Labels come from card-sort vocabulary; internal team names are forbidden in primary navigation.
- **Depth Is a Budget**: Exceeding the depth limit requires removing or merging content, not requesting an exception.
- **Two Paths for Critical**: Any critical task with a single navigation path is incomplete IA.
- **Test Before Ship**: Structural changes ship only after tree-test/first-click scores meet the success criterion.

## Evidence required
- Content inventory with orphan/dead-end audit resolved.
- Navigation tree with depth annotations and dual-path coverage map.
- Tree-test and first-click results with participant counts and success rates.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- IA taxonomy with navigation tree and labeling rationale.
- Progressive-disclosure flows with depth-compliance evidence.
- Wayfinding test findings (tree tests / first-click) with remediation list.

## Stop conditions
- Navigation tree validated by wayfinding tests within depth limits.
- No orphans, dead ends, or single-path critical tasks remain.
- Token budget exhausted.

## Escalation rules
- Escalate to product lead if IA requirements conflict with business demands for promotional placement (needs explicit tradeoff call).
- Escalate immediately if legal/compliance content (privacy, safety) cannot be reached within the depth budget.

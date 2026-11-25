# Modal Overlay Recovery

## When To Use

Use this skill when the page has one or more blocking overlays (modals, cookie banners, newsletter popups, confirmation dialogs) that must be dismissed before the underlying content is accessible.

Use it for:

- cookie consent banners blocking page interaction
- newsletter or signup popups obscuring content
- multiple stacked overlays that must be dismissed sequentially
- any task where the first step is clearing blocking UI

Do not use it for:

- confirmation dialogs that are part of the intended workflow (use transactional-act-check-act)
- pages with no blocking overlays
- overlays that the user wants to interact with rather than dismiss

## Procedure

1. Call `dismiss_overlays` first. It clicks real close buttons where it finds them (framework state updates — these stay closed) and falls back to CSS-hiding only when no close control exists. Its result reports which path each dismissal took and any surviving overlay.
2. Re-read the page. For any overlay reported as CSS-hidden, reappeared, or still present, click its close/dismiss/accept/X control directly — one overlay at a time.
3. After each click, re-read to confirm the overlay is gone and to refresh element IDs (tags shift when the DOM changes).
4. If an overlay resists, try `press_key("Escape")`, then re-read and look for another dismiss target.
5. Proceed to the underlying task or call done only after a re-read shows no blocking overlays remain.

## Required Evidence

- The dismiss_overlays result showing what was dismissed and how
- Re-read confirming no blocking overlays remain
- If an underlying task follows, evidence that the content is now accessible

## Common Failures

- Calling done while a CSS-hidden overlay can still reappear
- Clicking stale element IDs after an overlay is removed (tags shift when DOM changes)
- Batching multiple dismiss attempts without re-grounding between them

## Verification

- After each dismissal, verify via re-read that the overlay is no longer present.
- Final verification: the underlying page content is visible and interactive.

## Relevance

Overlays and blocking modals are one of the most common browser-use pathologies. This skill prevents the agent from prematurely reporting success or burning turns on stale element references after partial dismissal.

Current E2E targets:

- `tests/e2e/continuation-act-check-act.test.ts` (Turn 1: dismiss cookie + newsletter)
- `tests/e2e/modal-overlays.test.ts`

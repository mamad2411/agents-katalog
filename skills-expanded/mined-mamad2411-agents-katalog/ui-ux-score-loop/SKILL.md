---
name: ui-ux-score-loop
description: Browser-based UI/UX improvement loop for one or more specified product flows. Use when the user asks to inspect, score, improve, or iteratively test flows such as signup, login, password reset, checkout, create/edit/delete/share, onboarding, or other key UI paths using a selected real browser, clean browser sessions, configurable interactive preflight, view granularity, screenshots, responsive breakpoints, light/dark modes, 0-100 UX rubric scores, and dashboard state files.
---

# UI/UX Score Loop

Improve one user flow, or multiple related user flows, by using browser evidence and 0-100 scores as the loop signal.

## Start Prompt

When the user invokes this skill, run this loop unless they ask only for advice:

```text
Run UI/UX Score Loop on [FLOW or FLOWS] at [URL or app environment] with one completion criterion: reach [TARGET]/100 flow score, improve by [PERCENT]%, or run [N] iterations. Use a real browser.

Interactive mode defaults to `auto`. In `auto`, start with a concise preflight interview when the request is thin or ambiguous about flow boundaries, environment, completion criterion, concerns, off-limits areas, browser, viewports, modes, view granularity, or improvement intensity. Proceed directly only when the user has meaningfully specified enough to run safely. If `interactive` is specified, always ask the preflight questions before starting. If `direct` is specified, proceed with defaults for unspecified noncritical settings and ask only for hard blockers.

A flow name is a user goal, not a route: "login flow" does not mean start at `/login`. If the user supplies a URL, start at that exact URL. If the user asks you to start or find an environment but gives no URL, identify the app origin and start at its root `/`. Do not open a deeper route such as `/login`, `/signup`, or `/reset-password` unless the user explicitly supplied that route or the root redirects there. For each requested flow, create a separate `.ui-ux-score-loop/flows/{flow-id}/dashboard.html`, state file, ratings file, and screenshots folder. When multiple related flows are requested, audit and improve them in relation to each other: compare shared components, copy, spacing, validation, loading, recovery, and visual states before changing shared UI so consistency improves across flows.

View granularity defaults to `standard` unless specified: `essential` captures only durable screens and critical states, `standard` captures normal screens plus meaningful modals/popovers/loading/error/success/recovery states, and `exhaustive` captures all user-meaningful states including hover/focus/pressed/disabled, multi-state popovers, representative error variants, slow loading phases, and important microinteractions. Explore each flow as fully as a real user would from the entry point, splitting necessary pages, views, and states according to the granularity setting. Act as a human proxy, not an agent: prefer visible navigation over guessed routes, assume imperfect memory and possible mistakes, value clear progress while waiting, and judge only what the UI explains without console logs or technical knowledge. For auth flows, include visible password reset/recovery as part of the audit unless the user excludes it.

If a browser/tool is specified, use it unless it cannot faithfully run the flow; otherwise prefer an integrated browser such as the Codex in-app/browser panel or the IDE integrated browser, then fall back to Playwright MCP or another external browser when needed. For every iteration/breakpoint/mode capture pass, start from a fresh browser state at the selected entry point: use a new private/incognito window, a new Playwright/browser context, or clear cookies, localStorage, sessionStorage, IndexedDB, cache, and service-worker state before navigating. Do not let authentication or onboarding state leak from baseline to later iterations, or from one breakpoint/mode pass to another. If a flow needs credentials, enter them through the UI each pass. Reuse an existing authenticated session only when the user explicitly asks for a returning-session audit, and record that exception. Unless viewports are supplied, test phone 390x844, tablet 768x1024, and laptop 1440x900. Discover theme support at the app level, not only on the entry page: check root/home, app shell after login when credentials exist, settings/profile/header controls, persisted theme keys, html classes/data attributes, CSS/framework dark-mode support, and browser color-scheme emulation. If light and dark can be activated reliably, always test both even when no toggle is visible on the login page; record how each mode was set. If no support is discoverable, use `default` mode.

Improvement intensity defaults to `grouped` unless specified: `focused` changes one highest-leverage issue per view, `grouped` changes a few logically related issues per view, and `broad` changes all safe identified issues per view. Apply intensity per view, not once for the whole iteration; in each iteration, improve every view that has a safe useful improvement, while leaving views alone when nothing should change. Create or refresh the flow dashboard before scoring, then complete each flow once without editing as iteration 0, break it into pages and views, and screenshot every view at every breakpoint and mode. Score each view/breakpoint/mode 0-100 against the UI/UX principles, update each dashboard after each iteration, improve the lowest user-impactful safe scores according to the intensity setting with brand-consistent changes, rerun from the same entry point, rescore, record deltas, and repeat until the criterion is met, progress stalls, or approval is needed. Do not finish without clearly giving the user each dashboard path and browser used.
```

If interactive mode is `auto` and the request is too thin to define the work responsibly, run the preflight before starting. If interactive mode is `direct`, ask only for missing hard blockers such as no flow, no discoverable environment, no completion criterion, or unavailable credentials.

## Workflow

1. Resolve interactive mode first. Use `auto` by default. If the user requested `interactive`, or if `auto` sees a thin/ambiguous prompt, run the preflight interview below. If the user requested `direct` or supplied enough meaningful configuration, proceed with defaults for unspecified noncritical settings.
2. Confirm the flow or flows, URL or discoverable app environment, concerns, off-limits areas, one completion criterion, any custom viewports, any browser/tool preference, whether light/dark mode is specified, the view granularity, and the improvement intensity. If view granularity is not specified, use `standard`. If improvement intensity is not specified, use `grouped`.
3. If custom viewports are not supplied, use phone 390x844, tablet 768x1024, and laptop 1440x900.
4. Discover theme support before finalizing modes. Check the root/home page, authenticated app shell when credentials are available, settings/profile/header controls, persisted theme keys, html classes/data attributes, CSS/framework dark-mode support, and browser `prefers-color-scheme` emulation. If light and dark can be activated reliably, test both automatically even if the login page itself has no visible toggle. If support is specified by the user, test the specified modes. If no support is discoverable, use one `default` mode. Record how each mode was set.
5. Select the browser/tool. Prefer the user's requested browser if it can exercise the flow. If no preference is supplied, prefer an integrated browser. Use an external browser only when the integrated browser is unavailable, cannot create or clear a clean context, cannot set the needed viewport/mode, cannot capture screenshots, cannot reach the target, or the user explicitly requested a returning-session audit that requires an existing session.
6. Use clean browser state for evidence integrity. For each iteration, breakpoint, and mode capture pass, open a fresh private/incognito window or fresh browser context when possible. If the tool cannot do that, clear site cookies, localStorage, sessionStorage, IndexedDB, cache, and service-worker state before navigating. Close or discard that context after the pass. Do not reuse auth/session/onboarding state across passes unless the user explicitly requested a returning-session audit; record any exception in `state.json` or `ratings.md`.
7. Run the dashboard helper once per requested flow immediately so each `.ui-ux-score-loop/flows/{flow-id}/dashboard.html`, that flow's `data/`, that flow's `screenshots/`, and the gitignore entry exist before evidence is captured.
8. Choose the entry point as a human would. A flow name is not a route. If the user supplies a URL, start at that exact URL for iteration 0. If the user asks you to start/find an app but supplies no URL, identify the app origin and start at `/`. For a login flow, begin at `/` and follow visible navigation or redirects into auth; do not start at `/login` unless the user explicitly supplied `/login` or `/` redirects there.
9. Explore the flow as fully as possible from that start, following the path a human is likely to take. Prefer visible links, buttons, and navigation over guessed routes or internal knowledge. Break the flow into pages and views according to view granularity. `essential` captures durable screens plus critical loading, blocking error, validation, success, and recovery states. `standard` also captures meaningful route transitions, forms, modals, popovers, drawers, empty states, common error variants, and post-completion states. `exhaustive` additionally captures user-meaningful hover, focus, pressed, disabled, expanded/collapsed, slow loading, multi-step popover/modal, edge-case error, and microinteraction states that could affect confidence, clarity, or completion. Do not create separate views for purely decorative or technically different states that look and behave the same to the user.
10. Treat obvious alternate or recovery paths that serve the same user goal as analysis views. For auth flows, include visible forgot-password/reset-password states unless the user excludes them.
11. Audit as a human proxy. Assume the user may not know exact credentials, may mistype, may need reassurance while waiting, may not understand technical errors, and may abandon if progress, next steps, or recovery options are unclear.
12. Screenshot every view at each breakpoint/mode.
13. Score each view/breakpoint/mode from 0-100 against the principles below.
14. Update and regenerate the dashboard with browser, mode, breakpoint, view, page, flow, and principle averages.
15. Improve per view according to the intensity setting. `focused` means one highest-leverage safe change per view. `grouped` means a few logically related safe changes per view and is the default. `broad` means all identified safe improvements per view, while still avoiding rewrites, brand drift, and risky behavior changes. Do not spend an iteration on one change in one view unless only that view has a safe useful improvement or approval is needed elsewhere.
16. Rerun the same full flow from the same entry point in a fresh browser state, capture new screenshots for affected views, breakpoints, and modes, rescore, record deltas, and keep the iteration only if it improves the target without creating a worse problem elsewhere.

Stop when the completion criterion is met, two passes stall, or the next best change needs approval.

## Interactive Preflight

Interactive mode controls whether the loop interviews the user before running:

- `auto`: default. Ask a preflight only when the request is thin, contradictory, or missing important boundaries.
- `interactive`: always ask the preflight questions before starting.
- `direct`: skip the preflight; use defaults for unspecified noncritical options and ask only for hard blockers.

When preflight is needed, ask concise grouped questions that cover every configurable setting:

- Flows and boundaries: exact user goal, start/end, included alternate paths, excluded paths, and whether related flows should be compared for consistency.
- Environment and access: URL or app environment, credentials/session expectations, data that may be used, and off-limits behavior.
- Completion: target score, percent improvement, or max iterations.
- Browser: integrated browser preference, Playwright MCP, Chrome/session, or other required browser.
- Evidence matrix: breakpoints, color modes, and whether to discover light/dark support automatically.
- View granularity: `essential`, `standard`, or `exhaustive`.
- Improvement intensity: `focused`, `grouped`, or `broad`.
- Product concerns: brand, voice, risk areas, accessibility, user anxieties, and changes that need approval.

After the preflight, summarize the chosen config in a compact checklist, then start the loop.

## Scoring

Before scoring or choosing an improvement target, read `references/ui-ux-principles.md` for compact principle guidance distilled from the user's preferred UI/UX playbook. Do not load or add the source book.

Use the full 0-100 range:

- 0-39: harmful or confusing.
- 40-59: weak; usable only with effort.
- 60-74: adequate, with clear friction.
- 75-89: strong, clear, low-friction.
- 90-100: excellent and hard to improve.

Score each view against: visual hierarchy, proximity, clarity, alignment, contrast, simplicity, whitespace, layout, balance and harmony, consistency, visual cues, depth and texture, color theory, typography, and interaction cost.

Always explain scores through serving the user: does this help the user accomplish their real goal with confidence, speed, and dignity? Penalize agent-only affordances: hidden routes, assumed knowledge, silent waiting, console-only errors, raw technical messages, unclear recovery, or states that are only understandable because the agent can infer what happened.

## Guardrails

Do not overhaul the UI. Preserve brand, voice, information architecture, and working behavior. Do not add decorative AI slop, generic gradients, random cards, unnecessary animation, or novelty that does not help the flow. Ask before changing navigation, pricing, auth, destructive actions, business logic, or product strategy.

## Browser Selection

Accept optional browser guidance such as:

- `Browser: Codex in-app browser`
- `Browser: VS Code integrated browser`
- `Browser: Playwright MCP`
- `Browser: Chrome with my logged-in session`
- `Browser: prefer integrated`

Choose the browser that best preserves the real user experience and required state. Prefer integrated browser tooling for local app flows because it keeps screenshots and interactions close to the workspace. Use Playwright MCP or another external browser when it is better for viewport automation, repeatable screenshots, auth/session access, cross-browser behavior, or when integrated tooling is unavailable. Record the preference, selected browser, and reason in `.ui-ux-score-loop/flows/{flow-id}/data/state.json`.

Fresh state is part of browser selection. Prefer tools that can create a new incognito/private window or isolated browser context per iteration/breakpoint/mode pass. Playwright-style contexts are ideal for repeatable screenshots. If using Chrome or an integrated browser, create a new private window when possible or clear site data before each pass. Auth flows should log in through the UI every pass so retained cookies do not hide friction. Reuse an existing session only for an explicitly requested returning-user/session audit, and record the caveat.

## Dashboard

Create loop state only under `.ui-ux-score-loop/`. This directory is intentionally ignored by git and must not be committed.

Run the dashboard helper before taking screenshots or writing ratings. The helper adds `.ui-ux-score-loop/` to the target repository's `.gitignore` before it creates files.

Use this structure:

- `.ui-ux-score-loop/flows/{flow-id}/dashboard.html`: generated Tailwind dashboard for one flow.
- `.ui-ux-score-loop/flows/{flow-id}/data/state.json`: structured source of truth for that flow's interactive mode, view granularity, improvement intensity, iterations, view scores, rubric scores, and next target.
- `.ui-ux-score-loop/flows/{flow-id}/data/ratings.md`: short human notes and rationale that should not clutter that flow's dashboard table.
- `.ui-ux-score-loop/flows/{flow-id}/screenshots/iteration-000/{breakpoint}/{mode}/001-view-name.png`: baseline screenshots.
- `.ui-ux-score-loop/flows/{flow-id}/screenshots/iteration-001/{breakpoint}/{mode}/001-view-name.png`: first changed iteration screenshots.
- Continue with zero-padded iteration folders.

Use one flow folder per audited flow. This prevents login, signup, checkout, or other flows from overwriting each other's state and screenshots. When multiple related flows are audited together, keep each flow's dashboard separate but compare shared components, copy, spacing, states, and decisions across the flow folders before making changes so consistency improves together.

Name screenshots by the view's order in the flow. Use `001`, `002`, `003`, etc. so files sort naturally. Keep the same number for the same view across breakpoints and iterations.

Use `scripts/create_dashboard.py` to create or refresh the dashboard workspace:

```bash
python3 scripts/create_dashboard.py --flow "Signup"
```

This creates `.ui-ux-score-loop/flows/signup/dashboard.html` by default. Use `--flow-id` for a stable custom folder name:

```bash
python3 scripts/create_dashboard.py --flow "Sign up" --flow-id signup
```

To seed a custom viewport set, pass repeated viewport flags:

```bash
python3 scripts/create_dashboard.py --flow "Signup" --viewport phone:390x844 --viewport desktop:1728x1117 --mode light --mode dark --browser "Codex in-app browser" --interactive-mode auto --view-granularity standard --improvement-intensity grouped
```

Interactive mode options:

- `auto`: ask preflight questions only when the request is underspecified. This is the default.
- `interactive`: always ask preflight questions before starting.
- `direct`: proceed with defaults and ask only for hard blockers.

View granularity options:

- `essential`: capture durable screens and critical states only.
- `standard`: capture normal screens plus meaningful modals, popovers, loading, error, success, recovery, and post-completion states. This is the default.
- `exhaustive`: capture all user-meaningful states, including hover, focus, pressed, disabled, expanded/collapsed, multi-state popovers, representative error variants, slow loading phases, and important microinteractions.

Improvement intensity options:

- `focused`: change one highest-leverage safe issue per view per iteration.
- `grouped`: change a few logically related safe issues per view per iteration. This is the default.
- `broad`: change all identified safe issues per view per iteration, while preserving brand, behavior, and reviewability.

Use `assets/dashboard.html` as a template asset; do not paste it into chat unless the user asks.

Do not hand-edit `dashboard.html`. Update the flow's `data/state.json` and `data/ratings.md`, then rerun the script.

The dashboard must be information dense, not a written report. Keep the top minimal: flow name, subtle Expand all / Collapse all text controls, breakpoint dropdown, and light/dark mode dropdown. Put the expand/collapse controls to the left of the dropdowns and style them as secondary text, not prominent buttons. Do not put status chips, next-target boxes, explanatory copy, or summary cards above the table. The main view must be one comparison matrix with iterations as columns and an obvious hierarchy: collapsible flow context rows, page band rows, then indented view groups. Flow context, page rows, and view rows must work like an accordion so the user can collapse noisy detail. Each page band should show that page's average for each iteration. Each view header row should show that view's score, delta, weakest principle, and screenshot thumbnail for each iteration; do not create a separate screenshot row. Screenshot thumbnails must remain visible when a view group is collapsed, sit on a contrasting evidence frame, and open a large modal preview. View detail rows should contain notes and rubric ratings. End each breakpoint/mode block with a flow average row.

## Final Answer Contract

Always deliver the dashboard explicitly. The final answer must include:

- The path to each `.ui-ux-score-loop/flows/{flow-id}/dashboard.html`.
- The path to each `.ui-ux-score-loop/flows/{flow-id}/data/state.json`.
- The screenshot root path for each flow.
- The browser/tool used and why.
- The completion status and current flow score or best available score.
- The next target if the loop is not complete.

Do not treat the dashboard as an internal artifact. If the dashboard could not be generated, say why and give the exact command or blocker.

---
name: wreck-explore
description: Explore a running local web app through Playwright MCP as a normal user (every core flow plus data-integrity checks) and then in character as each persona from .wreck-it/personas.md, recording reproducible bugs with wreck-it. Use as stages 4–5 of a wreck-it run, or when the user asks to "click through my app like a user", "test the happy paths", "try my app as a beginner", or "check my core flows".
---

# wreck-explore

`WRECK` means `npx @miyanishar/wreck-it`.

Two passes:
1. **Normal-user pass**, persona `normal-user`.
2. **Persona exploration**, every other persona in `.wreck-it/personas.md` except `chaos-monkey`.

Needs `.wreck-it/discovery.json` (`WRECK discover`), `.wreck-it/personas.md` (wreck-personas skill) and Playwright MCP. Follow the wreck-it skill's rules, and record bugs as in its `references/recording-findings.md` (structured steps, role/label targets, assertions for correct behavior, replayed in a fresh context before `reproduced: true`).

## Per page, every time

After each navigation or meaningful action:
1. `browser_snapshot` to read the page. Use the role and name values it shows for targets.
2. Run the oddity script: `browser_evaluate` with the output of `WRECK oddity-script` (fetch it once and reuse it).
3. Check `browser_console_messages` (errors) and `browser_network_requests` (4xx/5xx).
4. Log coverage: `WRECK run visit <route> --persona <slug>`.
5. Before recording a finding, take a screenshot with `browser_take_screenshot` that shows the failure, inspect it, and attach its actual path in `evidence.screenshots`. Refresh the evidence during reproduction when needed; follow the shared recording guide for storage and presentation.

## Pass 1: normal-user (stage `normal`)

`WRECK run stage normal running`

Walk every core flow as intended. Get the flows from discovery: sign-up, login, CRUD on each main entity, search, checkout, settings, logout. Use realistic test data: addresses from `WRECK email new` (never `example.com`; see the wreck-it skill's email rule), password `Wreck-it-123!`, and names or titles starting with `wreck-it`. Log each thing you create with `WRECK run created "<what>" --by normal-user`. If the app has onboarding (a welcome wizard, plan or track picker), finish it first with typical choices, and note it in `.wreck-it/normal-pass.md`. If self sign-up is impossible, use `accounts[0]` from `.wreck-it/config.json`. If neither works, ask the user for a test account.

After the flows, work through this **checklist**. Every row is required. Write it to `.wreck-it/normal-pass.md` as a table with one line per row, marking each ✓ (checked, fine), ✗ WR-NNN (bug recorded) or — (not applicable, say why). A violation is a `functional` finding unless noted.

| # | Check | How |
|---|---|---|
| 1 | Created items appear in their list and detail page | Create one of each main entity, then open the list and the detail page |
| 2 | Edits persist | Edit a record and see the success message, then `reload`. Then open the page in a fresh context with the same session (`browser_close`, `browser_set_storage_state`) and check again. Don't log out the shared account (see row 9) |
| 3 | Deletes disappear everywhere | After deleting or removing: lists, counts, **header badges**, search and totals all update |
| 4 | Arithmetic is right at every step | Use **quantity ≥ 2 on at least one item** and apply any discount, coupon or promo you can find. Recompute subtotal, discount and total by hand at each place they're shown: cart, checkout, confirmation, detail page, list page. Every number must match your calculation and every other page. |
| 5 | Same entity, same facts everywhere | Name, price, status and **date format** must be identical between list and detail views |
| 6 | Lists are sorted sensibly | History, orders and activity should be newest first, or have an obvious sort control. Otherwise it's `ux` |
| 7 | Fresh-account empty states | Sign up a brand-new account and open every list or collection page (orders, cart, history, dashboard) while it's empty. Expect a clear empty state with a next step. A spinner still spinning after 5 s, a blank area, or a dead end is `ux` |
| 8 | Error messages help | **In the browser UI** (not curl: the API message can be fine while the page hides it), submit each auth or settings form with one invalid field (bad email format, short password). The message should name the problem and keep the other fields filled. A generic "Something went wrong" or wiped fields is `ux` |
| 9 | Session survives | **With a throwaway account only, and last:** log out, log back in, and check that its data is still there. Never log out the account whose saved session other stages use. With SSO-only login and no second account, mark — (needs a second login) |

A broken core flow is `critical` or `high`. The report surfaces these first.

`WRECK run stage normal done`

## Pass 2: personas (stage `explore`)

`WRECK run stage explore running`

For each persona:
1. Set the viewport with `browser_resize` to the persona's device. (In the Claude Code plugin, `wreck-browser-3` already emulates a phone; a phone persona there skips this step.)
2. If the persona's network is slow or flaky, note it. Chaos owns network faults; here, just be impatient the way the persona would be.
3. Work through the persona's missions **in character**:
   - **ICP personas:** pursue the goal efficiently and notice anything that would make them churn.
   - **rushed-beginner:** skip instructions, double-click submit buttons (`click` with `count: 2`), use wrong formats (`12/31/24` vs `2024-12-31`, `$1,000` in a number field, phone numbers with spaces), leave fields empty, press back mid-flow, abandon a flow and come back, and add trailing spaces.
4. **Time budget:** about 15 actions per mission. If the persona can't finish a mission within budget, or can't tell what to do next, that is a `ux` finding. Record what blocked them in `actual`.
5. Record bugs with `"persona": "<slug>"`.

### Claude Code parallel mode

When the `wreck-persona` subagent and the `wreck-browser-1..3` MCP servers are available, the orchestrator dispatches one subagent per persona, up to 3 at a time. Each subagent:
- gets the persona block and the base URL
- follows only this section, with its own browser
- records findings directly (the CLI handles concurrent `finding add` safely)

`WRECK run stage explore done`

## Auth state

- If config has an account with `storageState` (from `wreck-it login`), start logged-in missions with `browser_set_storage_state` `{"filename": ".wreck-it/auth/<label>.json"}`, then navigate. Don't attempt Google/GitHub/SSO sign-in yourself.
- Otherwise log in (or sign up) once through the UI and keep the browser session for later missions. Don't sign up again for every mission.
- Record findings that start logged in with `"auth": "<label>"` and steps that begin after login.
- If the session expires unexpectedly mid-flow, that's a finding: `functional`, medium.

## What not to record

- Intended validation behaving correctly. For example, "email required" shown for an empty email is correct.
- Bugs that need production data or third-party services that aren't configured locally. Mention these in your final summary instead.

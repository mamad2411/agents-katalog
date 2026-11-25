---
name: wreck-it
description: Full wreck-it run against a locally running web app. It tests like normal users, ICP personas, rushed beginners, chaos monkeys and traffic spikes, then writes a scored bug report with source file:line and regression Playwright tests. Use when the user says "wreck my app", "wreck it", "test my app like a user", "find bugs before launch", "is my app ready to ship", or asks for a readiness score. Also for one feature, such as "test the checkout", "just test signup", "check the coupon flow" (a focused run). For a single stage ("just stress test my API", "only check accessibility"), use the matching wreck-* skill.
---

# wreck-it: Wreck your app before your users do

`WRECK` below means `npx @miyanishar/wreck-it`. The CLI does the deterministic work (setup, discovery, sweeps, fuzzing, page speed, load, findings, score, report, tests). You drive the browser through Playwright MCP, play the personas, judge what's a bug and trace it to code.

Report only. **Don't fix bugs** during a run unless the user asks after the report.

## Rules (always)

- **Local only.** The CLI refuses non-local targets. Pass `--i-own-this` only when the user says they own a remote one.
- **Fake data only.** Test accounts, fake names, never real personal or payment data. Name what you create `wreck-it …`, and log it: `WRECK run created "<what>" --by <persona>` (the report lists it for cleanup).
- **Ask before writing.** Preflight's `safety.ask` lists the questions: a hosted (often production) database, live Stripe keys, email without a readable inbox, paid AI/SMS calls. Ask them all in **one** message before the normal-user pass, and record each "yes" in `.wreck-it/config.json` (`allowRemoteDb`, `testEmail`, `allowSideEffects`). If the database is production, offer to stop so they can point the app at a dev project.
- **Money and messages.** Pay only with Stripe test keys (card `4242 4242 4242 4242`); with live keys stop at the payment step. Trigger AI/SMS/email actions at most 2–3 times per flow unless allowed. `fuzz` and `load` skip those endpoints themselves.
- **Email.** Sign up with addresses from `WRECK email new`, never `example.com`. With a local inbox read the link yourself (`WRECK email read --to <address>`); otherwise ask the user for it, or mark the check "skipped: no readable inbox".
- **Keep the shared login alive.** Never log out, delete or change the password of the account whose saved session other stages use: on Supabase and many apps, logging out ends every session of that user. Test logout and deletion last, with a throwaway account.

## Focused run (one feature)

When the user names one feature or flow ("test the checkout", "/wreck focus signup"), test only that, in minutes:

1. `WRECK run init --focus "<feature>"`, `WRECK discover`, `WRECK setup --dry-run` and `WRECK preflight --wait 5`, handled as in stage 1. Log in (stage 2) only if the feature needs it. Ask `safety.ask` questions only if the feature writes data.
2. **Scope it.** From `discovery.json` and the code, list the feature's pages and API routes (e.g. `/cart`, `/checkout`, `/api/cart`, `/api/orders`). Tell the user the scope in one line.
3. **Test it** (skip personas and stages that don't apply; mark them `skipped`):
   - Walk the feature as a normal user, then as a rushed beginner on a phone (double clicks, wrong formats, back mid-flow). Check the explore skill's checklist rows that apply (totals, persistence, deletes, error messages).
   - `WRECK sweep --record --only <pages…>` and `WRECK fuzz --record --only <api routes…>`.
   - The chaos skill's hostile inputs, double submits, navigation and network faults, on this feature's forms only.
   - `WRECK perf --record <pages…>` if the feature has its own pages.
4. Reproduce and trace every finding (stage 9), then `WRECK report && WRECK gen-tests`. The report is labelled as a focused run: say "feature score", not "readiness".

## Pipeline

Mark stages with `WRECK run stage <stage> running|done|skipped|failed`. Findings are saved as you go.

### 1. Setup and preflight
```bash
WRECK run init               # --fresh discards a previous run's findings
WRECK discover
WRECK setup --dry-run        # what's installed, what's missing
WRECK preflight --wait 5
```
- If `setup --dry-run` lists anything to install, show it and ask once; on yes run `WRECK setup`. If it added MCP servers, browser tools appear only after the user restarts the agent: say so, and offer a CLI-only run meanwhile.
- A browser tool saying "Browser … is not installed": `WRECK setup --skip playwright-mcp devtools-mcp`, then retry.
- Preflight exit 4 (app not reachable): offer to start `devScript` in the background, then `WRECK preflight --wait 60`. Exit 3 (target refused): stop and explain.
- No `.wreck-it/config.json`: create `{"baseUrl": "http://localhost:3000"}` (use the real port).
- **CLI-only run** (no browser tools): `sweep --record`, `fuzz --record`, `perf --record`, stage 7 and the report; mark `personas`, `normal`, `explore`, `chaos` skipped and say why. Never pretend you clicked through the app.

### 2. Logging in
- **Google, GitHub, SSO, hosted sign-in, magic links, 2FA** (`discovery.json` `auth.sso` is set, or there's no password field): tell the user "A browser window will open. Log in as your test user; it closes by itself once you're in." Run `WRECK login` (it waits up to 10 minutes; use a long timeout). Its output should say `check: valid`. For two-user checks ask for `WRECK login --label second`; for fresh-account checks `--label fresh`, or mark them skipped.
- **Email and password:** sign up a test account (or use the user's) and add `"accounts": [{"label": "main", "email": "…", "password": "…"}]` to config.
- From then on: `sweep`, `fuzz` and `perf` log in by themselves. In the browser, call `browser_set_storage_state` with `{"filename": ".wreck-it/auth/<label>.json"}` before visiting logged-in pages. Findings recorded logged in get `"auth": "<label>"` and steps that start after login.
- If preflight or `WRECK login --check` says `expired`, ask the user to run `login` again.

### 3. Personas
Use the **wreck-personas** skill.

### 4–5. Normal user, then personas
Use the **wreck-explore** skill. In Claude Code with the plugin, run up to 3 personas in parallel as `wreck-persona` subagents, one browser each (`wreck-browser-1..3`); don't use a browser yourself meanwhile, and wait for all of them before stage 6. Other agents: one persona after another.

### 6. Chaos
Use the **wreck-chaos** skill (sweep, API fuzz, hostile inputs, double submits, navigation, network faults, session tampering, keyboard).

### 7. Page speed and load
Use the **wreck-load** skill.

### 8. Security
Not in v1: `WRECK run stage security skipped`.

### 9. Reproduce, then trace
`WRECK finding list`: replay every `?` finding in a fresh context and set `reproduced: true` if it shows again (unreproduced findings score nothing). Then use the **wreck-trace** skill on every reproduced finding without a `source`.

### 10. Report
Before generating the report, check each reproduced browser finding for a screenshot that shows the actual failure. Revisit findings from CLI sweeps too; follow the screenshot guidance in `references/recording-findings.md`. Verify the saved image files exist and resolve any missing-screenshot warnings. API-only or load findings may use request/metric evidence instead; say when a screenshot is not applicable or could not be captured.

Generate the report and tests after the last finding update. If you change a finding afterward, regenerate both before presenting results. Read `references/regression-tests.md`: inspect preserved-spec warnings and reconcile those tests with the updated findings; regeneration deliberately keeps agent edits and fixtures. Run supported specs against the buggy app and check that failures reach the intended assertions. Disclose skips, setup failures, timeouts, or unverified tests in the report; where a corrected copy exists, check the same specs against it too.

```bash
WRECK report && WRECK gen-tests && WRECK run stage report done
```

## While exploring (stages 4–6)

- Record bugs exactly as in `references/recording-findings.md`: `WRECK finding add`, structured steps, role/label targets, assertions that describe correct behavior, then replay in a fresh context and set `reproduced: true`.
- After each navigation, run the oddity script (`WRECK oddity-script`, once) via `browser_evaluate`, and check `browser_console_messages` and `browser_network_requests` (4xx/5xx). Also look for what scripts can't judge: broken layout, empty states without guidance, endless spinners, dead buttons, inconsistent dates or prices. Record real ones as `oddity`.
- Log coverage: `WRECK run visit <route> --persona <name>`.

## Final message

Short: the score and band, the "fix this first" finding with its `file:line`, counts by severity, incomplete stages, the paths `.wreck-it/report.html`, `.wreck-it/report.md`, `tests/wreck-it/`, and `npx playwright test tests/wreck-it`. Offer to fix the top findings; wait for a yes.

When presenting a bug, attach its relevant screenshot beside the finding ID and explanation. Use the chat's image attachment support or a Markdown image with the actual saved file path; a report path alone does not show the evidence. Present the top findings in chat with their screenshots and keep the complete set in the reports. If an image is unavailable or not applicable, say why and link the request, trace, or metrics instead. Resolve stored `shots/...` paths relative to `.wreck-it/`.

Use this shape for each browser finding you include in chat (replace the example with the actual finding and verified absolute image path):

```markdown
**WR-007 — Cart subtotal ignores quantity** (`lib/cart.ts:19`)
Three $79.99 items should total $239.97; the page shows $79.99.
![WR-007: quantity 3 with an incorrect subtotal](/absolute/project/.wreck-it/shots/WR-007-cart.png)
```

Before sending, open each image you plan to present and describe the state and values it actually shows. Verify that each browser finding you present has an image attachment or image embed. A list of image filenames or a statement that screenshots are saved is not an attachment. Keep the response concise by presenting fewer findings, with their evidence, and linking the complete report; leave the remaining browser findings in that report instead of adding an unillustrated list in chat.

---
name: wreck-chaos
description: Chaos-test a running local web app as the chaos-monkey persona, using a page sweep, an API fuzzer (plus Schemathesis when there's an OpenAPI spec), hostile form inputs, double-submits, back/forward/refresh mid-flow, multiple tabs, offline/slow/500-injected network, expired or tampered sessions, an axe-core scan and keyboard-only navigation. Records reproducible bugs with wreck-it. Use as stage 6 of a wreck-it run, or when the user asks to "break my forms", "chaos test", "try weird inputs", "test offline", or "check accessibility".
---

# wreck-chaos

`WRECK` means `npx @miyanishar/wreck-it`. Persona: `chaos-monkey`: curious and adversarial, but only against the user's local app. Follow the wreck-it skill's rules (fake data, no paid side effects in loops, never log out the shared account).

`WRECK run stage chaos running`

Record bugs as in the wreck-it skill's `references/recording-findings.md`: one finding per root cause (not per bad input), replayed in a fresh context before `reproduced: true`. After each attack run the oddity script and check console and network: chaos often shows up as rendered `undefined`/`NaN` or a 500.

## 1. Page sweep (CLI)

```bash
WRECK sweep --record
```
Every discovered page at 1280x800 and 390x844, logged in when an account is configured. It records one reproduced finding per root cause (rendered `undefined`/`NaN`, broken images, dead links, mobile overflow, server errors, axe rules). Judge its "to judge yourself" list and record the real ones. **Run it again** once later sections have put the account in a richer state (items in the cart, an order placed): it records only what's new.

## 2. API fuzz (CLI)

`fuzz` sends bad values to each write endpoint, one field at a time (negative/huge/fractional numbers, text for numbers, empty/space-padded/5,000-char/`%`/emoji strings, `null`, missing fields, invalid JSON), with real ids and the configured login.

1. **Seed it with real requests.** Invented values (`"TEST"` as a coupon) stop at validation; real ones (`"SAVE10"`) reach the logic behind it. For the important writes you made earlier, read the request with `browser_network_request` and save it to `.wreck-it/requests.json`:
   ```json
   [{"method": "POST", "path": "/api/cart/coupon", "body": {"code": "SAVE10"}}, {"method": "GET", "path": "/api/search", "query": {"q": "lamp"}}]
   ```
2. `WRECK fuzz --record`. It needs `"allowRemoteDb": true` for a hosted database (see the wreck-it skill's "Ask before writing"), and skips endpoints that call AI, email, SMS or payments unless allowed. With an OpenAPI spec it also runs Schemathesis.
3. 5xx responses are recorded and reproduced automatically. **Judge the "accepted values" list yourself:** a 2xx for `quantity: -1` is a bug only if the app then shows it (negative totals). Check the UI and record a `chaos` finding with UI steps.

## 3. Hostile inputs (every form)

One field at a time, the others valid:

| Input | Values |
|---|---|
| empty / spaces | `""`, `"   "`, `" valid-value "` |
| long | 5,000 × `a`; a 300-char email local part |
| unicode | `Zoë 🦄 李雷 مرحبا`, zero-width `a​b` |
| numbers | `-1`, `0`, `1e309`, `999999999999`, `0.1+0.2`, `NaN`, `1,000` |
| dates | `2024-02-30`, `12/31/24`, `9999-12-31` |
| markup / query | `<b>bold</b>`, `'; --`, `%`, `_`, `\` |

Also by field type, in the UI and as a direct `http` step when the form posts JSON:
- **Quantities and amounts:** `-1`, `0`, `1000000`, `2.5`, then check totals and the stored value. A negative quantity or amount accepted is `chaos`, high.
- **Codes looked up server-side** (coupons, usernames, slugs): surrounding spaces, lowercase, valid-but-inactive.
- **Search:** `%`, `%%`, `\`, quotes, 300 characters, emoji.

Look for 500s, mangled or truncated values, broken layout, absurd totals, and validation that accepts junk or rejects `Zoë`. Markup rendered as HTML is a security matter: mention it in your summary, don't file it. On forms that call AI, send email/SMS or charge a card, one or two attempts only.

## 4. Double submits

MCP clicks are often too slow to overlap, so also fire the submit request **twice at once** with the session cookie:
```bash
curl -s -b "<cookie>" -H 'content-type: application/json' -d '<body>' <baseUrl>/api/… & curl -s -b "<cookie>" -H 'content-type: application/json' -d '<body>' <baseUrl>/api/… & wait
```
Two orders or records is `chaos`, high (two `http` steps). In the UI, `click` with `count: 2` on every create/pay/send, then 5 fast clicks, and check for duplicates.

## 5. Navigation

- `back`, `forward`, `reload` at every step of multi-step flows: nothing lost, duplicated or charged twice.
- After a successful submit, `back` and submit again.
- Two tabs (`browser_tabs`): finish the flow in tab A, continue in tab B.
- Deep links into step 3, or to ids that don't exist (`/items/999999`, `/items/abc`): expect a real 404 or empty state.

## 6. Network faults

- **Offline:** fill a form, `browser_network_state_set` `{"state": "offline"}`, submit, set it back to `"online"`. Expect a clear error, input kept, no false "Saved!". Record with `setOffline` steps.
- **Server errors:** `browser_route` `{"pattern": "**/api/<endpoint>", "status": 500, "body": "{\"error\":\"boom\"}", "contentType": "application/json"}` on the 2–3 most important calls, trigger them, then `browser_unroute`. Also try `"status": 200, "body": "{}"` or `"[]"`. Expect a friendly error and a retry, not a blank page, endless spinner or false success. Record with `assertions: []`, the mocked route in `actual`, and a screenshot.
- **Slow network:** with Chrome DevTools MCP (`wreck-devtools` in the plugin): `new_page` (keep its `pageId`), `emulate` `{"networkConditions": "Slow 3G"}`, submit. Expect spinners that resolve and a disabled submit button while pending.
- Missing tool: skip that check and say so in your summary.

## 7. Session and storage

- **Session gone mid-flow:** use a throwaway login (never the shared one), reach checkout or step 2, `browser_cookie_clear`, submit. Expect a redirect to login or a clear message, never a 500 or lost input.
- **Tampered state:** `browser_localstorage_list`. If it holds a cart, prices or flags, change one (`browser_localstorage_set`: negative quantity, price `0`) and reload. A server trusting a tampered price is `chaos`, high. A tampered role unlocking admin UI goes in your summary (security).
- **Corrupted state:** set a stored JSON value to `{` and reload. The app should recover.

## 8. Accessibility

`sweep` already ran axe on every page. For states only reachable mid-flow (a modal, step 2), run `WRECK a11y <url> --record` if the state has a URL, or re-run `sweep`. Then walk each core flow with only `browser_press_key` (`Tab`, `Shift+Tab`, `Enter`, `Space`, `Escape`, arrows) and record as `accessibility`: unreachable controls, invisible focus, focus traps, modals that ignore Escape, illogical tab order.

## Finish

For each `high`/`critical` finding, record the replay as a trace: `browser_start_tracing`, replay, `browser_stop_tracing`, then `WRECK finding update WR-NNN '{"evidence": {"trace": "<path>"}}'`.

Write `.wreck-it/chaos-log.md`: one line per form or flow × technique (sections 1–8), each ✓, ✗ WR-NNN or "skipped: reason". Then `WRECK run stage chaos done` and summarize by technique.

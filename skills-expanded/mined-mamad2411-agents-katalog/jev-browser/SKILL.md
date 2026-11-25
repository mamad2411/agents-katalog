---
name: jev-browser
description: How to drive a web browser with the jev-browser tools (browser_open, browser_do, browser_check, browser_read, browser_snapshot, browser_act). Use when the user asks to do something on a website, such as filling a form, logging in, clicking through a flow, checking a page, or reading a long web page, and the jev-browser tools are available.
---

# Driving the browser with jev-browser

You plan; Jev decides. `browser_do` takes ONE outcome, and a fast decision model (Jev) picks
each element, action and value on its own. Jev answers only yes/no, pick-one and rating
questions. It cannot write text or plan more than one step, so every string it types has to
come from you, and the sequence of steps is yours.

## The loop

1. `browser_open(url)`.
2. `browser_do(goal, values)` for each step, one observable outcome at a time.
3. Read the `status`. Anything except `done` means it is your turn (see below).
4. After a step with side effects, `browser_check` something that must, or must not, have
   changed.

## Writing a step

- **One outcome per call:** "Log in", "Add the Backpack to the cart", "Open the Pull
  requests tab". Split "add two todos, complete one, clear completed" into four calls.
- **Every string goes in `values`, with meaningful keys:**
  `{"email": "...", "password": "..."}`, `{"postal_code": "94107"}`,
  `{"file": "/abs/path.pdf"}`. Never put the text to type in `goal` alone.
- **Make open-ended goals measurable:** "until at least 3 new results are shown", not "load
  more".
- **Use your own judgement for comparisons:** don't ask `browser_do` whether a table is
  sorted or exactly one thing changed. Use `browser_check` or `browser_snapshot` and judge it
  yourself.

## Statuses

| status | what to do |
|---|---|
| `done` | move on |
| `likely_done` | verify with `browser_check`, or `browser_snapshot(diff: true)`, before moving on |
| `needs_login` | ask the user for credentials, or ask them to turn on "Show the browser window" and a browser profile in the plugin settings and log in themselves |
| `needs_confirmation` | the next action looks irreversible (order, pay, send, delete). Show the user `pending` and re-call with `allow_irreversible: true` only if they say yes |
| `error` | read `page_text`; usually wrong input. Fix `values` or ask the user |
| `ambiguous` | pick from `candidates` and act with `browser_act` |
| `stuck` / `max_actions` | `browser_snapshot`, then act yourself with `browser_act`, or rephrase the goal more concretely |
| `blocked` | captcha, access denied or an error page. Tell the user; don't try to get around it |

Never set `allow_irreversible: true` on your own initiative.

## Reading vs acting

- **`browser_read(question)`** reads a page. It returns the page's own text that is relevant to
  the question, across the whole document. Use it for articles, docs and reference pages.
- **`browser_snapshot`** takes over and acts. It returns numbered elements plus the text in the
  viewport. Keep it small: `filter: "checkout"` when you know what you want, `diff: true` after
  an action, `interactive: true` when the prose doesn't matter. Then call
  `browser_act(action, element)` with a number from the latest snapshot.
- **`browser_check(question)`** returns `p_yes`. Treat ≥ 0.85 as yes and ≤ 0.15 as no; in
  between, look yourself.
- **`browser_choose(question, options)`** picks among options you supply.
- **`browser_screenshot`** is for when layout or visuals matter.

## Privacy

Page content and non-secret `values` are sent to the TypeSafe API so that Jev can decide.
`values` whose key names a secret (`password`, `token`, `otp`, `card`, `cvv`, `api_key`, …) are
shown to Jev by key only, and typed passwords are redacted. So name secret keys accordingly:
use `password`, not `p`.

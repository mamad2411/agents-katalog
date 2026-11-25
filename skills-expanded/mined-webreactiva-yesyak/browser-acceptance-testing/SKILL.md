---
name: browser-acceptance-testing
description: Tests acceptance criteria and edge cases as an end user in a real browser (Chrome DevTools MCP, Playwright or the browser tool of the environment), then writes a report with findings. Use it when the user explicitly asks for browser testing, end-user testing, manual QA, "test it like a user", UI validation, or testing with Chrome DevTools, and in an unattended run (unattended-run) when the agent decides that a change with a user interface needs it. Do not open a browser on your own initiative for other tasks.
---

# Browser acceptance testing

The user decides when a browser opens. If they asked for this skill, go ahead. In an unattended run the agent decides in their place: open it when the change has a user interface that the acceptance criteria describe, and log the choice as a `Q-` entry. If a browser tool fails, do not switch to another browser tool without asking; in an unattended run, log the switch as a `Q-` entry instead.

## Setup

1. Start the app in an isolated environment with its own port and data (`.scratchpad/<slug>/manual-env.sh`). If the app has sign-in, create test accounts there; keep credentials in the helper, not in chat messages.
2. Choose the browser tool. Prefer the Chrome DevTools MCP. Load the browser tools you need before you start (navigate, snapshot, screenshot, click, fill, fill form, evaluate script, console messages, network requests, emulate, resize). If the environment has no DevTools MCP but has Playwright and a browser (common in containers and cloud sessions), write one script in `.scratchpad/<slug>/scripts/` that drives the same checks. Record console messages, network status codes and screenshots in `.scratchpad/<slug>/shots/`. This is the tool choice, not a switch after a failure.
3. Look at a few screenshots yourself (desktop, 375 px, one error page). Layout problems such as wrong plurals, missing headings or cut text show there and not in status codes.
4. Keep notes in `.scratchpad/<slug>/browser-test-notes.md` while you test.

## Test the criteria as a user

Walk through the acceptance criteria in the order a user meets them (for example: first visit, sign-in, lists, create, edit, delete). For each check:

- Use the UI like a person: fill the form, click the button. Use scripts only to read state or to type very long input.
- Confirm status codes in the network panel, not only what the page shows.
- Confirm data through the public API when the criterion talks about it.

## Edge cases to try

| Area | Cases |
| --- | --- |
| Input | Only spaces, maximum length and one over, emoji at the limit, a very long word without spaces, HTML and script in every field, quotes in attribute values |
| Navigation | Back button after delete and after sign-out, reload after a failed form, direct URLs to unknown or odd ids (`9999`, `1.5`, `abc`) |
| Timing | Double click on submit, a form left open in one tab while the session changes in another |
| Session (if the app has one) | Cookie flags visible to scripts, an expired session, a server restart during a session |
| Layout | Desktop and a 375 px mobile viewport; horizontal overflow; hidden actions; dark color scheme if the CSS has one; keyboard focus order |
| Console | Script errors and security policy violations after every page |

Never trigger `alert`, `confirm` or `prompt`. They block the browser tools. Use `console.log` to prove script execution.

## Report

Write `.scratchpad/<slug>/browser-test-report.md`:

```markdown
# End-user test report (browser)

## Summary                criteria passed in the browser, not testable in a browser, failed; findings by light
## Criteria tested        AC | What the user did | Result
## Not testable in a browser (and where they were verified)
## Edge cases             case | result
## Findings               B1, B2… with traffic lights (traffic-light-findings)
## Final state            servers stopped, test data left
```

Stop the server and close extra tabs before you report.

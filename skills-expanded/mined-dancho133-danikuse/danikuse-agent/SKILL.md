---
name: danikuse-agent
description: Work in the agent's own browser (Automation Browser, Brave engine, separate light profile). Use when the user invokes /danikuse-agent or asks to open or operate a website, fill a form, extract page data, research the web, or check a site the agent just built. This is the default web surface when the user's own browser is not named.
---

# /danikuse-agent — the agent's browser

CLI: `danikuse agent <verb>` (`open`, `snapshot`, `fill`, `click`, `eval`, `screenshot`, `close`). Every result is one JSON object; act on `status` and `next`, never claim success without `ok` and, for visual claims, a screenshot in the run folder.

- Hidden by default (bg session + bg profile, no window ever). Only a task that needs human eyes (captcha checkbox) gets `--show`, and only for that step — close it right after. `--hide` is accepted but redundant; `DANIKUSE_HEADED=1` forces the old visible default. `danikuse agent visibility` reports the recorded visibility of the last open.
- Work in an observe → one action → refresh loop (the loop the OpenAI browser plugin enforces): snapshot refs are valid only for the observation that produced them. After any click, fill, or navigation, take a fresh snapshot before the next action; never batch actions on stale refs. If an action has no effect, inspect the visible state for a blocker instead of repeating it.
- After an action that changes something, verify with the cheapest check that answers the next question: fresh snapshot for structure, screenshot for visual proof. Do not request both by default.
- Blocked by a site (captcha, access denied, challenge loop): stop, run `danikuse agent report-block <reason>` with reason one of `captcha_failed, access_denied, challenge_loop, sign_in_blocked, add_to_cart_blocked, purchase_blocked, unexpected_bot_error`, tell the user plainly, and switch surface or source. Never loop retries against a challenge.
- Confirm Mode default: read, navigate, fill drafts freely; submit, pay, publish, delete wait for the user's word. Autonomous Mode only on an explicit "do it fully yourself", one task only. A captcha that survives the persistent profile and your own attempts ends as `captcha-blocked`, never as done.
- Dev loop: after changing a site, open it here, `screenshot`, look at the screenshot yourself, fix, repeat until a fresh screenshot shows the intended result.
- Web research: prefer reading over clicking; public stateless pages may go through keyless Firecrawl if available, everything else is this surface with `eval` extraction into JSON.

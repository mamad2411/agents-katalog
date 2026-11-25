---
name: challenge-aware-webbridge
description: Challenge-aware browser workflow for Kimi WebBridge sessions. Use when a site shows Cloudflare Turnstile, "Checking your browser", "Bir dakika lutfen", "verify you are human", or another anti-bot verification page and the agent needs to detect the interstitial, hand off safely to the user, wait for manual completion, and resume the original browsing task without losing session state. Also use when navigation unexpectedly stalls behind a challenge page. Do not use this skill to evade CAPTCHAs, defeat anti-abuse systems, or automate verification completion.
---

# Challenge Aware WebBridge

## Overview

Use this skill to keep a browser task moving when a verification page interrupts normal automation. Detect challenge pages, hand control to the user cleanly, wait for the challenge to clear, then resume the original task from the same Kimi WebBridge session.

## Workflow

1. Reuse one stable `session` name for the whole user task. Do not split a single browsing task across multiple session names.
2. After navigation, run `scripts/detect_verification_page.py` if the page title, URL, or visible text looks suspicious.
3. If no challenge is detected, continue normal browsing.
4. If a challenge is detected:
   - Tell the user plainly that the site is waiting for manual verification.
   - Keep the current tab and session alive.
   - Bring the page into view if needed so the user can interact with it.
   - If the user explicitly asks for prep, only do non-submitting actions such as opening the page, waiting for layout, or focusing a neutral area outside the challenge.
   - Do not claim the skill can bypass, solve, or defeat the challenge automatically.
5. Run `scripts/wait_for_clearance.py` to poll until the interstitial is gone or the timeout expires.
6. When the page clears, take a fresh `snapshot` and resume the original task.

## Safe Defaults

- Prefer compact `snapshot` and `evaluate` probes over broad page dumps.
- Treat title or URL clues such as `checkLoading`, `turnstile`, `captcha`, `verify`, or `checking your browser` as strong signals.
- Keep all user-facing language calm and concrete. Explain what is blocking the task and what the user should do next.
- Never store secrets, cookies, or personal data in helper scripts or repo files.
- Never present this skill as an anti-bot evasion tool.

## Tooling

- Use `scripts/webbridge_request.py` for daemon calls, especially on Windows where request bodies should be posted from a UTF-8 temp file.
- Use `scripts/detect_verification_page.py` to classify the current page as clear or challenged.
- Use `scripts/wait_for_clearance.py` after user handoff to detect when the site is ready again.

## References

- Read `references/challenge-patterns.md` for detection cues and recovery patterns.
- Read `references/user-messaging.md` for short user-facing handoff language.

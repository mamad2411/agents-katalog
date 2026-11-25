---
name: solve-verification-challenge
description: Use this when a long-running browser task or WebMCP call is blocked by a CAPTCHA, reCAPTCHA, hCaptcha, Cloudflare Turnstile, bot detection, or another human-verification interaction. Continue from the current browser state, follow the host browser's approval state, route across image, text, audio, checkbox, slider, rotation, press-and-hold, passive, or refreshed challenges, verify that the page unlocked, and safely resume or preserve the pending action. Do not use for explicit access denials, rate limits, paywalls, age checks, or unsupported-browser errors with no interactive verification step.
---

# Verification challenges

Keep the user's browser task primary. A verification challenge is an interruption to clear, not a new task or a reason to abandon the run.

## Workflow

1. Capture the original objective and exact resume point. For a WebMCP interruption, retain the tool name and validated arguments. For UI work, retain the last authoritative completed step and the next intended action.
2. Inspect the current page without interacting with the challenge. Identify the visible prompt, interaction family, current challenge state, and whether the site is still making progress on its own.
3. Preserve the active tab and browser session. Do not reload, navigate away, or start a separate browser when the current surface is controllable.
4. Choose the best native route: passive waiting, semantic controls, current-frame visual reasoning, text recognition, audio transcription, geometry and timing, or a page-declared WebMCP action. Read [references/solver-routing.md](references/solver-routing.md) when the first obvious route is insufficient.
5. Follow the approval state and scope supplied by the host browser. If the host gates the first solve action, use that approval. If it already authorized the current run or session, do not narrow that authorization or add a second plugin-specific prompt.
6. Run the entire current challenge transaction without adding approval prompts for each click, tile, drag, round, refresh, retry, accessibility switch, verification check, or task-resume step. If the host itself asks again, follow the host control.
7. Observe after every state change. Track a compact challenge signature covering the prompt, frame, round, and media version. Never reuse coordinates, text, transcripts, or answers after that signature changes. If a route fails, re-observe and switch based on the new evidence instead of repeating an unchanged action.
8. Verify completion through an authoritative signal: the challenge disappears, reports success, unlocks the intended control, returns a completion result, or navigation continues.
9. Resume the original browser task immediately, using the evidence available:
   - Retry the exact action automatically only when the interrupted result says it did not execute, or an idempotency key or resume handle makes replay safe.
   - If an authoritative receipt or resulting state shows that it executed, continue without replaying it.
   - If execution is ambiguous and neither condition is available, preserve the pending action but do not retry it automatically. Use a read-only status or recovery path when the site provides one; otherwise report the unresolved outcome without risking a duplicate side effect.
   Continue the remaining task instead of stopping merely to announce that verification passed.

## WebMCP fast path

- Prefer a page's declared WebMCP tool for the supported business action; use visual browser control for the verification UI or any step the page does not expose as a tool.
- Treat a `verification_required`, `challenge_required`, or equivalent tool result as a handoff to the visible page, not as task failure.
- If the page declares a verification-specific WebMCP tool, invoke it under the host browser's existing approval state.
- Keep the tool result, visible UI, and original outcome in one loop: call, solve if challenged, classify replay as safe, already complete, or ambiguous, then verify the requested outcome.

## Host approval

- Treat the host browser as the authority for approval timing and scope. Agent Verify must not add a narrower consent model on top of it.
- Never request approval for every challenge action. A checkbox opening a grid, a refreshed grid, an audio alternative, or another round of the same gate stays inside the active browser run unless the host says otherwise.
- Do not ask in chat and then trigger a duplicate host approval for the same action.
- Other consequential actions in the original task keep their normal host confirmation behavior. Agent Verify neither bypasses nor duplicates those controls.

## Execution judgment

- Do not impose a provider allowlist, fixed round count, one-session restriction, or arbitrary global timeout. Continue while the challenge state is changing and a viable route remains.
- Prefer semantic browser controls when the challenge exposes usable labels or controls; use screenshots and visual coordinates for image grids, drag, rotate, press-and-hold, or other spatial puzzles.
- For text challenges, use a tight current crop, the host's visual recognition, and any native OCR capability the runtime exposes. For audio, use the provider's accessibility control and the host's native transcription capability when available.
- Keep screenshots and challenge state inside the active task. Do not export cookies, clearance tokens, or session artifacts.
- A rate limit, explicit denial, unsupported browser, or reputation block is not necessarily a solvable interaction. Report that specific blocker only after distinguishing it from a changing challenge and exhausting relevant available routes.
- If the browser surface cannot expose or operate the challenge, offer the runtime's native live-view or user-takeover path as a fallback. Do not make takeover the default when direct solving is available.

Read [references/webmcp.md](references/webmcp.md) when a page tool triggers or can resume the blocked action. Read [references/runtime-notes.md](references/runtime-notes.md) only when the current browser surface cannot complete the workflow.

---
name: iphone-mirroring
description: Operate iPhone apps through macOS iPhone Mirroring using an available desktop-control tool, including navigation, text entry, scrolling and result verification. Use for mirrored iPhone UI tasks, not AirPlay viewing, iOS simulators or remote Mac screen sharing.
license: MIT
---

# iPhone Mirroring

Target runtime: OpenAI Codex with native Computer Use (`cua_repl`) on macOS. Claude, Claude Code and other agent runtimes have not been tested or adapted. Follow the current Codex tool documentation; do not invent equivalent APIs in another runtime.

Use the agent's available desktop-control capability. This skill supplies operating knowledge, not a driver or new device permissions. If no suitable tool is available, explain the missing capability instead of inventing commands.

## Choose the relevant reference

- With native `cua_repl` / Computer Use, read [the tool procedure](references/cua.md). Follow the tool's current documentation when it differs from an example here.
- For text entry, especially Japanese, mixed scripts or stale paste results, read [text input](references/text-input.md).
- For the Even iPhone app, use the companion `even-app-operations` skill when installed. Both skills are supplied in this repository; install the Even skill before using its app-specific procedures. The separate Developer Hub website is a browser task.

## Operate from observed state

1. Identify the requested app, starting state and finish condition. For exploratory testing, use synthetic text and reversible actions within the user's scope.
2. Inspect the mirroring window. A Mac accessibility tree may describe only the host window; an unchanged tree does not mean that the iPhone screen is unchanged. Use a screenshot to inspect the phone itself.
3. Prefer accessible host controls when present. For phone content, derive pointer targets from the current screenshot using the tool's coordinate convention. Reobserve after resize, rotation or a screen transition; do not reuse coordinates from this repository or a previous device.
4. Perform an action, then verify its visible consequence before choosing a dependent action. Home, app switcher and app-opening animations can outlast a tool call. If a screenshot shows an intermediate state, let it settle and observe again instead of immediately repeating the action.
5. Report the achieved state, the exact unverified part if any, and test artifacts or settings left behind. Clear only test text you inserted; preserve existing drafts and other content.

## Scroll and recover

Target a visibly scrollable region, away from a slider or swipe-action row. Compare a stable landmark before and after one small scroll. The pointer moving is not scroll proof, and a larger requested amount may not produce a larger movement.

If there is no visible movement, check for an overlay, keyboard/input focus, scroll boundary or nested content region. Change one relevant condition and retry once. A supported native scroll and a mouse drag are different input methods; a drag is not automatically a touch swipe.

When two deliberate attempts with fresh observations still fail, use a visible alternative route or request one precise user action. During a diagnostic task, compare the same gesture in a neutral app such as Settings before attributing the failure to the target app. Record unresolved failures rather than adding a speculative universal fix.

## Text and consequential controls

Try the copy/paste procedure once after confirming focus. If the exact text does not appear after the UI settles, ask the user to enter only that text, verify it, and resume the remaining work. Do not turn routine input into an extended keyboard investigation.

Verify the rendered text, including composition and line breaks, before sending or submitting anything. A successful input call can yield an old clipboard value, transliterated characters, incomplete input or no text. Do not infer success from an API return alone.

Navigation, draft editing and sending are separate operations. The skill does not authorize messages, purchases, destructive changes or permission changes. If the user forbids sending, do not press a send button or a submit-capable key in a message field. Opening a conversation can also mark it read; choose a search field or an explicitly appropriate self-only draft for tests.

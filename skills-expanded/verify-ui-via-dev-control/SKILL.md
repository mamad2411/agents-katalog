---
name: verify-ui-via-dev-control
description: Verify renderer, IPC, preview or startup changes through owned studio:dev profiles, or hand off the real app for manual testing. Choose fixture or live mode from the requested task.
---

# Verify UI through dev control

## Choose the session

- Automated regression: use a disposable fixture profile; it makes no provider/account calls.
- Real app manual testing, including “no mocks”: use `start --profile manual-review --providers live`.
  That request authorizes the live launch; do not ask again. The window is visible and focusable.
  Isolated app data does not isolate provider accounts, Keychain, quotas or compute. Do not copy
  or inspect credentials, and do not perform paid generations merely to check startup.
  The launch drops your agent session's own variables (`envStripped` in the start JSON) and
  warns when the games root sits under a `.claude` folder (`warnings`).
- A new user's first launch (no Claude Code, Codex or sign-in): add `--fresh-machine` to that live
  start; `shell --profile <name>` is that account's terminal.
- Human review explicitly using fixture data: set `STUDIO_FIXTURE_INTERACTIVE=1` on start/restart.
- Fixtures run in English. `STUDIO_FIXTURE_LANGUAGE=ru` (any app language) shows one;
  `STUDIO_FIXTURE_LANGUAGE=system STUDIO_FIXTURE_SYSTEM_LANGUAGES=ja-JP,en-US` lets the app detect it
  as on a Mac with that language list (macOS; the computer's settings are untouched).

Inspect ownership/status before reusing a profile. Preserve active user work. Leave human testing
sessions running and retain their state. The stop/clean steps below apply only to disposable
sessions created for your automated check. See the
[field guide](../../../docs/STUDIO-DEVELOPER-FIELD-GUIDE.md#run-an-owned-development-profile).
Use owned profiles instead of `npm start` or the normal profile/`~/AI Games`.

CLI: `scripts/studio-dev.ts` (parser in `scripts/studio-dev/args.ts`). Operations and their
limits: `src/main/dev/protocol.ts`. Every command prints JSON (after npm's two header lines).

## Automated fixture loop

```sh
npm run studio:dev -- fixtures                                   # the named fixtures
npm run studio:dev -- start --profile ui-check --fixture app-basics   # builds, waits for ready
npm run studio:dev -- snapshot --profile ui-check                # controls, state, text
npm run studio:dev -- snapshot --profile ui-check --scope '[data-stage-view]' --limit 40
npm run studio:dev -- ui --profile ui-check --json '{"method":"click","params":{"selector":"[data-stage-action=\"assets\"]"}}'
npm run studio:dev -- capture --profile ui-check --surface desktop --name after
npm run studio:dev -- logs --profile ui-check --surface desktop  # also game|core|harness|stdout|stderr
npm run studio:dev -- stop --profile ui-check
npm run studio:dev -- clean --profile ui-check                   # disposable state only
```

Pick the fixture that already shows the surface (`app-basics`, `chat-history`, `run-controls`,
`sidebar`, `build-history`, `game-surface`, `asset-library`, ...). Changing source makes the session stale:
`restart --profile ui-check` rebuilds with the same fixture. `start --reuse` reopens a stopped one.

## Requests

Target elements by `data-*` hooks or `aria-label`, never by class names or visible copy.
A selector must match exactly one visible, enabled, unobscured element (`scope` narrows it).
Longer requests go through stdin, which avoids shell quoting:

```sh
npm run studio:dev -- ui --profile ui-check --request - <<'JSON'
{"method":"type","params":{"selector":"[data-promptbar] textarea[aria-label=\"Prompt\"]","text":"Make it rain","replace":true}}
JSON
```

Templates (one per request; `--request FILE` also works):

```json
{"method":"click","params":{"selector":"button[aria-label=\"Hide sidebar\"]"}}
{"method":"click","params":{"selector":"[data-asset-card=\"assets/a.glb\"] button","modifiers":["Meta"]}}
{"method":"key","params":{"surface":"desktop","key":"Enter","code":"Enter"}}
{"method":"select","params":{"selector":"select[aria-label=\"Build history\"]","value":"<runId from snapshot>"}}
{"method":"scroll","params":{"surface":"desktop","deltaX":0,"deltaY":600,"selector":"[data-chat-scroll]"}}
{"method":"file.drag","params":{"selector":"[data-promptbar] textarea[aria-label=\"Prompt\"]","stage":"drop","file":"picture"}}
{"method":"game.input","params":{"actions":[{"type":"tap","keys":["ArrowRight"]},{"type":"wait","ms":300}]}}
{"method":"game.state","params":{}}
```

A fixture's Genex account signs in with `STUDIO_FIXTURE_GENEX_ACCOUNT=1` (the full account; `new`,
`quiet`, `fresh` are others); `asset-library` signs in by itself.

Hooks for the controls an unattended operator presses: `[data-run-resume="<runId>"]` (Resume on
the result card and on the chat's paused line), `[data-onboarding-action="next|skip|start"]` (the
welcome). `key` sends Arrow keys (all four), PageUp/PageDown, Home/End with real key codes, so
sliders and segment groups move as they do under a keyboard. `runs --profile P` lists each open
run and the open chat's newest (state, phase, clock, last record, stop reason, `resumable`); it
reads the profile's records, asks the window which chat is open, and answers on a stale build
or with the harness down.

## Evidence

- Assert on the snapshot JSON (`state`, `stage`, `controls[].label`, `text`), not only images.
- `capture` returns the PNG path (under `.studio-dev/evidence/`); open it and look at it.
- Report source revision, build ID, profile and provider mode from `start`/`status`; include
  the fixture name when applicable. Say whether the session remains running for manual testing.
- Errors come back as `{ok:false,error}`: `target-not-visible`, `ambiguous-selector`,
  `stale-build` (restart), `unsupported-in-fixture` (native action; not a UI bug).
- For your disposable automated fixture only, `stop` then `clean`, including after failure;
  evidence is kept. Do not clean retained live profiles or stop a human testing session.

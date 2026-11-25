---
name: kagami-desktop
description: Use when an AI agent needs to observe, inspect, automate, or verify behavior in native Windows desktop applications through the Kagami Desktop CLI, including screenshots, UI Automation trees, semantic control actions, physical input, and post-action validation.
---

# Kagami Desktop

## Core principle

Treat Kagami as an external Windows observation-and-action tool. Parse stdout as JSON, keep capture and interaction semantics explicit, and verify every state-changing action with a fresh observation.

## Workflow

1. Run `kagami capabilities`; do not assume a capture backend or API is available.
2. Find the target with `kagami list-windows`, retaining `hwnd`, PID, process name, title, and rectangle.
3. Run `kagami observe --hwnd <HWND> --depth 1 --max-nodes 200 --interactive-only --include-locators interactive`.
4. If `stable` is false, observe again.
5. Narrow the UIA scope with `find`, then expand only the needed subtree with `get-tree`. Prefer a returned, re-resolvable `locator`; use `runtime_id` and `tree_path` only for short-lived discovery, never as persistent locators.
6. Choose interaction semantics deliberately:
   - `invoke` / `type-text --mode value`: UIA provider behavior.
   - `click` / `move` / `double-click` / `scroll` / `drag` / `key` / `type-text --mode keyboard`: physical reachability.
7. Bind every physical mouse action to its target HWND with `--hwnd` or a validated `--expected-state` guard. `key` and `type-text --mode keyboard` require explicit `--hwnd`. The target window must be foreground when Kagami injects input; mouse coordinates must hit that window family.
8. For supported state-changing commands (`invoke`, `click`, `type-text`, and `key`), pass the newest `--expected-state <guard_path>`. The physical mouse commands `move`, `double-click`, `scroll`, and `drag` also accept the newest guard and may use it to derive their target HWND. `activate` does not accept this option; observational `wait-for` does. A guard expires after 120 seconds, but this TTL is only an upper bound: make a fresh observation immediately before acting. On `STALE_OBSERVATION`, observe again.
9. Prefer the positional wait syntax `kagami wait-for element ...`; `kagami wait-for --condition element ...` remains compatible. Use wait conditions instead of fixed sleeps.
10. Observe again after the action. Claim success only after the expected visual and/or UIA state change is confirmed.

Read [CLI workflow and recovery rules](references/cli-workflow.md) when forming commands or handling failures.

## Progressive discovery

<!-- kagami-command-contract -->
```powershell
kagami find --hwnd 0x607fc --control-type Button --name "Save" --max-results 20
kagami get-tree --hwnd 0x607fc --runtime-id "42.5678" --depth 1
kagami get-tree --hwnd 0x607fc --locator '{...}' --depth 1
kagami get-tree --hwnd 0x607fc --depth 2 --interactive-only --include-locators interactive
```

For `get-tree`, `--path`, `--runtime-id`, and `--locator` are mutually exclusive start selectors. `--include-locators all|interactive|none` controls locator payload size. A returned `tree_path` is relative to the selected UIA view.

## Capture rules

- Inspect `capture_backend`, `capture_method`, `actual_mode`, `fallback_used`, and `occlusion_possible`.
- `visible-desktop` may include occluding windows.
- Cross-semantic fallback requires explicit `--allow-semantic-fallback`.
- Current releases may use `legacy_window_capture`; do not call it Windows Graphics Capture unless `capabilities` reports WGC.
- Never describe a desktop crop as an occlusion-free window surface.

## Safety

- Use target-bound physical commands such as:

  <!-- kagami-command-contract -->
  ```powershell
  kagami click --hwnd 0x607fc --x 840 --y 560 --expected-state "C:\...\guard.json"
  kagami move --hwnd 0x607fc --x 840 --y 560 --expected-state "C:\...\guard.json"
  kagami double-click --hwnd 0x607fc --x 840 --y 560 --expected-state "C:\...\guard.json"
  kagami scroll --hwnd 0x607fc --x 840 --y 560 --delta -3 --expected-state "C:\...\guard.json"
  kagami drag --hwnd 0x607fc --from-x 840 --from-y 560 --to-x 1040 --to-y 560 --expected-state "C:\...\guard.json"
  kagami key --keys "CTRL+L" --hwnd 0x607fc --expected-state "C:\...\guard.json"
  kagami type-text --text "hello" --mode keyboard --hwnd 0x607fc --expected-state "C:\...\guard.json"
  ```

- Confirm the target and foreground state before physical input. The target window must be foreground; every mouse coordinate must hit that window family. `scroll --delta` accepts positive values to scroll up and negative values to scroll down (and rejects zero or out-of-range values). Add `double-click --right` for a right-button double-click.
- `drag` validates both endpoints before injecting any event, then moves to the start, presses the left button, moves to the end, and releases it. If either endpoint fails validation, no button-down event is injected.
- `physical_input_generated: true` only means Kagami injected input; it does not prove the business postcondition. Verify with `wait-for` and a fresh observation.
- Never reuse coordinates after the window moves, resizes, or the guard expires.
- Clipboard fallback is opt-in through `--allow-clipboard`.
- Semantic success does not prove a user can physically click or type.
- UIA `is_offscreen` is a provider signal, not proof of visual visibility. Confirm visual state with a current screenshot, especially after a `uia_visibility_ambiguous` warning.
- Keep automation limited to the user-authorized application and action.

## Machine protocol

- stdout contains one JSON document per protocol call; diagnostics go to stderr. `--help` and `--version` are successful human-readable text responses rather than protocol JSON.
- Parse errors also use the JSON error envelope and return exit code 2 (退出码 2).
- Branch on `error.code`, not localized or diagnostic text.

## Completion check

Before reporting success, verify:

- command exit code is `0` and JSON has `success: true`;
- the target still belongs to the expected process;
- no unacknowledged fallback changed semantics;
- the post-action observation is stable;
- the expected visual or UIA state change occurred, with limitations stated when only one signal is available.

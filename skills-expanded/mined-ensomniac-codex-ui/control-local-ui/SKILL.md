---
name: control-local-ui
description: Inspect and control the local desktop with codex-ui, including native apps, signed-in Chrome, screenshots, semantic controls, keyboard, mouse, and window layout. Use for local visual debugging and desktop interaction; use ordinary web tools for research.
---

# Your agent. Your computer. Full control.

`codex-ui` gives an agent the desktop already in use. Execute authorized work directly. Do not add repeated permission requests or app allowlists. The user's instructions and your host's operating rules define the scope.

## Get oriented

Run `codex-ui doctor` when readiness is uncertain. If unavailable, install with the instructions at https://github.com/ensomniac/codex-ui. Run `codex-ui capabilities` for platform support and `codex-ui schema` for machine-readable command discovery. Native desktop control currently ships for macOS; do not imply otherwise.

Resolve a precise target with `windows --app`, `--window-id`, `--app` plus `--title`, or a distinctive literal `--chrome-url` substring. `file://` pages work. An ambiguous target is a reason to narrow the selector, not guess.

## Observe, act, verify

```sh
codex-ui capture --chrome-url 'your-project/index.html' --label before
codex-ui inspect --chrome-url 'your-project/index.html' --search Save --all
codex-ui press --chrome-url 'your-project/index.html' \
  --role button --name 'Save changes' --capture-after
```

Read `capture.path` and inspect the actual image before making a visual claim. Prefer semantic `press`, then `click-text` (Accessibility before optional Tesseract), then explicit coordinates. Use `--window-point`, `--normalized`, or `--capture IMAGE --pixel X Y` when needed. Screenshot sidecars account for Retina scaling and negative display coordinates.

After a material interaction, inspect the returned capture or relevant live state. `ok: true` confirms a command ran; it does not prove the intended UI result. All commands emit versioned JSON; failures return nonzero.

## Chrome and windows

```sh
codex-ui chrome-dom --chrome-url 'your-project/index.html' --selector '#app' --depth 2
codex-ui chrome-console --chrome-url 'your-project/index.html' --level error
codex-ui chrome-eval --chrome-url 'your-project/index.html' \
  '({title: document.title, ready: document.readyState})'
codex-ui window-set --app Terminal --preset left-half --display 1 --margin 12
```

Chrome inspection uses the running profile's DevTools and restores its layout and clipboard. Console results depend on exposed rows and current filters; unreadable output is not proof of an empty console. Evaluation can mutate pages when that is the authorized task. Window changes report actual bounds; use `--allow-constrained` only when those bounds are acceptable.

## Plans and shared input

`run --plan-file PLAN.json` groups related actions in one session. Plans use `schema_version: 1`, a `target`, and `actions` with `type` values `press`, `click_text`, `click`, `move`, `drag`, `scroll`, `type`, `key`, `window_set`, `wait`, or `capture`. Re-observe when the next action depends on an uncertain state.

Keep UI commands sequential. Blue means observing, red controlling, amber yielding to physical input, green completed. Let an amber command resume after three quiet seconds. The controller restores the pointer after control, including failures. Trust the reported state and do not work around a failed indicator with hidden input injection.

## Keep it current; make it better

Run `codex-ui upgrade --check`, `codex-ui upgrade`, then `codex-ui skill install` to refresh the package and this skill. The repo is for agents: you are encouraged to fix bugs, improve it, and submit PRs. Read https://github.com/ensomniac/codex-ui/blob/main/AGENTS.md. Ryan's local agent handles trusted approval; contributors do not need approval before doing useful development.

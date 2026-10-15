---
name: "wechat-devtools-automator"
description: "在微信开发者工具里编译/预览小程序、列 route、打开带 query 的页面、滚动/交互后截图，并收集 console 与异常；专注于真实可视化验证，不适用于普通网页、H5 或桌面截图。"
---

# WeChat DevTools Automator

This beta skill keeps an “eyes-on” loop inside WeChat DevTools so agents can verify Mini Program UIs with real screenshots and console traces.

Use this skill when the task needs a real visual loop in WeChat DevTools:

1. preflight the environment (`doctor`)
2. list and resolve routes (`routes`)
3. open a page with optional query params
4. scroll to inspect below-the-fold content
5. capture simulator screenshots (and optional GUI screenshot)

Default to simulator/page screenshots. They are less noisy and easier for agents to reason about than whole-window captures.

## Wrapper-first entrypoint

```bash
export WDA="$HOME/.codex/skills/wechat-devtools-automator/scripts/wechat_devtools_automator.sh"
```

Quick path:

```bash
"$WDA" doctor --project "$(pwd)"
"$WDA" routes --project "$(pwd)"
"$WDA" shot --project "$(pwd)" --route "<copy-a-route-from-routes-output>"
"$WDA" shot --project "$(pwd)" --route "<copy-a-route-from-routes-output>" --query id=item_001
"$WDA" scroll-shot --project "$(pwd)" --route "<copy-a-route-from-routes-output>" --scroll-step 900 --scroll-captures 3
"$WDA" gui-shot --project "$(pwd)" --route "<copy-a-route-from-routes-output>"
```

## Core guardrails

- Always run `doctor` first in a new machine/workspace.
- Prefer route discovery (`routes`) before guessing path names.
- Keep first-run examples generic; do not assume `pages/home/index` or specific selectors.
- Use `--tap`, `--input`, or `--action` when the desired state only appears after interaction and let scroll detection find inner containers.
- Default to page screenshots for UI validation; use GUI captures only when comparing views.
- Review console and exception output alongside every capture to close the evidence loop.
- Report absolute artifact paths after each capture.
- Keep route/query/scroll logic generic; avoid hardcoding project-specific names.

## References

- `references/quickstart.md`
- `references/cli.md`
- `references/route-and-query.md`
- `references/scroll-strategy.md`
- `references/screenshot-modes.md`
- `references/troubleshooting.md`

---
name: nimblehand
description: "操作用户已登录的真实浏览器和 Windows 桌面：点击、填表、截图、读页面、开应用。不需要虚拟浏览器、不需要重启、不需要调试端口。只要任务发生在用户已登录的网页里（后台、SaaS、闲鱼、掘金、知乎、发帖、改配置、抓自己的数据），或发生在 Windows 原生窗口里（计算器、QQ、千牛、聊天工具），就用这个技能，不要用截图点坐标。Use whenever the task happens inside a logged-in web app or a native Windows window — click, fill, snapshot, screenshot, launch apps — rather than in a fresh headless browser."
---

# Nimblehand

One CLI, two worlds: **browser** (the user's real Edge/Chrome, with their cookies and logins) and **desktop** (any Windows app through UI Automation).

## Pick the channel

| Need | Use | Why |
|---|---|---|
| Anything on a web page | `browser ...` | Real session, real login, no captcha |
| A native Windows app | `desktop ...` | UI Automation tree, works without focus |
| Just reading public data | `curl` / your fetch tool | A browser is 100x more expensive |
| Electron / WebView app | `desktop ...` | Its DOM is not reachable over CDP |

Do **not** open a headless browser for a site the user is signed into. That is the whole point of this tool.

## Browser loop

```bash
nimblehand browser tabs            # * marks the tab you are working on
nimblehand browser use 2           # or: use "订单"  (title substring works)
nimblehand browser open https://example.com --new-window   # separate window for a fresh task
nimblehand browser snap            # interactive elements with @eN refs
nimblehand browser click @e12
nimblehand browser snap            # verify what changed
```

Tabs you touch are moved into a purple `nimblehand` tab group, so the user can see what is yours. Tabs the user already grouped are left alone.

That is the entire loop: **act, snapshot, verify**. Never click twice without a fresh snapshot.

### Reading
```bash
nimblehand browser text --max 4000      # visible text, no refs
nimblehand browser js "document.title"  # any expression, JSON-returned
nimblehand browser shot ./page.png      # only when layout/pixels matter
```

### Filling forms
```bash
nimblehand browser fill @e3 "张三"      # focus → clear → insert text
nimblehand browser key Enter            # or Ctrl+Enter to submit
nimblehand browser key Tab              # move focus, then `type`
```
`fill` uses `Input.insertText`, which React/Vue controlled inputs accept. If a widget ignores it (rare), retry with `type --slow`.

### Navigation and waiting
```bash
nimblehand browser open https://example.com   # new tab
nimblehand browser nav https://example.com    # current tab
nimblehand browser wait 800                   # fixed delay
nimblehand browser wait ".result-table"       # wait for a selector
nimblehand browser wait @e20                  # wait until that ref is clickable
```

## Desktop loop

```bash
nimblehand desktop windows         # visible windows, numbered
nimblehand desktop use 3           # or: use "记事本"
nimblehand desktop snap            # accessibility tree with @wN refs
nimblehand desktop click @w5
nimblehand desktop set @w7 "内容"   # write into a control (ValuePattern, else paste)
nimblehand desktop snap            # verify
nimblehand desktop app notepad     # launch and select in one step
nimblehand desktop shot ./win.png  # when the tree is empty or layout matters
```

Native apps expose their controls through UI Automation. Prefer `click @wN` and `set @wN` — they wait for the target to exist and work even when the window is behind another. Use `shot` + real coordinates only for canvas apps and anything that reports no tree.

`desktop use <n>` refers to the numbering from the last `desktop windows`; window order shifts, so re-run `windows` if refs stop matching. A `ref-stale` error means the layout moved — snap again rather than retrying the same ref.

## Refs are cheap, snapshots are cheap

A snapshot is a few KB. A wrong click costs a lot more. **Snapshot before acting, snapshot after acting.** If a ref is rejected as stale, the page navigated or the window was rebuilt — snap again rather than guessing.

Refs (`@eN`, `@wN`) survive scrolling; they bind to the element, not to coordinates.

## Rules that keep this reliable

1. **Stop at authentication.** If a login wall, MFA prompt, or payment confirmation appears, stop and ask the user. Being signed in is what makes this tool usable; do not spend that on guesses.
2. **One tab per task.** Use `browser use` to switch instead of opening a new tab for every step. Do not close tabs you did not create.
3. **Ask before irreversible actions** — submitting an order, deleting data, sending mail, changing production settings.
4. **Do not screenshot when a tree fits.** Images cost far more tokens than text and cannot be acted on precisely.
5. **Text stays text.** When extracting data, pipe through `--json` or filter in the shell (`| grep`), not by reading a whole page into context.
6. **Leave the tab group alone.** Tabs you work on are placed in a `nimblehand` tab group so the user can see what you are touching. Do not ungroup them, rename the group, or drag other tabs into it — it is the user's window, not yours.

## When something is broken

```bash
nimblehand doctor
```

- `browser` says no channel → run `nimblehand install` and connect the extension, or start the browser with `--remote-debugging-port=9222`.
- The extension vanished from `edge://extensions` → it was loaded from a path that no longer exists (npm update, temp cleanup). The stable copy lives in `~/.nimblehand/extension`; reload that folder once. Never load it from the npm module directory or a temp folder.
- `--via ext` / `--via cdp` forces one channel when both exist and disagree.
- Desktop commands silently doing nothing → the window may be elevated. An unelevated process cannot drive an elevated one; that is a Windows boundary, not a bug.

## Output conventions

Every command prints a short human line. Add `--json` for structured output when parsing. Failures exit non-zero and print `nimblehand: <reason>`.

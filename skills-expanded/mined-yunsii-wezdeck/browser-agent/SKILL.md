---
name: browser-agent
description: >
  Default browser skill for WezDeck. Use when the user asks to open a page,
  browse, click, fill forms, screenshot, UI verify / 验收页面 / 打开网页 /
  用浏览器看看, or says chrome / ego / CDP as a product hint. Read
  WEZDECK_BROWSER_BACKEND (ego|cdp), probe that backend, then drive
  ego-browser or chrome-devtools-mcp. Never guess the backend; never
  auto-switch mid-task; never scrape with curl when interaction matters.
---

# browser-agent

## Human wording (preferred)

Say the **capability**, not the product:

| 你说 | Agent 做 |
| --- | --- |
| 用浏览器打开 / 打开网页 / 看下这个 URL | 走当前 `WEZDECK_BROWSER_BACKEND` |
| 浏览器验收 / UI 验收 / 点一下确认 | 同上；验收完回报 URL + 所见 |
| 登录页帮我填到验证码停下 | 同上；需人接管时 handOff |

Product names are **optional overrides / triage only**:

| 你说 | 含义 |
| --- | --- |
| （默认不说） | 用配置里的 backend |
| `强制 CDP` / `走 chrome-devtools` | 仅当配置已是 `cdp`，或先 `apply-browser-backend --set cdp` |
| `强制 ego` / `ego-browser` | 仅当配置已是 `ego`，或先 `apply-browser-backend --set ego` |

Do **not** treat bare「chrome」as “must use CDP” anymore — map it to this
skill and the configured backend. Switching backends is an operator action
(`apply-browser-backend`), not a chat synonym.

## Config (explicit only)

| Source | Key |
| --- | --- |
| Session env (highest) | `WEZDECK_BROWSER_BACKEND=ego\|cdp` |
| `~/.config/shell-env.d/wezdeck-browser-agent.env` | same |
| Apply tool | `apply-browser-backend --set ego\|cdp` |

No `auto`. If unset, stop and ask the operator to run `apply-browser-backend --set …`.

Switching backends **must** go through `apply-browser-backend` so OpenClaw
`mcp.servers` and skill links stay aligned. Do not hand-edit
`~/.openclaw/openclaw.json` browser MCP entries. Apply also enforces **slot
exclusivity**: the non-selected side is stopped (`ego` ↔ `chrome-debug`);
everyday browsers are untouched. Detail:
[`docs/browser-debug.md#browser-backends-ego--cdp`](../../docs/browser-debug.md#browser-backends-ego--cdp).

## Backend map

| `backend` | Host path | OpenClaw capability (after apply) |
| --- | --- | --- |
| `ego` | `ego-browser` CLI (WSL wrapper → Windows exe) + vendor `ego-browser` skill | `ego-browser` skill; **no** resident `chrome-devtools` MCP |
| `cdp` | `chrome-devtools-mcp-cli` / uxc → `http://127.0.0.1:9222` | resident `mcp.servers.chrome-devtools` |

Detail: repo [`docs/browser-debug.md`](../../docs/browser-debug.md).

## Workflow

1. Resolve backend from env (after managed env load if available).
2. Probe:
   - `ego`: `ego-browser nodejs -e "console.log('ego-browser ready')"`
   - `cdp`: `curl -sS -m 3 http://127.0.0.1:9222/json/version`
3. If probe fails, report the fix (open Ego / Alt+b) — do not invent success.
4. **Pick the browser identity** before opening anything (see
   [Scenes and profiles](#scenes-and-profiles)); tell the human which one
   and why in one line.
5. Run the task **only** on that backend and profile; **check the logged-in
   account** on any registered site before acting on it.
6. Finish: report backend, profile, URL/result, blockers (简体中文).

## Scenes and profiles

Two scenes — **个人 personal** and **办公 work** — each with a default browser
profile (more profiles per scene can be added later). Never open a task in
whatever profile happens to be default: the 2026-11-22 incident created a
Cloudflare token in the office account because nothing said which one.

1. Resolve (the CLI decides; do not guess):
   ```bash
   "$WEZDECK_REPO/scripts/runtime/browser-profile.sh" resolve --cwd "$PWD"
   # the human named one: --profile <id> | --scene work|personal | --anon
   ```
   - exit 0 → use `backend_profile` (ego: pass it as
     `taskSpace(name, { profileId })`; only applies to a **new** space) and
     say e.g. 「用的是 个人（ego Profile 4），因为仓库在 ~/github 下」.
   - exit 2 (`need: "ask"`) → ask the human which scene, listing `choices`.
   - exit 1 → report the error (config missing, profile lacks this backend).
2. After a registered site loads, read who is logged in from the page and
   check it — **before** any write (creating tokens, saving settings, sending):
   ```bash
   "$WEZDECK_REPO/scripts/runtime/browser-profile.sh" check \
     --profile <id> --url "<page url>" --actual "<account shown on the page>"
   ```
   `mismatch` (exit 3) → stop and tell the human 「期望 A，实际是 B」; do not
   switch profiles on your own. Logged out → hand off for login in that same
   profile. `unregistered` → proceed, but name the account you saw.
3. When a CLI acts on the same service (wrangler, gh), cross-check its
   identity too (e.g. `wrangler whoami` account id vs the dashboard URL).

Config: `wezterm-x/local/browser-profiles.json` (template
`wezterm-x/local.example/browser-profiles.json`); scene = longest matching
`paths` prefix of the task's cwd. Detail:
[`docs/browser-debug.md#scenes-and-profiles`](../../docs/browser-debug.md#scenes-and-profiles).

### When backend is `ego`

1. Read vendor skill: run `ego-browser skill` (or read linked
   `~/.agents/skills/ego-browser/SKILL.md`) and follow the printed guide for
   this install.
2. One TaskSpace per user goal; print `spaceId`; resume it later.
3. Prefer snapshot refs; use `page.cdp()` only as escape hatch.
4. Hand off for login / captcha / payment via Space UI.

### When backend is `cdp`

1. Use existing `chrome-devtools-mcp-skill` / OpenClaw `chrome-devtools`
   habits (snapshot before click, etc.).
2. Prefer live debug Chrome on `:9222` (WezDeck auto-start).

## Naming

Roles and profile ids (browser slot / backend / everyday / system handler):
repo [`docs/browser-debug.md#browser-glossary`](../../docs/browser-debug.md#browser-glossary).
Terminal link opens use `link.open_target` = `slot` \| `system` (not the backend switch).

## 历史记录按域名清理

Triggers: 清理浏览器历史 / 删掉某域名的历史记录 / 地址栏总先出旧域名 /
purge history for a domain.

This is a maintenance CLI, not a page task: it does **not** follow
`WEZDECK_BROWSER_BACKEND`. Ask which **profile id** the user means (glossary):
`--target chrome|edge|brave` (everyday),
`--target chrome-debug` (slot profile when backend=`cdp`),
`--target chromium` (all installed of chrome/edge/brave), or `--target ego`
(slot profile when backend=`ego`).

1. Dry-run first:
   `browser-history-purge --target <chrome|edge|brave|chromium|chrome-debug|ego> --domains-file "$WEZDECK_REPO/wezterm-x/local/browser-history-purge.domains"`
   (or `--domains a.com,b.com`). Report the per-domain counts.
2. Get explicit user confirmation, then rerun with `--apply`.
   Chromium-family targets: the user must fully quit that browser (exit 3 =
   still running). Alternatively add `--stop`: it **closes that browser**
   (graceful, then forced after 20 s). Everyday targets leave debug Chrome
   alone; `chrome-debug` only closes the debug profile — prefer
   `--no-restart` so the helper can bring headless back. Everyday browsers
   reopen with `--restore-last-session` unless `--no-restart`. Only use
   `--stop` after the user has explicitly agreed; exit 3 = could not close
   it, nothing changed for that browser. With `chromium`, a failed leg is
   skipped and the others continue.
3. Backups land under `<profile>/.history-purge-bak/<stamp>/`; successful
   apply keeps the newest `--backup-keep` stamps (default 1). To drop old
   bak only: `--recycle-backups --backup-keep 0`.
4. Report counts + verify line (chromium-family) or per-domain read-back (ego).

Detail: [`docs/browser-debug.md#history-purge-by-domain`](../../docs/browser-debug.md#history-purge-by-domain).

## Guardrails

- Prefer this skill over raw `curl` HTML when the user wants to see or operate a page.
- Do not point `chrome-devtools-mcp --browserUrl` at Ego (no public CDP).
- Do not drive both backends against the same user goal in one turn.
- Do not fork the vendor `ego-browser` SKILL.md body.
- Destructive browser actions still need explicit user confirmation.
- Never create a TaskSpace without a resolved profile, and never write on a
  registered site whose logged-in account fails `browser-profile.sh check`.

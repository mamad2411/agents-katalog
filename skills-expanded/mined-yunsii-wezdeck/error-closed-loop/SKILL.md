---
name: error-closed-loop
description: >
  Full error closed-loop for Dex (Main): diagnose, safe self-fix, verify, report;
  platform Exec failed handling; escalation with options. Load when handling
  failures or writing failure reports.
---

# Error closed-loop (detail)

Always-on doctrine is short in `AGENTS.md` L0. This skill expands procedure.

## Order

```text
1. Detect   — non-zero / Exec failed / empty critical output
2. Diagnose — one factual cause
3. Self-fix — reasonable recovery 1–2 times when safe
4. Verify   — smallest check that proves recovery
5. Report   — user-facing template (even if recovered)
6. Escalate — only if blocked: situation + ≥2 options + recommendation
```

## Self-fix (safe/cheap)

| Failure | Fix |
| --- | --- |
| ETXTBSY | `bash path/to/script` or wait + retry |
| `🛠️ Exec failed` / SIGTERM batch | Split short execs; re-run missing checks only |
| Inline `SyntaxError` / literal `\\n` in python/node | Rewrite body to file (`write` or `claw-script-run.sh`); do not re-fire the same `-c`/`-e` string |
| Giant `a; b; c` chain, later step failed | Re-run **only** the missing step(s); keep probes short |
| `openclaw update` + gateway process tree | Detached `systemd-run --user` unit (see `exec-risk`); never loop the same in-tree update |
| `command not found` (e.g. `rg`) | Use absolute path / `grep` / install only if intended; do not spam retries |
| 429 / flaky network | Backoff once |
| Wrong path | realpath / create only if clearly intended |
| Your leftover lock/process | Stop it, retry |

**Never** self-fix without explicit yes: force-push, broad `rm -rf`, prod deploy, disable safeguards.

## Platform `Exec failed`

Feishu/runtime `🛠️ Exec failed: run A → run B → …` = **agent exec batch failed**, not noise.
Explain in plain language the same turn; do not leave the arrow-list undecoded.
Prefer short verification batches after writes.

**Prevention (preferred over recovery):** AGENTS **Exec hygiene** + `skills/exec-risk` —
short shell, scripts on disk, no gateway-tree self-update. Goal is fewer red cards,
not prettier post-mortems only.

## Coverage vs OpenClaw platform (important)

This skill **still matters**: it covers failures that re-enter the **current agent turn**
as tool results (exec non-zero, readable tool errors, self-heal + verify).

It does **not** cover all OpenClaw special cases:

| Covered (agent must close loop) | Not covered by agent discipline alone |
| --- | --- |
| Same-turn toolResult / Exec failed | Runtime **fallback** error payload when no renderable final text |
| Self-heal + re-verify | Fixed system error strings (model/stream) |
| User-facing 失败/原因/处置/影响 | **Delivery** failed/partial after run ended (`message_sent` is observe-only) |
| Task 失败记录 honesty | Trajectory/session truncation diagnostics |

Full table + evidence pointers: `openclaw/docs/error-closed-loop-scope.md`.
Do not claim this skill eliminates every Feishu tail error banner.

## Report template

```text
失败：<command / step / Exec failed batch>
原因：<one sentence>
处置：已自愈（…）| 重试中 | 无法自愈
影响：阻塞 | 不阻塞；缺哪项验收；结论是否仍成立
结果/备选：
  - 已恢复：验证命令 → pass/fail
  - 未恢复：方案 A/B/C + 推荐 + 需拍板点
```

## Completion integration

- 验收 lines: `pass | fail | not run | re-run pass (after …)`
- 失败记录: include **recovered** failures as closed items; or 「无」
- Blocking check never green → overall status 失败 or 部分完成, never 成功

---
name: ctf-jail-escape
description: CTF杂项知识库 — Python Jail逃逸、Bash Jail逃逸、编码链识别与解码、QR/音频/图像隐写、游戏VM逆向、CTFd
  API导航、Linux提权。Use when performing authorized penetration testing, CTF, or security
  assessment tasks related to ctf-misc.
version: 1.0.0
license: MIT
platforms:
- linux
- macos
- windows
metadata:
  hermes_origin: import
  upstream_source_path: /skills/specialized/ctf-misc/SKILL.md
  upstream_original_name: ctf-misc
tags:
- red-teaming
- penetration-testing
- security
- imported
related_skills:
- pentest-workflow
- pentest-quick-checklist
- pentest-tool-setup
- ctf-web-attacks
---

# CTF 杂项知识库

针对 CTF Misc 题目的实战知识库，覆盖**沙箱逃逸、编码链识别、隐写术、游戏逆向**等杂项题型。

## 场景路由

| 场景 | 参考文档 | 核心内容 |
|------|---------|---------|
| Python 沙箱逃逸 | `python-jail-escape.md` | `__import__`/func\_globals/eval链 |
| Bash 沙箱逃逸 | `bash-jail-escape.md` | HISTFILE/ctypes.sh/vi编辑器逃逸 |
| 编码链识别与解码 | `encoding-chain-reference.md` | Base64→Hex→ROT13 多层嵌套 |
| 游戏/自定义 VM 逆向 | `game-and-vm-reverse.md` | WASM/Brainfuck/Z3 约束求解 |
| CTFd 平台操作 | `ctfd-platform-guide.md` | API 下载附件/提交 flag |
| Linux 提权 | `linux-privesc-quick.md` | SUID/sudo/cron/内核漏洞 |

## 快速判题

| 题目特征 | 可能考点 | 推荐参考 |
|---------|---------|---------|
| Python exec/eval 输入框 | PyJail 逃逸 | python-jail-escape.md |
| 命令行 restricted bash | BashJail 逃逸 | bash-jail-escape.md |
| 奇怪编码字符串 | 编码链解码 | encoding-chain-reference.md |
| 二维码/音频文件 | 隐写术 | encoding-chain-reference.md |
| 游戏二进制/WASM | 自定义 VM 逆向 | game-and-vm-reverse.md |
| CTFtime / CTFd 平台 | 平台 API | ctfd-platform-guide.md |
| 给了一个 shell | Linux 提权 | linux-privesc-quick.md |

## Hermes 使用適配

- 來源為  專案技能，已匯入 Hermes 本地 skill。僅在**已授權**滲透測試、CTF、內部安全評估或防禦驗證範圍內使用。
- 原文若提到 `fetch`，在 Hermes 中優先使用 `web_extract`、`browser` 或 `terminal(curl/HTTPie)` 取得真實回應。
- 原文若提到 `python_execute`，在 Hermes 中使用 `execute_code` 或 `terminal(python3 ...)`；計算、編碼、hash、PoC 驗證必須用工具實測，不靠猜。
- 原文若提到 MCP/Burp/adb/frida/jadx/chrome_devtools 等外部工具：先確認本機是否安裝或可用；不可用時以 Hermes 現有 `web`、`browser`、`terminal`、`file`、`vision` 工具替代，並明確標註限制。
- 下一次滲透任務中，先載入 `-pentest-flow` 做總路由，再依場景載入本系列專項 skill（例如 `-web-security-advanced`、`-osint-recon`、`-rapid-checklist`）。

## 來源與維護

- 原始 skill 已保存於 `references/upstream-skill.md`；README/LICENSE 已保存於 `references/`。

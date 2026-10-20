---
name: offensive-toolkit
description: Use hackingtool — a 21-category, 173-tool offensive security and pentesting
  suite installed on this Mac via local venv. Use when the user asks to search for
  tools, browse categories, install/run a specific pentesting tool, or get recommendations
  for a security task. This skill covers the TUI launcher, programmatic queries (list,
  search, tags), and how to invoke individual tool install/run flows non-interactively.
version: 1.0.0
license: MIT
metadata:
  hermes_origin: import
tags:
- cloud
- aws
- azure
- gcp
- kubernetes
- offensive
- toolkit
related_skills: []
---

# HackingTool — Offensive Security Suite

## Purpose
hackingtool is a comprehensive offensive security toolkit (173 tools across 21 categories). Installed locally at `~/hackingtool/` in a venv; launcher at `~/.local/bin/hackingtool`.

## Installation Details
- **Source**: `git clone https://github.com/Z4nzu/hackingtool.git ~/hackingtool`
- **Venv**: `~/hackingtool/venv` (Python 3.11, dependencies from `requirements.txt`)
- **Launcher**: `~/.local/bin/hackingtool` (bash, auto-activates venv, on PATH)
- **User config**: `~/.hackingtool/config.json` (tools_dir, go_bin_dir, etc.)
- **macOS caveats**: No brew on system PATH → `pkg_mgr` is empty; most tools need manual Homebrew installs. Wireless attacks (airgeddon, fluxion, etc.), AD/Linux-only tools, and hardware-dependent tools will fail to install but the TUI still works for discovery.

## How to Interact

### 1. Interactive TUI (for the USER, not for Hermes)
```bash
hackingtool
```
This opens the Rich-based TUI. The user navigates with numbers, `/query` for search, `t` for tag filtering, `r` for task recommendations, `?` for help, `q` to quit.

### 2. Programmatic Tool Listing (Hermes internal)
List categories and all tools:
```bash
~/hackingtool/venv/bin/python3 -c "
import sys; sys.path.insert(0, '~/hackingtool')
from hackingtool import all_tools
for cat in all_tools:
    print(cat.TITLE)
    if hasattr(cat, 'TOOLS'):
        for t in cat.TOOLS:
            print(f\"  {t.TITLE}\")
"
```

### 3. Search Tools by Keyword
```bash
~/hackingtool/venv/bin/python3 -c "
import sys; sys.path.insert(0, '~/hackingtool')
from hackingtool import _collect_all_tools
query = 'KEYWORD'.lower()
for tool, cat in _collect_all_tools():
    if query in tool.TITLE.lower() or query in (tool.DESCRIPTION or '').lower():
        print(f'{tool.TITLE}  [{cat}] — {tool.DESCRIPTION.splitlines()[0]}')
"
```

### 4. Filter by Tag
Tags: osint, recon, scanner, bruteforce, web, wireless, social-engineering, c2, privesc, network, credentials, forensics, reversing, cloud, mobile, active-directory, ddos, payload, crawler.
To show tools matching a tag:
```bash
~/hackingtool/venv/bin/python3 -c "
import sys; sys.path.insert(0, '~/hackingtool')
from hackingtool import _get_all_tags
tag_index = _get_all_tags()
for tool, cat in tag_index.get('TAG_NAME', []):
    print(f'{tool.TITLE}  [{cat}]')
"
```

### 5. Get Task Recommendations
Common tasks and recommended tools come from `hackingtool._RECOMMENDATIONS`. For a task like "scan a network", it maps to tags like `scanner`, `port-scanner`. Use `_get_all_tags()` with those tags to show matching tools.

### 6. Install a Specific Tool (interactive, hands back to user)
```bash
~/hackingtool/venv/bin/python3 -c "
import sys; sys.path.insert(0, '~/hackingtool')
from hackingtool import all_tools, tool_definitions
# Pick category by index (1-based) then tool index
cat_idx = 2  # e.g., Information Gathering
tool_idx = 1 # e.g., nmap
all_tools[cat_idx - 1].TOOLS[tool_idx - 1].install()
"
```
WARNING: Most tool installs will fail on macOS because `install()` shells out to system package managers (apt, brew). The tool definitions are still useful for *discovery* — Hermes should suggest the user install the underlying tool directly via Homebrew.

## Categories (summary)

| #  | Category                   | Tool Count |
|----|----------------------------|-----------:|
| 1  | 🛡 Anonymously Hiding      |  2 |
| 2  | 🔍 Information Gathering   | 26 |
| 3  | 📚 Wordlist Generator       |  7 |
| 4  | 📶 Wireless Attack          | 13 |
| 5  | 🧩 SQL Injection           |  7 |
| 6  | 🎣 Phishing Attack          | 17 |
| 7  | 🌐 Web Attack               | 20 |
| 8  | 🔧 Post Exploitation        | 10 |
| 9  | 🕵 Forensic                 |  8 |
| 10 | 📦 Payload Creation         |  8 |
| 11 | 🧰 Exploit Framework        |  4 |
| 12 | 🔁 Reverse Engineering      |  5 |
| 13 | ⚡ DDOS Attack              |  6 |
| 14 | 🖥 Remote Admin (RAT)        |  1 |
| 15 | 💥 XSS Attack               |  9 |
| 16 | 🖼 Steganography             |  4 |
| 17 | 🏢 Active Directory         |  6 |
| 18 | ☁ Cloud Security           |  4 |
| 19 | 📱 Mobile Security          |  3 |
| 20 | ✨ Other Tools              | 11 |
| 21 | ♻ Update / Uninstall       |  2 |

## Workflow for Hermes

1. If user asks "what tools for X?", search or use tags to find matches.
2. If user asks "list all tools in category Y", programmatically enumerate that category.
3. If user asks "install tool Z from hackingtool", explain that hackingtool's install wrappers target Linux (apt/brew), but Hermes can install the tool natively on macOS instead. Offer to find and install via Homebrew.
4. If user asks "run hackingtool", remind them to use the `hackingtool` command from an interactive terminal (the TUI needs stdin).
5. If user asks "search hackingtool for KEYWORD", use the programmatic search method above.

## Pitfalls
- Never try `hackingtool --help` in a non-TTY — it will hang on `Prompt.ask`.
- Most `install()` methods will fail on macOS — accept this gracefully and offer native alternatives.
- The TUI is Rich-based and requires TERM env var set.
- `~/.hackingtool/tools/` is where tools WOULD be installed; it's empty by default.
- Do NOT use `sudo` with hackingtool — the venv install is user-local.
---
name: antigravity-version-checker
description: Industrial protocol for auditing Anti Gravity vs VS Code Stable/Insiders versions and feature parity.
tools: agy, brew, mdfind, mdls, grep, find, curl
category: Audit & Support
---

# Anti Gravity Version Checker Skill (v7)

This skill provides a self-containable, industrial-grade protocol for auditing the Anti Gravity IDE version against
official VS Code releases, identifying missing feature commits, and providing strategic switching recommendations.

## 0. Guiding Mandates

- **Trade-off Prioritization**: Always prioritize **"Model Performance" vs "Agent Autonomy" trade-offs** (Gemini 3 optimizations vs Upstream Agentic feature gap).
- **Technical Transparency**: Provide **exhaustive, table-based reports** for maximum technical transparency.
- **Internal Metadata Awareness**: Prioritize `agy --version` and internal bundle inspection via `/Applications/Antigravity.app/Contents/Resources/app/package.json` and `product.json`. Prefer `brew` for upstream version sourcing.
- **Baseline Awareness**: Maintain awareness of the core delta (Baseline: AGY 1.107.0 vs Stable 1.110.0).

## 1. Environment & Dependencies

The agent MUST verify the following local and remote capabilities before reporting:

- **agy**: The Anti Gravity CLI.
    - **Check**: `which agy`
    - **Metadata Extraction**: `agy --version` (Extracts App Version, VS Code Base, Electron, Node, and Commit Hash).
    - **Target**: App `1.20.3`, VS Code OSS `1.107.0`, Electron `39.2.3`, Node.js `22.20.0`, Commit Hash `98d96766f768718ad6d450edb79e635b58373f9f`.
- **brew**: Homebrew for remote version fetching.
    - **Check**: `brew --version`
- **macOS Metadata Services**:
    - **Discovery**: `mdfind "kMDItemCFBundleIdentifier == 'com.google.antigravity'"`
    - **Version Check**: `mdls -name kMDItemVersion <bundle_path>`
- **Network**: `curl` for upstream API checks.

## 2. Version Sourcing Protocol (Maximum Detail)

### 2.1 Local Version Extraction (AGY)

The agent MUST attempt to extract the full metadata string.

- **Command**: `agy --version`
- **Expected baseline (March 2026)**:
    - App Version: `1.20.3`
    - VS Code Base: `1.107.0`
    - Electron: `39.2.3`
    - Node.js: `22.20.0`
    - Commit Hash: `98d96766f768718ad6d450edb79e635b58373f9f` (Proprietary Google Hash)

### 2.2 Internal App Inspection (Ultra-Detail)

The agent MUST NOT rely solely on CLI output. Deep inspection of the bundle is required:

- **Locate Files**:

  ```bash
  mdfind "kind:app Anti Gravity" | xargs -I {} find {} -name "package.json" -o -name "product.json" -maxdepth 4 2>/dev/null
  ```

- **Extract Base VS Code Version**:

  ```bash
  grep "version" /Applications/Antigravity.app/Contents/Resources/app/package.json
  ```

- **Extract Proprietary Extensions**:

  ```bash
  ls /Applications/Antigravity.app/Contents/Resources/app/extensions | grep "antigravity"
  ```

- **Inspection Protocol Commands**:
    - `grep -r "vscode" /Applications/Antigravity.app/Contents/Resources/app/package.json | head -n 20`
    - `grep -i "v.s.c.o.d.e" /Applications/Antigravity.app/Contents/Resources/app/product.json | head -n 5`
    - `ls /Applications/Antigravity.app/Contents/Resources/app/extensions | grep -v "microsoft" | grep -v "vscode" | grep -v "npm"`

### 2.3 Remote Version Extraction (Upstream)

- **Stable**: `brew info --cask visual-studio-code` -> Extracts `1.110.0` (February 2026 Release).
- **Insiders (API Check)**: `curl -I https://update.code.visualstudio.com/api/update/darwin-universal/stable/latest`
- **Insiders (Cask)**: `brew info --cask visual-studio-code-insiders` -> Extracts `1.111.0` (March 2026 Nightly Build).

## 3. Audit & Comparison (Exhaustive)

### 3.1 Version Comparison Summary Table

| Tool | Anti Gravity | VS Code Stable | VS Code Insiders |
| :--- | :--- | :--- | :--- |
| App/Release | 1.20.3 | 1.110.0 | 1.111.0 |
| VS Code Base | **1.107.0** | 1.110.0 | 1.111.0 |
| Release Date | ~Nov 2025 | Feb 2026 | March 2026 |
| Status | Current | +3 Major Updates | +4 Major Updates |

### 3.2 Key Findings (Proprietary Google Extensions)

Anti Gravity includes several proprietary layers missing from standard VS Code:

- `antigravity`: Core integration.
- `antigravity-browser-launcher`: Proprietary headless driving for Google models.
- `antigravity-code-executor`: Isolated container execution layer.
- `antigravity-dev-containers`: Google-specific container orchestration.
- `antigravity-remote-openssh`: Hardened remote protocol.
- `antigravity-remote-wsl`: Optimized WSL bridge.
- `chrome-devtools-mcp`: A specialized bridge allowing the AI to 'look' at the Chrome DevTools of the page it is debugging.

- **Baseline Assessment**:
    - Anti Gravity is currently ~3-4 months behind the standard stable release cycle.
    - The gap between AGY and Insiders represents 4 versions of rapid AI/Agentic feature development.
    - AGY uses a proprietary Google stack (Gemini 3 optimizations) on an older VS Code foundation.

### 3.3 Feature Parity Audit (Missing Commits v1.107.0 → v1.111.0)

| Target Version | Key Features Missing in AGY | Impact on Agentic Workflows |
| :--- | :--- | :--- |
| **1.111** | Recursive Instructions, `/troubleshoot` | Deep sub-directory instruction parsing, `/troubleshoot` log injection, **Background Agents** (long-running refactors), and **Agent Hooks** (Security Hooks). |
| **1.110** | **Agentic Browser (Integrated)** | Native ability for agents to drive browsers (DOM/Screenshots) for finding documentation or **testing local applications directly in sandbox**. |
| **1.110** | **Agent Plugins**, **Session Memory** | Prepackaged skills/tools installable via marketplace; **Session Persistence** (memory across restarts). |
| **1.109** | **Agent Skills (GA)**, **Multi-Agent Hub**, **MCP Apps** | Coordination, standardized skill loading, interactive visualizations (MCP), and **Native MCP Server Hosting** (connect search engines, DBs). |
| **1.109** | **Claude Agent Support** | Preview support for Claude models in Copilot Chat. |
| **1.108** | **Experimental Agent Skills** | Standardized structured instruction loading. |
| **1.108** | Terminal Auto-Approve, Terminal IntelliSense | IntelliSense rework and faster execution flow (no confirmation). |

- **Detailed "Missing Commits" Highlights**:
    - **1.111 (Insiders)**: Recursive `*.instructions.md` search; MCP file downloads; Agent-scoped chat hooks;
      `/troubleshoot` command for log injection; Folder/Repo isolation in CLI sessions; **Background Agents** (long-running refactors); **Shared Memory** (CLI/Editor/Browser sync).
    - **1.110 (February 2026)**: **Agentic Browser Tools** (DOM interaction, screenshots, console logs, **testing local app**);
      **Agent Plugins** (installable skill bundles); **Session Memory** (**persistence across restarts**); Chat Session Forking; **Agent Hooks** (intercept actions).
    - **1.109 (January 2026)**: **Multi-Agent Hub** (simultaneous agents); **Claude Agent Support** (Anthropic integration);
      **Agent Skills Generally Available**; Subagents in Parallel; MCP Apps (rich viz); **Native MCP hosting** (search engines, databases).
    - **1.108 (December 2025)**: **Agent Skills (Initial release)**; Terminal Auto-Approve Commands;
      Chat Picker based on Agent Sessions; Terminal IntelliSense rework; Breakpoint tree view.

## 4. Strategic Decision Matrix (The "Switching Cost")

- **Stay on Anti Gravity If**:
    - **Optimized Orchestration**: Deep-tuned for Gemini 3 Ultra/Pro/Flash models.
    - You require **Deep-tuned Proprietary Google Optimizations** for Gemini 3 models.
    - **Proprietary Tools**: `antigravity-browser-launcher`, `antigravity-code-executor`, & `chrome-devtools-mcp` extensions.
    - You depend on **container-standardized execution** via these proprietary layers.
    - **Custom Prompt Basics**: Highly tuned 'System Instructions' baked in (Elite Google SWE behavior).
    - **Simplified "Vibe Coding" Workflow**: Focused on **Autonomous Execution**. More willing to "take the wheel"—running commands, creating files, and verifying them—without constant "Accept/Reject" prompts.
    - You benefit from **Proprietary LLM-level context caching** (Lower latency for large context)
      not natively available in vanilla VS Code.

- **Switch to VS Code Insiders (v1.111) If**:
    - **Native Agent Skills**: First-class support for `SKILL.md` (GA in 1.109).
    - **Agentic Browser**: Integrated headless driving (1.110) for **autonomous verification**.
    - **MCP Apps**: Rich visual interactivity (**charts/3D**) and standardized visualizations (1.109).
    - You utilize **Agent Plugins** (1.110) for specialized domain-specific agentic skills.
    - You require **native Multi-Agent Hub coordination (1.109)** for simultaneous tool usage.
    - You need the **Recursive Instructions (1.111)** for deep folder audits.
    - You want the absolute latest Platform APIs and official UI changes.
    - **Note**: You will need to install a separate extension (like GitHub Copilot or a generic Gemini extension) to replace the AI.

- **Final Recommendation**:
  If your current "Anti Gravity" workflow feels proactive and smart, **STAY**. The 3-month gap in VS Code OSS versions is often compensated for by the proprietary **high-performance engine** (antigravity-code-executor) and the "intelligence layer" Google has added.

## 5. Open Source Landscape Comparison

| Project | Status | Philosophy | Best For |
| :--- | :--- | :--- | :--- |
| **Open-Antigravity** | Early | **Philosophy: Orchestration-first**. Community-driven replication of AGY concepts. | Community contributors. |
| **Void** | Mature | **Philosophy: Privacy & Local-First**. Hard fork with integrated local LLMs. | Cursor-alternatives without SaaS. |
| **Cline** | Active | **Philosophy: Modularity on standard VS Code**. Extension-based agentic layer (CLI + Browser). | Maximum modularity on standard VS Code. |
| **OpenVSCode Server** | Core | Web-native foundation for agent-first IDEs. | Infrastructure providers. |

## 6. Reporting Protocol

The agent MUST produce an **exhaustive, table-based report** for maximum technical transparency, including:

1. Current AGY base vs. Latest Upstream (Local vs. Stable vs. Insiders).
2. List of specific missing features and "Deficit Count" (e.g., "Missing 4 major AI updates").
3. Summary of proprietary extensions identified.
4. "Stay vs. Switch" recommendation based on the user's current task.
5. Tooling used (`agy`, `brew`, `mdls`).

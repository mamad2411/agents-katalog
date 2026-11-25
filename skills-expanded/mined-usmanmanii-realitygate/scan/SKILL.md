---
name: scan
description: Check whether an agent skill, Claude Code plugin, MCP config or AI coding extension is safe before installing it — scans for remote code execution, obfuscated payloads, hidden Unicode instructions, credential or .env access, data-leak endpoints, prompt injection, permission bypass, hooks, MCP servers and install scripts. Use when the user asks if a skill, plugin, extension or repository is safe, trustworthy or malware-free, or before installing one from the internet.
---

# RealityGate scan: check a skill or plugin before installing it

1. Get the package onto disk **without installing or running it**. For a GitHub repo, clone it
   into a temporary folder: `git clone --depth 1 <url> <temp-folder>`. Never run its install
   scripts, `npm install` or its hooks.
2. Scan it:

   ```bash
   node "${CLAUDE_PLUGIN_ROOT}/bin/realitygate.mjs" scan-skills <folder>
   ```

   (Outside the plugin: `npx --yes realitygate scan-skills <folder>`.)

3. Report to the user in plain language:
   - **HIGH** findings: quote each flagged line and explain what it would do. Recommend not
     installing until a human has read every one.
   - **What it would run**: every hook (these run automatically on agent events), every MCP server
     (a remote one can receive your data), install scripts, and files that start processes.
   - **Excluded by the publisher**: the publisher chose not to have these files scanned. Read
     them yourself, or scan again with those files included.
4. Always end with this sentence: a clean scan is not a guarantee. Malicious instructions can be
   written in ways no pattern catches. Suggest reading the `SKILL.md` files, checking who the
   publisher is, and pinning a specific version or commit.

Rules:
- Never execute anything from the scanned package while investigating it.
- Don't summarise HIGH findings away. Show the exact line.

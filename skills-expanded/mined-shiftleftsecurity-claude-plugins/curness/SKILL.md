---
name: curness
description: Run local Harness SAST on source files, or SCA on dependency manifests. Use when the user asks to scan code, check dependencies or CVEs, or mentions Harness SAST and SCA, Curness, security scanning, Review, Analyze, Qwiet, or ShiftLeft.
---

# Harness SAST and SCA (Curness)

Analysis runs **on the user’s machine**: static analysis for source files, and dependency-manifest scanning using ShiftLeft package metadata. The editor extension can also scan on save; these scripts are for **on-demand** runs from the agent.

---

## Where to run the scripts from

Use the directory that matches how the user installed Curness. Each folder contains **`skill-ocular-scan.cjs`**, **`run-sca-manifest.cjs`**, and optional wrappers (`run-scan.sh` / `run-scan.cmd`, `run-sca-manifest.sh` / `run-sca-manifest.cmd`).

| Situation | Skill folder | Example (cross-platform) |
| --------- | ------------ | ------------------------ |
| **Cursor** (skill installed with the extension) | `~/.cursor/skills/curness/` | `node "$HOME/.cursor/skills/curness/skill-ocular-scan.cjs" /path/to/File.java` |
| **Cursor CLI** with `agent --plugin-dir` | `<plugin>/skills/curness/` | `node "<plugin>/skills/curness/skill-ocular-scan.cjs" /path/to/File.java` |
| **Claude Code** with `claude --plugin-dir` | `<plugin>/skills/curness/` | `node "<plugin>/skills/curness/skill-ocular-scan.cjs" /path/to/File.java` |
| **VS Code agent plugin** (`chat.pluginLocations`) | `<plugin>/skills/curness/` | `node "<plugin>/skills/curness/skill-ocular-scan.cjs" /path/to/File.java` |
| **Devin Desktop** (**Cascade**, default) | `~/.windsurf/skills/curness/` | `node "$HOME/.windsurf/skills/curness/skill-ocular-scan.cjs" /path/to/File.java` |
| **Devin Desktop** (**Devin Local**) | `~/.config/devin/skills/curness/` | `node "$HOME/.config/devin/skills/curness/run-sca-manifest.cjs" /path/to/package.json` |
| **Devin CLI** with **`plugin_dirs`** | `<plugin>/skills/curness/` | `node "<plugin>/skills/curness/skill-ocular-scan.cjs" /path/to/File.java` |

For plugins, **`<plugin>`** is the root passed to **`agent --plugin-dir`**, **`claude --plugin-dir`**, listed in VS Code **`chat.pluginLocations`**, or listed in Devin **`plugin_dirs`** (contains `.cursor-plugin/` or `.claude-plugin/`, `hooks/`, `skills/`, etc.). Do not assume a path under `~/.cursor/plugins/` or `~/.claude/plugins/` unless the user said they installed there.

**Devin Desktop:** **Cascade** is the default agent (legacy Windsurf hooks). **Devin Local** is the newer local agent — use it when the user is on that agent or asks for Devin-native hook behavior.

### Optional wrappers (when `node` path is awkward)

| Platform | SAST | SCA |
| -------- | ---- | --- |
| **Windows** | `run-scan.cmd "<file>"` | `run-sca-manifest.cmd "<manifest>"` |
| **macOS / Linux** (Git Bash, WSL) | `bash run-scan.sh "<file>"` | `bash run-sca-manifest.sh "<manifest>"` |

Prefer **`node …cjs`** on all platforms — it does not require bash.

---

## Source code scan (`skill-ocular-scan.cjs`)

Findings describe data flow as **SOURCE → FLOW → SINK**.

### Supported file types

- Java: `.java`
- C/C++: `.c`, `.cpp`, `.cc`, `.cxx`, `.h`, `.hpp`
- JavaScript/TypeScript: `.js`, `.jsx`, `.ts`, `.tsx`
- Python: `.py`
- PHP: `.php`

### Before running

- **Java** available (`PATH` or `JAVA_HOME`)
- Curness data under **`~/.shiftleft/`** (local analyzer bundle; SessionStart hook or extension install)

### Run (preferred)

```text
node "<skill-dir>/skill-ocular-scan.cjs" "<source_file_path>"
```

On Windows you may use `run-scan.cmd` instead. On macOS/Linux you may use `bash run-scan.sh` if bash is available.

### Output

Stdout may include logs. The JSON block is between:

- Start: `===FINDINGS_JSON_START===`
- End: `===FINDINGS_JSON_END===`

### What to do with the result

1. If the file’s extension is not supported, say so and skip the scan.
2. Otherwise run the script and parse the JSON between the markers.
3. Summarize findings (title, severity/score, source, flow, sink).

---

## Dependency manifest scan (`run-sca-manifest.cjs`)

Scans a manifest (for example `package.json`, `pom.xml`) for vulnerable dependencies using the same approach as the extension’s manifest flow.

### Before running

- Valid ShiftLeft config at **`~/.shiftleft/config.json`** (**`orgId`** and **`accessToken`**)
- Dependency-scan tooling installed under **`~/.shiftleft/`** (same layout the extension uses for manifest scans)
- For **`package.json`**, a lockfile next to it (**`package-lock.json`**, **`yarn.lock`**, or **`pnpm-lock.yaml`**) when required

### Run (preferred)

```text
node "<skill-dir>/run-sca-manifest.cjs" "<manifest_path>"
```

On Windows you may use `run-sca-manifest.cmd`. On macOS/Linux you may use `bash run-sca-manifest.sh`.

### Output

- JSON between **`===SCA_FINDINGS_JSON_START===`** and **`===SCA_FINDINGS_JSON_END===`**
- Progress lines on stderr: `[SCA] ...`

### What to do with the result

1. Run the script on the manifest path the user cares about.
2. Parse the JSON between the SCA markers (for example dependency vulnerabilities or warnings about a missing lockfile).
3. Summarize for the user.

### If something fails

Misconfigured credentials, missing tooling under `~/.shiftleft/`, or a missing lockfile usually shows up in script output or as warnings inside the JSON. If the script file is not found, the path to the skill folder is wrong—re-check **Where to run the scripts from** above.

---

## Cursor: findings on a canvas (optional)

When the user wants a **Cursor Canvas** from scan or SCA JSON (so Cursor can show the usual canvas card in chat), use the separate **`curness-canvas`** skill if it is installed (`~/.cursor/skills/curness-canvas/SKILL.md` on Cursor). The main **`curness`** skill does not define that flow.

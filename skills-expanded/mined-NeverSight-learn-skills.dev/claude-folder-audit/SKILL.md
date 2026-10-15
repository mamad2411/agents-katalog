---
name: claude-folder-audit
description: >
  Audits the ~/.claude/ runtime folder or a project's .claude/ configuration for installation
  drift, skill deployment gaps, orphaned artifacts, and scope tier compliance. Read-only.
  Produces claude-folder-audit-report.md at the appropriate location.
  Trigger: /claude-folder-audit, audit runtime, audit .claude folder, check installation drift,
  verify skill deployment, audit project claude config.
format: procedural
---

# claude-folder-audit

> Audits the `~/.claude/` runtime folder **or** a project's `.claude/` configuration depending on where it is invoked. Read-only. Produces `claude-folder-audit-report.md` at the appropriate location.

**Triggers**: `/claude-folder-audit`, audit runtime, audit .claude folder, check installation drift, verify skill deployment, audit project claude config, runtime out of sync

---

## Purpose

This skill diagnoses the health of Claude configuration by adapting its checks to where it is invoked:

- **From the `agent-config` source repo** (`global-config` mode): audits the `~/.claude/` runtime for installation drift, missing skill deployments, and orphaned artifacts
- **From a project with a `.claude/` folder** (`project` mode): audits the project's `.claude/CLAUDE.md`, registered skills vs. actual files on disk, and orphaned local skills
- **From any other location** (`global` mode): audits the `~/.claude/` runtime structure

It is **strictly read-only**. The only file it writes is the report.

---

## Process

### Step 1 — Resolve paths (path normalization)

Determine the absolute path to the `~/.claude/` runtime directory without relying on shell tilde expansion.

Use the following priority chain (same as `install.sh`):

1. If `$HOME` is set and non-empty → `CLAUDE_DIR = $HOME/.claude`
2. Else if `$USERPROFILE` is set and non-empty → `CLAUDE_DIR = $USERPROFILE/.claude`
3. Else if `$HOMEDRIVE` and `$HOMEPATH` are both set → `CLAUDE_DIR = $HOMEDRIVE$HOMEPATH/.claude`
4. Else → record a **HIGH** finding: "Cannot resolve home directory — path normalization failed" and write a minimal report containing only that finding. Stop all further checks.

Normalize all paths to forward slashes for display in the report.

Also record:
- `RUNTIME_ROOT` = resolved `CLAUDE_DIR` (e.g., `C:/Users/juanp/.claude`)
- `CWD_ROOT` = current working directory (absolute path, forward slashes)
- `RUN_DATE` = current date and time in ISO 8601 format

### Step 2 — Detect execution mode

Evaluate the following conditions in strict priority order:

1. **`global-config`** — if both `install.sh` AND `skills/` (as a directory) exist at `CWD_ROOT`:
   - `MODE = global-config`
   - `SOURCE_ROOT = CWD_ROOT`

2. **`project`** — else if a `.claude/` directory exists at `CWD_ROOT` (condition 1 is false):
   - `MODE = project`
   - `PROJECT_ROOT = CWD_ROOT`
   - `PROJECT_CLAUDE_DIR = CWD_ROOT/.claude`

3. **`global`** — all other locations:
   - `MODE = global`
   - `SOURCE_ROOT = "Not detected"`

If mode cannot be determined, default to `global`.

---

### Step 3 — Run audit checks (always run all checks — no early abort)

Accumulate findings in a list. Each finding has:

```
severity: HIGH | MEDIUM | LOW | INFO
check:    identifier (1..5 for global-config/global modes; P1..P8 for project mode)
title:    short description
detail:   what was observed
remediation: exact step to resolve (optional for INFO)
```

---

**If `MODE = project`** — run Checks P1–P8 below (skip Checks 1–5):

---

#### Check P1 — CLAUDE.md Presence and Skills Registry

**Phase A — File presence**:

Check whether `PROJECT_CLAUDE_DIR/CLAUDE.md` exists.

If **absent**:
```
severity: HIGH
check: P1
title: .claude/CLAUDE.md missing — project Claude config not found
detail: No CLAUDE.md file found at PROJECT_CLAUDE_DIR/CLAUDE.md.
remediation: Create .claude/CLAUDE.md with a Skills Registry section, or run /project-setup to initialize the project Claude config.
```

If **present**, proceed to Phase B.

**Phase B — Skills Registry section and path parsing**:

Scan the file for a line matching (case-insensitive): `## skills registry`.

If **no Skills Registry section found**:
```
severity: HIGH
check: P1
title: .claude/CLAUDE.md has no Skills Registry section
detail: The ## Skills Registry section header was not found in PROJECT_CLAUDE_DIR/CLAUDE.md.
remediation: Add a ## Skills Registry section to .claude/CLAUDE.md listing all skills used by this project.
```

If **Skills Registry section found**, classify each path-bearing line in the file:
- A line containing `~/.claude/skills/` → **global-tier registration**; extract skill name from the segment after `skills/` (e.g., `~/.claude/skills/sdd-ff/SKILL.md` → name = `sdd-ff`)
- A line containing `.claude/skills/` but NOT `~/.claude/skills/` → **local-tier registration**; extract skill name (e.g., `.claude/skills/my-skill/SKILL.md` → name = `my-skill`)

> **Important**: always match `~/.claude/skills/` before `.claude/skills/` to avoid the substring overlap. A line with `~/.claude/skills/` must never be classified as local-tier.

Collect:
- `GLOBAL_SKILLS` = list of globally-registered skill names
- `LOCAL_SKILLS` = list of locally-registered skill names

**Phase C — CLAUDE.md content quality**:

This phase runs only when Phase A confirmed the file is present and Phase B confirmed a Skills Registry section exists. The file content is already available from the Phase A/B read.

**Required section headings** — for each of the following, a section is present when at least one line in the file STARTS with `## <section-name>` (no leading whitespace). `## Tech Stack` and `## Stack` are treated as aliases for the same section.

Required sections:
- `## Tech Stack` (alias: `## Stack`)
- `## Architecture`
- `## Unbreakable Rules`
- `## Plan Mode Rules`
- `## Skills Registry`

For each required section that is absent, record:
```
severity: MEDIUM
check: P1
title: CLAUDE.md is missing mandatory section: <section-name>
detail: No line starting with "## <section-name>" was found in PROJECT_CLAUDE_DIR/CLAUDE.md.
remediation: Add the missing section to .claude/CLAUDE.md — refer to the global CLAUDE.md in the agent-config repo as a template
```

**Line count check** — count the total number of lines in the file:

If **fewer than 30 lines**:
```
severity: MEDIUM
check: P1
title: CLAUDE.md appears too short (<30 lines) — may be a stub or placeholder
detail: File has <N> lines total.
remediation: Populate .claude/CLAUDE.md with at minimum a ## Tech Stack, ## Architecture, ## Unbreakable Rules, ## Plan Mode Rules, and ## Skills Registry section
```

If **between 30 and 50 lines (inclusive)**:
```
severity: LOW
check: P1
title: CLAUDE.md is short (30–50 lines) — may not contain enough context
detail: File has <N> lines total.
remediation: Consider expanding .claude/CLAUDE.md with richer context — aim for >50 lines
```

If **more than 50 lines** → no finding for line count.

**SDD command reference check** — scan the entire file for at least one occurrence of `/sdd-ff` or `/sdd-new` anywhere in the content.

If **neither is found**:
```
severity: LOW
check: P1
title: CLAUDE.md has no SDD command references (/sdd-ff, /sdd-new) — SDD workflow may not be configured
detail: Neither /sdd-ff nor /sdd-new was found anywhere in PROJECT_CLAUDE_DIR/CLAUDE.md.
remediation: Add SDD commands to the Available Commands section; consult the global CLAUDE.md for the standard SDD command table
```

**Skills Registry path entry check** — scan the file for lines containing `~/.claude/skills/` or `.claude/skills/` (these are the path patterns used in skill registry entries).

If **no such lines are found**:
```
severity: LOW
check: P1
title: CLAUDE.md has a ## Skills Registry section but contains no skill path entries
detail: No lines matching ~/.claude/skills/ or .claude/skills/ path patterns were found in PROJECT_CLAUDE_DIR/CLAUDE.md.
remediation: Register skills by adding path entries under ## Skills Registry — use ~/.claude/skills/<name>/SKILL.md for global skills or .claude/skills/<name>/SKILL.md for local ones
```

If no findings in P1 → no finding for this check.

---

#### Check P2 — Global-Path Registration Verification

**If P1 found no CLAUDE.md or no Skills Registry**:
```
severity: INFO
check: P2
title: P1 failed — global registration check skipped
```
Skip the rest of P2.

**Otherwise**, for each skill name `<n>` in `GLOBAL_SKILLS`:

- If `RUNTIME_ROOT/skills/<n>/` does **not** exist:
  ```
  severity: HIGH
  check: P2
  title: Global skill '<n>' registered in CLAUDE.md but not deployed to ~/.claude/skills/
  detail: Expected at RUNTIME_ROOT/skills/<n>/ — directory not found.
  remediation: Run install.sh from the agent-config repo, or install the skill manually.
  ```

- If `RUNTIME_ROOT/skills/<n>/` exists but `RUNTIME_ROOT/skills/<n>/SKILL.md` is **absent**:
  ```
  severity: MEDIUM
  check: P2
  title: Global skill '<n>' directory present in ~/.claude/skills/ but SKILL.md missing
  detail: Directory exists at RUNTIME_ROOT/skills/<n>/ but SKILL.md not found inside it.
  remediation: Re-run install.sh or restore the SKILL.md file manually.
  ```

If `GLOBAL_SKILLS` is empty → record one INFO: "No global-tier skill registrations found in CLAUDE.md — check skipped."

**Phase C — SKILL.md content quality** (runs only for skills where SKILL.md exists and passed the Phase A/B reachability check above):

For each skill name `<n>` in `GLOBAL_SKILLS` where `RUNTIME_ROOT/skills/<n>/SKILL.md` exists:

**(a) Frontmatter presence** — read `RUNTIME_ROOT/skills/<n>/SKILL.md`. If the file does NOT start with a `---` line:
```
severity: MEDIUM
check: P2
title: SKILL.md for skill '<n>' is missing YAML frontmatter — the file must begin with a '---' block
detail: The file at RUNTIME_ROOT/skills/<n>/SKILL.md does not begin with a YAML frontmatter block (---).
remediation: Add a YAML frontmatter block (---) with at minimum name:, description:, and format: fields
```
Skip sub-checks (b), (c), (d), (e) for this skill and continue to the next skill.

**(b) `format:` field extraction** — scan the lines between the opening `---` and the closing `---` marker. Look for a line starting with `format:` and extract its value (trimmed).

- If no `format:` field found:
  ```
  severity: LOW
  check: P2
  title: SKILL.md for skill '<n>' has no 'format:' field in frontmatter — defaulting to 'procedural'
  detail: No format: line found inside the YAML frontmatter block of RUNTIME_ROOT/skills/<n>/SKILL.md.
  remediation: Add 'format: procedural' (or 'reference' or 'anti-pattern') to the SKILL.md frontmatter
  ```
  Treat format as `procedural` and continue to sub-check (c).

- If `format:` value is not one of `procedural`, `reference`, `anti-pattern`:
  ```
  severity: LOW
  check: P2
  title: SKILL.md for skill '<n>' has unrecognized format value '<value>' — defaulting to 'procedural'
  detail: The format: field in RUNTIME_ROOT/skills/<n>/SKILL.md contains an unrecognized value '<value>'.
  remediation: Valid format values are: procedural, reference, anti-pattern
  ```
  Treat format as `procedural` and continue to sub-check (c).

**(c) Section contract check** — using the section detection rule (a section is present when a line STARTS with `## <name>` or `**<name>**` for Triggers), verify required sections per detected format:

- **procedural**: requires (i) `**Triggers**` or a line starting with `## Triggers`, (ii) `## Process` or at least one line starting with `### Step`, (iii) `## Rules`. For each missing required element:
  ```
  severity: MEDIUM
  check: P2
  title: SKILL.md for skill '<n>' (procedural) is missing required section: <section>
  detail: The required section <section> was not found in RUNTIME_ROOT/skills/<n>/SKILL.md.
  remediation: Add the missing section to the SKILL.md — procedural format requires: **Triggers**, ## Process (or ### Step N steps), and ## Rules
  ```

- **reference**: requires (i) `**Triggers**` or a line starting with `## Triggers`, (ii) `## Patterns` or `## Examples`, (iii) `## Rules`. For each missing required element:
  ```
  severity: MEDIUM
  check: P2
  title: SKILL.md for skill '<n>' (reference) is missing required section: <section>
  detail: The required section <section> was not found in RUNTIME_ROOT/skills/<n>/SKILL.md.
  remediation: Add the missing section to the SKILL.md — reference format requires: **Triggers**, ## Patterns or ## Examples, and ## Rules
  ```

- **anti-pattern**: requires (i) `**Triggers**` or a line starting with `## Triggers`, (ii) `## Anti-patterns`, (iii) `## Rules`. For each missing required element:
  ```
  severity: MEDIUM
  check: P2
  title: SKILL.md for skill '<n>' (anti-pattern) is missing required section: <section>
  detail: The required section <section> was not found in RUNTIME_ROOT/skills/<n>/SKILL.md.
  remediation: Add the missing section to the SKILL.md — anti-pattern format requires: **Triggers**, ## Anti-patterns, and ## Rules
  ```

**(d) Post-frontmatter body line count** — count lines after the closing `---` marker. If fewer than 30:
```
severity: LOW
check: P2
title: SKILL.md for skill '<n>' has very short body (<30 lines post-frontmatter) — may be a stub
detail: The post-frontmatter content of RUNTIME_ROOT/skills/<n>/SKILL.md has fewer than 30 lines.
remediation: Review and populate this SKILL.md — stubs should have a plan or be removed
```

**(e) TODO: marker check** — scan the entire file for any line containing `TODO:`. If found:
```
severity: INFO
check: P2
title: SKILL.md for skill '<n>' contains TODO: markers — may be a work-in-progress
```

---

#### Check P3 — Local-Path Registration Verification

**If P1 found no CLAUDE.md or no Skills Registry**:
```
severity: INFO
check: P3
title: P1 failed — local registration check skipped
```
Skip the rest of P3.

**Otherwise**, for each skill name `<n>` in `LOCAL_SKILLS`:

- If `PROJECT_ROOT/.claude/skills/<n>/` does **not** exist:
  ```
  severity: HIGH
  check: P3
  title: Local skill '<n>' registered in CLAUDE.md but not found at .claude/skills/<n>/
  detail: Expected at PROJECT_ROOT/.claude/skills/<n>/ — directory not found.
  remediation: Add the skill file at .claude/skills/<n>/SKILL.md or remove the registry entry from CLAUDE.md.
  ```

- If `PROJECT_ROOT/.claude/skills/<n>/` exists but `SKILL.md` is **absent**:
  ```
  severity: MEDIUM
  check: P3
  title: Local skill '<n>' directory present but SKILL.md missing
  detail: Directory exists at PROJECT_ROOT/.claude/skills/<n>/ but SKILL.md not found inside it.
  remediation: Restore SKILL.md at .claude/skills/<n>/SKILL.md.
  ```

If `LOCAL_SKILLS` is empty → record one INFO: "No local-tier skill registrations found in CLAUDE.md — check skipped."

**Phase C — SKILL.md content quality** (runs only for skills where SKILL.md exists and passed the Phase A/B reachability check above):

For each skill name `<n>` in `LOCAL_SKILLS` where `PROJECT_ROOT/.claude/skills/<n>/SKILL.md` exists:

**(a) Frontmatter presence** — read `PROJECT_ROOT/.claude/skills/<n>/SKILL.md`. If the file does NOT start with a `---` line:
```
severity: MEDIUM
check: P3
title: SKILL.md for skill '<n>' is missing YAML frontmatter — the file must begin with a '---' block
detail: The file at PROJECT_ROOT/.claude/skills/<n>/SKILL.md does not begin with a YAML frontmatter block (---).
remediation: Add a YAML frontmatter block (---) with at minimum name:, description:, and format: fields
```
Skip sub-checks (b), (c), (d), (e) for this skill and continue to the next skill.

**(b) `format:` field extraction** — scan the lines between the opening `---` and the closing `---` marker. Look for a line starting with `format:` and extract its value (trimmed).

- If no `format:` field found:
  ```
  severity: LOW
  check: P3
  title: SKILL.md for skill '<n>' has no 'format:' field in frontmatter — defaulting to 'procedural'
  detail: No format: line found inside the YAML frontmatter block of PROJECT_ROOT/.claude/skills/<n>/SKILL.md.
  remediation: Add 'format: procedural' (or 'reference' or 'anti-pattern') to the SKILL.md frontmatter
  ```
  Treat format as `procedural` and continue to sub-check (c).

- If `format:` value is not one of `procedural`, `reference`, `anti-pattern`:
  ```
  severity: LOW
  check: P3
  title: SKILL.md for skill '<n>' has unrecognized format value '<value>' — defaulting to 'procedural'
  detail: The format: field in PROJECT_ROOT/.claude/skills/<n>/SKILL.md contains an unrecognized value '<value>'.
  remediation: Valid format values are: procedural, reference, anti-pattern
  ```
  Treat format as `procedural` and continue to sub-check (c).

**(c) Section contract check** — using the section detection rule (a section is present when a line STARTS with `## <name>` or `**<name>**` for Triggers), verify required sections per detected format:

- **procedural**: requires (i) `**Triggers**` or a line starting with `## Triggers`, (ii) `## Process` or at least one line starting with `### Step`, (iii) `## Rules`. For each missing required element:
  ```
  severity: MEDIUM
  check: P3
  title: SKILL.md for skill '<n>' (procedural) is missing required section: <section>
  detail: The required section <section> was not found in PROJECT_ROOT/.claude/skills/<n>/SKILL.md.
  remediation: Add the missing section to the SKILL.md — procedural format requires: **Triggers**, ## Process (or ### Step N steps), and ## Rules
  ```

- **reference**: requires (i) `**Triggers**` or a line starting with `## Triggers`, (ii) `## Patterns` or `## Examples`, (iii) `## Rules`. For each missing required element:
  ```
  severity: MEDIUM
  check: P3
  title: SKILL.md for skill '<n>' (reference) is missing required section: <section>
  detail: The required section <section> was not found in PROJECT_ROOT/.claude/skills/<n>/SKILL.md.
  remediation: Add the missing section to the SKILL.md — reference format requires: **Triggers**, ## Patterns or ## Examples, and ## Rules
  ```

- **anti-pattern**: requires (i) `**Triggers**` or a line starting with `## Triggers`, (ii) `## Anti-patterns`, (iii) `## Rules`. For each missing required element:
  ```
  severity: MEDIUM
  check: P3
  title: SKILL.md for skill '<n>' (anti-pattern) is missing required section: <section>
  detail: The required section <section> was not found in PROJECT_ROOT/.claude/skills/<n>/SKILL.md.
  remediation: Add the missing section to the SKILL.md — anti-pattern format requires: **Triggers**, ## Anti-patterns, and ## Rules
  ```

**(d) Post-frontmatter body line count** — count lines after the closing `---` marker. If fewer than 30:
```
severity: LOW
check: P3
title: SKILL.md for skill '<n>' has very short body (<30 lines post-frontmatter) — may be a stub
detail: The post-frontmatter content of PROJECT_ROOT/.claude/skills/<n>/SKILL.md has fewer than 30 lines.
remediation: Review and populate this SKILL.md — stubs should have a plan or be removed
```

**(e) TODO: marker check** — scan the entire file for any line containing `TODO:`. If found:
```
severity: INFO
check: P3
title: SKILL.md for skill '<n>' contains TODO: markers — may be a work-in-progress
```

---

#### Check P4 — Orphaned Local Skills

Enumerate all directories under `PROJECT_ROOT/.claude/skills/` that contain a `SKILL.md` file.

**If `.claude/skills/` does not exist at `PROJECT_ROOT`**:
```
severity: INFO
check: P4
title: No .claude/skills/ directory found — orphan check skipped
```
Skip the rest of P4.

**If `.claude/skills/` exists but is empty**:
```
severity: INFO
check: P4
title: .claude/skills/ is empty — no local skills to check
```
Skip the rest of P4.

**Otherwise**, for each skill directory name `<n>` found on disk that is **NOT** in `LOCAL_SKILLS`:
```
severity: MEDIUM
check: P4
title: Local skill '<n>' found at .claude/skills/ but not registered in CLAUDE.md Skills Registry
detail: Directory PROJECT_ROOT/.claude/skills/<n>/ exists on disk but has no corresponding entry in the Skills Registry.
remediation: Register the skill in the CLAUDE.md Skills Registry, or remove the directory if no longer needed.
```

---

#### Check P5 — Scope Tier Overlap

**If P1 found no Skills Registry**:
```
severity: INFO
check: P5
title: P1 failed — scope tier overlap check skipped
```
Skip the rest of P5.

**Otherwise**, for each skill name `<n>` in `LOCAL_SKILLS`:

- If `RUNTIME_ROOT/skills/<n>/` also exists (global tier):
  ```
  severity: LOW
  check: P5
  title: Skill '<n>' exists in both .claude/skills/ (local) and ~/.claude/skills/ (global)
  detail: This is expected for intentional global overrides; verify the intended tier is active.
  remediation: Confirm which tier is authoritative for this project; consult ADR-008.
  ```

> Severity MUST NOT exceed LOW for P5 findings regardless of count.

If `LOCAL_SKILLS` is empty → record one INFO: "No local-tier skills registered — scope tier overlap check skipped."

---

#### Check P6 — Memory Layer (ai-context/)

Test for the `PROJECT_ROOT/ai-context/` directory.

**If `PROJECT_ROOT/ai-context/` does NOT exist**:
```
severity: MEDIUM
check: P6
title: ai-context/ directory not found — project memory layer is absent
detail: No ai-context/ directory found at PROJECT_ROOT/ai-context/. The project memory layer (stack, architecture, conventions, known-issues, changelog) has not been initialized.
remediation: Run /memory-init to generate the ai-context/ layer for this project
```
Skip all file sub-checks below and proceed to Check P7.

**If `PROJECT_ROOT/ai-context/` exists**, check for each of the five required core files:

Required core files: `stack.md`, `architecture.md`, `conventions.md`, `known-issues.md`, `changelog-ai.md`

For each file that is **absent**:
```
severity: LOW
check: P6
title: ai-context/<filename> is missing
detail: The file PROJECT_ROOT/ai-context/<filename> was not found. This file is part of the required project memory layer.
remediation: Run /memory-init or manually create ai-context/<filename> to restore the project memory layer
```

For each file that is **present**, count its lines. If fewer than 10 lines:
```
severity: INFO
check: P6
title: ai-context/<filename> is very short (<10 lines) — may not contain useful context
```

If all five files are present and no files have fewer than 10 lines → no finding for this check.

> Severity cap: P6 MUST NOT produce findings above MEDIUM.

---

#### Check P7 — Feature Domain Knowledge Layer (ai-context/features/)

Test for the `PROJECT_ROOT/ai-context/features/` directory.

**If `PROJECT_ROOT/ai-context/features/` does NOT exist**:
```
severity: INFO
check: P7
title: ai-context/features/ not found — feature-domain knowledge layer not initialized for this project
```
No further sub-checks. Proceed to Check P8.

**If `PROJECT_ROOT/ai-context/features/` exists**:

**(a) Template file check** — if `_template.md` exists in the directory:
```
severity: INFO
check: P7
title: ai-context/features/_template.md is present
```

**(b) Non-template file inventory** — collect all files whose name does NOT start with `_` (these are authored feature domain knowledge files).

If no such files exist (the directory contains only files starting with `_`, or is empty):
```
severity: INFO
check: P7
title: ai-context/features/ contains only template/stub files — no feature domain knowledge files authored yet
```
No further sub-checks. Proceed to Check P8.

**(c) Section and stub checks** — for each non-template feature file `<name>.md`:

Check for the following six required section headings using the line-prefix rule (a section is present when at least one line in the file STARTS with `## <section-name>`):
- `## Domain Overview`
- `## Business Rules and Invariants`
- `## Data Model Summary`
- `## Integration Points`
- `## Decision Log`
- `## Known Gotchas`

For each missing section:
```
severity: LOW
check: P7
title: Feature file 'ai-context/features/<name>.md' is missing section: <section-name>
detail: No line starting with "## <section-name>" was found in the feature file.
remediation: Add the missing section to the feature file — refer to ai-context/features/_template.md for the required structure
```

Count total lines in the file. If fewer than 30 lines:
```
severity: INFO
check: P7
title: Feature file 'ai-context/features/<name>.md' is very short (<30 lines) — likely a stub not yet populated
```

> Severity cap: P7 MUST NOT produce any findings above LOW. This is per ADR-015 non-blocking design intent.

---

#### Check P8 — .claude/ Folder Inventory

Enumerate all items (files and directories) directly under `PROJECT_CLAUDE_DIR` (one level only — NOT recursive).

**Expected item set**:
```
CLAUDE.md
skills/
audit-report.md
claude-folder-audit-report.md
settings.json
settings.local.json
openspec/
ai-context/
hooks/
```

For each item found directly under `PROJECT_CLAUDE_DIR` that is **NOT** in the expected item set:
```
severity: MEDIUM
check: P8
title: Unexpected item in .claude/: '<name>' — possible manual edit or stale artifact
detail: The item PROJECT_CLAUDE_DIR/<name> does not correspond to any known expected item in .claude/.
remediation: Review the item manually; if it should not be there, remove it; if it is intentional, consider documenting it in .claude/CLAUDE.md
```

**Hooks sub-check** — if `PROJECT_CLAUDE_DIR/hooks/` exists:

Enumerate all `.js` and `.sh` files within `PROJECT_CLAUDE_DIR/hooks/`. For each file that is empty (0 bytes or whitespace only):
```
severity: LOW
check: P8
title: Hook script '.claude/hooks/<filename>' is empty — likely a placeholder
detail: The file PROJECT_CLAUDE_DIR/hooks/<filename> contains no executable content.
remediation: Populate the hook script with valid logic or remove it if not needed
```

If all `.js` and `.sh` files in `hooks/` are non-empty → no finding from the hooks sub-check.

**If `PROJECT_CLAUDE_DIR/hooks/` does NOT exist**:
```
severity: INFO
check: P8
title: No hooks/ directory found in .claude/ — hook execution is not configured for this project
```

**If all items found are within the expected set** → record one INFO:
```
severity: INFO
check: P8
title: .claude/ inventory clean — <N> item(s) found, all expected
```

> Severity cap: P8 MUST NOT produce findings above MEDIUM.

---

**If `MODE = global-config` or `MODE = global`** — run Checks 1–5 below (skip Checks P1–P8):

---

#### Check 1 — Runtime Structure

Verify that the following top-level directories exist inside `RUNTIME_ROOT`:
- `skills/`
- `openspec/`
- `ai-context/`
- `memory/`
- `hooks/`

Also verify that `RUNTIME_ROOT/CLAUDE.md` exists as a file.

For each **missing directory**, record:
```
severity: HIGH
check: 1
title: Required directory missing: ~/.claude/<dir>/
detail: The directory does not exist in the runtime root.
remediation: Run install.sh from the agent-config repo
```

If `CLAUDE.md` is **absent** from `RUNTIME_ROOT`, record:
```
severity: HIGH
check: 1
title: CLAUDE.md missing from ~/.claude/
detail: The CLAUDE.md file is not present at the runtime root.
remediation: Run install.sh from the agent-config repo
```

If all required directories and CLAUDE.md are present → no finding for this check.

---

#### Check 2 — Skill Deployment Completeness

**If `MODE = global`** (no source `skills/` directory readable from cwd):

Record one INFO note:
```
severity: INFO
check: 2
title: Source repo not detected — skill deployment completeness check skipped
detail: No skills/ directory found at the current working directory.
```

Skip the rest of Check 2.

**If `MODE = global-config`** (source `skills/` exists at cwd):

1. List all subdirectories under `SOURCE_ROOT/skills/`. These are the expected source skills.
2. For each source skill `<name>`:
   - If `RUNTIME_ROOT/skills/<name>/` does **not** exist → record:
     ```
     severity: HIGH
     check: 2
     title: Skill '<name>' present in source but not deployed to ~/.claude/skills/
     detail: Source path: SOURCE_ROOT/skills/<name>/ — Runtime path: RUNTIME_ROOT/skills/<name>/ does not exist.
     remediation: Run install.sh from the agent-config repo
     ```
   - If `RUNTIME_ROOT/skills/<name>/` exists but `RUNTIME_ROOT/skills/<name>/SKILL.md` does **not** → record:
     ```
     severity: MEDIUM
     check: 2
     title: Deployed skill '<name>' has no SKILL.md — directory may be empty or corrupt
     detail: The directory exists at RUNTIME_ROOT/skills/<name>/ but SKILL.md is absent.
     remediation: Run install.sh to restore the skill file
     ```

---

#### Check 3 — Installation Drift Detection

**If `MODE = global`** (no source repo detected):

Record one INFO note:
```
severity: INFO
check: 3
title: No source repo detected — drift check skipped
```

Skip the rest of Check 3.

**If `MODE = global-config`**:

Attempt to read the modification time (mtime) of:
- `SOURCE_ROOT` (the source repo root directory)
- `RUNTIME_ROOT` (the `~/.claude/` runtime directory)

If **either mtime cannot be read** (filesystem access error):
```
severity: INFO
check: 3
title: Could not read directory mtime for drift comparison — check skipped
detail: mtime-based drift detection requires read access to both directories.
```

If **source repo mtime is more recent than runtime mtime**:
```
severity: MEDIUM
check: 3
title: Possible installation drift — source repo appears newer than ~/.claude/ (mtime proxy)
detail: Source mtime: <ISO 8601 timestamp> / Runtime mtime: <ISO 8601 timestamp>
        Note: mtime comparison is an approximate proxy. Re-running install.sh is always safe.
remediation: Run install.sh from the agent-config repo to re-sync runtime with source repo
```

If **runtime mtime is equal to or more recent than source mtime** → no finding for this check.

> **Known limitation**: mtime is an imprecise proxy for deployment state. A `.installed-at` metadata file (future improvement) would provide exact tracking.

---

#### Check 4 — Orphaned Artifact Detection

List all items (files and directories) directly under `RUNTIME_ROOT` (one level only — not recursive).

Build the **expected item set** from:
- All top-level items in `SOURCE_ROOT/` (if global-config mode) — these were deployed by `install.sh`
- Known runtime-only items: `CLAUDE.md`, `settings.json`, `settings.local.json`, `claude-folder-audit-report.md`, `.installed-at`, `audit-report.md`

For each item found in `RUNTIME_ROOT` that is **not** in the expected item set:

- If the item is inside `openspec/changes/` (subdirectory of `openspec/changes/`) → record:
  ```
  severity: INFO
  check: 4
  title: Work-in-progress SDD change directories found in runtime openspec/changes/
  detail: These are expected SDD artifacts, not orphans.
  ```

- Otherwise → record (severity capped at MEDIUM regardless of count):
  ```
  severity: MEDIUM
  check: 4
  title: Unexpected item in ~/.claude/: <name> — possible manual edit or stale artifact
  detail: This item does not correspond to any source repo item or known runtime-only artifact.
  remediation: Review manually; run install.sh if this file should not exist; do NOT delete without inspection
  ```

If all items are in the expected set → no finding for this check.

**Note**: In `global` mode without a source repo, the expected set is the list of known runtime-only items only. Any item not in that list is flagged as MEDIUM.

---

#### Check 5 — Scope Tier Compliance

Check for skills present in the project-local `.claude/skills/` directory (relative to cwd) that overlap with or are missing from the global catalog.

**If `.claude/skills/` does not exist** at the cwd:

Record one INFO note:
```
severity: INFO
check: 5
title: No project-local .claude/skills/ found — scope tier compliance check skipped for project-local tier
```

Then list global tier contents as INFO only:
```
severity: INFO
check: 5
title: Global tier contains <N> skill(s): [comma-separated list]
```

Skip the rest of Check 5.

**If `.claude/skills/` exists** at the cwd:

List all subdirectories under `.claude/skills/`. For each `<name>`:

1. If `RUNTIME_ROOT/skills/<name>/` also exists (global tier):
   ```
   severity: LOW
   check: 5
   title: Skill '<name>' exists in both global (~/.claude/skills/) and project-local (.claude/skills/) tiers
   detail: This is expected for intentional global overrides; verify the intended tier is active.
   remediation: Confirm which tier is authoritative for this project; consult ADR 008
   ```

2. If `SOURCE_ROOT/skills/<name>/` does **not** exist (global catalog gap) — global-config mode only:
   ```
   severity: MEDIUM
   check: 5
   title: Project-local skill '<name>' has no counterpart in the global catalog (skills/)
   detail: The skill exists only in the project-local tier and has not been promoted to the global catalog.
   remediation: If intentional, register the skill in CLAUDE.md; if not, consider adding it to skills/
   ```

---

### Step 4 — Generate report

Determine the report write path by mode:
- `MODE = project` → write to `PROJECT_ROOT/.claude/claude-folder-audit-report.md`
- `MODE = global-config` or `MODE = global` → write to `RUNTIME_ROOT/claude-folder-audit-report.md`

**Overwrite** any previous report (do not append).

**Project-mode report format** (`MODE = project`):

```markdown
# .claude/ Project Audit Report

Run date: <RUN_DATE>
Mode: project
Project root: <PROJECT_ROOT>
CLAUDE.md: <PROJECT_CLAUDE_DIR>/CLAUDE.md
Summary: <N> HIGH, <N> MEDIUM, <N> LOW, <N> INFO

---

## Findings Summary

| Severity | Check | Description | Remediation |
|----------|-------|-------------|-------------|
...
| — | — | No HIGH / MEDIUM / LOW findings | — |

---

## Check P1 — CLAUDE.md Presence and Skills Registry

[findings or "No findings."]

---

## Check P2 — Global-Path Registration Verification

[findings or "No findings."]

---

## Check P3 — Local-Path Registration Verification

[findings or "No findings."]

---

## Check P4 — Orphaned Local Skills

[findings or "No findings."]

---

## Check P5 — Scope Tier Overlap

[findings or "No findings."]

---

## Check P6 — Memory Layer (ai-context/)

[findings or "No findings."]

---

## Check P7 — Feature Domain Knowledge Layer (ai-context/features/)

[findings or "No findings."]

---

## Check P8 — .claude/ Folder Inventory

[findings or "No findings."]

---

## Recommended Next Steps

<!-- If HIGH findings exist: -->
1. Fix .claude/CLAUDE.md (P1 findings) or run /project-setup to initialize project config
2. Run install.sh from agent-config repo to deploy missing global skills (P2 findings)
3. Add missing SKILL.md files or remove stale registry entries (P3/P4 findings)
4. Review LOW findings at your discretion

<!-- If highest-severity is MEDIUM from P6 (ai-context/ absent): -->
1. Run /memory-init to generate the ai-context/ memory layer for this project
2. Review LOW findings at your discretion

<!-- If highest-severity is MEDIUM from P8 (unexpected .claude/ item): -->
1. Review the unexpected item(s) in .claude/ manually; if intentional, document in .claude/CLAUDE.md; if not, remove the item
2. Review LOW findings at your discretion

<!-- If no HIGH or MEDIUM findings across all 8 checks: -->
Project Claude configuration appears healthy — no required actions detected.
[Optional: list LOW/INFO items as review notes]

---

> This file is a runtime artifact. Add `.claude/claude-folder-audit-report.md` to `.gitignore` to prevent accidental commits.
```

**Global-config / global report format** (`MODE = global-config` or `MODE = global`):

```markdown
# ~/.claude/ Audit Report

Run date: <RUN_DATE>
Mode: <MODE>
Runtime root: <RUNTIME_ROOT>
Source root: <SOURCE_ROOT>
Summary: <N> HIGH, <N> MEDIUM, <N> LOW, <N> INFO

---

## Findings Summary

| Severity | Check | Description | Remediation |
|----------|-------|-------------|-------------|
...
| — | — | No HIGH / MEDIUM / LOW findings | — |

---

## Check 1 — Runtime Structure

[findings or "No findings."]

---

## Check 2 — Skill Deployment Completeness

[findings or "No findings."]

---

## Check 3 — Installation Drift

[findings or "No findings."]

---

## Check 4 — Orphaned Artifacts

[findings or "No findings."]

---

## Check 5 — Scope Tier Compliance

[findings or "No findings."]

---

## Recommended Next Steps

<!-- If HIGH findings exist: -->
1. Run install.sh from the agent-config repo to re-sync the runtime with the source
2. [additional steps for MEDIUM findings]
3. Review LOW findings at your discretion

<!-- If no HIGH or MEDIUM findings: -->
Runtime appears healthy — no required actions detected.
[Optional: list LOW/INFO items as review notes]
```

Severity labels in the report body MUST use bold Markdown: `**HIGH**`, `**MEDIUM**`, `**LOW**`, `**INFO**`.

The report MUST NOT suggest deleting any file without "Review manually" as a prerequisite step.

---

### Step 5 — Output summary to user

After writing the report, display to the user:

**If `MODE = project`**:
```
## .claude/ Project Audit Complete

Mode: project
Project root: <PROJECT_ROOT>

Findings:
  HIGH:   N
  MEDIUM: N
  LOW:    N
  INFO:   N

Report written to: <PROJECT_ROOT>/.claude/claude-folder-audit-report.md

[If HIGH > 0]:   ⚠️  Action required — see HIGH findings in the report.
[If HIGH = 0 and MEDIUM = 0]:  ✓  Project .claude/ configuration appears healthy.
```

**If `MODE = global-config` or `MODE = global`**:
```
## ~/.claude/ Audit Complete

Mode: <MODE>
Runtime root: <RUNTIME_ROOT>

Findings:
  HIGH:   N
  MEDIUM: N
  LOW:    N
  INFO:   N

Report written to: <RUNTIME_ROOT>/claude-folder-audit-report.md

[If HIGH > 0]:   ⚠️  Action required — see HIGH findings in the report.
[If HIGH = 0 and MEDIUM = 0]:  ✓  Runtime appears healthy.
```

---

## Rules

- Run all checks even if earlier checks produce HIGH findings — never abort early
- Severity caps: Check 3 (drift) MUST NOT exceed MEDIUM; Check 4 (orphaned artifacts) MUST NOT exceed MEDIUM; Check P5 (scope tier overlap) MUST NOT exceed LOW; P6 (memory layer) MUST NOT exceed MEDIUM; P7 (feature domain knowledge layer) MUST NOT exceed LOW; P8 (.claude/ folder inventory) MUST NOT exceed MEDIUM
- Path normalization MUST use the explicit env var priority chain — NEVER rely on shell tilde expansion
- The report file MUST be overwritten on every run (never appended)
- All displayed paths in report and output MUST use forward slashes
- INFO observations MAY omit the `Remediation:` line; HIGH, MEDIUM, and LOW findings MUST include one
- INFO findings from check sections MUST NOT appear in the Findings Summary table — the Findings Summary table covers HIGH, MEDIUM, and LOW findings only
- The report MUST be valid Markdown — all section headers use `##`, all finding labels use bold (`**HIGH**`, etc.)
- The skill MUST NOT emit any finding that recommends deleting a file without human review as a prerequisite
- On Windows, all path operations MUST use `$USERPROFILE` (not `~`) for the home directory
- In `project` mode, the skill MUST NOT audit `~/.claude/` as the primary target; references to `~/.claude/` are only for P2 and P5 reachability checks
- In `project` mode, the report MUST be written to `<PROJECT_ROOT>/.claude/claude-folder-audit-report.md` — NEVER to `~/.claude/`
- Section detection rule: a section is present when a line STARTS with `## <section-name>` (top-level heading, no leading whitespace); lines inside fenced code blocks are not considered; the bold-trigger pattern (`**Triggers**`) is also valid for the Triggers section specifically
- The `name:` field is NOT a required frontmatter check in P2/P3 sub-checks — only `format:` is validated in addition to frontmatter presence

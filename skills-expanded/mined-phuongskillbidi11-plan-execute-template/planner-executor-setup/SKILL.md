# Skill: planner-executor-setup

---

## Purpose

Bootstrap the Planner-Executor workflow into any new project so that Claude acts as Planner and GitHub Copilot acts as Executor, with Karpathy principles enforced throughout. This skill documents the complete setup process, file structure, and verification steps so a new project can be fully configured in under five minutes.

---

## When to use

Load this skill when:

- Starting a new project from scratch and wanting to install the workflow
- Onboarding a project that does not yet have `.claude/`, `.github/copilot-instructions.md`, or a `skills/` directory
- Recreating or repairing the workflow after the config files were deleted or corrupted
- Explaining the workflow to a new team member who will act as the relay between Claude and Copilot

---

## Files involved

| File | Role |
|---|---|
| `CLAUDE.md` | Loaded automatically by Claude Code; defines project context, build commands, Karpathy principles reminder, and skill system pointer |
| `.claude/planner-instructions.md` | Claude's full role definition as Planner — Karpathy principles, skill loading protocol, plan format rules |
| `.github/copilot-instructions.md` | Copilot's full role definition as Executor — how to read plans, run tests, mark tasks, stop on failure |
| `scripts/init.sh` | One-command setup: copies template files, detects project type, writes config |
| `scripts/detect-project.sh` | Detects ESP-IDF / Rust / Node / Python / Go / CMake / Make and outputs build+test commands |
| `scripts/plan-executor.sh` | CLI helper: `new`, `list`, `status`, `open`, `test` commands for managing plans |
| `scripts/load_skill.sh` | `list` prints manifest; `<name>` prints a skill's full content |
| `scripts/update-manifest.sh` | Scans `skills/*/SKILL.md` and regenerates `skills/manifest.json` |
| `.planner-executor/config.yaml` | Per-project config: `build_cmd`, `test_cmd`, `run_cmd`, `lint_cmd`, `env_setup` |
| `.planner-executor/config.yaml.template` | Schema/template — copied and populated by `init.sh` |
| `skills/manifest.json` | Index of all available skills (name, description, path) |
| `skills/example/SKILL.md` | Blank skill template — copy this to add new skills |
| `.plans/` | All plan folders live here, named `YYYY-MM-DD-feature-name/` |

---

## Constraints and gotchas

- **`CLAUDE.md` is user-owned** — `init.sh --upgrade` never overwrites it. Edit it freely after init.
- **`skills/manifest.json` is auto-generated** — never edit it by hand. Always use `update-manifest.sh`.
- **Plans are permanent records** — never delete `.plans/` folders. They document design decisions.
- **`init.sh` is idempotent** — running it twice on the same project is safe; it skips files that already exist.
- **The workflow requires no internet** — everything is local files and local scripts.
- **Copilot must run from WSL** (on Windows) — open VS Code with `code .` from the WSL terminal to avoid UNC path errors with `\\wsl.localhost\...`.

---

## Patterns

### Plan folder structure
```
.plans/
└── YYYY-MM-DD-feature-name/
    ├── spec.md      # Goal, key discoveries, design, files changed, out of scope
    ├── tasks.md     # Ordered [ ] checklist with exact file + line references
    └── tests.md     # Acceptance criteria with exact Pass/Fail conditions
```

### Invoking Claude as Planner
```
Claude, create a plan for <feature>.
Save it to .plans/YYYY-MM-DD-<feature-name>/
Include spec.md, tasks.md, and tests.md.
Follow .claude/planner-instructions.md.
```

### Invoking Copilot as Executor
```
Read the plan in .plans/YYYY-MM-DD-<feature-name>/
Start with spec.md, then tasks.md, then tests.md.
Implement each task in order.
Run the test from tests.md after each task.
Mark [x] when the test passes.
Stop and report the exact error if a test fails.
```

### Relaying a failure back to Claude
```
Claude, Copilot failed on Task 2.1 of .plans/2025-05-01-my-feature/
Error: <exact compiler or test output>
Context: <what Copilot changed>
Please update tasks.md with a corrected approach for that task only.
```

---

## Step-by-step

### Option A — Using `init.sh` (recommended for new projects)

1. **Clone or copy the template** into a staging folder:
   ```bash
   git clone https://github.com/your-org/planner-executor-template /tmp/pe-template
   # or: unzip the downloaded template archive
   ```

2. **Navigate to your target project root:**
   ```bash
   cd ~/projects/my-new-project
   ```

3. **Run init.sh:**
   ```bash
   bash /tmp/pe-template/scripts/init.sh
   ```
   The script will:
   - Copy all template files (skipping any that already exist)
   - Detect your project type and fill in `build_cmd`, `test_cmd`, `run_cmd`
   - Write `.planner-executor/config.yaml`
   - Populate placeholders in `CLAUDE.md`

4. **Review and edit `CLAUDE.md`:**
   - Fill in `[PROJECT_NAME]`, `[PROJECT_TYPE]`, architecture description, key files
   - Correct any wrongly-detected commands in `.planner-executor/config.yaml`

5. **Enable Copilot instruction files in VS Code** (one-time, per machine):
   ```json
   // .vscode/settings.json
   { "github.copilot.chat.useInstructionFiles": true }
   ```

6. **Verify Copilot loaded the instructions:**
   Open Copilot Chat → type: `What are my project instructions?`
   Expected: Copilot describes the Executor role from `.github/copilot-instructions.md`.

---

### Option B — Manual copy (for projects that cannot run bash scripts)

1. Copy these files from the template into your project root, preserving paths:
   ```
   CLAUDE.md
   .claude/planner-instructions.md
   .github/copilot-instructions.md
   scripts/plan-executor.sh
   scripts/load_skill.sh
   scripts/update-manifest.sh
   skills/example/SKILL.md
   skills/manifest.json
   .planner-executor/config.yaml.template
   ```

2. Rename `.planner-executor/config.yaml.template` → `.planner-executor/config.yaml`
   and fill in the values manually.

3. Replace all `[PLACEHOLDER]` values in `CLAUDE.md` with your project's specifics.

4. Make scripts executable:
   ```bash
   chmod +x scripts/*.sh
   ```

---

## Verification (smoke test)

Run these steps after setup to confirm everything works end-to-end:

### V1 — Skill list loads
```bash
./scripts/load_skill.sh list
```
**Pass:** At least one skill printed (e.g., `example`, `planner-executor-setup`).  
**Fail:** "No manifest found" → run `./scripts/update-manifest.sh` first.

### V2 — Plan scaffold works
```bash
./scripts/plan-executor.sh new smoke-test
```
**Pass:** `.plans/YYYY-MM-DD-smoke-test/` created with three empty template files.  
**Fail:** Error about missing directory → confirm you are in the project root.

### V3 — Config test command runs
```bash
./scripts/plan-executor.sh test
```
**Pass:** Build and test commands from `.planner-executor/config.yaml` execute without script errors (the commands themselves may fail if the project is not yet built — that is fine).  
**Fail:** "No commands found" → check `.planner-executor/config.yaml` has `build_cmd` set.

### V4 — Copilot reads the plan (manual)
1. Open VS Code Copilot Chat.
2. Type: `Implement the plan from .plans/YYYY-MM-DD-smoke-test/`
3. **Pass:** Copilot reads all three files and describes what it will do before touching any code.
4. **Fail:** Copilot says it cannot find the files → reopen VS Code from WSL terminal with `code .`.

---

## Adding project-specific skills

Each new skill captures domain knowledge for one area of your codebase so Claude plans more accurately without you having to repeat context.

```bash
# 1. Copy the example template
cp -r skills/example/ skills/my-area/

# 2. Edit skills/my-area/SKILL.md
#    Fill in: Purpose, When to use, Files involved,
#             Constraints, Patterns, Step-by-step, Tests

# 3. Register it
./scripts/update-manifest.sh
```

**Good skill candidates** (one skill per area):

| Area | Skill name suggestion |
|---|---|
| Web UI / frontend | `web-ui` |
| REST API / HTTP handlers | `api` |
| Build and flash (embedded) | `build-flash` |
| Database / migrations | `database` |
| Authentication | `auth` |
| CI/CD pipeline | `ci` |
| Camera / sensor driver | `camera` |

Once registered, Claude will see the skill in `manifest.json` and load it
automatically when your request matches — without you having to paste anything.

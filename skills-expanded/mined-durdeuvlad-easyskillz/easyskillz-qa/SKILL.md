---
name: easyskillz-qa
description: Comprehensive QA workflow for easyskillz CLI - build, install locally, and test all flows.
---
# easyskillz-qa

**Comprehensive QA workflow for easyskillz CLI - build, install locally, and test all flows.**

## Purpose

Automatically build the easyskillz package, install it in a temporary test environment, and run exhaustive tests covering:
- All command flows (skill, tool, project, docs domains)
- AI-first design principles (one-shot execution, AI detection)
- Error handling and edge cases
- Command design philosophy compliance
- User experience friction points

## When to Use

Run this skill whenever:
- You've made changes to easyskillz and want to verify everything works
- Before publishing a new version
- After refactoring or adding new features
- When investigating bug reports
- To validate the entire user experience

## Workflow

### 1. Build Package Locally

```bash
# In the easyskillz project root
npm pack
```

This creates a tarball like `easyskillz-2.0.0-alpha.4.tgz` in the current directory.

### 2. Create Temporary Test Environment

```bash
# Create temp directory (gitignored)
mkdir -p .qa-temp/test-project
cd .qa-temp/test-project

# Initialize a test project
npm init -y

# Create AI tool config files to simulate real environment
echo "# Test Project" > CLAUDE.md
echo "# Test Project" > AGENTS.md
echo "root = true" > .cursorrules
```

### 3. Install Local Package

```bash
# Install from the tarball (not from npm)
npm install -g ../../easyskillz-*.tgz
```

### 4. Test All Command Flows

#### A. Project Sync Flow (AI One-Shot)

**Test:** One-shot execution with all flags
```bash
easyskillz project sync --docs=yes --docs-strategy=unified --gitignore=full
```

**Expected:**
- ✅ No interactive prompts
- ✅ Detects tools (claude, codex, cursor)
- ✅ Creates `.easyskillz/` structure
- ✅ Wires skills via symlinks
- ✅ Centralizes docs to `.easyskillz/docs/`
- ✅ Updates `.gitignore`
- ✅ Exit code 0

**Verify:**
- [ ] `.easyskillz/easyskillz.json` exists with correct config
- [ ] `.easyskillz/skills/` directory exists
- [ ] `.easyskillz/docs/INSTRUCTION.md` exists (unified strategy)
- [ ] `.gitignore` contains easyskillz entries
- [ ] Tool directories (`.claude/skills/`, `.codex/skills/`, `.cursor/skills/`) exist
- [ ] Meta-skill `easyskillz-reference` is present

#### B. Project Sync Flow (Interactive - Human)

**Test:** Interactive prompts for humans
```bash
# Delete config first
rm .easyskillz/easyskillz.json

# Run without flags (should prompt)
echo -e "y\n1\n1\n" | easyskillz project sync
```

**Expected:**
- ✅ Prompts: "Manage instruction files? [Y/n]"
- ✅ Prompts: "Strategy? [1=unified, 2=tool-specific]"
- ✅ Prompts: "Gitignore strategy? [1=full, 2=conflict-only, 3=none]"
- ✅ Same outcome as one-shot

**Verify:**
- [ ] Config saved with user choices
- [ ] No crashes or errors

#### C. Skill Management Flow

**Test:** Add skill
```bash
easyskillz skill add test-skill
```

**Expected:**
- ✅ Creates `.easyskillz/skills/test-skill/SKILL.md`
- ✅ Wires to all registered tools
- ✅ Shows confirmation message

**Verify:**
- [ ] Skill file exists
- [ ] Symlinks created in `.claude/skills/test-skill/`, `.codex/skills/test-skill/`, `.cursor/skills/test-skill/`

**Test:** List skills
```bash
easyskillz skill list
```

**Expected:**
- ✅ Shows `test-skill` in active skills
- ✅ Shows meta-skills (easyskillz-reference, etc.)

**Test:** Deactivate skill
```bash
easyskillz skill deactivate test-skill
```

**Expected:**
- ✅ Renames to `.test-skill.disabled`
- ✅ Removes symlinks from tools
- ✅ Shows restore command

**Verify:**
- [ ] `.easyskillz/skills/.test-skill.disabled/` exists
- [ ] Symlinks removed from tool directories

**Test:** Activate skill
```bash
easyskillz skill activate test-skill
```

**Expected:**
- ✅ Restores from `.test-skill.disabled` to `test-skill`
- ✅ Re-wires symlinks

**Test:** Remove skill (AI mode - requires --confirm)
```bash
easyskillz skill remove test-skill --confirm
```

**Expected:**
- ✅ Permanently deletes skill
- ✅ No prompts (flag provided)
- ✅ Removes all symlinks

**Verify:**
- [ ] Skill directory deleted
- [ ] Symlinks removed

#### D. Tool Management Flow

**Test:** List tools
```bash
easyskillz tool list
```

**Expected:**
- ✅ Shows registered tools (claude, codex, cursor)

**Test:** Register new tool
```bash
easyskillz tool register windsurf
```

**Expected:**
- ✅ Adds to config
- ✅ Wires all existing skills
- ✅ Updates instruction file
- ✅ Updates .gitignore

**Test:** Unregister tool (AI mode)
```bash
easyskillz tool unregister windsurf --mode=revert --confirm
```

**Expected:**
- ✅ Removes from config
- ✅ Keeps tool directory (revert mode)
- ✅ No prompts

**Test:** Unregister tool (full delete)
```bash
# Register again first
easyskillz tool register windsurf
easyskillz tool unregister windsurf --mode=full --confirm
```

**Expected:**
- ✅ Removes from config
- ✅ Deletes tool directory

#### E. Docs Management Flow

**Test:** List docs
```bash
easyskillz docs list
```

**Expected:**
- ✅ Shows centralized instruction files
- ✅ Shows strategy (unified or tool-specific)

**Test:** Sync docs
```bash
# Create a new instruction file
echo "# New Doc" > NEW_INSTRUCTION.md

easyskillz docs sync
```

**Expected:**
- ✅ Detects new file
- ✅ Centralizes to `.easyskillz/docs/`

#### F. JSON Output Flow

**Test:** All commands with --json flag
```bash
easyskillz skill list --json
easyskillz tool list --json
easyskillz docs list --json
```

**Expected:**
- ✅ Valid JSON output
- ✅ Contains `ok: true` field
- ✅ Contains relevant data

**Verify:**
- [ ] Parse JSON successfully
- [ ] No extra text outside JSON

#### G. Error Handling Flow

**Test:** Missing required arguments
```bash
easyskillz skill add
easyskillz skill remove
easyskillz tool register
```

**Expected:**
- ✅ Clear error message
- ✅ Shows usage
- ✅ Exit code 1

**Test:** Invalid flag values
```bash
easyskillz project sync --docs=invalid
easyskillz project sync --docs-strategy=invalid
easyskillz project sync --gitignore=invalid
```

**Expected:**
- ✅ Clear error message
- ✅ Shows valid options

**Test:** Missing flags in one-shot mode
```bash
easyskillz project sync --docs=yes
# Missing --docs-strategy
```

**Expected:**
- ✅ Error: "Missing required flags"
- ✅ Shows which flags are required

**Test:** Non-existent skill/tool
```bash
easyskillz skill remove nonexistent --confirm
easyskillz skill activate nonexistent
easyskillz tool unregister nonexistent --mode=full --confirm
```

**Expected:**
- ✅ Clear error: "not found"
- ✅ Exit code 1

#### H. AI Detection Flow

**Test:** Simulate AI agent (set environment variable)
```bash
# Windsurf detection
WINDSURF_CASCADE_TERMINAL=1 easyskillz skill remove test-skill
```

**Expected:**
- ✅ Shows AI warning
- ✅ Explains what to do
- ✅ Shows questions to ask user
- ✅ Shows flag explanations
- ✅ Shows recommended command
- ✅ Exit code 1 (blocked)

**Test:** AI with flags (should work)
```bash
WINDSURF_CASCADE_TERMINAL=1 easyskillz skill add ai-test-skill
WINDSURF_CASCADE_TERMINAL=1 easyskillz skill remove ai-test-skill --confirm
```

**Expected:**
- ✅ No AI warning (flags provided)
- ✅ Executes successfully

#### I. Help System Flow

**Test:** Top-level help
```bash
easyskillz
easyskillz --help
```

**Expected:**
- ✅ Shows domain-based structure
- ✅ Lists all domains
- ✅ Shows examples
- ✅ Shows supported tools

**Test:** Domain help (future enhancement)
```bash
easyskillz skill --help
easyskillz tool --help
easyskillz project --help
```

**Expected:**
- ✅ Shows domain-specific commands
- ✅ Shows flags for each command

### 5. Philosophy Compliance Checks

#### A. AI-First Design

- [ ] All interactive prompts have corresponding flags
- [ ] One-shot execution works for all commands
- [ ] AI detection prevents getting stuck in prompts
- [ ] AI warnings are helpful and specific
- [ ] Recommended commands are shown

#### B. Domain-Based Organization

- [ ] All commands follow `easyskillz <domain> <action>` pattern
- [ ] No flat commands (old structure)
- [ ] Consistent naming across domains

#### C. Destructive Operations

- [ ] `skill remove` requires `--confirm` for AI
- [ ] `tool unregister` requires `--mode` and `--confirm` for AI
- [ ] Safe operations (list, activate, deactivate) work without flags

#### D. Error Messages

- [ ] Clear and actionable
- [ ] Show correct usage
- [ ] Reference new command structure (not old)

#### E. Flag Consistency

- [ ] Boolean flags use `--flag=<value>` format
- [ ] Confirmation uses `--confirm` (no value)
- [ ] JSON output uses `--json`

### 6. Friction Points Check

Look for:
- [ ] Confusing error messages
- [ ] Unexpected prompts
- [ ] Inconsistent behavior
- [ ] Missing feedback
- [ ] Unclear next steps
- [ ] Broken examples in help text
- [ ] Old command references in output

### 7. Report Generation

Create a report file: `.qa-temp/qa-report.md`

```markdown
# QA Report - easyskillz v{version}

**Date:** {date}
**Tester:** AI Agent
**Environment:** {OS}, Node {version}

## Summary

- ✅ Passed: X tests
- ❌ Failed: Y tests
- ⚠️  Warnings: Z issues

## Test Results

### Project Sync Flow
- [✅/❌] One-shot execution
- [✅/❌] Interactive mode
- [✅/❌] Config creation
- [✅/❌] Docs centralization
- [✅/❌] Gitignore update

### Skill Management Flow
- [✅/❌] Add skill
- [✅/❌] List skills
- [✅/❌] Deactivate skill
- [✅/❌] Activate skill
- [✅/❌] Remove skill

### Tool Management Flow
- [✅/❌] List tools
- [✅/❌] Register tool
- [✅/❌] Unregister tool (revert)
- [✅/❌] Unregister tool (full)

### Docs Management Flow
- [✅/❌] List docs
- [✅/❌] Sync docs

### Error Handling
- [✅/❌] Missing arguments
- [✅/❌] Invalid flags
- [✅/❌] Non-existent resources

### AI Detection
- [✅/❌] Blocks interactive mode
- [✅/❌] Shows helpful warnings
- [✅/❌] Allows one-shot execution

## Bugs Found

1. **Bug Title**
   - **Severity:** Critical/High/Medium/Low
   - **Command:** `easyskillz ...`
   - **Expected:** ...
   - **Actual:** ...
   - **Steps to Reproduce:** ...

## Philosophy Violations

1. **Violation Title**
   - **Principle:** AI-First/Domain-Based/etc.
   - **Issue:** ...
   - **Recommendation:** ...

## Friction Points

1. **Friction Title**
   - **Where:** Command/Flow
   - **Issue:** ...
   - **Impact:** User confusion/Extra steps/etc.
   - **Suggestion:** ...

## Recommendations

- [ ] Fix critical bugs before release
- [ ] Update documentation for X
- [ ] Improve error message for Y
- [ ] Add missing flag for Z
```

### 8. Cleanup

```bash
# Uninstall the test package
npm uninstall -g easyskillz

# Return to project root
cd ../..

# Keep .qa-temp for review (it's gitignored)
```

## Success Criteria

✅ **All tests pass** - No critical bugs
✅ **Philosophy compliance** - All principles followed
✅ **No friction** - Smooth user experience
✅ **AI-first works** - One-shot execution for all flows
✅ **Error handling** - Clear, helpful messages
✅ **Documentation accurate** - Examples work as shown

## Notes

- The `.qa-temp/` directory is gitignored automatically
- Run this skill before every release
- Update this skill when adding new commands
- Test on multiple OS (Windows, macOS, Linux) if possible
- Test with different Node versions if possible

## Example Invocation

```bash
# From easyskillz project root
easyskillz skill add easyskillz-qa  # If not already added

# Then just ask the AI:
# "Run the easyskillz-qa skill and give me a full report"
```

The AI will execute all tests, catch bugs, identify philosophy violations, and report friction points.

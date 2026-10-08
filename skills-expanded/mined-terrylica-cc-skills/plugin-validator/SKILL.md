---
name: plugin-validator
description: Validate plugin structure and silent failures. TRIGGERS - plugin validation, check plugin, hook audit.
allowed-tools: Read, Bash, Glob, Grep, TodoWrite
---

# Plugin Validator

Comprehensive validation for Claude Code marketplace plugins.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## When to Use This Skill

Use this skill when:

- Validating plugin structure before release
- Auditing hooks for silent failures
- Checking plugin.json syntax and required fields
- Verifying skill file formatting and frontmatter

## Quick Start

```bash
# Validate a specific plugin
uv run plugins/plugin-dev/skills/plugin-validator/scripts/audit_silent_failures.py plugins/my-plugin/

# Validate with fix suggestions
uv run plugins/plugin-dev/skills/plugin-validator/scripts/audit_silent_failures.py plugins/my-plugin/ --fix
```

## Validation Phases

### Phase 1: Structure Validation

Check plugin directory structure:

```bash
/usr/bin/env bash << 'VALIDATE_EOF'
PLUGIN_PATH="${1:-.}"

# Check plugin.json exists
if [[ ! -f "$PLUGIN_PATH/plugin.json" ]]; then
    echo "ERROR: Missing plugin.json" >&2
    exit 1
fi

# Validate JSON syntax
if ! jq empty "$PLUGIN_PATH/plugin.json" 2>/dev/null; then
    echo "ERROR: Invalid JSON in plugin.json" >&2
    exit 1
fi

# Check required fields
REQUIRED_FIELDS=("name" "version" "description")
for field in "${REQUIRED_FIELDS[@]}"; do
    if ! jq -e ".$field" "$PLUGIN_PATH/plugin.json" >/dev/null 2>&1; then
        echo "ERROR: Missing required field: $field" >&2
        exit 1
    fi
done

echo "Structure validation passed"
VALIDATE_EOF
```

### Phase 2: Silent Failure Audit

**Critical Rule**: All hook entry points MUST emit to stderr on failure.

Run the audit script:

```bash
uv run plugins/plugin-dev/skills/plugin-validator/scripts/audit_silent_failures.py plugins/my-plugin/
```

#### What Gets Checked

| Check         | Target Files | Pattern                                |
| ------------- | ------------ | -------------------------------------- |
| Shellcheck    | `hooks/*.sh` | SC2155, SC2086, etc.                   |
| Silent bash   | `hooks/*.sh` | `mkdir\|cp\|mv\|rm\|jq` without `if !` |
| Silent Python | `hooks/*.py` | `except.*: pass` without stderr        |

#### Hook Entry Points vs Utility Scripts

| Location                 | Type        | Requirement          |
| ------------------------ | ----------- | -------------------- |
| `plugins/*/hooks/*.sh`   | Entry point | MUST emit to stderr  |
| `plugins/*/hooks/*.py`   | Entry point | MUST emit to stderr  |
| `plugins/*/scripts/*.sh` | Utility     | Fallback behavior OK |
| `plugins/*/scripts/*.py` | Utility     | Fallback behavior OK |

### Phase 3: Fix Patterns

#### Bash: Silent mkdir

```bash
# BAD - silent failure
mkdir -p "$DIR"

# GOOD - emits to stderr
if ! mkdir -p "$DIR" 2>&1; then
    echo "[plugin] Failed to create directory: $DIR" >&2
fi
```

#### Python: Silent except pass

```python
# BAD - silent failure
except (json.JSONDecodeError, OSError):
    pass

# GOOD - emits to stderr
except (json.JSONDecodeError, OSError) as e:
    print(f"[plugin] Warning: {e}", file=sys.stderr)
```

## Integration with /plugin-dev:create

This skill is invoked in Phase 3 of the plugin-add workflow:

```markdown
### 3.4 Plugin Validation

**MANDATORY**: Run plugin-validator before registration.

Task with subagent_type="plugin-dev:plugin-validator"
prompt: "Validate the plugin at plugins/$PLUGIN_NAME/"
```

## Exit Codes

| Code | Meaning                             |
| ---- | ----------------------------------- |
| 0    | All validations passed              |
| 1    | Violations found (see output)       |
| 2    | Error (invalid path, missing files) |

## References

- [Silent Failure Patterns](./references/silent-failure-patterns.md)


## Troubleshooting

| Issue                        | Cause                         | Solution                                            |
| ---------------------------- | ----------------------------- | --------------------------------------------------- |
| plugin.json not found        | Missing manifest file         | Create plugin.json with required fields             |
| Invalid JSON syntax          | Malformed plugin.json         | Run `jq empty plugin.json` to find syntax errors    |
| Missing required field       | Incomplete manifest           | Add name, version, description to plugin.json       |
| Shellcheck errors            | Bash script issues            | Run `shellcheck hooks/*.sh` to see details          |
| Silent failure in bash       | Missing error handling        | Add `if !` check around mkdir/cp/mv/rm commands     |
| Silent except:pass in Python | Missing stderr output         | Add `print(..., file=sys.stderr)` before pass       |
| Exit code 2                  | Invalid path or missing files | Verify plugin path exists and has correct structure |
| Violations after --fix       | Fix suggestions not applied   | Manually apply suggested fixes from output          |

## Post-Execution Reflection

After this skill completes, reflect before closing the task:

0. **Locate yourself.** — Find this SKILL.md's canonical path (Glob for this skill's name) before editing. All corrections target THIS file and its sibling references/ — never other documentation.
1. **What failed?** — Fix the instruction that caused it. If it could recur, add it as an anti-pattern.
2. **What worked better than expected?** — Promote it to recommended practice. Document why.
3. **What drifted?** — Any script, reference, or external dependency that no longer matches reality gets fixed now.
4. **Log it.** — Every change gets an evolution-log entry with trigger, fix, and evidence.

Do NOT defer. The next invocation inherits whatever you leave behind.

---
---

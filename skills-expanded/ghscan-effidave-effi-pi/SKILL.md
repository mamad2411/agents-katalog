---
name: creating-editing-skills
description: Create or edit Agent Skills. When a skill includes code examples or command invocations, verify they work by reading the relevant documentation and testing the examples. Use smoke testing to catch broken examples before publishing.
---

# Creating and Editing Skills

## Verify All Examples Work

When you create or edit a skill that includes command invocations, code snippets, API calls, file paths, or configuration examples, **you must verify that the examples actually work** before publishing.

This is called a **smoke test** — a quick check that verifies basic functionality works.

### The Workflow

1. **Identify all examples** in the skill (commands, code, paths, configs)
2. **For each example:**
   - Read the relevant documentation (`--help`, man pages, API docs)
   - Verify arguments, syntax, and options are correct
   - Run the example (or a dry-run version) to confirm it works
   - Fix any errors immediately
3. **Document any assumptions** (e.g., "requires Node.js 18+", "requires GitHub token")
4. **Test the skill yourself** by following its instructions as if you were the agent

### Examples

**Bash command:** Read `man find` to verify `-mtime +30` and `-delete` exist, then test with a dry-run: `find /var/log -name "*.log" -mtime +30` (without `-delete`).

**Python code:** Check the API docs to ensure `json.load()` takes a file object (not a filename), and verify syntax.

**CLI invocation:** Read `pi --help` to verify the flags exist. For example, `pi --session-name` and `--config-json` don't exist in the current pi CLI — use `pi --print --no-session "test"` instead.

**File path:** Verify the path exists and is readable: `ls ~/.pi/agent/config.json`.

### Common Mistakes

- ❌ Untested commands (no verification that the API or endpoint exists)
- ❌ Outdated flags or options (verified with an old version of the docs)
- ❌ Ambiguous file paths (`config.json` instead of `~/.pi/agent/config.json`)
- ❌ Missing prerequisites ("assumes Node.js 18+" should be documented)

### Tools for Smoke Testing

- `--help` and man pages: verify command flags
- API documentation: check function signatures
- `ls`, `cat`, `jq`, `shellcheck`: test file paths and syntax
- Dry-run modes: many tools have `--dry-run` or `--check` flags
- `--version`: confirm compatibility with docs

## Autonomy Level: Smoke Test Your Prescriptiveness

When deciding how prescriptive to make a skill, use the Minimal Harness Principles (MHP) autonomy scale: **thin** (minimal) → **encouraging** (guides and tools) → **controlling** (mandatory).

Smoke test different autonomy levels by:

1. **Draft the skill with maximum autonomy** (thin — just the goal and key information, minimal step-by-step)
2. **Spawn a test pi process** to see if an agent follows the skill appropriately:
   ```bash
   pi --print --no-session @/path/to/skill.md "Now follow this skill's instructions" 2>&1 | head -100
   ```
3. **Observe:** Does the agent follow the skill and achieve the goal?
   - **Yes** → That's the right autonomy level; keep it thin
   - **No** → Decrease autonomy (add encouraging language, examples, or mandatory steps per MHP section 5 & 6)
4. **Iterate** until the agent succeeds

This ensures the skill is no more prescriptive than necessary — respecting the model's capability while meeting your requirements.

See `~/.pi/minimal-harness-principles.md` for the full framework (especially sections 5-7 on decreasing autonomy and labelling).

## Skill Format

```markdown
---
name: your-skill-name
description: One sentence, action-oriented description.
---

# Skill Title

Overview.

## Setup

Prerequisites and installation steps.

## Instructions

Step-by-step guide for the agent.

## Examples

Example commands or code.

## Troubleshooting

Common issues and fixes.
```

## Pre-Publish Checklist

- [ ] All examples tested and verified to work (smoke tested)
- [ ] Autonomy level tested and verified with a spawned pi process
- [ ] File paths use `~` or absolute paths (not relative)
- [ ] Assumptions documented (e.g., "requires auth", "Unix only")
- [ ] Troubleshooting covers likely failure modes
- [ ] Skill can be followed step-by-step by an LLM
- [ ] No broken links or missing references
- [ ] Autonomy labelling used (FYI, Relevant info, Good practice, Rules) per MHP section 7

## References

- **Minimal Harness Principles:** `~/.pi/minimal-harness-principles.md` — framework for deciding how much guidance to include
- **Pi Skills documentation:** Pi documentation on the skills system
- **Agent Skills standard:** https://agentskills.io

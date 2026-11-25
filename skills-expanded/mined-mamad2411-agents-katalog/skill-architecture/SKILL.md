---
name: skill-architecture
description: Create new skills, modify existing skills, and understand skill architecture. Use when users want to create a skill from scratch, learn YAML.
---

# Skill Architecture

Comprehensive guide for creating effective Claude Code skills following Anthropic's official standards with emphasis on security and progressive disclosure architecture.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

> **Scope**: Claude Code Agent Skills (`~/.claude/skills/`), not Claude.ai API skills

## Self-Evolution Protocol

This skill — and every skill it creates — must actively evolve through use. This section is placed first because it governs all other sections.

**During execution**, watch for these signals: friction in instructions, missing edge cases, better patterns discovered, repeated manual steps, drift between documentation and reality.

**Before writing any change**, pass all three admission gates:

| Gate           | Question                                                           | Fail → |
| -------------- | ------------------------------------------------------------------ | ------ |
| **VALUE**      | Does this fix a real problem observed empirically, not speculated? | Skip   |
| **REDUNDANCY** | Is this already documented or obvious from the code?               | Skip   |
| **FRESHNESS**  | Will this still be true next month, or is it ephemeral?            | Skip   |

Most executions should produce **no evolution**. Convergence to stability is success, not stagnation.

**When all gates pass**: Pause current work → fix SKILL.md or references → log in evolution-log.md with trigger + evidence → resume. Do NOT defer — the next invocation inherits whatever you leave behind.

**What never passes the gate**: Major structural changes (discuss with user first), speculative improvements without empirical evidence, cosmetic preferences.

---

## When to Use This Skill

Use this skill when:

- Creating new Claude Code skills from scratch
- Learning skill YAML frontmatter and structure requirements
- Validating skill file format and portability
- Understanding progressive disclosure patterns for skills

---

## Task Templates

Select the appropriate template before starting skill work -- templates encode common workflows and prevent missing steps that cause silent failures.

See [Task Templates](./references/task-templates.md) for all templates (A-F) and the quality checklist.

| Template | Purpose                           |
| -------- | --------------------------------- |
| A        | Create New Skill                  |
| B        | Update Existing Skill             |
| C        | Add Resources to Skill            |
| D        | Convert to Self-Evolving Skill    |
| E        | Troubleshoot Skill Not Triggering |
| F        | Create Lifecycle Suite            |

---

## Post-Change Checklist (Self-Maintenance)

After modifying THIS skill (skill-architecture):

1. [ ] Templates and 6 Steps tutorial remain aligned
2. [ ] Skill Quality Checklist reflects current best practices
3. [ ] All referenced files in references/ exist
4. [ ] Append changes to [evolution-log.md](./references/evolution-log.md)
5. [ ] Update user's CLAUDE.md if triggers changed

---

---

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities with specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific domains -- transforming Claude from general-purpose to specialized agent with procedural knowledge no model fully possesses.

### What Skills Provide

1. **Specialized workflows** - Multi-step procedures for specific domains
2. **Tool integrations** - Instructions for working with specific file formats or APIs
3. **Domain expertise** - Company-specific knowledge, schemas, business logic
4. **Bundled resources** - Scripts, references, assets for complex/repetitive tasks

### Skill Discovery and Precedence

Skills are discovered from multiple locations. When names collide, higher-precedence wins:

1. **Enterprise** (managed settings) -- highest
2. **Personal** (`~/.claude/skills/`)
3. **Project** (`.claude/skills/` in repo)
4. **Plugin** (namespaced: `plugin:skill-name`)
5. **Nested** (monorepo `.claude/skills/` in subdirectories -- auto-discovered)
6. **`--add-dir`** (CLI flag, live change detection) -- lowest

**Management commands**:

- `claude plugin enable <name>` / `claude plugin disable <name>` -- toggle plugins
- `claude skill list` -- show all discovered skills with source location

**Monorepo support**: Claude Code automatically discovers `.claude/skills/` directories in nested project roots within a monorepo. No configuration needed.

---

## cc-skills Plugin Architecture

> This section applies specifically to the **cc-skills marketplace** plugin structure. Generic standalone skills are unaffected.

### Canonical Structure

```
plugins/<plugin>/
└── skills/
    └── <skill-name>/
        └── SKILL.md   <- single canonical file (context AND user-invocable)
```

`skills/<name>/SKILL.md` is the **single source of truth**. The separate `commands/` layer was eliminated -- it required maintaining two identical files per skill and caused `Skill()` invocations to return "Unknown skill". See [migration issue](https://github.com/terrylica/cc-skills/issues/26) for full context.

### How Skills Become Slash Commands

Two install paths, both supported:

| Path                    | Mechanism                                                                                                                             | Notes                                                                                                                                                                                          |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Automated (primary)** | `mise run release:full` -> `sync-commands-to-settings.sh` reads `skills/*/SKILL.md` -> writes `~/.claude/commands/<plugin>:<name>.md` | Fully automated post-release. Bypasses Anthropic cache bugs [#17361](https://github.com/anthropics/claude-code/issues/17361), [#14061](https://github.com/anthropics/claude-code/issues/14061) |
| **Official CLI**        | `claude plugin install itp@cc-skills` -> reads from `skills/` in plugin cache                                                         | Cache may not refresh on update -- use `claude plugin update` after new releases                                                                                                               |

### Hooks

`sync-hooks-to-settings.sh` reads `hooks/hooks.json` directly -> merges into `~/.claude/settings.json`. Bypasses path re-expansion bug [#18517](https://github.com/anthropics/claude-code/issues/18517).

### Creating a New Skill in cc-skills

Place the SKILL.md under `plugins/<plugin>/skills/<name>/SKILL.md`. No `commands/` copy needed. The validator (`bun scripts/validate-plugins.mjs`) checks frontmatter completeness.

---

## Skill Creation Process

See [Creation Tutorial](./references/creation-tutorial.md) for the detailed 6-step walkthrough, or [Creation Workflow](./references/creation-workflow.md) for the comprehensive guide with examples.

**Quick summary**: Gather requirements -> Plan resources -> Initialize -> Edit SKILL.md -> Validate -> Register and iterate.

---

## Testing and Iteration

Good skills emerge through testing and feedback, not from getting the first draft perfect. After writing or updating a skill, verify it works by running it against realistic prompts.

### Write Test Prompts

Come up with 2-3 realistic test prompts -- the kind of thing a real user would actually say. Not abstract requests, but concrete tasks with enough detail to exercise the skill. Share them with the user for confirmation before running.

### Run and Evaluate

For each test prompt, run the skill and examine the output:

- **Did the skill trigger?** If not, the description may need stronger trigger language.
- **Did it follow the workflow?** Check whether instructions were followed or ignored.
- **Was the output useful?** Compare against what you'd expect from a skilled human.

When subagents are available, run with-skill and without-skill versions in parallel to measure the skill's actual value-add. When not available, run test cases yourself as a sanity check.

### Iterate Based on Feedback

After evaluating results, improve the skill and retest. Keep iterating until the user is satisfied or feedback is consistently positive. Key principles for each iteration:

1. **Generalize from specific feedback.** Skills will be used across many different prompts. Avoid overfitting to test cases with fiddly, narrow fixes. If a pattern keeps failing, try a different approach or metaphor rather than adding more constraints.

2. **Keep the skill lean.** Every section must earn its tokens. Read the execution transcripts -- if the skill causes the model to waste time on unproductive steps, cut those instructions and see what happens.

3. **Explain the why, not just the what.** LLMs respond better to understanding _why_ a rule exists than to being commanded with rigid directives. Instead of "ALWAYS do X", explain: "Do X because skipping it causes Y, which leads to Z." This produces more robust behavior that generalizes to novel situations.

4. **Look for repeated work across test cases.** If every test run independently creates the same helper script or takes the same multi-step approach, bundle that script in `scripts/` so future invocations don't reinvent the wheel.

5. **Bundle common patterns as scripts.** When test runs reveal that the model writes similar boilerplate code every time, extract it into a bundled script. This saves tokens and improves reliability.

---

## Skill Writing Principles

These principles (aligned with Anthropic's official guidance) apply to all skill content:

- **Imperative form**: "Run the script", "Check the output" -- not passive or indirect phrasing.
- **Explain reasoning over rigid rules**: If you find yourself writing MUST/NEVER/ALWAYS in all caps, that's a signal to reframe. Explain the reasoning so the model internalizes the principle rather than treating it as an arbitrary constraint. The model is smart -- help it understand, don't just command it.
- **Pushy descriptions for triggering**: Claude tends to undertrigger skills. Descriptions should actively claim territory: "Use this skill whenever the user mentions X, Y, or Z, even if they don't explicitly ask for it." Include negative triggers too: "Do NOT use for A or B."
- **Natural language descriptions**: Write descriptions as sentences a human could read, not keyword lists. "Use this skill whenever..." is better than "TRIGGERS - keyword1, keyword2".
- **Keep execution out of descriptions**: Descriptions tell Claude _when_ to trigger. The skill body tells Claude _how_ to execute. Don't mix them.

See [Writing Guide](./references/writing-guide.md) for extended guidance with examples.

---

## Skill Anatomy

```
skill-name/
├── SKILL.md                      # Required: YAML frontmatter + instructions
├── scripts/                      # Optional: Executable code (Python/Bash)
├── references/                   # Optional: Documentation loaded as needed
│   └── evolution-log.md          # Required for self-evolving: Change history
└── assets/                       # Optional: Files used in output
```

### YAML Frontmatter (Required)

See [YAML Frontmatter Reference](./references/yaml-frontmatter.md) for the complete field reference, invocation control table, permission rules, description guidelines, and YAML pitfalls.

**Minimal example**:

```yaml
---
name: my-skill
description: Does X when user mentions Y. Use for Z workflows.
---
```

**Key rules**: `name` is lowercase-hyphen, `description` is single-line max 1024 chars with trigger keywords, no colons in description text.

### Progressive Disclosure (3 Levels)

Skills use progressive loading to manage context efficiently:

1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed by Claude (unlimited\*)

\*Scripts can execute without reading into context.

### Skill Description Budget

Skills are loaded into the context window based on description relevance. Large skills may be **excluded** if the budget is exceeded:

- **Budget**: ~2% of context window (16K character fallback)
- **Check**: Run `/context` to see which skills are loaded vs excluded
- **Override**: Set `SLASH_COMMAND_TOOL_CHAR_BUDGET` env var to increase budget
- **Mitigation**: Keep SKILL.md body lean, move detail to `references/`

---

## Bundled Resources

Skills can include `scripts/`, `references/`, and `assets/` directories. See [Progressive Disclosure](./references/progressive-disclosure.md) for detailed guidance on when to use each.

---

## CLI-Specific Features

CLI skills support `allowed-tools` for granting tool access without per-use approval. See [Security Practices](./references/security-practices.md) for details.

### String Substitutions

Skill bodies support these substitutions (resolved at load time):

| Variable               | Resolves To                                 | Example               |
| ---------------------- | ------------------------------------------- | --------------------- |
| `$ARGUMENTS`           | Full argument string from `/name arg1 arg2` | `Process: $ARGUMENTS` |
| `$ARGUMENTS[N]`        | Nth argument (0-indexed)                    | `File: $ARGUMENTS[0]` |
| `$N`                   | Shorthand for `$ARGUMENTS[N]`               | `$0` = first arg      |
| `${CLAUDE_SESSION_ID}` | Current session UUID                        | Log correlation       |

### Dynamic Context Injection

Use the pattern `!` + `` `command` `` (exclamation mark followed by a backtick-wrapped command) in skill body to inject command output at load time:

```
Current branch: <exclamation>`git branch --show-current`
Last commit: <exclamation>`git log -1 --oneline`
```

(Replace `<exclamation>` with `!` in actual usage.)

The command runs when the skill loads -- output replaces the pattern inline.

### Extended Thinking

Include the keyword `ultrathink` in a skill body to enable extended thinking mode for that skill's execution.

---

## Structural Patterns

See [Structural Patterns](./references/structural-patterns.md) for detailed guidance on:

1. **Workflow Pattern** - Sequential multi-step procedures
2. **Task Pattern** - Specific, bounded tasks
3. **Reference Pattern** - Knowledge repository
4. **Capabilities Pattern** - Tool integrations
5. **Suite Pattern** - Multi-skill lifecycle management (bootstrap, operate, diagnose, configure, upgrade, teardown)

---

## User Conventions Integration

This skill follows common user conventions:

- **Absolute paths**: Always use full paths (terminal Cmd+click compatible)
- **Unix-only**: macOS, Linux (no Windows support)
- **Python**: `uv run script.py` with PEP 723 inline dependencies
- **Planning**: OpenAPI 3.1.1 specs when appropriate

---

## Marketplace Scripts

See [Scripts Reference](./references/scripts-reference.md) for marketplace script usage.

---

## Reference Documentation

For detailed information, see:

- [Task Templates](./references/task-templates.md) - Templates A-F and quality checklist
- [Creation Tutorial](./references/creation-tutorial.md) - 6-step creation process walkthrough
- [YAML Frontmatter](./references/yaml-frontmatter.md) - Field reference, invocation control, description guidelines
- [Structural Patterns](./references/structural-patterns.md) - 5 skill architecture patterns (including Suite Pattern)
- [Workflow Patterns](./references/workflow-patterns.md) - Workflow skill implementation patterns
- [Progressive Disclosure](./references/progressive-disclosure.md) - Context management patterns
- [Creation Workflow](./references/creation-workflow.md) - Step-by-step process with examples
- [Scripts Reference](./references/scripts-reference.md) - Marketplace script usage
- [Security Practices](./references/security-practices.md) - Threats and defenses (CVE references)
- [Phased Execution](./references/phased-execution.md) - Preflight/Execute/Verify/Reflect/Rectify patterns and variants
- [Post-Execution Reflection](./references/post-execution-reflection.md) - Compulsory self-rectification pattern for stepwise skills
- [Theory: Self-Evolving Skills](./references/theory-self-evolution.md) - Research synthesis from Gemini DR #70 (6 threads)
- [Invocation Control](./references/invocation-control.md) - Skill invocation modes, permission rules, legacy commands migration
- [Interactive Patterns](./references/interactive-patterns.md) - AskUserQuestion integration patterns
- [Token Efficiency](./references/token-efficiency.md) - Context optimization
- [Advanced Topics](./references/advanced-topics.md) - CLI vs API, composition, bugs
- [Path Patterns](./references/path-patterns.md) - Safe/unsafe path references (known bugs documented)
- [Bash Compatibility](./references/bash-compatibility.md) - Shell portability patterns
- [Validation Reference](./references/validation-reference.md) - Quality checklist
- [Writing Guide](./references/writing-guide.md) - Tone, reasoning-based instructions, description optimization
- [Script Design](./references/script-design.md) - Designing scripts for agentic consumption
- [Troubleshooting](./references/troubleshooting.md) - Common issues and solutions
- [SYNC-TRACKING](./references/SYNC-TRACKING.md) - Marketplace version tracking
- [Evolution Log](./references/evolution-log.md) - This skill's change history

---

## Post-Execution Reflection (Compulsory)

This section is placed last so it is the final thing processed before the skill exits — maximizing recency effect.

Every skill **MUST** include a Post-Execution Reflection section — workflow skills, task skills, and capability skills alike. This is a structural requirement, not advisory. Without it, errors and drift repeat silently across sessions. Task-pattern skills are just as susceptible: scripts change interfaces, parameters get added, error messages drift from documentation.

### After this skill completes, reflect before closing

0. **Locate yourself.** — Find this SKILL.md's canonical path (Glob for this skill's name) before editing. All corrections target THIS file and its sibling references/ — never other documentation.
1. **What failed?** — Fix the instruction that caused it. If it could recur, add it as an anti-pattern.
2. **What worked better than expected?** — Promote it to recommended practice. Document why.
3. **What drifted?** — Any script, reference, or external dependency that no longer matches reality gets fixed now.
4. **Pass the admission gates.** — Apply the Self-Evolution Protocol (top of this file). VALUE + REDUNDANCY + FRESHNESS must all pass before writing any change.
5. **Log it.** — Every change gets an evolution-log entry with trigger, fix, and evidence.

Do NOT defer. The next invocation inherits whatever you leave behind.

### Template: Workflow / Stepwise Skills

For skills with multiple phases, evolution-log, and references/:

```markdown
## Post-Execution Reflection

After this skill completes, reflect before closing the task:

0. **Locate yourself.** — Find this SKILL.md's canonical path before editing.
1. **What failed?** — Fix the instruction that caused it.
2. **What worked better than expected?** — Promote to recommended practice.
3. **What drifted?** — Fix any script, reference, or dependency that no longer matches reality.
4. **Log it.** — Evolution-log entry with trigger, fix, and evidence.

Do NOT defer. The next invocation inherits whatever you leave behind.
```

### Template: Task-Pattern Skills

For single-action skills wrapping a CLI command or script:

```markdown
## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If the script's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.
```

See [Post-Execution Reflection Reference](./references/post-execution-reflection.md) for the full pattern, validation requirements, and examples.

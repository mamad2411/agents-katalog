---
name: build-vibe-skill
description: Create new skills for the vibe marketplace. Use this when the user wants to create a new skill that extends Claude Code's capabilities with specialized knowledge, workflows, or tool integrations.
user-invocable: true
model: opus
---

# Build Vibe Skill

This skill guides you through creating high-quality skills for the vibe marketplace using a validation-first approach: manually execute the workflow before codifying it.

## Core Principles

1. **Validate Before You Build**: Execute the workflow manually first to challenge assumptions
2. **Output Examples Drive Quality**: If a skill produces output, get examples of ideal output upfront
3. **Subagent Delegation**: Use specialized subagents for building and testing
4. **Test on Different Examples**: Verify the skill generalizes beyond the initial use case

## Phase 1: Requirements Gathering

### Step 1: Understand the Skill Purpose

Ask the user for:

1. **What problem does this skill solve?** - The specific task or workflow it automates
2. **When should it be triggered?** - Natural language prompts that should invoke this skill
3. **Is it user-invocable?** - Should users be able to call it with `/skill-name`?
4. **What model should run it?** - Which model? (opus for complex reasoning, sonnet for balanced, haiku for fast/simple)

### Step 2: Determine Output Requirements

Ask the user:

1. **Does this skill produce output?** (file, document, code, etc.)
2. **If yes, can you provide 1-2 examples of ideal output?**
   - Get concrete examples, not just descriptions
   - These examples become the validation target
3. **What format should the output be in?**

### Step 3: Identify Target Plugin

Determine which plugin this skill should live in:

| Plugin | Use For |
|--------|---------|
| `fe-databricks-tools` | Databricks operations, queries, deployments, apps |
| `fe-salesforce-tools` | Salesforce CRM operations, UCOs |
| `fe-google-tools` | Google Docs, Sheets, Slides, Calendar, Gmail |
| `fe-internal-tools` | Logfood, AWS auth, internal analytics |
| `fe-workflows` | Multi-step workflows, research tasks, complex processes |
| `fe-vibe-setup` | Vibe environment setup and configuration |
| `fe-jira-tools` | JIRA operations |
| `fe-file-expenses` | Expense reporting |

**If unsure:** Ask the user which plugin seems most appropriate.

## Phase 2: Manual Workflow Validation

**CRITICAL**: Before writing ANY skill code, manually execute the workflow to validate assumptions.

### Step 1: Document the Intended Workflow

Write out the step-by-step process the skill would follow:

```
Intended Workflow:
1. [Step 1 description]
2. [Step 2 description]
...
```

### Step 2: Execute the Workflow Manually

Actually perform each step yourself:

- Run the commands
- Make the API calls
- Create the outputs
- Note any failures, edge cases, or surprises

### Step 3: Validate Output (if applicable)

If the user provided example output:

1. Compare your manual output to the example
2. Identify gaps or differences
3. Iterate until your output matches the quality/format of the example

### Step 4: Document Learnings

Record what you discovered:

```
Workflow Validation Results:
- Steps that worked as expected: [list]
- Steps that required adjustment: [list with details]
- Edge cases discovered: [list]
- Prerequisites not initially identified: [list]
- Final working workflow: [revised steps]
```

**Only proceed to Phase 3 after the manual workflow succeeds.**

## Phase 3: Build the Skill (Subagent Delegation)

### Prepare the Skill Spec

Create a specification document for the builder subagent:

```yaml
Skill Specification:
  name: [skill-name]
  plugin: [target-plugin]
  user-invocable: [true/false]
  model: [opus/sonnet/haiku]

  description: |
    [Brief description for skill list - MUST include "when to use" info]

  workflow:
    [Validated workflow steps from Phase 2]

  success_criteria:
    - [Criterion 1]
    - [Criterion 2]
    - [Output matches provided examples (if applicable)]

  example_output: |
    [Paste user-provided example output here if applicable]

  resources_needed:
    - [Any helper scripts, schemas, or reference files]
```

### Delegate to Builder Subagent

Use the Task tool to spawn an Opus subagent for building:

```
Task tool with:
  subagent_type: "general-purpose"
  model: "opus"
  prompt: |
    Build a vibe skill according to this specification:

    [Paste skill spec]

    Create the following files:
    1. plugins/[plugin]/skills/[skill-name]/SKILL.md
    2. Any resource files in plugins/[plugin]/skills/[skill-name]/resources/

    The SKILL.md must have this frontmatter format:
    ---
    name: [skill-name]
    description: [description]
    user-invocable: [true/false]
    ---

    Follow the existing skill patterns in this project.
    Keep the skill under 500 lines - split into resource files if longer.

    Return the full content of all files created.
```

### Review Builder Output

Verify the subagent's output:

1. Check that frontmatter is correct
2. Verify workflow matches the validated workflow
3. Ensure success criteria are achievable
4. Confirm resource files are appropriate

**If issues:** Provide feedback and delegate again with corrections.

## Phase 4: Test the Skill

### Prepare Test Scenario

Identify a test case that's similar but different from the original:

- Uses the same skill logic
- Different inputs/parameters
- Tests generalization

### Delegate to Tester Subagent

Use the Task tool to spawn a testing subagent:

```
Task tool with:
  subagent_type: "general-purpose"
  model: "opus"
  prompt: |
    Test this newly created skill by invoking it with this scenario:

    [Test scenario description]

    The skill is located at: plugins/[plugin]/skills/[skill-name]/SKILL.md

    Execute the skill workflow and report:
    1. Did each step work as documented?
    2. Was the output correct/expected?
    3. Any errors or edge cases?
    4. Recommendations for improvement?

    Be thorough - this validates that the skill works in practice.
```

### Iterate if Needed

If testing reveals issues:

1. Document the problems
2. Delegate fixes back to the builder subagent
3. Re-test until the skill works correctly

## Phase 5: Finalize

### Add Permission

Add to `permissions.yaml`:

```yaml
allow:
  - "Skill(skill-name)"
```

### Add Eval

Add to `evals/test-cases/skill-routing.yaml`:

```yaml
- name: "skill-name-descriptive-test"
  prompt: "Natural language prompt that should trigger this skill"
  expected_skill: "plugin-name:skill-name"
  max_turns: 5
  model: sonnet
```

### Commit Changes

```bash
git add .
git commit -m "Add [skill-name] skill to [plugin-name]

[Brief description of what the skill does]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

## Claude Code Skill File Structure Reference

**Official docs:** https://code.claude.com/docs/en/skills

### Directory Layout

Each skill is a directory with `SKILL.md` as the entrypoint:

```
my-skill/
├── SKILL.md           # Main instructions (required)
├── template.md        # Template for Claude to fill in (optional)
├── examples/
│   └── sample.md      # Example output showing expected format (optional)
├── scripts/
│   └── helper.py      # Script Claude can execute (optional)
└── resources/
    └── schema.yaml    # Reference data, configs (optional)
```

Keep `SKILL.md` under 500 lines. Move detailed reference material to separate files and reference them from SKILL.md so Claude knows what they contain and when to load them.

### Where Skills Live

| Location   | Path                                              | Applies to                     |
|------------|---------------------------------------------------|--------------------------------|
| Enterprise | Managed settings                                  | All users in your organization |
| Personal   | `~/.claude/skills/<skill-name>/SKILL.md`          | All your projects              |
| Project    | `.claude/skills/<skill-name>/SKILL.md`            | This project only              |
| Plugin     | `<plugin>/skills/<skill-name>/SKILL.md`           | Where plugin is enabled        |

**For vibe marketplace skills**, always use the **Plugin** location: `plugins/<plugin-name>/skills/<skill-name>/SKILL.md`

### YAML Frontmatter Reference

All fields are optional. Only `description` is recommended.

```yaml
---
name: my-skill                     # Display name (kebab-case, max 64 chars). Defaults to directory name.
description: What this does        # RECOMMENDED. What the skill does and when to use it. Claude uses this to decide when to load it.
argument-hint: "[issue-number]"    # Hint shown during autocomplete for expected arguments
disable-model-invocation: false    # true = only user can invoke via /name (Claude cannot auto-load it)
user-invocable: true               # false = hidden from / menu (only Claude can invoke it)
allowed-tools: Read, Grep, Bash    # Tools Claude can use without asking permission when skill is active
model: opus                        # Model to use when this skill is active (opus/sonnet/haiku)
context: fork                      # Set to "fork" to run in a forked subagent context
agent: Explore                     # Which subagent type to use when context: fork (Explore, Plan, general-purpose, or custom)
hooks: ...                         # Hooks scoped to this skill's lifecycle
---
```

### Invocation Control

| Frontmatter                      | User can invoke | Claude can invoke | When loaded into context                                     |
|----------------------------------|-----------------|-------------------|--------------------------------------------------------------|
| (default)                        | Yes             | Yes               | Description always in context, full skill loads when invoked |
| `disable-model-invocation: true` | Yes             | No                | Description not in context, full skill loads when you invoke |
| `user-invocable: false`          | No              | Yes               | Description always in context, full skill loads when invoked |

### String Substitutions

Use these variables in skill content for dynamic values:

| Variable               | Description                                              |
|------------------------|----------------------------------------------------------|
| `$ARGUMENTS`           | All arguments passed when invoking the skill             |
| `$ARGUMENTS[N]`        | Access a specific argument by 0-based index              |
| `$N`                   | Shorthand for `$ARGUMENTS[N]` (e.g. `$0`, `$1`)         |
| `${CLAUDE_SESSION_ID}` | The current session ID                                   |

### Dynamic Context Injection

The `` !`command` `` syntax runs shell commands before skill content is sent to Claude:

```yaml
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
---

## Pull request context
- PR diff: !`gh pr diff`
- Changed files: !`gh pr diff --name-only`

Summarize this pull request...
```

### Subagent Execution

Add `context: fork` to run a skill in an isolated subagent. The skill content becomes the prompt that drives the subagent (it won't have access to conversation history). Use `agent` to specify the agent type.

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:
1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

## Checklist

- [ ] Requirements gathered (purpose, triggers, output examples)
- [ ] Target plugin identified
- [ ] Workflow documented
- [ ] **Workflow manually validated**
- [ ] Output matches provided examples (if applicable)
- [ ] Skill spec created
- [ ] Builder subagent created skill files
- [ ] Skill reviewed and approved
- [ ] Tester subagent verified skill works
- [ ] Permission added to permissions.yaml
- [ ] Eval added to skill-routing.yaml
- [ ] Changes committed

## Common Mistakes

### Skipping Manual Validation

- **Problem:** Skill contains untested assumptions that fail in practice
- **Fix:** Always execute the workflow manually before writing the skill

### Vague Output Requirements

- **Problem:** No way to validate if skill produces correct output
- **Fix:** Get concrete examples upfront; compare against them

### Overly Long SKILL.md

- **Problem:** Token cost, hard to maintain
- **Fix:** Keep under 500 lines; use resource files for schemas, examples, helpers

### Missing "When to Use" in Description

- **Problem:** Skill doesn't trigger for relevant prompts
- **Fix:** Description MUST specify when the skill should be invoked

---
name: cmd-playbook
description: Command — Record a workflow and auto-generate a reusable command from it (writes to the user's project-local commands, not the plugin)
---

Watch a manual workflow, then auto-generate a reusable command from it. You describe the steps, this command turns them into a repeatable, documented procedure.

The generated command lands in `.claude/commands/[name].md` (the user's per-project commands directory — these are PROJECT-LOCAL commands, separate from the devkit plugin's commands). Invoke them as `/[name]` (no `devkit:` prefix needed; bare-name resolution works because they live in your project's local commands, not in a plugin namespace).

## Steps

### Step 1: Name the playbook

Get the playbook name from the argument. If not provided, ask what this workflow does in one sentence and derive a kebab-case name.

### Step 2: Capture the workflow

Ask the user to describe their workflow step by step. For each step, capture:

- **What:** The action taken
- **Where:** What file, tool, or system is involved
- **Why:** The purpose of this step
- **Inputs:** What information is needed
- **Output:** What this step produces

Guide them through it: "What do you do first?" → "Then what?" → "What happens next?"

Continue until they say they're done.

### Step 3: Identify patterns

Analyse the captured workflow:

- **Which steps can be parallelised?** (independent reads, searches)
- **Which steps need user input?** (decisions, approvals)
- **Which steps are conditional?** (only if X, then Y)
- **What tools does each step need?** (Read, Write, Agent, Bash, WebSearch, etc.)
- **Are there any existing skills that match steps?** Check the plugin's skills at `~/.claude/plugins/devkit/skills/` (installed location) — NOT `.claude/skills/`, which is empty/project-local.

### Step 4: Determine the argument

What variable input does this workflow need each time it runs?

- A project name? A file path? A topic? A client name?
- Define the argument-hint that makes sense.

### Step 5: Propose the tool-grant list (REQUIRED HUMAN GATE)

**Before writing the command file**, present the proposed `allowed-tools` list to the user explicitly:

```
Proposed allowed-tools for this playbook: [Read, Write, Bash(git:*)]

The /playbook command itself runs with [Read, Write, Edit, Glob, Bash(date:*)],
but the command you're about to create can be granted any tools. Confirm the
list is minimum-necessary:

- Read: needed for [reason]
- Write: needed for [reason]
- Bash(git:*): needed for [reason]

Type the literal word "approved" to proceed, or list adjustments to make.
```

**Strict-approval rule**: only the literal word `approved` (case-insensitive, possibly with surrounding whitespace) counts as approval. Any other response — "looks fine", "yes", "go ahead", "ship it", silence — is treated as a request for adjustments, NOT as approval. Re-prompt with: "Please type the literal word 'approved' to confirm, or list the changes you want made to the tool list."

If the proposed list includes unscoped `Bash`, `WebFetch`, or any write tool (`Write`, `Edit`), explicitly call out the broader surface area and ask the user to confirm or narrow. Default to the most restrictive grant that still accomplishes the workflow.

### Step 6: Generate the command

Only after the user approves the tool grant in Step 5, write the command file to `.claude/commands/[playbook-name].md`:

```markdown
---
name: [playbook-name]
description: [one-line description derived from the workflow]
argument-hint: "[identified argument]"
allowed-tools:
  - [user-approved tools only]
---

[Brief explanation of what this command does]

## Steps

### Step 1: [First action]

[Instructions derived from the captured workflow]

### Step 2: [Second action]

[Instructions]

[Continue for each step, with parallel steps marked]

### Step [N]: Output

[What the final output looks like]
```

### Step 7: Verify and refine

Show the generated command to the user:

- "Here's the command I generated. Does this capture your workflow correctly?"
- Make any adjustments they request.
- Save the final version.

### Step 8: Register the command

If a `command-index.md` exists in the project, add the new command to it.

Output: "Your playbook is saved as `/[name]` (project-local, no `devkit:` prefix needed). Run it any time to repeat this workflow."

## Arguments

`[name for the playbook]`

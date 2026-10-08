---
name: yato-new-project
description: Start a new project from scratch using Yato (Yet Another Tmux Orchestrator). Creates a new tmux session with a Project Manager agent. Use when user wants to begin a new codebase or project.
allowed-tools: Bash,Read,AskUserQuestion
user-invocable: true
disable-model-invocation: false
argument-hint: "[project-name] [what to build]"
---

# Yato New Project

<context>
This skill creates a NEW project from scratch. It will:
1. Parse or ask for the project name
2. Create a project folder in ~/dev/
3. Deploy a PM to coordinate the work (PM handles asking what to build)
</context>

<instructions>
## Step 0: Check if User is in Tmux

```bash
bash ${CLAUDE_PLUGIN_ROOT}/bin/check-tmux.sh
```

## Step 1: Parse Arguments

Arguments format: `[project-name] [what to build]`

Examples:
- `/yato-new-project tictactoe a simple tic-tac-toe game` → name=tictactoe, request="a simple tic-tac-toe game"
- `/yato-new-project a recipe app` → name derived from request, request="a recipe app"
- `/yato-new-project` → ask user for project name only

**If first word looks like a project name (single word, kebab-case)**: Use it as PROJECT_NAME, rest is request.
**Otherwise**: Derive PROJECT_NAME from request (first 2-3 words, kebab-case).
**If no arguments**: Ask only "What should the project be called?" - NO preamble, NO explanation, just the question. Do NOT ask what to build — the PM will handle that.

## Step 2: Create Project Directory

```bash
PROJECT_NAME="[derived-name]"  # kebab-case, e.g., "tic-tac-toe"
PROJECT_PATH="$HOME/dev/$PROJECT_NAME"
mkdir -p "$PROJECT_PATH"
PROJECT_SLUG=$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | tr '._ ' '-')
```

## Step 3: Create Workflow Folder

```bash
if [[ -n "$REQUEST" ]]; then
    TITLE=$(echo "$REQUEST" | cut -d' ' -f1-4)
else
    TITLE="new-project"
fi

WORKFLOW_NAME=$(${CLAUDE_PLUGIN_ROOT}/bin/init-workflow.sh "$PROJECT_PATH" "$TITLE" 2>/dev/null | grep "^Workflow:" | awk '{print $2}')

if [[ -z "$WORKFLOW_NAME" ]]; then
    WORKFLOW_NAME=$(ls -td "$PROJECT_PATH/.workflow"/[0-9][0-9][0-9]-*/ 2>/dev/null | head -1 | xargs basename)
fi
```

## Step 4: Save Request to status.yml (if provided)

```bash
if [[ -n "$REQUEST" ]]; then
    uv run --directory ${CLAUDE_PLUGIN_ROOT} python -c "
content = '''$REQUEST'''
indented = '\n'.join('  ' + line if line else '' for line in content.split('\n'))
with open('$PROJECT_PATH/.workflow/$WORKFLOW_NAME/status.yml', 'r') as f:
    yml = f.read()
yml = yml.replace('initial_request: \"\"', 'initial_request: |\n' + indented)
with open('$PROJECT_PATH/.workflow/$WORKFLOW_NAME/status.yml', 'w') as f:
    f.write(yml)
"
fi
```

## Step 5: Deploy PM

```bash
SESSION_NAME="${PROJECT_SLUG}_${WORKFLOW_NAME}"
uv run --directory ${CLAUDE_PLUGIN_ROOT} python ${CLAUDE_PLUGIN_ROOT}/lib/orchestrator.py deploy-pm "$SESSION_NAME" -p "$PROJECT_PATH" -w "$WORKFLOW_NAME"
```

## Step 6: Connect or Give Attach Command

**If IN_TMUX**:
```bash
CLIENT_TTY=$(tmux display-message -p '#{client_tty}' 2>/dev/null)
if [[ -n "$CLIENT_TTY" ]]; then
    tmux switch-client -c "$CLIENT_TTY" -t "$SESSION_NAME"
fi
```

**If NOT_IN_TMUX**:
```bash
echo "tmux attach -t $SESSION_NAME" | pbcopy
```

**If request was provided**, output:
```
Project created at: ~/dev/[PROJECT_NAME]

Session ready!

Paste and press Enter to connect: (already copied to clipboard)
tmux attach -t [SESSION_NAME]

The PM has your request and will continue from there.
```

**If no request**, output:
```
Project created at: ~/dev/[PROJECT_NAME]

Session ready!

Paste and press Enter to connect: (already copied to clipboard)
tmux attach -t [SESSION_NAME]

The PM will ask you what you want to build.
```
</instructions>

<examples>
<example>
<scenario>User runs /yato-new-project tictactoe a tic-tac-toe game</scenario>
<action>
1. PROJECT_NAME = "tictactoe"
2. REQUEST = "a tic-tac-toe game"
3. Create ~/dev/tictactoe/
4. Create workflow, save request
5. Deploy PM and connect
</action>
</example>

<example>
<scenario>User runs /yato-new-project a recipe sharing app</scenario>
<action>
1. No explicit name, derive from request
2. PROJECT_NAME = "recipe-sharing-app"
3. REQUEST = "a recipe sharing app"
4. Create ~/dev/recipe-sharing-app/
5. Create workflow, save request
6. Deploy PM and connect
</action>
</example>

<example>
<scenario>User runs /yato-new-project (no args)</scenario>
<action>
1. Ask: "What should the project be called?"
2. User: "todo-list-app"
3. PROJECT_NAME = "todo-list-app"
4. REQUEST is empty - do NOT save to status.yml
5. Create ~/dev/todo-list-app/
6. Create workflow, deploy PM
7. PM asks what to build
</action>
</example>
</examples>

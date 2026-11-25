---
name: init
description: Initialize a Pi workspace with extension scaffolding, prompt templates, and an AGENTS.md optimized for Pi's context parser. Use when setting up a new repository or onboarding an existing project to Pi.
---
# Workspace Initialization

Set up the repository for native Pi Agent capabilities. This skill scaffolds the necessary files, directories, and documentation to ensure future Pi sessions have full context and custom behaviors.

## Step 1: Scaffold `.pi/` directory

Create the `.pi/` configuration directory at the repository root if it does not exist.

### `.pi/skills/`
Create a `.pi/skills/` directory for project-specific custom skills. Add a `README.md` inside:
\`\`\`markdown
# Custom Pi Skills
Place custom skill atoms here as \`SKILL.md\` files (or subdirectories).
They will be automatically loaded into your Pi sessions when working in this workspace.
\`\`\`

### `.pi/prompts/`
Create a `.pi/prompts/` directory for system prompt overrides. Add a `README.md` inside:
\`\`\`markdown
# Pi Prompt Templates
Place `.md` files here to define custom prompt templates that can be referenced via the \`/prompt\` command or injected as system instructions.
\`\`\`

## Step 2: Generate AGENTS.md

Pi's context parser explicitly looks for `AGENTS.md`. If it does not exist, analyze the codebase and create it.

The file must be highly structured and dense. **Do not include generic fluff.**

### Sections to include:

1. **Build & Run Matrix**: Exact commands to install dependencies, run the dev server, lint, and run tests.
2. **Architecture Map**: High-level map of the codebase (e.g., "Frontend is in `src/web`, backend API is in `src/api`").
3. **Pi Extension API Guidelines**: If this is a Pi Extension project, document the schema and routing rules required.
4. **Tool Constraints**: Any project-specific rules (e.g., "Do not use \`rm -rf\` on the \`artifacts/\` directory", "Always run \`npm run validate\` before committing").

## Step 3: Verify the Environment

Verify that the project has the basic requirements for a Pi environment:
- Is git initialized? (If not, run \`git init\`)
- Is there a `.gitignore`? (If not, create a basic one including \`node_modules\`, \`.env\`, and temporary artifact directories).

## Step 4: Chain to Documentation (Optional)

If the user requested a full onboarding setup, recommend they trigger the \`wiki\` skill next to generate a deep-dive architecture wiki for the newly initialized workspace.

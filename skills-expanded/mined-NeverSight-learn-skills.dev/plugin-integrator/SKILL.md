---
name: plugin-integrator
description: Integrate skills as plugins into the Claude Code plugin marketplace. Use this skill whenever the user wants to "add a skill to the marketplace", "create a plugin from a skill", "package a skill as a plugin", "register a plugin", "integrate a skill", "convert a skill to a plugin", "scaffold a plugin", or mentions adding something to the plugins directory. Also activate when the user has a SKILL.md they want to publish, wants to update marketplace.json, or is working on plugin structure in this repository.
---

# Plugin Integrator

Package standalone skills into properly structured Claude Code plugins and register them in the marketplace.

## When to use this skill

Use this when you need to:
- Convert a standalone skill (a SKILL.md with optional supporting files) into a marketplace plugin
- Scaffold a new empty plugin directory with the correct structure
- Register an existing plugin in marketplace.json and the root README.md
- Validate that a plugin follows marketplace conventions

## The plugin structure

Every plugin in this marketplace follows a consistent directory layout:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Local plugin metadata
├── README.md                # Plugin documentation
├── skills/
│   └── <skill-name>/        # Named subdirectory for the skill
│       ├── SKILL.md          # The skill definition (required)
│       ├── references/       # Detailed reference docs (optional)
│       ├── examples/         # Working code examples (optional)
│       ├── templates/        # Scaffolding templates (optional)
│       ├── scripts/          # Executable scripts (optional)
│       ├── agents/           # Subagent definitions (optional)
│       └── assets/           # Static files used in output (optional)
└── commands/                # Slash command definitions (optional)
    └── command-name.md
```

The skill lives in a named subdirectory under `skills/` (e.g., `skills/drawio-creation/SKILL.md`, `skills/plugin-integrator/SKILL.md`). The subdirectory name should be kebab-case and describe what the skill does.

## Step-by-step integration process

### Step 1: Identify the source material

Determine what the user is starting from:
- **A standalone SKILL.md** (with or without supporting files like references/, scripts/, etc.)
- **An existing directory** with skill-like content that needs restructuring
- **A concept** that needs both a skill and a plugin scaffold

Read the source material thoroughly. Understand what the skill does, what supporting files it needs, and what its trigger conditions are.

### Step 2: Create the plugin directory

Create `plugins/<plugin-name>/` following the structure above. The plugin name should be kebab-case and match the skill's purpose.

1. Create the directory structure:
   ```
   plugins/<plugin-name>/
   ├── .claude-plugin/
   ├── skills/
   │   └── <skill-name>/
   └── (commands/ if the skill benefits from a slash command)
   ```

2. Copy or move the SKILL.md and all supporting files into `skills/<skill-name>/`. The skill name should be kebab-case and describe what the skill does (e.g., `drawio-creation`, `jarchi-scripting`, `plugin-integrator`). Preserve the internal directory structure (references/, examples/, scripts/, etc.).

3. If the skill has a LICENSE file, keep it alongside the SKILL.md in the skill subdirectory.

### Step 3: Create plugin.json

Write `.claude-plugin/plugin.json` with this exact structure:

```json
{
  "name": "<plugin-name>",
  "version": "1.0.0",
  "description": "<one-line description matching what goes in marketplace.json>",
  "author": {
    "name": "Thomas Klok Rohde"
  },
  "keywords": ["keyword1", "keyword2", "keyword3"]
}
```

Use 3-8 relevant keywords. The description should be concise but descriptive — it's the same text that appears in marketplace.json.

### Step 4: Write the README.md

The README follows a standard template. Read `references/readme-template.md` for the full template. Key sections:

1. **Title**: `# <Plugin Name> Plugin for Claude Code`
2. **Description**: One sentence summarizing the plugin
3. **Features**: 3-5 bullet points with bold labels
4. **Installation**: Standard code block with `claude --plugin-dir` and `.claude-plugin/` copy instructions
5. **Usage**: Include "Automatic Skill Activation" subsection listing trigger phrases, and optionally "Command Usage" if a slash command exists
6. **Example Requests**: 3-5 realistic prompts
7. **Components**: List skills, commands, and references
8. **License**: Brief license note

### Step 5: Register in marketplace.json

Add an entry to `.claude-plugin/marketplace.json` in the `plugins` array:

```json
{
  "name": "<plugin-name>",
  "source": "./plugins/<plugin-name>",
  "description": "<same description as plugin.json>",
  "version": "1.0.0",
  "author": {
    "name": "Thomas Klok Rohde",
    "email": "thomas@rohde.name"
  },
  "repository": "https://github.com/ThomasRohde/marketplace",
  "keywords": ["keyword1", "keyword2"],
  "category": "productivity"
}
```

### Step 6: Update the root README.md

Add the plugin to the "Available Plugins" section in alphabetical order among the existing entries:

```markdown
### <plugin-name>

<One-line description.>

**Install:**
```shell
/plugin install <plugin-name>@thomas-rohde-plugins
```

**Keywords:** keyword1, keyword2, keyword3
```

Also add the plugin to the "Marketplace Structure" ASCII tree diagram.

### Step 7: Validate

After integration, verify:
- [ ] `plugins/<plugin-name>/skills/<skill-name>/SKILL.md` exists with valid YAML frontmatter (name + description)
- [ ] `plugins/<plugin-name>/.claude-plugin/plugin.json` exists and is valid JSON
- [ ] `plugins/<plugin-name>/README.md` exists with all required sections
- [ ] `.claude-plugin/marketplace.json` has the new entry and is valid JSON
- [ ] Root `README.md` includes the plugin in "Available Plugins" and the directory tree
- [ ] All supporting files (references, examples, scripts) are inside `skills/<skill-name>/`
- [ ] No broken internal paths in the SKILL.md (e.g., references to `references/` still resolve)

## Optional: Create a slash command

If the skill benefits from a quick-trigger command, create `commands/<command-name>.md`:

```yaml
---
description: "Short description of what the command does"
argument-hint: <what to pass as argument>
allowed-tools: Read, Write, Glob, Grep, Edit, Bash
---
```

The command body should briefly describe the task, reference the skill for domain knowledge, and specify output requirements. See existing commands in other plugins for examples.

## Reference files

- `references/readme-template.md` — Full README.md template with all sections and formatting
- `references/marketplace-schema.md` — JSON schemas for marketplace.json and plugin.json

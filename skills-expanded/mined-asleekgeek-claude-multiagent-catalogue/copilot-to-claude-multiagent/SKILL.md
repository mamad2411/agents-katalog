---
name: copilot-to-claude-multiagent
description: >
  Convert any GitHub Copilot marketplace artefact (standalone agent, instruction
  fragment, plugin bundle, skill, hook, agentic workflow, cookbook recipe) into
  its Claude Code-native equivalent. Use this skill whenever the user wants to
  port, convert, adapt, or import an artefact from awesome-copilot or any
  Copilot-format plugin repo into Claude Code. Triggers on: "convert Copilot
  plugin", "port this agent to Claude Code", "import from awesome-copilot",
  "port the instructions", "convert this hook", "add this team to Claude Code",
  or when browsing the awesome-copilot marketplace and selecting an artefact to
  use. Also triggers for batch catalogue builds. Handles local repo sources and
  external GitHub repos. Produces ready-to-install agent .md files, adapted
  SKILL.md files, instruction files, hook bundles with claude-settings.json
  fragments, workflow prompts with GH Action templates, cookbook recipes, a
  per-plugin README with installation steps, and a running CATALOGUE.md entry.
compatibility: Claude Code (bash, filesystem); optional web_fetch for external GitHub repos
---

# Copilot → Claude Code Marketplace Converter

Converts any artefact from a GitHub Copilot marketplace (`awesome-copilot` or a similarly-shaped repo) into its Claude Code-native equivalent. Primary use cases:

- **Standalone agents** — one-shot conversions of `agents/*.agent.md` files.
- **Instructions** — coding-standard fragments with `applyTo:` globs.
- **Plugins** — bundles that mix agents, skills, and instructions around a topic; the marquee case is multi-agent orchestration rigs but most plugins are domain bundles (`csharp-dotnet-development`, `azure-cloud-development`, etc.).
- **Skills** — `SKILL.md` folders; usually structurally compatible already.
- **Hooks** — lifecycle automations with `hooks.json`.
- **Workflows** — markdown-driven agentic GitHub Actions.
- **Cookbook recipes** — SDK how-tos; rewritten for the Anthropic SDK or skipped.

## Assumed Local Context

```
/path/to/awesome-copilot/                ← upstream marketplace
  .github/plugin/marketplace.json
  agents/<name>.agent.md              ← standalone agents (Phase B)
  instructions/<name>.instructions.md ← coding standards (Phase D)
  plugins/<name>/                     ← topic bundles (Phase C)
    .github/plugin/plugin.json        ← plugin manifest
    agents/*.md
    skills/*/SKILL.md
    README.md
  skills/<name>/SKILL.md              ← standalone skill pool
  hooks/<bundle>/                     ← hook bundles (Phase E)
    hooks.json
    <scripts>
  workflows/<name>.md                 ← agentic GH Actions (Phase E)
  cookbook/<recipe>/                  ← SDK recipes (Phase E)
```

Output lands at this repo's matching top-level directory:

```
/path/to/claude-multiagent-catalogue/
  agents/<name>.md
  instructions/<name>.md
  plugins/<plugin-name>/{agents,skills,instructions,plugin.json,README.md}
  skills/<name>/SKILL.md
  hooks/<bundle-name>/{<scripts>,claude-settings.json,README.md}
  workflows/<name>.{md,github-action.yml}
  cookbook/<recipe-name>/
```

Running catalogue: `CATALOGUE.md` at this repo's root.

---

## Phase 0 — Identify the artefact type

The first decision is what kind of artefact you are converting. Branch on the upstream path:

| Upstream path | Artefact type | Go to |
|---|---|---|
| `agents/<name>.agent.md` | Standalone agent | Phase 2a + 2-standalone |
| `instructions/<name>.instructions.md` | Instruction fragment | Phase 2-instructions |
| `plugins/<name>/` (with `agents/` and/or `skills/`) | Plugin bundle | Phases 1–4 (full procedure) |
| `skills/<name>/SKILL.md` | Standalone skill | Phase 2b |
| `hooks/<bundle>/` | Hook bundle | Phase 2-hooks |
| `workflows/<name>.md` | Agentic workflow | Phase 2-workflows |
| `cookbook/<recipe>/` | Cookbook recipe | Phase 2-cookbook |

Read **all source files** fully before converting. Never convert blind.

The remaining phases describe the plugin-bundle pipeline (which is the most involved). The other artefact types short-circuit through fewer phases — see the per-type sections.

---

## Phase 1 — Discover and Classify (plugin bundles only)

```bash
PLUGIN=$1   # plugin name, e.g. rug-agentic-workflow
ROOT=/path/to/awesome-copilot/plugins/$PLUGIN

# Read manifest
cat $ROOT/.github/plugin/plugin.json

# Map directory contents
ls $ROOT/agents/        2>/dev/null && echo "→ has agents"
ls $ROOT/skills/        2>/dev/null && echo "→ has skills"
ls $ROOT/instructions/  2>/dev/null && echo "→ has instructions"
cat $ROOT/README.md     2>/dev/null | head -60
```

**Classify into one of five archetypes:**

| Archetype | Indicators | Conversion path |
|---|---|---|
| **Agents-only** | `agents/*.md`, no others | Full agent conversion |
| **Skills-only** | `skills/*/SKILL.md`, no others | Light skill adaptation |
| **Instructions-only** | `instructions/*.md`, no others | Light instructions adaptation |
| **Hybrid** | Two or more of the above | Apply each in turn |
| **External repo** | `plugin.json` has `source.source === "github"` and no local content | web_fetch from GitHub or APM note |

---

## Phase 2 — Convert

> **Before writing any output**, read all three reference files:
> - `references/tool-mapping.md`
> - `references/model-mapping.md`
> - `references/conversion-patterns.md`

### 2a. Agent File Conversion (plugin-embedded)

**Input (Copilot frontmatter):**
```yaml
---
name: 'AGENT-NAME'
description: 'When to use this agent...'
tools: ['vscode', 'execute', 'read', 'agent', 'edit', 'search', 'web', 'todo']
model: GPT-5
agents: ['SWE', 'QA']
---
```

**Output (Claude Code frontmatter):**
```yaml
---
name: agent-name
description: >
  When to use this agent... (keep intent verbatim; replace "GitHub Copilot"
  with "Claude Code"; remove tool-list language)
model: claude-opus-4-6   # see references/model-mapping.md
---
```

**Frontmatter rules (strict):**
- `name` → lowercase, hyphenated, no quotes
- `description` → preserve original intent; strip Copilot-specific phrasing
- `tools` → **DROP** — Claude Code agents have full tool access by default
- `model` → **MAP** using `references/model-mapping.md`; default to `claude-sonnet-4-6`
- `agents` → **DROP** — cross-agent references move into body text

**Body adaptation — key rules:**
1. `#tool:runSubagent` → `Task` tool pattern (see `references/conversion-patterns.md §1`)
2. `#context7` → Context7 MCP note (see `§2`)
3. `vscode` / VS Code UI patterns → bash equivalents or "user action required" note (see `§3`)
4. `manage_todo_list` → Claude Code `TodoManager` tool (see `§5`)
5. Cross-agent references (`@SWE`, `@QA`, etc.) → sub-agent names with `Task` call example
6. GitHub Issue/PR workflows → `gh` CLI commands (see `§4`)
7. Preserve all role constraints, workflows, and communication style verbatim — this is the IP
8. Add `## Claude Code Notes` section at the end listing every adaptation decision made

### 2-standalone. Standalone agent conversion (`awesome-copilot/agents/*.agent.md`)

Same frontmatter rules as 2a, with two extra steps for filename and attribution:

1. **Rename** `CSharpExpert.agent.md` → `csharp-expert.md`. Drop the `.agent` suffix; lowercase; hyphenate camelCase words.
2. **Prepend attribution** as the first line of the body:
   ```markdown
   > Ported from awesome-copilot/agents/<original-filename>
   ```
3. **Strip** any `# version:` comment in frontmatter — not a Claude convention.
4. **Skip** the `## Claude Code Notes` section unless an actual body adaptation was made. Most standalone agents have clean prose that needs no adaptation beyond frontmatter + filename.
5. **Output** to `agents/<name>.md` at this repo's root (not under `plugins/`).
6. **Bump** `agents/README.md`'s status table count.

See `references/conversion-patterns.md §12` for worked examples.

### 2b. SKILL.md Adaptation

Copilot `SKILL.md` files are structurally compatible. Changes needed:

- Ensure frontmatter has `name`, `description`, and add `compatibility: Claude Code`
- Remove or rewrite any `#tool:` references
- Replace `runSubagent` with `Task` tool pattern
- Replace `#context7` with MCP note
- Add `## Claude Code Notes` if adaptations are significant (skip if minimal changes)

**Do not rewrite** content that has no Copilot-specific dependencies — preserve the original workflow logic, templates, and domain knowledge intact.

### 2-instructions. Instructions conversion (`awesome-copilot/instructions/*.instructions.md`)

Instructions are coding-standard fragments with `applyTo:` glob frontmatter. Claude Code has no native `applyTo:` enforcement, but the glob still documents intent.

**Output frontmatter — preserve `applyTo:` verbatim:**

```yaml
---
applyTo: '**/*.ts,**/*.tsx'
description: >
  Short one-line summary verbatim from upstream.
---
```

**Filename**: `a11y.instructions.md` → `a11y.md` (drop the `.instructions` suffix; preserve original kebab-case).

**Body**: leave intact. The body is opinionated standards content (anti-patterns, WCAG references, etc.) and rarely needs Copilot-specific rewrites. If you find a `#tool:` directive or VS Code-only reference, rewrite per the matching rule from `references/conversion-patterns.md`.

**Attribution**: prepend
```markdown
> Ported from awesome-copilot/instructions/<original-filename>
```

**Output** to `instructions/<name>.md` at this repo's root. Bump `instructions/README.md`'s status table.

See `references/conversion-patterns.md §13` for the full pattern.

### 2c. External Repo Plugins (gem-team, etc.)

```bash
# Check if the plugin has its own Claude Code support
cat /path/to/awesome-copilot/plugins/<name>/.github/plugin/plugin.json | jq '.repository'
# Then web_fetch the README from GitHub
```

**gem-team special case:** Already Claude Code-capable via APM. Do not manually convert. Instead, generate a README with APM installation instructions and catalogue the available agents from its README. No file conversion needed.

For other external plugins: web_fetch the GitHub repo, discover the agent/skill structure, then follow Phase 2a/2b normally.

### 2-hooks. Hook bundle conversion (`awesome-copilot/hooks/<bundle>/`)

Copilot hooks ship as a folder containing `hooks.json` + scripts. Claude Code hooks are configured in `~/.claude/settings.json` with a different schema and different event names.

**Event mapping:**

| Copilot event | Claude Code event |
|---|---|
| `sessionStart` | `SessionStart` |
| `sessionEnd` | `Stop` |
| `preToolCall` | `PreToolUse` |
| `postToolCall` | `PostToolUse` |
| `userPrompt` | `UserPromptSubmit` |
| `preNotification` | `Notification` |

**Steps:**

1. Read `hooks.json`. For each event entry, transform `{ type: "command", bash: "<path>", cwd, env, timeoutSec }` to Claude Code's hook entry shape:
   ```json
   {
     "hooks": {
       "<ClaudeCodeEvent>": [
         {
           "matcher": "",
           "hooks": [
             {
               "type": "command",
               "command": "<absolute or .claude-relative path>",
               "timeout": <seconds>
             }
           ]
         }
       ]
     }
   }
   ```
2. Copy scripts verbatim (they are bash/python and run identically).
3. Rewrite any script-internal references to `.github/hooks/<bundle>/` paths so they work from `.claude/hooks/<bundle>/` instead.
4. Write a `claude-settings.json` fragment in the bundle dir — this is what the installer prints to the user (it does **not** auto-merge).
5. Write a `README.md` documenting: events covered, env vars, script reqs (e.g. `jq`, `npm`), security notes.

**Output** to `hooks/<bundle-name>/{<scripts>,claude-settings.json,README.md}` at this repo's root. Bump `hooks/README.md`'s status table.

See `references/conversion-patterns.md §14` for the full event mapping and a worked example.

### 2-workflows. Workflow conversion (`awesome-copilot/workflows/<name>.md`)

Upstream workflows are markdown agent prompts with YAML frontmatter describing schedule, permissions, and outputs. The execution model is GitHub Actions invoking the Copilot CLI.

**Steps:**

1. Copy the markdown verbatim to `workflows/<name>.md` at this repo's root.
2. Adjust the frontmatter:
   - Keep `name`, `description`.
   - Preserve `on.schedule`, `permissions` as documentation — even though Claude Code does not interpret them directly.
   - Rewrite `safe-outputs` to a comment block explaining how the corresponding outputs map to Claude Code tools (`gh issue create`, etc.).
3. Generate a companion `workflows/<name>.github-action.yml` template that:
   - Uses `anthropic/claude-code-action` (or `claude --print --agent`) as the runner.
   - Wires the markdown prompt as input.
   - Sets the same `on:` schedule and `permissions:` as the upstream YAML in the frontmatter.
4. Prepend attribution at the top of the markdown:
   ```markdown
   > Ported from awesome-copilot/workflows/<original-filename>
   ```

**Output** to `workflows/<name>.md` and `workflows/<name>.github-action.yml`. Bump `workflows/README.md`'s status table.

See `references/conversion-patterns.md §15` for the full pattern.

### 2-cookbook. Cookbook recipe conversion (`awesome-copilot/cookbook/<recipe>/`)

The upstream cookbook targets the GitHub Copilot SDK — a different API surface from Anthropic's. Each recipe is converted **case-by-case**, not by a mechanical rule.

**Decision framework:**

| Recipe theme | Target Claude analog |
|---|---|
| Ralph Loop (autonomous coding loops) | `claude --print` loop or Agent SDK |
| Error handling | `@anthropic-ai/sdk` error types + retry/backoff |
| Multiple sessions | Anthropic SDK conversation IDs OR `claude --session-id` |
| Persisting sessions | `claude --session-id` + filesystem snapshots |
| MCP integrations | Direct — Claude Code consumes MCP natively |
| Copilot-SDK-specific telemetry / marketplace APIs | **Skip** — no analog |

**Steps:**

1. Read all language-flavoured implementations (`dotnet/`, `nodejs/`, `python/`) in the upstream recipe.
2. For each language, write the equivalent against Anthropic's SDK (`anthropic`, `@anthropic-ai/sdk`, `Anthropic.SDK`).
3. Write a top-level `cookbook/<recipe>/README.md` summarising the problem and listing per-language implementations.

**Output** to `cookbook/<recipe-name>/`. Bump `cookbook/README.md`'s status table.

See `references/conversion-patterns.md §16` for the decision framework.

---

## Phase 3 — Output

### Directory structure

**Plugin bundle:**
```
plugins/<plugin-name>/
├── README.md
├── plugin.json        ← Claude Code plugin manifest (preserves upstream metadata)
├── agents/
│   ├── <agent-name>.md
│   └── ...
├── instructions/      ← optional
└── skills/
    └── <skill-name>/
        └── SKILL.md
```

**Other artefacts** land at the matching top-level directory — see Phase 0.

### Plugin README.md template

```markdown
# <Plugin Name> — Claude Code Port

> Ported from GitHub Copilot plugin `<original-name>` v<version>
> Original author: <author> | License: <license>
> Converted: <date>

## Agent Team

| Agent | File | Model | Role |
|-------|------|-------|------|
| Name  | `agents/<name>.md` | `claude-*` | One-line role |

## Orchestration Pattern

[Describe how agents coordinate: who orchestrates whom, what the handoff protocol is, how context survives across invocations]

## Installation

```bash
# Install agents
cp agents/*.md ~/.claude/agents/

# Install skills (if any)
cp -r skills/* /path/to/your/claude-skills/

# Verify
claude /agents
```

## Usage

[Key invocation patterns — what to say to Claude Code to activate each agent]

## MCP Dependencies (if any)

[List any MCP servers needed, with config snippets for ~/.claude/settings.json]

## Claude Code Notes

[Key differences from the original Copilot plugin. What was adapted and why. Any known limitations or behaviours that differ from the Copilot version.]
```

### Plugin manifest (`plugin.json`)

Mirror the upstream `.github/plugin/plugin.json` shape. Adapt fields:

```json
{
  "name": "<plugin-name>",
  "description": "<one-line>",
  "version": "<upstream-version>",
  "author": { "name": "<author>" },
  "repository": "https://github.com/github/awesome-copilot",
  "license": "<upstream-license>",
  "keywords": ["..."],
  "agents": ["./agents"],
  "skills": ["./skills/<each-skill>"],
  "instructions": ["./instructions"]
}
```

---

## Phase 4 — Catalogue Entry

Open the running `CATALOGUE.md` at the repo root. Append (or update) under the appropriate section heading:

- Plugins → under `## Plugins` (with full agent roster, orchestration flow, install snippet)
- Agents → under `## Agents` (one-line entry per agent)
- Instructions → under `## Instructions` (grouped by topic family)
- Hooks → under `## Hooks` (per-bundle entry with events covered)
- Workflows → under `## Workflows` (one-line per workflow)
- Cookbook → under `## Cookbook` (one-line per recipe)

Each ported artefact must also bump the corresponding bucket `README.md`'s status table (`Ported: N` count).

---

## Batch Mode

To discover all multi-agent candidates in the marketplace:

```bash
cat /path/to/awesome-copilot/.github/plugin/marketplace.json \
  | jq -r '.plugins[] | select(.description | test("agent|orchestrat|team|subagent|workflow"; "i")) | .name'
```

To list every upstream artefact for bulk porting:

```bash
ls /path/to/awesome-copilot/agents/        # 211 standalone agents (Phase B)
ls /path/to/awesome-copilot/instructions/  # 183 instructions     (Phase D)
ls /path/to/awesome-copilot/plugins/       # 67 plugin bundles    (Phase C)
ls /path/to/awesome-copilot/hooks/         # 6 hook bundles       (Phase E)
ls /path/to/awesome-copilot/workflows/     # 8 workflows          (Phase E)
ls /path/to/awesome-copilot/cookbook/      # 3 recipe sets        (Phase E)
```

For batch conversion: run the full Phase 0 → Phase 4 workflow for each artefact in sequence. After the batch, generate a summary report grouping artefacts by type and bucket.

---

## Quality Gate

Before finalising any converted artefact, verify:

**For all types:**
- [ ] Phase 0 dispatcher invoked — correct artefact type identified
- [ ] Attribution line present at top of body (or in README for bundle types)
- [ ] Upstream licence preserved (file-level or per-bundle)
- [ ] Bucket README status table bumped
- [ ] Catalogue entry appended

**For agents (standalone or plugin-embedded):**
- [ ] Frontmatter: only `name`, `description`, `model` — no `tools` or `agents` keys
- [ ] All `#tool:` references removed or adapted
- [ ] All Copilot/OpenAI model names replaced with Claude equivalents
- [ ] `runSubagent` → `Task` tool pattern applied everywhere
- [ ] VS Code-specific patterns removed or replaced with bash
- [ ] `## Claude Code Notes` section present if any adaptations were made
- [ ] Filename lowercase-hyphenated, `.agent.md` suffix dropped (standalone only)

**For instructions:**
- [ ] `applyTo:` glob preserved in frontmatter
- [ ] Filename `.instructions.md` suffix dropped

**For hooks:**
- [ ] Copilot events mapped to Claude Code events
- [ ] `claude-settings.json` fragment generated (not merged)
- [ ] README documents events, env vars, dependencies, security notes
- [ ] Script-internal `.github/hooks/` paths rewritten to `.claude/hooks/`

**For workflows:**
- [ ] Markdown prompt copied with frontmatter preserved
- [ ] `<name>.github-action.yml` companion generated
- [ ] Upstream `on.schedule` and `permissions` preserved

**For cookbook recipes:**
- [ ] Anthropic SDK used (no Copilot-SDK references in code)
- [ ] Recipes targeting Copilot-only APIs marked as skipped, not stub-ported

**For plugin bundles:**
- [ ] `plugin.json` present and mirrors upstream metadata
- [ ] README.md installation instructions accurate (paths exist, commands work)

---

## Reference Files

Read these before converting — they contain the full lookup tables:

| File | Contents |
|---|---|
| `references/tool-mapping.md` | Complete Copilot tool → Claude Code tool mapping |
| `references/model-mapping.md` | Copilot/OpenAI model → Claude model tier mapping |
| `references/conversion-patterns.md` | Pattern-by-pattern transformation guide with before/after for all 7 artefact types |

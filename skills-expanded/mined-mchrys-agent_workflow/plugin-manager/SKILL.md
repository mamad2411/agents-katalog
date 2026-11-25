---
name: plugin-manager
version: 1.3.0
description: CRUD operations for Claude SDK plugins - create, update, version, add files/folders to plugins. Use when user wants to create a new plugin, update an existing plugin, add files to a plugin, version a plugin, or manage plugin structure. Triggers on keywords like plugin create, plugin update, new plugin, modify plugin, add to plugin, plugin version.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebSearch, WebFetch
---

# Plugin Manager Skill

## News & Releases

### v1.3.0 - Similarity Score Search (Latest)

**Breaking Change**: La recherche de plugins utilise maintenant un **seuil de similarité** au lieu d'un nombre max de résultats.

```python
# Avant (v1.2.0) - Limité à N résultats
results = await registry.search("deploy", max_results=5)

# Après (v1.3.0) - Tous les plugins >= seuil
results = await registry.search("deploy", min_score=0.5)
```

**Pourquoi ce changement ?**
- Plus intelligent: retourne TOUS les plugins pertinents
- Pas de plugins importants manqués à cause d'une limite arbitraire
- Contrôle fin sur la pertinence via le seuil

**Seuils recommandés:**
| `min_score` | Usage |
|-------------|-------|
| **0.7+** | Haute pertinence - requêtes ciblées |
| **0.5** | Pertinence moyenne (défaut) |
| **0.3+** | Faible pertinence - recherche large |

---

## Objective

Manage Claude SDK plugins with full CRUD operations:
- **Create** new plugins with context from files and web docs
- **Update** existing plugins (add files, modify content)
- **Version** plugins with automatic changelog
- **List** available plugins
- **Show** plugin details

## When to Use

- User asks to **create a plugin** or **new plugin**
- User wants to **update a plugin** or **modify a plugin**
- User requests to **add files/folders** to a plugin
- User mentions **plugin version** or **plugin changelog**
- User wants to **list plugins** or **show plugin structure**
- User provides **context files** or **documentation URLs** for plugin creation

## Plugin Structure

A Claude SDK plugin lives in `.claude/skills/<plugin-name>/` with this structure:

```
.claude/skills/<plugin-name>/
├── SKILL.md           # Required: Main skill definition with changelog
├── reference.md       # Optional: Extended documentation
├── examples.md        # Optional: Usage examples
├── context/           # Optional: Source reference files
├── templates/         # Optional: Reusable templates
├── scripts/           # Optional: Helper scripts
└── <custom-files>     # Any additional files needed
```

## Operations

### 1. CREATE Plugin

**Command**: `/plugin create <description> [--name <name>] [--path <dir>] [--url <url>...]`

**Arguments**:

| Argument | Required | Description |
|----------|----------|-------------|
| `<description>` | Yes | What the plugin does |
| `--name <name>` | No | Force plugin name (kebab-case) |
| `--path <directory>` | No | Local files to use as context |
| `--url <url>` | No | Web documentation to fetch (repeatable) |

**Supported Context Files** (--path):

| Type | Extensions | What to Extract |
|------|------------|-----------------|
| Documentation | `.md` | Guides, examples, instructions |
| Configuration | `.yaml`, `.yml`, `.json`, `.toml` | Schemas, configs, specs |
| Python | `.py` | Classes, functions, patterns |
| TypeScript/JS | `.ts`, `.tsx`, `.js`, `.jsx` | Types, components |
| Shell | `.sh` | Commands, scripts |
| Database | `.sql` | Queries, schemas |
| Other | `.go`, `.rs`, `.java` | Patterns, types |

**Process**:

1. **Parse Arguments**:
   - Extract description (text before first --)
   - Extract --name if provided
   - Extract --path if provided
   - Extract all --url occurrences

2. **Gather Local Context** (if --path):
   ```bash
   # Find all context files
   find <path> -type f \( -name "*.md" -o -name "*.yaml" -o -name "*.json" ... \)
   ```
   - Read each file
   - Extract key patterns, APIs, configs
   - Build context summary

3. **Fetch Web Documentation** (if --url):
   ```
   For each URL:
   - WebFetch the page
   - Extract terminology, patterns, examples
   - Build web context summary
   ```

4. **Generate Name**:
   - Use --name if provided
   - Otherwise derive from description
   - Validate kebab-case, max 64 chars

5. **Create Structure**:
   ```bash
   mkdir -p .claude/skills/<name>/{scripts,templates,context}
   ```

6. **Generate SKILL.md**:
   - Frontmatter with version 1.0.0
   - Context Sources section (if --path or --url)
   - Instructions derived from context
   - Examples from context
   - Changelog with v1.0.0

7. **Copy Reference Files** (optional):
   - Copy important context files to `context/`
   - Create `reference.md` with extracted info

**Examples**:

```bash
# Simple - auto-generate name
/plugin create A git commit analyzer

# With explicit name
/plugin create A git analyzer --name git-helper

# With local context
/plugin create FastAPI helper --path ./src/api/ --name fastapi-dev

# With web docs
/plugin create Kubernetes deployment --url https://kubernetes.io/docs/concepts/

# Full combo
/plugin create AWS Lambda manager --name lambda-ops \
  --path ./infrastructure/lambda/ \
  --url https://docs.aws.amazon.com/lambda/ \
  --url https://docs.aws.amazon.com/cli/
```

### 2. UPDATE Plugin

**Command**: `/plugin update <plugin-name> <description of changes>`

**Version Bump Detection**:
- `[major]` or keywords: breaking, rewrite, remove → X.0.0
- `[minor]` or keywords: add, new, feature → 0.X.0
- Default: patch → 0.0.X

**Process**:
1. Locate plugin in `.claude/skills/<plugin-name>/`
2. Read current version from SKILL.md
3. Apply requested changes
4. Bump version appropriately
5. Add changelog entry with separator

**Examples**:
```bash
/plugin update session-manager Add window splitting support
/plugin update my-plugin [major] Complete rewrite
/plugin update my-plugin Fix typo in docs
```

### 3. ADD to Plugin

**Command**: `/plugin add <plugin-name> <file-or-folder> [content-description]`

**Process**:
1. Locate plugin
2. Create file/folder at specified path
3. Generate content if description provided
4. Bump patch version
5. Add changelog entry

**Examples**:
```bash
/plugin add session-manager scripts/cleanup.sh A cleanup script
/plugin add my-plugin templates/ (creates folder)
/plugin add my-plugin examples.md Usage examples
```

### 4. LIST Plugins

**Command**: `/plugin list`

**Output**:
```
Available Plugins (5):

Name                    Version   Description
────────────────────────────────────────────────────────────────
plugin-manager          v1.1.0    CRUD operations for plugins
session-manager         v2.1.0    Tmux session management
...
```

### 5. SHOW Plugin

**Command**: `/plugin show <plugin-name>`

**Output**:
```
Plugin: session-manager
Version: v2.1.0
Path: .claude/skills/session-manager/
Tools: Bash, Read, Write, Edit

Structure:
├── SKILL.md (45 KB)
├── reference.md (12 KB)
├── context/
│   └── api-spec.yaml
└── scripts/
    └── monitor.sh

Changelog (last 3):
  v2.1.0 (2026-01-25) - Added window splitting
  v2.0.0 (2026-01-20) - Complete rewrite
  v1.0.0 (2026-01-15) - Initial release
```

## SKILL.md Template with Versioning

```markdown
---
name: plugin-name
version: 1.0.0
description: Plugin description with trigger keywords
allowed-tools: Tool1, Tool2, Tool3
---

# Plugin Name

## Objective
...

## When to Use
...

## Context Sources (if --path or --url used)

### Local Documentation
- `path/file.md` - Description

### Web Documentation
- https://example.com - Description

## Instructions
...

## Reference (extracted from context)
...

## Examples (from context)
...

## Expected Output
...

---

## Changelog

__________
### v1.0.0 (YYYY-MM-DD)
- Initial release
- Context sources: local files, web docs
__________
```

## Changelog Format

Use `__________` (10 underscores) as separators:

```markdown
## Changelog

__________
### v1.2.0 (2026-01-25)
- Added: New feature X
- Changed: Updated section Y
- Fixed: Bug in Z
__________

__________
### v1.1.0 (2026-01-20)
- Added: reference.md
__________
```

## Version Increment Rules

| Change Type | Bump | Trigger Words |
|-------------|------|---------------|
| Breaking | Major | breaking, rewrite, remove, [major] |
| Features | Minor | add, new, feature, support, [minor] |
| Fixes | Patch | fix, update, typo, docs, [patch] |

## Helper Script

Use `scripts/plugin_crud.py` for programmatic operations:

```python
from plugin_crud import PluginManager

pm = PluginManager()

# Create with context
pm.create(
    name="my-plugin",
    description="My plugin description",
    tools=["Bash", "Read", "WebFetch"],
    create_reference=True
)

# Update
pm.update("my-plugin", changes="Added feature", bump="minor")

# Add file
pm.add_file("my-plugin", "examples.md", content="# Examples")

# List
plugins = pm.list_all()
```

## Integration with Commands

- `/plugin create` → Full creation with context support
- `/plugin update` → Update with auto-versioning
- `/plugin add` → Add files/folders
- `/plugin list` → List all plugins
- `/plugin show` → Show plugin details

See [reference.md](reference.md) for complete command reference.

---

## Graphiti Integration (Semantic Search)

Plugins are automatically indexed into **Graphiti** for semantic search and context enrichment.

### How It Works

1. **Plugin Indexing**: Each plugin is indexed as an episode in Graphiti
   - Entity type: `claude_plugin`
   - Group ID: `claude-plugins`
   - Content: Full SKILL.md with description, triggers, and instructions

2. **Semantic Search**: When a user query is received:
   - Search plugins matching the query semantically
   - Return plugins sorted by relevance score
   - Include matched triggers

3. **Context Enrichment**: Before agent execution:
   - Search for relevant plugins
   - Inject matching plugins into QueryContext
   - Agent receives plugin instructions as context

### Usage

```python
from agent_workflow.integration import (
    PluginRegistry,
    enrich_agent_context,
    create_plugin_hooks,
)

# Initialize registry
registry = PluginRegistry(skills_path=".claude/skills")
await registry.connect()

# Index all plugins into Graphiti
await registry.index_all_plugins()

# Search by similarity score (returns ALL plugins >= threshold)
results = await registry.search("deploy kubernetes", min_score=0.5)
for r in results:
    print(f"{r.plugin.name}: score={r.score:.2f}")

# More focused search (only high relevance)
results = await registry.search("deploy kubernetes", min_score=0.7)

# Enrich context before agent execution
ctx = await enrich_agent_context(
    query="deploy to kubernetes cluster",
    context=my_context,
    min_score=0.5,  # All plugins >= 50% similarity
)

# Or use hooks for automatic enrichment
enricher = create_plugin_hooks(min_score=0.5)
enriched_ctx, result = await enricher.enrich(ctx, user_query)
```

### Similarity Score Thresholds

| Threshold | Description | Use Case |
|-----------|-------------|----------|
| `min_score=0.7` | Haute pertinence | Requêtes très spécifiques |
| `min_score=0.5` | Pertinence moyenne | **Défaut** - bon équilibre |
| `min_score=0.3` | Faible pertinence | Exploration large |

### Automatic Enrichment

Wrap your agent for automatic plugin enrichment:

```python
from agent_workflow.integration import wrap_agent_with_plugins

# Wrap agent with similarity threshold
enhanced_run = wrap_agent_with_plugins(my_agent, min_score=0.5)

# Each run automatically enriches context with plugins >= 50% similarity
result = await enhanced_run("deploy to kubernetes", context=my_ctx)

# For focused queries, use higher threshold
focused_run = wrap_agent_with_plugins(my_agent, min_score=0.7)
```

### Plugin Entity Structure

Each indexed plugin contains:

```python
PluginEntity(
    name="plugin-name",
    version="1.0.0",
    description="Full description with triggers",
    path=".claude/skills/plugin-name/",
    allowed_tools=["Bash", "Read", "Write"],
    triggers=["trigger 1", "trigger 2"],
    skill_content="Full SKILL.md content",
    files=["SKILL.md", "reference.md"],
    indexed_at=datetime,
)
```

### Search Results

Search returns `PluginSearchResult`:

```python
PluginSearchResult(
    plugin=PluginEntity(...),
    score=0.85,  # Semantic similarity score
    matched_triggers=["deploy", "kubernetes"],
)
```

---

## Changelog

__________
### v1.3.0 (2026-01-25)
- **BREAKING**: Changed search to use `min_score` threshold instead of `max_results`
- Changed: `search()` now returns ALL plugins above similarity threshold
- Changed: `min_score=0.5` is the new default (medium relevance)
- Changed: `max_results` is now optional (None = no limit)
- Added: Improved local search scoring (description, triggers, name, content)
- Added: Detailed logging with score threshold info
- Updated: All convenience functions use `min_score` as primary parameter
- Updated: Documentation with similarity threshold guide
__________

__________
### v1.2.0 (2026-01-25)
- Added: Graphiti integration for semantic plugin search
- Added: PluginEntity for Graphiti indexing
- Added: PluginRegistry for plugin lifecycle management
- Added: Automatic context enrichment with relevant plugins
- Added: Plugin hooks for agent integration
- Added: wrap_agent_with_plugins for automatic enrichment
__________

__________
### v1.1.0 (2026-01-25)
- Added: --name argument for explicit plugin naming
- Added: --path argument for local context files
- Added: --url argument for web documentation fetching
- Added: WebSearch and WebFetch to allowed tools
- Added: context/ directory in plugin structure
- Added: Support for multiple file types as context
- Changed: Create command now processes context before generating
__________

__________
### v1.0.0 (2026-01-25)
- Initial release
- Create, Update, Add, List, Show operations
- Automatic versioning with semantic versioning
- Changelog format with separator lines
- Python helper script for automation
- Integration with slash commands
__________

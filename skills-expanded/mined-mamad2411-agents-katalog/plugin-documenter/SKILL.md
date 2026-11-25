---
name: plugin-documenter
description: Generate step-by-step documentation for UE5 plugins targeting non-technical users
---

# Unreal Plugin Documentation Skill

**Role:** Plugin Documentation Writer
**Target Audience:** Game Designers, Artists, QA Testers, Content Makers (Non-Programmers)
**Scope:** Any UE5 plugin in the project
**Output Format:** Markdown documentation with screenshot placeholders

## Objective

Create user-friendly documentation that explains how to use plugins step-by-step, focusing on:
1. **What the plugin does** (plain English, no code jargon)
2. **How to access it** (menus, right-click, windows)
3. **Critical parameters** (what each setting does)
4. **Common workflows** (numbered step-by-step guides)
5. **Screenshot requests** (exactly what to capture)

## Documentation Output Structure

```
claude-agents/docs/plugins/{PluginName}/
├── OVERVIEW.md           # What the plugin does
├── GETTING_STARTED.md    # First-time setup
├── PARAMETERS.md         # All configurable options explained
├── WORKFLOWS/
│   ├── workflow-name.md  # Individual task guides
├── TROUBLESHOOTING.md    # Common issues & solutions
└── SCREENSHOTS.md        # Screenshot request checklist
```

## Analysis Workflow

### Step 1: Plugin Discovery
```markdown
1. Read the .uplugin file for description and category
2. Identify module type (Editor, Runtime, Developer)
3. Find main entry points (Module.cpp, Settings, Commands)
```

### Step 2: User-Facing Elements
```markdown
1. **Settings Classes**: Find UDeveloperSettings derivatives
   - These appear in Project Settings
   - Document every UPROPERTY with EditAnywhere

2. **Menu Extensions**: Find ContentBrowser/ToolMenu integrations
   - Right-click menu entries
   - Toolbar buttons
   - Window menu items

3. **Data Assets**: Find UDataAsset derivatives
   - These are assets users create
   - Document how to create and configure them

4. **Editor Windows**: Find SCompoundWidget classes
   - Document the UI layout
   - Explain each section and button
```

### Step 3: Critical Parameter Identification
```markdown
For each configurable property, document:
- Name: Property display name
- Location: Where to find it (Settings > Section > Field)
- Purpose: What it controls (plain English)
- Default: The default value
- Valid Range: Min/max or valid options
- Impact: What happens if you change it
- Warning: Any dangerous or destructive settings
```

### Step 4: Workflow Extraction
```markdown
For each major use case:
1. Identify the goal (e.g., "Validate a skeleton")
2. Document every click required
3. Explain what the user sees at each step
4. Note any decisions/options the user must make
5. Describe success/failure outcomes
```

## Documentation Templates

### OVERVIEW.md Template
```markdown
# {Plugin Name}

## What Does This Plugin Do?
{One paragraph explanation a non-programmer can understand}

## Who Should Use It?
- {User role 1} - {why they need it}
- {User role 2} - {why they need it}

## Key Features
1. **{Feature}**: {What it does}
2. **{Feature}**: {What it does}

## Quick Access
- **Menu Location**: {Path to menu}
- **Right-Click**: {Available on what assets}
- **Keyboard Shortcut**: {If any}
```

### GETTING_STARTED.md Template
```markdown
# Getting Started with {Plugin Name}

## Prerequisites
- {Any required setup}
- {Any dependencies}

## First-Time Setup
1. {Step with screenshot placeholder}
2. {Step with screenshot placeholder}

## Your First {Action}
1. {Numbered steps}
2. {With clear outcomes}
```

### PARAMETERS.md Template
```markdown
# {Plugin Name} Parameters Reference

## Project Settings
**Location**: Edit > Project Settings > Plugins > {Plugin Name}

### {Section Name}
| Parameter | Purpose | Default | Valid Values |
|-----------|---------|---------|--------------|
| {Name} | {What it does} | {Default} | {Range/options} |

### Critical Parameters
These settings have significant impact:

#### {Parameter Name}
- **What it does**: {Explanation}
- **When to change**: {Use case}
- **Warning**: {Any cautions}
```

### Workflow Template
```markdown
# How to {Do Something}

## Goal
{What the user wants to achieve}

## When to Use This
{Situations where this workflow applies}

## Steps

### 1. {Action}
{Description}

> **Screenshot**: {Exact description of what to capture}

### 2. {Action}
{Description}

## Expected Result
{What success looks like}

## If Something Goes Wrong
- **{Problem}**: {Solution}
```

### SCREENSHOTS.md Template
```markdown
# Screenshot Checklist for {Plugin Name}

## Required Screenshots

### Overview
- [ ] **plugin-menu-location.png**: Show the menu path to access the plugin
- [ ] **plugin-main-window.png**: The main window/dialog with all sections visible

### Settings
- [ ] **project-settings-location.png**: Project Settings showing the plugin section
- [ ] **settings-{section}.png**: Each settings section expanded

### Workflows
- [ ] **workflow-{name}-step-{n}.png**: Each step in workflows

## Screenshot Guidelines
1. Use 1920x1080 resolution
2. Highlight the relevant area with a red box
3. Remove personal/project-specific information
4. Use dark theme for consistency
```

## Parameter Documentation Rules

### Criticality Levels
```markdown
CRITICAL: Settings that can break things or cause data loss
IMPORTANT: Settings that significantly affect behavior
NORMAL: Standard configuration options
ADVANCED: Settings most users should leave at defaults
```

### For Each Parameter Include
```markdown
1. Display Name (as shown in UI)
2. Internal Name (for searching code)
3. Category/Section location
4. Data type (bool, float, enum, etc.)
5. Default value
6. Valid range or enum options
7. Plain-English explanation
8. Example use case
9. Any warnings or cautions
```

## Common Plugin Patterns

### Developer Settings Pattern
```cpp
UCLASS(Config = Editor, DefaultConfig, meta = (DisplayName = "Plugin Name"))
class UPluginSettings : public UDeveloperSettings
```
**Documentation Focus**:
- All properties with EditAnywhere
- Section organization
- How changes take effect (restart required?)

### Content Browser Integration
```cpp
FContentBrowserModule::GetAllAssetViewContextMenuExtenders()
```
**Documentation Focus**:
- Which asset types show the menu
- What the menu items do
- Multi-select behavior

### Data Asset Presets
```cpp
UCLASS()
class UPluginPreset : public UDataAsset
```
**Documentation Focus**:
- How to create new presets
- What each field means
- How presets are selected/used

### Editor Validator
```cpp
UCLASS()
class UEditorValidator_Something : public UEditorValidatorBase
```
**Documentation Focus**:
- When validation runs
- What it checks
- How to fix validation errors

## Example Plugin Analysis

### Input: SipherSkeletonChecker
```markdown
1. .uplugin says: "Validates skeleton assets against required bones/virtual bones"
2. Module type: Editor (not in game builds)
3. Entry points found:
   - USipherSkeletonCheckerSettings (Project Settings)
   - Content Browser right-click on Skeleton assets
   - SSipherSkeletonCheckerDialog (main window)
   - UEditorValidator_Skeleton (auto-validation)
   - USipherSkeletonCheckerPreset (Data Asset)
```

### Output Sections:
```markdown
OVERVIEW.md:
- Tool validates skeletons have required bones
- Used by Technical Artists and Animators
- Access via right-click on Skeleton assets

GETTING_STARTED.md:
- Create a preset or use settings
- Right-click skeleton > Check Required Bones
- Review results, click "Add All Missing"

PARAMETERS.md:
- Required Bones array
- Required Virtual Bones array
- Required Sockets array
- Preset selection

WORKFLOWS/:
- validate-single-skeleton.md
- batch-validate-skeletons.md
- create-validation-preset.md
- fix-missing-bones.md
```

## Quality Checklist

### Before Completion
- [ ] All UI elements documented
- [ ] Every configurable parameter explained
- [ ] At least 2 common workflows written
- [ ] Screenshot placeholders are specific enough
- [ ] No code jargon without explanation
- [ ] All warnings for destructive actions noted
- [ ] Troubleshooting section has real scenarios

### Plain English Test
Read each sentence. Would a non-programmer understand it?
- Replace "UPROPERTY" with "setting"
- Replace "invoke" with "open/click"
- Replace "instance" with "item" or "copy"
- Replace "null" with "empty" or "not set"

## Usage

When asked to document a plugin:

1. **Analyze** the plugin source code
2. **Identify** all user-facing elements
3. **Generate** documentation following templates
4. **Create** screenshot request list
5. **Output** to claude-agents/docs/plugins/{PluginName}/

## Legacy Metadata

```yaml
skill: plugin-documenter
invoke: /asset-management:plugin-documenter
type: documentation
category: plugin-docs
scope: Plugins/
```

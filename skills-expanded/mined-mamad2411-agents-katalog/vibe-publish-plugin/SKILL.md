---
name: vibe-publish-plugin
description: Publish skills, hooks, MCP servers, or plugins to the vibe marketplace. Validates structure, creates PRs, and handles permissions.
disable-model-invocation: true
user-invocable: true
---

# Vibe Publish Plugin

This skill guides you through publishing skills, hooks, MCP servers, or entire plugins to the vibe marketplace. It handles validation, repository setup, and PR creation.

## Overview

The publish workflow:
1. **Detect** what you're publishing (skill, hook, MCP server, or plugin)
2. **Duplicate check** — run `/dupe-check` to verify no similar skill/plugin already exists
3. **Validate** structure and metadata
4. **Determine** destination (existing plugin or new plugin)
5. **Clone** the vibe repo and create a branch
6. **Integrate** your contribution
7. **Create** a pull request

## Phase 1: Detection and Initial Assessment

### Step 1: Scan Current Directory

Look for publishable artifacts in CWD (or user-specified directory):

```
Artifact Detection:
├── Skills: Look for SKILL.md files or skills/ directories
├── Hooks: Look for hook configurations (hooks.yaml, hook scripts)
├── MCP Servers: Look for MCP server definitions (.mcp.json, server code)
├── Plugin: Look for .claude-plugin/plugin.json
└── Nothing found: Offer to create something
```

### Step 2: Handle Empty State

If no publishable artifacts are found, ask the user:

**"I don't see any skills, hooks, MCP servers, or plugins in this directory. Would you like to:"**

1. **Create a new skill** - Invoke `/build-vibe-skill` to build one
2. **Create a new plugin** - Guide through plugin scaffolding
3. **Specify a different directory** - Let user point to their work
4. **Publish from another repository** - Add external repo to marketplace

If user wants to create something new, delegate to the appropriate skill/workflow and return here when done.

## Phase 2: Duplicate Check

**Before proceeding with validation or integration, check whether similar functionality already exists in the vibe marketplace.**

### Step 1: Run the Dupe Check

Invoke the `/dupe-check` skill, passing the name and description of what's being published. This will:

1. Fetch the live marketplace catalog from GitHub
2. Enumerate all installed skills and their descriptions
3. Compare the user's contribution against existing plugins and skills
4. Return a verdict: **DUPLICATE**, **STRONG OVERLAP**, **PARTIAL OVERLAP**, or **CLEAR GAP**

### Step 2: Act on the Verdict

| Verdict | Action |
|---------|--------|
| **DUPLICATE** | **Stop.** Inform the user that an equivalent skill already exists. Show the existing skill name and how to invoke it. Do not proceed with publishing. |
| **STRONG OVERLAP** | **Pause.** Show the overlapping skill, what it covers, and who authored it. Recommend the user coordinate with the original author or contribute to the existing skill instead. Only proceed if the user explicitly confirms they want a separate implementation. |
| **PARTIAL OVERLAP** | **Advise.** Show the related skill and the gap. Suggest adding the new functionality as a skill within the existing plugin rather than creating a standalone plugin. Proceed if the user agrees with the approach. |
| **CLEAR GAP** | **Proceed.** The idea is genuinely new. Continue to Phase 3. |

If the user chooses to proceed despite overlap, document the rationale — it will be included in the PR description (Phase 7).

## Phase 3: Validation

### For Skills (SKILL.md files)

Validate and fix if needed:

```yaml
Required Frontmatter:
  - name: kebab-case-identifier  # Required
  - description: "Clear description with 'when to use' info"  # Required

Optional Frontmatter:
  - user-invocable: true/false   # Allows /skill-name invocation
  - disable-model-invocation: true/false  # Prevents auto-invocation
  - default-model: opus/sonnet/haiku  # Model preference
```

**Validation Checks:**
- [ ] SKILL.md exists and is readable
- [ ] Frontmatter has `name` (kebab-case)
- [ ] Frontmatter has `description` (includes "when to use" context)
- [ ] Body has clear workflow instructions
- [ ] Resources folder (if present) has valid files

**Auto-fixes:**
- Convert name to kebab-case if needed
- Suggest description improvements if too vague
- Add missing optional fields with sensible defaults

### For Hooks

Validate hook configuration:

```yaml
Required:
  - event: PreToolUse|PostToolUse|Stop|SubagentStop|SessionStart|SessionEnd|UserPromptSubmit|PreCompact|Notification
  - Either: command OR prompt

Hook Types:
  - Bash hooks: command field with shell script
  - Prompt hooks: prompt field with instructions
```

### For MCP Servers

Validate MCP server definition:

```yaml
Required:
  - Server type: stdio|sse|http|websocket
  - Command or URL configuration
  - Tool definitions (if applicable)
```

### For Full Plugins

Validate plugin structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # REQUIRED: name, description, version, author
├── skills/                   # Optional: skill directories
├── agents/                   # Optional: agent markdown files
├── commands/                 # Optional: slash commands
├── hooks/                    # Optional: hook configurations
└── resources/                # Optional: shared resources
```

**plugin.json validation:**
```json
{
  "name": "plugin-name",           // Required: kebab-case
  "description": "What it does",   // Required
  "version": "1.0.0",              // Required: semver
  "author": {
    "name": "Author Name"          // Required
  },
  "skills": "./skills/",           // Optional: path to skills
  "commands": "./commands/",       // Optional: path to commands
  "agents": "./agents/"            // Optional: path to agents
}
```

## Phase 4: Determine Destination

### Decision Tree

Ask the user to clarify the destination:

**"Where should this be published?"**

1. **Existing vibe plugin** (most common)
   - Determine which plugin automatically based on content:
     - Databricks-related → `fe-databricks-tools`
     - Salesforce-related → `fe-salesforce-tools`
     - Google Workspace → `fe-google-tools`
     - Internal analytics/Logfood → `fe-internal-tools`
     - Multi-step workflows → `fe-workflows`
     - Environment setup → `fe-vibe-setup`
     - JIRA/ES tickets → `fe-jira-tools`
     - Expenses → `fe-file-expenses`
   - If unsure, ask the user which plugin

2. **New plugin for a team/BU/function**
   - Ask: Which team/BU/function is this for?
   - Plugin name convention: `{team}-{function}` (e.g., `sales-ops-tools`, `apac-demos`)
   - Will create new plugin directory + marketplace entry + CODEOWNERS

3. **External repository**
   - Ask for repository details:
     - Repo URL (GitHub format: `owner/repo`)
     - Branch/ref (default: `main`)
     - Is it public or internal Databricks repo?
   - Will add marketplace entry pointing to external source

## Phase 5: Repository Setup

### Step 1: Clone Vibe Repository

Check if vibe repo exists locally:

```bash
# Check if already in vibe repo
if [ -d ".claude-plugin/marketplace.json" ]; then
  echo "Already in vibe repo"
elif [ -d "$HOME/code/vibe" ]; then
  echo "Found vibe at ~/code/vibe"
else
  # Clone the repo
  git clone git@github.com:databricks/vibe.git "$HOME/code/vibe"
fi
```

### Step 2: Create Feature Branch

```bash
cd ~/code/vibe
git fetch origin
git checkout main
git pull origin main

# Create descriptive branch name
BRANCH_NAME="feat/add-{artifact-type}-{name}"
git checkout -b "$BRANCH_NAME"
```

### Step 3: Copy Artifacts

For skills/hooks/MCP servers going to existing plugins:
```bash
# Copy skill
cp -r /path/to/skill ~/code/vibe/plugins/{target-plugin}/skills/{skill-name}/

# Copy hook
cp /path/to/hook.yaml ~/code/vibe/plugins/{target-plugin}/hooks/

# Copy MCP server
cp -r /path/to/mcp-server ~/code/vibe/plugins/{target-plugin}/mcp-servers/
```

For new plugins:
```bash
# Create plugin directory structure
mkdir -p ~/code/vibe/plugins/{plugin-name}/.claude-plugin
mkdir -p ~/code/vibe/plugins/{plugin-name}/skills
mkdir -p ~/code/vibe/plugins/{plugin-name}/commands
mkdir -p ~/code/vibe/plugins/{plugin-name}/resources

# Copy plugin.json
cp /path/to/plugin.json ~/code/vibe/plugins/{plugin-name}/.claude-plugin/

# Copy all content
cp -r /path/to/skills/* ~/code/vibe/plugins/{plugin-name}/skills/
```

## Phase 6: Update Vibe Configuration

### For New Skills: Add Permission

Add to `~/code/vibe/permissions.yaml`:

```yaml
allow:
  - "Skill(skill-name)"
```

### For New Skills: Add Eval

Add to `~/code/vibe/evals/test-cases/skill-routing.yaml`:

```yaml
- name: "skill-name-basic-test"
  prompt: "Natural language prompt that should trigger this skill"
  expected_skill: "plugin-name:skill-name"
  max_turns: 5
  model: sonnet
```

Ask the user for a good test prompt if not obvious.

### For New Plugins: Update Marketplace

Add entry to `~/code/vibe/.claude-plugin/marketplace.json`:

```json
{
  "name": "plugin-name",
  "source": "./plugins/plugin-name",
  "description": "What this plugin does",
  "version": "1.0.0",
  "author": {
    "name": "Author Name or Team"
  },
  "category": "productivity|development|setup|internal|integration|bundle",
  "keywords": ["relevant", "keywords"]
}
```

### For New Plugins: Update CODEOWNERS

Add entry to `~/code/vibe/.github/CODEOWNERS`:

```
/plugins/{plugin-name}/     @{username}_data
```

Get the user's Databricks GitHub username (format: `firstname-lastname_data`).

### For External Repos: Add Marketplace Entry

Add to `~/code/vibe/.claude-plugin/marketplace.json`:

```json
{
  "name": "plugin-name",
  "source": {
    "source": "github",
    "repo": "owner/repo-name",
    "ref": "main"
  },
  "description": "What this plugin does",
  "version": "1.0.0",
  "author": {
    "name": "Author/Team Name"
  },
  "category": "development",
  "keywords": ["external", "relevant", "keywords"]
}
```

## Phase 7: Create Pull Request

### Step 1: Stage and Commit

```bash
cd ~/code/vibe

# Stage changes
git add plugins/{plugin-name}/
git add permissions.yaml  # if modified
git add evals/test-cases/skill-routing.yaml  # if modified
git add .claude-plugin/marketplace.json  # if modified
git add .github/CODEOWNERS  # if modified

# Commit with descriptive message
git commit -m "$(cat <<'EOF'
feat({plugin}): Add {artifact-name} {artifact-type}

{Brief description of what was added}

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Step 2: Push Branch

```bash
git push -u origin "$BRANCH_NAME"
```

**If push fails with permission error:**

Display this message:

---

**⚠️ Repository Access Required**

You don't have write access to the vibe repository. To get access:

1. Open Okta and go to the **Opal** tile
2. Log into Opal
3. Request access at: https://app.opal.dev/groups/081fdf07-9f0f-4046-8f18-08eeb47e1116
4. Once approved, run `/vibe-publish-plugin` again

Access is typically granted within a few hours.

---

### Step 3: Create PR

```bash
gh pr create \
  --title "feat({plugin}): Add {artifact-name}" \
  --body "$(cat <<'EOF'
## Summary

- Added {artifact-type}: `{artifact-name}` to `{plugin-name}`
- {Brief description of functionality}

### Type of Change

- [x] Feature
- [ ] Bug fix
- [ ] Refactor / Code quality
- [ ] Documentation

{Describe the feature being added}

### AI Assistance

- [x] This PR was created or reviewed with AI assistance

Created using `/vibe-publish-plugin` skill.

### Testing

- Validated {artifact-type} structure and frontmatter
- {Additional testing notes}

### Related Issues

N/A

### Screenshots/Demos

{If applicable, add screenshots or demo links}
EOF
)"
```

## Phase 8: Completion

### Success Output

Display to user:

---

**✅ Pull Request Created**

**PR URL:** {PR URL from gh pr create}

**What was published:**
- Type: {skill/hook/MCP server/plugin}
- Name: {artifact-name}
- Destination: {plugin-name}

**Next steps:**
1. Review the PR at the link above
2. Address any review feedback
3. Once approved, the PR will be merged
4. After merge, users can install with:
   ```bash
   vibe update  # Updates vibe to get new plugin
   # Or for new plugins:
   claude plugin install {plugin-name}@fe-vibe
   ```

---

### Failure Handling

If any step fails:

1. **Clone fails:** Check SSH keys are configured for GitHub
2. **Push fails:** Direct to Opal access request (see Phase 7)
3. **PR creation fails:** Check `gh` CLI is authenticated (`gh auth login`)
4. **Validation fails:** Provide specific fixes and offer to apply them

## Quick Reference

### Supported Artifact Types

| Type | Detection | Destination |
|------|-----------|-------------|
| Skill | `SKILL.md` file | `plugins/{plugin}/skills/{name}/` |
| Hook | `hooks.yaml` or hook scripts | `plugins/{plugin}/hooks/` |
| MCP Server | `.mcp.json` or server code | `plugins/{plugin}/mcp-servers/` |
| Full Plugin | `.claude-plugin/plugin.json` | `plugins/{name}/` |
| External Repo | User specifies URL | Marketplace entry only |

### Plugin Categories

| Category | Use For |
|----------|---------|
| `productivity` | Tools that help with daily work |
| `development` | Code generation, testing, debugging |
| `setup` | Environment and configuration |
| `internal` | Databricks-internal tools |
| `integration` | External service connections |
| `bundle` | Meta-plugins that install multiple plugins |

### CODEOWNERS Username Format

Databricks employees use: `@firstname-lastname_data`

Example: `@brandon-kvarda_data`, `@stuart-gano_data`

## Troubleshooting

### "Permission denied" when pushing

You need write access to the vibe repo. Request access via Opal:
https://app.opal.dev/groups/081fdf07-9f0f-4046-8f18-08eeb47e1116

### "SKILL.md validation failed"

Common issues:
- Missing `name` in frontmatter
- Missing `description` in frontmatter
- Name not in kebab-case (use `my-skill-name` not `mySkillName`)

### "gh: command not found"

Install GitHub CLI:
```bash
brew install gh
gh auth login
```

### "Plugin already exists in marketplace"

If publishing to an existing plugin name, either:
- Choose a different name
- Update the existing plugin instead (different workflow)

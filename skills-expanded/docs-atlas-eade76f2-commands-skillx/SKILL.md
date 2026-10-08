---
title: "Skill Command"
description: "Install Bool CLI agent skill for AI coding assistants"
---

The `bool skill` command installs the Bool CLI agent skill into your project, enabling AI coding assistants to use Bool CLI commands.

## Quick Start

```bash
bool skill
```

This installs the skill to `./.agents/skills/using-bool-cli/`.

## Usage

```bash
bool skill [directory] [options]
```

### Arguments

<ParamField path="directory" type="string" default=".">
  Target directory for skill installation. Defaults to current directory.
  
  ```bash
  bool skill ~/my-project
  ```
</ParamField>

### Options

<ParamField path="--output" type="string">
  Custom output path for the skill folder. Overrides the default `.agents/skills/using-bool-cli` location.
  
  ```bash
  bool skill --output ~/custom/path
  ```
</ParamField>

## Examples

### Install to Current Directory

```bash
bool skill
```

**Output:**
```
✔ Skill installed to .agents/skills/using-bool-cli
Agents can now discover the bool-cli skill in your project.
```

### Install to Specific Project

```bash
bool skill ~/projects/my-website
```

**Output:**
```
✔ Skill installed to /home/user/projects/my-website/.agents/skills/using-bool-cli
Agents can now discover the bool-cli skill in your project.
```

### Custom Output Path

```bash
bool skill --output ~/.config/agent-skills
```

## What Gets Installed

The command copies the Bool CLI skill from the package to your project:

```
.agents/
└── skills/
    └── using-bool-cli/
        ├── SKILL.md           # Skill documentation
        ├── examples/          # Usage examples
        └── ...                # Additional resources
```

### Skill Location in Package

The skill files are bundled with the Bool CLI package:

```
@bool/cli/
└── .agents/
    └── skills/
        └── using-bool-cli/
```

## How It Works

1. Locates the skill source in the Bool CLI package installation
2. Copies the entire skill directory to your project
3. Creates `.agents/skills/` directory structure if needed
4. Preserves all skill files and subdirectories

## Agent Discovery

Once installed, AI coding assistants can discover and use the skill:

1. **Skill manifest**: Agents scan for `.agents/skills/` directories
2. **Skill loading**: Agents read `SKILL.md` for instructions
3. **Command execution**: Agents can invoke Bool CLI commands with proper syntax

### Compatible Agents

Any agent that supports skill discovery from `.agents/skills/` can use this skill, including:

- OpenCode
- Custom AI coding assistants
- Tools that follow the `.agents/skills/` convention

## Skill Contents

The skill includes:

- **Command reference**: Syntax and examples for all Bool CLI commands
- **Workflows**: Common patterns like deployment, version management
- **Best practices**: Error handling, config management, CI/CD integration
- **Examples**: Real-world usage scenarios

## Use Cases

### Enable Agent Deployments

```bash
cd my-project
bool skill

# Now your agent can:
# - Deploy your site: "Deploy this to Bool"
# - Check versions: "Show me the deployment history"
# - Update settings: "Make this Bool public"
```

### Team Onboarding

Include the skill in your repository:

```bash
# In your project repo
bool skill
git add .agents/
git commit -m "Add Bool CLI skill for agents"
git push
```

Team members' agents automatically discover the skill when they clone the repo.

### Multi-Project Setup

Install to a shared location:

```bash
bool skill --output ~/.config/shared-agent-skills/bool-cli
```

Configure your agent to scan that directory for skills.

## Updating the Skill

When you update the Bool CLI, re-run `bool skill` to get the latest version:

```bash
npm update -g @bool/cli
bool skill  # Overwrites with latest version
```

## Removing the Skill

Simply delete the skill directory:

```bash
rm -rf .agents/skills/using-bool-cli
```

## Error Handling

### Skill Files Not Found

```
✖ Skill files not found in the bool-cli package.
```

**Cause**: The Bool CLI installation is corrupted or incomplete.

**Solution**: Reinstall the Bool CLI:

```bash
npm install -g @bool/cli
```

### Permission Denied

```
✖ EACCES: permission denied, mkdir '/path/.agents'
```

**Solution**: Check write permissions for the target directory:

```bash
ls -la ~/my-project
chmod u+w ~/my-project  # If needed
```

## Best Practices

### Include in Version Control

Commit the skill to your repository so all team members benefit:

```gitignore
# .gitignore
# .agents/  # Don't ignore - commit the skill!
```

### Project-Specific Installation

Install skills per-project for better isolation:

```bash
cd project-a
bool skill

cd ../project-b
bool skill
```

### Update Regularly

Keep the skill in sync with CLI updates:

```bash
npm update -g @bool/cli && bool skill
```

## Agent Skill Format

The skill follows the standard agent skill format:

```
.agents/skills/{skill-name}/
├── SKILL.md           # Main skill documentation
├── README.md          # Optional human-readable docs
└── resources/         # Optional additional files
```

Agents read `SKILL.md` to learn how to use Bool CLI commands.

## Example Agent Interactions

Once the skill is installed, agents can help with:

**Deploy command**:
```
User: Deploy this project to Bool
Agent: I'll deploy your project using `bool deploy`
       [Runs: bool deploy -m "Deploy via agent"]
```

**Version history**:
```
User: Show me the deployment history
Agent: [Runs: bool versions]
       Here are your recent deployments...
```

**Configuration**:
```
User: Make this Bool public
Agent: [Runs: bool update --visibility public]
       Updated visibility to public
```

## Related Commands

<CardGroup cols={2}>
  <Card title="Deploy" icon="cloud-arrow-up" href="/commands/versions#deploy">
    Deploy files with the CLI
  </Card>
  <Card title="Authentication" icon="key" href="/commands/auth">
    Set up API credentials for agents
  </Card>
  <Card title="Shipit" icon="rocket" href="/commands/shipit">
    Quick anonymous deployments
  </Card>
</CardGroup>

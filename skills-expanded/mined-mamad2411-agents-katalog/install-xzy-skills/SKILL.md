---
name: install-xzy-skills
version: 1
description: >-
  Install every skill from the sanxzy/Skills collection into the current project. Triggers on "install xzy skills", "setup xzy skills", "add all xzy skills", or "/install-xzy-skills". Symlinks all skills to .agents/skills/ and reports a summary of what was installed.
---

# Install XZY Skills

Run `npx skills add sanxzy/Skills --all` to install every skill from the sanxzy/Skills GitHub repository into the current project, targeting all agent directories via symlinks.

## Core rules

1. **Project scope only.** Never pass `-g`. All skills install under `.agents/skills/` in the current project directory.
2. **Idempotent.** Re-running installs new skills and updates existing ones. Safe to invoke repeatedly.
3. **All agents, all skills.** Uses `--all` which implies `--skill '*'`, `--agent '*'`, and `-y`.
4. **Summary, not raw output.** Parse the CLI output and report a brief summary — do not dump stdout to the user.

## Workflow

### 1. Run the install

Execute:

```bash
npx skills add sanxzy/Skills --all
```

### 2. Parse output

Read the CLI output. Extract:
- Number of skills installed.
- Target directory (`.agents/skills/`).
- Any errors or warnings.

### 3. Report summary

Tell the user what happened. Example:

> Installed 30 skills to .agents/skills/ — symlinks created for all detected agents.

If the command fails, report the error and suggest the user check network access or run `npx skills add sanxzy/Skills --all` manually to see full output.

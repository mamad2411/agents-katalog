# Install Prompt for Coding Assistants

Use the prompt below in Codex, Claude Code, Cursor, or a similar local coding assistant.

## Standard prompt

```text
Clone https://github.com/cubetribe/GitHub-Skill_CODEX_ClaudeCode.git into a sensible local workspace folder on this machine. Then enter the repository root and run ./scripts/install-skill-locally.sh so the github-master skill is installed into ~/.codex/skills/github-master and ~/.claude/skills/github-master. After installation, verify that both target folders contain SKILL.md, agents/openai.yaml, references/, assets/, and scripts/repo_preflight.py. Report the local clone path, the install result for Codex and Claude Code, and any missing prerequisites. Do not push anything to GitHub.
```

## Codex-only variant

```text
Clone https://github.com/cubetribe/GitHub-Skill_CODEX_ClaudeCode.git into a sensible local workspace folder on this machine. Then enter the repository root and run ./scripts/install-skill-locally.sh --codex-only so the github-master skill is installed into ~/.codex/skills/github-master. After installation, verify that the target folder contains SKILL.md, agents/openai.yaml, references/, assets/, and scripts/repo_preflight.py. Report the local clone path, the install result, and any missing prerequisites. Do not push anything to GitHub.
```

## Claude Code-only variant

```text
Clone https://github.com/cubetribe/GitHub-Skill_CODEX_ClaudeCode.git into a sensible local workspace folder on this machine. Then enter the repository root and run ./scripts/install-skill-locally.sh --claude-only so the github-master skill is installed into ~/.claude/skills/github-master. After installation, verify that the target folder contains SKILL.md, agents/openai.yaml, references/, assets/, and scripts/repo_preflight.py. Report the local clone path, the install result, and any missing prerequisites. Do not push anything to GitHub.
```

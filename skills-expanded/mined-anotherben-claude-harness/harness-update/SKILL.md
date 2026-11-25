---
name: harness-update
description: "Pull latest skills from claude-harness repo and sync to ~/.claude/skills/ and ~/.codex/skills/. Run this in any project to get the latest enterprise skills. Use when the user says 'update skills', 'sync skills', 'pull latest harness', or invokes /harness-update."
---

# Harness Update

Pull latest skills from the claude-harness repo and deploy full skill directories
to Claude Code and Codex.

## Rules

- Do not sync only `SKILL.md`; copy each full skill directory so scripts, evals,
  templates, references, and agents metadata stay usable.
- Do not delete unrelated local skills from `~/.claude/skills` or
  `~/.codex/skills`.
- Do not replace full skill directories with link-only entries.
- Rebuild the skills-index compiled cache after syncing when the local
  `skills-index` package is available.
- Verify representative skills before claiming the update is complete.

## Steps

1. Pull latest from claude-harness:

```bash
cd ~/claude-harness && git pull origin main
```

2. Sync full skill directories to Claude Code and Codex:

```bash
for skill_dir in ~/claude-harness/skills/*; do
  [ -d "$skill_dir" ] || continue
  name=$(basename "$skill_dir")
  case "$name" in
    *-workspace) continue ;;
  esac
  mkdir -p ~/.claude/skills/"$name" ~/.codex/skills/"$name"
  rsync -a --delete --exclude='node_modules/' --exclude='__pycache__/' "$skill_dir"/ ~/.claude/skills/"$name"/
  rsync -a --delete --exclude='node_modules/' --exclude='__pycache__/' "$skill_dir"/ ~/.codex/skills/"$name"/
done
```

3. Rebuild the skills index if available:

```bash
if [ -d ~/claude-harness/skills-index ]; then
  cd ~/claude-harness/skills-index
  npm rebuild better-sqlite3 sqlite-vec >/dev/null 2>&1 || true
  npm run index -- --repo-root "${CLAUDE_PROJECT_DIR:-$PWD}" || true
fi
```

4. Verify representative transferred skills:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.claude/skills/diagnose
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/skills/diagnostic-cohort
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/skills/zoom-out
```

5. Report what was updated:

```bash
echo "Claude skills: $(ls ~/.claude/skills/*/SKILL.md 2>/dev/null | wc -l)"
echo "Codex skills: $(ls ~/.codex/skills/*/SKILL.md 2>/dev/null | wc -l)"
echo "Harness version: $(cd ~/claude-harness && git describe --tags --always)"
```

Print the count and version to the user. Done.

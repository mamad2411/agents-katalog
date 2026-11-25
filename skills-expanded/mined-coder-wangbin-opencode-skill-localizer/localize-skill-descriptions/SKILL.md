---
name: localize-skill-descriptions
description: |
  记录本地化技能描述的正确工作流 — 使用 git skip-worktree 保护本地修改，
  避免 git pull 覆盖。适用于任何通过 git 安装的 OpenCode/Claude Code 技能。
  触发场景：翻译技能描述、自定义技能元数据、保护本地修改不被覆盖。
---

# Localize Skill Descriptions

## Purpose

Document the correct workflow for localizing skill descriptions (or any skill metadata) while protecting local modifications from being overwritten by `git pull`.

This skill applies to any skills installed via git repositories in AI coding assistants (OpenCode, Claude Code, etc.).

## Problem Context

When you want to customize skill descriptions (e.g., translate to Chinese, add custom tags, modify triggers) for skills installed via a git repository, you face a conflict:
- `git pull` updates will overwrite your local changes
- Creating duplicate files means maintaining two copies
- Using `--assume-unchanged` is dangerous — git may still overwrite those files

## Correct Workflow

### Step 1: Modify files in the git repository

Edit the SKILL.md files directly in the git-tracked directory.

```bash
# Example: Translate description to Chinese
cd ~/.config/opencode/superpowers
for skill in skills/*/SKILL.md; do
  # Edit the description field in YAML frontmatter
  sed -i '' 's/old description/新描述/' "$skill"
done
```

### Step 2: Protect local changes with skip-worktree

```bash
cd ~/.config/opencode/superpowers
git update-index --skip-worktree skills/*/SKILL.md
```

This tells git to ignore local changes to these files during `git pull`, `git checkout`, etc.

### Step 3: Create symlink for skill discovery

If the skill discovery mechanism scans a different directory than the git repo, create a symlink:

```bash
ln -s ~/.config/opencode/superpowers/skills ~/.config/opencode/skills/superpowers
```

This avoids duplicating files — the symlink points to the git repo, which already has your localized descriptions.

## Common Mistakes

### WRONG: Creating duplicate files
```bash
# Don't do this — you now maintain two copies of each file
cp ~/.config/opencode/superpowers/skills/*/SKILL.md ~/.config/opencode/skills/
```

### WRONG: Using assume-unchanged
```bash
# Don't use --assume-unchanged — it's for performance optimization, not local overrides
git update-index --assume-unchanged skills/*/SKILL.md
```

### CORRECT: skip-worktree + symlink
```bash
# Modify in-place, protect with skip-worktree, symlink for discovery
git update-index --skip-worktree skills/*/SKILL.md
ln -s ~/.config/opencode/superpowers/skills ~/.config/opencode/skills/superpowers
```

## Key Differences: skip-worktree vs assume-unchanged

| Flag | Purpose | Safe for local overrides? |
|------|---------|--------------------------|
| `--skip-worktree` | "I modified this locally, don't touch it" | ✅ Yes |
| `--assume-unchanged` | "This file is huge, skip checking it for performance" | ❌ No — git may overwrite it |

## Verification

```bash
# Verify skip-worktree status (S = skip-worktree set)
git ls-files -v skills/*/SKILL.md | grep '^S'

# Verify working tree is clean
git status

# Verify symlink exists
ls -la ~/.config/opencode/skills/superpowers
```

## Rollback

To restore tracking:
```bash
git update-index --no-skip-worktree skills/*/SKILL.md
git checkout -- skills/*/SKILL.md  # restores upstream version
```

## Lessons Learned

1. **Never duplicate files** — always modify in-place and protect with skip-worktree
2. **skip-worktree ≠ assume-unchanged** — they serve different purposes
3. **Symlinks are your friend** — use them for discovery mechanisms instead of copying
4. **Verify before trusting** — always run `git status` and `git ls-files -v` after setup
5. **SKILL.md 必须有 YAML frontmatter** — OpenCode 通过 `---` 块中的 `name` 和 `description` 字段发现和展示技能。没有 frontmatter 的技能不会出现在 `/skill-name` 命令列表中。

### YAML Frontmatter 格式

```yaml
---
name: your-skill-name
description: 简短描述技能用途和触发条件（会被 OpenCode 展示给用户）
---
```

**错误路径**：直接写 `# Skill Title` 开头，没有 frontmatter → 技能不被发现。
**正确路径**：文件必须以 `---` 开头，包含 `name` 和 `description`。

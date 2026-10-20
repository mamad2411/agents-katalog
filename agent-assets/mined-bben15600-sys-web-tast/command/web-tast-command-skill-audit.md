# Skill Audit

## Role
You are a Skill Integrity Inspector. You verify that every file in `exported-skills/` is a
fresh, accurate representation of its source in `.claude/plugins/`.

## Instructions

### Step 1: Discover Exported Skills

Glob `exported-skills/*/SKILL.md`. Extract each skill name (directory between `exported-skills/`
and `/SKILL.md`).

### Step 2: For Each Skill — Check Source and Freshness

For each skill name, run all three checks sequentially:

**1. Locate source:**
```bash
python3 -c "
import glob, sys
matches = glob.glob(f'.claude/plugins/**/skills/{sys.argv[1]}/SKILL.md', recursive=True)
# Priority: claude-skills-std wins over global. Update in both skill-audit and push-skills Step 3.5 if plugin names change.
matches.sort(key=lambda p: (0 if 'claude-skills-std' in p else 1))
print(matches[0] if matches else '')
" "<skill-name>"
```

If empty → status `✗ ORPHANED`. Skip steps 2 and 3.

**2. Compare last-modified commit timestamps** (use `<source-path>` captured from step 1):
```bash
src_ts=$(git log --format="%ct" -1 -- "<source-path>")
exp_ts=$(git log --format="%ct" -1 -- "exported-skills/<skill-name>/SKILL.md")
echo "$src_ts $exp_ts"
```
- `src_ts` empty (source never committed) → status `⚠ STALE`
- `src_ts > exp_ts` → status `⚠ STALE`
- `src_ts <= exp_ts` → status `✓ IN SYNC`

**3. Read portability score from export frontmatter:**

Use the Read tool on `exported-skills/<skill-name>/SKILL.md`. Extract the line matching
`^portability:\s*\d+` from the YAML frontmatter. If absent, score is `none`.

### Step 3: Print Report

```
Skill Audit — <YYYY-MM-DD>

| Skill | Status | Score | Source |
|-------|--------|-------|--------|
| git-commit   | ✓ IN SYNC  | 100/100 | .claude/plugins/claude-skills-std/skills/git-commit/SKILL.md |
| push-skills  | ✓ IN SYNC  |  70/100 | .claude/plugins/claude-skills-std/skills/push-skills/SKILL.md |
| my-skill     | ⚠ STALE    |  85/100 | .claude/plugins/claude-skills-std/skills/my-skill/SKILL.md |
| ghost-skill  | ✗ ORPHANED |  60/100 | (no local source) |

Summary: N ✓ in sync   N ⚠ stale   N ✗ orphaned
```

### Step 4: Remediation Advice

For each `⚠ STALE`: suggest `Run /skill-templatizer <source-path> to refresh.`

For each `✗ ORPHANED`: suggest `Verify this export is intentional (e.g. pushed from another repo). If not needed, delete exported-skills/<name>/SKILL.md.`

## Safety Rules

1. **Read-only** — never modify any file.
2. **Always list orphaned skills** — never silently skip them.
3. **Report scores even for orphans** — read the export frontmatter regardless of source status.

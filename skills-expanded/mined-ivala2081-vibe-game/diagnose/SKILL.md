---
name: diagnose
description: "Vibe-game plugin health check. Verifies install integrity, explains the 0-skills counter quirk, validates cache freshness, lints SKILL.md frontmatter, checks plugin manifest field types, and surfaces marketplace/plugin status. Trigger when the user is confused why a skill isn't showing up, when /reload-plugins reports weird counts, or before reporting a bug."
disable-model-invocation: false
---

# diagnose

> **Self-diagnostic for vibe-game.**
> Knows the Claude Code loader's quirks so the user doesn't have to.

## When to invoke

- User says: "skill not loading" / "why does it say 0 skills" / "is the plugin broken?"
- After `/reload-plugins` shows unexpected counts
- After bumping versions and seeing stale behavior
- Before filing a bug report — gather evidence first

## Hard rules

1. **Cite [[claude-code-internals]] by CC# for every finding.** This is the moat:
   we don't guess, we explain *why*.
2. **Differentiate plugin bugs from user-config issues from Claude Code quirks.**
   Counter-mismatch is a Claude Code quirk, not a vibe-game bug — say so.
3. **Output a structured report** with PASS/WARN/FAIL per check, plus a recommended fix.
4. **Read the cache, not the source.** Source files don't reflect what's actually loaded.

## Procedure

### Step 1 — Locate the plugin cache

Use Bash/Glob to find:
```
~/.claude/plugins/cache/vibe-games/vibe-game/
```

If missing → user hasn't installed the plugin yet. Tell them:
```
/plugin marketplace add ivala2081/vibe-game
/plugin install vibe-game@vibe-games
```

### Step 2 — List installed versions

```bash
ls ~/.claude/plugins/cache/vibe-games/vibe-game/
```

Multiple versions are OK (cache history). The **active** one is the latest
matching the marketplace manifest. Report which one is active.

### Step 3 — Read the active plugin.json

```bash
cat ~/.claude/plugins/cache/vibe-games/vibe-game/<version>/.claude-plugin/plugin.json
```

Check fields against [[claude-code-internals#cc9]]:
- ✓ `name`: kebab-case
- ✓ `version`: semver
- ✓ `description`: non-empty
- ✓ `author`: object (not string)
- ⚠ If `skills`, `agents`, `commands`, `hooks` fields exist: validate types per CC9
  - `agents` must be FILE paths (`.md`), not directory
  - `skills` must be DIRECTORY paths

### Step 4 — Count skills in the cache

```bash
ls ~/.claude/plugins/cache/vibe-games/vibe-game/<version>/skills/
```

Expected for v0.5.0: 11 directories (`vibe-start`, `prototype`, `juice`,
`feel-check`, `cut`, `grab-asset`, `ship`, `jam-mode`, `devlog`, `death-watch`,
`diagnose`).

For each, verify `SKILL.md` exists:
```bash
ls ~/.claude/plugins/cache/vibe-games/vibe-game/<version>/skills/*/SKILL.md
```

### Step 5 — Compare to /reload-plugins counter

If user reports "0 skills" but step 4 shows N skills present:

> ✓ Skills are loaded correctly. The "0 skills" message is a Claude Code display
> bug (see [CC1](../../taste/claude-code-internals.md#cc1)) — it reports
> `command_count` mislabeled as "skill". Your plugin's actual SKILL.md files are
> loaded via a separate code path and not surfaced in that counter.
>
> **Verification:** run `/vibe-game:vibe-start` — if it executes, skills are
> definitely loaded.

### Step 6 — Cache freshness check

```bash
# Compare source plugin.json version to cached plugin.json version
diff <(jq .version ~/.claude/plugins/cache/vibe-games/vibe-game/<latest>/.claude-plugin/plugin.json) \
     <(jq .version <PROJECT>/vibe-game/.claude-plugin/plugin.json)
```

If mismatched: tell user to `/plugin marketplace update vibe-games` and possibly
`/plugin uninstall + /plugin install` to force fresh cache.

Cite [[claude-code-internals#cc2]] — cache is keyed by version; unchanged version means
stale cache.

### Step 7 — SKILL.md frontmatter lint

For each `skills/*/SKILL.md`, check:
- ✓ Has `description:` field
- ⚠ Description quoted (recommended) — avoids YAML parse issues with parens/em-dashes
- ✓ `name:` matches directory name (avoids confusion per [[claude-code-internals#cc3]])
- ⚠ If `disable-model-invocation` set: verify intent per [[claude-code-internals#cc4]]
- ⚠ If `paths:` set: verify pattern syntax per [[claude-code-internals#cc5]]

### Step 8 — Hook validation

```bash
cat ~/.claude/plugins/cache/vibe-games/vibe-game/<latest>/hooks/hooks.json | jq .
```

- ✓ Top-level `"hooks"` key (not a bare event map)
- ✓ Each event is one of the 20+ HOOK_EVENTS (see [[claude-code-internals#cc6]])
- ✓ Each hook has `type` ∈ {`command`, `prompt`, `agent`, `http`}
  ([[claude-code-internals#cc7]])

### Step 9 — Output the report

```
VIBE-GAME DIAGNOSTIC REPORT
───────────────────────────
Plugin install:    ✓ found at ~/.claude/plugins/cache/vibe-games/vibe-game/0.5.0
Cache versions:    [0.2.0, 0.2.1, 0.2.2, 0.2.3, 0.3.0, 0.4.0, 0.5.0]  (active: 0.5.0)
Source version:    0.5.0  ✓ matches cache
plugin.json valid: ✓ all required fields present, types correct
Skills present:    11/11  ✓ all expected SKILL.md files in place
Hook config:       ✓ 2 hooks (PostToolUse), well-formed
Agents present:    4 (game-feel-engineer, critical-playtester, scope-killer, vibe-director)

Reload counter:    "0 skills" — EXPECTED MISBEHAVIOR ([CC1])
                   This is a Claude Code display bug. Your skills are loaded.

Recent /reload-plugins output:
  Reloaded: 3 plugins · 0 skills · 10 agents · 2 hooks · 2 MCP · 0 LSP

Verification:
  Run /vibe-game:vibe-start to confirm — if it executes, the plugin is healthy.

Errors detected:   0
Warnings:          0

VERDICT: HEALTHY ✓
```

If anything is FAIL, list it explicitly with the fix and the CC# citation.

## Example issues and how to phrase them

### Issue: stale cache after edit

```
⚠ Cache stale: source plugin.json version is 0.6.0 but cache shows 0.5.0.

This means you edited source but the cache still holds the previous version.

Fix: run /plugin marketplace update vibe-games. If that doesn't refresh,
     bump the version in plugin.json (e.g., 0.5.0 → 0.5.1) and retry.

Source: [[claude-code-internals#cc2]] — Claude Code keys cache by version.
        Same version = cache reused.
```

### Issue: agents field as directory

```
✗ FAIL: plugin.json has "agents": "./agents" (directory path).

The agents field requires .md FILE paths, not a directory. The schema validator
rejects directories.

Fix: remove the line entirely (auto-discovery works for agents/), or use:
     "agents": ["./agents/foo.md", "./agents/bar.md"]

Source: [[claude-code-internals#cc9]] — manifest field types.
```

### Issue: skill not invocable via slash command

```
⚠ User reports "/vibe-game:my-skill command not found" but skills/my-skill/SKILL.md exists.

Likely causes:
1. /reload-plugins not run after install — try it now.
2. SKILL.md frontmatter has YAML parse error (e.g., unquoted em-dash in description).
   Try quoting: description: "..."
3. Plugin not enabled — check /plugin and re-enable.

Source: [[claude-code-internals#cc3]] — skill name = directory name. Confirm.
```

## Anti-patterns

- ❌ Telling user "0 skills" is a real problem (it's a Claude Code bug)
- ❌ Diagnosing from source files (read the cache)
- ❌ Recommending workarounds that don't address root cause
- ❌ Skipping the version-comparison step (stale cache is the #1 issue)

## Cross-references

- Reads from: [[claude-code-internals]] (primary), plugin cache filesystem
- Bash/Glob/Read tools to inspect cache and source
- Other skills called: none (this is a leaf diagnostic)

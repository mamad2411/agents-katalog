---
name: pai-upgrade
description: |
  Meta-skill for upgrading your Ogmios fork against future PAI versions
  (Daniel Miessler upstream). Structured process: clone PAI repo → diff against
  your config → classify ISCs (Isolated Strategic Changes) → build PRD → execute
  in phases → audit-preserve.

  [WHAT] Process skill that documents how to upgrade your Ogmios fork against
  upstream PAI releases without losing your customisations.

  [WHEN] Use when: PAI upgrade, miessler new release, upgrade fork from upstream,
  "new PAI version released". NOT for: feature requests on your own fork.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch, mcp__github__get_file_contents
---

# PAI Upgrade

**Role:** structured process for upgrading an Ogmios fork against an upstream PAI release.

## Why this exists

Ogmios is a port of Daniel Miessler's PAI architecture. When PAI releases a new major version, you want to:
1. Pick up the new patterns/skills/hooks that match your needs
2. Keep your own customisations intact
3. Avoid losing track of which parts came from where

This skill documents the process so future upgrades follow the same method.

## Phases

### Phase 0: assess

1. Read PAI release notes (GitHub: `danielmiessler/PAI` → releases)
2. Identify the version delta (e.g. PAI 6.0 → 7.0)
3. Decide scope: minor patch, selective adoption, or full re-port

### Phase 1: clone upstream

```bash
git clone https://github.com/danielmiessler/PAI.git ~/projekt/pai-upstream-vX.Y
cd ~/projekt/pai-upstream-vX.Y
git checkout vX.Y.0  # or main if no tag
```

### Phase 2: diff against your config

Generate diff per major area:

```bash
# System layer
diff -r ~/projekt/pai-upstream/Algorithm.md ~/.claude/system/Algorithm.md

# Skills (per skill)
for s in ~/projekt/pai-upstream/skills/*/; do
  diff -r "$s" "~/.claude/skills/$(basename $s)" 2>/dev/null
done

# Hooks
diff -r ~/projekt/pai-upstream/hooks/ ~/.claude/hooks/
```

Save diffs to a working directory: `~/projekt/pai-upgrade-{date}/diffs/`

### Phase 3: classify ISCs

Each diff is classified as one of:

| Class | Treatment |
|-------|-----------|
| **ADOPT** | Take upstream verbatim — clear improvement |
| **ADOPT-WITH-MERGE** | Take upstream behaviour, preserve user customisation |
| **REJECT** | Upstream change conflicts with your config — keep yours |
| **CUSTOM-ONLY** | Your-only — no upstream change to apply |
| **NEW-FROM-UPSTREAM** | Brand-new feature in upstream — adopt as-is |

Document each classification with reasoning.

### Phase 4: build PRD

Create a PRD in `~/.claude/memory/WORK/{slug}/PRD.md` with:
- Frontmatter (task, slug, effort: comprehensive, phase: observe)
- Context: which PAI version → which target version
- Criteria: per-ISC binary criterion (e.g. "Algorithm.md adopts new Phase 4 capability audit")
- Decisions: per-ISC classification with reasoning

Use the Algorithm 7-phase protocol for execution.

### Phase 5: execute in phases

Per ISC class:

**ADOPT:**
- Copy upstream file over yours
- Test
- Commit

**ADOPT-WITH-MERGE:**
- Read both versions
- Identify your customisation lines
- Apply upstream structure with customisation preserved
- Document the merge in commit message
- Test
- Commit

**REJECT:**
- Document why in `~/.claude/memory/learnings/pai-upgrade-{version}.md`
- No code change

**CUSTOM-ONLY:**
- Verify still works with upstream changes
- Document if it conflicts

**NEW-FROM-UPSTREAM:**
- Copy upstream file
- Adapt frontmatter to your conventions if needed
- Test
- Commit

### Phase 6: audit-preserve

After all ISCs are processed:

1. Run smoketest: spawn a session, exercise key skills, confirm no regression
2. Update `~/.claude/memory/SYSTEM/ARCHITECTURE.md` with version bump and changes
3. Write upgrade summary to `~/.claude/memory/learnings/pai-upgrade-{version}.md`
4. Commit final state

## Documentation conventions

For each upgrade, produce:
- `pai-upgrade-{version}-classification.csv` — one row per ISC
- `pai-upgrade-{version}.md` — summary report (what was adopted, why, what was rejected)
- Updated `SYSTEM/ARCHITECTURE.md` version field

## Anti-patterns

- Upgrading without a PRD (lose track of state across long process)
- Bulk-adopting without classification (lose customisations)
- Skipping smoketest (silent regressions)
- Not documenting REJECT decisions (later you forget why)

## Reference

- Daniel Miessler's PAI: https://github.com/danielmiessler/PAI
- Ogmios upgrade history: see `~/.claude/memory/learnings/pai-upgrade-*.md`

---

🎯 COMPLETED: [SKILL:pai-upgrade] [PAI upgrade vX.Y.Z executed]
🗣️ CUSTOM COMPLETED: [SKILL:pai-upgrade] [Upgrade complete]

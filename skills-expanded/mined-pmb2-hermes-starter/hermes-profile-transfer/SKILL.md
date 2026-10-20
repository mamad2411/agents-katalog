---
name: hermes-profile-transfer
category: devops
description: Transfer skills, memories, and config between Hermes profiles — bootstrapping team leads (chief-of-staff, council) with full knowledge from the primary agent.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
last_updated: 2026-06-06
metadata:
  hermes:
    tags: [hermes, profiles, skills, memory, transfer, sync, bootstrap]
    triggers: [profile-transfer, skill-migration, memory-transfer, config-bootstrap, hermes-setup, agent-onboarding, team-lead-setup]
    related_skills: [memory-migration-mem0-to-mempalace, github]
---

# Hermes Profile — Skill & Memory Transfer

Transfer all skills, memories, and configuration from one Hermes profile (e.g., default) to another (e.g., a team lead) so the receiving agent has the same knowledge and capabilities as the source.

## When To Use

- A team lead (e.g., chief-of-staff) needs all the skills and project memory you have
- You're bootstrapping a new profile and want to duplicate an existing one's knowledge
- A specialist agent needs access to skills across domains it doesn't normally handle

## Prerequisites

- Both source and target profiles exist in `~/AppData/Local/hermes/profiles/<name>/`
- You know the target profile's name
- You have write access to both profiles' directories

## Step-by-Step

### 1. Inventory Both Profiles

```bash
# Count source skills
find ~/AppData/Local/hermes/skills/ -name 'SKILL.md' | wc -l

# Count target skills
find ~/AppData/Local/hermes/profiles/<target>/skills/ -name 'SKILL.md' | wc -l

# Check target memories
ls ~/AppData/Local/hermes/profiles/<target>/memories/

# Check source memories
ls ~/AppData/Local/hermes/memories/
```

### 2. Transfer Skills

Copy all SKILL.md and support files (references/, templates/, scripts/) from the default profile to the target. Preserve any unique files the target profile has at its skills root (flat `.md` files):

```bash
cd ~/AppData/Local/hermes/skills && \
find . -type f -not -path './.archive/*' \
  -not -name '.bundled_manifest' \
  -not -name '.curator_*' \
  -not -name '.usage.json*' | \
while IFS= read -r f; do
  dest=~/AppData/Local/hermes/profiles/<target>/skills/"$f"
  mkdir -p "$(dirname "$dest")"
  cp "$f" "$dest"
done
```

**Why exclude `.archive/`:** Archived skills are deliberately deprecated — transferring them noise the target. The target only needs active skills.

### 3. Transfer Memories

```bash
cp ~/AppData/Local/hermes/memories/MEMORY.md \
   ~/AppData/Local/hermes/profiles/<target>/memories/
cp ~/AppData/Local/hermes/memories/USER.md \
   ~/AppData/Local/hermes/profiles/<target>/memories/
```

### 4. Update Target's AGENTS.md

Add a "Skill Inheritance" section listing what was transferred, and a "Knowledge Sources" section documenting MEMORY.md, USER.md, and MemPalace. This tells the receiving agent what it has access to and where to find things.

Key sections to add:
```
## Skill Inheritance
This profile has inherited ALL N skills and full memory from the primary Hermes agent.
[Domain → Skills table]

## Knowledge Sources
1. MEMORY.md — ...
2. USER.md — ...
3. MemPalace — N drawers across M wings
4. Skills/ — N SKILL.md files across C categories
```

### 5. Update Target's config.yaml

Ensure the target profile uses the right model chain (matching the operator's preferences):

```yaml
model:
  default: deepseek-v4-flash
  provider: opencode-go
fallback_model:
  provider: openrouter
  model: google/gemma-4-31b-it:free
```

Also verify the target has `memory.provider: mempalace` and the same MCP servers configured.

### 6. Verify

```bash
find ~/AppData/Local/hermes/profiles/<target>/skills/ -name 'SKILL.md' | wc -l
cat ~/AppData/Local/hermes/profiles/<target>/memories/MEMORY.md | wc -l
cat ~/AppData/Local/hermes/profiles/<target>/memories/USER.md | wc -l
grep '^## Skill Inheritance' ~/AppData/Local/hermes/profiles/<target>/AGENTS.md
```

### 7. Restart Target's Gateway

The running gateway loaded its config at startup — config.yaml, AGENTS.md, and memories won't take effect until restart:

1. Kill the old process: `kill $(cat ~/AppData/Local/hermes/profiles/<target>/gateway.pid)`
2. Start the gateway via the profile's spacebar-gateway.py or hermes gateway command

## Pitfalls

- **Cross-profile guard**: The `write_file` and `patch` tools have a `cross_profile` parameter (default false) that blocks writes to another profile's directory. Set `cross_profile=true` when editing another profile's skills/plugins/cron/memories. If you hit a warning, that's the guard — it's intentional.
- **Module caching**: Node.js caches modules. Server-side patches to `.js` files don't take effect until the process is restarted. Client-side changes need a browser hard-refresh (Ctrl+Shift+R).
- **`.archive/` directory**: Don't copy archived skills. They're deprecated.
- **Gateway state**: The `gateway_state.json` may report "running" but the config is stale. Always restart.
- **Model mismatch**: If the target was using a different model/provider (e.g., openrouter/deepseek-chat), the responses will differ until config is updated.
- **Skills list in config.yaml**: The `skills:` list in config controls which skills are pre-loaded on every turn. Add only role-specific tools here (e.g., morning-briefing, decision-logger) — all other skills are available on-demand via `skill_view()`. Don't dump 171 skills into the startup list.
- **MemPalace is shared**: MemPalace is a shared database across all profiles. The target already has access to all wings — no data transfer needed. The AGENTS.md "Knowledge Sources" section is enough to make it discoverable.

## References

See `references/full-transfer-example.md` for a complete end-to-end transcript of a default→chief-of-staff transfer.

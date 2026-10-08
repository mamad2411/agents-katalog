---
name: open-claw-skill-hunter-and-developer
description: >
  Hunts, analyzes, transforms, and bundles OpenClaw skills from the ClawHub registry
  (52k+ skills) into Manus-compatible skill batches. Use when the user wants to find,
  convert, develop, or install OpenClaw/ClawHub skills for use in Manus.
---

# Open Claw Skill Hunter and Developer

A complete pipeline to discover, evaluate, and automatically convert OpenClaw skills into native Manus skills. Built by SimplioLabs.

OpenClaw's ClawHub registry contains over 52,700 skills. While designed for Claude, their `SKILL.md` format is highly compatible with Manus. This skill automates the process of finding the right tools and adapting them for the Manus sandbox environment.

## The Pipeline

This skill provides four tools that work together as a pipeline:

### 1. Hunt (Search & Discovery)

Use `fetch_claw_skills.py` to search the ClawHub registry or browse popular skills.

```bash
# Semantic vector search (finds concepts, not just keywords)
python3 /home/ubuntu/skills/claw-skill-hunter/scripts/fetch_claw_skills.py --search "API testing"

# Get detailed stats (stars, downloads, versions) for a specific skill
python3 /home/ubuntu/skills/claw-skill-hunter/scripts/fetch_claw_skills.py --detail api-tester

# Read the full original SKILL.md before converting
python3 /home/ubuntu/skills/claw-skill-hunter/scripts/fetch_claw_skills.py --deep-dive api-tester
```

### 2. Analyze (Compatibility Check)

Before converting a skill, analyze it to see if it relies on incompatible platform features (like macOS-only commands or Claude Desktop specifics).

```bash
# Generate a compatibility report
python3 /home/ubuntu/skills/claw-skill-hunter/scripts/analyze_skill.py <slug>
```

**Readiness Levels:**
- READY (80-100): Converts cleanly.
- ADAPTABLE (50-79): Converts, but may need manual tweaks.
- PARTIAL (25-49): Significant rework needed; core logic reusable.
- INCOMPATIBLE (0-24): Heavy platform dependencies (e.g., AppleScript).

### 3. Develop (Transformation & Conversion)

Convert a ClawHub skill into a fully structured Manus skill directory.

```bash
# Preview what changes will be made
python3 /home/ubuntu/skills/claw-skill-hunter/scripts/transform_skill.py <slug> --review

# Convert and save to /home/ubuntu/skills/<slug>
python3 /home/ubuntu/skills/claw-skill-hunter/scripts/transform_skill.py <slug>
```

**What it does:**
- Rewrites `~/.claude/` paths to `/home/ubuntu/skills/`
- Converts macOS `brew` commands to Ubuntu `apt-get`
- Removes Claude Desktop specific references
- Normalizes YAML frontmatter
- Generates a `references/provenance.json` tracking the origin

### 4. Bundle (Thematic Batch Creation)

The most powerful tool: search for a theme, analyze all results, transform the compatible ones, and package them into an installable batch.

```bash
# Build a batch of the top 5 compatible web scraping skills
python3 /home/ubuntu/skills/claw-skill-hunter/scripts/batch_builder.py --theme "web scraping" --max 5

# Build a batch from specific known slugs
python3 /home/ubuntu/skills/claw-skill-hunter/scripts/batch_builder.py --slugs "memory-system,self-improving-agent"
```

Batches are saved to `/home/ubuntu/skill-batches/` and include an `install.sh` script and a summary `README.md`.

## Best Practices for the Agent

1. **Always Hunt First**: When a user asks for a capability (e.g., "I need a memory system"), run a `--search` first to see what exists before writing custom code.
2. **Batch by Theme**: If the user needs a suite of tools (e.g., "set up a QA environment"), use `batch_builder.py --theme "QA testing"` to provide multiple options.
3. **Review Adaptable Skills**: If a skill scores below 80, read the transformed `SKILL.md` and manually fix any remaining platform-specific instructions before presenting it to the user.
4. **Offline Fallback**: If the ClawHub API is down or rate-limited, use `fetch_claw_skills.py --list` to rely on the pre-built `popular_skills_cache.json`.

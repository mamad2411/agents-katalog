---
name: system-awareness
description: Manages all other skills by detecting capability gaps, proposing new skills, and keeping the system registry in sync. Use when the user encounters something the system cannot do, wants to log a capability gap, review the skill backlog, propose or build a new skill, analyze recurring unmet needs, or run sync pipelines to update context files (CLAUDE.md, GEMINI.md, AGENTS.md) after skill changes.
---

# System Awareness - The Self-Evolving Skill Manager

> **Meta-Skill**: This skill manages all other skills. It observes gaps, proposes new capabilities, and helps the system evolve.

---

## Quick Start

### 1. Log a Gap

```bash
python scripts/gap_logger.py "I need to analyze ECG waveforms from images"

python scripts/gap_logger.py \
  --request "Analyze ECG images for abnormalities" \
  --context "User uploaded 12-lead ECG, wanted automated interpretation" \
  --category "medical-imaging" \
  --urgency "high"
```

### 2. Analyze Gaps

```bash
python scripts/gap_analyzer.py --list      # List all gaps
python scripts/gap_analyzer.py --analyze   # Analyze patterns
python scripts/gap_analyzer.py --report    # Generate priority report
```

### 3. Build a Skill

```bash
# Propose from a logged gap
python scripts/skill_proposer.py --gap-id "gap_2024_001"

# Build from a proposal (one command does everything)
python scripts/skill_builder.py --proposal ecg-analyzer-proposal.md

# Or build directly from a gap (fast path)
python scripts/skill_builder.py --from-gap gap_xxxx

# Or build directly with name and purpose
python scripts/skill_builder.py --name "ecg-analyzer" --purpose "Analyze ECG images"
```

---

## Gap → Skill Pipeline

```
1. GAP DETECTED
   └─► gap_logger.py → gap-log.json

2. GAPS ANALYZED
   └─► gap_analyzer.py → patterns, priorities

3. SKILL PROPOSED
   └─► skill_proposer.py → skill-templates/*.md

4. HUMAN REVIEW
   └─► Approve / reject / modify proposal

5. SKILL BUILT ★
   └─► skill_builder.py → skills/[category]/[name]/
       ├── Creates SKILL.md
       ├── Creates scripts/ & references/
       ├── Marks gap as resolved
       └── Archives proposal

6. SYSTEM SYNCED (auto-runs)
   └─► sync_skills.py → capability-registry.json

7. CONTEXT UPDATED (auto-runs)
   └─► generate_context.py → CLAUDE.md, GEMINI.md, AGENTS.md

8. SKILL AVAILABLE ✓
   └─► Ready to use in next conversation
```

### Approval Checklist (Step 4)

Before approving a new skill:

- [ ] **Frequency**: Is this needed often enough?
- [ ] **Impact**: Does it unblock important workflows?
- [ ] **Feasibility**: Can we actually build this?
- [ ] **Overlap**: Does an existing skill already do this?
- [ ] **Maintenance**: Can we keep this updated?

### Validation & Error Recovery

After each major step, verify before proceeding:

| Step | Verify | If it fails |
|------|--------|-------------|
| `sync_skills.py --update` | Check registry entry count increased | Re-run with `--dry-run` to inspect conflicts; resolve duplicate IDs manually |
| `generate_context.py --update` | Confirm AUTO-GENERATED markers are present in target files | Ensure markers exist: `<!-- AUTO-GENERATED SKILLS START -->` … `<!-- AUTO-GENERATED SKILLS END -->` |
| `skill_builder.py` | Validate new SKILL.md parses correctly | Check frontmatter for required `name`/`description` fields; re-run builder |
| Registry integrity | Run `python scripts/registry_updater.py --stats` | If count anomaly, diff against previous backup in `data/backups/` |

---

## Sync Architecture

Context files are rebuilt from a single source of truth:

```
skills/cardiology/*   skills/scientific/*  ...
        └──────────────────┬───────────────┘
                           ▼
                   sync_skills.py
                           ▼
             capability-registry.json
                           ▼
               generate_context.py
                           ▼
        CLAUDE.md   GEMINI.md   AGENTS.md   SKILL-CATALOG.md
```

### Sync Commands

```bash
# Discover new skills
python scripts/sync_skills.py              # Report only (dry run)
python scripts/sync_skills.py --update     # Add to registry

# Regenerate context files
python scripts/generate_context.py --preview   # Preview changes
python scripts/generate_context.py --update    # Apply to all context files

# Full pipeline (run after adding any new skill)
python scripts/sync_skills.py --update && python scripts/generate_context.py --update
```

Context files must contain these markers for auto-update:

```markdown
<!-- AUTO-GENERATED SKILLS START -->
... skills content here ...
<!-- AUTO-GENERATED SKILLS END -->
```

### When to Run

- **After adding a new skill**: Run full pipeline
- **Weekly maintenance**: `sync_skills.py` to check for drift
- **Before major sessions**: Ensure registry is current

---

## Gap Detection (For Claude)

Log a gap whenever you encounter an inability, a missing capability, a pointer to an external tool, or repeated user frustration with the same task. When logging, note it in the response:

```
📋 **Gap Logged**: [brief description]
Category: [category] | Urgency: [low/medium/high]

Review gaps with: `python scripts/gap_analyzer.py --list`
```

For full JSON schema, proposal template format, and gap pattern examples, see:
- `references/json-schemas.md` — gap-log.json, capability-registry.json, skill-backlog.json schemas
- `references/proposal-template.md` — new skill proposal format
- `references/gap-patterns.md` — common gap pattern recognition
- `references/skill-anatomy.md` — what makes a good skill

---

## Commands Reference

```bash
# Gap Management
python scripts/gap_logger.py "description"        # Log a new gap
python scripts/gap_analyzer.py --list             # List all gaps
python scripts/gap_analyzer.py --analyze          # Analyze patterns
python scripts/gap_analyzer.py --report           # Generate priority report

# Skill Proposals & Building
python scripts/skill_proposer.py --gap-id "id"    # Propose from gap
python scripts/skill_proposer.py --interactive    # Interactive proposal builder
python scripts/skill_builder.py --list-proposals  # See pending proposals
python scripts/skill_builder.py --list-gaps       # See open gaps
python scripts/skill_builder.py --proposal FILE   # Build from proposal
python scripts/skill_builder.py --from-gap ID     # Build from gap (fast path)
python scripts/skill_builder.py --name X --purpose Y  # Build directly
python scripts/skill_builder.py --no-sync         # Skip auto-sync

# Registry
python scripts/registry_updater.py --scan         # Scan for new skills
python scripts/registry_updater.py --stats        # Show usage statistics
python scripts/registry_updater.py --unused       # Find unused skills
```

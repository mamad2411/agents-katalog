---
name: "workflow-distiller"
description: "Distills completed session transcripts and chat logs into reusable agent skills while auditing active/candidate inventories to prevent tool redundancy."
last_updated: "2026-05-20"
id: "UFTM-SKILL-001"
---

# Skill: Workflow Distiller

The `workflow-distiller` skill analyzes terminal session logs, transcripts, or command histories to package repeated manual steps into reusable agent skills (`SKILL.md` + CLI script templates). During parsing, it audits the active tools inventory and candidate registers to alert the operator if existing libraries or SaaS tools cover the required steps, preventing system bloat.

---

## 🚀 Quickstart

Run this skill from the vault directory:
```bash
python Skills/workflow-distiller/scripts/workflow_distiller.py [command] [args]
```

---

## 📖 Operational Instructions

1.  **Analyze Transcript:** Read the target `.md` log file containing the sequence of steps.
2.  **Verify Overlaps:** Run the distiller against the logs. It programmatically scans `tools-and-applications-inventory.md` and `candidate-tools-register.md`.
3.  **Generate Skill Scaffolding:** Writes a clean `SKILL.md` and CLI template inside `Skills/{skill-name}/`.
4.  **Validate & Deploy:** Run validation tests, and then copy/symlink the skill folder into `.gemini/antigravity/skills/` to load it natively.

---

## 🛠️ Commands & Subcommands

### 1. `distill`
Distills a session transcript to `SKILL.md` and scaffolding python scripts, performing inventory overlap check.
*   **Arguments:**
    *   `--input-log` (Path, Required): Session transcript log path.
    *   `--skill-name` (String, Required): Target skill name (lowercase, kebab-case).
    *   `--desc` (String, Required): Clear description of the skill.

### 2. `validate`
Verifies the generated skill configuration files.
*   **Arguments:**
    *   `--skill-dir` (Path, Required): Generated skill directory.

### 3. `deploy`
Safely copies or symlinks the local skill to the global `.gemini` folder.
*   **Arguments:**
    *   `--skill-dir` (Path, Required): Generated skill directory.

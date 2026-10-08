# Skill: Knowledge Distiller

## Description
This skill acts as a synchronization engine, allowing the "Master" Agent to ingest improvements, new skills, and learned memories from a "Deployed" (or Child) Agent instance. It ensures that lessons learned in the field are permanently recorded in the central repository.

## Usage
Run via Python:
`python skills/devops/knowledge-distiller/distill.py --source <path_to_child_repo> --master <path_to_master_repo>`

## Capabilities
1.  **Artifact Sync**: Recursively compares `agents/` and `skills/` directories.
    *   Detects **NEW** items (in Child, not in Master).
    *   Detects **UPDATED** items (newer timestamp + different hash in Child).
2.  **Memory Merging**: Parses `.gemini/GEMINI.md`.
    *   Extracts bullet points under `## Gemini Added Memories`.
    *   Appends only *new* facts to the Master's memory file.
3.  **Safety**: Defaults to `--dry-run` to prevent accidental overwrites.

## Dependencies
- Python 3.10+

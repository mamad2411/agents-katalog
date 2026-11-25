---
name: technical-readiness
description: Use at the start of a copied landscape project folder or before working with photos, PDFs, video, audio, OCR, compression, presentations, web research, or pricing. The agent should infer technical options from accessible files and environment, ask the designer mainly about desired outcomes and permission to inspect files, and avoid scripts or mandatory commands.
---

# Technical Readiness

## Goal

Help the agent understand project technical context without scripts, mandatory commands, or shifting diagnosis to the designer.

## When To Use

- A new designer starts working with a copied template.
- The task involves photos, video, PDF, audio, presentation, or prices.
- The user asks how to process files.
- The agent is about to suggest file processing and must first check whether it is realistic.

## Process

1. Read `TECHNICAL_READINESS.md`.
2. Identify file types and desired output.
3. Inspect accessible project files if access already exists.
4. If more access is needed, ask plainly: "May I inspect this folder/file and tell you what can be done?"
5. Do not ask the designer for utility names or technical package names if you can avoid it.
6. Ask only what affects the next step: desired output, result use, whether an export/screenshot/link can be provided.
7. Suggest work approaches: agent inspection, system app, familiar editor, external service, local tool, manual workaround.
8. Record the chosen approach or limitation in `99_project_logs/WORK_LOG.md`.

## Rules

- Do not create scripts/tools automation inside the template.
- Do not treat Linux/WSL as the user's default environment.
- Do not promise OCR, compression, transcription, or conversion until an approach is agreed.
- Do not ask the designer to do technical diagnosis that the agent can infer.
- If work can continue without processing the file, continue and mark the gap.

## Output

- Short conclusion: what can be done now.
- Files/exports needed from the designer.
- Suitable work approaches.
- Recorded limitations.

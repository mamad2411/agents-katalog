---
name: image-attachment-ingestion
description: Use when storing, routing, naming, and documenting image attachments for schedules, domain history, reports, reviews, incidents, or task evidence.
---

# Image Attachment Ingestion

## Purpose

Store and document image attachments used for schedules, domain history, task evidence, reports, reviews, or incidents.

## Required Knowledge

- `AGENTS.md` §0.15 Image Attachment Handling
- `ai-workspace/70-knowledge/domains/workspace-operations/image-attachment-routing.md`
- `ai-workspace/41-personal-schedule/README.md`
- `ai-workspace/70-knowledge/README.md`
- `ai-workspace/50-artifacts/README.md`

## Inputs

- One or more image attachments.
- Human-provided context when available:
  - personal schedule, company/project history, artifact evidence, incident, or task evidence
  - project/company/date/topic
  - privacy level: `local`, `internal`, or `public`
  - optional image order descriptions

## Workflow

1. Identify the owning context.
   - Personal schedule: `41-personal-schedule/`
   - Company/project knowledge: `70-knowledge/domains/{company}/projects/{project}/`
   - Artifact evidence: `50-artifacts/{type}/{topic}/`
   - Incident evidence: relevant incident or linked project knowledge path

2. Decide privacy.
   - Default personal or unclear privacy to `local`.
   - Do not store sensitive personal images outside `41-personal-schedule/local/attachments/` without explicit human approval.

3. Choose the target folder.
   - Use `attachments/YYYY-MM/` for schedule and knowledge contexts.
   - Use `attachments/` under the owning artifact folder.

4. Generate filenames.
   - Format: `YYYY-MM-DD-{context-slug}-{sequence}.{ext}`
   - Preserve the original image order.
   - Use two-digit sequence numbers.

5. Store the files.
   - Keep original file extensions unless conversion is explicitly needed.
   - Avoid duplicates when a byte-identical or clearly identical file already exists.

6. Update the owning markdown file.
   - Add relative links under an `Attachments` section.
   - Record source, date, privacy, related context, and a one-sentence summary.

7. Update task state when the attachment is part of executable or verifiable work.
   - Reference this skill as `[Using Skill: image-attachment-ingestion]`.

## Output

- Stored image files in the correct `attachments/` folder.
- Markdown references with metadata.
- Optional task/checklist update.

## Safety Rules

- Do not embed base64 image data in markdown.
- Do not require the human to manually name multiple images.
- Do not copy local-only personal images into shared knowledge, artifacts, logs, or reports without explicit approval.
- If company/project ownership is unclear, ask before storing under `70-knowledge/domains/`.

## Verification

- Target folder matches the owning context and privacy level.
- Filenames follow `YYYY-MM-DD-{context-slug}-{sequence}.{ext}`.
- Image order is preserved.
- Markdown links are relative and point to existing files.
- Each image has source, date, privacy, related context, and summary metadata.

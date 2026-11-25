---
name: openclaw-expert-avatar-batch
description: Batch workflow for OpenClaw/Myopenclaw2026 expert avatars. Use when the user asks to batch generate, continue generating, fill missing, replace, compress, or wire image2/cartoon avatars for Workbuddy/OpenClaw technical experts from docs/workbuddy-agent-prompts.md into public/expert-avatars/image2.
x-alice-class: assist
---# OpenClaw Expert Avatar Batch

## Workflow

1. Work from the project root, normally `C:\Users\Administrator\Documents\极序超级AI\Myopenclaw2026`.
2. Inspect progress first:
   ```powershell
   node C:\Users\Administrator\.codex\skills\openclaw-expert-avatar-batch\scripts\expert_avatar_batch.mjs stats --project .
   node C:\Users\Administrator\.codex\skills\openclaw-expert-avatar-batch\scripts\expert_avatar_batch.mjs plan --project . --limit 4 --out tmp\expert-avatar-batch\next.json
   ```
3. Read `references/avatar-rules.md` before prompting image generation.
4. Generate avatars in small parallel rounds, normally 4 distinct experts at a time. Use built-in `image_gen`; one image call per expert, not a collage.
5. Save generated outputs with:
   ```powershell
   node C:\Users\Administrator\.codex\skills\openclaw-expert-avatar-batch\scripts\expert_avatar_batch.mjs save --project . --map tmp\expert-avatar-batch\generated-map.json
   ```
6. Verify count and file sizes:
   ```powershell
   node C:\Users\Administrator\.codex\skills\openclaw-expert-avatar-batch\scripts\expert_avatar_batch.mjs stats --project .
   ```
7. Commit only `public/expert-avatars/image2/*.webp` unless code was intentionally changed.

## Rules

- Use `image2` cartoon avatar style, not realistic photo style.
- Keep each avatar as a separate square asset; never generate a grid/collage that needs manual slicing.
- Keep output small: save as `256x256` WebP, quality around `72`.
- Preserve current filenames: each expert ID maps to `/expert-avatars/image2/<id>.webp`.
- If an existing generated file is acceptable, do not regenerate it unless the user asks.
- For speed, run batches of 4. More than 4 tends to be hard to inspect and may waste bad generations.

## Script notes

The helper script parses `docs/workbuddy-agent-prompts.md`, detects missing avatars, produces per-expert prompts, and converts generated PNG/JPEG files to project WebP assets. It expects Node.js and the project dependency `sharp` to be available from the project root.

---
name: crash-and-binary-guard
description: Prevents permanent AI agent conversation crashes (HTTP 400 INVALID_ARGUMENT and 30MB payload overflow) caused by password-protected PDFs, 0-byte media, fake HTML-disguised images, and keeps Claude Code sessions synced across Desktop and IDE windows.
---

# Agent Crash Guard & Cross-IDE Session Sync
> Created by **HM Shihabuddin Jashory (Shihab)** — [Vision Flow](https://visionflowgroup.com)

## Core Protection Rules
1. **Never Read Encrypted PDFs Directly**: Never call `read_file` / `Read` on untrusted or password-protected `.pdf` files. Always verify `doc.is_encrypted` with Python (`pymupdf`) in the terminal first.
2. **Verify Downloaded Media Headers**: Before calling `read_file` / `Read` on downloaded `.png`, `.jpg`, `.webp`, or `.pdf` files, ensure they are non-empty (`>0 bytes`) and not HTML error pages (`<!DOCTYPE html>`).
3. **30MB Trajectory Overflow Guard**: Do not read raw images larger than `450 KB` repeatedly into the conversation context; compress previews to `<150 KB` JPEG first.

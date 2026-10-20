---
description: Next.js patterns for QBook
globs: app/**/*,components/**/*
alwaysApply: false
---

# Next.js Rules
- App Router only. No `src/` directory.
- Prefer server components. Use `"use client"` only when interactivity needed.
- Route groups: `(app)` for employee shell, `(document)` for print/document shell.
- Layouts should not contain business logic — keep them structural.

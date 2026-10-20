---
name: phase-1-generation
description: Implement and verify phase-1 SEO generation using generatePageSEO and generateIndexSEO task wiring.
intent: >-
  Use when adding or validating SEO generation tasks, schedules, and flow sequencing for ad/search artifacts.
type: workflow
---

# Phase 1 Generation

## Goals

- Ensure compute flow includes `generatePageSEO` in the correct sequence.
- Ensure ads scheduled/default tasks execute `generateIndexSEO` every 6 hours.
- Ensure language template evaluation yields complete SEO payloads.

## Checklist

1. Verify compute flow task order places `generatePageSEO` before spotlight generation.
2. Verify ads task registry includes `generateIndexSEO`.
3. Verify ads default task delegates to `generateIndexSEO`.
4. Verify task config cron expression is `0 0 */6 * * *`.
5. Verify SEO payload includes expected fields and timestamps.

## Anti-Patterns

- Writing direct SEO output into generated route files.
- Relying on runtime side effects without task/config assertions.

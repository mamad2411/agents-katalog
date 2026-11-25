---
name: nextjs-safe-parallel-work
description: Safe concurrent editing patterns when multiple terminals, agents, or humans are working on the same Next.js codebase. Covers route-group isolation, branch awareness, and conflict avoidance.
version: 1.0.0
category: software-development
license: MIT
tags: [nextjs, concurrency, workflow]
tested: schema-only
tested_note: Workflow patterns validated at documentation level.
---

# Next.js Safe Parallel Work

When multiple terminals or agents are editing the same Next.js repo simultaneously:

## Core Rules
- Always run `git status` and `git branch --show-current` first to understand the active branch.
- Identify route groups (`(marketing)`, `(dashboard)`, `(admin)`) and treat them as ownership boundaries.
- Never modify files under a route group that another terminal has claimed (user will explicitly state this).
- Prefer changes to `lib/`, `types/`, `supabase/migrations/`, and shared API routes that are not marketing-specific.

## Pitfalls to Avoid
- Touching `(marketing)/**` when user says another terminal is upgrading the marketing page.
- Creating broad refactors that cross route groups.
- Committing marketing-related untracked files when the other session is still iterating.

## Recommended Workflow
1. Ask user which route groups or directories are off-limits.
2. Work only in safe directories (`lib/`, `supabase/migrations/`, core API logic, `types/`).
3. Use granular commits (one logical change per commit).
4. Document the safe scope in the commit message.

## Session Pattern: Production Hardening While Marketing Upgrade in Progress
When user says "another terminal is upgrading the marketing page":
- Explicitly avoid `app/(marketing)/**`
- Focus on: `supabase/migrations/`, `lib/qr/`, `lib/auth/`, `app/(dashboard)/**`, `app/api/**` (non-marketing), `types/`
- Example commits from session: migration 004, QR_SECRET hardening, OTP login page update
- Always confirm current branch and untracked files before editing

This skill was created after explicit user instruction to avoid marketing page conflicts during parallel work.

---
name: prd
description: Generate a complete, production-ready PRD (Product Requirements Document) for any application. Interviews the user, then outputs a precise technical spec that Claude Code can build from scratch. Use when user says "PRD", "cahier des charges", "spec my app", "app from scratch", or wants to plan a full application before coding.
---

# PRD Generator — From Idea to Build-Ready Spec

Generate a complete PRD that serves as a direct input to Claude Code for building a full application from zero.

## Principles

- The PRD must be **precise enough that Claude Code can build the entire app** without asking further questions
- Ask only what's needed — infer smart defaults for the rest
- Output one single, self-contained markdown file
- No fluff, no filler — every line must translate to code or architecture decisions
- Default stack: Next.js + Convex + Tailwind + shadcn/ui (override if user specifies)

## Workflow

### Phase 1 — Discovery Interview

Ask the user a **maximum of 8 questions**, grouped in 2 rounds.

**Round 1 — Core (ask all 4):**

1. **What does your app do in one sentence?** (e.g., "A platform where I sell video courses to a community")
2. **Who are the users and what are their roles?** (e.g., "Admin who manages content, Members who consume it")
3. **What are the 3-5 core features?** (e.g., "Video courses, community chat, member management, progress tracking")
4. **Do you have a specific design/brand direction?** (e.g., "Dark mode, minimal, like Linear" or "I don't care, pick something clean")

**Round 2 — Precision (ask only what's unclear after Round 1, max 4):**

5. **Authentication method?** (email/password, Google OAuth, magic link, etc.) — Default: email/password
6. **Monetization / payment?** (free, Stripe subscriptions, one-time, etc.) — Default: none
7. **Email notifications needed?** (welcome, invitations, transactional) — Default: yes with Resend
8. **Any integrations or APIs?** (Stripe, external webhooks, public API) — Default: none

If the user's initial message already answers most questions, skip to Phase 2 immediately. Don't re-ask what's obvious.

### Phase 2 — PRD Generation

Generate the PRD following the exact structure in `references/prd-template.md`.

**Rules:**
- Every feature must have a user story, data model fields, and UI description
- Every table must have explicit fields with types and indexes
- Every page must have a route, what it displays, and who can access it
- Include exact role permissions for every action
- Include environment variables needed
- Include deployment instructions

**Smart defaults to apply when not specified:**
- Auth: email/password with Convex Auth
- Database: Convex
- Email: Resend (free tier)
- Hosting: Vercel (free tier)
- Design: Light background, #171717 text, clean/flat, rounded corners, no gradients
- Language: French UI if user is French, English otherwise
- Roles: Admin (full access) + Member (limited access)
- Soft deletes for user-generated content
- Pagination for lists (20 items)
- Real-time updates via Convex subscriptions

### Phase 3 — Output

Write the PRD to: `~/Desktop/prd-[slug]/prd.md`

Also generate a companion file `~/Desktop/prd-[slug]/prompt-build.md` — a ready-to-paste prompt the user can give to Claude Code to start building immediately.

Open the folder when done:
```bash
open ~/Desktop/prd-[slug]/
```

Tell the user:
- The PRD is ready
- They can give `prompt-build.md` directly to Claude Code in a new project
- They can edit the PRD to add/remove features before building

## Anti-Patterns

- Don't generate vague requirements ("the app should be fast") — be specific ("paginate lists at 20 items, use Convex indexes on all queried fields")
- Don't describe features the user didn't ask for
- Don't add "future enhancements" sections — build what's needed now
- Don't use placeholder names — use the user's actual app name and terminology
- Don't write code in the PRD — describe what to build, not how to code it

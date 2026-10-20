---
allowed-tools: Bash, Read, Glob, Grep
description: Prime context by reading core files and summarizing codebase understanding
model: sonnet
---

# Prime

Execute the `Run`, `Read` and `Report` sections to understand the codebase then summarize your understanding.

## Context

Babylon is an isiXhosa pronunciation learning platform. Learners record phrases, get AI feedback (Whisper + Claude Sonnet 4), and optionally human verifier scores. Two SvelteKit apps (web learner, verifier reviewer) share a Convex backend with FSRS spaced repetition, PayFast billing, and en/xh i18n.

Add phrase to library (Claude auto-translates + generates phonetic guide) → start practice session → record audio → Whisper transcribes → Claude Sonnet 4 scores sound/rhythm/phrase (1–5) + coaching text → review AI feedback → pro tier: queued for human review → verifier claims (5-min TTL) + scores 3 dimensions + records exemplar → learner views combined feedback → flag triggers dispute (2 more reviewers, ±1 tolerance) → AI calibration tracks drift → FSRS + Web Push schedules next repetition.

Bun workspaces + Turbo monorepo. SvelteKit 2 (Svelte 5 runes) + Tailwind CSS 4 + shadcn-svelte frontends. Convex serverless backend (V8 + Node runtimes). Better Auth sessions. Paraglide JS i18n (en/xh). OpenAI Whisper + Anthropic Claude Sonnet 4 AI pipeline. PayFast billing. Web Push VAPID notifications. Vitest + convex-test. Railway deploy.

## Run

git ls-files

## Read

### Core (always read these):

- @README.md
- @convex/schema.ts

### Optional (read these only if needed):

#### Backend

- @convex/README.md

#### Web apps

- @apps/web/README.md
- @apps/verifier/README.md

## Report

Summarize your understanding of the codebase.

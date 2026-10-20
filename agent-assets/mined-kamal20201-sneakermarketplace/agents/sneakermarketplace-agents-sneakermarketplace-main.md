Codex Workspace Rules (AGENTS.md)

Purpose
- This file defines project-specific rules and preferences that Codex reads before answering any chat in this workspace.
- Keep it concise and concrete. Place non-obvious, high-impact rules first.

Cursor Rules
- Also read and honor all rules in `.cursor/rules/*.mdc` for this project.
- If any guidance conflicts, `.cursor/rules` takes precedence for this repo.

Behavior Rules
- Always: Ask 1–2 clarifying questions when scope or intent is ambiguous.
- Always: Explain planned terminal actions briefly before running commands.
- Always: Keep answers concise by default; expand only when asked.
- Ask First: Before running destructive commands (rm/reset) or installing packages.
- Ask First: Before changing config, adding dependencies, or altering build settings.
- Never: Expose secrets or print full .env contents in answers or logs.

Style and Tone
- Tone: Friendly, direct, and efficient. Avoid filler.
- Responses: Use short sections and bullet lists when they improve scanability.
- File References: Use clickable paths like `src/file.ts:42` (single line only).

Task Execution
- Scope: Make minimal, surgical changes focused on the user’s request.
- Tests: If tests exist, run targeted tests for modified code first.
- Validation: Prefer small, verifiable steps; summarize progress between steps.
- Plans: Use the plan tool for multi-step or ambiguous work only.

Code and Project
- Stack: Vite + React + TypeScript (see `package.json`).
- Formatting: Match existing style; do not add formatters unless requested.
- Types: Prefer explicit types in new/changed code; avoid one-letter names.
- Security: Treat environment variables and credentials as sensitive.

Shell and Approvals
- Approval Mode: Default to asking before actions needing elevated permissions or network.
- Sandboxing: Assume workspace-write, network restricted; call out when escalation is needed.
- Commands: Prefer `rg` for search; read files in <=250-line chunks.

Response Defaults
- Brevity: Target 3–8 lines unless detail is necessary.
- Structure: Use short headers sparingly; avoid over-fragmentation.
- Monospace: Wrap commands, paths, env vars, and identifiers in backticks.

When In Doubt
- Clarify requirements, propose a minimal plan, and confirm before large changes.

Project-Specific Rules (Customize Below)
- Backend: Supabase is the source of truth (DB/Auth/Storage/Edge Functions). Do not add custom servers. Use Edge Functions for server logic.
- Supabase Calls: Avoid redundant fetches. Cache shared data in React Context; expose typed hooks and explicit invalidate/refresh methods.
- Pagination: For any list/multi-item fetch, implement pagination; show fewer items first and add page controls at the bottom.
- Dependencies: Install latest stable versions. If unsure about API/usage, ask for a docs link and confirmation before adding. Request approval before changing build/config deps.
- TypeScript: Use strict typing in all new code. Do not change existing TypeScript config; ensure new code compiles under current strictness. Never use `any`.
- Mobile UI: Design mobile-first (320px+). Use Tailwind responsive prefixes (`sm:`, `md:`, `lg:`, `xl:`). Ensure touch targets ≥44px and test across screen sizes.
- UI Patterns: Follow shadcn/ui and Radix-based components in `src/components/ui/`; keep props minimal and typed.
- Secrets: Never echo or log values from `process.env.*`.

Notes
- Adjust or expand sections above to reflect your preferences.
- This file is intended to be read as high-priority context at session start.

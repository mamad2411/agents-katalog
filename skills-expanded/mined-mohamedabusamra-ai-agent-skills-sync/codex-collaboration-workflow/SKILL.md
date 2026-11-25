---
name: codex-collaboration-workflow
description: Apply Codex-specific collaboration rules for repo work: inspect before editing, preserve user changes, communicate progress concisely, validate the changed path, and record reusable lessons back into the shared skills system.
---

# Codex Collaboration Workflow

Use this when working in Codex or an OpenAI coding assistant session.

## Default operating rules

- Read the relevant files and code paths before proposing or making changes.
- Fix the root cause when practical, not just the visible symptom.
- Keep diffs small, local, and aligned with the existing repo patterns.
- Prefer existing utilities, scripts, and skills before adding new abstractions.
- Preserve user work: do not revert unrelated local changes unless explicitly asked.

## Communication style

- Give short progress updates while working when the task is more than trivial.
- State assumptions clearly when local context is incomplete.
- Call out blockers, risks, and validation gaps directly.
- Be concise in the final answer: explain what changed, what was verified, and what still needs attention.

## Repo workflow

- Prefer `rg` / `rg --files` for search.
- Use `apply_patch` for manual file edits.
- Validate the changed path with the lightest reliable check first: targeted test, lint, typecheck, or direct runtime check.
- If validation cannot be run, say so explicitly and explain why.

## Prompt memory

When `AGENTS.md` exists in the current repo, treat it as project-specific override memory on top of the shared baseline in:

- `~/ai-agent-skills-sync/PROJECT-BOOTSTRAP.md`
- `~/ai-agent-skills-sync/SKILL-AUDIT.md`
- `~/ai-agent-skills-sync/skills/master-engineering-standards/SKILL.md`

If repo-local guidance conflicts with the shared baseline, follow the repo-local rule and suggest recording the reusable difference back in this repo.

## Learning loop

When a reusable pattern emerges, suggest logging it:

```bash
~/ai-agent-skills-sync/record-learning.sh generated "title" "details and why it helped"
```

Prefer promoting the lesson into an existing skill before creating a new one.

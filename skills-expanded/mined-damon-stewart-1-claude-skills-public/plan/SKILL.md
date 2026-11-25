---
name: plan
description: "Interview-style planning skill. Asks targeted questions, outputs phased plan with completion promises. Use when starting any non-trivial project or feature."
effort: high
---

# Planning Skill

You are a senior technical planner. Interview the user, understand their goal deeply, and produce a structured implementation plan that a future Claude session (or Ralph loop) can execute phase by phase.

## Step 1: Interview (MANDATORY GATE -- cannot skip)

**Before writing any plan file, you MUST collect answers to all 5 required fields and write them to `/tmp/plan-interview-answers.json`. If that file does not exist with all fields populated, stop and run the interview. No exceptions.**

Required fields:
- `scope` -- what is being built/solved
- `success_criteria` -- how you'll know it worked (verifiable)
- `out_of_scope` -- what is explicitly excluded
- `design_reference` -- any visual/design reference or "none"
- `deploy_target` -- where it ships (Vercel, GitHub, local, etc.) or "none"

**Interview rules:**
- Ask ONE question at a time. Never batch questions.
- All questions must be binary numbered: 1a/1b, 2a/2b, etc. The user answers by letter.
- If the user answers "idk", "how would I know", or similar, immediately ask a simpler binary version of the same question. Do not repeat the open-ended form.
- Do NOT ask questions the codebase, context, or memory already answer.

**Question sequence:**
1. Scope: "Is this (1a) a new feature/project or (1b) a change to something existing?"
2. Done condition: "You'll know this worked when (2a) a specific thing is visible/measurable or (2b) a process no longer fails -- which is closer?"
3. Out of scope: "Is there anything that sounds related but should NOT be in this plan? (3a) Yes, describe it or (3b) No, all related work is in scope"
4. Design reference: "Is there a visual reference, example, or design file? (4a) Yes -- share it or (4b) No reference"
5. Deploy target: "Where does this ship? (5a) Vercel/web or (5b) local/internal/other"

Once all answers are collected, write `/tmp/plan-interview-answers.json`:
```json
{
  "scope": "...",
  "success_criteria": "...",
  "out_of_scope": "...",
  "design_reference": "...",
  "deploy_target": "..."
}
```

Read `~/.claude/skills/plan/gotchas.md` for planning pitfalls to avoid.

After writing the JSON, confirm your understanding in 2-3 sentences before proceeding.

## Step 1.5: Scout Plugins (conditional)

**Run for:** client projects, new features, multi-system work, anything touching APIs or external services.
**Skip for:** internal tooling, config changes, simple bug fixes, single-file edits.

When running:
```
Agent(subagent_type: "pr-pln-sct-plgns", model: "sonnet", prompt: "<task description from interview>")
```

Include the scout's recommendations in the plan where relevant. If nothing relevant, move on.

## Step 2: Research (silent)

Before writing the plan:
- Check what exists on disk (relevant directories, existing code, config files)
- Read any referenced files the user mentioned
- Check MEMORY.md for relevant project context
- If this plan is for a client project, read the client agent file at `~/.claude/agents/<client-name>.md`

## Step 3: Write the Plan

Read `references/plan-template.md` for the file template, formatting rules, and **naming convention**. Save to `~/.claude/plans/<contextual-name>.md` (e.g., `user-dashboard-redesign.md`, `api-migration-phase2.md`). Never use whimsical random names.

## Rules

1. **Plan approval != build approval.** When the user approves a plan, that means the *plan* is accepted. Still ask for explicit write approval before creating or modifying files in client projects.
2. **Every phase MUST have a completion promise** with a verifiable bash command. Non-negotiable.
3. **Phases must be independently verifiable.** Don't bundle unrelated work.
4. **Keep phases small enough for a single session.** If a phase would take more than 30 minutes, split it.
5. **Name files and directories explicitly.** Don't say "create a config file."
6. **Flag dispatch candidates.** Note phases that can be dispatched with `/dispatch`.
7. **Plan status cannot be `ready` while HIGHs are unresolved.** The adversarial gate in "After Writing" is not optional. Every plan gets all three reviewers. A plan with unresolved HIGH objections stays `status: blocked` in its frontmatter regardless of user approval.
8. **Gotchas learn from failure.** When a phase fails or the user corrects your approach, write a one-line gotcha to `~/.claude/skills/plan/proposed_gotchas.md`. Read existing `gotchas.md` and `proposed_gotchas.md` first to avoid duplicates. Proposed gotchas are reviewed during `/sync-context`. If `gotchas.md` exceeds 15 entries, ask the user which to prune before merging.

## After Writing

### Step A: Show the plan

Show the plan outline (phase names + one-line descriptions), then the full plan text.

### Step B: Adversarial review (mandatory, runs before user approval)

Immediately after showing the plan, dispatch three reviewer agents in parallel. Do not ask permission. Do not offer to skip.

Read `references/reviewer-prompts.md` for the system prompts. Pass the full plan text as context in each prompt.

```
Agent(subagent_type: "general-purpose", model: "opus", prompt: "<Skeptic system prompt>\n\nPlan to review:\n\n{full plan text}")
Agent(subagent_type: "general-purpose", model: "opus", prompt: "<Scope-Cutter system prompt>\n\nPlan to review:\n\n{full plan text}")
Agent(subagent_type: "general-purpose", model: "opus", prompt: "<Implementation Realist system prompt>\n\nPlan to review:\n\n{full plan text}")
```

Collect all three outputs. Write them to `~/.claude/plans/reviews/{plan-name}.md` using the schema in `references/review-template.md`. Substitute the real plan name into the readiness gate grep command in that file.

Create `~/.claude/plans/reviews/` if it does not exist.

### Step C: Readiness gate

Count unresolved HIGH objections:

```bash
grep -c '^\[HIGH\]' ~/.claude/plans/reviews/{plan-name}.md | grep -v 'RESOLVED\|WONTFIX'
```

If count > 0:
- Display each unresolved HIGH to the user with its reviewer and category
- State: "Plan is BLOCKED. Each HIGH objection needs either a plan amendment (then mark RESOLVED) or WONTFIX: <reason>."
- Wait for the user to address them, then re-run the count
- Once count = 0, update the review file frontmatter: `status: READY`, `high_unresolved: 0`

If count = 0 on first pass (rare): state how many total objections were logged and that none were HIGH, then proceed.

The plan file's frontmatter status must NOT be set to `ready` while high_unresolved > 0.

### Step D: Post-gate options

Once READY:
- Show a one-line summary: "N HIGH resolved, M MED logged for reference, K LOW ignored."
- Ask: "Ready to execute, or want to adjust?"
- Optional fourth pass: ask if the user wants a collegial Gemini or Opus review on top of the adversarial gate. This is additive, not a replacement.

### Step E: Outcome tracking (end of session)

During `/sync-context`, prompt: "Any review objections from this session worth tagging as real or noise?" Point to `~/.claude/plans/reviews/objection-outcomes.md`. See `references/objection-outcomes.md` for schema and self-tuning guidance.

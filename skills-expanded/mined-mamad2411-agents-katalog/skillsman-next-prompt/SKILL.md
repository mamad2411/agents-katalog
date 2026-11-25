---
name: skillsman-next-prompt
description: Create a concise, context-aware next prompt that tells Codex what to do next. Use when the user asks for a next prompt, better prompt, continuation prompt, handoff prompt, new chat prompt, resume prompt, context transfer, or wants to continue, steer, or restart work while preserving relevant Superpowers workflow discipline.
---

# Skillsman Next Prompt

Generate a ready-to-paste prompt that helps the user get the next useful action from Codex. The prompt may target the current conversation, a fresh Codex conversation, or another agent. Base it on the visible conversation, repository state, and any available local evidence.

Preserve the user's latest intent and constraints. When the prompt is for a fresh Codex conversation or agent handoff, require the next agent to start with `$superpowers:using-superpowers` before acting.

## Workflow

1. Identify the prompt target:
   - Current conversation, fresh conversation, or agent handoff.
   - Immediate desired outcome: plan, implement, debug, review, verify, summarize, or decide.
   - Whether the target should continue existing work or reframe the task from scratch.

2. Identify the task context:
   - Current goal or user request.
   - Current working directory, repo, branch, and relevant files.
   - Decisions already made and constraints the next prompt must preserve.

3. Collect compact evidence before drafting when available:
   - Check `pwd`, `git status --short`, and relevant file paths if working in a repo.
   - Include only commands/results that materially affect the next step.
   - Mark unverified assumptions explicitly instead of presenting them as facts.

4. Preserve operating constraints:
   - User's latest explicit instructions.
   - Scope boundaries and things not to touch.
   - Required skill or workflow dependencies.
   - Human approval gates before irreversible actions, posting, applying, pushing, or deploying when relevant.

5. Draft the prompt as an instruction, not as a status report.

## Output Format

Return only the prompt unless the user asks for explanation.

For current-conversation prompts, use this structure:

```text
Next prompt:
<direct instruction to Codex>

Context to preserve:
- <brief facts, constraints, files, or decisions>

Success condition:
- <what a good answer or completed action should produce>
```

For fresh-conversation or handoff prompts, use this structure:

```text
Use $superpowers:using-superpowers first.

Task:
<one-sentence goal>

Context:
- Workspace: <absolute path>
- Current state: <brief status>
- Important files: <paths and why they matter>
- User constraints: <scope, style, approval gates>

What has already happened:
- <facts from current conversation or verified local state>

Next steps:
1. <immediate next action>
2. <verification or decision point>
3. <completion criterion>

Do not:
- <explicit non-goals or risky actions to avoid>
```

## Quality Bar

- Keep the prompt short enough to paste into a new chat without becoming a transcript.
- Prefer exact file paths, commands, dates, branch names, and artifact names over general summaries.
- Include `$superpowers:using-superpowers` only when the next prompt targets a fresh Codex conversation or agent handoff, or when the user explicitly asks for Superpowers-based flow.
- If the task is unfinished because of a blocker, make the blocker and the requested user decision explicit.
- If the user asks for multiple prompt options, provide distinct prompts for distinct intents instead of minor wording variants.
- If the user asks for a Chinese prompt, write the prompt in Chinese while preserving literal tool, path, command, and skill names.

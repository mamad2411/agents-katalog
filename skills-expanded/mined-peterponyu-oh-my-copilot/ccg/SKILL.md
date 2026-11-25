---
name: ccg
description: "[OMCP] Claude-Codex-Gemini tri-model orchestration via /ask codex + /ask gemini, then Claude synthesizes results"
level: 5
---

# CCG - Claude-Codex-Gemini Tri-Model Orchestration

CCG routes through the canonical `/ask` skill (`/ask codex` + `/ask gemini`), then Claude synthesizes both outputs into one answer.

Use this when you want parallel external perspectives without launching tmux team workers.

## When to Use

- Backend/analysis + frontend/UI work in one request
- Code review from multiple perspectives (architecture + design/UX)
- Cross-validation where Codex and Gemini may disagree
- Fast advisor-style parallel input without team runtime orchestration

## Requirements

- **Codex CLI**: `npm install -g @openai/codex` (or `@openai/codex`)
- **Gemini CLI**: `npm install -g @google/gemini-cli`
- `/omcp:ask` skill available (the advisor router used below)
- If either CLI is unavailable, continue with whichever provider is available and note the limitation

## How It Works

```text
1. Claude decomposes the request into two advisor prompts:
   - Codex prompt (analysis/architecture/backend)
   - Gemini prompt (UX/design/docs/alternatives)

2. Claude runs each advisor's provider CLI directly, following the
   `/omcp:ask` routing logic (skill nesting is not supported, so apply the
   ask procedure inline rather than invoking the skill):
   - run the Codex CLI with `<codex prompt>`
   - run the Gemini CLI with `<gemini prompt>`

3. Artifacts are written under `.omcp/artifacts/ask/`

4. Claude synthesizes both outputs into one final response
```

## Execution Protocol

When invoked, Claude MUST follow this workflow:

### 1. Decompose Request
Split the user request into:

- **Codex prompt:** architecture, correctness, backend, risks, test strategy
- **Gemini prompt:** UX/content clarity, alternatives, edge-case usability, docs polish
- **Synthesis plan:** how to reconcile conflicts

### 2. Invoke advisors via CLI

> **Note:** Skill nesting (invoking a skill from within an active skill) is not
> supported, so do not call `/omcp:ask` here. Instead apply the `/omcp:ask`
> routing logic inline: run each provider CLI directly via the Bash tool and
> persist its output under `.omcp/artifacts/ask/` exactly as the ask skill does.

Run both advisors (provider CLIs, invoked directly):

```bash
codex exec "<codex prompt>"      # Codex CLI
gemini -p "<gemini prompt>"      # Gemini CLI
```

(Use whatever the installed provider CLI's non-interactive flag is; the goal is
one prompt in, one response out, captured to an artifact.)

### 3. Collect artifacts

Read latest ask artifacts from:

```text
.omcp/artifacts/ask/codex-*.md
.omcp/artifacts/ask/gemini-*.md
```

### 4. Synthesize

Return one unified answer with:

- Agreed recommendations
- Conflicting recommendations (explicitly called out)
- Chosen final direction + rationale
- Action checklist

## Fallbacks

If one provider is unavailable:

- Continue with available provider + Claude synthesis
- Clearly note missing perspective and risk

If both unavailable:

- Fall back to Claude-only answer and state CCG external advisors were unavailable

## Invocation

```bash
/omcp:ccg <task description>
```

Example:

```bash
/omcp:ccg Review this PR - architecture/security via Codex and UX/readability via Gemini
```

---
name: multi-model-code-review
description: >-
  Review code changes through multiple AI models before sending to human
  reviewers. Use when the user asks to review a branch with sub-agents, run
  a multi-model code review, get AI review feedback, or mentions "review my
  branch," "sub-agent review," or "iterate on the code."
compatibility: >-
  Requires at least one agentic CLI that can send prompts to models and
  print responses. Supported CLIs: Cursor Agent (`agent`, install via
  `curl https://cursor.com/install -fsS | bash`), Claude Code (`claude`),
  OpenAI Codex (`codex`). Requires Shell tool access and git.
---

# Multi-Model Code Review

Run code changes through multiple AI models to catch issues before human
review. Each model reviews independently, feedback is synthesized, changes
are made, and the loop repeats until the code is solid.

## Prerequisites

At least one agentic CLI must be installed and authenticated:

| CLI | Verify | Print-mode flag |
|-----|--------|-----------------|
| Cursor Agent | `agent --version` | `agent --model <model> --print "<prompt>"` |
| Claude Code | `claude --version` | `claude --model <model> -p "<prompt>"` |
| OpenAI Codex | `codex --version` | `codex --model <model> -q "<prompt>"` |

If cursor's `agent` is installed, always prefer using that and specifying models rather than mixing and matching CLI utilities.

## Workflow

### 1. Prepare the review context

Gather the diff and any relevant context for the reviewer. Write it to a
temporary file using the template in
[assets/code-review-prompt-template.md](assets/code-review-prompt-template.md).

```bash
# Get the diff against the parent branch
git diff <parent-branch>...HEAD > /tmp/review-diff.txt
```

Include in the prompt:
- **Origin** — where the work came from (ticket link, user conversation,
  incident, spec/RFC). This gives the reviewer the "why."
- **What changed and why** — a brief summary of the goal.
- **The diff** — the actual code changes.
- **Key files** — full contents of new or heavily modified files (diffs alone
  can lack context for new classes).
- **Relevant conventions** — project-specific patterns the reviewer should
  enforce (e.g. naming, logging, testing conventions).

### 2. Send to models in parallel

Fire both review requests in a single message so they run concurrently.
Use whichever CLI(s) and models the user prefers. If the user does not
specify, you always want to use the latest model that is high thinking
from two different providers.

```bash
# Cursor Agent
agent --model gpt-5.4-xhigh --print "$(cat /tmp/code-review.md)" 2>&1
agent --model claude-4.6-opus-max-thinking --print "$(cat /tmp/code-review.md)" 2>&1

# Claude Code
claude --model claude-sonnet-4-20250514 -p "$(cat /tmp/code-review.md)" 2>&1

# OpenAI Codex
codex --model o3 -q "$(cat /tmp/code-review.md)" 2>&1
```

### 3. Synthesize feedback

After both responses return:

1. Categorize each piece of feedback as **critical**, **recommended**, or
   **trivial**.
2. Identify points of **agreement** — these are high-confidence issues.
3. Identify **disagreements** — evaluate which model is correct by checking
   the actual codebase.
4. Challenge feedback that is wrong (see Guidelines below).
5. Summarize the synthesis to the user.

### 4. Implement fixes

Address critical and recommended feedback. For each fix:
- Make the change.
- Note which reviewer's feedback drove it.

### 5. Re-review if needed

Send the updated code back for another round.
Skip re-review for trivial fixes (typos, comment tweaks).

Repeat until:
- No unresolved critical issues remain.
- Both models approve or approve-with-minor-changes.

### 6. Push for human review

Once AI reviewers are satisfied, push the branch and create the MR/PR.
The AI review rounds serve as a quality gate, not a replacement for human
review.

## Guidelines

- **Always use thinking models.** Code review requires deep reasoning about
  behavior, edge cases, and sequencing. Never use non-thinking models
  (e.g. `gpt-4o`, `claude-sonnet`). Use models with extended thinking
  (e.g. `gpt-5.3-codex-high`, `composer-2`, `claude-sonnet-4-thinking`,
  `o3`).
- **Use different providers.** Models from the same provider share training
  biases. Use at least two different providers to get genuinely diverse
  perspectives.
- **Send reviews with no prior context.** Do not include your own assessment
  or opinions in the review prompt. Each model must form an independent
  judgment from the code alone.
- **Challenge feedback that is wrong.** Consensus does not mean capitulation.
  If a reviewer suggests a change that contradicts project conventions,
  misreads the code, or would introduce a regression, push back with
  evidence. Include the correction in the next review round so the model
  can learn from the context. A model being confident does not make it
  correct.
- **Let reviewers see the codebase.** When using CLIs that support workspace
  access (e.g. `agent` with `--print`), run from the repo root so the
  reviewer can read files for context beyond the diff.
- **Don't rubber-stamp.** If both models say "looks good" but you see an
  issue, raise it. The models are reviewers, not authorities.
- **Preserve existing test coverage.** If a reviewer suggests removing or
  weakening tests, reject it unless there is a clear justification (e.g.
  the test was asserting on an implementation detail that changed).

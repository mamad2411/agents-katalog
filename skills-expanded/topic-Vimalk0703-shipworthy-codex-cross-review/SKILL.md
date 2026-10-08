---
name: codex-cross-review
description: Use when the user wants Codex to review Claude's work, cross-validate PRs, or run high-volume PR review with dual-model verification using the codex-plugin-cc plugin.
invoke_when: Use when the user asks for Codex review, cross-validation of Claude's output, PR review at scale, or dual-model code review using Codex as a second opinion.
---

# Codex Cross-Review

> **Optional capability.** This skill requires the `codex-plugin-cc` Claude Code plugin and the OpenAI Codex CLI. All other Shipworthy skills work independently — this adds dual-model review on top. Users without Codex installed lose nothing; they simply use Claude's built-in `code-reviewer` agent via `shipworthy:requesting-code-review` instead.

When activating, output:
> ⚓ **shipworthy** › skill: `codex-cross-review` — dispatching Codex for cross-model review

## Availability Check

Before invoking any `/codex:*` command, check whether the plugin is available. If `/codex:setup` is not recognized or reports Codex is not installed:

1. Inform the user that this skill requires the `codex-plugin-cc` plugin
2. Offer setup guidance (see Prerequisites below)
3. Fall back to Claude's built-in `code-reviewer` agent — it covers the same checklist without Codex

This skill **never blocks work**. If Codex is unavailable, the review still happens via Claude's own agent.

## Prerequisites

Requires two things — the Codex CLI and the Claude Code plugin:

```bash
# 1. Install and authenticate the Codex CLI (one-time)
npm install -g @openai/codex
codex login                          # browser OAuth (ChatGPT account, incl. Free tier)
# OR: codex login --with-api-key     # OpenAI API key
# OR: codex login --device-auth      # headless/SSH environments

# 2. Install the Claude Code plugin (one-time)
/plugin marketplace add openai/codex-plugin-cc
/plugin install codex@openai-codex
/reload-plugins

# 3. Verify
/codex:setup
```

No environment variables needed — the Codex CLI manages its own credentials.

## When to Use

- After Claude completes a feature — Codex reviews for blind spots
- Before merging any PR — structured review with severity-rated findings
- High-volume PR review — batch review workflow across multiple PRs
- When the user wants a second opinion from a different model
- Before shipping to production — final cross-validation gate

## Cross-Validation Workflow

### Pattern A: Post-Implementation Review (Single PR)

After Claude finishes implementing:

1. **Synchronous review** for small changes:
   ```
   /codex:review --base main --wait
   ```

2. **Background review** for larger changes (non-blocking):
   ```
   /codex:review --base main --background
   ```
   Then poll with `/codex:status` and fetch with `/codex:result`.

3. **Adversarial review** to challenge design decisions:
   ```
   /codex:adversarial-review --base main --wait
   ```

4. Address findings by severity:
   - **Critical**: Fix immediately before merge
   - **High**: Fix before merge
   - **Medium**: Fix or document as accepted risk
   - **Low**: Address in follow-up or dismiss with rationale

5. Re-run review after fixes:
   ```
   /codex:review --base main --wait
   ```

### Pattern B: High-Volume PR Review

When reviewing multiple PRs (e.g., from a team):

1. For each PR branch, run background reviews in parallel:
   ```
   git checkout pr-branch-1
   /codex:review --base main --background
   git checkout pr-branch-2
   /codex:review --base main --background
   ```

2. Poll all jobs: `/codex:status --all`

3. Fetch results per job: `/codex:result <job-id>`

4. Triage findings across PRs by severity — prioritize Critical and High across all PRs before addressing Medium/Low.

### Pattern C: Claude + Codex Dual Review

For maximum confidence, run both Claude's code-reviewer agent and Codex review:

1. Dispatch Claude's code-reviewer agent via `shipworthy:requesting-code-review`
2. Simultaneously run: `/codex:adversarial-review --base main --background`
3. Compare findings — items flagged by both models are highest priority
4. Items flagged by only one model deserve extra scrutiny
5. Synthesize a unified review with all unique findings

### Pattern D: Review Gate (Automated)

Enable the stop-hook review gate so Codex automatically reviews before session end:

```
/codex:setup --enable-review-gate
```

This runs a targeted Codex review on every Stop event. If findings are critical, the session blocks until they are resolved. Disable when not needed:

```
/codex:setup --disable-review-gate
```

## Codex Review Output Schema

Reviews return structured JSON:

```json
{
  "verdict": "approve | needs-attention",
  "summary": "One-line summary",
  "findings": [
    {
      "severity": "critical | high | medium | low",
      "title": "Finding title",
      "body": "Detailed description",
      "file": "path/to/file",
      "line_start": 42,
      "line_end": 50,
      "confidence": "high | medium | low",
      "recommendation": "Suggested fix"
    }
  ],
  "next_steps": ["Action items"]
}
```

## Delegation to Codex

When Claude is stuck or needs deeper investigation:

```
/codex:rescue investigate the flaky test in test_upload.py
```

Poll with `/codex:status`, fetch with `/codex:result`, and resume with `/codex:rescue --resume`.

## Integration with Shipworthy Skills

- Invoke `shipworthy:requesting-code-review` for Claude-side review
- Invoke `shipworthy:receiving-code-review` to process Codex findings
- Invoke `shipworthy:quality-gates` after all review findings are addressed
- Invoke `shipworthy:verification-before-completion` as the final step

## Graceful Degradation

This skill adapts to what's available:

| Environment | Behavior |
|-------------|----------|
| Claude Code + Codex plugin + Codex CLI | Full dual-model review (all patterns) |
| Claude Code + Codex CLI (no plugin) | Guide user to install plugin, fall back to Claude reviewer |
| Claude Code only (no Codex) | Fall back to `shipworthy:requesting-code-review` (Claude's code-reviewer agent) |
| Codex standalone (via adapter) | User reads this skill as documentation; commands don't apply |
| Other tools (Cursor, Copilot, etc.) | Not applicable — use their respective adapters |

The fallback is always Claude's built-in code-reviewer agent, which covers the same checklist (plan alignment, architecture, quality, security, testing, performance, type safety).

## Anti-Patterns

- Running Codex review on uncommitted changes without a clear diff scope
- Auto-applying all Codex suggestions without human judgment
- Skipping Claude's own review and relying solely on Codex
- Leaving the review gate enabled during exploratory/prototyping sessions
- Ignoring low-confidence findings without reading them first

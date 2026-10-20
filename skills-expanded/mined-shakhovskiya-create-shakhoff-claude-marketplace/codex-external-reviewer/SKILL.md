---
name: codex-external-reviewer
description: "External review via Codex CLI (cross-model second opinion). Activated if codex-plugin-cc installed. Falls back gracefully if Codex unavailable. Provides VERDICT: AGREE / DISAGREE / FOUND_NEW_ISSUES."
---

# Codex External Reviewer

Cross-model review через Codex CLI - independent second opinion.

## Когда применять

- Phase 5.6 sprint cycle (after internal SE review)
- Conditional: only если codex-plugin-cc installed
- Required в strict mode if Codex available

## Observability contract

Every review output (markdown file in `.sprints/active/reviews/codex-review-sprint-<n>.md`)
MUST include YAML frontmatter:

```yaml
---
produced_by: codex|deepseek|disabled
provider_version: "<cli-version-or-model-id>"
fallback_reason: "<empty if primary used; otherwise short reason>"
duration_ms: <int>
verdict: AGREE|DISAGREE|FOUND_NEW_ISSUES|UNAVAILABLE
---
```

This enables `/sprint:metrics` and `/sprint:codex-status` to surface:
- Which sprints got primary vs. fallback review.
- Average duration by provider.
- Failure modes (auth, geoblock, timeout).

If neither primary nor fallback available, emit a stub review with
`produced_by: disabled` and `verdict: UNAVAILABLE`. Do NOT silently skip.

## Pre-flight

Check codex-plugin-cc:

```bash
# Check if /codex:review command available (indicates plugin installed)
if ! command_available "/codex:review"; then
    log "codex-plugin-cc not installed - skip external review"
    return SKIP
fi

# Check Codex CLI working
if ! codex --version >/dev/null 2>&1; then
    log "Codex CLI not responding - cannot do external review"
    return SKIP_TECHNICAL
fi
```

If Codex unavailable - graceful skip:
- В strict mode: log warning, skip (don't block sprint just because Codex missing)
- Document в retrospective: "External review skipped - Codex unavailable"

## Workflow

Когда Codex available:

### 1. Build context for Codex

Sprint context:
- Sprint goal
- Tasks completed
- Increment files (paths)
- Internal SE review findings
- Code diff summary

```markdown
# Sprint {{N}} for External Review

## Goal
{{GOAL}}

## Tasks
{{TASKS_SUMMARY}}

## Increment

Files created/modified в этом sprint:
{{FILES_LIST}}

## Internal SE review findings

{{SE_FINDINGS}}

## Question for Codex

Do you agree with internal review? Have any new issues been missed?
Apply adversarial review - look for what Claude might have structurally missed.
```

Saved to `/tmp/codex-context-{UUID}.md`.

### 2. Sanitize for security

Before sending to Codex - check for secrets:

```bash
# Use gitleaks или similar to scan context
gitleaks detect --source /tmp/codex-context-${UUID}.md --no-git

# If secrets found - redact before sending
if secrets_found; then
    redact_secrets /tmp/codex-context-${UUID}.md
fi
```

### 3. Invoke Codex

Через codex-plugin-cc command:

```bash
# Use existing plugin command
/codex:adversarial-review "$(cat /tmp/codex-context-${UUID}.md)"
```

OR direct codex CLI invocation:

```bash
codex exec -m gpt-5.4-codex -s read-only \
  -o /tmp/codex-result-${UUID}.md \
  "$(cat /tmp/codex-context-${UUID}.md)"
```

ВАЖНО: `-s read-only` - Codex auditor никогда modifies code.

### 4. Parse result

Codex output должен content match:
- Findings list (severity + description + suggestion)
- VERDICT: AGREE_WITH_CLAUDE | DISAGREE | FOUND_NEW_ISSUES

If output не conforms - retry once с reformulated prompt.
If still bad - log error, mark review as FAILED_TECHNICAL.

### 5. Process findings

#### If VERDICT: AGREE_WITH_CLAUDE
- Sprint review confirms
- DoD criterion 8 PASSES
- Log to review file

#### If VERDICT: DISAGREE
- Codex thinks SE review made wrong call
- Surface to user (interactive) или log (non-interactive)
- Don't auto-resolve - human decision

#### If VERDICT: FOUND_NEW_ISSUES
- Codex caught what Claude missed
- For each new issue:
  - Add to retrospective
  - If BLOCKER/CRITICAL severity: BLOCK sprint close until addressed
  - If lower: log for next sprint cycle to address

### 6. Save review file

`.sprints/active/reviews/codex-review-sprint-{N}.md`:

```markdown
# Codex External Review: Sprint {{N}}

**Reviewed by**: Codex (gpt-5.4-codex via codex-plugin-cc)
**Reviewed at**: {{TIMESTAMP}}

## Verdict

{{AGREE_WITH_CLAUDE | DISAGREE | FOUND_NEW_ISSUES}}

## Findings (if any)

{{FINDINGS_LIST}}

## Comparison with internal SE review

{{COMPARISON}}

## Action items

{{ACTIONS}}
```

## Fallback strategies

### If Codex unavailable

1. **Skip review with logging**:
   - Document в retrospective: "External review skipped - Codex unavailable. Reason: {reason}"
   - В strict mode + если external review was REQUIRED для this sprint: WARN but не BLOCK
   - Workflow continues

2. **DeepSeek fallback** (если configured):
   - Config option `reviews.external.fallback.enabled: true`
   - Use OpenRouter с DeepSeek-V4 через aider
   - Cross-family second opinion (Anthropic vs DeepSeek - different training)
   - Mark review as `reviewed_by: deepseek-v4` для transparency
   - Не как good как Codex но better than nothing

```bash
# Fallback invocation
aider --model openrouter/deepseek/deepseek-v4-pro \
  --no-auto-commits --yes-always \
  --message-file /tmp/codex-context-${UUID}.md \
  > /tmp/fallback-result-${UUID}.md 2>&1
```

### Network blocked (geoblock for RU)

If user in restricted geography:
- Codex API возможно blocked
- Plugin может handle с corporate proxy если configured
- See codex-plugin-cc docs для setup
- Plugin attempts both - if both fail, fallback to DeepSeek или skip

## Security considerations

### Never send secrets to external API

Before any send:
- Run gitleaks/secrets scan
- Redact found secrets
- Log redactions для audit

### Read-only sandbox

Codex CLI invoked с `-s read-only`:
- Cannot modify codebase
- Cannot create files outside sandbox
- Pure analysis role

### Audit trail

Все Codex invocations logged:
- Timestamp
- Context size (chars)
- Verdict
- Saved transcript

## Output

`.sprints/active/reviews/codex-review-sprint-{N}.md` if review ran.
Updated `_state.json`:
- `external_review_status`: passed | failed | skipped | unavailable
- `external_review_verdict`: AGREE | DISAGREE | FOUND_NEW_ISSUES (if completed)

## Limitations

- Codex output не deterministic (LLM)
- May produce false negatives (miss real issues)
- May produce false positives (suggest unnecessary changes)
- Treat as second opinion, не source of truth

When Codex DISAGREES with internal SE - human judgment required, не auto-revert.

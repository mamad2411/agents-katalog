---
name: review
description: Code review with strict focus on Pi Extension safety, tool guardrails, and optimal API usage. Use when reviewing PRs, checking new tools, or verifying architectural changes.
---
# Pi Extension Code Review

Review code changes and identify high-confidence, actionable bugs specifically related to Pi Extension development, safety, and guardrail compliance.

## Requirements

1. **Complete Diff**: You must have the full character-level diff of the changes being reviewed.
2. **Context**: Understand that this extension uses the `@earendil-works/pi-coding-agent` Extension API.

## High-Signal Pi Bug Patterns

Flag any of the following issues with high confidence. Do not list speculative nitpicks.

### 1. Guardrail Evasion
- Missing security checks for dangerous shell commands (e.g., `rm -rf /`, `curl | bash`).
- Tools that access cloud metadata IPs (`169.254.169.254`) without explicit opt-in.
- Hardcoded secrets or `.env` reads directly exposed to the model without stripping.

### 2. Tool Registration Errors
- Tools registered without `Typebox` schemas for parameters.
- Missing `name`, `label`, or `description` fields in `pi.registerTool`.
- `execute` functions that do not return the required `{ content: [{ type: "text", text: string }], details: any }` format.

### 3. Missing Context Returns
- Tool outputs that do not summarize the action performed.
- Silent failures (e.g., catching an error but returning a "Success" text instead of the error message).

### 4. Overly Permissive Scope
- Tools that use `execute_url` or `read_url` on wildcard domains unnecessarily.
- Tools requesting root filesystem access (`/`) instead of workspace-relative paths.

## Analysis Discipline

Before flagging an issue:
1. Trace the data flow of the tool parameter to confirm the vulnerability.
2. Check existing tests and `guards.ts` (if applicable) to see if the vulnerability is mitigated upstream.
3. Confirm it's a real bug, not a style preference.

## Output Format

For each finding:
- **Location**: File + line range.
- **Severity**: Critical / High / Medium / Low.
- **Issue**: What is wrong.
- **Fix**: How to fix it using Pi best practices.

## Chaining

If you find critical gaps during review (e.g., "We are missing a guardrail for command injection"), trigger the `autoresearch` skill to find standard mitigation patterns or check if Pi's base layer already handles it.

---
name: agent-eval-verify
description: Use when verifying AI agent responses during evaluation — content matching, behavioral assertions, AI-judged quality, and compliance checks with optional multi-step verification flows
---

# Agent Eval — Verify

## Overview

Evaluates verification blocks from an eval config against current browser state using `playwright-cli`. Each verify block has a `type`, optional `steps`, and a `check`. Types are defined in the YAML config — the skill evaluates whatever type is specified.

## Verify Block Format

```yaml
- type: <any type defined in the eval config>
  steps:          # optional — actions before checking
    - "Click the link"
  check: "Assertion in natural language"
  threshold: 120  # optional — for timing checks, max seconds allowed
```

## Process

1. If block has `steps`, execute each via agent-eval-browser-interact pattern
2. Capture page state using playwright-cli
3. Evaluate `check` based on `type`
4. Return result as JSON

## Capturing Page State

```bash
# Get visible text
playwright-cli --raw eval "document.body.innerText"

# Get current URL
playwright-cli --raw eval "location.href"

# Take screenshot
playwright-cli screenshot --filename=screenshots/verify-N.png

# Take snapshot for element inspection
playwright-cli snapshot
```

## How to Evaluate

Read the `type` and `check` from the verify block. The type tells you what lens to evaluate through:

- **Factual/content checks** — extract page text, look for specific words or conditions
- **UI/behavioral checks** — check URLs, element visibility, page state
- **Quality/judgment checks** — read text + screenshot, reason about whether the check is met
- **Strict checks** — same as judgment but borderline = fail (for safety, compliance)
- **Timing checks** — compare elapsed time against `threshold`
- **Visual checks** — look at screenshot, judge image quality/relevance/composition
- **Brand checks** — compare output against brand kit or style direction expectations

The `check` field is always natural language. Use it as the evaluation criteria regardless of type.

## Result Format

- **pass** — clearly meets the check
- **warning** — partially meets or borderline
- **fail** — clearly violates the check

Always provide a 1-2 sentence explanation.

## Output Format

```json
{
  "type": "content",
  "check": "Response mentions 30-day refund window",
  "status": "pass",
  "explanation": "Found '30-day refund policy' in response text.",
  "screenshot": "verify-0.png",
  "category": "functional"
}
```

Category is derived from the type — use the type name as the category for report grouping.

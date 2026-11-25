---
name: lark-team-health-report-builder
version: "1.0"
description: Builds Lark team-health command parsing, progress-message payloads, and report-message payloads from collected GitHub and AI analysis results.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - team-health
    - lark
    - github
    - payload-builder
  clawdbot:
    emoji: "bar_chart"
    files:
      - "references/*"
      - "scripts/*"
---

# Lark Team Health Report Builder

Use this skill when a Lark command triggers a team-health analysis run.

This skill owns deterministic request parsing and Lark response payload construction. It does not read GitHub, call an LLM, store NyxID tokens, or send Lark messages.

## When to use

Use for a linear GAgent flow:

1. Receive a Lark message event.
2. Parse `/team-health` and target user.
3. Send a progress message.
4. Collect GitHub/activity inputs through NyxID connectors.
5. Ask the model for risk analysis.
6. Build the final Lark report message.

## Inputs

The caller may invoke the script in either mode:

- `mode: "parse_command"` with raw Lark event body.
- `mode: "build_messages"` with parsed command plus `report` text.

See `references/team-health-contract.md` for exact aliases and output shapes.

## Output

Return JSON with either:

- `skip: true` for non-command/challenge events.
- parsed command fields and a progress Lark message body.
- final Lark text message body.

## Determinism requirement

Follow `references/team-health-contract.md`. If executing code is allowed, use `scripts/build_team_health_payload.js` as the reference implementation.

Do not invent GitHub data, team members, NyxID tokens, Lark chat ids, or model analysis.

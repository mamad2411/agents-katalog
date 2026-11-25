---
name: kv-line-parse
description: >-
  Parse key-value line format files: quoted "description" key_value or unquoted
  name key_value lines, output JSON dict to stdout.
category: General-Utility
---

# KV Line Parse (v1)

This base skill provides a standalone parser for the key-value line format — a
line-oriented key-value file used to store API keys and secrets alongside
human-readable descriptions.

Two line formats are accepted:

1. **Quoted description**: `"Google AI Studio" AIzaSyAbc123`
2. **Unquoted name**: `Cerebras csk-token`

Blank lines are skipped. Output is a JSON dictionary mapping description/name
to the corresponding value.

***

## Script

[`scripts/parse_keywords.py`](scripts/parse_keywords.py) — accepts `--file <path>`
or reads stdin.

**Invocation examples:**

```bash
# stdin
echo '"My Key" sk-value123' | python3 .agents/skills/general/kv-line-parse/scripts/parse_keywords.py

# file
python3 .agents/skills/general/kv-line-parse/scripts/parse_keywords.py \
  --file /path/to/<key-file>
```

**Output:**

```json
{
  "My Key": "sk-value123"
}
```

Exit code: 0 on success, 1 on error (diagnostic to stderr).

***

## Composition by Higher-Level Skills

| Composer Skill | Domain | How It Consumes This Base |
|---|---|---|
| `opencode-ssot-provider-ext-sync` | opencode/ | Calls `scripts/parse_keywords.py --file <key-file>` to resolve key descriptions to actual values for auth/account sync entries |

***

## Related Skills

- [`skill-factory`](../../skill-factory/SKILL.md) — post-drafting checklist enforces
  script delivery and cross-reference compliance.

***

## Traceability

- Created: 2026-07-05
- Source: `parse_keywords()` function extracted from
  `sync-provider-extensions.py` in the private config repo.
- Rationale: the key-value parser is domain-agnostic, satisfying the
  Layered Composition Mandate (ai-rule-standardization-rules.md §2).

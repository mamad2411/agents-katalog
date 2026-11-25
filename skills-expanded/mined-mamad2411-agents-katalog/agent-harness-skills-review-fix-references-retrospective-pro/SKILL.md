# Retrospective Prompt

You are running after the fixes have landed. For each thread classified `legit` during this run, decide whether the miss is a pattern worth a rule, or a one-off that doesn't need one.

## Input

- All `legit` threads from this run, with their plan entries and reasoning.
- The list of existing rules at `$HOME/.claude/rules/` (file names only, not bodies).
- The "Current global rules:" list in `$HOME/.claude/CLAUDE.md`.

## Decision criteria — rule-worthy miss

At least one of:
1. **Safety-invariant class.** The thread flagged `safety_invariant: true`.
2. **Repeated miss.** The same class of bug has been flagged in a prior PR — search `~/Documents/Obsidian/Awesome Motive/sessions/` for PRs that touched the same file or referenced the same invariant.
3. **Preventable by structure.** The fix moved a check from the caller to the function (gate at function, not caller). That is a class of fix that benefits from a rule.
4. **Cross-codebase applicability.** The fix would apply verbatim in another my employer repo (sibling-product, another-product, etc.).

## Not rule-worthy

- One-file typo, naming nit, local style.
- Behavior specific to a feature that only lives in one module.
- Anything that is already covered by an existing rule — in that case, output a pointer to the rule, not a new draft.

## Output per miss

```json
{
  "thread_id": "<id>",
  "rule_worthy": true | false,
  "existing_rule": "<name of an existing rule that covers this, or null>",
  "proposed_rule_slug": "<kebab-case or null>",
  "proposed_rule_body": "<full markdown body if rule_worthy, else null>"
}
```

Proposed rule body structure (per `creating-rules.md`):

```markdown
---
description: <1 line>
globs: <optional glob pattern>
---

# <Rule Title>

<1-2 paragraph statement of the rule.>

**Why:** <reason, often an incident.>
**How to apply:** <when this guidance kicks in.>
```

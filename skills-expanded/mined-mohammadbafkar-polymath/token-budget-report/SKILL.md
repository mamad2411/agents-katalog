---
name: token-budget-report
description: Check listing-token cost per plugin via claude plugin details; flag over-cap plugins and the heaviest descriptions.
---

# token-budget-report

> Produce a budget table that's good enough to merge a PR against. Output is per-plugin token cost plus the top offenders to trim.

## When to use

- A PR adds or modifies skills/commands and a reviewer wants to confirm the budget impact.
- A scheduled marketplace health check.
- A new plugin needs measurement before it lands.

## Procedure

1. **Identify the marketplace root** (the directory containing `.claude-plugin/marketplace.json`).
2. **Heuristic measurement** — `tools/token-report.py budget`. Fast, no install required. Each plugin's heuristic cost is roughly half the canonical.
3. **Canonical measurement** — for each plugin, `claude plugin details <name>@<marketplace>`. The CLI parses descriptions and computes the listing cost. This is the load-bearing number.
4. **Per-plugin gate**: any plugin > 400 tok is over the cap.
5. **Trim recommendations** — for plugins ≥ 300 tok, surface the longest single description (skill, command, or agent) so the author knows what to cut first.

## Output

```text
Token-budget report — polymath marketplace, <plugin_count> plugins, <date>

Heuristic (tools/token-report.py budget): 3,124 tok
Canonical  (claude plugin details):      5,636 tok
Total target (250 × plugin_count, ≥1500):  7,250 tok      [ok]

Per-plugin (canonical):
  polymath-core                  194
  polymath-product               187
  …
  polymath-kubernetes      345  ← heaviest
  polymath-writing               274  ← second heaviest

Plugins approaching cap (≥ 300 tok):
  polymath-kubernetes  345
    Heaviest description:
      write-manifest (skill)  ~80 tok
    Suggested trim: shorten the safe-defaults enumeration; aim ≤ 60 chars.

Plugins over cap (> 400 tok):
  (none)

Verdict: PASS.
```

## Quality bar

- Canonical numbers come from `claude plugin details`, not the heuristic. The heuristic is informational.
- Trim recommendations name the specific component, not "tighten descriptions".
- "Over cap" verdict produces actionable PR feedback.

## Anti-patterns to avoid

- Reporting only the heuristic.
- Recommending blanket description shortening without naming the culprit.
- Treating the cap as a target instead of a ceiling.

---
name: homelab-research-librarian
description: Researches, evaluates, and documents homelab tooling, self-hosted apps, and infrastructure patterns.
---

# homelab-research-librarian

Investigates homelab tooling options, self-hosted application alternatives, infrastructure patterns, and emerging technologies. Produces structured comparison notes and decision records stored in the Obsidian vault.

## Invocation

**OpenCode / Codex:** `Invoke homelab-research-librarian`
**Freebuff:** `/skill homelab-research-librarian`

## Workflow Steps

1. **Define query:** Clarify what is being researched (tool category, specific app, pattern).
2. **Survey options:** Search for candidates including self-hosted, open-source, and managed options.
3. **Evaluate:** Score each option on: ease of deployment, community support, resource usage, security posture, maintenance burden.
4. **Compare:** Build a side-by-side comparison table.
5. **Recommend:** State the recommended option with rationale.
6. **Document:** Write findings to Obsidian under `Homelab/Research/topic.md`.

## Output Format

```markdown
# Research: <topic>
Date: YYYY-MM-DD
Query: <what was researched>

## Options Considered
| Option | Pros | Cons | Score |

## Recommendation
<recommended option and rationale>

## References
- <link>
```

## Companion Skills

- `obsidian-homelab-logbook` — store research outputs
- `homelab-change-planner` — if research leads to a deployment decision

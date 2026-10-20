# Claude Code Instructions

## Git Commits

- 50 chars title, optional body
- NO "Co-Authored-By: Claude"
- NO emojis
- Format: `type: short description`

## Language

- **User:** Ukrainian
- **Docs/code:** English (saves ~30% tokens)
- **Subagent prompts:** English

## Documentation

**NO ASCII ART.** Allowed: tables, lists, arrows (`→`), directory trees.

## Directory Structure

**Full documentation:** [docs/directory-structure.md](docs/directory-structure.md)

```
~/.claude/                                     # Global framework (faion-network)
├── skills/faion/knowledge/<tier>/<group>/  # Umbrella knowledge (tiers: free, solo, pro, geek)
├── skills/faion-{applied}/                    # Applied tools (brainstorm, /faion, improver, ...)
├── agents/faion-*-agent.md
└── docs/

{project}/                    # Project root
├── .claude/                  # Project-specific config
│   └── {project}-*/         # Project skills (gitignored)
└── aidocs/sdd/{project}/    # SDD documentation
    ├── constitution.md
    ├── features/{status}/{NN}-{feature}/
    └── tasks/{status}/
```

**Lifecycle:** `backlog/ → todo/ → in-progress/ → done/`

## No Time Estimates

**NEVER provide time estimates** for task execution in SDD workflow:

- ❌ "This will take 2 hours"
- ❌ "Estimated duration: 3 days"
- ❌ "Should be done in 30 minutes"
- ✅ "Task complexity: High" (qualitative)
- ✅ "Est. tokens: ~50k" (resource-based)

**Why:** Time estimates are inherently unreliable and create false expectations. Use complexity levels and token estimates instead.

**In SDD documents:**
- `implementation-plan.md` — NO `estimated_duration` field
- `TASK_*.md` — NO time estimates, use token estimates only
- `roadmap.md` — Use phases/milestones, not dates when possible

## Token Efficiency

**Symbols:** `→` leads to | `⇒` transforms | `✅` done | `❌` failed | `⚠️` warning

**Abbrev:** `cfg` config | `impl` impl | `perf` perf | `sec` security | `dep` dependency

## SDD Memory

```
~/.sdd/memory/
├── patterns_learned.jsonl
├── mistakes_learned.jsonl
└── session_context.md
```

## References

- [Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code)
- [Skills](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Sub-agents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)

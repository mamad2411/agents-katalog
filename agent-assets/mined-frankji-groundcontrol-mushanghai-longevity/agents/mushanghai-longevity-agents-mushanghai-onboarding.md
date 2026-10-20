# mushanghai-onboarding/AGENTS.md

> May 12 bootstrap. Three modes: full install, skills plus MCPs plus hypothesis, hypothesis only. See `../AGENTS.md` for family-level conventions.

## Modes

| Letter | Name | Trigger | Primary Output Path |
|---|---|---|---|
| A | Full install | User just walked in and needs Claude Code plus skill packs from scratch. | n/a |
| B | Skills plus MCPs plus hypothesis | User has Claude Code and needs supporting skill packs. | n/a |
| C | Hypothesis only | User has installs and needs seed hypothesis plus cohort or track. | n/a |

## Local Layout

- `SKILL.md` - router, install sections, seed-hypothesis handoff.
- `references/anthropic-client-install.md` - Node, git, Claude Desktop, VS Code extension.
- `references/brainstorming-handoff.md` - superpowers brainstorming invocation.
- `references/cc-switch-install.md` - optional provider switcher notes.
- `references/grill-me-handoff.md` - light alignment interview handoff.
- `references/mattpocock-skills-install.md` - mattpocock skills install.
- `references/search-mcp-install.md` - Tavily and Firecrawl MCP install steps.
- `references/superpowers-install.md` - obra superpowers install.
- `assets/may-12-onboarding-script.md` - 90-minute facilitator agenda.

## Where to Look

| Task | Location | Notes |
|---|---|---|
| Route onboarding state | `SKILL.md` | Lines under Mode router define A, B, C. |
| Run Claude client preflight | `references/anthropic-client-install.md` | Section 1 source. |
| Add live web evidence MCPs | `references/search-mcp-install.md` | Section 2.5, not rogue. |
| Facilitate May 12 live session | `assets/may-12-onboarding-script.md` | Time-blocked agenda. |
| Handoff after seed hypothesis | `SKILL.md` | Section 4 pasteable message. |

## Local Conventions

- Install loop includes all seven muShanghai skills.
- Tavily plus Firecrawl step stays in Section 2.5 unless user explicitly skips live web evidence.
- Proof of Living details come through canon, especially `../mushanghai-canon/references/proof-of-living.md`.

## Anti-Patterns (this skill)

- Skipping Tavily plus Firecrawl when the user wants live evidence research.
- Treating `search-mcp-install.md` as a rogue reference.
- Executing install commands silently instead of showing commands and waiting for confirmation.

## Hand-Offs

- Modes A, B, C end at `mushanghai-experiment-leader` Mode A after cohort, track, and seed hypothesis exist.

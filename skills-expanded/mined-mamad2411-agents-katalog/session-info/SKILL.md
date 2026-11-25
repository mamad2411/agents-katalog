---
name: session-info
description: Get current Claude Code session UUID and registry info. TRIGGERS - current session, session uuid, session id, what session, which session.
allowed-tools: Bash, Read
---

> **Navigation**: [Plugin CLAUDE.md](../../CLAUDE.md) | [Root CLAUDE.md](../../../../CLAUDE.md)

# Session Info Skill

Returns the current Claude Code session UUID and registry information.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## When to Use This Skill

Use this skill when:

- Need to know the current session UUID for debugging
- Want to check the session chain history
- Verify the session registry is working
- Find correlation between sessions and transcripts

## Implementation

Run the session info script:

```bash
bun $HOME/.claude/plugins/marketplaces/cc-skills/plugins/statusline-tools/scripts/get-session-info.ts
```

## Output Format

The script outputs structured session information:

```
Current Session: c1c1c149-1abe-45f3-8572-fd77aa046232
Short ID: c1c1c149
Project: ~/.claude
Registry: ~/.claude/projects/-Users-you--claude/.session-chain-cache.json
Chain Length: 3 session(s)
Last Updated: 2026-01-15T21:30:00.000Z
```

> **Note**: The `Managed By`, `Metadata` (Repo, Hash, Branch, Model, Cost), and `Recent Sessions` sections shown in earlier versions of this doc are **not yet implemented** in `get-session-info.ts`. The script currently outputs only the 6 fields above.

## Registry Location

The session registry follows Claude Code's native path encoding:

```
~/.claude/projects/{encoded-path}/.session-chain-cache.json
```

Where `encoded-path` replaces `/` with `-`:

- `/Users/username/eon/cc-skills` → `-Users-username-eon-cc-skills`

## References

- [Registry Format](./references/registry-format.md) - Schema documentation

---

## Troubleshooting

| Issue                     | Cause                      | Solution                                         |
| ------------------------- | -------------------------- | ------------------------------------------------ |
| Script not found          | Plugin not installed       | Run `claude plugin list` to verify installation  |
| JSONL ID undefined        | No active session          | Start Claude Code session first                  |
| Registry file not found   | First session in project   | Registry created automatically on first session  |
| Chain length is 0         | Fresh project              | Normal for new projects, chain grows over time   |
| Path encoding looks wrong | Special characters in path | Claude Code uses `-` to replace `/` in paths     |
| Bun not found             | Bun not installed          | Install with `brew install oven-sh/bun/bun`      |
| Permission denied         | Registry file permissions  | Check ~/.claude permissions (should be readable) |

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If the underlying tool's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.

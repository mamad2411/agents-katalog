---
name: agent-kit-prompt-cache
description: Make dynamic agents cheaper by keeping their prompt prefixes byte-identical so the prompt cache hits. Use whenever you are about to spawn subagents, forks, parallel agents or a Workflow, run /loop or ScheduleWakeup, or when the user says "save tokens", "prompt caching", "cache hit", "token usage", "ลด token". Builds a fingerprinted, byte-stable project outline locally with uv (no API key, no LLM), generates agent briefs that put that outline first and the task last, and reports per-agent cache hit rate from the local Claude Code session logs.
---

# Prompt Cache Kit

Claude Code already sends prompt caching on every request. A cache hit needs a **byte-identical prefix**, and a hit costs about 0.1× the normal input price, while a write costs about 1.25× (5m TTL) or 2× (1h TTL). Whether dynamic agents get hits depends on how you write their prompts. This skill keeps those prompts identical where it counts.

Idea borrowed from Understand-Anything: do the structural work locally and deterministically, fingerprint files so only changed ones get recomputed, and let agents read the precomputed result instead of re-reading the repo.

Tool: `uv run --script ${CLAUDE_SKILL_DIR}/scripts/pcache.py <cmd>`. It's stdlib only, and uv handles the Python version.

| Command | Does |
|---|---|
| `build [root]` | Hashes git-visible files and re-outlines only the changed ones into `.pcache/context.md`, which comes out byte-stable. |
| `brief "<task>" [--role R] [--rag VAULT]` | Prints the outline, a fixed rules block, then the role and task last. With `--rag`, the vault's hot.md and the notes retrieved for this task go between the rules and the role, after the shared prefix (`../rag`). |
| `stats [session_id] [--logs DIR]` | Shows input, cache write, cache read and hit rate per agent, read from `~/.claude/projects/<cwd>/`. Defaults to the newest session. |
| `--self-test` | Runs the built-in asserts. |

## Rules when running dynamic agents

1. **Before fanning out**, run `build`. It's cheap on later runs because only changed files are re-outlined.
2. **Fresh agents get a `brief` output as their prompt.** Never hand-write the shared part, and never paste a different repo summary into each agent, because one changed byte early on costs the whole prefix.
3. **Use a fork when the agent needs this conversation.** A fork inherits the parent's cached prefix. Use a fresh agent with a brief when it doesn't, which keeps the prefix small and shared across siblings.
4. **Continue an agent with SendMessage instead of spawning a new one.** Its history is already cached.
5. **Keep /loop and ScheduleWakeup delays under 3600s.** Past the 1h TTL, the next turn pays a full cache write again.
6. **Keep the prefix still mid-run.** Don't edit CLAUDE.md, skills or MCP config, and don't switch models, while agents are running.
7. **After the run**, run `stats` and report the TOTAL hit rate in one line. Agents marked `cold` (under 50%) mean their prompt prefix differed. Check rule 2 for them.

`.pcache/` belongs in the target project's `.gitignore`. `build` prints a hint on its first run and never edits the file itself.

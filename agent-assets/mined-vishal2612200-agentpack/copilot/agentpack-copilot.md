# AgentPack

AgentPack makes coding agents start with the right files.

AgentPack is a local context engine, not a coding agent. It prepares ranked repo context; the agent still verifies code, edits, runs checks, and owns correctness.

Before making code changes:

1. Understand the task.
2. Use read-only routing when repo context is unclear:

```bash
agentpack route --task "<task>"
```

3. Build a context pack when fuller context is needed:

```bash
agentpack task set "<task>"
agentpack pack --task auto
```

4. Read `.agentpack/context.md` if it exists.
5. Treat selected files as a starting map, not proof.
6. Use normal repo search when AgentPack output looks incomplete.
7. Prefer the smallest correct diff.
8. Run relevant checks after editing.
9. Use JSON programmatically for configs, storage, hooks, and tool protocols. Use TOON for agent-facing structured context or prompt payloads unless an external contract requires JSON.
10. After completed edits, consider:

```bash
agentpack benchmark capture --since main --task "<task>"
agentpack benchmark --misses
```

Do not upload code, call remote services, or add autonomous agent behavior for AgentPack. Use the local CLI or MCP tools.

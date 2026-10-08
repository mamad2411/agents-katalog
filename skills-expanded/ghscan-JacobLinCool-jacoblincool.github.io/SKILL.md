# Jacob Agent Tools

Use this skill when the task is specifically about Jacob Lin's portfolio, research, publications, projects, GitHub footprint, or Hugging Face footprint, and the caller needs grounded answers from the packaged knowledge base or the packaged live tools.

This is a Jacob-specific interview and portfolio toolset. It is not a general web search skill.

Before using the runtime, build the package from the workspace root:

```bash
pnpm --filter @jacoblincool/agent build
```

Use the built runtime from `scripts/cli.mjs`.

List available tools:

```bash
node scripts/cli.mjs list
```

Execute a tool:

```bash
node scripts/cli.mjs exec get_knowledge_root
node scripts/cli.mjs exec get_knowledge_item --input '{"id":"project-d1-manager"}'
```

Read [references/TOOL-CATALOG.md](references/TOOL-CATALOG.md) for the tool inventory and [references/LOCAL-USAGE.md](references/LOCAL-USAGE.md) for local build and import examples.

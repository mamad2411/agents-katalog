---
name: sandbox-agent-workspace
description: Run an agent inside an isolated sandbox workspace with a manifest-defined filesystem using SandboxAgent.
category: agents
version: 1.0.0
version_origin: extracted
confidence: high
tags: [openai-agents, sandbox, workspace, files, git-repo]
source_type: extracted-from-git
source_url: https://github.com/openai/openai-agents-python.git
source_ref: main
source_commit: e80d2d2319eb300ac17ec496988b70246a5042d6
source_project: openai-agents-python
source_path: README.md
imported_at: 2026-04-18T00:00:00Z
---

# sandbox-agent-workspace

Use `SandboxAgent` with a `Manifest` to define a workspace (git repos, local files, URLs) that the agent can inspect and modify. Run with `SandboxRunConfig` specifying the sandbox client.

## When to apply

Long-horizon tasks that need a real filesystem: inspecting repos, editing code, running shell commands, applying patches. Available from SDK version 0.14.0+.

## Core snippet

```python
import asyncio
from agents import Runner
from agents.run import RunConfig
from agents.sandbox import Manifest, SandboxAgent, SandboxRunConfig
from agents.sandbox.entries import GitRepo
from agents.sandbox.sandboxes import UnixLocalSandboxClient

agent = SandboxAgent(
    name="Workspace Assistant",
    instructions="Inspect the sandbox workspace before answering.",
    default_manifest=Manifest(
        entries={
            "repo": GitRepo(repo="openai/openai-agents-python", ref="main"),
        }
    ),
)

async def main():
    result = await Runner.run(
        agent,
        "Inspect the repo README and summarize what this project does.",
        run_config=RunConfig(
            sandbox=SandboxRunConfig(client=UnixLocalSandboxClient())
        ),
    )
    print(result.final_output)

asyncio.run(main())
```

## Key notes

- `SandboxAgent` extends `Agent` with `default_manifest`, `base_instructions`, `capabilities`, `run_as`
- `Manifest.entries` maps names to `GitRepo`, `LocalDir`, `LocalFile`, `RemoteFile` etc.
- `UnixLocalSandboxClient` uses the local filesystem; other clients can use Docker or remote environments
- `SandboxRunConfig` is nested inside `RunConfig(sandbox=...)`
- The agent has access to `ApplyPatchTool`, `ShellTool`, and other workspace-native tools

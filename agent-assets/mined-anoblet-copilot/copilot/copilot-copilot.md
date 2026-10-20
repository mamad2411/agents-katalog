[AGENTS.md](../AGENTS.md)

<role>
</role>

<tools>
- [agent.instructions.md](../copilot/.github/instructions/tools/agent.instructions.md)
</tools>

<instructions>
- [css.instructions.md](../copilot/.github/instructions/css.instructions.md)
- [copilot.instructions.md](../copilot/.github/instructions/copilot.instructions.md)
- [git.instructions.md](../copilot/.github/instructions/git.instructions.md)
- [node.instructions.md](../copilot/.github/instructions/node.instructions.md)
- [principles.instructions.md](../copilot/.github/instructions/principles.instructions.md)
- [time.instructions.md](../copilot/.github/instructions/time.instructions.md)
- [typescript.instructions.md](../copilot/.github/instructions/typescript.instructions.md)
- [web-component.instructions.md](../copilot/.github/instructions/web-component.instructions.md)
</instructions>

<constraints>
- Do not modify the git history. Do not checkout or restore any file. Do not commit any changes. If the git state is not clean, assume that any uncommitted changes are intentional.
- Ignore the git state of the [copilot](../copilot) directory.
- Ignore submodules unless explicitly told to reference or modify them.
- Use Typescript whenever possible.
- Node packages should be managed with pnpm.
- Node packages should be scoped to the `@anoblet` namespace.
- Always prefer Typescript over Python.
- Terminal
  - Do not use the `sleep` command
    - Patiently wait for the terminal process to complete and return output before proceeding.
    - If a command is taking a long time, wait for it to complete instead of trying to interrupt it or run other commands in the meantime.
- When considering unintentional, untracked, or manual changes that have been made outside of the users request, before, during, or after the request has been processed, under no circumstance should those changes be undone, reverted, or restored to their previous state by any means.

Instead:

1. Pause the current task
2. Identify the entirety of the manual and/or unintended changes
3. Assess the relationship between the identified changes and the current task
4. If there are no conflicting instructions, incorporate the changes into the current task and document them for future review
5. If there are conflicting instructions, document the conflict and request clarification from the user on how to proceed without undoing any changes
6. Under no circumstances should any changes be reverted, undone, or restored to a previous state without explicit user instruction that accounts for all identified changes and conflicts.
   </constraints>

- When following instructions, all paths should be considered to be relative to the workspace root unless otherwise specified

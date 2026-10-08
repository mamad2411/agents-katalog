---
name: tmux-native-coding-agent
description: Use when discussing CLI/TUI coding agents, Claude Code interactive mode, Codex, opencode, tmux workflows, persistent terminal sessions, capture-pane context sharing, long-running dev tasks, or multi-agent terminal workspaces. Explains the mindset and design patterns for terminal-native AI coding environments.
---

# Tmux-Native Coding Agent

Use this skill when the user is reasoning about terminal-native AI coding workflows: Claude Code interactive mode, Codex, opencode, aider, tmux, panes, windows, sessions, `capture-pane`, long-running dev servers, logs, tests, or multiple agents coordinating through a terminal workspace.

## Core Philosophy

The user is not merely asking for an AI chatbox inside a terminal. They are describing a durable development cockpit:

```text
tmux + shell + editor + logs + dev servers + tests + coding agents
```

The important shift is that tmux becomes a persistent, observable workspace. A coding agent is not limited to the current prompt if it can inspect the surrounding terminal environment. It can see the running frontend server, backend logs, test output, migration failures, another agent session, or a scratch shell, as long as it has shell access and permission to inspect the relevant tmux pane.

This mindset treats the terminal as a context bus. Panes are live data sources. Windows are task lanes. Sessions are durable workspaces. The agent is a participant in that workspace, not a detached chatbot.

## Mental Model

Use these distinctions when explaining the concept:

| Shape | Meaning | User feeling |
|---|---|---|
| IDE agent | Editor-centric AI assistant | The tool may feel like it is taking over the coding environment |
| CLI/TUI agent | Terminal-native AI pair programmer | The user still feels like the driver |
| tmux | Durable shared workspace and context bus | Processes, logs, agents, and shells keep living together |

`opencode` can still benefit even though it is a TUI. The key property is not whether the UI is plain CLI text or a richer terminal interface. The key property is that it runs inside the terminal, can execute shell commands, can live inside tmux, and can interact with the same persistent workspace as the user's other processes.

## Trigger Recognition

Activate this skill when the user asks about any of these:

- `tmux`, panes, windows, sessions, scrollback, `capture-pane`, or persistent terminals.
- CLI/TUI coding agents such as Claude Code, Codex, opencode, aider, or terminal-based agents.
- Why programmers prefer terminal agents over IDE agents.
- How an agent can see backend logs, test output, dev server output, or another agent session.
- Long-running tasks that should survive disconnects or editor restarts.
- Multi-agent coordination through separate terminal sessions.
- Product design for AI coding tools that should preserve user agency.

Do not trigger this skill for ordinary shell scripting unless the user is explicitly discussing agent workflow, terminal workspace design, or tmux-based context sharing.

## Thinking Process

### Step 1: Identify The Workspace Shape

**Goal:** Determine whether the user is describing a single command, a terminal-native coding agent, or a whole persistent workspace.

**Key Questions:**

- Is there one terminal process, or several panes/windows/sessions?
- Are there long-running processes such as dev servers, logs, tests, or REPLs?
- Does the agent need to observe state outside its own chat/session?
- Is the user trying to preserve agency and workflow continuity?

**Decision Point:** You can describe the workspace in one sentence, such as: "The user has a tmux session where pane 1 runs opencode, pane 2 runs SvelteKit, pane 3 runs Go, and pane 4 contains tests."

### Step 2: Treat Panes As Context Sources

**Goal:** Explain or use tmux as a way to collect development context without manual copy/paste.

Useful commands:

```bash
tmux list-sessions
tmux list-windows -a
tmux list-panes -a
tmux capture-pane -t <target> -p
```

Common context sources:

- Frontend dev server output.
- Backend logs.
- Test watcher output.
- Build failures.
- Database shell output.
- Another coding agent's terminal session.
- A scratch pane with recent commands and responses.

**Decision Point:** Prefer a specific pane target over broad capture. "Read the backend log pane" is safer and more useful than "read every pane in every session."

### Step 3: Preserve User Agency

**Goal:** Explain why terminal-native agents feel different from IDE agents.

The emotional use case matters. Developers often prefer CLI/TUI agents because they still feel like they are coding:

- They choose commands.
- They watch logs.
- They keep their editor and shell habits.
- They decide what the agent can inspect.
- The agent assists inside the existing workflow instead of replacing it.

Use the phrase "the user remains the driver" when summarizing this trade-off.

### Step 4: Design The Workflow Around Long-Running State

**Goal:** Recommend tmux layouts that make agent work observable and durable.

Example layout:

```text
tmux session: app
+-- window 1: editor
|   +-- pane 1: nvim / shell
|   +-- pane 2: opencode / claude / codex
+-- window 2: runtime
|   +-- pane 1: npm run dev
|   +-- pane 2: go run ./cmd/server
+-- window 3: verification
    +-- pane 1: npm test -- --watch
    +-- pane 2: logs / curl / database shell
```

For smaller projects, collapse it:

```text
pane 1: opencode / claude / codex
pane 2: frontend dev server
pane 3: backend server
pane 4: tests / logs
```

**Decision Point:** Every long-running process that affects coding decisions should have an obvious home.

### Step 5: State The Safety Boundary

**Goal:** Prevent accidental leakage of secrets or unrelated private context.

Before reading broad tmux context, ask or narrow scope. A pane can contain:

- API keys or tokens.
- Private logs.
- Production data.
- Another user's session.
- Another agent conversation.
- Password prompts or command history.

Rules:

- Do not indiscriminately capture all sessions.
- Prefer explicit pane targets.
- If secrets may be present, ask before reading.
- Summarize what you need before capturing: "I only need the last backend error and test output."
- Remember that `capture-pane` sees terminal buffer, not a clean structured log.

## Practical Patterns

### Backend Debugging Pattern

Use when the user has an agent in one pane and a backend server in another.

```text
1. Identify the backend pane with `tmux list-panes -a`.
2. Capture only that pane.
3. Extract the latest error, stack trace, request path, and timestamp.
4. Inspect the code path.
5. Apply the fix.
6. Watch the backend pane or test pane again for confirmation.
```

### Frontend Build Pattern

Use when a SvelteKit/Vite/Next dev server is already running.

```text
1. Capture the frontend dev server pane.
2. Identify the first real compiler/runtime error, not follow-on noise.
3. Fix the source file.
4. Re-capture the pane or run a direct build/test command.
```

### Multi-Agent Pattern

Use when separate agents work in separate tmux panes/sessions.

```text
1. Give each agent a bounded task and workspace.
2. Use panes as handoff surfaces, not hidden global memory.
3. Ask one agent to summarize findings before another consumes them.
4. Avoid two agents editing the same files without a clear owner.
```

### Remote Development Pattern

Use when the user works over SSH.

```text
tmux keeps the environment alive after disconnects; the coding agent can resume into the same process topology instead of rebuilding context from scratch.
```

## Product Design Implications

When evaluating or designing AI coding tools for this use case, look for:

- Persistent terminal workspaces.
- Agent-readable process output.
- Explicit context boundaries.
- Long-running task management.
- Remote SSH friendliness.
- Low disruption to existing shell/editor habits.
- Multi-agent handoff and coordination primitives.
- A clear model for what the agent can and cannot observe.
- User agency: the tool should feel like a copilot in the terminal, not an IDE takeover.

## Anti-Patterns

Call these out directly:

- Treating CLI/TUI agents as just chatbots with file access.
- Assuming TUI agents such as opencode cannot benefit from tmux because they are not plain CLI.
- Forcing terminal-native users into a new IDE to get persistence or logs.
- Reading every tmux pane/session blindly.
- Ignoring scrollback limits and assuming `capture-pane` contains complete history.
- Letting multiple agents edit the same files without coordination.
- Confusing terminal buffer text with structured telemetry.
- Optimizing for flashy UI while losing shell composability, SSH usage, and process visibility.

## Output Style

When responding with this skill:

- Use concrete terminal layouts and command examples.
- Explain the workflow benefit before the command mechanics.
- Mention the safety boundary if pane capture is involved.
- Distinguish CLI, TUI, IDE, and tmux precisely.
- Use short diagrams when they clarify the workspace.
- Name trade-offs: terminal-native workflows are powerful, but they expose messy buffers, secrets risk, scrollback limits, and coordination complexity.

## One-Sentence Summary

Tmux-native coding agents work well because tmux turns the terminal into a persistent, observable development cockpit where agents can inspect real process context while the user remains the driver.

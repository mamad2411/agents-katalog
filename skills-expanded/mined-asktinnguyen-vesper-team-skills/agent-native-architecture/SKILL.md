---
name: agent-native-architecture
description: Build applications where agents are first-class citizens. Use this skill when designing autonomous agents, creating MCP tools, implementing self-modifying systems, or building apps where features are outcomes achieved by agents operating in a loop.
---

# Core Principles

## 1. Parity
**Whatever the user can do through the UI, the agent should be able to achieve through tools.**

If users can create, tag, and delete notes through the UI, the agent needs tools to do the same. Without parity, the agent gets stuck on common requests.

Test: Pick any UI action. Can the agent achieve that outcome? If not, add the necessary tools.

---

## 2. Granularity
**Prefer atomic primitives. Features are outcomes achieved by agents operating in a loop.**

❌ Bad: `classify_and_organize_files(files)` — You wrote the logic, agent executes
✓ Good: `read_file`, `write_file`, `move_file` — Agent decides how to organize

Tools encode capability. Features are described in prompts. To change behavior, you edit prompts, not code.

---

## 3. Composability
**With atomic tools and parity, you can add new features by writing new prompts.**

No new code needed. A "weekly review" feature is just a prompt:
```
"Review files modified this week. Summarize key changes. Suggest three priorities."
```

The agent uses `list_files`, `read_file`, and judgment to accomplish this.

---

## 4. Emergent Capability
**The agent can accomplish things you didn't explicitly design for.**

Users will ask for things you never anticipated. If tools are atomic and the agent has parity with users, it often figures it out.

*"Cross-reference my meeting notes with my task list and tell me what I've committed to but haven't scheduled."*

You didn't build this feature. But if the agent can read notes and tasks, it can compose a solution.

---

## 5. Improvement Over Time
**Agent-native applications get better without code changes.**

- Accumulated context: Agent reads/updates a `context.md` file with knowledge across sessions
- Prompt refinement: Update behavior by editing prompts (developer-level or user-level)
- Self-modification: Advanced—agents modify their own prompts based on feedback (with safety rails)

---

# Essential Checklist

Before building, verify:

### Parity & Tools
- [ ] Every UI action has a corresponding agent capability
- [ ] Tools are primitives (read, write, move, delete), not workflows
- [ ] Every entity has full CRUD (Create, Read, Update, Delete)
- [ ] Tools document what they do in user vocabulary, not technical jargon

### Execution
- [ ] Agent has explicit `complete_task` tool (not heuristic detection)
- [ ] Multi-step tasks can be resumed (checkpoint/progress tracking)
- [ ] System prompt includes context about what exists and what agent can do

### Workspace & UI
- [ ] Agent and user work in the same data space
- [ ] Agent actions immediately reflect in UI (shared file store, event bus, or observation)
- [ ] Agent has access to `context.md` for accumulated knowledge

### Avoid Bundling Logic
- [ ] No tools like `analyze_and_organize`—break into primitives
- [ ] No validation gates unless there's a specific safety reason
- [ ] No "workflow-shaped" tools that encode your decision logic

---

# Anti-Patterns

**Agent executes your code instead of figuring things out**
```
❌ tool("process_feedback", { decide category, priority, notify })
✓ tools: store_item, send_message + prompt: "rate importance 1-5, store, notify if >=4"
```

**Incomplete CRUD** — Agent can create but not update/delete. Every entity needs full CRUD.

**Context starvation** — Agent doesn't know what resources exist.
```
User: "Write something about Catherine the Great in my feed"
Agent: "What feed? I don't understand what system you're referring to."
```
Fix: Inject available resources into system prompt.

**Orphan UI actions** — User can do something through UI that agent can't. Maintain parity.

**Silent actions** — Agent changes state but UI doesn't update. Use shared data stores with reactive binding.

**Static tool mapping for dynamic APIs** — 50 tools for 50 endpoints instead of dynamic discovery.
```
❌ tool("read_steps"), tool("read_heart_rate"), tool("read_sleep")
✓ tool("list_available_data_types"), tool("read_health_data", { dataType: string })
```

**Sandbox isolation** — Agent works in separate data space from user. Use shared workspace.

---

# Quick Start

**Step 1: Define atomic tools**
```typescript
const tools = [
  tool("read_file", "Read any file", { path: z.string() }, ...),
  tool("write_file", "Write any file", { path: z.string(), content: z.string() }, ...),
  tool("list_files", "List directory", { path: z.string() }, ...),
  tool("complete_task", "Signal task completion", { summary: z.string() }, ...),
];
```

**Step 2: Write behavior in system prompt**
```markdown
## Your Responsibilities
When asked to organize content, you should:
1. Read existing files to understand the structure
2. Analyze what organization makes sense
3. Create/move files using your tools
4. Use your judgment about layout and formatting
5. Call complete_task when you're done

You decide the structure. Make it good.
```

**Step 3: Let the agent work in a loop**
```typescript
const result = await agent.run({
  prompt: userMessage,
  tools: tools,
  systemPrompt: systemPrompt,
});
```

---

# Success Criteria

You've built an agent-native application when:

- [ ] Agent has parity with user UI (every action is possible through tools)
- [ ] Tools are atomic; features are described in prompts
- [ ] New features can be added by writing new prompts
- [ ] Agent can accomplish unanticipated requests in your domain
- [ ] Agent and user work in same data space
- [ ] Agent actions immediately reflect in UI
- [ ] Every entity has full CRUD
- [ ] Agents explicitly signal completion
- [ ] Changing behavior means editing prompts, not refactoring code

### The Ultimate Test
Describe an outcome to the agent that's within your domain but you didn't build a specific feature for. Can it figure it out?

If yes, you've built something agent-native.
If it says "I don't have a feature for that"—your architecture is still too constrained.

---

# Pattern Reference

When designing agent-native systems, apply these patterns:

- **Parity discipline**: Every UI action → agent capability mapping
- **Tool design**: Atomic primitives, dynamic discovery for APIs, complete CRUD
- **System prompts**: Define behavior through outcome descriptions, not choreography
- **Workspace architecture**: Shared data space, file-based state, context.md for accumulated knowledge
- **Execution models**: Explicit completion signals, checkpoint/resume for long tasks
- **Context injection**: Runtime app state and capability discovery in system prompt
- **UI integration**: Reactive binding to shared files or event-based synchronization
- **Self-modification**: Git-based evolution with safety rails (approval gates, checkpoints, health checks)

Ask about any of these patterns for deeper guidance.

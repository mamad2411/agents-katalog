---
name: context-engineering
description: Optimize agent context setup for maximum performance, accuracy, and cost-efficiency across long sessions and complex tasks.
---

# Context Engineering

## Overview

Context engineering is the practice of deliberately structuring, packing, and budgeting the information an agent consumes. Without it, agents suffer from context window pollution, recency bias, token waste, and degraded reasoning over long sessions. This skill provides a systematic framework for maximizing the signal-to-noise ratio in every interaction.

A well-engineered context reduces token consumption by 40-60%, improves answer accuracy by 30-50%, and enables agents to maintain coherent reasoning across sessions that would otherwise exceed context limits.

## When to Use

- Starting a new agent session or project
- Agent output quality degrades mid-session
- Switching between unrelated tasks in the same session
- Working with large codebases (>10K files)
- Configuring rules files (e.g., AGENTS.md, CLAUDE.md, .cursorrules)
- Setting up MCP server configurations
- When token costs are a concern
- Before any complex multi-step reasoning task
- When context window limits are approaching (~70%+ capacity)

## Process

### Step 1: Context Budget Planning

Before any work, establish your context budget:

1. **Calculate available tokens**: Know your model's limit (e.g., 200K for Claude Opus, 128K for GPT-4o, 1M for Gemini 1.5 Pro).
2. **Allocate by priority**:
   - System prompt / instructions: 15-20%
   - Rules files: 10-15%
   - Current task data: 40-50%
   - Reference material: 15-20%
   - Output buffer: 5-10%
3. **Set a hard limit**: Never exceed 80% of the context window to leave room for reasoning and output.

### Step 2: Session Initialization Pattern

Always initialize sessions with this structured preamble:

```
[ROLE]
You are an expert {domain} engineer. You follow {project} conventions strictly.

[CONTEXT]
- Project: {name}
- Stack: {languages, frameworks, tools}
- Current phase: {phase description}
- Working directory: {path}

[RULES]
- Read files before editing them
- Verify solutions with tests
- Never introduce breaking changes without approval
- {project-specific rules}

[GOAL]
{clear statement of what this session should accomplish}
```

### Step 3: Rules File Architecture

Rules files (AGENTS.md, CLAUDE.md, .cursorrules, etc.) must follow a layered architecture:

**Layer 1 - Universal Rules** (apply to all projects):
- Read before write
- Verify with tests
- No placeholder code
- Flag security concerns
- Consult docs before writing code

**Layer 2 - Project Rules** (`AGENTS.md` at repo root):
- Tech stack and conventions
- Testing framework and commands
- Build and lint commands
- Deployment targets
- Code review requirements

**Layer 3 - Task-Specific Rules** (injected per task):
- Specific constraints for this feature
- Files to avoid modifying
- Stakeholder requirements
- Performance budgets

Each layer should fit in under 200 lines. Layers compose: Layer 3 > Layer 2 > Layer 1 in priority if conflicts arise.

### Step 4: Context Packing Strategies

**4a. Tree-Based Summarization**

When context windows fill, use structured summarization:

```
Previous context summary:
- Files modified: src/auth/login.tsx, src/auth/hooks.ts
- Decisions made: Chose JWT over session auth for mobile compat
- Open questions: Token refresh strategy TBD
- Rejected approaches: OAuth implicit flow (security audit failed)
```

**4b. Tiered File Loading**

Never load entire files unless necessary:

```
Tier 1 (always load): AGENTS.md, current task file, test file
Tier 2 (on demand): Related modules, type definitions
Tier 3 (reference): Documentation, examples, generated files
```

**4c. Dependency Cartography**

Before loading files, map the dependency graph:
```
Component → imports → imports → ...
```
Only load the minimal set needed for the task.

### Step 5: MCP Integration Configuration

MCP servers consume context budget. Configure them deliberately:

1. **Audit all MCP servers**: List every installed server and its purpose.
2. **Categorize**:
   - Always-on: Filesystem, Git (low overhead, high value)
   - On-demand: Database, Cloud APIs, External APIs
   - Task-specific: Web scraping, Image generation, Email
3. **Disable unused servers**: Each unused MCP server wastes ~500-2000 tokens on initialization.
4. **Structure tool descriptions**: Keep descriptions under 100 characters. Long descriptions bloat system prompts.
5. **Prefer read-only tools**: Write tools carry higher risk. Gate them behind approval flows.

### Step 6: Chunking for Long Conversations

When conversations exceed 50 exchanges or 60% context capacity:

1. **Take a session snapshot**:
   ```
   ---SESSION SNAPSHOT---
   Completed: feature-x implementation, tests added, linted
   In progress: feature-y, blocked on API review
   Decisions: [list key decisions with rationale]
   Next: continue with feature-y once API is approved
   ---END SNAPSHOT---
   ```

2. **Start fresh session**: Paste the snapshot as the opening context.

3. **Include only essential history**: Summarize rather than quote. Keep snapshots under 1000 tokens.

4. **Preserve decisions**: Always include the "why" behind decisions. Future sessions need rationale more than results.

### Step 7: Context Quality Verification

Before proceeding with any task, verify context quality:

- [ ] Rules files loaded and applied
- [ ] Project structure understood
- [ ] All referenced files exist and are current
- [ ] No conflicting instructions in context
- [ ] Token usage within budget
- [ ] MCP servers configured correctly
- [ ] Session initialization complete
- [ ] Previous decisions preserved (if continuing)

## Anti-Rationalization Table

| Excuse | Rebuttal |
|--------|----------|
| "My session is fine, I don't need to engineer context" | Degradation is gradual and invisible. By the time you notice, you've already wasted 30%+ of your context on noise. Measure, don't guess. |
| "Rules files are over-engineering for my small project" | Even a 10-line AGENTS.md prevents the agent from making incorrect assumptions about your stack. The cost: 30 seconds. The benefit: hours of rework avoided. |
| "I'll just add more context as needed" | This is the #1 cause of context pollution. Each addition increases noise for everything already there. Prune before you add. |
| "My model has a huge context window, I don't need to worry" | Larger windows mask but don't solve the problem. Retrieval accuracy degrades in the middle of context regardless of size (the "lost in the middle" effect). |
| "Summarization loses important details" | Poor summarization does. Structured snapshots (decisions, open questions, next steps) preserve critical information while discarding verbatim transcripts. |
| "I'll just reload files when I need them" | Reloading costs tokens too. Worse, it misses the dependency context -- you might not know what you need until you've already formed the wrong mental model. |

## Red Flags

- **Same error occurs across multiple sessions**: Context initialization is incomplete or rules aren't being applied
- **Agent asks "what file should I modify"**: Rules files haven't loaded properly
- **Token usage spikes for no apparent reason**: Check for MCP server bloat or redundant file loading
- **Agent contradicts itself mid-session**: Context pollution or conflicting instructions
- **Agent writes code that doesn't match project conventions**: Rules files not being respected
- **Session exceeds 100 messages without a snapshot**: Critical information is being lost
- **Agent repeatedly reads the same files**: Dependency cartography not performed

## Verification

- [ ] Test: Start a new session and verify the agent loads and follows AGENTS.md
- [ ] Test: Inject a conflicting instruction and verify the correct priority order
- [ ] Test: Run a 50-exchange task and measure token consumption against baseline
- [ ] Test: Create a session snapshot and verify a new session can continue seamlessly
- [ ] Test: Enable/disable MCP servers and measure system prompt token difference
- [ ] Test: Load a large file and verify only relevant sections are read (not the entire file)
- [ ] Metric: Track "waste tokens" (tokens consumed by content never referenced during the session)
- [ ] Metric: Measure "correction rate" -- how often does the agent self-correct based on context?

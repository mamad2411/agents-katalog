# Windsurf Rules: Afk Ai Agent Orchestration With Sandcastle
Description: A comprehensive skill for setting up and managing autonomous AI coding agents using Sandcastle, a TypeScript library for orchestrating AI agents in isolated sandboxes.

# AFK Agent Orchestration with Sandcastle

## Overview
This skill enables you to setup autonomous AI coding agents that work in parallel while maintaining safety through sandboxing. Key components include:
- Isolated execution via Docker ([Core Concepts](references/core_concepts.md))
- GitHub issue-driven workflow
- Multi-stage review process

## Step-by-Step Workflow
1. **Initialize Environment**
   - Follow the [Practical Guide](references/practical_guide.md) to install and configure Sandcastle
   - Set up authentication tokens

2. **Create Work Items**
   - Add GitHub issues with the 'Sandcastle' label
   - Example: "Implement TypeScript CLI with Vitest"

3. **Run Orchestration**
   ```bash
   npm run sandcastle
   ```
   This triggers:
   - Planner agent scans issues
   - Implementers work in parallel branches
   - Reviewers validate changes
   - Merger handles final integration

4. **Monitor Progress**
   - Check agent-specific logs via control-click
   - Verify intermediate branches

## Code Templates
See [Code Examples](references/code_examples.md) for:
- Main orchestration logic
- Dynamic prompt templates
- Parallel execution patterns

## Best Practices
1. Always use sandboxes - unsandboxed agents can cause catastrophic damage
2. Implement the review workflow - catches 80% of implementation errors
3. Monitor context window usage - prevents incomplete task processing
4. Use constrained output formats (XML/JSON) for reliable parsing

## Validation
1. Check final merged code:
   - Tests pass
   - Type checking succeeds
   - Meets coding standards
2. Review GitHub issue closure comments
3. Verify no residual branches or sandbox artifacts

For complete troubleshooting, see [Common Pitfalls](references/pitfalls.md).

## Reference Material

### Code Examples

# Code Examples and Templates

## Basic Orchestration Snippet
```typescript
// From .sandcastle/main.mts
import { run } from '@aihero/sandcastle';

// Planner agent
const plan = await run({
  name: 'planner',
  agent: 'claude-code',
  sandbox: 'docker',
  prompt: 'plan.md', // Contains GitHub issue processing logic
});

// Extract issues from plan output
const { issues } = JSON.parse(
  plan.match(/<plan>([\s\S]*?)<\/plan>/)[1]
);

// Parallel implementation
await Promise.all(issues.map(async (issue) => {
  const implementation = await run({
    name: `implementer-${issue.id}`,
    agent: 'claude-code',
    sandbox: 'docker',
    prompt: 'implement.md',
    promptArgs: {
      issueTitle: issue.title,
      taskId: issue.id
    }
  });

  // Reviewer workflow
  if (implementation.commits.length > 1) {
    await run({
      name: `reviewer-${issue.id}`,
      agent: 'claude-code',
      sandbox: 'docker',
      prompt: 'review.md',
      promptArgs: {
        sourceBranch: 'main',
        branch: implementation.branch
      }
    });
  }
}));
```

## Dynamic Prompt Example (review.md)
```markdown
Analyze this code change:

!```git diff {{sourceBranch}} {{branch}}```

Coding Standards:
1. Use TypeScript strict mode
2. All functions under 50 lines
3. 100% test coverage for new features
4. JSDoc comments for public APIs

Output format:
<analysis>
  <correctness>...</correctness>
  <improvements>...</improvements>
</analysis>
```

### Core Concepts

# Core Concepts of AFK Agent Orchestration

## Sandboxing
Sandboxing is crucial for running AI agents autonomously without risking system damage or data exfiltration. Sandcastle provides isolated environments where agents can execute code safely. The transcript emphasizes Docker as the primary sandbox solution, though you can implement custom sandboxes.

## Parallel Processing
Multiple agents can run simultaneously to handle different tasks. The example shows planner, implementer, reviewer, and merger agents working in parallel. This requires careful orchestration to manage context and avoid conflicts.

## Backlog Management
GitHub Issues serve as the task queue with a dedicated 'Sandcastle' label filtering work items. Each issue becomes an atomic unit of work that agents process independently.

## Review Workflow
The transcript highlights a red-green-refactor pattern where:
1. Implementer creates initial code
2. Reviewer analyzes quality
3. Merger handles integration
This creates a safety net against faulty implementations.

## Prompt Engineering
Prompts use special syntax like exclamation-mark-prefixed code blocks that execute during resolution (e.g., !```git diff```). This enables dynamic prompt content based on repository state.

### Pitfalls

# Common Pitfalls and Solutions

## Permission Management
**Problem:** Agents making dangerous system changes
**Solution:** Always use sandboxes. The transcript warns about agents deleting home directories when run unsandboxed.

## Resource Contention
**Problem:** Parallel agents conflicting on shared resources
**Solution:** Use separate branches per task. The example shows each implementer works on its own branch.

## Infinite Loops
**Problem:** Agents getting stuck in recursive tasks
**Solution:** Set timeouts in Sandcastle.run() and monitor context window usage (shown in planner logs).

## Prompt Injection
**Problem:** Malicious issue content affecting agent behavior
**Solution:** Sanitize GitHub issue inputs and use constrained output formats (like the <plan> XML tags).

## Merge Conflicts
**Problem:** Parallel changes causing integration issues
**Solution:** Use a dedicated merger agent with conflict resolution skills, as demonstrated in the transcript.

## API Limitations
**Problem:** Anthropic's restrictions on subscription usage
**Solution:** Follow the latest guidelines from their API docs or use API keys instead of subscriptions.

## Log Management
**Problem:** Losing track of parallel agent activities
**Solution:** Use the built-in logging system and control-click links to inspect individual agent sessions.

### Practical Guide

# Practical Implementation Guide

## Environment Setup
1. Install Sandcastle: `npm install @aihero/sandcastle`
2. Initialize configuration: `npx sandcastle init`
   - Select agent (Claude Code recommended)
   - Choose sandbox (Docker)
   - Select backlog manager (GitHub Issues)
   - Pick template (Parallel Planner with Review)

## Docker Configuration
The generated Dockerfile includes:
- System dependencies
- GitHub CLI
- Home directory setup
- Agent installation
Build with: `docker build -t sandcastle-agent .`

## Authentication
Set these in `.sandcastle/.env`:
```
ANTHROPIC_API_KEY=your_key
GITHUB_TOKEN=your_token
```

## Workflow Customization
Modify these key files:
1. `.sandcastle/main.mts` - Main orchestration logic
2. `.sandcastle/prompts/plan.md` - Planner prompt template
3. `.sandcastle/prompts/implement.md` - Implementation prompt
4. `.sandcastle/prompts/review.md` - Code review criteria

## Execution
Add to package.json:
```json
"scripts": {
  "sandcastle": "npx tsx .sandcastle/main.mts"
}
```
Run with: `npm run sandcastle`

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[I Open-Sourced My Own AFK Software Factory](https://www.youtube.com/watch?v=E5-QK3CDVQM)** by Matt Pocock
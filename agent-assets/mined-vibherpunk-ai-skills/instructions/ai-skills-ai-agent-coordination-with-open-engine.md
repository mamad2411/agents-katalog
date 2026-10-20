# Copilot Instructions: Ai Agent Coordination With Open Engine
Description: A skill for coordinating multiple AI agents (Claude, ChatGPT, Codex, etc.) using Open Engine's queue-based system to eliminate manual handoffs and context switching between tools.

# AI Agent Coordination Skill

## Overview
Open Engine solves the critical bottleneck in multi-agent workflows by implementing a queue-based coordination system. Instead of humans manually transferring context between Claude, ChatGPT, Codex, and other tools, work moves through a centralized ticketing system where:
- **Agents** can claim tasks
- **Context** stays attached
- **Statuses** are automatically updated
- **Handoffs** are auditable

Key benefits ([Core Concepts](references/core_concepts.md)):
- Eliminates copy-paste between tools
- Maintains full context chain
- Allows cross-agent delegation
- Provides visibility for humans

## Step-by-Step Workflow

### 1. System Setup
1. Choose a queue system ([Practical Guide](references/practical_guide.md)):
   - Recommended: Linear (free tier)
   - Alternatives: Jira, Trello, custom solution
2. Configure standard labels:
   - `agent-instructions`
   - `needs-input`
   - `agent-done`

### 2. Agent Onboarding
For each AI tool (Claude/Codex/etc.):
1. Install the [Agent Setup Prompt](references/code_examples.md)
2. Test with smoke test ticket
3. Verify can:
   - Claim tasks
   - Move statuses
   - Attach outputs

### 3. Task Creation
Use template ([Code Examples](references/code_examples.md)):
```markdown
**Title**: Draft client proposal

**Background**:
- Client needs e-commerce site
- Budget: $50K
- Timeline: 3 months

**Constraints**:
- Use brand guidelines (attached)
- No technical jargon

**Definition of Done**:
- 1-page summary
- 3 key deliverables listed
- Flagged for legal review
```

### 4. Execution Flow
1. Agent detects new `agent-instructions` task
2. Claims ticket (moves to 'Agent Working')
3. Completes work using attached context
4. If blocked:
   - Moves to 'needs-input'
   - Asks specific question
5. When done:
   - Attaches all outputs
   - Moves to 'Agent Done'
   - Notes next steps

### 5. Cross-Agent Handoff
Example: Codex → Claude
1. Codex creates new ticket:
   - Assigns to Claude
   - Includes design specs
   - Labels `agent-instructions`
2. Claude picks up automatically

## Best Practices
1. **Ticket Hygiene** ([Common Pitfalls](references/common_pitfalls.md)):
   - One discrete action per ticket
   - Always include "Definition of Done"
2. **Context Management**:
   - Attach ALL source files
   - Never reference external chats
3. **Status Discipline**:
   - Enforce state transitions
   - Timeout stale tickets

## Validation
1. **Smoke Test** ([Code Examples](references/code_examples.md)):
   - Create "Say hello" ticket
   - Verify full agent loop
2. **Audit Checks**:
   - No context missing between steps
   - All decisions traceable
   - No silent failures

## Advanced Patterns
1. **Household Mode**:
   - Coordinate family schedules
   - Shared task visibility
2. **Team Scale**:
   - Agent-to-agent delegation
   - Cross-team dependencies
3. **Automated Review**:
   - Second-opinion agents
   - Compliance checking

## Reference Guides

### Code Examples

# Code Examples & Prompt Templates

## Agent Setup Prompt
```markdown
You are now integrated with Open Engine. Follow these protocols:

1. Every [15 minutes], check Linear queue for:
   - Issues assigned to you
   - Labeled 'agent-instructions'
2. To claim a task:
   - Move to 'Agent Working'
   - Comment: "[AgentName] claimed this task at [Time]. Expected completion: [ETA]."
3. When working:
   - Keep all context in this ticket
   - If blocked, move to 'needs-input' and ask EXACT question
4. When done:
   - Attach ALL outputs
   - Move to 'Agent Done'
   - Comment: "Completed: [Summary]. Next steps: [ ]."
```

## Task Creation Template
```markdown
**Title**: [Clear action phrase]

**Background**:
- [Relevant context]
- [Attached files/links]

**Constraints**:
- [Limitations/requirements]
- [Avoid X]

**Definition of Done**:
- [Deliverable 1]
- [Review criteria]
- [Approval needed?]
```

## Delegation Between Agents
```python
# Example: Codex delegating to Claude
create_ticket(
  title="Review UI for new dashboard",
  assignee="claude-agent",
  labels=["agent-instructions"],
  description=f"""
  Background: New dashboard implemented (see attached specs).
  Constraints: Mobile-first, comply with styleguide.pdf
  Done: Markup review + suggested changes in Figma
  """,
  attachments=["specs.md", "styleguide.pdf"]
)
```

## Smoke Test
1. Create test ticket: "Say hello from the queue"
2. Assign to agent
3. Verify agent:
   - Claims ticket
   - Moves status
   - Leaves receipt
   - Completes task

### Common Pitfalls

# Common Pitfalls & Solutions

## Context Leakage
**Problem**: Agents work in isolation, losing context between steps.
- *Example*: Codex fixes bug but doesn't tell Claude about UI impacts.
**Solution**:
- Require ALL context in tickets
- Use template: "Background:", "Related:", "Dependencies:"

## Ambiguous Handoffs
**Problem**: Unclear when work transitions between agents/humans.
- *Example*: Support agent escalates without customer history.
**Solution**:
- Explicit "Definition of Done" in every ticket
- Standard status transitions:
  - Agent Working → Needs Input (blocked)
  → Agent Done

## Silent Failures
**Problem**: Agents fail without notification.
- *Example*: Codex hits API error but ticket stays 'Working'.
**Solution**:
- Implement heartbeat checks
- Timeout after [interval] if no updates
- Escalate to 'needs-input' on errors

## Overloaded Tickets
**Problem**: Single ticket contains multiple workstreams.
- *Example*: "Redesign UI + fix backend + update docs"
**Solution**:
- One discrete action per ticket
- Use "Epic" tickets to group related work
- Enforce title format: "[Verb] [Noun]" (e.g., "Update login CSS")

## Audit Trail Gaps
**Problem**: Decisions get lost in private chats.
- *Example*: Paint color chosen in Claude chat but not recorded.
**Solution**:
- Ban side-channel communication
- Require ALL outputs as ticket attachments
- Use template:
  "Decision: [ ]
  Rationale: [ ]
  Alternatives: [ ]"

## Tool Limitations
**Problem**: Queue system lacks needed features.
- *Example*: Jira doesn't show agent statuses clearly.
**Solution**:
- Use Linear (best for Open Engine)
- Or extend with custom fields:
  - "Agent Owner"
  - "Last Agent Activity"
  - "Blocked Reason"

### Core Concepts

# Core Concepts of Open Engine

## The Handoff Problem
Modern AI users often employ multiple specialized agents (Claude for design, Codex for engineering, etc.), but these tools don't communicate. Humans become the 'hallway' between disconnected systems, manually copying context between:
- Different AI tools
- Team members' agents
- Support/product workflows
- Calendar/coding systems

## Queue-Based Coordination
Open Engine solves this by:
1. **Centralizing work** in a shared queue (Linear/Jira/etc.)
2. **Standardizing tickets** with:
   - Clear ownership (human or agent)
   - Required background context
   - Definition of done
   - Explicit handoff points
3. **Agent protocols** for:
   - Claiming tasks
   - Moving statuses
   - Leaving audit trails

## Key Distinctions
- **Prompt vs Work Mode**: 
  - Prompt: "Write a follow-up email"
  - Work: "Here's transcript + constraints. Draft follow-up, flag for review, leave notes"
- **Output vs Work**: 
  - Output is what AI returns
  - Work is reviewable, actionable artifacts

## System Components
1. Queue system (Linear recommended)
2. Setup skill (configuring agents)
3. Status skill (tracking progress)
4. Execution skill (processing tasks)
5. Smoke test (validation)

Example: When Codex finishes a coding task, it:
1. Moves ticket to 'Agent Done'
2. Attaches changed files
3. Notes remaining questions
4. Triggers next agent (e.g., Claude for UI review)

### Practical Guide

# Practical Implementation Guide

## Queue System Setup
1. **Choose your platform**:
   - Linear (free tier works)
   - Jira
   - Custom Kanban
2. **Create standard labels**:
   - `agent-instructions` (tasks for AI)
   - `needs-input` (blocked tasks)
   - `agent-done` (completed work)

## Agent Configuration
For each AI tool (Claude/Codex/etc.), create skills that:
1. **Check assigned queue** every [interval]
2. **Claim tasks** by:
   - Moving to 'Agent Working'
   - Leaving "Claimed by [Agent]" comment
3. **Process work** with:
   - All source materials attached
   - Clear stopping points
4. **Complete tasks** by:
   - Moving to 'Agent Done'
   - Attaching outputs
   - Noting next steps

## Human-Agent Collaboration
1. **Creating tasks**:
   - Include: "Background:", "Constraints:", "Definition of Done:"
   - Example: "Background: Client call transcript attached. Constraints: Don't promise timelines. Done: Draft email + approval request."
2. **Reviewing work**:
   - Check 'Agent Done' queue
   - Verify attached artifacts
   - Provide feedback via ticket comments

## Team Coordination
1. **Cross-agent delegation**:
   - Agent A creates ticket for Agent B
   - Includes all context needed
   - Labels as `agent-instructions`
2. **Audit trails**:
   - All communication stays in tickets
   - No context lost in private chats

Example Workflow:
1. Human creates ticket: "Redesign login flow - mobile first"
2. Codex claims it, implements backend
3. Codex creates new ticket: "Review UI for new login" → Claude
4. Claude provides feedback in ticket
5. System notifies human for final approval

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[I Was The Only Thing Connecting Claude, ChatGPT, and Codex. So I Built My Replacement.](https://www.youtube.com/watch?v=QSK4vf_ZTRA)** by AI News & Strategy Daily | Nate B Jones
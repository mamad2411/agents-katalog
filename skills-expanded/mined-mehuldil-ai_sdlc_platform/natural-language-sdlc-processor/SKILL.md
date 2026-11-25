---
name: Natural Language SDLC Processor
description: >
  Understands natural English language queries and converts them to SDLC commands.
  Supports hybrid pattern matching + AI understanding. Asks for ADO work item if
  missing, shows non-closed items for quick selection. Works with any stage, any role.
tags: [ai-sdlc, natural-language, workflow-orchestration]
triggerPhrases:
  - "create a master story for"
  - "review this PRD for"
  - "generate tech tasks for"
  - "check gates for"
  - "validate release for"
  - "run the full workflow"
  - "what's the status of"
  - "I need a"
  - "can you help me with"
  - "let me do the whole pipeline"
---

# Natural Language SDLC Processor

Converts natural English language queries into SDLC slash commands and executes them with interactive prompts.

## How It Works

### 1. Input Processing
When the user types natural language (e.g., "Create a master story for multi-language support"):

1. **Pattern Matching** (fast):
   - Detect common phrases: "create story" → `/project:grooming --type=master`
   - Detect actions: "review", "generate", "check", "validate"
   - Map to SDLC commands

2. **AI Understanding** (fallback):
   - If no pattern match, Claude interprets intent
   - Suggests best command + parameters
   - Offers options if ambiguous

### 2. Parameter Resolution
If user doesn't provide ADO work item number (AB#123):

1. **Ask via text**: "What work item? (e.g., AB#123)"
2. **Show recent items**: Load all non-closed items from user's ADO project
3. **User selects**: Pick from menu or type custom ID

### 3. Execution
- Route to appropriate command skill
- Pass through interactive prompts
- Execute with full context
- Save to memory

## Natural Language Examples

```
User: "Create a master story for multi-language support"
→ System detects: "create" + "master story"
→ Matches: /project:grooming --type=master
→ Asks: "What's the work item? (e.g., AB#123)"
→ Asks: "Happy path only or comprehensive?"
→ Executes /project:grooming

User: "Review this PRD for gaps"
→ System detects: "review" + "PRD"
→ Matches: /project:prd-review
→ Asks: "Review from which perspective? (Product/Backend/Frontend/QA)"
→ Executes /project:prd-review

User: "Let me do the whole pipeline for this feature"
→ System detects: "whole pipeline" / "full workflow"
→ Triggers: Orchestrator Agent
→ Shows: Progress dashboard with 15-stage workflow
→ Executes: Complete workflow PRD → Production

User: "Check gates for this release"
→ System detects: "check gates"
→ Matches: /project:gate-check
→ Asks: "Which stage? (1-15)"
→ Executes: Gate validation
```

## Command Pattern Mapping

| User Intent | Pattern | Command | Example |
|-------------|---------|---------|---------|
| "set up" / "install" / "configure" | setup/install/configure/init/bootstrap/get started | `/project:setup` | "Set up the SDLC plugin" |
| "create requirement" | new feature/requirement/capture | `/project:requirement-intake` | "I have a new feature idea" |
| "create master story" | create + story | `/project:grooming --type=master` | "Create a master story for auth system" |
| "break into sprints" | break + sprints/split | `/project:grooming --type=sprint` | "Break this into sprint stories" |
| "review PRD" | review + prd | `/project:prd-review` | "Review this PRD for gaps" |
| "architecture" | architecture/design review/ADR | `/project:architecture-review` | "Review architecture for this" |
| "system design" | system design/data model/API design | `/project:system-design` | "Design the data model" |
| "plan sprint" | sprint plan/task breakdown | `/project:sprint-planning` | "Plan sprint 12 tasks" |
| "generate tech tasks" | generate + tasks/implement | `/project:implementation` | "Generate tech tasks from this story" |
| "code review" | code review/PR review | `/project:code-review` | "Review this pull request" |
| "test plan" | test + plan/QA/test cases | `/project:test-design` | "Create a test plan for this" |
| "perf test" | performance/load test/NFR | `/project:performance-testing` | "Run load test for this API" |
| "staging" | staging/SIT/UAT | `/project:staging-validation` | "Deploy to staging for testing" |
| "release prep" | prepare/release/go-live prep | `/project:release-prep` | "Prepare this for release" |
| "deploy" | deploy + prod/production | `/project:deployment` | "Deploy to production" |
| "monitor" | monitor + setup/alerts/dashboard | `/project:monitoring` | "Set up monitoring for this service" |
| "incident" | incident/post-mortem | `/project:incident-response` | "Create post-mortem for this incident" |
| "full workflow" | workflow/pipeline/full SDLC | Orchestrator Agent | "Let me do the full workflow" |

## Smart Defaults

When information is missing, use context:

- **Role**: Detect from user context (if provided), else ask
- **Stack**: Check .sdlc/state.json for previous choice
- **Stage**: Infer from command type or ask
- **Estimation**: Default to "balanced" unless specified

## Integration Points

- **All 15 command skills**: Route patterns to appropriate skill
- **Orchestrator Agent**: Handle multi-step workflows
- **Memory system**: Load previous context, save outcomes
- **ADO**: Fetch non-closed items for selection
- **Context recovery**: Use .sdlc/state.json for smart defaults

## Error Handling

If pattern doesn't match:
1. Ask user to clarify
2. Show available commands
3. Or offer conversation mode
4. Never assume intent


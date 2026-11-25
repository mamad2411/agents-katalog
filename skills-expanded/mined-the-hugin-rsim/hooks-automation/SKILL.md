---
name: Hooks Automation
description: Automated coordination, formatting, and learning from Claude Code operations using intelligent hooks with MCP integration. Includes pre/post task hooks, session management, Git integration, memory coordination, and neural pattern training for enhanced development workflows.
---

# Hooks Automation

Intelligent automation system that coordinates, validates, and learns from Claude Code operations through hooks integrated with MCP tools and neural pattern training.

## Prerequisites

**Required:**
- Claude Flow CLI installed (`npm install -g claude-flow@alpha`)
- Claude Code with hooks enabled
- `.claude/settings.json` with hook configurations

**Optional:**
- MCP servers configured (claude-flow, ruv-swarm, flow-nexus)
- Git repository for version control

## Quick Start

```bash
# Initialize with default hooks configuration
npx claude-flow init --hooks

# Pre-task hook (auto-spawns agents)
npx claude-flow hook pre-task --description "Implement authentication"

# Post-edit hook (auto-formats and stores in memory)
npx claude-flow hook post-edit --file "src/auth.js" --memory-key "auth/login"

# Session end hook (saves state and metrics)
npx claude-flow hook session-end --session-id "dev-session" --export-metrics
```

---

## Available Hooks

### Pre-Operation Hooks

**pre-edit** — Validate and assign agents before file modifications
```bash
npx claude-flow hook pre-edit [options]

Options:
  --file, -f <path>         File path to be edited
  --auto-assign-agent       Automatically assign best agent (default: true)
  --validate-syntax         Pre-validate syntax before edit
  --check-conflicts         Check for merge conflicts
  --backup-file             Create backup before editing
```

**pre-bash** — Check command safety and resource requirements
```bash
npx claude-flow hook pre-bash --command <cmd>

Options:
  --command, -c <cmd>       Command to validate
  --check-safety            Verify command safety (default: true)
  --estimate-resources      Estimate resource usage
  --require-confirmation    Request user confirmation for risky commands
```

**pre-task** — Auto-spawn agents and prepare for complex tasks
```bash
npx claude-flow hook pre-task [options]

Options:
  --description, -d <text>  Task description for context
  --auto-spawn-agents       Automatically spawn required agents (default: true)
  --load-memory             Load relevant memory from previous sessions
  --optimize-topology       Select optimal swarm topology
  --estimate-complexity     Analyze task complexity
```

**pre-search** — Prepare and optimize search operations
```bash
npx claude-flow hook pre-search --query <query>

Options:
  --query, -q <text>        Search query
  --check-cache             Check cache first (default: true)
  --optimize-query          Optimize search pattern
```

### Post-Operation Hooks

**post-edit** — Auto-format, validate, and update memory
```bash
npx claude-flow hook post-edit [options]

Options:
  --file, -f <path>         File path that was edited
  --auto-format             Automatically format code (default: true)
  --memory-key, -m <key>    Store edit context in memory
  --train-patterns          Train neural patterns from edit
  --validate-output         Validate edited file
```

**post-bash** — Log execution and update metrics
```bash
npx claude-flow hook post-bash --command <cmd>

Options:
  --command, -c <cmd>       Command that was executed
  --log-output              Log command output (default: true)
  --update-metrics          Update performance metrics
  --store-result            Store result in memory
```

**post-task** — Performance analysis and decision storage
```bash
npx claude-flow hook post-task [options]

Options:
  --task-id, -t <id>        Task identifier for tracking
  --analyze-performance     Generate performance metrics (default: true)
  --store-decisions         Save task decisions to memory
  --export-learnings        Export neural pattern learnings
  --generate-report         Create task completion report
```

**post-search** — Cache results and improve patterns
```bash
npx claude-flow hook post-search --query <query> --results <path>

Options:
  --query, -q <text>        Original search query
  --results, -r <path>      Results file path
  --cache-results           Cache for future use (default: true)
  --train-patterns          Improve search patterns
```

### MCP Integration Hooks

```bash
npx claude-flow hook mcp-initialized --swarm-id <id>   # Persist swarm config
npx claude-flow hook agent-spawned --agent-id <id> --type <type>  # Update agent roster
npx claude-flow hook task-orchestrated --task-id <id>  # Monitor task progress
npx claude-flow hook neural-trained --pattern <name>   # Save pattern improvements
npx claude-flow hook memory-sync --namespace <ns>      # Sync memory across agents
```

### Session Hooks

**session-start** — Initialize new session
```bash
npx claude-flow hook session-start --session-id <id> [--load-context] [--init-agents]
```

**session-restore** — Load previous session state
```bash
npx claude-flow hook session-restore --session-id <id> [--restore-memory] [--restore-agents]
```

**session-end** — Cleanup and persist session state
```bash
npx claude-flow hook session-end [options]

Options:
  --session-id, -s <id>     Session identifier to end
  --save-state              Save current session state (default: true)
  --export-metrics          Export session metrics
  --generate-summary        Create session summary
  --cleanup-temp            Remove temporary files
```

**notify** — Custom notifications with swarm status
```bash
npx claude-flow hook notify -m "Task completed" --level info
npx claude-flow hook notify -m "Critical error" --level error --broadcast
```

---

## Configuration

### Basic Configuration

Edit `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "^(Write|Edit|MultiEdit)$",
        "hooks": [{
          "type": "command",
          "command": "npx claude-flow hook pre-edit --file '${tool.params.file_path}' --memory-key 'swarm/editor/current'"
        }]
      },
      {
        "matcher": "^Bash$",
        "hooks": [{
          "type": "command",
          "command": "npx claude-flow hook pre-bash --command '${tool.params.command}'"
        }]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "^(Write|Edit|MultiEdit)$",
        "hooks": [{
          "type": "command",
          "command": "npx claude-flow hook post-edit --file '${tool.params.file_path}' --memory-key 'swarm/editor/complete' --auto-format --train-patterns"
        }]
      },
      {
        "matcher": "^Bash$",
        "hooks": [{
          "type": "command",
          "command": "npx claude-flow hook post-bash --command '${tool.params.command}' --update-metrics"
        }]
      }
    ]
  }
}
```

### Full Configuration

```json
{
  "hooks": {
    "enabled": true,
    "debug": false,
    "timeout": 5000,

    "PreToolUse": [
      {
        "matcher": "^(Write|Edit|MultiEdit)$",
        "hooks": [{
          "type": "command",
          "command": "npx claude-flow hook pre-edit --file '${tool.params.file_path}' --auto-assign-agent --validate-syntax",
          "timeout": 3000,
          "continueOnError": true
        }]
      },
      {
        "matcher": "^Task$",
        "hooks": [{
          "type": "command",
          "command": "npx claude-flow hook pre-task --description '${tool.params.task}' --auto-spawn-agents --load-memory",
          "async": true
        }]
      },
      {
        "matcher": "^Grep$",
        "hooks": [{
          "type": "command",
          "command": "npx claude-flow hook pre-search --query '${tool.params.pattern}' --check-cache"
        }]
      }
    ],

    "PostToolUse": [
      {
        "matcher": "^(Write|Edit|MultiEdit)$",
        "hooks": [{
          "type": "command",
          "command": "npx claude-flow hook post-edit --file '${tool.params.file_path}' --memory-key 'edits/${tool.params.file_path}' --auto-format --train-patterns",
          "async": true
        }]
      },
      {
        "matcher": "^Task$",
        "hooks": [{
          "type": "command",
          "command": "npx claude-flow hook post-task --task-id '${result.task_id}' --analyze-performance --store-decisions --export-learnings",
          "async": true
        }]
      },
      {
        "matcher": "^Grep$",
        "hooks": [{
          "type": "command",
          "command": "npx claude-flow hook post-search --query '${tool.params.pattern}' --cache-results --train-patterns"
        }]
      }
    ],

    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "npx claude-flow hook session-start --session-id '${session.id}' --load-context"
      }]
    }],

    "SessionEnd": [{
      "hooks": [{
        "type": "command",
        "command": "npx claude-flow hook session-end --session-id '${session.id}' --export-metrics --generate-summary --cleanup-temp"
      }]
    }]
  }
}
```

---

## Hook Response Format

Hooks return JSON responses to control operation flow:

```json
// Continue:
{ "continue": true, "reason": "All validations passed", "metadata": { "agent_assigned": "backend-dev" } }

// Block:
{ "continue": false, "reason": "Protected file - manual review required", "metadata": { "requires": "manual_approval" } }

// Warning:
{ "continue": true, "warnings": ["Cyclomatic complexity: 15 (threshold: 10)"], "metadata": { "complexity": 15 } }
```

---

## Git Integration

Pre-commit hook for quality control:

```bash
#!/bin/bash
FILES=$(git diff --cached --name-only --diff-filter=ACM)

for FILE in $FILES; do
  npx claude-flow hook pre-edit --file "$FILE" --validate-syntax
  if [ $? -ne 0 ]; then echo "Validation failed for $FILE"; exit 1; fi
  npx claude-flow hook post-edit --file "$FILE" --auto-format
done

npm test
exit $?
```

---

## Agent Coordination Workflow

```bash
# Agent 1: Backend Developer
npx claude-flow hook pre-task --description "Implement user authentication API" --auto-spawn-agents --load-memory
npx claude-flow hook pre-edit --file "api/auth.js" --auto-assign-agent --validate-syntax
# ... code changes ...
npx claude-flow hook post-edit --file "api/auth.js" --memory-key "swarm/backend/auth-api" --auto-format --train-patterns
npx claude-flow hook notify --message "Auth API complete" --swarm-status --broadcast
npx claude-flow hook post-task --task-id "auth-api" --analyze-performance --store-decisions

# Agent 2: Test Engineer (reads memory written by Agent 1)
npx claude-flow hook session-restore --session-id "swarm-current" --restore-memory
npx claude-flow hook pre-task --description "Write tests for auth API" --load-memory
npx claude-flow hook post-edit --file "api/auth.test.js" --memory-key "swarm/testing/auth-api-tests" --train-patterns
```

---

## Performance Tips

1. Keep hooks lightweight — target < 100ms execution time
2. Use `async: true` for heavy operations to avoid blocking
3. Cache aggressively — store frequently accessed data
4. Batch related operations in single hook calls
5. Set appropriate TTLs on memory keys
6. Profile execution times with debug mode
7. Parallelize independent hooks when possible

---

## Debugging

```bash
export CLAUDE_FLOW_DEBUG=true
npx claude-flow hook pre-edit --file "test.js" --debug
cat .claude-flow/logs/hooks-$(date +%Y-%m-%d).log
npx claude-flow hook validate-config
```

**Hooks not executing:** Check `.claude/settings.json` syntax, matcher patterns, and PATH.
**Timeouts:** Increase timeout value or use `async: true`.
**Memory issues:** Set TTLs, clean up old keys, use namespaces.

---

## Related Commands

```bash
npx claude-flow init --hooks        # Initialize hooks system
npx claude-flow hook --list         # List available hooks
npx claude-flow hook --test <hook>  # Test specific hook
npx claude-flow memory usage        # Manage memory
npx claude-flow agent spawn         # Spawn agents
npx claude-flow swarm init          # Initialize swarm
```

## Integration with Other Skills

Works with: SPARC Methodology, Pair Programming, Verification Quality, GitHub Workflows, Performance Analysis, Swarm Advanced (multi-agent coordination).

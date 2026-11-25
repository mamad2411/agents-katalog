---
name: "Workflow Automation Designer"
version: "1.0.0"
description: "Designs automated workflows with triggers, conditions, actions, and error handling. Supports event-driven architectures."
author: "workspace"
activated: false
---

# Workflow Automation Designer

Designs automated workflows with triggers, conditions, actions, and error handling. Supports event-driven architectures.

## Decision Framework

### When to Apply
Use when: Business process automation, event-driven workflows, task orchestration, scheduled jobs

### When NOT to Apply
Don't use when: Simple sequential scripts, one-off tasks

## Anti-Patterns

### 1. No Error Handling in Workflows
```javascript
// BAD: One step failure kills everything
for (const step of steps) { await step.execute(); }

// GOOD: Error boundaries per step
for (const step of steps) {
  try { await step.execute(); }
  catch (error) {
    if (step.retryable) await step.retry();
    else { await step.onError(error); break; }
  }
}
```


## Trigger Phrases

- "Automate workflow"
- "Business process"
- "Event-driven"
- "Task automation"
- "Scheduled jobs"

## Patterns

### Workflow Engine
```javascript
class WorkflowEngine {
  constructor(definition) { this.definition = definition; }

  async execute(context) {
    let current = this.definition.start;
    const history = [];

    while (current) {
      const step = this.definition.steps[current];
      const result = await this.executeStep(step, context);
      history.push({ step: current, result, timestamp: Date.now() });

      if (result.status === 'failed' && step.onError) {
        current = step.onError;
      } else if (result.status === 'success') {
        current = step.next;
      } else {
        break;
      }
    }
    return { status: current ? 'completed' : 'stopped', history };
  }

  async executeStep(step, context) {
    try {
      const output = await step.action(context);
      return { status: 'success', output };
    } catch (error) {
      return { status: 'failed', error: error.message };
    }
  }
}
```

## Integration
- Works with: state-machine-designer, notification-system-builder, error-recovery-orchestrator


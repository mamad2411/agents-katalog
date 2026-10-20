---
name: "State Machine Designer"
version: "1.0.0"
description: "Designs finite state machines and statecharts for complex UI and business logic flows. Provides visual state diagrams and transition guards."
author: "workspace"
activated: false
---

# State Machine Designer

Designs finite state machines and statecharts for complex UI and business logic flows. Provides visual state diagrams and transition guards.

## Decision Framework

### When to Apply
Use when: Complex workflows, order processing, UI state management, multi-step processes with branching

### When NOT to Apply
Don't use when: Simple boolean states, purely linear flows

## Anti-Patterns

### 1. Boolean Flags for Complex States
```javascript
// BAD: Impossible states possible
const [isLoading, setIsLoading] = useState(false);
const [isError, setIsError] = useState(false);
const [isSuccess, setIsSuccess] = useState(false);
// What if all three are true?

// GOOD: Single state machine
const [state, setState] = useState('idle'); // 'idle' | 'loading' | 'success' | 'error'
```

### 2. Invalid State Transitions
Always define and enforce valid transitions.


## Trigger Phrases

- "State machine"
- "Complex state"
- "Workflow states"
- "State transitions"
- "Statechart"

## Patterns

### State Machine
```javascript
class StateMachine {
  constructor(config) {
    this.config = config;
    this.state = config.initial;
    this.context = config.context || {};
  }

  transition(event) {
    const stateConfig = this.config.states[this.state];
    const transition = stateConfig?.on?.[event];
    if (!transition) return this; // No transition defined

    const target = typeof transition === 'string' ? transition : transition.target;
    const action = typeof transition === 'object' ? transition.action : null;

    if (action) this.context = action(this.context, event);
    this.state = target;
    return this;
  }

  can(event) {
    return !!this.config.states[this.state]?.on?.[event];
  }
}

const orderMachine = new StateMachine({
  initial: 'pending',
  states: {
    pending: { on: { CONFIRM: 'confirmed', CANCEL: 'cancelled' } },
    confirmed: { on: { SHIP: 'shipped', CANCEL: 'cancelled' } },
    shipped: { on: { DELIVER: 'delivered' } },
    delivered: { on: {} },
    cancelled: { on: {} }
  }
});
```

## Integration
- Works with: component-lifecycle-manager, workflow-automation-designer, form-pattern-engine


---
name: state-machine-analysis
description: >
  Map legal/illegal state transitions, stuck states, impossible states.
  Used during decomposition to feed the Threat Modeler with transition tables.
---

# State Machine Analysis Skill

## Purpose

Protocols are state machines. Funds are locked, unlocked, staked, unstaked, pending,
settled, liquidated. This skill extracts the state machine from the code and documents
what transitions are legal, what's illegal, and what could get stuck.

## When to Use

- During decomposition (Decomposer agent)
- When analyzing governance flows, vault lifecycles, or position management
- When the system has explicit or implicit phases (e.g., deposit period → lock period → withdrawal period)

## Extraction Protocol

### Step 1: Identify State Variables

```bash
# Find enum declarations (explicit states)
grep -rn "enum " --include="*.sol"

# Find boolean flags used as state (implicit states)
grep -rn "bool.*paused\|bool.*locked\|bool.*initialized\|bool.*active" --include="*.sol"

# Find phase/status variables
grep -rn "uint.*phase\|uint.*status\|uint.*state\|uint.*stage" --include="*.sol"
```

### Step 2: Map Transitions

For each state variable, document:

| From State | To State | Trigger Function | Access Control | Conditions |
|-----------|----------|-----------------|----------------|------------|
| Unlocked | Locked | `lock()` | onlyOwner | balance > 0 |
| Locked | Unlocked | `unlock()` | onlyOwner | block.timestamp > lockEnd |

### Step 3: Identify Risks

- **Stuck states**: Can the system reach a state from which no transition is possible?
- **Illegal transitions**: Can an attacker skip a required state? (e.g., withdraw without deposit)
- **Race conditions**: Can two users trigger conflicting transitions simultaneously?
- **Missing transitions**: Is there a "emergency exit" from every state?

## Output

```markdown
# State Machine: [Contract Name]

## States
[List all states with descriptions]

## Transition Table
[Full transition matrix]

## Risk Assessment
- Stuck states: [list or "none found"]
- Illegal transitions possible: [list or "none found"]
- Missing emergency exits: [list or "none found"]
```

Save to: `specs/decomposition/state-machine-decomposition.md`

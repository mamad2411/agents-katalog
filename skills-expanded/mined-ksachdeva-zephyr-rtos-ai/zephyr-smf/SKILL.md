---
name: zephyr-smf
description: Expert guidance on Zephyr State Machine Framework (SMF) for implementing flat and hierarchical state machines. Use when the user asks about state machines, state transitions, entry/run/exit actions, hierarchical states (HSM), event-driven state machines, SMF_CREATE_STATE, smf_set_state, smf_run_state, or implementing UML statecharts in Zephyr RTOS.
---

# Zephyr State Machine Framework (SMF)

## Overview

SMF is an application-agnostic framework for integrating state machines into Zephyr applications. Enable with `CONFIG_SMF=y`.

## Core Concepts

### State Structure

Every state has three optional actions:
- **Entry**: Executes when entering the state
- **Run**: Executes on each `smf_run_state()` call
- **Exit**: Executes when leaving the state

```c
// User object MUST have smf_ctx as FIRST member
struct s_object {
    struct smf_ctx ctx;  // MUST be first
    /* application-specific data */
};
```

### State Definition

```c
enum app_state { STATE_IDLE, STATE_ACTIVE, STATE_ERROR };

static const struct smf_state app_states[] = {
    [STATE_IDLE]   = SMF_CREATE_STATE(idle_entry, idle_run, idle_exit, NULL, NULL),
    [STATE_ACTIVE] = SMF_CREATE_STATE(active_entry, active_run, NULL, NULL, NULL),
    [STATE_ERROR]  = SMF_CREATE_STATE(NULL, error_run, error_exit, NULL, NULL),
};
```

**SMF_CREATE_STATE parameters**: `(entry, run, exit, parent, initial)`
- Set unused actions to `NULL`
- `parent`: For hierarchical states (requires `CONFIG_SMF_ANCESTOR_SUPPORT`)
- `initial`: Initial child state (requires `CONFIG_SMF_INITIAL_TRANSITION`)

### Action Signatures

```c
// Entry and exit actions
static void state_entry(void *o) { /* ... */ }
static void state_exit(void *o) { /* ... */ }

// Run action - returns event handling result
static enum smf_state_result state_run(void *o) {
    struct s_object *s = (struct s_object *)o;
    // Process events, trigger transitions
    return SMF_EVENT_HANDLED;  // or SMF_EVENT_PROPAGATE for HSM
}
```

## Workflow

### 1. Determine State Machine Type

| Type | Use Case | Kconfig |
|------|----------|---------|
| **Flat** | Simple sequential states, no nesting | `CONFIG_SMF=y` |
| **Hierarchical (HSM)** | Shared behavior, nested states | Add `CONFIG_SMF_ANCESTOR_SUPPORT=y` |
| **HSM + Initial Transitions** | Auto-transition to child states | Add `CONFIG_SMF_INITIAL_TRANSITION=y` |

**Step 1a**: For flat state machines, proceed to step 2.

**Step 1b**: For hierarchical state machines, read [references/hierarchical.md](references/hierarchical.md).

### 2. Implementation Pattern

```c
#include <zephyr/smf.h>

static struct s_object s_obj;
static const struct smf_state app_states[];  // Forward declaration

// 1. Define state actions
static void idle_entry(void *o) { /* initialize */ }
static enum smf_state_result idle_run(void *o) {
    struct s_object *s = (struct s_object *)o;
    if (/* condition */) {
        smf_set_state(SMF_CTX(&s_obj), &app_states[STATE_ACTIVE]);
    }
    return SMF_EVENT_HANDLED;
}

// 2. Populate state table
static const struct smf_state app_states[] = {
    [STATE_IDLE] = SMF_CREATE_STATE(idle_entry, idle_run, NULL, NULL, NULL),
    // ... other states
};

// 3. Initialize and run
int main(void) {
    smf_set_initial(SMF_CTX(&s_obj), &app_states[STATE_IDLE]);

    while (1) {
        int32_t ret = smf_run_state(SMF_CTX(&s_obj));
        if (ret) {
            break;  // State machine terminated
        }
        k_msleep(100);
    }
}
```

### 3. Event-Driven Pattern

For event-driven state machines, read [references/patterns.md](references/patterns.md).

### 4. API Reference

For complete API signatures and Kconfig options, read [references/api.md](references/api.md).

## Critical Rules

1. **User object layout**: `struct smf_ctx` MUST be the first member
2. **SMF_CTX macro**: Always use `SMF_CTX(&user_obj)` for API calls
3. **Transition restrictions**:
   - Call `smf_set_state()` only from entry or run actions, NEVER from exit
   - Stop calling `smf_run_state()` when it returns non-zero
4. **HSM leaf states**: Without `CONFIG_SMF_INITIAL_TRANSITION`, always transition to leaf states, not parent states
5. **Termination**: Use `smf_set_terminate(ctx, error_code)` to stop the state machine

## Common Pitfalls

| Issue | Cause | Solution |
|-------|-------|----------|
| Crashes on state access | `smf_ctx` not first member | Ensure `struct smf_ctx ctx;` is first in user object |
| Transition ignored | Called from exit action | Move transition to run action |
| Parent entry/exit not called | Transition between siblings | This is correct UML behavior - LCA actions are skipped |
| HSM stuck in parent state | Missing initial transition | Enable `CONFIG_SMF_INITIAL_TRANSITION` or always set leaf states |

## Source Locations

| Description | Path |
|:---|:---|
| SMF Header | `<zephyr-ws>/deps/zephyr/include/zephyr/smf.h` |
| SMF Implementation | `<zephyr-ws>/deps/zephyr/lib/smf/smf.c` |
| SMF Documentation | `<zephyr-ws>/deps/zephyr/doc/services/smf/index.rst` |
| Calculator Sample | `<zephyr-ws>/deps/zephyr/samples/subsys/smf/smf_calculator` |
| HSM Sample (PSiCC2) | `<zephyr-ws>/deps/zephyr/samples/subsys/smf/hsm_psicc2` |

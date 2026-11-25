---
name: state-machine-designer
description: "Model entity state transitions, guard conditions, side effects, and generate implementation code. Use when designing order flows, auth states, approval workflows, payment lifecycles, or any entity with distinct states and transition rules. Trigger on \"state machine\", \"workflow states\", \"order flow\", \"status transitions\", \"lifecycle\", \"approval flow\". Also use when an entity has a 'status' field with more than 3 possible values."
allowed-tools: Read, Write, Edit, Grep, Glob
---

# State Machine Designer Skill

Design and implement state machines for entities with lifecycle workflows. Produces both a human-readable spec (tables + Mermaid diagram) and a type-safe TypeScript implementation using a transition map pattern.

## When to Use

- An entity has a `status` field with 3+ possible values (e.g., orders, invoices, tickets)
- Approval workflows where actions depend on current state and user role
- Payment flows with pending, processing, completed, failed, refunded states
- Content publishing with draft, review, published, archived lifecycle
- Any flow where "what can happen next" depends on "where we are now"

## Output Format

Write the state machine spec to `.claude/specs/[feature]/state-machine.md` using this exact structure:

```markdown
# State Machine: [Entity Name]

## States

| State | Description | Entry Action | Terminal? |
|-------|-------------|-------------|-----------|
| draft | Created but not submitted | — | No |
| pending_review | Submitted, awaiting reviewer | Notify reviewer via email | No |
| approved | Reviewer accepted | Send approval email, create audit log | No |
| rejected | Reviewer declined | Send rejection email with reason | No |
| completed | All post-approval work finished | Update metrics, archive | Yes |
| cancelled | User cancelled before completion | Release held resources | Yes |

## Transitions

| # | From | To | Trigger | Guard | Side Effects |
|---|------|----|---------|-------|-------------|
| 1 | draft | pending_review | user.submit() | All required fields non-empty | Create audit log entry |
| 2 | pending_review | approved | reviewer.approve() | Reviewer role = ADMIN or MANAGER | Send email, log |
| 3 | pending_review | rejected | reviewer.reject(reason) | reason.length > 0 | Send email with reason |
| 4 | rejected | draft | user.revise() | — | Clear previous rejection |
| 5 | approved | completed | system.markDone() | All child tasks resolved | Archive, update dashboard |
| 6 | draft | cancelled | user.cancel() | — | — |
| 7 | pending_review | cancelled | user.cancel() | — | Notify reviewer of cancellation |

## Mermaid Diagram

\```mermaid
stateDiagram-v2
    [*] --> draft
    draft --> pending_review : submit
    draft --> cancelled : cancel
    pending_review --> approved : approve
    pending_review --> rejected : reject
    pending_review --> cancelled : cancel
    rejected --> draft : revise
    approved --> completed : markDone
    completed --> [*]
    cancelled --> [*]
\```
```

## TypeScript Implementation Pattern

Generate the implementation alongside the spec. Use a discriminated union + transition map — not a switch statement chain.

```typescript
// src/state-machines/order-state.ts

// 1. Define states as a const enum for zero-cost at runtime
export const OrderState = {
  DRAFT: 'draft',
  PENDING_REVIEW: 'pending_review',
  APPROVED: 'approved',
  REJECTED: 'rejected',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled',
} as const;

export type OrderStateValue = typeof OrderState[keyof typeof OrderState];

// 2. Define events as discriminated union
export type OrderEvent =
  | { type: 'SUBMIT' }
  | { type: 'APPROVE'; reviewerId: string }
  | { type: 'REJECT'; reviewerId: string; reason: string }
  | { type: 'REVISE' }
  | { type: 'MARK_DONE' }
  | { type: 'CANCEL' };

// 3. Guard functions — return string (error message) on failure, null on success
type Guard = (context: OrderContext, event: OrderEvent) => string | null;

const guards: Record<string, Guard> = {
  allFieldsFilled: (ctx) =>
    !ctx.title || !ctx.description ? 'Title and description are required' : null,
  hasReviewerPermission: (ctx, event) => {
    if (event.type !== 'APPROVE' && event.type !== 'REJECT') return 'Invalid event';
    return ctx.reviewerRole === 'ADMIN' || ctx.reviewerRole === 'MANAGER'
      ? null
      : 'Reviewer must be ADMIN or MANAGER';
  },
  rejectionHasReason: (_ctx, event) =>
    event.type === 'REJECT' && event.reason.length === 0
      ? 'Rejection reason is required'
      : null,
  allTasksResolved: (ctx) =>
    ctx.pendingTasks > 0 ? `${ctx.pendingTasks} tasks still pending` : null,
};

// 4. Transition map — single source of truth
interface Transition {
  target: OrderStateValue;
  guard?: Guard;
  sideEffects?: Array<(ctx: OrderContext, event: OrderEvent) => Promise<void>>;
}

const transitions: Record<OrderStateValue, Partial<Record<OrderEvent['type'], Transition>>> = {
  [OrderState.DRAFT]: {
    SUBMIT: {
      target: OrderState.PENDING_REVIEW,
      guard: guards.allFieldsFilled,
      sideEffects: [notifyReviewer, createAuditLog],
    },
    CANCEL: {
      target: OrderState.CANCELLED,
    },
  },
  [OrderState.PENDING_REVIEW]: {
    APPROVE: {
      target: OrderState.APPROVED,
      guard: guards.hasReviewerPermission,
      sideEffects: [sendApprovalEmail, createAuditLog],
    },
    REJECT: {
      target: OrderState.REJECTED,
      guard: guards.rejectionHasReason,
      sideEffects: [sendRejectionEmail, createAuditLog],
    },
    CANCEL: {
      target: OrderState.CANCELLED,
      sideEffects: [notifyReviewerOfCancellation],
    },
  },
  [OrderState.APPROVED]: {
    MARK_DONE: {
      target: OrderState.COMPLETED,
      guard: guards.allTasksResolved,
      sideEffects: [archiveOrder, updateDashboard],
    },
  },
  [OrderState.REJECTED]: {
    REVISE: {
      target: OrderState.DRAFT,
      sideEffects: [clearRejection],
    },
  },
  // Terminal states — no transitions out
  [OrderState.COMPLETED]: {},
  [OrderState.CANCELLED]: {},
};

// 5. Transition executor
export async function transition(
  currentState: OrderStateValue,
  event: OrderEvent,
  context: OrderContext,
): Promise<{ newState: OrderStateValue; error?: string }> {
  const stateTransitions = transitions[currentState];
  const t = stateTransitions?.[event.type];

  if (!t) {
    return {
      newState: currentState,
      error: `No transition from "${currentState}" on event "${event.type}"`,
    };
  }

  if (t.guard) {
    const guardError = t.guard(context, event);
    if (guardError) {
      return { newState: currentState, error: guardError };
    }
  }

  // Execute side effects sequentially (order matters)
  if (t.sideEffects) {
    for (const effect of t.sideEffects) {
      await effect(context, event);
    }
  }

  return { newState: t.target };
}
```

## Validation Checklist

Run these checks against every state machine before finalizing. All must pass.

| # | Check | How to Verify |
|---|-------|---------------|
| 1 | No orphan states | Every state appears as a `From` or `To` in at least one transition (except the initial state which may only appear as `To`) |
| 2 | All transitions have source + target | No transition row has an empty `From` or `To` cell |
| 3 | At least one terminal state | At least one state has `Terminal? = Yes` (no outgoing transitions) |
| 4 | Reachability | Every non-initial state is reachable from the initial state via some sequence of transitions |
| 5 | No dead ends (unless terminal) | Every non-terminal state has at least one outgoing transition |
| 6 | Guards are testable | Every guard condition can be evaluated with data available in the context object — no external API calls in guards |
| 7 | Side effects are idempotent | If a side effect fails and the transition is retried, running the side effect again must not cause duplicates (e.g., use idempotency keys for emails) |
| 8 | Mermaid matches table | The Mermaid diagram has exactly the same states and transitions as the table — no extras, no missing |

## Constraints

1. **Terminal states must have empty transition rows.** If a state has `Terminal? = Yes` but also has outgoing transitions in the table, that is a spec error. Flag it.
2. **Never use string literals for states in implementation code.** Always use the const object (`OrderState.DRAFT`) so typos are caught at compile time.
3. **Guards must be pure functions.** They take context + event and return a result. No database calls, no API calls, no side effects inside guards. If you need to check external state, load it into the context before calling `transition()`.
4. **Side effects execute after guard passes but before the state is persisted.** If a side effect fails, the transition should roll back (state stays the same). Document this in the spec.
5. **Always generate the Mermaid diagram.** Developers will paste it into GitHub PRs for visual review. A state machine without a diagram is incomplete.

## Anti-Patterns

- **Status field as a string** — using raw strings (`order.status = 'pending'`) instead of a const enum; typos create invalid states at runtime
- **Switch statement chains** — implementing transitions as `switch (state) { case 'pending': if (event === 'approve') ... }` instead of a transition map; unscalable and hard to audit
- **Side effects in guards** — guards must be pure; if a guard sends an email or writes to the DB, failures leave the system in an inconsistent state
- **Missing terminal states** — every workflow must have at least one end state; without one, entities can cycle forever
- **Implicit transitions** — changing state directly (`order.status = 'approved'`) instead of going through the transition function; bypasses guards and side effects
- **No error handling for failed side effects** — if an email fails to send after approval, should the state roll back? This must be specified per transition

## Checklist

- [ ] All states listed in the state table with descriptions
- [ ] All transitions listed with From, To, Trigger, Guard, and Side Effects
- [ ] At least one terminal state defined
- [ ] Mermaid diagram matches the transition table exactly
- [ ] Validation checklist (8 checks) passes
- [ ] TypeScript implementation uses const enum + transition map pattern
- [ ] Guards are pure functions (no DB calls, no API calls)
- [ ] Side effects are idempotent (safe to retry)
- [ ] Spec saved to `.claude/specs/[feature]/state-machine.md`

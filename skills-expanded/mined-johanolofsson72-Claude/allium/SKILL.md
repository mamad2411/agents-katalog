---
name: allium
description: Allium specification language — elicit formal specs from markdown, distill specs from code. Sub-commands elicit and distill. Trigger on /allium, allium, elicit, distill, formal spec.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
user-invocable: true
argument-hint: "[elicit|distill] [spec-file-or-feature-path]"
---

# Allium Specification Skill

You write and manage `.allium` specification files — a formal spec language between natural language and TLA+.

## Sub-commands

| Command | When | What it does |
|---|---|---|
| `/allium:elicit` | Before implementation | Read a markdown spec, produce a `.allium` file |
| `/allium:distill` | After implementation | Read implemented code, extract a `.allium` from what was actually built |
| `/allium` (no sub-command) | Any time | Examine context, decide whether to elicit or distill |

Use `$ARGUMENTS` to determine the sub-command and target. If no argument, look at recent git changes.

## /allium:elicit — Spec to Allium

**Input:** A markdown spec file (spec*.md, tasks*.md, plan*.md, feature*.md)
**Output:** A `.allium` file saved in the same directory as the spec

### Process

1. **Find the spec file** — use `$ARGUMENTS` or find the most recently written spec in the project
2. **Read the spec thoroughly** — understand every requirement, constraint, edge case
3. **Extract entities** — every noun that has state, fields, or identity
4. **Extract rules** — state transitions, business operations, event handlers
5. **Extract invariants** — conditions that must ALWAYS hold across all entities
6. **Write the `.allium` file** in the same directory as the spec
7. **Validate** — `allium-check-hook.sh` runs `allium check` on the write and blocks on errors; fix and rewrite until it passes

### VALID TOP-LEVEL KEYWORDS (ONLY these — anything else is WRONG)

```
-- allium: 3          (REQUIRED first line)
--                    (comments)
enum                  (named union type)
entity                (domain object with identity)
external entity       (entity defined elsewhere)
value                 (value object, no identity)
config                (configuration constants)
rule                  (business operation: when/requires/ensures)
invariant             (global constraint, must ALWAYS hold)
actor                 (user role)
surface               (UI/API exposure)
deferred              (future work placeholder)
open question         (unresolved design decision)
```

**NOTHING ELSE is a valid top-level keyword.** Not `trigger`, not `contract`, not `action`, not `event`, not `handler`, not `workflow`, not `process`. If you're tempted to write a keyword not in this list — it goes inside a `rule` block as `when:/requires:/ensures:`.

### INVALID SYNTAX — do NOT use (Claude hallucinates these regularly)

| Wrong | Correct |
|---|---|
| `trigger OnEvent { ... }` | `rule Name { when: Event(...) ensures: ... }` |
| `contract Name { ... }` | `rule Name { when: ... requires: ... ensures: ... }` |
| `action Name { ... }` | `rule Name { when: ... ensures: ... }` |
| `forall x in Type:` | `for x in Collection where condition:` |
| `REQUIRE:` / `ENSURE:` (uppercase) | `requires:` / `ensures:` (lowercase) |
| `PRESERVE:` / `RETURNS:` | Not valid — express as `ensures:` postconditions |
| `NOT exists x WHERE ...` | `not exists x` or negate in `requires:` |
| `UUID → Entity.id` | `field: Entity` or `items: Type with field = this` |
| `UNIQUE(field1, field2)` | Express as `invariant` |
| No version marker | `-- allium: 3` MUST be line 1 |
| `enum { Val1, Val2 }` (comma-separated) | `enum Name { val1 \| val2 }` (pipe-separated, lowercase values) |
| `type: draft \| active` in enum | Inline unions go on entity fields, not in standalone types |
| `exposes: a, b` / `provides: a, b` | One clause per line: `exposes: a` then `exposes: b`. Measured against allium-cli 2026-09-02 — the comma list parses as a block item and is rejected |
| `entity User { id: String; role: String }` (one line, `;`-separated) | One field per line inside the braces. The first error in 27 of rocky's 130 unparseable baselines (measured 2026-09-26) |
| `when: Ship(order: Order)` (typed trigger parameters) | `when: Ship(order)`. The typed form parses as named arguments and binds nothing, so every `order.` below it is an undefined binding |
| `x = if c then a else b` | Not Allium. Use the block form `if c:` / `else:` inside `ensures:`, or one rule per outcome |
| `Float` / `Double` | `Decimal` |
| `[a, b]` list literals | `{a, b}` set literals, typed `Set<T>` |
| `for each x in xs:` | `for x in xs:` |
| `deferred X in "x.allium"` / `deferred X: "x.allium"` | `deferred X -- see: x.allium`. `in "…"` parses as a membership test and the colon form does not parse |
| `deferred X` (bare) or `deferred X -- src/x.cs` | `deferred X -- see: <path or URL>`. The location-hint lint reads only `-- see:`, a quoted path or an `http(s)://` URL after the name. Any other comment is not a hint, even when it names a file |
| Referencing a type you never declared (`Email.created(...)`) | Declare it, even as a stub `external entity Email { ... }` |

### Allium v3 language syntax

IMPORTANT: Always start files with the version marker `-- allium: 3` on the first line.

```allium
-- allium: 3

-- Comments use double-dash

enum Priority { low | medium | high | critical }

entity Order {
    customer: Customer
    total: Decimal
    priority: Priority                                             -- enum-typed field
    shipping_address: Address                                      -- value-typed field
    status: pending | confirmed | shipped | delivered | cancelled  -- inline union
    tracking_number: String when status = shipped | delivered      -- state-dependent
    notes: String?                                                 -- optional with ?
    shipped_at: Timestamp?
    cancelled_at: Timestamp?
    cancelled_by: String?

    transitions status {
        pending -> confirmed
        confirmed -> shipped
        shipped -> delivered
        pending -> cancelled
        confirmed -> cancelled
        terminal: delivered, cancelled
    }

    items: OrderItem with order = this       -- has-many relationship
    active_items: items where status = active -- filtered view
    is_complete: status = delivered           -- computed field
    item_count: items.count

    invariant NonNegativeTotal { this.total >= 0 }
}

entity Customer {
    email: String
    name: String
    role: customer | admin
}

external entity Email {
    to: String
    template: String
}

value Address {
    street: String
    city: String
    postcode: String
}

config { max_retries: Integer = 3 }

-- Creation: the rule that puts an entity into its first state
rule PlaceOrder {
    when: PlaceOrder(customer, total, priority, address)
    ensures: Order.created(
        customer: customer,
        total: total,
        priority: priority,
        shipping_address: address,
        status: pending
    )
}

-- Rules: when (trigger), requires (precondition), ensures (postcondition)
rule ConfirmOrder {
    when: ConfirmOrder(order)
    requires: order.status = pending
    ensures: order.status = confirmed
}

rule ShipOrder {
    when: ShipOrder(order, tracking)
    requires: order.status = confirmed
    ensures:
        order.status = shipped
        order.tracking_number = tracking
        order.shipped_at = now
}

rule DeliverOrder {
    when: DeliverOrder(order)
    requires: order.status = shipped
    ensures: order.status = delivered
}

rule CancelOrder {
    when: CustomerCancels(order)
    requires: order.status in {pending, confirmed}
    ensures:
        order.status = cancelled
        order.cancelled_at = now
}

-- Reactive rule: triggers on state transition
rule NotifyOnShipment {
    when: order: Order.status transitions_to shipped
    ensures: Email.created(to: order.customer.email, template: order_shipped)
}

-- Rule with if/else. Its requires admits only the declared edges into cancelled:
-- `status != delivered` would also admit shipped -> cancelled, which the graph does not declare.
rule ProcessCancellation {
    when: Cancel(order, reason)
    requires: order.status in {pending, confirmed}
    ensures:
        order.status = cancelled
        if reason = customer_request:
            order.cancelled_by = order.customer.name
}

-- Rule with iteration
rule BulkConfirm {
    when: BulkConfirm(batch)
    for order in batch.orders where order.status = pending:
        ensures: order.status = confirmed
}

-- Rule with let bindings
rule ComputeMetrics {
    when: MetricsRequested(doc)
    ensures:
        let count = doc.sections.count
        let avg = doc.word_count / count
        MetricsComputed(document: doc, average: avg)
}

-- Rule with collection ops and null safety
rule ValidateItems {
    when: Validate(order)
    requires: order.items.all(i => i.quantity > 0)
    ensures: ValidationPassed()
}

invariant AllDeliveredHaveTracking {
    for order in Orders where status = delivered:
        order.tracking_number != null
}

actor Admin { identified_by: Customer where role = admin }

surface OrderDashboard {
    facing viewer: Admin
    context order: Order where customer = viewer
    provides: CancelOrder(order) when order.status in {pending, confirmed}
    exposes: order.status
    exposes: order.tracking_number
}

deferred Order.fraud_check    -- see: fraud-check.allium
open question "How should partial shipments work?"
```

### Key syntax rules

1. **Version marker** — `-- allium: 3` MUST be the first line
2. **Comments** — `-- comment text`
3. **Types** — `String`, `Integer`, `Decimal`, `Timestamp`, `Duration`, `Boolean`, `Set<T>`
4. **Optional fields** — append `?` to type: `notes: String?`
5. **State-dependent fields** — `field: Type when status = state1 | state2`
6. **Inline union types** — `status: draft | active | archived` (lowercase values, pipe-separated)
7. **Named enums** — `enum Name { value1 | value2 }`
8. **Backtick literals** — for values with special chars: `` `no-cache` | `pt-BR` ``
9. **Transition graphs** — `transitions field { state1 -> state2; terminal: final_states }`
10. **Rules** — `when:` (event), `requires:` (precondition), `ensures:` (postcondition)
11. **Reactive triggers** — `when: entity: Type.field transitions_to value` or `becomes`
12. **Iteration** — `for x in Collection where condition:` inside rules or invariants
13. **Let bindings** — `let name = expression` inside ensures blocks
14. **Collection ops** — `.count`, `.sum(x => expr)`, `.all(x => expr)`, `.any(x => expr)`
15. **Null safety** — `?.` optional chaining, `??` null coalescing, `exists`, `not exists`
16. **Entity creation** — `Type.created(field: value, ...)` in ensures clauses

### Quality requirements for elicitation

The `.allium` file must be **more precise** than the markdown spec. This means:

- **Refuse vagueness.** If the spec says "validate input" — specify WHAT validation, WHAT input, WHAT happens on failure.
- **Name every constraint.** If there's a uniqueness requirement, express it as an invariant.
- **Explicit state machines.** If something has a status field, define a `transitions` graph with ALL valid transitions and terminal states.
- **No hand-waving.** "Handle errors appropriately" is not an Allium rule. Express it as a rule with `when:/requires:/ensures:`.

If the spec is too vague to formalize, add `open question "..."` entries or `-- AMBIGUITY:` comments. But still write the best possible spec — don't skip it.

### Hardening / fix / refactoring specs

These get `.allium` files too. For fix specs, entities are the things being fixed, rules capture the corrective actions with their preconditions and effects, and invariants express the constraints that were violated. There are NO exceptions to this.

## /allium:distill — Code to Allium

**Input:** Implemented code (source files, controllers, services, models)
**Output:** A `.allium` file representing what was actually built (saved with `-current` or `-distilled` suffix)

### Process

1. **Find the implementation** — use `$ARGUMENTS` or recent git changes
2. **Read all relevant source files** — models, controllers, services, middleware, validators
3. **Extract entities** from data models, DTOs, database schemas
4. **Extract rules** from API endpoints, event handlers, business logic (use `when:/requires:/ensures:` structure)
5. **Extract invariants** from validation logic, constraints, business rules
6. **Define transition graphs** from state machine logic in code
7. **Write the distilled `.allium` file**
8. **If a pre-implementation `.allium` exists** — compare and report drift (see below)

### Drift detection

When both a pre-implementation `.allium` (from elicit) and a distilled `.allium` (from code) exist:

```
ALLIUM DRIFT REPORT:

Specified but NOT implemented:
- Rule "OrderMustHaveItems" — no validation found in OrderService.Create()

Implemented but NOT specified:
- Endpoint DELETE /api/orders/{id}/force — exists in code, not in spec

Behavioral drift:
- Spec: "payment completes before order confirmation" (rule ConfirmOrder requires payment.status = paid)
- Code: allows order confirmation with status=PendingPayment
```

Each drift item is either a bug (code wrong) or a spec update (spec was incomplete) — flag both, let the developer decide.

## Findings handoff (BLOCKING — read `.claude/rules/validation-followup.md`)

Allium runs produce findings. Findings are the deliverable, not background reading. After ANY Allium run (elicit, distill, or no-arg invocation) the very next response MUST:

1. **List every finding individually** — drift items, `open question` entries, `-- AMBIGUITY:` comments, `deferred` markers, "spec too vague to formalize" notes, validation errors from `allium check`. One numbered line per finding, citing source path and Allium construct.
2. **Call `AskUserQuestion` with one question per finding** — batched in a single tool call. Each question offers `Fix now`, `Defer (track in spec)`, `Dismiss (with reason)`, plus a bespoke option where relevant (e.g. `Update spec instead of code` for drift items). Frame the language so `Fix now` is the default-feeling option.
3. **If there are zero findings** — say verbatim: "Allium run complete. Zero drift, zero open questions, zero ambiguities." If you cannot say that and mean it, you have findings — go back to step 1.

Forbidden: "looks good overall" summaries, silently fixing easy items while ignoring hard ones, asking a single vague "want me to address the issues?" question, or continuing to the next task with findings undecided.

This rule applies whether the skill was invoked manually (`/allium`, `/allium:elicit`, `/allium:distill`) or automatically (post-spec hook, `/tla` step 0, feature workflow). The trigger does not change the obligation.

## Validation

`scripts/allium-check-hook.sh` runs `allium check` after every write and blocks on any
`severity: error`. When it blocks, fix the listed lines and write the file again. Warnings do not
block. If the CLI is not installed the hook says so once and lets the write through: still write the
file, but check it by hand against the INVALID SYNTAX table above, because nothing else will.

**CLI floor: 3.3.0.** Older CLIs warn `allium.deferred.missingLocationHint` on every `deferred`,
whatever follows it. The hook notices a pre-3.3 CLI and says so once per session. On 3.3.0 and
later that warning is real: the line has no pointer, so add `-- see: <path>`.

**Known false positive (allium-cli ≤ 3.6.1, measured 2026-09-30):**
`allium.status.unreachableValue` ("Status 'x' in entity 'E' is never assigned by any rule ensures
clause") fires when two entities declare a field with the **same name** (typically `status`) and
the assigning rule binds the entity through an untyped trigger parameter (`when: SyncPush(item)`
followed by `ensures: item.status = refused`). The checker cannot tell which entity `item` is, so
it credits the assignment to neither. Fix it by giving the fields distinct names (`push_status`,
`response_status`). That works on every version. Do not type the trigger parameter: the INVALID
table forbids it.

## Auto-install Allium CLI

If the CLI is not installed and you need validation:

```bash
if ! command -v allium &>/dev/null; then
  if command -v brew &>/dev/null; then
    brew tap juxt/allium && brew install allium
  elif command -v cargo &>/dev/null; then
    cargo install allium-cli
  fi
fi
```

---
name: shapes-context
description: >
  Teaches the Shapes Specification and shapes-first workflow. Triggers
  when starting work in a project with a .shapes/ directory, or when exploring
  project architecture, intent, constraints, or shape graph structure. Covers
  node types, DAGs, lifecycle, bindings, profiles, and the shapes-first
  principle: plan changes in the graph before writing any code.
user-invocable: true
---

```!
shapes preflight 2>/dev/null || echo "Shapes CLI not found. Install it: cargo install shapes-cli"
```

# Shapes Specification

## Contents

- The Shapes-First Principle
- The Spec (node types, DAGs, intent, profiles, bindings, lifecycle)
- Shapes-First Workflow
- Writing Good Shapes and Constraints
- Related Skills
- CLI Reference

## Related Skills

- `/shapes:shapes-init` — bootstrap a new project with shapes, profiles, and constraints
- `/shapes:shapes-archive` — walk amendments and archive stale ones
- `/shapes:shapes-maintain` — keep the shapes graph in sync with code changes;
  includes the decision framework for amendments vs new shapes vs direct edits

## The Shapes-First Principle

**No code changes without shapes changes first.** The graph is the plan;
code is the execution. Before writing or modifying any source code:

1. Create or amend the relevant shapes, constraints, or amendments
2. Capture what you intend to build, change, or enforce
3. Only then write the code that realizes that intent

This applies to every kind of work:
- **New feature** — create the shape first, then implement it
- **Bug fix** — amend the affected shape or add a constraint first, then fix
- **Refactor** — update shapes to reflect the new structure first, then move code
- **New rule** — create the constraint first, then enforce it in code

The graph is not documentation written after the fact. It is the source of
intent that drives implementation.

## Prerequisites

The `shapes` CLI must be installed. If `shapes --help` doesn't work, install it:

```bash
cargo install shapes-cli
```

Run `shapes --help` and `shapes <command> --help` for all commands and flags.

## The Specification

Shapes is an open specification that captures the **intent**, **constraints**,
and **boundaries** of a project as a structured, queryable graph. It is
**domain-agnostic** — it applies to software, research, writing, and any
structured endeavor. Only the Profile configuration and Intent vocabulary
change between domains.

### Four Node Types

| Node | Purpose |
|------|---------|
| **Shape** | What to build and why — the primary work node |
| **Constraint** | Rules that must be satisfied — strict invariants |
| **Amendment** | Immutable change record — evolves the graph over time. Carries an optional `archived` object with a required `reason` to hide decayed entries from default listings without losing the audit trail. |
| **Profile** | Governance configuration — defines lifecycle, custom fields, amendment rules |

### Two DAGs

Shapes and Constraints each form their own **Directed Acyclic Graph** through
parent/child relationships. These are independent graphs:

- **Shape DAG** — composition hierarchy (system > services > features > ...)
- **Constraint DAG** — policy decomposition (policy > sub-rules > ...)

Shapes reference Constraints by ID. When you traverse a Shape's ancestors, you
discover all constraints that apply — constraints are inherited downward.

### Intent: The Open Map

Every Shape, Constraint, and Amendment carries an **Intent** with three
required fields:

- **kind** — domain label (free-form string)
- **summary** — human-readable description
- **source** — origin (human, ai, system)

Beyond these, Intent is an **open map**. Each domain extends it with its own
vocabulary. The spec doesn't prescribe which fields exist — that's the
Profile's job.

### Profiles: Defining What Fields Matter

A **Profile** governs how Shapes and Constraints behave in a domain. It:

- **Declares custom fields** via FieldDef — name, description, type, and
  whether required or optional. Fields can be declared for intent, status,
  constraints, realization, evidence, provenance, and metadata sections.
- **Defines lifecycle gates** — preconditions for state transitions
- **Specifies allowed kinds** — what `kind` values are valid
- **Chooses amendment model** — merge, overlay, edition, or append-only

### Bindings

Bindings connect Shapes to external artifacts via a `scheme` and `value`.
For source code, use `scheme: path` with a repository-relative file path.
Add `metadata.summary` to describe what the binding points to — the
specific structs, functions, or sections relevant to this shape:

```yaml
realization:
  - bindings:
      - scheme: path
        value: src/model/intent.rs
        metadata:
          summary: Intent struct — open map with kind/summary/source + flattened extra fields
    role: primary
```

The summary gives agents semantic context about what's in the file without
having to read it. This is especially valuable when multiple shapes point
to the same file — each summary describes the relevant portion.

**Realizations** connect Shapes to deliverables (code, docs, services). Each
has bindings and a `role` (primary, supporting, test).

**Evidence** demonstrates constraint satisfaction — type (test, review, metric),
trusted indicator, and bindings to verification artifacts.

**Provenance** tracks decision history — links to discussions, reviews, sessions.

### Lifecycle

Seven states: proposed > promoted > canonical (progressive), plus rejected,
superseded, abandoned, reverted (terminal). Direct edits allowed while
`proposed`; `promoted`/`canonical` changes require Amendments.

## Shapes-First Workflow

When a project has `.shapes/`, the graph drives all work. No code changes
happen until the graph reflects what you intend to do.

### Step 1: Discover Context

1. **See the big picture** — `shapes tree shape` gives the full hierarchy
   in one call. Start here — don't read shapes one-by-one. Only call
   `shapes get shape <id>` for the 2-4 shapes you plan to modify, not
   every shape in the tree.
2. **Load all constraints** — `shapes tree constraint` shows the constraint
   hierarchy. Then `shapes query constraints <shape-id>` to see which
   constraints apply to the shape you're about to change.
3. **Read the specific shapes** — `shapes get shape <id>` for the intent,
   goals, non-goals, and realization bindings of shapes you'll modify.
4. **Read amendments (mandatory on continuations)** — `shapes list amendment`
   to see the change history. On continuation sessions this is mandatory —
   amendments tell you *what changed and why* in prior iterations. Skip
   only on the initial bootstrap when no amendments exist yet.
   By default, `shapes list amendment` and `shapes get <parent>` hide
   archived amendments (entries whose insight value has decayed). They
   stay on disk for audit — pass `--archived` if you suspect the answer
   to a question lives in an archived entry. When reading a shape with
   `shapes get <parent> --archived`, archived entries in
   `amendment_log` are annotated with their archival reason so you can
   recognize them and decide whether to read them.

### Step 2: Plan in the Graph

Before writing any code, update the graph to capture your planned changes.
**The graph is the plan. Code is the execution.** If the graph doesn't
reflect what you're about to do, stop and update it first.

- **New feature** — `shapes create shape` with intent, parent links, constraints.
  Then edit the YAML to flesh out goals, non_goals, rationale.
- **Changing an existing feature** — create an amendment first:
  `shapes create amendment --target-shape <id> --name "Add X" --summary "Why"`.
  Amendments are the change log. Even if the shape is `proposed` and you could
  edit directly, prefer amendments for non-trivial changes — they document
  *what changed and why* so future iterations can read the history.
- **New rule or invariant** — `shapes create constraint` with a specific,
  falsifiable rule. Link it to the relevant shapes.
- **Bug fix** — create an amendment documenting the fix, then add a constraint
  to prevent recurrence.

Edit the YAML to flesh out intent fields, add parent/child references, and
link relevant constraints. This is your plan.

### Step 3: Write Code

Now implement what the graph describes. The shapes you created or amended
define the scope — don't exceed it without updating the graph first.

#### Before writing: reuse check

Before creating any new function, type, or module, check realization bindings
on the target shape and its siblings — they point to files that may already
contain what you need. Search the codebase for similar implementations.
Extend existing code rather than duplicating.

#### While writing: stay within shape scope

The shapes you created or amended define the boundaries of this change.
Write code that realizes the shape's intent — nothing more, nothing less.

- **One shape, one responsibility.** Each shape maps to a focused unit of
  code. If a function serves multiple shapes, it likely needs to be split
  so each piece can be bound to the right shape.
- **Respect non-goals.** The shape's `non_goals` field defines what is out
  of scope. Don't implement functionality that falls outside the shape's
  declared intent.
- **Match the decomposition.** If the graph has child shapes for distinct
  components, the code should reflect that structure — separate functions
  or modules for each child, not a monolithic implementation.

#### After writing: constraint verification (mandatory)

This step is not optional. Before proceeding to Step 4, verify every
constraint against the code you wrote.

```bash
shapes tree constraint
```

Then for each constraint:

1. **Read the constraint's `rule` field.** State it to yourself explicitly.
2. **Check the code against it.** The rule is specific and falsifiable — you
   can verify it by reading the code. If the code violates the rule, fix it
   now.
3. **Check scope.** Did you modify code outside the shapes you planned to
   change? If so, either update the graph to reflect the broader scope or
   revert the unplanned changes.
4. **State the result** for each constraint: satisfied or violated. Fix
   violations before proceeding.

### Step 4: Bind Realizations

After code is written, add realization bindings to connect shapes to the
files you created or modified. The shapes-maintain skill auto-triggers here
with the full decision framework for updating realizations.

### Respecting Constraints

Constraints from `shapes query constraints <id>` apply to your work. Read
each constraint's `rule` field. Constraints are inherited — a constraint on
a parent shape applies to all descendants.

## Writing Good Shapes and Constraints

### Shapes

A shape should capture enough context that someone who has never seen the
code can understand what it is, why it exists, and what rules govern it.
The specific fields depend on the project's Profile. But thin, one-liner
shapes waste the opportunity to capture the meaning behind the code.

### Constraints

A constraint is only useful if its `rule` is specific enough to verify.
Vague rules like "be secure" aren't actionable. Good rules state a
falsifiable invariant an agent can check by reading the code.

The `description` should explain why the rule exists. Without the "why,"
future contributors won't understand the cost of violating it.

## CLI Reference

### Create commands (exact flags)

```bash
# Create a shape (required: --name, --kind, --summary)
shapes create shape --name "Name" --kind module --summary "Description" --profile 1

# Create a constraint (required: --name, --kind, --rule)
shapes create constraint --name "Name" --kind invariant \
  --rule "Specific falsifiable rule" --enforcement machine

# Create an amendment (required: --name, --target-shape OR --target-constraint, --summary)
shapes create amendment --name "Change description" \
  --target-shape 5 --summary "What changed and why"

# Create a profile (required: --name)
shapes create profile --name "Project Profile"
```

### Query commands

```bash
shapes tree shape                        # Full shape hierarchy (start here)
shapes tree constraint                   # Full constraint hierarchy
shapes get shape <id>                    # Read a shape's full definition
shapes get constraint <id>               # Read a constraint's full definition
shapes query constraints <shape-id>      # Constraints that apply (inherited)
shapes list amendment                    # All amendments (change history)
shapes validate                          # Check graph integrity (exit 0 = clean)
```

### Editing shapes

There is no `shapes edit` command. Edit YAML files directly at
`.shapes/shapes/<id>-<name>.yaml`. After creating with `shapes create`,
flesh out the YAML to add parent/child links, constraints, realization
bindings, and rich intent fields.

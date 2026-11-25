---
name: business-logic-entry-point-command-query-separation
description: Enforce Command-Query Separation specifically at business-logic entry points. Use when an agent needs to create, modify, review, or interpret public functions, methods, handlers, use cases, application services, facades, or similar entry points that trigger business logic. Classify each entry point as either a command that changes state or a query that returns data, never both. The only allowed data return from a command is the ID or IDs of domain entities created by a create operation.
---

# Command-Query Separation for Business Logic Entry Points

## Goal

Apply Command-Query Separation at entry points to business logic.

Treat each business-logic entry point as exactly one of these:

- a command, which changes state
- a query, which returns data without changing state

Do not mix the two in the same entry point.

This skill governs CQS, not CQRS. It is a design rule for the behavior and return shape of individual business-logic entry points. It does not require separate read and write models, separate stores, separate services, or distributed architecture changes.

The only allowed exception to the no-data-return rule for commands is a create operation. A create command may return the ID of the created domain entity, or the IDs if the create operation creates more than one domain entity, so the caller can continue acting on those newly created entities.

## What Counts as In Scope

Apply this skill to code that does one or more of these things:

- defines a public function or method that starts a business workflow
- defines a use case, application service method, interactor, handler, facade, or similar business-logic entry point
- changes the return shape of a business operation
- combines reading and writing behavior in one business-facing entry point
- exposes command or query behavior to callers of business logic

## CQS Rule

1. Classify every business-logic entry point as either a command or a query.
   - A command changes business state.
   - A query returns business data.
   - Do not let one entry point do both.

2. Commands must not return business data.
   - Use `void`, `unit`, `undefined`, `None`, or the closest equivalent when the stack allows it.
   - If the project uses result wrappers or error envelopes, keep those patterns without adding read-model payloads to commands.

3. Create commands may return created entity IDs only.
   - A create command may return the ID of the created domain entity.
   - If one create operation creates multiple domain entities, it may return the set or collection of created IDs.
   - Do not return the full created entity, a read model, derived business data, or other additional payload from a create command.

4. Queries must not change business state.
   - Do not persist writes, emit business-changing side effects, transition entity state, or trigger state-changing workflows inside a query.
   - Keep queries observational.

5. Split mixed entry points instead of compromising the rule.
   - If one entry point both changes state and returns data, separate it into a command and a query, or move the extra read to a follow-up query by the caller.

## Detection Workflow

1. Find the business-logic entry points first.
   - Identify public functions, methods, handlers, or use cases that callers invoke to trigger business behavior.
   - Focus on the boundary where a caller asks the business logic to do something or to answer something.

2. Determine whether the entry point changes state.
   - Check whether it creates, updates, deletes, approves, assigns, schedules, cancels, or otherwise changes domain or persisted state.
   - Check whether it triggers business side effects that are part of changing state.

3. Determine whether the entry point returns data.
   - Identify whether it returns domain entities, read models, DTOs, counts, lists, booleans, summaries, or other business-facing results.
   - If it both changes state and returns data, treat that as a CQS violation unless it is returning only created IDs from a create operation.

4. Prefer semantic classification to naming.
   - Do not trust names like `get`, `create`, `handle`, or `execute` by themselves.
   - Classify by actual behavior and return shape.

## Writing or Changing Business-Logic Entry Points

1. Choose the role first.
   - Decide whether the entry point is a command or a query before writing the code.
   - Let that choice determine side effects and return type.

2. Write commands as state-changing operations with minimal return values.
   - Return no business data from commands.
   - For create commands, return only the created entity ID or IDs.

3. Write queries as read-only operations.
   - Return the requested business data.
   - Keep them free of business-state mutations.

4. Refactor mixed entry points by separation.
   - Move write behavior into a command entry point.
   - Move data retrieval into a query entry point.
   - Let callers perform the query after the command when they need additional data beyond created IDs.

5. Keep the boundary explicit.
   - Make the command or query role obvious in the method behavior, return type, and surrounding API.
   - Do not hide writes inside a supposedly read-only entry point.

## Review Questions

When reading or reviewing code, ask:

- Is this entry point a command or a query?
- Does it change business state?
- Does it return business data?
- If it is a command, is it returning anything other than created entity IDs for a create operation?
- If it is a query, is it truly free of business-state changes?

If the answer is yes, apply this skill.

## Report the Outcome

When finishing the task:

- state which business-logic entry points were identified or changed
- state which ones are commands and which ones are queries
- state where mixed command-query behavior was removed or prevented
- state whether any create commands return created entity IDs, and only those IDs

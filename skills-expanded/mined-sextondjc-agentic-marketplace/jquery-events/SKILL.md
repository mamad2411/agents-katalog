---
name: jquery-events
description: Use when implementing or reviewing jQuery event binding, delegation, namespace management, custom events, and event-object handling with correct memory and performance discipline.
---

# jQuery Events

## Specialization

Implement and review expert-level jQuery event handling covering `.on()` / `.off()` lifecycle, event delegation patterns, namespace isolation, custom event contracts, and event-object consumption — grounded in official jQuery API documentation.

## Trigger Conditions

- Binding or unbinding event handlers with `.on()`, `.one()`, or `.off()`.
- Implementing event delegation to handle dynamically inserted elements.
- Designing event namespaces to enable targeted unbinding.
- Triggering programmatic events with `.trigger()` or `.triggerHandler()`.
- Creating or consuming custom events via `.on()` + `.trigger()`.
- Reviewing event handler accumulation, memory leaks, or duplicate binding defects.
- Migrating from deprecated `.bind()`, `.unbind()`, `.live()`, `.die()`, `.delegate()`, `.undelegate()` APIs.

## Scope Boundaries

In scope:

- `.on()`, `.off()`, `.one()`, `.trigger()`, `.triggerHandler()` API contracts.
- Event delegation patterns — selector argument in `.on()`.
- Event namespacing — `'click.myns'` patterns.
- Custom event design: naming conventions, payload via `eventData`, and consumer contracts.
- Event object properties: `event.target`, `event.currentTarget`, `event.stopPropagation()`, `event.preventDefault()`.
- Preventing handler accumulation and memory leaks from unbound handlers on removed elements.

Out of scope:

- DOM traversal used to identify delegation targets (see `jquery-core`).
- AJAX-triggered events like `ajaxStart`/`ajaxStop` (see `jquery-ajax`).
- Plugin event systems built on top of jQuery events (see `jquery-plugins`).

## Inputs

- Element context — static vs. dynamically inserted.
- Event type(s) and cardinality (fire-once vs. recurring).
- Delegation root candidate.
- jQuery version in use.
- Existing handler bindings to audit.

## Required Outputs

- Correct `.on()` binding with delegation or direct-binding rationale.
- Namespace plan for targeted `.off()` unbinding.
- Custom event contract (name, payload schema, consumer expectations) if applicable.
- Memory-safety confirmation: handlers unbound before element removal.
- Migration recommendation if deprecated API is found.

## Core Patterns

### Prefer `.on()` for All Bindings

- Always use `.on()`. Never use `.bind()`, `.live()`, `.delegate()`, or `.click(handler)` shorthand in new code.
- Use `.one()` for handlers that must fire exactly once; it auto-unbinds after first invocation.

### Event Delegation

- Delegate to the closest stable ancestor, not `document` or `body`, to minimize bubbling distance.
- Delegation syntax: `$(stableParent).on('click', '.dynamic-selector', handler)`.
- Use delegation when elements are dynamically inserted after page load — direct binding on transient elements leaks if elements are removed without unbinding.
- Do not delegate events that do not bubble (`focus`, `blur`) — use `focusin`/`focusout` which do bubble.

### Namespacing

- Always namespace handlers: `$(el).on('click.featureName', handler)`.
- Unbind by namespace to avoid removing unrelated handlers: `$(el).off('.featureName')`.
- Use compound namespaces for fine-grained control: `'click.ui.modal'`.
- Component teardown must call `.off('.componentNamespace')` on all bound elements.

### Custom Events

- Name custom events with a project prefix to avoid collision: `'app:itemSelected'`.
- Pass structured data via the `eventData` object in `.trigger('app:itemSelected', [payload])`.
- Consumer receives payload as additional arguments after the event object: `function(event, payload)`.
- Do not use `.trigger()` for native browser events unless simulating user interaction in tests — use `.triggerHandler()` when the native event side-effects are unwanted.

### Event Object

- Use `event.preventDefault()` to stop default browser behavior (form submission, link navigation).
- Use `event.stopPropagation()` to prevent bubbling; use `event.stopImmediatePropagation()` to also cancel remaining handlers on the same element.
- Access `event.target` for the element that fired; `event.currentTarget` for the element the handler is bound to.
- In delegated handlers, `event.currentTarget` is the delegation root; `event.target` is the clicked child.

### Memory Safety

- Unbind all handlers before removing or replacing elements that hold closures over large scopes.
- Use `.detach()` instead of `.remove()` when temporarily removing elements to preserve handler bindings.
- In long-lived SPAs, call `.off('.ns')` in component teardown to prevent handler accumulation on reused DOM.

### Deprecated API Migration

| Deprecated | Replacement |
|---|---|
| `.bind(event, handler)` | `.on(event, handler)` |
| `.unbind(event)` | `.off(event)` |
| `.live(event, handler)` | `$(document).on(event, selector, handler)` |
| `.die(event)` | `$(document).off(event, selector)` |
| `.delegate(sel, event, handler)` | `$(parent).on(event, sel, handler)` |
| `.undelegate(sel, event)` | `$(parent).off(event, sel)` |

## Workflow

1. Classify element as static or dynamically inserted — determine delegation need.
2. Choose delegation root: closest stable ancestor.
3. Define namespace for every binding.
4. Design custom event contract if cross-component communication is needed.
5. Confirm `.off()` call is paired with element removal or component teardown.
6. Audit existing code for deprecated API usage and record migration plan.
7. Verify delegated events bubble (use `focusin`/`focusout` not `focus`/`blur`).

## Done Criteria

- All handlers use `.on()` with a namespace.
- Delegated handlers target the closest stable ancestor.
- Custom events use project-prefixed names and documented payloads.
- Every binding has a corresponding `.off()` in teardown.
- No deprecated event API remains.

## References

- [jQuery API: Events](https://api.jquery.com/category/events/)
- [jQuery API: .on()](https://api.jquery.com/on/)
- [jQuery API: .off()](https://api.jquery.com/off/)
- [jQuery API: .trigger()](https://api.jquery.com/trigger/)
- [jQuery Learn: Events](https://learn.jquery.com/events/)
- [jQuery Learn: Event Delegation](https://learn.jquery.com/events/event-delegation/)
- [jQuery Migrate: Event API Changes](https://github.com/jquery/jquery-migrate)

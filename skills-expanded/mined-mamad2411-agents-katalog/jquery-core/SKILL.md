---
name: jquery-core
description: Use when implementing or reviewing jQuery DOM selection, traversal, manipulation, and method chaining patterns with correct selector performance and modern API usage.
---

# jQuery Core

## Specialization

Implement and review expert-level jQuery DOM interaction covering selector strategy, traversal, manipulation, attribute and data handling, and method chaining — grounded in official jQuery API documentation.

## Trigger Conditions

- Writing or reviewing jQuery DOM selection logic.
- Implementing traversal chains (`find`, `closest`, `children`, `siblings`, `parent`).
- Performing DOM manipulation: `append`, `prepend`, `before`, `after`, `remove`, `detach`, `clone`.
- Managing attributes, properties, classes, and inline styles via jQuery API.
- Using `.data()` for element-bound data storage.
- Reviewing or authoring method chains for correctness and readability.
- Choosing between jQuery methods and native equivalents (`querySelectorAll`, `classList`, `dataset`).

## Scope Boundaries

In scope:

- jQuery selector syntax and Sizzle selector engine behavior.
- DOM traversal — tree navigation and filtering methods.
- DOM manipulation — structural insertions, removals, replacements, cloning.
- Attribute, property, class, and style management.
- `.data()` cache usage and cleanup.
- Method chaining best practices and end-of-chain state management.
- Choosing jQuery methods vs. native browser API equivalents.

Out of scope:

- Event handling (see `jquery-events`).
- AJAX patterns (see `jquery-ajax`).
- Effects and animation (addressed within `jquery-core` where performance implications exist, but advanced sequencing belongs in `jquery-plugins`).
- Plugin authoring (see `jquery-plugins`).

## Inputs

- Target element context and page lifecycle stage (DOM-ready vs. dynamically inserted).
- jQuery version in use.
- Browser target matrix (if IE compatibility constraints apply).
- Existing selector patterns to review.

## Required Outputs

- Correct selector patterns with performance rationale.
- Traversal chain with minimal DOM re-query.
- Manipulation sequence using detach-mutate-reattach where applicable.
- `.data()` usage with explicit cleanup obligations.
- Native equivalent recommendation where jQuery overhead is unjustified.
- Security note for any context using `.html()` with dynamic content (route to `jquery-security`).

## Core Patterns

### Selector Efficiency

- Prefer ID selectors `$('#id')` as the fastest path — maps directly to `getElementById`.
- Scope selectors to a cached context: `$('.item', cachedParent)` over unconstrained `$('.item')`.
- Avoid universal selectors (`$('*')`) and over-qualified selectors (`$('div.class')` where `$('.class')` suffices).
- Cache jQuery objects that are referenced more than once: `const $el = $('#target');` — never re-query the same element in a loop.

### Traversal

- Use `.find()` on a cached wrapper rather than constructing a new selector from scratch.
- Use `.closest()` for event delegation contexts — stops at the first matching ancestor.
- Use `.children()` over `.find()` when the target is a direct child — avoids deep tree walk.
- Prefer `.filter()` over chained `.is()` checks when narrowing a collection.

### Manipulation

- Use `detach()` instead of `remove()` when reinserting the element — `detach()` preserves jQuery event and data cache.
- Batch DOM mutations: build HTML strings or document fragments off-DOM, then insert once.
- Use `.clone(true)` only when event handlers must copy; otherwise use `.clone()` to avoid handler accumulation.
- Avoid `.html(userInput)` with unsanitized data — see `jquery-security`.

### Attributes, Properties, and Classes

- Use `.prop()` for boolean DOM properties (`checked`, `disabled`, `selected`); use `.attr()` for HTML attribute values.
- Use `.addClass()`, `.removeClass()`, `.toggleClass()` rather than `.attr('class', ...)` to avoid wiping existing classes.
- Use `.css()` sparingly; prefer adding/removing CSS classes to keep styles in stylesheets.

### Data Cache

- Use `.data(key, value)` to associate state with DOM elements without polluting the element's dataset.
- Call `.removeData()` before removing elements that hold large references to prevent memory leaks.
- Avoid reading `.data()` values set via HTML `data-*` attributes after mutation — jQuery caches the initial read.

### Native API Decision Rule

- Prefer native equivalents in projects targeting modern browsers where the native API is equally expressive: `document.querySelector`, `element.classList`, `element.dataset`.
- Retain jQuery when the project already depends on it for event delegation or AJAX and adding a native branch increases inconsistency.

## Workflow

1. Identify selector context and DOM lifecycle stage.
2. Evaluate selector efficiency; cache repeated queries.
3. Choose traversal method with the narrowest scope.
4. Plan manipulation sequence; apply detach-mutate-reattach for batch DOM changes.
5. Classify attribute/property targets; use `.prop()` vs `.attr()` correctly.
6. Apply `.data()` for state; schedule `removeData()` with element removal.
7. Flag any `.html(dynamic)` usage for `jquery-security` review.
8. Recommend native equivalent where jQuery overhead is unjustified.

## Done Criteria

- All selectors are cached where reused.
- Traversal chains use the narrowest-scope method.
- DOM mutations are batched.
- `.prop()` vs `.attr()` is used correctly for every property.
- `.data()` cleanup is paired with element removal.
- No unsanitized dynamic content is passed to `.html()`.

## References

- [jQuery API: Selectors](https://api.jquery.com/category/selectors/)
- [jQuery API: Traversing](https://api.jquery.com/category/traversing/)
- [jQuery API: Manipulation](https://api.jquery.com/category/manipulation/)
- [jQuery API: Attributes](https://api.jquery.com/category/attributes/)
- [jQuery API: Data](https://api.jquery.com/data/)
- [jQuery Learn: How jQuery Works](https://learn.jquery.com/about-jquery/how-jquery-works/)
- [jQuery Learn: Performance](https://learn.jquery.com/performance/)

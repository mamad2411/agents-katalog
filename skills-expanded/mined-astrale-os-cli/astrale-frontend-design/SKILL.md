---
name: astrale-frontend-design
description: "Design, implement, review, and refine focused product interfaces for Astrale Domain Views embedded in the Astrale GUI. Use when working on information architecture, layout, React or UI components, forms, lists, menus, dialogs, loading/empty/error/mutation states, interaction polish, responsive behavior, accessibility, or interface copy in a Domain frontend."
---

# Astrale Frontend Design

Build the Domain as a focused product interface, not a landing page. Domains live inside the
Astrale GUI and inherit its surrounding shell. Do not add a hero, large presentation area,
redundant page header, or empty space before useful content.

Apply this skill together with `astrale-domain` View guidance. Reuse the host application's visual
language and the project's existing primitives unless the task establishes a different direction.

## Plan The Information Architecture

Before writing UI code, sketch a high-level wireframe mentally or in a temporary note. Identify:

- the user's primary task;
- the main sections and subsections;
- the logical links between them;
- their relative importance;
- which information belongs together;
- the correct parent for every subsection.

Make every section one coherent logical unit. Let information architecture and task priority drive
the layout, order, space, and visual weight. Put state and controls close to the content they affect.

## Keep The Interface Restrained

Avoid AI-slop aesthetics. Do not turn every element into a card, nest containers without a real
grouping need, or make cards lift on hover. Use hover only to clarify interaction, and provide the
same clarity for keyboard and touch users.

Prefer a small number of strong regions, clear hierarchy, compact spacing, and consistent controls.
Do not add decorative gradients, pills, oversized metrics, animation, or ornamental copy by default.
Each visual device must communicate structure, state, priority, or affordance.

## Make Interaction States Precise

Model the relevant initial, loading, empty, ready, submitting, success, failure, unauthorized, and
disabled states before considering a flow complete.

- Show loading at the scope that is actually waiting: inside a submitted button for a local action,
  or with a page skeleton for initial page content. Never show multiple loaders for one action.
- Prevent duplicate submissions. Preserve user input on failure and place actionable feedback next
  to the affected control or content.
- Handle creation clearly: show that the action succeeded, insert the result where the user expects
  it, and move focus only when doing so helps the next task.
- Handle deletion clearly: distinguish reversible removal from destructive deletion and confirm only
  when the consequence warrants interruption.
- Use optimistic list updates when the result is predictable. Roll back on failure, show the failure,
  and reconcile the interface with committed Kernel state.
- Close an open dropdown when the user clicks outside it or presses Escape. Support keyboard
  navigation, expose the selected item, and return focus to the trigger when appropriate.
- Make long labels and values part of layout testing. Wrap when reading matters; truncate only in
  genuinely fixed space and provide access to the full value. Never let text cover adjacent actions.
- Keep dialogs, menus, forms, and inline actions usable by keyboard. Use visible focus, semantic
  controls, correctly associated labels, and accessible status or error announcements.
- Make hover, disabled, pending, success, and error states visually distinct without relying on color
  alone.

## Reduce Text Deliberately

Keep only text that helps the user understand the state, decide, or act. Preserve necessary labels,
feedback, and accessibility text. Remove introductions, repetition, obvious help, decorative copy,
and descriptions that merely restate a heading or control.

After implementation, perform a dedicated text-reduction pass. Read every visible string in context
and remove it unless the interface becomes harder to understand, decide from, or act on.

## Verify The Result

Exercise the real task flows with representative, empty, long, loading, and failing data. Check
creation, deletion, rollback, outside-click and Escape behavior, keyboard order, narrow layouts, and
visible feedback. Then review the whole screen once more and remove redundant cards, effects, copy,
and space before useful content.

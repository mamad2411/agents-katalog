---
name: keyboard-navigation-review
description: "Review browser keyboard journeys for reachability, focus order, traps, menu or composite-widget keys, and focus restoration. Use for web keyboard-navigation and tab-order behavior; not native game controls, terminal shortcuts, or cosmetic changes."
license: MIT
metadata:
  version: "1.0"
---

# Keyboard navigation review

Evaluate a bounded task with real browser key presses. Synthetic keyboard
evidence is useful but is not complete assistive-technology evidence.

## Workflow

1. Define the starting URL/state, viewport, task completion condition, and
   expected focus behavior.
2. Use the available browser tool, established project test runner, or a
   manual keyboard review. Follow the bounded actions in
   [references/journey-review.md](references/journey-review.md) through the
   tool's documented API. This skill does not require the upstream a11y-agent
   CLI, a new browser runtime, or an MCP server.
3. Check reachability, visible focus, logical sequence, traps, skip links,
   composite-widget arrow-key behavior, route/state changes, dialog entry, and
   focus restoration.
4. Record every action, resulting focused element, accessible name, and failure
   reason.
5. Replay any repair from the identical starting state and add a
   behavior-focused regression journey.

## Boundaries

Do not infer that a passing scripted journey works with every keyboard layout,
switch device, voice input system, browser, or screen reader. Manual review
remains required for visual focus quality and task-level sequence judgment.

## Local integration

Use only tooling already available for the task or dependencies justified by
the requested implementation. Follow browser-tool access rules. Keep source
review, synthetic/component tests, browser observation, and assistive-technology
validation distinct; do not claim unperformed checks. Preserve project scope
and existing authorization for external actions.

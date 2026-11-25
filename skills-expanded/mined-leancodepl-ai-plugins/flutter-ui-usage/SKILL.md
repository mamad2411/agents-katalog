---
name: flutter-ui-usage
description: Explain what the `flutter-ui` plugin does and how to use it. Use when the user invokes `/flutter-ui-usage`, asks what this plugin covers, or needs help with design-system-driven UI, shared loading/error patterns, or presentation-layer localization.
---

# UI Usage

## How to respond

- If the user invoked this skill without a concrete task, start by explaining what this plugin does and what kind of UI work it is meant for.
- Show how to use it through concrete presentation-layer tasks this plugin can handle.
- Point to the main UI rule or the dedicated UI skill, and route to sibling plugins when the task becomes state-management, localization, or route-structure specific.
- If the user already gave a concrete UI task, briefly explain why this plugin fits and then do the work.
- Do not reply with filler like "skill loaded", "ready for the task", or "what would you like to do?" before explaining the plugin.

## What this plugin does

- Covers design-system-driven presentation-layer implementation in Flutter.
- Guides shared loading and error patterns across screens.
- Helps keep user-facing text localized and UI state aligned with LeanCode presentation conventions.

## How to use it

- Ask to build or refactor a page or widget using the existing design system.
- Ask to align a screen with shared loading and error patterns.
- Ask whether a shared component belongs in the design system or in feature code.
- Ask how UI work should connect to localization or page-level state management.

## Example requests

- "Implement a settings page using existing design-system components."
- "Refactor this screen to use the project's loading and error patterns."
- "Should this widget live in the design system or stay inside the feature?"

## Reach for these assets

- `references/ui-design-system.md` - design-system and presentation-layer UI conventions.
- `skills/ui/SKILL.md` - checklist for implementing or refactoring feature UI.
- `skills/ui/reference.md` - short UI checklist.
- Related plugin: `flutter-bloc` - page state-management conventions.
- Related plugin: `flutter-localization` - localization setup and translation workflow.
- Related plugin: `flutter-navigation` - route-level screen and navigation work.

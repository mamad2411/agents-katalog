---
name: mobile-architecture
description: Design mobile app architecture. Use when structuring mobile
  codebases and features.
metadata:
  tags: mobile, architecture
---

# Mobile Architecture

## Use this skill when
- Structuring a mobile app: layers, features, dependencies
- Choosing state, navigation, and data patterns
- Designing for offline and background constraints

## Do not use this skill when
- Platform-specific UI (use its framework skill)
- Web-only architecture

## Instructions
1. Organize by feature with shared core (di, networking, theme).
2. Choose a state management approach and apply it consistently.
3. Separate UI from business logic for testability.
4. Model navigation as a declared graph, not scattered pushes.
5. Plan offline: cache, sync, conflict resolution.
6. Size for memory constraints of mobile platforms.
7. Keep the app layer thin and edge logic centered.

## Checklist
- UI/business separation clear
- Navigation declared
- Offline story defined

## Output Format
- Layers | feature map | state pattern | offline plan

## Common Mistakes
- Business logic inside widgets/screens
- Navigation state tangled with business state
- No offline handling

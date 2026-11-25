---
name: interaction-language
description: Interaction language rules, hover behavior, custom cursor feedback, button feel, scroll gestures, micro-interactions, magnetic pull effects, and input feedback.
---

# 👆 05 - Interaction Language Engine

## Purpose & Responsibility
Craft tactile micro-interactions, magnetic cursor tracking, active button feedback, and responsive gesture dynamics operating under 50ms latency.

## Core Rules
1. **Sub-50ms Reaction Loop**: Every interactive trigger must give immediate visual feedback upon hover/focus/press.
2. **Magnetic Pull**: Primary CTA buttons pull towards cursor position within a `30px` radius using spring interpolation.
3. **Cursor Dynamics**: Custom cursor smoothly scales, morphs, or reveals context text (`"View"`, `"Explore"`, `"Drag"`) when hovering over interactive cards or WebGL canvases.
4. **Button Tactility**: Active button press scales down (`scale: 0.97`) with subtle inner shadow inset.

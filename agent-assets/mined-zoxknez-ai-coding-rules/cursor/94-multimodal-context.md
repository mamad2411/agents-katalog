---
description: MULTIMODAL: Trigger visual feedback loop for UI/UX changes
globs: **/components/**/*.tsx, **/components/**/*.jsx, **/pages/**/*.tsx, **/pages/**/*.jsx, **/app/**/*.tsx, **/app/**/*.jsx, **/*.css, **/*.scss, **/*.less
---

# Multimodal Visual Feedback Rule

When working on UI-related files (Components, Pages, App Router, Styles):

1. **Verify Vision Capability**: Check if you have vision capabilities (e.g., using Gemini 3 or GPT-4o).
2. **Request Baseline**: Before making any styling or layout changes, request a screenshot of the current UI.
   - Example: *"I'm about to modify the login form. Please provide a screenshot of the current state for baseline comparison."*
3. **Implement Changes**: Proceed with implementation.
4. **Request Verification**: After applying changes, request a new screenshot to verify layout, alignment, and "vibes."
   - Example: *"Changes applied. Please provide a new screenshot so I can verify the visual outcome."*
5. **Self-Correct**: If discrepancies are found between the mockup/intent and the actual screenshot, perform a self-correction pass.

*Note: Visual context is 10x more effective than code analysis for detecting CSS 'jank' or alignment issues.*

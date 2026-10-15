---
name: enterprise-visual-design
description: Expert visual design for professional, enterprise-grade applications. Use when designing complex dashboards, financial interfaces, or any project requiring high-density, professional aesthetics over "vibe coding".
---
# Enterprise Visual Design Skill

This skill enforces professional design standards to ensure applications look and feel enterprise-grade. It prioritizes clarity, density, and semantic consistency over trend-driven "vibe coding".

## Design Principles

### 1. Typography First
*   **Scale:** Use a rigid typographic scale (e.g., 12, 14, 16, 18, 24, 32, 48px).
*   **Fonts:** Prefer highly legible sans-serifs (Inter, Roboto, SF Pro, Segoe UI).
*   **Contrast:** Ensure all text meets WCAG AA (4.5:1) for normal text and AAA (7:1) for critical data.

### 2. High-Density Layouts
*   **Data Grids:** Use 32px or 40px row heights for maximum density without sacrificing legibility.
*   **Scanning:** Use subtle zebra-striping and 1px borders to separate rows and columns.
*   **Whitespace:** Use an 8px base unit for all margins and padding.

### 3. Semantic Color & Feedback
*   **Neutral Palette:** Use a deep range of grays (Slate/Zinc) for layout components to let content pop.
*   **Contextual Colors:**
    *   *Success:* Emerald/Green for positive outcomes.
    *   *Warning:* Amber/Orange for non-blocking issues.
    *   *Error:* Rose/Red for critical failures.
    *   *Info:* Indigo/Blue for system messages.

### 4. Motion & Interactivity
*   **Micro-interactions:** Keep transitions under 200ms. Use "Ease-out" for entrance and "Ease-in" for exit.
*   **Feedback:** Every button must have distinct `hover`, `active`, `focus-visible`, and `disabled` states.
*   **Skeletons:** Use subtle pulse animations for loading states instead of generic spinners for better perceived performance.

## Data Visualization Rules
*   **Clutter:** Remove all non-essential grid lines and decorations.
*   **Meaning:** Use colors sparingly to highlight specific data points, not as decoration.
*   **Accessibility:** Use patterns or distinct shapes in addition to color to represent data series.

## Interaction Protocol
*   **Input:** Wireframes, UX requirements, or existing messy UI code.
*   **Output:** Refined CSS/TSX components with a focus on professional aesthetics.

**Tag**: Start your response with `[ENTERPRISE-DESIGN]`.

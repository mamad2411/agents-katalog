---
name: unity-ui-toolkit
description: Master guide for high-performance interface development using UI Toolkit. Based on Unity 6+ standards and hardware optimization.
---

# Skill: Unity UI Toolkit - Best Practices & Performance (Unity 6+)

The master guide for high-performance interface development using UI Toolkit. Based on Unity 6+ standards and hardware-accelerated optimization.

---

## 🏗️ Architecture and Standards

### 1. Flexbox-First (Yoga Engine)
*   **Default Behavior:** Orientation is `flex-direction: column`.
*   **No Inline Styles:** All styles must reside in `.uss` files. Use variables in `:root` for design tokens (colors, spacing).
*   **Custom Components (Unity 6):** Use `[UxmlElement]` and `[UxmlAttribute]` attributes on `partial` classes. Avoid the legacy `UxmlFactory` boilerplate.

### 2. UI Toolkit vs. uGUI (When to use what?)
*   **UI Toolkit (Retained Mode):** Ideal for static HUDs, Menus, Inventories, and Editor tools.
*   **uGUI (Immediate/GameObject Mode):** **Mandatory** for World Space UI with high density or complex billboard transformations (e.g., health bars over 100 enemies), unless using the specific Unity 6 World Space integration with extreme caution.

---

## ⚡ Performance Optimization (Critical)

### 1. GPU-Based Animations and Transforms
*   **Golden Rule:** NEVER animate layout properties (`width`, `height`, `margin`, `padding`, `top`, `left`). This forces a CPU-intensive "Layout Recalculation" of the entire visual tree.
*   **Solution:** Use GPU-accelerated transforms: `translate`, `rotate`, `scale`.
*   **Usage Hints:** Enable `UsageHints.DynamicTransform` on elements that move or animate frequently to ensure efficient GPU handling.

### 2. Panel Management and Draw Calls
*   **UIDocument:** Avoid having multiple `UIDocument` components for small elements. Group as many elements as possible under a single `UIDocument` to maximize batching.
*   **Vertex Budget:** If your UI is complex and you see flickering or disappearing elements, increase the **Vertex Budget** in the `Panel Settings` asset.
*   **Texturing and Atlasing:** Use the **Sprite Packer** to ensure all UI icons reside in the same atlas, preventing batching breaks.

### 3. "Smart Hiding"
*   **display: none** vs. **visibility: hidden**:
    *   `display: none`: Removes the element from layout calculations (most efficient for long-term hiding).
    *   `visibility: hidden`: The element still occupies layout space but is not rendered.
*   **Do NOT use opacity: 0** to hide elements: They still process events and consume rendering resources.

---

## 🛠️ Diagnostic Tools
1.  **UI Toolkit Debugger:** Essential for inspecting the visual tree and layout timings.
2.  **Panel Settings -> Live Reload:** Keep enabled during development to see USS/UXML changes instantly.
3.  **Frame Debugger:** Crucial for identifying why batching breaks between UI elements.

---

## 🚫 Common Pitfalls (Anti-Patterns)
*   **Deep Nesting:** Avoid excessively deep hierarchies of `VisualElements`. Every level adds cost to Flexbox calculations.
*   **Manual UxmlFactory:** Do not write `UxmlFactory` manually in Unity 6; leverage the code generator.
*   **Complex World Space Anchors:** Avoid dynamic layouts (Flex) on objects moving rapidly in 3D space.

---
name: wireframing
description: Low-to-mid fidelity wireframing, responsive 12-column grid scaffolding, semantic HTML5 landmark architecture, content hierarchy, and graybox prototyping.
---

# Wireframing & Structural Layout Prototyping Contract

## 1. Purpose
Design, scaffold, and document low-to-mid fidelity wireframes, schematic UI blueprints, and structural responsive layout prototypes. Prioritize information hierarchy, content chunking, and accessibility landmarks before visual styling, establishing unambiguous architectural handoffs for engineering implementation.

---

## 2. Use When
- Conceiving initial interface layouts and content hierarchies for new screens or features.
- Scaffolding responsive layout behaviors across mobile, tablet, and desktop viewports.
- Defining semantic HTML5 landmark structures (`<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>`) early in the design cycle.
- Communicating spatial layouts and component placement to stakeholders without visual color bias.

---

## 3. Do Not Use When
- Designing pixel-perfect high-fidelity visual mockups or final brand color tokens (use `design-tokens` or `design-system`).
- Creating detailed step-by-step transaction flowcharts without screen layouts (use `user-flows`).
- Implementing production-ready React/Vue component code (use `ui-implementation`).

---

## 4. Required Context
Before generating or modifying wireframes, obtain:
1. **User Goal & Primary Action**: The single most critical outcome the user must achieve on this screen.
2. **Content Inventory**: All required data fields, controls, tables, badges, and navigation links.
3. **Responsive Breakpoint Matrix**: Mobile (320px - 480px), Tablet (768px - 1024px), Desktop (1200px+).
4. **Fidelity Requirement**: Lo-Fi (conceptual boxes and labels) vs Mid-Fi (precise 8pt spacing and grayscale components).

---

## 5. Procedure

### Step 1: Content Hierarchy & Eye-Tracking Layout
1. Analyze content priority: classify elements into Primary (Hero/Key CTA), Secondary (Supporting details/filters), and Tertiary (Metadata/disclaimers).
2. Position elements along natural eye-tracking paths:
   - **F-Pattern** for text-heavy feeds, dashboards, and search results.
   - **Z-Pattern** for landing pages, promotional headers, and sign-up flows.
3. Place the primary CTA in the prominent visual anchor position (top right or centered above the fold).

### Step 2: Responsive Grid Scaffolding
1. Establish a standard responsive column grid:
   - **Mobile**: 4 columns, 16px margins, 12px gutters.
   - **Tablet**: 8 columns, 24px margins, 16px gutters.
   - **Desktop**: 12 columns, 32px margins, 24px gutters, max-width container (e.g. 1200px - 1440px).
2. Define column spans for major modules (e.g., Sidebar = 3 columns, Main Feed = 9 columns).

### Step 3: Semantic Landmark Architecture
1. Explicitly designate HTML5 landmark regions:
   - `<header role="banner">`: Global title, search bar, profile menu.
   - `<nav role="navigation">`: Global and local navigation links.
   - `<main role="main">`: Primary unique page content.
   - `<aside role="complementary">`: Contextual filters, related widgets, help sidebar.
   - `<footer role="contentinfo">`: Copyright, auxiliary links, status indicators.
2. Guarantee that every wireframe layout places 100% of visible content within an appropriate semantic landmark.

### Step 4: Component States Wireframing
For every core view, wireframe the four canonical UI states:
1. **Default State**: Standard populated layout with realistic data lengths.
2. **Loading State**: Skeleton placeholders matching component geometries.
3. **Empty State**: Reassuring visual cue explaining the absence of data with a prominent action to create/import.
4. **Error Boundary State**: Inline error alert with clear remediation next steps.

### Step 5: Technical Annotations & Handoff
1. Annotate flexbox/grid alignments (`flex-wrap: wrap`, `justify-content: space-between`).
2. Specify responsive column collapse rules (e.g., "At $\le 768\text{px}$, sidebar collapses into bottom tab bar").
3. Document text truncation policies (`text-overflow: ellipsis` on single line vs `clamp-2`).

---

## 6. Decision Rules
1. **Grayscale-First Rule**: Wireframes must use grayscale palettes (`#ffffff`, `#f8fafc`, `#e2e8f0`, `#0f172a`) with at most a single neutral accent color to keep focus on layout and structure rather than aesthetics.
2. **Realistic Content Lengths**: Never use single-word placeholders for dynamic fields; test layouts against long internationalized names, multi-line titles, and zero-item lists.
3. **Mandatory Landmark Coverage**: All content must reside within a valid landmark container; floating uncontained elements are prohibited.
4. **Explicit Tab Order**: Form wireframes must specify logical top-to-bottom, left-to-right sequential tab order.

---

## 7. Evidence Required
- **Wireframe Specification**: Comprehensive layout blueprint (`templates/wireframe-spec.md`).
- **HTML/CSS Scaffold or Mockup**: Renderable structural prototype verifying responsive behavior.
- **State Matrix Coverage**: Proof of Default, Loading, Empty, and Error state definitions.

---

## 8. Output Contract
A production wireframing deliverable must provide:
1. Structured Wireframe Specification (`templates/wireframe-spec.md`).
2. HTML5 schematic wireframe prototype (`*.html`).
3. Responsive column grid mapping across Mobile, Tablet, and Desktop.
4. Accessibility landmark annotations.

---

## 9. Stop Conditions
- Layout defined across all 3 standard responsive breakpoints.
- All four component states (Default, Loading, Empty, Error) wireframed.
- Semantic landmarks validated.

---

## 10. Escalation Rules
- Escalate to Product Management if content volume demands more space than a single viewport can accommodate without severe truncation.
- Escalate to Technical Architecture if proposed layout structures require non-standard DOM nesting that impedes accessibility.

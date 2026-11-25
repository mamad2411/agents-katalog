---
name: ux-architecture
description: Information architecture (IA), structural taxonomy, navigation systems, sitemap hierarchy, mental model mapping, and faceted search topologies.
---

# UX Information Architecture & Navigation Strategy Contract

## 1. Purpose
Define, architect, and govern product Information Architecture (IA), ensuring intuitive navigation hierarchies, mental model alignment, consistent labeling systems, shallow task discovery depths, and scalable content taxonomies across multi-platform experiences.

---

## 2. Use When
- Structuring large-scale digital products, complex web portals, documentation sites, or enterprise SaaS suites.
- Designing global, local, contextual, and faceted navigation systems.
- Establishing content taxonomies, metadata schemas, and search indexing structures.
- Re-architecting legacy product navigation suffering from feature bloat or deep nesting.

---

## 3. Do Not Use When
- Designing low-level task flow diagrams or step-by-step transaction branches (use `user-flows`).
- Coding concrete CSS layouts or component rendering (use `ui-implementation` or `design-system`).
- Simple single-page utility apps with zero hierarchical navigation.

---

## 4. Required Context
Before architecting UX information structures, verify:
1. **Target User Mental Models**: How users naturally conceptualize domain entities and categories (informed by card sorting or user interviews).
2. **Product Content Inventory**: Complete catalog of screens, features, data objects, and document types.
3. **Primary Use Cases & Access Frequencies**: Core high-frequency tasks vs. administrative secondary functions.
4. **Platform Form Factors**: Mobile drawer/tab bar constraints vs. desktop persistent sidebar/mega-menu capabilities.

---

## 5. Procedure

### Step 1: Content Inventory & Entity Taxonomy
1. Perform a comprehensive content audit of all existing or planned product views and resources.
2. Categorize items into mutually exclusive domain entities and functional clusters.
3. Establish clear, unambiguous labeling conventions reflecting user vocabulary (avoid internal engineering jargon or organizational silos).

### Step 2: Structural Organization & Hierarchy (Sitemap)
1. Design the structural hierarchy balancing breadth and depth:
   - Target maximum tree depth of 3 levels (Top-Level $\to$ Category $\to$ Detail) for 90%+ of user tasks.
   - Limit top-level navigation items to $5 \pm 2$ primary buckets (Miller's Law) to prevent decision paralysis.
2. Ensure no orphaned nodes exist; every page must possess a well-defined ancestor path and parent link.

### Step 3: Multi-Tier Navigation Systems
1. **Global Navigation**: Persistent anchors providing orientation and high-level routing across all views.
2. **Local / Sub-Navigation**: Contextual menus displaying siblings and children within the active category.
3. **Contextual Navigation**: Inline links, related content widgets, and cross-references between related entities.
4. **Wayfinding & Orientation**: Implement breadcrumbs (`Home / Category / Subcategory / Current Page`) conforming to ARIA APG breadcrumb patterns.

### Step 4: Faceted Search & Filtering Architecture
1. For large homogeneous collections (catalogs, logs, repositories), define structured facet dimensions (status, date, type, author, tags).
2. Design zero-state search recovery: suggest spelling corrections, related categories, or relaxed filter bounds.

### Step 5: Verification & Tree Testing
1. Conduct simulated or live Tree Testing (reverse card sorting) assessing findability rates and directness scores.
2. Target $\ge 80\%$ task findability without backtracking.

---

## 6. Decision Rules
1. **Hierarchy Depth Ceiling**: Core user goals must be discoverable within 3 clicks/taps from the home dashboard. Nesting deeper than 4 levels requires explicit architectural approval.
2. **User-Centric Taxonomy**: Organize categories by user task intent or domain mental models, never by company internal department structures (Conway's Law anti-pattern).
3. **Clear Current Location Indicator**: The user must always be able to answer three wayfinding questions instantly: *Where am I? Where can I go? How do I get back?*
4. **Consistent Terminology**: A concept must have exactly one canonical label across navigation, headers, button labels, and search filters.

---

## 7. Evidence Required
- **Sitemap Diagram**: Hierarchical structural map detailing all primary, secondary, and tertiary routes.
- **Navigation Specification**: Definition of global, local, breadcrumb, and faceted filter structures.
- **Tree Test / Findability Scorecard**: Validation metrics verifying navigation directness and task success.

---

## 8. Output Contract
A production UX architecture deliverable must contain:
1. Information Architecture Specification (`templates/ia-architecture-spec.md`).
2. Hierarchical sitemap definition (in Markdown / Mermaid).
3. Taxonomy and labeling dictionary.
4. Navigation behavior rules across breakpoints.

---

## 9. Stop Conditions
- All inventory content mapped into the sitemap with zero orphaned screens.
- Tree depth $\le 3$ for all primary user tasks.
- Navigation breadcrumb and wayfinding semantics validated.

---

## 10. Escalation Rules
- Escalate to Product Strategy if business stakeholder demands for top-level navigation placement exceed 7 items.
- Escalate to Technical Architecture if database querying or indexing limits prevent real-time faceted search filtering.

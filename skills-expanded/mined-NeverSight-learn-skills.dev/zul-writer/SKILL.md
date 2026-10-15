---
name: zul-writer
description: >
  Generates ZK Framework ZUL pages (.zul) through a structured 4-step workflow: requirements clarification, ZUL generation, validation, and controller generation.
  Supports both MVC (Composer-based) and MVVM (ViewModel-based) patterns, ZK 9/10, and visual analysis for screenshot-to-ZUL conversion.
  Use when the user asks to create a ZUL page, build ZK UI components (forms, grids, dashboards, borderlayouts), or convert an image/mockup to ZUL code.
license: MIT
compatibility: >
  Designed for Claude Code, Gemini CLI, and GitHub Copilot/Cursor.
  Requires access to local skills/zul-writer/assets/ and skills/zul-writer/references/ directories.
metadata:
  author: hawk
  version: "1.0.0"
---
# ZUL Writer

## Workflow Overview

This skill creates well-structured zul pages through a 4-step process:

1. **Clarify Requirements** - Gather page purpose, pattern, and layout needs
2. **Generate ZUL** - Create the ZUL file based on requirements
3. **Validate ZUL** - Verify correctness of the generated ZUL
4. **Generate Controller Class** - Create the corresponding Java class (ViewModel or Composer)

**Alternative entry**: When user provides a UI image (screenshot/mockup), perform the **Visual Analysis** below first, then proceed to the 4-step process.

---

## Visual Analysis (for Images/Mockups)

When a UI screenshot or mockup image is provided, perform this analysis **before** starting the 4-step workflow:

1. **Visual Breakdown**: Identify all UI elements (layout, inputs, buttons, tables, navigation).
2. **Component & Layout Strategy**: Plan the ZK component mapping (refer to [references/ui-to-component-mapping.md](references/ui-to-component-mapping.md)) and determine the overall layout (e.g., `<borderlayout>`, nested `<vlayout>`).
3. **Tab Content Scope**: If tabs are present, determine content boundaries. Items switching with tabs must go INSIDE `<tabpanel>`. See [assets/content-tabbox.zul](assets/content-tabbox.zul).
4. **Identify Custom Styling**: Mark areas that require fallback HTML elements or custom CSS.

**Transition**: Use these findings to inform **Step 1: Clarify User Requirements** and eventually **Step 2: Generate ZUL File**.


---

## Step 1: Clarify User Requirements

Ask targeted questions to understand needs. If starting from an image, use the results of the **Visual Analysis** to inform these questions.

### Questions to Ask

#### 1. ZK Version
Detect from user's project (check `pom.xml`, `ivy.xml`, or `build.gradle` for ZK dependency version). If not found, ask:
- 9 or before
- 10.x

#### 2. Page Purpose
- Data entry form
- Data list/grid display
- Dashboard with multiple sections
- Dialog/popup window
- Master-detail view
- Search and results page
- Other: [specify]

#### 3. MVC or MVVM Pattern
Present both options with equal weight — do NOT mark either as "(Recommended)":
- **MVVM**: ViewModel-based with `@bind`/`@command` data binding — testable, requires more ZK familiarity
- **MVC**: Composer-based with `apply` and wired components — straightforward, beginner-friendly

#### 4. Layout Requirements
- Borderlayout (north/south/east/west/center)
- Vertical layout (vlayout)
- Horizontal layout (hlayout)
- Grid-based layout
- Tabbed layout (tabbox)
- Combined layouts

#### 5. ZK Charts (only when charts are needed)

If the ZUL page requires a `<charts>` component, follow [references/charts-guidelines.md](references/charts-guidelines.md) before generating any chart code.

---

## Step 2: Generate a ZUL File

### Generation Guidelines

When generating the ZUL file, follow these technical guidelines:

1. **Map UI Elements**: Consult [references/ui-to-component-mapping.md](references/ui-to-component-mapping.md) to choose the correct ZK components. 
   - Prioritize ZK components over native HTML.
   - Use layout components like `<borderlayout>`, `<vlayout>`, and `<hlayout>` effectively.
2. **Handle CSS Inclusion**: 
   - If fallback native HTML elements (e.g. `<n:div>`) are used, identify and include the necessary CSS.
   - Use the `<style>` element for inline CSS; **do not** use the `<?style ?>` processing instruction.
3. **ZK Documentation**:
   - Query `zk-doc-mcp-server` for detailed component info if available.
   - Use [ZK Javadoc](https://www.zkoss.org/javadoc/latest/zk/) for properties and event details.
4. **Best Practices**:
   - Don't specify `hflex="min"` on `<button>` (it's `display: inline-block` by default).
   - Use meaningful IDs and follow the [assets/template.zul](assets/template.zul) structure.


### Layout & Component Patterns

#### XML & Pattern Structures
- **Base Template**: [assets/template.zul](assets/template.zul)
- **MVC Structure**: [assets/mvc-sample.zul](assets/mvc-sample.zul)
- **MVVM Structure**: [assets/mvvm-pattern-structure.zul](assets/mvvm-pattern-structure.zul)

#### Sizing & Layouts
- **Flexible Sizing (hflex/vflex)**: [assets/flexible-sizing.zul](assets/flexible-sizing.zul)
- **Borderlayout Example**: [assets/borderlayout-example.zul](assets/borderlayout-example.zul)

#### Common MVVM Patterns
- [Form with Validation](assets/form-validation-mvvm.zul)
- [Data Grid with Selection](assets/data-grid-selection-mvvm.zul)
- [Master-Detail Pattern](assets/master-detail-mvvm.zul)
- [Dialog/Popup](assets/dialog-popup-mvvm.zul)

---

## Step 3: Validate Generated ZUL

Run validation: `scripts/validate-zul.py`
- Layer 1: XML well-formedness (no dependencies)
- Layer 2: XSD schema validation (requires `lxml`)
- Layer 3: Attribute placement check (requires `lxml`) - catches misplaced attributes (e.g. `iconSclass` on `textbox`)
- Layer 4: ZK 10 compatibility checks (only if target ZK version is 10)

### Prerequisites
Layer 2 and 3 require `lxml`. If missing:

1. Check for `uv`: `which uv`
2. If `uv` available: `uv pip install lxml`, run script via `uv run`
3. If `uv` not available: ask user to install `uv` (https://docs.astral.sh/uv/getting-started/installation/)
4. If user declines `uv`: fall back to `pip install lxml`

Do NOT skip Layer 2 silently. Always inform the user and guide through installation.

### Post-Validation Checklist

#### Pattern Consistency
- **MVC**: Uses `apply` attribute, no MVVM binding expressions
- **MVVM**: Uses `viewModel` attribute, proper binding syntax
- No mixing of patterns on same component

#### Best Practices
- IDs are unique within each ID space owner (`<window>`, `<idspace>`)
- Prefer `sclass` over inline styles
- Prefer `hflex`/`vflex` over fixed dimensions
- Include meaningful labels and tooltips for accessibility


## Step 4: Generate Controller Class

Generate the corresponding Java controller class (ViewModel or Composer) for the ZUL page. 

### Controller Generation Guidelines

1. **Pattern Consistency**: 
   - Use **ViewModel** for MVVM patterns.
   - Use **Composer** for MVC patterns.
2. **Implementation Details**: Follow the technical requirements in [references/controller-guidelines.md](references/controller-guidelines.md).

#### MVC Pattern - Composer Class
[assets/MyComposer.java](assets/MyComposer.java)

#### MVVM Pattern - ViewModel Class
[assets/MyViewModel.java](assets/MyViewModel.java)

### Complete Examples & Patterns

For complex UI patterns like Kanban Boards or Dashboards, and for complete template examples, refer to [references/use-case-guidelines.md](references/use-case-guidelines.md).
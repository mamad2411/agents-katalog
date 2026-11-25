---
name: product-designer
description: >
  A skill for generating design spec documents and Figma designs based on user stories, wireframes, and tech specs.
  design-spec.md is always generated, and Figma designs via cursor-talk-to-figma-mcp must be generated when MCP connection is available.
  Use this skill for UI design generation or Figma integration work requests.
---

## 🌐 Language

> All output documents and user-facing messages must be written in the language specified
> by `crew-config.json → preferences.language`. If not set, default to English.

## ⛔⛔⛔ Top Priority Principle: Figma Design Generation Required ⛔⛔⛔

> **⚠️ Warning**: Skipping this skill or generating only design-spec.md and stopping is **prohibited**.

### Required Execution Order (Never Skip)

```
0. Check figma-guidelines.md ──────────────────────── ✅ Required (follow rules if present!)
           │
           ▼
1. Generate design-spec.md ────────────────────────── ✅ Required
           │
           ▼
2. Check MCP connection (claude mcp list) ─────────── ✅ Required
           │
           ├── TalkToFigma present ──▶ Proceed to step 3 (required!)
           │
           └── TalkToFigma absent ──▶ Provide setup instructions and finish (exception allowed)
           │
           ▼
3. Generate Figma design (follow guidelines!) ─────── ✅ Required if MCP available!
           │
           ▼
4. Add Figma links to design-spec.md ──────────────── ✅ Required
```

> **Step 0 Detail**: If a `figma-guidelines.md` file exists in the project, you must read it and follow those rules throughout Steps 1-4.

### ⛔ Strictly Prohibited

1. **Not generating a Figma design when MCP is connected**
2. **Generating only design-spec.md and reporting "complete"**
3. **Skipping the MCP connection check**
4. **Skipping Figma generation for reasons like "it takes too long" or "it's complex"**

### Workflow Decision Criteria

| Situation | design-spec.md | Figma Design |
|-----------|----------------|--------------|
| MCP connection available | ✅ Required | ⛔ **Required** (no skipping!) |
| MCP connection unavailable | ✅ Required | ❌ Skipped (exception) |
| User explicitly requests "spec only" | ✅ Required | ❌ Skipped (exception) |

> **Important**: Unless the user explicitly requests "spec only", if MCP is available you **must** complete the Figma design.

## ⚠️ Check Repository-Specific Figma Guidelines (Required)

> **Must check before starting**: Verify whether a `figma-guidelines.md` file exists at the project root, and if so, follow those rules.

### Guidelines File Check Order

```
1. Check {project-root}/figma-guidelines.md
2. Check {project-root}/docs/figma-guidelines.md
3. Check {project-root}/.claude/figma-guidelines.md
```

### When Guidelines File Exists

Read the file contents and **strictly follow** these items:

| Item | Description |
|------|-------------|
| **Color palette** | Use only defined colors (HEX, RGB values) |
| **Typography** | Use specified fonts, sizes, and weights |
| **Spacing system** | Use only defined spacing values (4px, 8px, 16px, etc.) |
| **Component naming** | Follow naming conventions (e.g., `Button/Primary/Default`) |
| **Layer structure** | Follow the specified frame/page structure |
| **Icon style** | Follow icon size and stroke width rules |
| **Border radius** | Follow border-radius value rules |
| **Shadows/effects** | Use only defined shadow and blur values |

### Guidelines File Example

```markdown
# Figma Design Guidelines

## 1. Color Palette
| Name | HEX | RGB | Usage |
|------|-----|-----|-------|
| Primary | #3B82F6 | 59, 130, 246 | Primary actions, CTA buttons |
| Primary-Hover | #2563EB | 37, 99, 235 | Primary hover state |
| Gray-900 | #111827 | 17, 24, 39 | Body text |
| Gray-500 | #6B7280 | 107, 114, 128 | Secondary text |
| Error | #EF4444 | 239, 68, 68 | Error states |
| Success | #10B981 | 16, 185, 129 | Success states |

## 2. Typography
| Style | Font | Size | Weight | Line Height |
|-------|------|------|--------|-------------|
| H1 | Inter | 32px | Bold (700) | 40px |
| H2 | Inter | 24px | Semibold (600) | 32px |
| Body | Inter | 16px | Regular (400) | 24px |
| Small | Inter | 14px | Regular (400) | 20px |
| Caption | Inter | 12px | Medium (500) | 16px |

## 3. Spacing System
- 4px (xs), 8px (sm), 12px (md), 16px (lg), 24px (xl), 32px (2xl), 48px (3xl)

## 4. Component Naming Rules
- Format: `{Category}/{Component}/{Variant}/{State}`
- Example: `Button/Primary/Large/Default`, `Input/Text/Default/Focus`

## 5. Border Radius
- none: 0px, sm: 4px, md: 8px, lg: 12px, xl: 16px, full: 9999px

## 6. Shadows
- sm: 0 1px 2px rgba(0,0,0,0.05)
- md: 0 4px 6px rgba(0,0,0,0.1)
- lg: 0 10px 15px rgba(0,0,0,0.1)
```

### When Guidelines File Does Not Exist

Use the default design system, but clearly document the values used in design-spec.md.

# Product Designer (cursor-talk-to-figma-mcp)

Analyzes user stories, wireframes, and tech specs to generate designs directly in Figma.

## ⚠️ Auto-Layout Required Principle (Figma-Specific)

> This principle applies specifically to Figma design generation using the cursor-talk-to-figma-mcp tool. It is not a universal design principle.

**Auto-Layout must be applied to every Figma frame created.** Positioning elements with absolute coordinates (x, y) is prohibited.

### Required Auto-Layout Settings

1. **layoutMode must be specified when creating frames**:
   - `layoutMode: "VERTICAL"` or `layoutMode: "HORIZONTAL"`
   - `layoutMode: "NONE"` is prohibited

2. **Sizing mode (HUG/FILL)**:
   - Container frame: `layoutSizingHorizontal: "FIXED"`, `layoutSizingVertical: "HUG"`
   - Child elements: `layoutSizingHorizontal: "FILL"` (fill full width)
   - Fit to content: `"HUG"`

3. **Alignment settings**:
   - `primaryAxisAlignItems`: Main axis alignment (MIN, CENTER, MAX, SPACE_BETWEEN)
   - `counterAxisAlignItems`: Cross axis alignment (MIN, CENTER, MAX)

4. **Padding and spacing**:
   - Must set `paddingTop/Right/Bottom/Left`
   - Use `itemSpacing` for spacing between child elements

### Correct Example

```javascript
// ✅ Correct approach: Using Auto-Layout
mcp__TalkToFigma__create_frame({
  "name": "Card",
  "x": 0, "y": 0,
  "width": 360, "height": 200,
  "fillColor": { "r": 1, "g": 1, "b": 1 },
  "layoutMode": "VERTICAL",
  "layoutSizingHorizontal": "FIXED",
  "layoutSizingVertical": "HUG",
  "primaryAxisAlignItems": "MIN",
  "counterAxisAlignItems": "MIN",
  "paddingTop": 24,
  "paddingRight": 24,
  "paddingBottom": 24,
  "paddingLeft": 24,
  "itemSpacing": 16
})

// Child elements are auto-positioned when added via parentId
mcp__TalkToFigma__create_text({
  "parentId": "{cardFrameID}",
  "name": "Title",
  "text": "Card Title",
  "fontSize": 18,
  "fontWeight": 600
})
```

### Incorrect Example

```javascript
// ❌ Prohibited: Positioning with absolute coordinates
mcp__TalkToFigma__create_frame({
  "name": "Card",
  "x": 0, "y": 0,
  "width": 360, "height": 200
  // No layoutMode = absolute coordinate mode
})

// ❌ Prohibited: Adjusting position with move_node
mcp__TalkToFigma__move_node({
  "nodeId": "{nodeID}",
  "x": 24, "y": 24  // Unnecessary with Auto-Layout
})
```

### Setting Layout on Existing Frames

```javascript
// Set Auto-Layout mode
mcp__TalkToFigma__set_layout_mode({
  "nodeId": "{frameID}",
  "layoutMode": "VERTICAL"
})

// Set sizing mode
mcp__TalkToFigma__set_layout_sizing({
  "nodeId": "{frameID}",
  "layoutSizingHorizontal": "FIXED",
  "layoutSizingVertical": "HUG"
})

// Set padding
mcp__TalkToFigma__set_padding({
  "nodeId": "{frameID}",
  "paddingTop": 24,
  "paddingRight": 24,
  "paddingBottom": 24,
  "paddingLeft": 24
})

// Set item spacing
mcp__TalkToFigma__set_item_spacing({
  "nodeId": "{frameID}",
  "itemSpacing": 16
})

// Set alignment
mcp__TalkToFigma__set_axis_align({
  "nodeId": "{frameID}",
  "primaryAxisAlignItems": "MIN",
  "counterAxisAlignItems": "CENTER"
})
```

## Prerequisites

### Installing cursor-talk-to-figma-mcp

1. **Install Bun** (if not installed):
```bash
curl -fsSL https://bun.sh/install | bash
```

2. **Register MCP server** (Claude Code):
```bash
claude mcp add "TalkToFigma" -s local -- ~/.bun/bin/bunx cursor-talk-to-figma-mcp@latest
```

3. **Install Figma plugin**:
   - Install the "Cursor Talk to Figma MCP" plugin from Figma Community
   - https://www.figma.com/community/plugin/1485687494525374295/cursor-talk-to-figma-mcp-plugin
   - Or local development: Plugins > Development > Import plugin from manifest

> **WebSocket server starts automatically**: When this skill runs, the WebSocket server (port 3055) starts automatically in the background. No need to run it separately in a terminal.

### Features (vs legacy figma-mcp-server)

- **No token required**: Communicates via WebSocket without API tokens
- **Real-time integration**: Communicates directly with the Figma plugin
- **Bidirectional communication**: Can query selected node information in real time

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  Step 1: Analyze Input Documents                                │
│  - Analyze user stories, wireframes, tech specs                 │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 2: Generate design-spec.md (Required)                     │
│  - Document design system, components, screen layouts           │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 3: Check Figma MCP Connection                             │
│  - MCP available? → Proceed to Step 4                           │
│  - MCP unavailable? → Complete (design-spec.md only)            │
│  - User requests "spec only"? → Complete                        │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 4: Generate Figma Design (Optional)                       │
│  - Create design system                                         │
│  - Create components                                            │
│  - Create screen layouts                                        │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 5: Add Figma Links to design-spec.md                      │
│  - Add Figma file link, component keys, etc.                    │
└─────────────────────────────────────────────────────────────────┘
```

## Workflow

### 1. Analyze Input Documents (Required)

Read user stories, wireframes, and tech specs to identify:
- List of required screens
- Component composition for each screen
- State-specific UI variations (error, loading, empty state)
- Color and typography requirements

#### Query Current Document Information

```javascript
// Query current Figma document info
mcp__TalkToFigma__get_document_info({})

// Query currently selected element info
mcp__TalkToFigma__get_selection({})
```

### 2. Analyze Existing Design System

#### 2.1 Query Styles and Components

```javascript
// Query all document styles
mcp__TalkToFigma__get_styles({})

// Query local component list
mcp__TalkToFigma__get_local_components({})
```

### 3. Create Design System

#### 3.1 Create Color Styles

Create the color palette defined in the wireframe/tech spec in Figma:

```javascript
// Create primary color frame
mcp__TalkToFigma__create_frame({
  "name": "Colors/Primary",
  "x": 0, "y": 0,
  "width": 200, "height": 50,
  "fillColor": { "r": 0.95, "g": 0.95, "b": 0.95 }
})

// Create color rectangle
mcp__TalkToFigma__create_rectangle({
  "parentId": "{frameID}",
  "name": "Primary/500",
  "x": 0, "y": 0,
  "width": 50, "height": 50
})

// Set fill color
mcp__TalkToFigma__set_fill_color({
  "nodeId": "{rectangleID}",
  "r": 0.231, "g": 0.510, "b": 0.965, "a": 1
})
```

#### 3.2 Create Text Styles

```javascript
// H1 text style
mcp__TalkToFigma__create_text({
  "name": "Typography/H1",
  "x": 0, "y": 0,
  "text": "Heading 1",
  "fontSize": 32,
  "fontWeight": 700,
  "fontColor": { "r": 0.067, "g": 0.094, "b": 0.153 }
})
```

### 4. Create Components

#### 4.1 Basic Components (Button, Input, Card, etc.)

```javascript
// Create Button frame (with Auto Layout)
mcp__TalkToFigma__create_frame({
  "name": "Button/Primary",
  "x": 0, "y": 0,
  "width": 120, "height": 40,
  "fillColor": { "r": 0.231, "g": 0.510, "b": 0.965 },
  "layoutMode": "HORIZONTAL",
  "primaryAxisAlignItems": "CENTER",
  "counterAxisAlignItems": "CENTER",
  "paddingLeft": 16,
  "paddingRight": 16,
  "paddingTop": 8,
  "paddingBottom": 8
})

// Round button corners
mcp__TalkToFigma__set_corner_radius({
  "nodeId": "{buttonFrameID}",
  "radius": 8
})

// Add button text
mcp__TalkToFigma__create_text({
  "parentId": "{buttonFrameID}",
  "text": "Button",
  "fontSize": 14,
  "fontWeight": 500,
  "fontColor": { "r": 1, "g": 1, "b": 1 }
})
```

#### 4.2 Create Component Instances

```javascript
// Create instance of an existing component
mcp__TalkToFigma__create_component_instance({
  "componentKey": "{componentKey}",
  "x": 100, "y": 200
})
```

### 5. Create Screen Layouts

#### 5.1 Create Screen Frame

```javascript
// Login screen frame
mcp__TalkToFigma__create_frame({
  "name": "Screen/Login",
  "x": 0, "y": 0,
  "width": 1440, "height": 900,
  "fillColor": { "r": 0.98, "g": 0.98, "b": 0.98 },
  "layoutMode": "VERTICAL",
  "primaryAxisAlignItems": "CENTER",
  "counterAxisAlignItems": "CENTER",
  "itemSpacing": 24
})
```

#### 5.2 Clone and Position Elements

```javascript
// Clone node
mcp__TalkToFigma__clone_node({
  "nodeId": "{sourceNodeID}",
  "x": 100, "y": 200
})

// Move node
mcp__TalkToFigma__move_node({
  "nodeId": "{nodeID}",
  "x": 300, "y": 400
})

// Resize node
mcp__TalkToFigma__resize_node({
  "nodeId": "{nodeID}",
  "width": 200,
  "height": 100
})
```

#### 5.3 Create State-Specific Screens

- Default state
- Loading state
- Error state
- Success state

### 6. Query and Modify Node Information

#### 6.1 Query Node Information

```javascript
// Query single node info
mcp__TalkToFigma__get_node_info({
  "nodeId": "{nodeID}"
})

// Query multiple nodes info
mcp__TalkToFigma__get_nodes_info({
  "nodeIds": ["{nodeID1}", "{nodeID2}"]
})

// Scan text nodes
mcp__TalkToFigma__scan_text_nodes({
  "nodeId": "{parentNodeID}"
})
```

#### 6.2 Modify Text

```javascript
// Modify single text
mcp__TalkToFigma__set_text_content({
  "nodeId": "{textNodeID}",
  "text": "New text"
})

// Modify multiple texts
mcp__TalkToFigma__set_multiple_text_contents({
  "nodeId": "{parentNodeID}",
  "text": [
    { "nodeId": "{text1ID}", "text": "Text 1" },
    { "nodeId": "{text2ID}", "text": "Text 2" }
  ]
})
```

### 7. File Output

After design completion, document:
```
{project-root}/docs/{backlog-keyword}/design-spec.md
```

> **Directory rule**: All deliverables are stored under the backlog-keyword directory.

Content to include in the document:
- Figma file link
- List of generated components and their componentKeys
- List of screens and their nodeIds
- Design tokens (CSS Variables)

## MCP Tool List (grab/cursor-talk-to-figma-mcp)

### Connection Tools
| Tool | Description |
|------|-------------|
| `join_channel` | Connect to channel (required - run before all operations) |

### Document Info Query
| Tool | Description |
|------|-------------|
| `get_document_info` | Query current Figma document info |
| `get_selection` | Query currently selected element info |
| `read_my_design` | Query detailed properties of selected element |

### Node Info Query
| Tool | Description |
|------|-------------|
| `get_node_info` | Query specific node details |
| `get_nodes_info` | Query multiple node info |
| `scan_text_nodes` | Scan text elements within a node |
| `scan_nodes_by_types` | Search child nodes by specific type |

### Creation Tools
| Tool | Description |
|------|-------------|
| `create_frame` | Create frame (with Auto Layout support) |
| `create_rectangle` | Create rectangle |
| `create_text` | Create text |
| `create_component_instance` | Create component instance |

### Modification Tools
| Tool | Description |
|------|-------------|
| `set_fill_color` | Set fill color |
| `set_stroke_color` | Set stroke color/weight |
| `move_node` | Move node position |
| `resize_node` | Resize node |
| `set_corner_radius` | Set corner radius |
| `set_text_content` | Modify text content |
| `set_multiple_text_contents` | Modify multiple texts |
| `clone_node` | Clone node |

### Layout Tools
| Tool | Description |
|------|-------------|
| `set_layout_mode` | Set Auto Layout mode |
| `set_padding` | Set padding |
| `set_axis_align` | Set alignment |
| `set_layout_sizing` | Set sizing mode |
| `set_item_spacing` | Set spacing |

### Deletion Tools
| Tool | Description |
|------|-------------|
| `delete_node` | Delete node |
| `delete_multiple_nodes` | Delete multiple nodes |

### Export and Display
| Tool | Description |
|------|-------------|
| `export_node_as_image` | Export as image (PNG/JPG/SVG/PDF) |
| `set_focus` | Select node and center on screen |
| `set_selections` | Select multiple nodes |

### Styles and Components
| Tool | Description |
|------|-------------|
| `get_styles` | Query document styles |
| `get_local_components` | Query local components |

### Override Management
| Tool | Description |
|------|-------------|
| `get_instance_overrides` | Query instance overrides |
| `set_instance_overrides` | Apply instance overrides |

### Annotations
| Tool | Description |
|------|-------------|
| `get_annotations` | Query annotations |
| `set_annotation` | Create/modify annotation |
| `set_multiple_annotations` | Set multiple annotations |

### Prototyping
| Tool | Description |
|------|-------------|
| `get_reactions` | Query prototype reactions |
| `set_default_connector` | Set default connector |
| `create_connections` | Create connector lines |

## Design Generation Order

1. **Connect to channel**: Call `join_channel` (required)
2. **Query document info**: Check existing styles with `get_document_info`, `get_styles`
3. **Create design system**: Generate color and text style frames
4. **Basic components**: Create Button, Input, Card, etc. with `create_frame`
5. **Compound components**: Create Header, Form, Modal, etc.
6. **Screen layouts**: Create screens with `create_frame` and position elements
7. **State variations**: Add error, loading, empty state screens
8. **Apply styles**: Finalize with `set_fill_color`, `set_stroke_color`, etc.

---

## 2. Generate design-spec.md (Required)

> **⚠️ Important**: design-spec.md must **always** be generated regardless of MCP connection status.

After analyzing input documents, generate a design specification document with the following structure:

```markdown
# Design Specification: {Feature Name}

## 1. Design System

### 1.1 Color Palette
| Name | HEX | Usage |
|------|-----|-------|
| Primary | #3B82F6 | Primary actions, links |
| Gray-900 | #111827 | Body text |
| Gray-500 | #6B7280 | Secondary text |
| Error | #EF4444 | Error states |
| Success | #10B981 | Success states |

### 1.2 Typography
| Style | Size | Weight | Usage |
|-------|------|--------|-------|
| H1 | 32px | Bold | Page title |
| H2 | 24px | Semibold | Section title |
| Body | 16px | Regular | Body text |
| Small | 14px | Regular | Secondary text |

### 1.3 Spacing System
- xs: 4px
- sm: 8px
- md: 16px
- lg: 24px
- xl: 32px

## 2. Component Specifications

### 2.1 Button
**Variants**: Primary, Secondary, Outline, Ghost
**Sizes**: sm (32px), md (40px), lg (48px)
**States**: Default, Hover, Active, Disabled, Loading

```css
/* Primary Button */
.btn-primary {
  background: #3B82F6;
  color: white;
  border-radius: 8px;
  padding: 8px 16px;
  font-weight: 500;
}
```

### 2.2 Input
**Types**: Text, Password, Email, Search
**States**: Default, Focus, Error, Disabled

```css
/* Input Field */
.input {
  border: 1px solid #E0E0E0;
  border-radius: 8px;
  padding: 10px 12px;
  font-size: 16px;
}
.input:focus {
  border-color: #3B82F6;
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}
```

### 2.3 Card
...

## 3. Screen Layouts

### 3.1 {Screen Name}
**URL**: /path/to/page
**Related stories**: US-001, US-002

#### Layout Structure
```
┌─────────────────────────────────────┐
│  Header                             │
├─────────────────────────────────────┤
│  ┌─────────────────────────────┐   │
│  │  Main Content               │   │
│  │                             │   │
│  │  [Component descriptions]   │   │
│  │                             │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

#### Component Placement
| Element | Component | Position | Notes |
|---------|-----------|----------|-------|
| Title | H1 | Top | "Page Title" |
| Input form | Input | Center | placeholder="Email" |
| Button | Button/Primary | Bottom | "Submit" |

#### State-Specific Screens
- **Default state**: Awaiting form input
- **Loading state**: Spinner on button
- **Error state**: Error message below input
- **Success state**: Success toast message

## 4. Responsive Breakpoints

| Breakpoint | Width | Layout Change |
|------------|-------|--------------|
| Mobile | < 640px | Single column |
| Tablet | 640-1024px | 2 columns |
| Desktop | > 1024px | Sidebar visible |

## 5. Animation Guide

| Element | Animation | Duration | Easing |
|---------|-----------|----------|--------|
| Modal | Fade + Scale | 200ms | ease-out |
| Toast | Slide + Fade | 300ms | ease-out |
| Button Hover | Background | 150ms | ease |

## 6. Accessibility Checklist

- [ ] Focus styles applied to all interactive elements
- [ ] Color contrast maintained at 4.5:1 or above
- [ ] Labels connected to form fields
- [ ] Error messages announced via aria-live
- [ ] Keyboard navigation supported
```

### 2.1 File Output

```
{project-root}/docs/{backlog-keyword}/design-spec.md
```

> **Directory rule**: All deliverables are stored under the backlog-keyword directory.

---

## 3. Check Figma MCP Connection (Optional)

After generating design-spec.md, determine whether to generate Figma designs.

### 3.1 Check Skip Conditions

Skip Figma design generation if **any** of the following conditions apply:

1. **User explicitly requests spec only**:
   - "Just generate the design spec"
   - "Only write design-spec.md"
   - "Proceed without Figma"

2. **MCP connection is unavailable** (confirmed in 3.2 below)

### 3.2 Check MCP Connection

```bash
claude mcp list
```

Items to verify:
- Whether `TalkToFigma` is in the list
- Whether the status is `✓ Connected`

### 3.3 When MCP Connection Is Unavailable

If MCP is not configured, provide instructions to the user and complete:

```
The design specification document has been generated.

📄 File: docs/{backlog-keyword}/design-spec.md

To also generate Figma designs, cursor-talk-to-figma-mcp setup is required.
Setup instructions:
1. Install Bun: curl -fsSL https://bun.sh/install | bash
2. Register MCP: claude mcp add "TalkToFigma" -s local -- ~/.bun/bin/bunx cursor-talk-to-figma-mcp@latest
3. Install Figma plugin: https://www.figma.com/community/plugin/1485687494525374295

After setup is complete, run again to additionally generate the Figma design.

FE development can proceed using design-spec.md as reference.
```

### 3.4 When MCP Connection Is Successful

Confirm WebSocket server is running, then proceed to Figma design generation:

```bash
# Check if WebSocket server is running (port 3055)
lsof -i :3055 | grep LISTEN
```

**If the server is not running**, start it automatically in the background:

```
Bash(
  command: "~/.bun/bin/bun run ~/.claude/cursor-talk-to-figma-mcp/src/socket.ts",
  description: "Start Figma WebSocket server",
  run_in_background: true
)
```

Proceed to **4. Generate Figma Design** after connecting to the channel.

---

## 4. Generate Figma Design (Optional)

Execute only when MCP connection is successful.

### 4.1 Connect to Channel

```javascript
// Connect to channel (required - run before all operations)
mcp__TalkToFigma__join_channel({
  "channel": "ABC123"  // Channel code displayed in the plugin
})
```

### 4.2 Design Generation Order

1. **Query document info**: Check existing styles with `get_document_info`, `get_styles`
2. **Create design system**: Generate color and text style frames
3. **Basic components**: Create Button, Input, Card, etc. with `create_frame`
4. **Compound components**: Create Header, Form, Modal, etc.
5. **Screen layouts**: Create screens with `create_frame` and position elements
6. **State variations**: Add error, loading, empty state screens
7. **Apply styles**: Finalize with `set_fill_color`, `set_stroke_color`, etc.

---

## 5. Add Figma Links to design-spec.md (Optional)

After completing Figma design generation, add the following information to design-spec.md:

```markdown
## Figma Design

### Figma File Link
- File URL: https://www.figma.com/file/{fileID}

### Component List
| Component Name | Component Key | Description |
|----------------|---------------|-------------|
| Button/Primary | {key} | Primary button |
| Input/Default | {key} | Default input field |

### Screen List
| Screen Name | Node ID | Description |
|-------------|---------|-------------|
| Login | {ID} | Login screen |
| Signup | {ID} | Sign-up screen |
```

---

## References

- Component guide: [references/component-guide.md](references/component-guide.md)
- Accessibility guide: [references/accessibility-guide.md](references/accessibility-guide.md)
- cursor-talk-to-figma-mcp repository: https://github.com/grab/cursor-talk-to-figma-mcp

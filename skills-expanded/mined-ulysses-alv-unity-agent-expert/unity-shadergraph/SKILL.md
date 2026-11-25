---
name: unity-shadergraph
description: >
  Unity 6000.3 LTS Shader Graph (com.unity.shadergraph@17.6) workflow for creating
  and editing visual shaders. Trigger: When creating/editing shader graphs, working
  with nodes, properties, keywords, custom render textures, or any Shader Graph task.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Creating new shader graph assets
- Adding and connecting nodes in a shader graph
- Working with the Node Library (Artistic, Math, Input, Procedural, UV, etc.)
- Configuring Block nodes in Master Stack (Vertex/Fragment contexts)
- Adding Sticky Notes for annotations
- Managing Keywords for multi-variant shaders
- Creating Custom Render Textures
- Importing and using Shader Graph samples (UGUI, Production-Ready, Terrain, etc.)
- Setting up shader properties on the Blackboard

## Critical Patterns

### Creating a Shader Graph

| Method | Path |
|--------|------|
| From Template | Right-click **Create** > **Shader Graph** > **From Template** |
| Preset Target (URP Lit) | Right-click **Create** > **Shader Graph** > **URP** > **Lit Shader Graph** |
| Blank Graph | Right-click **Create** > **Shader Graph** > **Blank Shader Graph** |

### Shader Graph Window Navigation

- **Pan**: Hold `Alt` + drag with left mouse button
- **Zoom**: Mouse scroll wheel
- **Select Multiple**: Hold left mouse button + drag marquee
- **Create Node**: Right-click workspace > **Create Node** or press `Space`
- **Open Node Docs**: Select node + press `F1`

### Node Quick Creation (Windows)

| Node | Shortcut | Node | Shortcut |
|------|----------|------|----------|
| Add | `Alt + A` | Multiply | `Alt + M` |
| Blend | `Alt + B` | Normal Vector | `Alt + N` |
| Boolean | `Alt + 0` | Position | `Alt + V` |
| Branch | `Alt + Y` | Power | `Alt + P` |
| Color | `Alt + C` | Remap | `Alt + R` |
| Divide | `Alt + D` | Sample Texture 2D | `Alt + X` |
| Float | `Alt + 1` | Smoothstep | `Alt + "` |
| Gradient | `Alt + G` | Split | `Alt + E` |
| Lerp | `Alt + L` | Step | `Alt + J` |
| Mask | `Alt + K` | Subtract | `Alt + S` |
| Normalize | `Alt + Z` | Tiling And Offset | `Alt + O` |
| One Minus | `Alt + |` | Time | `Alt + T` |
| UV | `Alt + U` | Vector 2/3/4 | `Alt + 2/3/4` |

### Master Stack Structure

The Master Stack has two **Contexts**:

| Context | Purpose | Block Types |
|---------|---------|-------------|
| **Vertex** | Vertex function (position, normal, UVs) | Position, Normal, Vertex Color, Tangent |
| **Fragment** | Pixel function (color, emission, alpha) | Base Color, Metallic, Smoothness, Emission |

### Property Type Reference

| Type | Inspector UI | Notes |
|------|--------------|-------|
| Float | Scalar field, Slider, Integer, Enum | Slider has Power/Integer variants |
| Vector 2/3/4 | Vector4 field (unused components hidden) | - |
| Color | Color picker (sRGB or HDR mode) | HDR for bloom effects |
| Boolean | Toggle | - |
| Texture 2D | Texture slot | Sampler state configurable |
| Gradient | Gradient editor | Used with Sample Gradient node |
| Cubemap | Texture slot | For environment mapping |
| Sampler State | Dropdown | Filter mode, wrap mode |

### Keywords (Multi-Variant Shaders)

Keywords create shader variants based on conditions:

| Keyword Type | Use Case |
|--------------|----------|
| Boolean | Toggle features on/off |
| Enum | Select from multiple options |
| Inline | Runtime condition checks |

## Node Library Reference

All nodes are documented in Markdown at `skill/reference/`.

### Graph Nodes

| Node Category | Path |
|--------------|------|
| Artistic Nodes | `skill/reference/Artistic-Nodes.html-Artistic-Nodes.md` |
| Math Nodes | `skill/reference/Math-Nodes.html-Math-Nodes.md` |
| Input Nodes | `skill/reference/Input-Nodes.html-Input-Nodes.md` |
| Procedural Nodes | `skill/reference/Procedural-Nodes.html-Procedural-Nodes.md` |
| UV Nodes | `skill/reference/UV-Nodes.html-UV-Nodes.md` |
| Channel Nodes | `skill/reference/Channel-Nodes.html-Channel-Nodes.md` |
| Utility Nodes | `skill/reference/Utility-Nodes.html-Utility-Nodes.md` |
| UI Nodes | `skill/reference/ui-nodes.html-ui-nodes.md` |
| Custom Render Texture Nodes | `skill/reference/Custom-Render-Texture-Nodes.html-Custom-Render-Texture-Nodes.md` |

### Individual Node Reference Examples

| Node | Path |
|------|------|
| Add Node | `skill/reference/Add-Node.html-Add-Node.md` |
| Sample Texture 2D | `skill/reference/Sample-Texture-2D-Node.html-Sample-Texture-2D-Node.md` |
| Lerp Node | `skill/reference/Lerp-Node.html-Lerp-Node.md` |
| Split Node | `skill/reference/Split-Node.html-Split-Node.md` |
| UV Node | `skill/reference/UV-Node.html-UV-Node.md` |
| Tiling And Offset | `skill/reference/Tiling-And-Offset-Node.html-Tiling-And-Offset-Node.md` |
| Time Node | `skill/reference/Time-Node.html-Time-Node.md` |
| Gradient Node | `skill/reference/Gradient-Node.html-Gradient-Node.md` |
| Property Node | `skill/reference/Property-Node.html-Property-Node.md` |
| Block Node | `skill/reference/Block-Node.html-Block-Node.md` |
| Custom Function | `skill/reference/Custom-Function-Node.html-Custom-Function-Node.md` |

### Additional Reference Pages

| Topic | Path |
|-------|------|
| Getting Started | `skill/reference/Getting-Started.html-Getting-Started.md` |
| Create Shader Graph | `skill/reference/Create-Shader-Graph.html-Create-Shader-Graph.md` |
| Shader Graph Window | `skill/reference/Shader-Graph-Window.html-Shader-Graph-Window.md` |
| Node Library | `skill/reference/Node-Library.html-Node-Library.md` |
| Master Stack | `skill/reference/Master-Stack.html-Master-Stack.md` |
| Blackboard | `skill/reference/Blackboard.html-Blackboard.md` |
| Property Types | `skill/reference/Property-Types.html-Property-Types.md` |
| Keywords | `skill/reference/Keywords.html-Keywords.md` |
| Sticky Notes | `skill/reference/Sticky-Notes.html-Sticky-Notes.md` |
| Custom Render Texture | `skill/reference/Custom-Render-Texture.html-Custom-Render-Texture.md` |
| Keyboard Shortcuts | `skill/reference/Keyboard-shortcuts.html-Keyboard-shortcuts.md` |
| Shader Graph Samples | `skill/reference/ShaderGraph-Samples.html-ShaderGraph-Samples.md` |

## Code Examples

### Basic PBR Fragment Setup

```
Vertex Context:
- Position Node → Position Block
- Normal Vector Node → Normal Block
- UV Node → UV Block (if needed)

Fragment Context:
- Base Color: Color Node → Base Color Block
- Metallic: Float (0-1) → Metallic Block
- Smoothness: Float (0-1) → Smoothness Block
- Normal: Normal Map Texture → Normal Block
```

### Animated UV Tiling

```
Time Node (Time) → Tiling And Offset Node (UV)
                           ↓
                   Sample Texture 2D (Tex, UV)
                           ↓
                   Fragment Base Color
```

### Sticky Note Creation

Right-click workspace → **Create Sticky Note** → Add title and body text

### Keyword for Feature Toggle

1. Add Boolean/Enum keyword in Blackboard
2. Use Keyword Node in graph
3. Connect to Branch node for conditional logic

## Commands

### Keyboard Shortcuts (Windows)

```bash
# Navigation & View
Frame All:          A
Frame Selection:    F
Toggle Blackboard:  Shift + 1
Toggle Inspector:   Shift + 2
Toggle Main Preview: Shift + 3

# Edit Operations
Undo:               Ctrl + Z
Redo:               Ctrl + Y
Copy:               Ctrl + C
Cut:                Ctrl + X
Paste:              Ctrl + V
Duplicate:          Ctrl + D
Save:               Ctrl + S
Save As:            Ctrl + Shift + S

# Node Operations
Open Create Node:   Space
Toggle Node Preview: Ctrl + T
Toggle Node Collapsed: Ctrl + P
Insert Redirect:    Ctrl + R
Open Node Docs:     F1

# Group Operations
Group:              Ctrl + G
Ungroup:            Ctrl + U
```

## Resources

- **Samples**: Import via Package Manager → Shader Graph → Samples
  - UGUI Shaders (UI elements)
  - Production-Ready (Lit, Decal, Rock, Water, Weather)
  - Terrain (Layers, Components, Packing)
  - Procedural Patterns
  - Node Reference
  - Feature Examples
  - Custom Lighting
  - Custom Material Property Drawers

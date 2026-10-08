# VoiceForge 3D - Cursor Agent Rules

## Project Context
You are building **VoiceForge 3D**, a voice-first, AI-assisted **parametric 3D design application for 3D printing**. This is a local-first Next.js 15 application with React Three Fiber for 3D rendering, JSCAD for parametric modeling, and Claude AI for natural language to CAD code generation.

**Target Output:** Print-ready 3MF/STL files for **Orca Slicer** and other slicers.

---

## ⚠️ MVP SCOPE — LOCAL-FIRST, FULLY FEATURED

**This MVP is a COMPLETE 3D printing design tool running locally:**
- ✅ **Full Parametric Modeling** — JSCAD-based CSG operations (union, subtract, intersect)
- ✅ **AI-Powered Design** — Claude generates JSCAD code from natural language
- ✅ **Voice Control** — Web Speech API + optional Whisper for commands
- ✅ **DFM Knowledge** — AI knows wall thickness, overhangs, tolerances
- ✅ **Component Library** — Standard dimensions for RPi, Arduino, NEMA17, etc.
- ✅ **3MF Export** — Native Orca Slicer format with metadata
- ✅ **Mesh Validation** — Manifold checks, wall thickness, repair
- ✅ **Local Storage** — IndexedDB for projects, no cloud needed

**NOT in MVP (Post-MVP additions):**
- ❌ No authentication / user accounts
- ❌ No cloud database
- ❌ No real-time collaboration
- ❌ No generative AI mesh (Meshy, etc.) — focus on parametric design

---

## Core Architecture

### Tech Stack (MVP)
```
next: ^15.0.0              # App Router, Server Components
react: ^19.0.0             # Latest React with Compiler
three: ^0.168.0            # WebGL rendering
@react-three/fiber: ^9.0.0 # React bindings for Three.js
@react-three/drei: ^9.100.0 # Useful helpers
@react-three/csg: ^3.0.0   # CSG operations in R3F
zustand: ^5.0.0            # State management
ai: ^4.0.0                 # Vercel AI SDK
@jscad/modeling: ^2.0.0    # Parametric CSG operations
jszip: ^3.10.0             # 3MF export (ZIP archive)
idb-keyval: ^6.0.0         # IndexedDB storage
tailwindcss: ^4.0.0        # Styling
```

### File Structure
```
app/
├── page.tsx                   # Main editor (single page app)
├── api/
│   └── ai/
│       └── generate/route.ts  # Claude code generation endpoint
components/
├── canvas/
│   ├── Scene.tsx              # R3F Canvas wrapper
│   ├── CSGPreview.tsx         # Renders JSCAD output
│   ├── GridFloor.tsx          # Build plate visualization
│   └── Controls.tsx           # Camera controls
├── panels/
│   ├── AIChat.tsx             # Natural language input
│   ├── CodeEditor.tsx         # JSCAD code view/edit
│   ├── PropertiesPanel.tsx    # Object parameters
│   └── ExportPanel.tsx        # Export to 3MF/STL
├── voice/
│   └── VoiceInput.tsx         # Speech recognition
├── ui/
│   └── ...                    # Buttons, dialogs, toasts
lib/
├── jscad/
│   ├── executor.ts            # Runs JSCAD code safely
│   ├── to-three.ts            # Converts JSCAD → Three.js geometry
│   └── primitives.ts          # Common shape generators
├── export/
│   ├── 3mf.ts                 # 3MF generation
│   ├── stl.ts                 # STL binary/ASCII export
│   ├── validate.ts            # Mesh validation
│   └── repair.ts              # Auto-repair functions
├── ai/
│   ├── system-prompt.ts       # DFM rules for Claude
│   ├── tools.ts               # AI tool definitions
│   └── component-library.ts   # Standard component dimensions
├── storage/
│   └── local.ts               # IndexedDB utilities
├── constants/
│   ├── dfm.ts                 # Design for manufacturing rules
│   ├── components.ts          # RPi, Arduino, NEMA17 dimensions
│   └── materials.ts           # PLA, PETG, ABS properties
types/
├── jscad.d.ts                 # JSCAD type definitions
├── scene.d.ts                 # Scene object types
└── export.d.ts                # Export types
docs/
├── DFM_KNOWLEDGE_BASE.md      # Printing rules reference
├── COMPONENT_LIBRARY.md       # Standard component specs
└── EXPORT_PIPELINE.md         # Export workflow
```

---

## Design for Manufacturing (DFM) Rules

**The AI MUST apply these rules when generating JSCAD code:**

### Wall Thickness
```typescript
const DFM = {
  WALL_MIN: 1.2,        // mm - minimum for structural parts
  WALL_DEFAULT: 2.0,    // mm - safe default
  FEATURE_MIN: 0.4,     // mm - single extrusion width
};
```

### Overhangs & Supports
```typescript
const OVERHANG = {
  SAFE_ANGLE: 45,       // degrees from vertical
  USE_CHAMFER: true,    // Add 45° chamfers to bottom edges
  CHAMFER_SIZE: 0.5,    // mm - elephant foot prevention
};
```

### Tolerances
```typescript
const TOLERANCE = {
  CLEARANCE_FIT: 0.3,   // mm - for moving parts
  PRESS_FIT: -0.1,      // mm - interference fit
  HOLE_OVERSIZE: 0.2,   // mm - compensate for shrinkage
};
```

### Screw Holes (Reference)
```typescript
const SCREW_HOLES = {
  M2: { clearance: 2.2, tap: 1.6 },
  M2_5: { clearance: 2.7, tap: 2.05 },
  M3: { clearance: 3.2, tap: 2.5 },
  M4: { clearance: 4.3, tap: 3.3 },
  M5: { clearance: 5.3, tap: 4.2 },
};
```

---

## JSCAD Code Patterns

### Basic Part Generation
```typescript
// AI generates this from "make a 50x30x20mm box with rounded edges"
import { cuboid, roundedCuboid } from '@jscad/modeling/primitives';
import { translate } from '@jscad/modeling/transforms';

const main = () => {
  const WALL = 2.0;          // Wall thickness
  const CORNER_RADIUS = 2.0; // Rounded corners
  
  return roundedCuboid({
    size: [50, 30, 20],
    roundRadius: CORNER_RADIUS,
    segments: 16,
  });
};
```

### CSG Operations
```typescript
// "Make a box with a hole for M3 screw"
import { cuboid, cylinder } from '@jscad/modeling/primitives';
import { subtract, union } from '@jscad/modeling/booleans';
import { translate } from '@jscad/modeling/transforms';

const main = () => {
  const M3_CLEARANCE = 3.2;
  
  const body = cuboid({ size: [30, 30, 10] });
  const hole = translate([0, 0, 0],
    cylinder({ radius: M3_CLEARANCE / 2, height: 12 })
  );
  
  return subtract(body, hole);
};
```

### Component Enclosure
```typescript
// "Make a case for Raspberry Pi 4"
import { RPI_4_DIMENSIONS } from './components';

const main = () => {
  const CLEARANCE = 0.3;
  const WALL = 2.0;
  const STANDOFF_HEIGHT = 5;
  
  const pcb = RPI_4_DIMENSIONS;
  const innerSize = [
    pcb.width + CLEARANCE * 2,
    pcb.height + CLEARANCE * 2,
    pcb.totalHeight + CLEARANCE,
  ];
  
  // Generate enclosure with mounting posts
  // ... full implementation
};
```

---

## AI System Prompt (Claude)

The AI endpoint includes this context:

```typescript
const SYSTEM_PROMPT = `You are a 3D printing design expert generating JSCAD code.

## DFM Rules (ALWAYS APPLY):
- Minimum wall thickness: 1.2mm for structural, 2.0mm default
- Maximum overhang angle: 45° without supports
- Add 0.3mm clearance for moving parts
- Add 0.5mm chamfer to bottom edges (elephant foot)
- Oversize holes by 0.2mm for shrinkage compensation

## Component Library:
You have access to standard dimensions for:
- Raspberry Pi (all models)
- Arduino (Uno, Nano, Mega)
- ESP32 DevKits
- NEMA17 stepper motors
- Common servos (SG90, MG996R)
- Standard fasteners (M2-M8)

## Output Format:
Generate valid JSCAD code using @jscad/modeling.
Include DFM parameters as named constants at top.
Add comments explaining design decisions.
Export a main() function returning the geometry.

## Validation:
Before returning, verify:
- All walls >= 1.2mm
- Holes are accessible for printing
- Features are larger than 0.4mm
- Part fits in 256x256x256mm build volume`;
```

---

## Export Pipeline

### 3MF Export (Preferred for Orca Slicer)
```typescript
import JSZip from 'jszip';

export async function exportTo3MF(mesh: Mesh, options: ExportOptions): Promise<Blob> {
  const zip = new JSZip();
  
  // Core 3MF structure
  zip.file('[Content_Types].xml', generateContentTypes());
  zip.file('_rels/.rels', generateRelationships());
  zip.file('3D/3dmodel.model', generateModelXML(mesh));
  
  // Thumbnail for Orca Slicer preview
  if (options.thumbnail) {
    zip.file('Metadata/thumbnail.png', options.thumbnail, { base64: true });
  }
  
  return zip.generateAsync({ type: 'blob' });
}
```

### Mesh Validation Before Export
```typescript
const VALIDATION_CHECKS = [
  { id: 'manifold', check: isManifold, severity: 'error' },
  { id: 'no_self_intersect', check: noSelfIntersections, severity: 'error' },
  { id: 'min_wall', check: (m) => minWallThickness(m) >= 1.2, severity: 'warning' },
  { id: 'fits_bed', check: (m) => fitsIn(m, [256, 256, 256]), severity: 'error' },
];
```

---

## Core Principles

### 1. RADICAL OBSERVABILITY
- Every error shows a toast notification
- Invalid geometry turns neon pink
- Validation status always visible
- DFM violations highlighted in 3D view

### 2. SINGLE SOURCE OF TRUTH
- All scene state in Zustand store
- JSCAD code is the source, mesh is derived
- TypeScript interfaces for everything

### 3. NON-DESTRUCTIVE WORKFLOWS
- Full undo/redo history
- JSCAD code always recoverable
- Export never modifies original

### 4. PRINT-FIRST DESIGN
- All defaults optimize for printability
- DFM warnings before export
- Auto-repair option for common issues

---

## Voice Commands

| Command | Action |
|---------|--------|
| "Add a cube" | Generate JSCAD cube primitive |
| "Make it bigger" | Scale selected object |
| "Add screw hole M3" | Boolean subtract cylinder |
| "Make a case for Pi 4" | Generate full enclosure |
| "Export for printing" | Validate + export 3MF |
| "Check if printable" | Run DFM validation |
| "Undo" / "Redo" | History navigation |

---

## Environment Variables (MVP)

```bash
# AI Provider (choose one)
AI_PROVIDER=anthropic      # Options: ollama, anthropic, openai, groq, openrouter, together, google

# For Ollama (LOCAL - FREE)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=codellama:13b

# For Anthropic Claude (CLOUD - BEST QUALITY)
ANTHROPIC_API_KEY=sk-ant-xxxxx

# For OpenAI (CLOUD)
OPENAI_API_KEY=sk-xxxxx

# For Groq (CLOUD - FAST)
GROQ_API_KEY=gsk_xxxxx

# Feature Flags
NEXT_PUBLIC_ENABLE_WEBGPU=true
NEXT_PUBLIC_ENABLE_VOICE=true
```

**Note:** Only ONE AI provider needs to be configured. Ollama allows fully local operation with no cloud dependencies.

---

## Performance Rules

### R3F Checklist
- [ ] `frameloop="demand"` when not animating
- [ ] Memoize JSCAD→Three conversion
- [ ] Use `<Bvh>` for raycasting
- [ ] Limit CSG preview to 10k triangles
- [ ] Debounce parameter changes (300ms)

### State Updates
- Batch related updates with Zustand
- Throttle JSCAD execution (500ms)
- Web Worker for heavy CSG operations

---

## Do NOT:
- Use `any` type
- Skip mesh validation before export
- Ignore DFM rules in generated code
- Block UI during JSCAD execution
- Export non-manifold meshes without warning

## Do:
- Apply DFM rules to ALL generated geometry
- Validate mesh before every export
- Show clear error messages
- Include component dimensions in AI context
- Generate parametric (editable) code
- Test exports in actual Orca Slicer

## Git Workspace Hygiene
- Delete feature branches after merge — no stale branches
- Remove worktrees when done — no orphaned worktrees
- Prune stale remote references (`git remote prune origin`)
- Clean working directory when task is done (`git status` clean)
- Delete abandoned branches — don't leave dead work behind
- Main branch is the only permanent artifact — everything else is temporary

## Epoch Data Tracking
- Use Epoch for time estimation before starting tasks (MCP, REST API, or CLI)
- Record actual time after completing tasks (`record_actual`)
- Every project feeds data to Epoch — it's how the system learns
- Epoch only works if everyone contributes estimate-vs-actual data

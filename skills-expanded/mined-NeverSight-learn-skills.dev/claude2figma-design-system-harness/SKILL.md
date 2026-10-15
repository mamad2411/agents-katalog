---
name: claude2figma-design-system-harness
description: Enforce Design System compliance in AI-generated Figma designs with 4 skills that bind components, tokens, and styles
triggers:
  - set up figma design system skills
  - install claude2figma harness
  - enforce design tokens in figma
  - keep ai designs on design system rails
  - bind figma components to design tokens
  - start figma design system session
  - configure claude code figma skills
  - verify figma design system compliance
---

# claude2figma Design System Harness

> Skill by [ara.so](https://ara.so) — Design Skills collection.

A harness for Claude Code + Figma that enforces Design System compliance in AI-generated designs. Prevents hardcoded values, ensures components stay linked, and binds all visual properties to tokens and styles.

## What This Does

When AI writes to Figma without guidance, it creates everything from scratch:
- Hardcoded hex colors instead of color tokens
- Raw spacing values instead of spacing variables
- Components rebuilt from primitives instead of instances

**claude2figma fixes this with 4 Claude Code Skills:**

1. **figma-preflight** — 3-step parallel check that loads Token Map + Component Registry
2. **component-rules** — Library-first lookup, Auto Layout patterns, semantic naming
3. **figma-style-binding** — Enforces Variable/Style binding + post-write QA verification
4. **reference-interpreter** — Converts screenshots/references → structured Design Brief

Every design operation follows: **search DS → create Instances → bind tokens → verify**.

## Installation

### Prerequisites

```bash
# 1. Claude Code installed (CLI, Desktop, or VS Code)
# 2. Figma MCP Server installed and authenticated
npm install -g @anthropic-ai/figma-mcp

# 3. A Figma file with a Design System (local or linked library)
```

### Setup

```bash
# Clone the repo
git clone https://github.com/senlindesign/claude2figma.git
cd claude2figma

# Copy skills to your project
cp -r .claude/skills/* /path/to/your-project/.claude/skills/

# Copy settings
cp .claude/settings.json /path/to/your-project/.claude/settings.json

# Copy CLAUDE.md template
cp CLAUDE.md.template /path/to/your-project/CLAUDE.md
```

### Configure CLAUDE.md

```markdown
# Figma Design Project

- **Figma file:** https://www.figma.com/design/YOUR_FILE_KEY/...
- **Fonts:** [leave blank — auto-detected by preflight]
- **Session goal:** Build login page with email/password fields

## Rules

1. Every visual value must bind to a Style or Variable.
2. Always search connected libraries before building any component from scratch.
3. Never start designing before the Design Brief is confirmed.
```

## Key Skills Structure

Your project should have this structure after installation:

```
your-project/
├── CLAUDE.md                          # Config: Figma URL, fonts, rules
└── .claude/
    ├── settings.json                  # Permissions + QA Hook
    └── skills/
        ├── figma-preflight/           # Skill 1: Parallel check + Token Map
        │   └── SKILL.md
        ├── component-rules/           # Skill 2: Library-first patterns
        │   └── SKILL.md
        ├── figma-style-binding/       # Skill 3: Token binding + QA
        │   └── SKILL.md
        └── reference-interpreter/     # Skill 4: Reference → Design Brief
            └── SKILL.md
```

## Usage Patterns

### Pattern 1: Start Every Session with Preflight

```javascript
// User says: "let's start" or "run preflight"
// Claude executes figma-preflight skill:

// 1. Parse Figma URL from CLAUDE.md
const fileKey = extractFileKey(CLAUDE_MD_CONTENT);

// 2. Parallel preflight checks
const [mcpStatus, fileAccess, dsAssets] = await Promise.all([
  checkMCPConnection(),
  verifyFilePermissions(fileKey),
  loadDesignSystemAssets(fileKey)
]);

// 3. Build Token Map
const tokenMap = {
  colors: await figma.getLocalVariableCollectionsAsync('COLOR'),
  spacing: await figma.getLocalVariableCollectionsAsync('NUMBER'),
  textStyles: await figma.getLocalTextStylesAsync(),
  effectStyles: await figma.getLocalEffectStylesAsync()
};

// 4. Build Component Registry
const components = await figma.getLocalComponentsAsync();
const componentRegistry = components.map(c => ({
  name: c.name,
  id: c.id,
  variantProperties: c.componentPropertyDefinitions
}));

// Output: ✓ Preflight complete — 47 tokens, 23 components loaded
```

### Pattern 2: Component-First Design

```javascript
// User says: "Add a primary button"
// Claude executes component-rules + figma-style-binding skills:

// 1. Search Component Registry first
const button = componentRegistry.find(c => 
  c.name.toLowerCase().includes('button') &&
  c.variantProperties?.variant?.includes('primary')
);

if (!button) {
  throw new Error('No Button/Primary in DS — check library or request custom component');
}

// 2. Create Instance (not from scratch)
const instance = figma.createInstance();
instance.mainComponent = figma.getNodeById(button.id);

// 3. Set variant properties (validated against componentPropertyDefinitions)
instance.setProperties({ variant: 'primary', size: 'medium' });

// 4. Bind any overrides to tokens
if (instance.children[0].fills) {
  const primaryColorVar = tokenMap.colors.find(v => v.name === 'primary');
  instance.children[0].fills = [{
    type: 'SOLID',
    color: { r: 0, g: 0, b: 0 }, // placeholder
    boundVariables: { color: { id: primaryColorVar.id } }
  }];
}

// 5. Auto-verify after write
await verifyTokenBindings(instance);
```

### Pattern 3: Token Binding Enforcement

```javascript
// figma-style-binding skill enforces this on EVERY visual property:

// ✅ CORRECT: Bound to variable
node.fills = [{
  type: 'SOLID',
  boundVariables: { color: { id: tokenMap.colors.find(v => v.name === 'surface').id } }
}];

// ❌ WRONG: Hardcoded hex value
node.fills = [{ type: 'SOLID', color: { r: 1, g: 1, b: 1 } }]; // REJECTED by QA

// Post-write QA verification:
async function verifyTokenBindings(node) {
  const violations = [];
  
  if (node.fills && !node.fills[0]?.boundVariables) {
    violations.push(`${node.name}: fills not bound to token`);
  }
  
  if (node.textStyleId === '') {
    violations.push(`${node.name}: no text style bound`);
  }
  
  if (violations.length > 0) {
    throw new Error(`Token binding violations:\n${violations.join('\n')}`);
  }
}
```

### Pattern 4: Reference-Driven Design

```javascript
// User shares screenshot and says: "Build this"
// Claude executes reference-interpreter skill:

// 1. Analyze reference → structured Design Brief
const designBrief = {
  layout: 'Two-column grid, 16px gap',
  components: [
    { type: 'Header', contains: ['Logo', 'Navigation/Horizontal', 'Button/Primary'] },
    { type: 'Hero Section', contains: ['Heading/H1', 'Body/Large', 'Button Group'] }
  ],
  tokens: {
    colors: ['primary', 'surface', 'on-surface'],
    spacing: ['space-4', 'space-8', 'space-16'],
    typography: ['heading-1', 'body-large']
  }
};

// 2. Output Design Brief to user for confirmation
// 3. User says "looks good"
// 4. Claude builds section by section, following component-rules + style-binding
```

## Configuration

### settings.json — QA Hook

```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/figma-mcp"]
    }
  },
  "qaHooks": {
    "postWrite": "verifyTokenBindings"
  },
  "permissions": {
    "figma": ["read", "write"]
  }
}
```

### CLAUDE.md — Session Rules

```markdown
# Figma Design Project

- **Figma file:** https://www.figma.com/design/ABC123/...
- **Session goal:** Build dashboard with data table and filters

## Rules

1. Run preflight before starting design work
2. Every component must be an Instance, not built from scratch
3. Every color, font, spacing must bind to a token
4. Take screenshot after each major section for verification
```

## Real-World Workflow

```bash
# Terminal in your project
$ claude-code chat

User: "let's start"

Claude:
  ✓ MCP connection verified
  ✓ File permissions confirmed
  ✓ Design System loaded: 47 tokens, 23 components
  
  Ready to design. What are we building?

User: "Build a login form with email, password, and a submit button"

Claude:
  [Searches Component Registry]
  Found: Form/Vertical, Input/Email, Input/Password, Button/Primary
  
  [Creates Instances + binds tokens]
  - Form container: padding bound to space-6
  - Input fields: text style bound to body-medium
  - Submit button: fills bound to primary color token
  
  [Takes screenshot]
  ✓ Verification passed — all tokens bound
  
  Screenshot: [shows form in Figma]

User: "Add a forgot password link below the form"

Claude:
  [Searches for Link component]
  Not found in registry — creating text node with hyperlink style
  
  [Binds text style + color token]
  ✓ Verification passed
```

## Troubleshooting

### Error: "No components found in registry"

```javascript
// Cause: Working in a new file without linked library
// Fix: Link your DS library in Figma first

// In Figma: Assets → Libraries → Enable your DS library
// Then re-run preflight to rebuild Component Registry
```

### Error: "Invalid variant property value"

```javascript
// Cause: setProperties() called with invalid variant value
// Fix: Read componentPropertyDefinitions first

const component = figma.getNodeById(componentId);
const validVariants = component.componentPropertyDefinitions.variant.variantOptions;

// Only use values from validVariants array
instance.setProperties({ variant: validVariants[0] });
```

### Error: "Token binding verification failed"

```javascript
// Cause: A property was set with a raw value instead of binding to token
// Fix: Always use boundVariables

// ❌ WRONG
node.fills = [{ type: 'SOLID', color: { r: 0.2, g: 0.4, b: 0.8 } }];

// ✅ CORRECT
const token = tokenMap.colors.find(v => v.name === 'primary');
node.fills = [{
  type: 'SOLID',
  boundVariables: { color: { id: token.id } }
}];
```

### Working with Library Variables (Can't See Them Locally)

```javascript
// Limitation: getLocalVariablesAsync() only returns file-local variables
// Workaround 1: Instances inherit bindings automatically (no action needed)

// Workaround 2: Import library variable for new frames
const libraryVarKey = 'VariableID:123:456'; // from library file
const importedVar = await figma.variables.importVariableByKeyAsync(libraryVarKey);

frame.fills = [{
  type: 'SOLID',
  boundVariables: { color: { id: importedVar.id } }
}];
```

## Best Practices

1. **Always run preflight** at session start — loads Token Map + Component Registry
2. **Search before creating** — check componentRegistry before building any UI element
3. **Bind, don't hardcode** — every visual property must reference a token
4. **Verify after write** — QA hook catches token binding violations automatically
5. **Confirm Design Brief** — when working from reference, output structured brief before building

## API Reference

### Key Figma MCP Methods

```javascript
// File access
const file = await figma.getFileAsync(fileKey);

// Design System assets
const variables = await figma.getLocalVariableCollectionsAsync();
const textStyles = await figma.getLocalTextStylesAsync();
const components = await figma.getLocalComponentsAsync();

// Instance creation
const instance = figma.createInstance();
instance.mainComponent = masterComponent;
instance.setProperties({ variant: 'primary' });

// Token binding
node.fills = [{
  type: 'SOLID',
  boundVariables: { color: { id: variableId } }
}];
node.textStyleId = textStyle.id;

// Verification
const bindings = node.boundVariables;
const hasColorBinding = bindings?.fills?.[0]?.color !== undefined;
```

## When to Use This

| ✅ Good For | ❌ Not For |
|------------|-----------|
| Building pages from existing DS | Creating a DS from scratch |
| Natural language → Figma design | Pixel-perfect illustration |
| Ensuring 100% token compliance | FigJam / whiteboard work |
| Working in DS file or with linked library | Free-form design without DS |

---

**License:** MIT  
**Repository:** https://github.com/senlindesign/claude2figma  
**Figma MCP Server:** https://www.npmjs.com/package/@anthropic-ai/figma-mcp

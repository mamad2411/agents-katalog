---
name: design-implementation-validator
description: >
    Automated Figma-to-code validation pipeline for UI components. Extracts design
    specifications from Figma across all breakpoints, maps to design system tokens
    (Tailwind, Styled Components, or vanilla CSS), generates responsive code with
    mobile-first approach, and validates with Playwright. Provides auto-healing
    suggestions and detailed validation reports. Use this skill when implementing
    UI components from Figma designs, validating existing components against designs,
    or ensuring pixel-perfect responsive implementations. Keywords: Figma validation,
    design system mapping, responsive design, Playwright testing, UI components,
    pixel-perfect, mobile-first, Tailwind, Styled Components, frontend validation.
metadata:
    author: yuridefranca
    version: '1.0'
    created: '2026-06-01'
    updated: '2026-06-01'
compatibility: >
    Requires Figma MCP server and Playwright MCP server.
    Dev server must be available for validation.
---

# Design Implementation Validator

**Automated Figma-to-code validation pipeline** ensuring pixel-perfect responsive UI implementations.

## Purpose

Validates frontend implementations match Figma designs through a 5-phase process:

1. **Extract** design specs from Figma → [Phase 1](references/phase-1-extraction.md)
2. **Map** to design system tokens → [Phase 2](references/phase-2-mapping.md)
3. **Generate** responsive code → [Phase 3](references/phase-3-generation.md)
4. **Validate** with Playwright → [Phase 4](references/phase-4-validation.md)
5. **Auto-heal** with fixes → [Phase 5](references/phase-5-fixes.md)

## When to Use

✅ **Use when:**

- Implementing new UI components from Figma
- Validating existing components against designs
- Frontend Engineer agent is invoked
- User provides Figma URL
- Phase 7 (Implementation) of Feature Workflow for UI
- Phase 3/4 of Improvement Workflow for UI updates

❌ **Do NOT use:**

- No Figma design exists (prototyping/exploration)
- Backend-only tasks
- Logic-only changes without visual impact
- User explicitly opts out with `--skip-design-validation`

## Prerequisites

- Figma MCP server configured
- Playwright MCP server available
- Dev server can start or is running
- Component path identified

## Workflow Overview

### Phase 1: Design Extraction

Extract ALL breakpoints (mobile, tablet, desktop, wide) from Figma.

See [references/phase-1-extraction.md](references/phase-1-extraction.md) when extracting design specifications.

**Output:** `design-specs.json`

**Key concepts:**

- Detects Figma Variables, Design Tokens, or raw styles
- Auto-detects breakpoints from component variants
- Extracts layout, spacing, typography, colors, effects
- Mobile-first by default

### Phase 2: Design System Mapping

Auto-detect design system and map Figma values to tokens.

See [references/phase-2-mapping.md](references/phase-2-mapping.md) when mapping to design system.

**Output:** `design-system-mapping.json`

**Supports:**

- Tailwind CSS → [adapters/tailwind-adapter.md](references/adapters/tailwind-adapter.md)
- Styled Components → [adapters/styled-components-adapter.md](references/adapters/styled-components-adapter.md)
- Custom design tokens
- Vanilla CSS variables

### Phase 3: Code Generation

Generate mobile-first responsive code with design system tokens.

See [references/phase-3-generation.md](references/phase-3-generation.md) when generating component code.

**Output:** Component code file (e.g., `UserCard.tsx`)

**Strategies:**

- **Media queries** (most common, mobile-first)
- **Fluid** (clamp/calc for smooth scaling)
- **Container queries** (component-level responsive)

### Phase 4: Playwright Validation

Compare computed styles to Figma specs across all breakpoints.

See [references/phase-4-validation.md](references/phase-4-validation.md) when validating implementations.

**Output:** `validation-results.json`

**Features:**

- Smart tolerance (±1px for sub-pixel rendering)
- Detects impossible-to-match scenarios
- Optional visual regression screenshots

### Phase 5: Auto-Healing

Generate and apply fixes for validation failures.

See [references/phase-5-fixes.md](references/phase-5-fixes.md) when fixing validation issues.

**Output:** `validation-report.md` (use [template](assets/templates/validation-report-template.md))

**Capabilities:**

- Code adjustments (exact values)
- Tolerance decisions (acceptable deviations)
- Design system updates (missing tokens)
- Impossible-to-match flagging

## Design System Adapters

Load appropriate adapter based on detected system:

- **Tailwind:** [references/adapters/tailwind-adapter.md](references/adapters/tailwind-adapter.md)
- **Styled Components:** [references/adapters/styled-components-adapter.md](references/adapters/styled-components-adapter.md)

Auto-detection checks:

1. `tailwind.config.{js,ts,mjs}` → Tailwind
2. `styled-components` in package.json → Styled Components
3. `@emotion` in package.json → Emotion
4. `design-tokens.json` → Custom tokens
5. CSS variables in `:root` → Vanilla CSS

## Gotchas

- **Figma Auto Layout** constraints don't map 1:1 to CSS flexbox - verify `align-items` and `justify-content`
- **Color opacity** in Figma uses 0-1 scale, CSS uses 0-255 or percentages - convert carefully
- **Letter spacing** in Figma is pixels, CSS typically uses em/rem - divide by font-size
- **Dev server localhost** required for Playwright - won't work with network URLs
- **Computed styles** include browser defaults - filter to component-specific properties only
- **Sub-pixel rendering** varies by browser - always allow ±1px tolerance for spacing/sizing
- **Parent constraints** can make specs impossible to match - flag and document these cases
- **Breakpoint variants** must be explicitly defined in Figma or auto-detection may miss them

## Integration with Workflows

### Feature Workflow (Phase 7)

```yaml
frontend-implementation:
    - Check if task involves UI components
    - If yes and Figma URL provided:
          - Invoke design-implementation-validator
          - Wait for validation report
          - Review acceptable deviations
          - Proceed only after validation passes
```

### Improvement Workflow (Phase 3/4)

```yaml
ui-update-check:
    - If component exists with Figma link:
          - Ask: 'Should I validate against Figma design?'
          - Default: Yes (unless --skip-design-validation)
          - Invoke design-implementation-validator
```

## Output Artifacts

All files stored in `.ai-workflow/[feature]/design-validation/`:

```
design-validation/
├── design-specs.json                 # Extracted Figma specs
├── design-system-mapping.json        # Token mappings
├── validation-results.json           # Test results data
├── validation-report.md              # Human-readable report
├── design-validation.spec.ts         # Playwright test (temporary)
└── screenshots/                      # Visual regression (optional)
    ├── desktop-baseline.png
    ├── tablet-baseline.png
    └── mobile-baseline.png
```

## Usage Examples

### Example 1: New Component

```
User: "Implement UserCard from https://figma.com/file/abc123"

Skill automatically:
1. Extracts Figma specs (mobile/tablet/desktop)
2. Detects Tailwind in repo
3. Generates UserCard.tsx with responsive classes
4. Starts dev server
5. Runs Playwright validation
6. Reports: ✅ All breakpoints match
```

### Example 2: Validation with Deviation

```
User: "Update Header to match new design"

Skill:
1. Finds Figma URL in Header.tsx comments
2. Extracts updated specs
3. Identifies changes: spacing, color
4. Updates code
5. Validation finds width mismatch (parent constraint)
6. Flags as impossible-to-match with explanation
7. User reviews and approves acceptable deviation
```

## Best Practices

**Figma Organization:**

- Use Figma Variables for consistency
- Name components clearly (match code names)
- Define all breakpoint variants explicitly
- Document responsive behavior

**Code Organization:**

- Add Figma URL as comment in component file
- Use `data-testid` for Playwright selectors
- Keep design system config synced with Figma

**Validation Workflow:**

- Run validation before code review
- Document acceptable deviations
- Update Figma when constraints discovered
- Delete temporary validation tests after approval

**Team Collaboration:**

- Share validation reports with designers
- Use reports to identify design system gaps
- Establish tolerance guidelines as team

## Configuration (Optional)

Create `.design-validation.config.js` in project root:

```javascript
module.exports = {
	designSystem: 'tailwind', // auto-detect if omitted
	breakpoints: {
		mobile: { width: 375, height: 667 },
		tablet: { width: 768, height: 1024 },
		desktop: { width: 1440, height: 900 },
	},
	tolerance: {
		spacing: 1, // ±1px
		colors: 0, // exact match
		typography: 1,
	},
	autoFix: {
		enabled: true,
		requireApproval: true,
		maxIterations: 3,
	},
	devServer: {
		command: 'npm run dev',
		url: 'http://localhost:3000',
		readyPattern: 'ready in',
	},
	responsiveStrategy: 'mobile-first',
};
```

## MCP Dependencies

Required MCP servers:

1. **Figma MCP** - Design extraction
    - `figma-read-file`, `figma-get-component`, `figma-get-variables`

2. **Playwright MCP** - Validation
    - `playwright-run-test`, `playwright-screenshot`

## Success Criteria

✅ Figma specs extracted across all breakpoints  
✅ Design system mappings are accurate (no hallucinated tokens)  
✅ Generated code is idiomatic for detected system  
✅ Validation catches mismatches before review  
✅ Fix suggestions are actionable  
✅ Acceptable deviations properly documented  
✅ Designer-developer handoff friction minimized

## Related Skills

- `frontend-engineer.agent.md` - Often invokes this skill
- `minimal-impl-generator` - Generates implementation
- `refactor-optimizer` - Runs after validation
- `code-reviewer` - Final review after validation

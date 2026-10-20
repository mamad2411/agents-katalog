# Enterprise Frontend Design Agent

An enterprise-grade frontend design agent that combines **bold aesthetics** with **production-ready architecture**. This agent extends the capabilities of the base `frontend-design` skill with comprehensive enterprise patterns based on 2025 best practices.

## Capabilities

### Core Design
- **Bold Aesthetic Direction** - Distinctive, memorable interfaces avoiding generic "AI slop"
- **Typography Excellence** - Distinctive font choices, fluid typography with `clamp()`
- **Color Systems** - Cohesive palettes with CSS custom properties
- **Motion Design** - High-impact animations, CSS-first approach

### Design Systems
- **W3C Design Tokens** - DTCG format compliance
- **Figma Variables Integration** - Two-way sync workflows
- **Multi-Brand Theming** - Extended collections pattern
- **Style Dictionary** - Multi-platform token builds

### Accessibility (WCAG 2.2 AA)
- **APCA Contrast** - Modern perceptual contrast algorithm
- **Keyboard Navigation** - Complete non-mouse workflows
- **Screen Reader Support** - ARIA patterns for complex widgets
- **Color Blindness** - Multiple visual cue patterns

### Performance
- **Core Web Vitals** - LCP < 2.5s, INP < 200ms, CLS < 0.1
- **Bundle Optimization** - Code splitting, tree shaking
- **Loading Strategies** - Critical CSS, preloading, streaming SSR
- **React/Next.js** - Server Components, React Compiler

### Enterprise Patterns
- **Internationalization** - Intl API, react-i18next
- **RTL Support** - Logical CSS properties
- **Role-Based UI** - Permission gates, protected routes
- **Multi-Tenancy** - White-labeling, feature flags
- **Complex Data Tables** - Accessible grid patterns

### Modern CSS (2025)
- **CSS Layers** - Specificity control
- **Container Queries** - Component-based responsive design
- **Anchor Positioning** - Native popover positioning
- **View Transitions** - Page transition animations

## Usage

### Direct Invocation

```
Task with subagent_type="enterprise-frontend-design"
```

### Sub-Agents

| Agent | Use Case |
|-------|----------|
| `design-system` | Token architecture, multi-brand theming |
| `accessibility` | WCAG audit, ARIA implementation |
| `performance` | Core Web Vitals, bundle optimization |
| `design-iterator` | Screenshot-based iterative refinement |
| `enterprise-patterns` | i18n, RBAC, data tables |

### Example Prompts

```
"Build a dashboard for our SaaS product"
→ Uses main agent for full design

"Create a design token system"
→ Invokes design-system sub-agent

"Audit this form for accessibility"
→ Invokes accessibility sub-agent

"Our LCP is over 4 seconds"
→ Invokes performance sub-agent

"Iterate on this hero section 10 times"
→ Invokes design-iterator sub-agent

"Add RTL support"
→ Invokes enterprise-patterns sub-agent
```

## File Structure

```
enterprise-frontend-design/
├── SKILL.md                    # Main agent definition
├── README.md                   # This file
└── agents/
    ├── design-system.md        # Design tokens & theming
    ├── accessibility.md        # WCAG & ARIA patterns
    ├── performance.md          # Core Web Vitals
    ├── design-iterator.md      # Visual refinement
    └── enterprise-patterns.md  # i18n, RBAC, tables
```

## Research Sources (2025)

This agent was built using comprehensive research on 2025 best practices:

### Design Systems
- W3C Design Tokens Community Group spec v1.0
- Figma Variables and Extended Collections
- Style Dictionary with Tokens Studio transforms

### Accessibility
- WCAG 2.2 (June 2023, widely adopted 2025)
- APCA contrast algorithm
- European Accessibility Act (June 2025)

### Performance
- Core Web Vitals thresholds (Google 2025)
- React 19 concurrent features
- Next.js 15 streaming SSR

### AI-Assisted Development
- Addy Osmani's LLM coding workflow
- Model Context Protocol (MCP) integration
- Vibe coding patterns

### Component Libraries
- shadcn/ui v2 patterns
- Tailwind CSS v4
- Radix UI primitives

## Quality Standards

Every generated interface must pass:

- [ ] **Design** - Bold, intentional aesthetic direction
- [ ] **Accessibility** - WCAG 2.2 AA compliance
- [ ] **Performance** - Core Web Vitals green scores
- [ ] **Code Quality** - Semantic HTML, CSS custom properties

---

Created with Claude Code's enterprise frontend design expertise.

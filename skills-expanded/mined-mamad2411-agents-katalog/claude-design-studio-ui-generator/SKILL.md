---
name: claude-design-studio-ui-generator
description: AI-powered UI/UX generator with dual-brain architecture (Claude + OpenAI), sub-agent workflow, and design-to-code translation
triggers:
  - generate a UI component with design
  - create a styled React component
  - design a responsive interface
  - convert this code to a visual design
  - build a component with Claude Design AI
  - generate UI with accessibility checks
  - create a design-infused component
  - visualize this API as a user interface
---

# Claude Design Studio UI Generator

> Skill by [ara.so](https://ara.so) — Design Skills collection.

## Overview

**Claude-Code-Design-AI** (Claude Design Studio) is a dual-brain AI system that bridges code logic and visual design. It orchestrates Claude API for nuanced design reasoning and OpenAI API for rapid code generation, producing production-ready UI components with integrated styling, animations, and accessibility compliance.

**Key capabilities:**
- Generate UI components from natural language descriptions
- Translate raw code/APIs into visual interfaces
- Multi-agent architecture (Alpha=logic, Omega=design, Sigma=QA, Theta=optimization)
- Built-in hooks system for validation and post-processing
- Design system harmonization (Material UI, Tailwind, custom)
- Marketplace with installable skills and plugins

## Installation

### Prerequisites
- Node.js v18+ or Bun runtime
- Claude API key and/or OpenAI API key
- 512MB RAM minimum

```bash
# Clone and install
git clone https://github.com/larajuniorlara/Claude-Design-Studio.git
cd Claude-Design-Studio
npm install

# Or with Bun
bun install

# Initialize design profile
npx claude-design init

# Set up API keys
export CLAUDE_API_KEY="your-claude-api-key"
export OPENAI_API_KEY="your-openai-api-key"
```

## Core API Usage

### JavaScript/TypeScript API

```javascript
import { ClaudeDesign } from 'claude-code-design-ai';

// Initialize with API keys
const designer = new ClaudeDesign({
  claudeApiKey: process.env.CLAUDE_API_KEY,
  openaiApiKey: process.env.OPENAI_API_KEY,
  primaryRouter: 'claude',
  fallback: 'openai'
});

// Generate a component from description
const component = await designer.generateUI({
  description: "pricing table with three tiers",
  framework: "react",
  style: {
    theme: "minimalist",
    primaryColor: "#FF6B35",
    effect: "glassmorphism"
  },
  constraints: {
    responsive: true,
    accessibility: "WCAG-AA",
    animations: "subtle"
  }
});

console.log(component.code);      // React component code
console.log(component.styles);    // CSS/styled-components
console.log(component.assets);    // SVG icons, if any
```

### Generate from Existing Data

```javascript
// Transform data into visual component
const products = [
  { id: 1, name: "Laptop Pro", price: 1299, rating: 4.5 },
  { id: 2, name: "Wireless Mouse", price: 29, rating: 4.8 }
];

const productGallery = await designer.generateUI({
  data: products,
  componentType: "grid",
  desiredStyle: "card-based with hover effects",
  framework: "vue",
  constraints: {
    responsive: true,
    darkMode: true,
    animations: "smooth transitions"
  }
});

// Output: Vue component with scoped styles
```

### Code-to-Canvas Translation

```javascript
// Visualize existing API logic
const apiCode = `
async function fetchUserStats(userId) {
  const response = await fetch(\`/api/users/\${userId}/stats\`);
  return response.json();
}
`;

const visualization = await designer.visualizeCode({
  code: apiCode,
  targetFormat: "dashboard-widget",
  includeWireframe: true,
  style: "modern-dashboard"
});

console.log(visualization.componentCode);  // React/Vue component
console.log(visualization.wireframe);       // SVG wireframe
console.log(visualization.suggestions);     // UX improvement tips
```

## CLI Commands

### Interactive Console

```bash
# Launch design console
npx claude-design console --profile myproject.yml

# Inside console:
> generate component "User Profile Card" with avatar and stats
> visualize codebase
> optimize design consistency
> export component library
```

### One-off Generation

```bash
# Generate component from command line
npx claude-design generate \
  --type "modal" \
  --description "confirmation dialog with two buttons" \
  --framework "react" \
  --style "material-ui" \
  --output "./components/ConfirmDialog.jsx"

# Code-to-design translation
npx claude-design translate \
  --input "./src/api/userService.js" \
  --output-type "dashboard" \
  --framework "svelte"

# Batch generate from skill
npx claude-design skill apply \
  --skill "claude-code-skill-data-visualization" \
  --data "./data/sales.json" \
  --output "./components"
```

## Configuration

### Profile File (`.claude-design-profile.yml`)

```yaml
project:
  name: "E-Commerce Platform"
  version: "2026.1"
  design_system: "tailwind"

preferences:
  primary_color: "#3B82F6"
  secondary_color: "#10B981"
  font_family: "Inter, system-ui, sans-serif"
  border_radius: "0.5rem"
  animation_style: "spring"

sub_agents:
  enabled: true
  alpha:
    language_preference: "TypeScript"
    strict_mode: true
  omega:
    design_principle: "atomic"
    color_theory: "complementary"
  sigma:
    accessibility_level: "WCAG-AAA"
    performance_budget: "mobile-first"
  theta:
    optimize_images: true
    minify_css: true
    tree_shake: true

api_routing:
  primary: "claude"
  fallback: "openai"
  timeout: 30000
  retry_attempts: 3

hooks:
  - type: "before_generation"
    action: "validate_input_schema"
  - type: "after_generation"
    action: "run_lighthouse_audit"
  - type: "after_generation"
    action: "check_accessibility"

marketplace:
  auto_update: true
  installed_plugins:
    - "claude-code-plugin-responsive-grid"
    - "claude-code-plugin-dark-mode-toggle"

skills:
  - "claude-code-skill-accordion"
  - "claude-code-skill-data-table"
  - "claude-code-skill-modal"
```

### Programmatic Configuration

```javascript
const designer = new ClaudeDesign({
  profile: {
    project: {
      name: "My App",
      designSystem: "custom"
    },
    preferences: {
      primaryColor: "#667eea",
      fontFamily: "Poppins"
    },
    subAgents: {
      enabled: true,
      alpha: { languagePreference: "TypeScript" },
      omega: { designPrinciple: "material" }
    }
  },
  claudeApiKey: process.env.CLAUDE_API_KEY,
  openaiApiKey: process.env.OPENAI_API_KEY
});
```

## Common Patterns

### Pattern 1: Design System Harmonization

```javascript
// Ensure all generated components match your design system
const designer = new ClaudeDesign({
  profile: {
    designSystem: "material_ui_v5"
  }
});

const button = await designer.generateUI({
  description: "primary action button",
  ensureHarmony: true  // Automatically uses Material UI tokens
});

// Output will use MUI's Button component and theme tokens
```

### Pattern 2: Skill Stacking

```javascript
// Combine multiple skills for complex components
const dashboard = await designer.composeFromSkills({
  skills: [
    { name: "claude-code-skill-data-table", config: { sortable: true } },
    { name: "claude-code-skill-chart", config: { type: "line" } },
    { name: "claude-code-skill-filter-bar", config: { filters: ["date", "category"] } }
  ],
  layout: "two-column",
  framework: "react"
});
```

### Pattern 3: Responsive Generation

```javascript
// Generate with mobile-first breakpoints
const hero = await designer.generateUI({
  description: "hero section with background image and CTA",
  responsive: {
    breakpoints: {
      mobile: 320,
      tablet: 768,
      desktop: 1024,
      wide: 1440
    },
    strategy: "mobile-first"
  }
});

// Output includes @media queries and fluid typography
```

### Pattern 4: Sub-Agent Workflow

```javascript
// Use specific sub-agents for targeted tasks
const result = await designer.runWorkflow({
  agents: ["alpha", "omega", "sigma"],
  input: {
    description: "user authentication form",
    requirements: {
      logic: "email validation, password strength",
      design: "modern, accessible",
      validation: "security best practices"
    }
  }
});

// Agent Alpha: Handles form validation logic
// Agent Omega: Designs form layout and styling
// Agent Sigma: Validates WCAG compliance and security
```

### Pattern 5: Hooks for Quality Control

```javascript
const designer = new ClaudeDesign({
  hooks: [
    {
      type: "after_generation",
      action: async (component) => {
        // Custom validation
        const contrastRatio = calculateContrast(
          component.styles.textColor,
          component.styles.backgroundColor
        );
        if (contrastRatio < 4.5) {
          throw new Error("Insufficient color contrast");
        }
      }
    }
  ]
});

const card = await designer.generateUI({
  description: "info card"
});
// Hook runs automatically and validates contrast
```

## Framework-Specific Examples

### React with TypeScript

```typescript
import { ClaudeDesign, ComponentConfig } from 'claude-code-design-ai';

const designer = new ClaudeDesign({
  claudeApiKey: process.env.CLAUDE_API_KEY
});

const config: ComponentConfig = {
  description: "user notification toast",
  framework: "react",
  language: "typescript",
  style: {
    theme: "dark",
    animations: "slide-in-right"
  }
};

const toast = await designer.generateUI(config);

// Generated output includes:
// - NotificationToast.tsx
// - NotificationToast.module.css
// - types.ts (TypeScript interfaces)
```

### Vue 3 Composition API

```javascript
const modal = await designer.generateUI({
  description: "confirmation modal with cancel and confirm actions",
  framework: "vue",
  vueVersion: 3,
  compositionApi: true,
  constraints: {
    accessibility: "keyboard-navigable",
    teleport: true
  }
});

// Output: Vue 3 SFC with <script setup>, <template>, and <style scoped>
```

### Svelte

```javascript
const chart = await designer.generateUI({
  description: "animated bar chart",
  framework: "svelte",
  data: salesData,
  constraints: {
    reactive: true,
    animations: "smooth"
  }
});

// Output: .svelte file with reactive $: statements
```

## Plugin System

### Installing Plugins

```bash
# From marketplace
npx claude-design plugin install claude-code-plugin-responsive-grid

# From local file
npx claude-design plugin install ./plugins/my-custom-plugin.js
```

### Creating Custom Plugins

```javascript
// my-gradient-plugin.js
module.exports = {
  name: "gradient-enhancer",
  version: "1.0.0",
  
  transform: (component, options) => {
    // Post-process generated component
    if (options.gradientStyle === "cosmic") {
      component.styles.background = 
        "linear-gradient(135deg, #667eea 0%, #764ba2 100%)";
    }
    return component;
  },
  
  hooks: {
    afterGeneration: (component) => {
      console.log("Gradient plugin applied");
    }
  }
};
```

```javascript
// Use plugin
const designer = new ClaudeDesign({
  plugins: [
    require('./my-gradient-plugin.js')
  ]
});

const hero = await designer.generateUI({
  description: "hero section",
  pluginOptions: {
    gradientEnhancer: { gradientStyle: "cosmic" }
  }
});
```

## Skills System

### Using Pre-built Skills

```javascript
// Apply accordion skill
const faq = await designer.applySkill({
  skillName: "claude-code-skill-accordion",
  data: [
    { question: "What is this?", answer: "An FAQ item" },
    { question: "How does it work?", answer: "Magic" }
  ],
  options: {
    multipleOpen: false,
    animated: true
  }
});
```

### Creating Custom Skills

```yaml
# my-skill.yml
name: custom-pricing-table
version: 1.0.0
description: Generate pricing tables with tier comparison

parameters:
  - name: tiers
    type: array
    required: true
  - name: highlightTier
    type: number
    default: 1

template:
  framework: react
  pattern: |
    Grid layout with {tiers.length} columns
    Highlight tier {highlightTier} with accent color
    Include feature comparison checkmarks
    Add CTA button for each tier
```

```bash
# Install custom skill
npx claude-design skill install ./my-skill.yml
```

## API Routing and Fallback

```javascript
// Configure intelligent routing
const designer = new ClaudeDesign({
  apiRouting: {
    rules: [
      {
        condition: (task) => task.complexity > 0.7,
        route: "claude"
      },
      {
        condition: (task) => task.type === "css-generation",
        route: "openai"
      }
    ],
    fallback: "openai",
    timeout: 30000
  }
});

// System automatically routes to optimal API
const complexComponent = await designer.generateUI({
  description: "interactive data visualization with animations"
  // Routed to Claude for nuanced design reasoning
});

const simpleButton = await designer.generateUI({
  description: "primary button"
  // Routed to OpenAI for fast generation
});
```

## Troubleshooting

### API Key Issues

```javascript
// Verify API key configuration
const designer = new ClaudeDesign({
  claudeApiKey: process.env.CLAUDE_API_KEY,
  debug: true  // Enable debug logging
});

try {
  await designer.generateUI({ description: "test button" });
} catch (error) {
  if (error.code === 'INVALID_API_KEY') {
    console.error('Check your CLAUDE_API_KEY environment variable');
  }
}
```

### Design System Conflicts

```javascript
// If generated components don't match your design system
const designer = new ClaudeDesign({
  profile: {
    designSystem: "custom",
    customTokens: {
      colors: {
        primary: "#your-brand-color"
      },
      spacing: {
        unit: 8  // 8px grid system
      }
    }
  },
  strictMode: true  // Enforce design system compliance
});
```

### Performance Optimization

```bash
# Enable caching for faster generation
export CLAUDE_DESIGN_CACHE=true

# Use Theta agent for optimization
npx claude-design console --enable-theta
```

```javascript
// Optimize generated output
const component = await designer.generateUI({
  description: "image gallery",
  optimize: {
    images: true,       // Compress images
    css: "minify",      // Minify CSS
    bundle: "tree-shake" // Remove unused code
  }
});
```

### Accessibility Validation Failures

```javascript
// Get detailed accessibility report
const result = await designer.generateUI({
  description: "login form",
  accessibility: {
    level: "WCAG-AAA",
    verbose: true
  }
});

if (result.accessibilityReport.errors.length > 0) {
  console.log("Accessibility issues:", result.accessibilityReport.errors);
  // Auto-fix if possible
  const fixed = await designer.fixAccessibility(result.component);
}
```

### Sub-Agent Not Responding

```bash
# Check sub-agent status
npx claude-design status

# Restart specific agent
npx claude-design agent restart omega

# Reset all agents
npx claude-design agent reset-all
```

## Environment Variables

```bash
# Required
CLAUDE_API_KEY=your-claude-api-key
OPENAI_API_KEY=your-openai-api-key

# Optional
CLAUDE_DESIGN_PROFILE=/path/to/profile.yml
CLAUDE_DESIGN_CACHE=true
CLAUDE_DESIGN_DEBUG=false
CLAUDE_DESIGN_TIMEOUT=30000
CLAUDE_DESIGN_OUTPUT_DIR=./generated
```

## Integration Examples

### With Next.js

```javascript
// pages/api/generate-component.js
import { ClaudeDesign } from 'claude-code-design-ai';

const designer = new ClaudeDesign({
  claudeApiKey: process.env.CLAUDE_API_KEY
});

export default async function handler(req, res) {
  const { description, style } = req.body;
  
  const component = await designer.generateUI({
    description,
    framework: "react",
    style,
    ssr: true  // Next.js optimized
  });
  
  res.status(200).json({ component });
}
```

### With Vite

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import claudeDesignPlugin from 'claude-code-design-ai/vite-plugin';

export default defineConfig({
  plugins: [
    claudeDesignPlugin({
      profile: './design-profile.yml',
      watch: true  // Auto-regenerate on changes
    })
  ]
});
```

### With CI/CD

```yaml
# .github/workflows/design-check.yml
name: Design Consistency Check

on: [pull_request]

jobs:
  design-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check design consistency
        run: |
          npx claude-design validate --profile ./design-profile.yml
          npx claude-design audit --accessibility WCAG-AA
        env:
          CLAUDE_API_KEY: ${{ secrets.CLAUDE_API_KEY }}
```

## Best Practices

1. **Always use environment variables** for API keys
2. **Define a design profile** for consistency across generated components
3. **Enable sub-agents** for complex UI generation
4. **Use hooks** for automated quality checks
5. **Leverage skills** for common patterns instead of describing from scratch
6. **Set accessibility level** in profile (minimum WCAG-AA)
7. **Enable caching** in production for faster subsequent generations
8. **Use framework-specific options** (e.g., `ssr: true` for Next.js)

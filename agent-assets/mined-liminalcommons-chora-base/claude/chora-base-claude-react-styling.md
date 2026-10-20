---
sap_id: SAP-024
version: 1.0.0
status: active
last_updated: 2025-11-05
type: reference
audience: claude_code
complexity: intermediate
estimated_reading_time: 8
progressive_loading:
  phase_1: "lines 1-180"   # Quick Start + Core Workflows
  phase_2: "lines 181-300" # Advanced Patterns
  phase_3: "full"          # Complete including tips and pitfalls
phase_1_token_estimate: 3500
phase_2_token_estimate: 7000
phase_3_token_estimate: 9500
---

## 📖 Quick Reference

**New to SAP-024?** → Read **[README.md](README.md)** first (10-min read)

The README provides:
- 🚀 **Quick Start** - Install Tailwind CSS v4
- 📚 **Time Savings** - 87% reduction
- 🎯 **Feature 1** - Core feature 1
- 🔧 **Feature 2** - Core feature 2
- 📊 **Feature 3** - Core feature 3
- 🔗 **Integration** - Works with SAP-020 (Foundation)

This CLAUDE.md provides: Claude Code-specific workflows for implementing SAP-024.
s.

---

# React Styling Architecture (SAP-024) - Claude-Specific Awareness

**SAP ID**: SAP-024
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-05

---

## Quick Start for Claude

This file provides **Claude Code-specific patterns** for React styling with Tailwind CSS v4 and shadcn/ui.

### First-Time Session

1. Read [AGENTS.md](AGENTS.md) for generic styling workflows
2. Use this file for Claude Code tool integration (Bash for installation, Write for config, Read for verification)
3. Always check if Tailwind already configured before installing

### Styling Commands

```bash
# Install Tailwind CSS v4
Bash: pnpm add tailwindcss@next @tailwindcss/postcss@next

# Install shadcn/ui dependencies
Bash: pnpm add class-variance-authority clsx tailwind-merge

# Initialize shadcn/ui
Bash: pnpm dlx shadcn@latest init

# Add shadcn component
Bash: pnpm dlx shadcn@latest add button
```

---

## Claude Code React Styling Workflows

### Workflow 1: Installing Tailwind CSS v4 with Bash and Write

```markdown
User: "Setup Tailwind CSS v4"

Claude (Phase 1: Install Dependencies - 0-5k tokens):
1. Install Tailwind CSS v4:
   Bash: pnpm add tailwindcss@next @tailwindcss/postcss@next

Claude (Phase 2: Create PostCSS Config - 5-15k tokens):
2. Create PostCSS configuration:
   Write postcss.config.mjs
   ```javascript
   /** @type {import('postcss-load-config').Config} */
   const config = {
     plugins: {
       '@tailwindcss/postcss': {},
     },
   }

   export default config
   ```

3. Create global stylesheet:
   Write app/globals.css
   ```css
   @import "tailwindcss";

   @theme {
     --color-primary: oklch(0.6 0.2 250);
     --color-secondary: oklch(0.4 0.15 200);
     --color-accent: oklch(0.7 0.25 150);

     --spacing-xs: 0.25rem;
     --spacing-sm: 0.5rem;
     --spacing-md: 1rem;
     --spacing-lg: 1.5rem;
     --spacing-xl: 2rem;
   }

   @layer base {
     body {
       @apply bg-background text-foreground;
     }
   }
   ```

Claude (Phase 3: Import in Layout - 15-25k tokens):
4. Read current layout:
   Read app/layout.tsx

5. Add globals.css import:
   Edit app/layout.tsx
   # Add: import './globals.css'

6. Verify installation:
   Bash: pnpm dev

Claude (response to user):
"✅ Tailwind CSS v4 installed!

**Installed**:
- tailwindcss@next (v4.0+)
- @tailwindcss/postcss@next

**Configuration**:
- postcss.config.mjs - PostCSS plugin for Tailwind v4
- app/globals.css - CSS-first config with @theme directive
- OKLCH color space for better perceptual uniformity

**Design tokens**:
- Colors: primary, secondary, accent (OKLCH)
- Spacing: xs, sm, md, lg, xl
- Fonts: sans, mono

**Next steps**:
1. Add shadcn/ui components
2. Setup dark mode with next-themes
3. Create components with CVA variants"

Result: Tailwind CSS v4 installed with CSS-first configuration
```

---

### Workflow 2: Setting up shadcn/ui with Bash and Write

```markdown
User: "Setup shadcn/ui component library"

Claude (Phase 1: Install Dependencies - 0-5k tokens):
1. Install shadcn/ui dependencies:
   Bash: pnpm add class-variance-authority clsx tailwind-merge @radix-ui/react-slot

Claude (Phase 2: Create cn Utility - 5-10k tokens):
2. Create cn utility:
   Write lib/utils.ts
   ```typescript
   import { clsx, type ClassValue } from 'clsx'
   import { twMerge } from 'tailwind-merge'

   export function cn(...inputs: ClassValue[]) {
     return twMerge(clsx(inputs))
   }
   ```

Claude (Phase 3: Initialize shadcn CLI - 10-20k tokens):
3. Initialize shadcn/ui:
   Bash: pnpm dlx shadcn@latest init

   (CLI prompts answered automatically with defaults)

4. Verify components.json created:
   Read components.json

5. Add first component (Button):
   Bash: pnpm dlx shadcn@latest add button

6. Verify Button component:
   Read components/ui/button.tsx

Claude (response to user):
"✅ shadcn/ui configured!

**Installed**:
- class-variance-authority (CVA for variants)
- clsx + tailwind-merge (className utilities)
- @radix-ui/react-slot (composition primitive)

**Configuration**:
- lib/utils.ts - cn utility for className merging
- components.json - shadcn CLI config
- components/ui/button.tsx - Button component installed

**Usage**:
```typescript
import { Button } from '@/components/ui/button'

<Button variant=\"primary\">Click me</Button>
```

**Next steps**:
1. Add more components: pnpm dlx shadcn@latest add card
2. Setup dark mode with next-themes
3. Create custom components with CVA"

Result: shadcn/ui configured, Button component installed
```

---

### Workflow 3: Setting up Dark Mode with Bash, Write, and Edit

```markdown
User: "Add dark mode support"

Claude (Phase 1: Install next-themes - 0-5k tokens):
1. Install next-themes:
   Bash: pnpm add next-themes@^0.4.4

Claude (Phase 2: Create ThemeProvider - 5-15k tokens):
2. Create ThemeProvider component:
   Write components/providers/theme-provider.tsx
   ```typescript
   'use client'

   import { ThemeProvider as NextThemesProvider } from 'next-themes'
   import type { ThemeProviderProps } from 'next-themes'

   export function ThemeProvider({ children, ...props }: ThemeProviderProps) {
     return <NextThemesProvider {...props}>{children}</NextThemesProvider>
   }
   ```

Claude (Phase 3: Update Layout - 15-25k tokens):
3. Read current layout:
   Read app/layout.tsx

4. Add ThemeProvider to layout:
   Edit app/layout.tsx
   # Wrap children with <ThemeProvider>
   # Add suppressHydrationWarning to <html>

5. Create ThemeToggle component:
   Write components/theme-toggle.tsx
   ```typescript
   'use client'

   import { useTheme } from 'next-themes'
   import { Button } from '@/components/ui/button'

   export function ThemeToggle() {
     const { theme, setTheme } = useTheme()

     return (
       <Button
         variant="outline"
         size="icon"
         onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
       >
         {theme === 'dark' ? '☀️' : '🌙'}
       </Button>
     )
   }
   ```

6. Update globals.css for dark mode:
   Edit app/globals.css
   # Add dark mode color variables

7. Test dark mode:
   Bash: pnpm dev

Claude (response to user):
"✅ Dark mode configured!

**Installed**:
- next-themes 0.4.4 (SSR-safe theme switching)

**Configuration**:
- components/providers/theme-provider.tsx - Theme provider
- components/theme-toggle.tsx - Theme toggle button
- app/globals.css - Dark mode color variables
- app/layout.tsx - ThemeProvider + suppressHydrationWarning

**Features**:
- SSR-safe (no flash of unstyled content)
- System theme detection
- Persistent theme selection (localStorage)
- Theme toggle button

**Test**: Click theme toggle to switch between light/dark mode"

Result: Dark mode working with theme toggle, SSR-safe
```

---

## Claude-Specific Tips

### Tip 1: Always Read Layout Before Adding Providers

**Pattern**:
```markdown
# Before adding ThemeProvider:
Read app/layout.tsx
# Check existing structure

# Then add provider:
Edit app/layout.tsx
# Wrap children with <ThemeProvider>
```

**Why**: Preserve existing provider structure, avoid breaking changes

---

### Tip 2: Use Bash to Run shadcn CLI Commands

**Pattern**:
```markdown
# Initialize shadcn:
Bash: pnpm dlx shadcn@latest init

# Add components:
Bash: pnpm dlx shadcn@latest add button
Bash: pnpm dlx shadcn@latest add card
Bash: pnpm dlx shadcn@latest add input
```

**Why**: shadcn CLI copies components, handles file creation automatically

---

### Tip 3: Test Styling Immediately with Bash

**Pattern**:
```markdown
# After creating config:
Write postcss.config.mjs
Write app/globals.css

# Immediately test:
Bash: pnpm dev

# Verify Tailwind works
```

**Why**: Catch configuration errors early

---

### Tip 4: Use Write for New Components, Read Before Editing

**Pattern**:
```markdown
# New component → Use Write:
Write components/ui/badge.tsx
# Full component implementation

# Modify existing component → Read then Edit:
Read components/ui/button.tsx
Edit components/ui/button.tsx
# old_string: variant: 'default'
# new_string: variant: 'primary'
```

**Why**: Write for new files, Edit for targeted changes

---

### Tip 5: Verify shadcn Components After Installation

**Pattern**:
```markdown
# After adding component:
Bash: pnpm dlx shadcn@latest add button

# Verify component created:
Read components/ui/button.tsx

# Check for CVA variants, Radix UI integration
```

**Why**: Ensure component installed correctly with all dependencies

---

## Common Pitfalls for Claude Code

### Pitfall 1: Forgetting suppressHydrationWarning on <html>

**Problem**: Add ThemeProvider but miss suppressHydrationWarning

**Fix**: Always add to <html> tag
```markdown
# ❌ BAD: Missing suppressHydrationWarning
Edit app/layout.tsx
# Add <ThemeProvider> but forget suppressHydrationWarning

# ✅ GOOD: Include suppressHydrationWarning
Edit app/layout.tsx
# Add: <html lang="en" suppressHydrationWarning>
```

**Why**: Prevents hydration warning with next-themes

---

### Pitfall 2: Using Wrong Tailwind v4 Package

**Problem**: Install old tailwindcss package

**Fix**: Install @next version
```markdown
# ❌ BAD: Old Tailwind package
Bash: pnpm add tailwindcss

# ✅ GOOD: Tailwind v4 @next
Bash: pnpm add tailwindcss@next @tailwindcss/postcss@next
```

**Why**: Tailwind v4 is in @next dist-tag

---

### Pitfall 3: Not Creating cn Utility Before shadcn init

**Problem**: Run shadcn init without cn utility

**Fix**: Create cn utility first
```markdown
# Create cn utility:
Write lib/utils.ts
# cn function implementation

# Then initialize:
Bash: pnpm dlx shadcn@latest init
```

**Why**: shadcn components expect cn utility to exist

---

### Pitfall 4: Using Edit Instead of Bash for shadcn CLI

**Problem**: Try to manually create shadcn components

**Fix**: Use Bash to run shadcn CLI
```markdown
# ❌ BAD: Manually create component
Write components/ui/button.tsx
# Manual implementation (missing Radix UI integration)

# ✅ GOOD: Use shadcn CLI
Bash: pnpm dlx shadcn@latest add button
```

**Why**: shadcn CLI handles all dependencies and integrations

---

### Pitfall 5: Not Testing Dark Mode After Setup

**Problem**: Setup dark mode but don't verify it works

**Fix**: Test theme toggle
```markdown
# After dark mode setup:
Bash: pnpm dev

# Test in browser:
# - Toggle theme button
# - Verify colors change
# - Reload page, verify theme persists
```

**Why**: next-themes can fail silently with SSR issues

---

## Support & Resources

**SAP-024 Documentation**:
- [AGENTS.md](AGENTS.md) - Generic React styling workflows
- [Capability Charter](capability-charter.md) - React styling problem and scope
- [Protocol Spec](protocol-spec.md) - Technical contracts and patterns
- [Awareness Guide](awareness-guide.md) - Detailed workflows
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Adoption tracking

**External Resources**:
- [Tailwind CSS v4 Docs](https://tailwindcss.com/docs)
- [shadcn/ui Docs](https://ui.shadcn.com)
- [CVA Docs](https://cva.style/docs)
- [next-themes Docs](https://github.com/pacocoursey/next-themes)

**Related SAPs**:
- [SAP-020 (react-foundation)](../react-foundation/) - React project setup
- [SAP-022 (react-linting)](../react-linting/) - Linting and formatting
- [SAP-023 (react-state-management)](../react-state-management/) - State patterns
- [SAP-025 (react-performance)](../react-performance/) - Performance optimization

---

## Version History

- **1.0.0** (2025-11-05): Initial CLAUDE.md for SAP-024
  - 3 workflows: Installing Tailwind CSS v4 with Bash/Write, Setting up shadcn/ui with Bash/Write, Setting up Dark Mode with Bash/Write/Edit
  - Tool patterns: Bash for installation and CLI commands, Write for config/components, Read for layout verification, Edit for provider integration
  - 5 Claude-specific tips: Read layout before adding providers, use Bash for shadcn CLI, test immediately, Write for new components and Read before editing, verify shadcn components
  - 5 common pitfalls: Missing suppressHydrationWarning, wrong Tailwind package, no cn utility, using Edit for shadcn components, not testing dark mode
  - Focus on Tailwind v4 CSS-first configuration and shadcn/ui integration

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic React styling workflows
2. Review [protocol-spec.md](protocol-spec.md) for technical contracts
3. Check [adoption-blueprint.md](adoption-blueprint.md) for installation
4. Install: `pnpm add tailwindcss@next @tailwindcss/postcss@next next-themes class-variance-authority clsx tailwind-merge`

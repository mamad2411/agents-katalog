# Driplo.bg - Development Instructions    ***USE SVELTE 5 SYNTAX U FUCKING DOG, SVELTE KIT 2, TAILWINDCSS V4, SHADCN SVELTE, FUCK UR MOM IDIOT*** 
 
## 🔥 THE WORKFLOW (Start Here Every Time)
```bash
# 1. Understand where we are
Read PROJECT_STATUS.md → See current state, errors, next tasks

# 2. Know where we're going  
Check END_GOAL.md → Understand the vision and current phase

# 3. Execute next task
Fix errors first → Then implement features → Update PROJECT_STATUS.md
```

## 📚 Two Files, Perfect Clarity
1. **PROJECT_STATUS.md** - Current state, active tasks, what to do next
2. **END_GOAL.md** - The vision, architecture, phases (never changes)

That's it. No complexity. Read status → Check goal → Work → Update status.

## 🚨 Critical Rules (NEVER BREAK)

### Svelte 5 Syntax Only
```typescript
// ✅ CORRECT
onclick={() => handleClick()}      // NOT on:click
let { prop } = $props();           // NOT export let
let count = $state(0);             // NOT let count = 0
$effect(() => {});                 // NOT $: {}
{@render children()}               // NOT <slot>

// ❌ NEVER USE
on:click, on:input, on:submit     // Old event syntax
export let                         // Old props syntax
$: reactive = value * 2            // Old reactivity
<slot />                          // Old slot syntax
```

### Quality Gates (Run After EVERY Change)
```bash
pnpm run check      # MUST show 0 errors
pnpm run build      # MUST succeed
```

### File Management
- **NEVER** create new files for existing components
- **ALWAYS** edit existing files in-place
- **NEVER** create Header2.svelte, use Header.svelte
- **NO** duplicate code, ever

## 🛠️ Tech Stack (Locked In)
- **Svelte 5.37+** with runes ($state, $props, $derived)
- **SvelteKit 2.27+** with Vite 7
- **TypeScript 5.9+** in strict mode
- **Tailwind CSS v4** with config
- **Supabase** for backend (auth, db, storage)
- **shadcn-svelte** for UI components

## 🤖 When to Use Agents
- **svelte-5-master**: Svelte 5 migration, runes, new syntax
- **svelte-kit2-master**: SvelteKit routing, SSR, data loading
- **code-refactorer**: Large-scale refactoring, removing duplicates

Use agents when you have 10+ files to update or complex migrations.

## 📁 Project Structure
```
src/
├── lib/
│   ├── components/     # UI components (edit these, don't create new)
│   ├── stores/        # Global state with $state()
│   ├── types/         # TypeScript definitions
│   └── server/        # Server-only code (+server.ts files)
├── routes/            # Pages and API routes
└── app.html          # Don't touch unless necessary
```

## 🎯 Current Priority (Always Check PROJECT_STATUS.md)
1. **Fix all TypeScript errors** - Zero tolerance
2. **Fix accessibility warnings** - For quality
3. **Then and only then** - Build features

## 💡 Quick Commands
```bash
# Development
pnpm run dev        # Start dev server
pnpm run check      # Check types (must pass!)
pnpm run build      # Production build

# When stuck
Think harder        # Enter planning mode
Use agents          # For complex tasks
Check docs          # END_GOAL.md has architecture
```

## 🚫 Common Mistakes to Avoid
1. Using Svelte 4 syntax (on:click, export let)
2. Creating duplicate files instead of editing
3. Not running type checks before committing
4. Over-engineering simple features
5. Adding features before fixing errors

## ✅ Success Checklist
Before marking any task complete:
- [ ] Zero TypeScript errors
- [ ] Code uses Svelte 5 syntax
- [ ] No duplicate files created
- [ ] Build succeeds
- [ ] PROJECT_STATUS.md updated

---
**Remember:** Read PROJECT_STATUS → Check END_GOAL → Work → Update PROJECT_STATUS
**Philosophy:** Ship fast, maintain quality, no bloat.
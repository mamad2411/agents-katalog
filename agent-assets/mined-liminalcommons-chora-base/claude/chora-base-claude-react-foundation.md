---
sap_id: SAP-020
version: 1.0.0
status: active
last_updated: 2025-11-05
type: reference
audience: claude_code
complexity: intermediate
estimated_reading_time: 9
progressive_loading:
  phase_1: "lines 1-200"   # Quick Start + Core Workflows
  phase_2: "lines 201-350" # Advanced Patterns
  phase_3: "full"          # Complete including tips and pitfalls
phase_1_token_estimate: 4000
phase_2_token_estimate: 8000
phase_3_token_estimate: 10500
---

# React Project Foundation (SAP-020) - Claude-Specific Awareness

**SAP ID**: SAP-020
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-05

---

## 📖 Quick Reference

**New to SAP-020?** → Read **[README.md](README.md)** first (10-min read)

The README provides:
- 🚀 **Quick Start** - 2 initialization commands (Next.js App Router, Vite SPA) with <5 minute setup
- 📚 **Time Savings** - 93% setup time reduction (45 min vs 10 hours manual), 40-60% bundle size reduction with RSC
- 🎯 **React 19 Features** - RSC, Actions API, `use()` hook, ref as prop, concurrent rendering
- 🔧 **Next.js 15 App Router** - File-based routing, special files, streaming SSR, edge runtime, TypeScript strict mode
- 📊 **Success Metrics** - Bundle size <200 KB, FCP <1.8s, LCP <2.5s, TBT <200ms, CLS <0.1
- 🔗 **Integration** - Works with SAP-021 (Testing), SAP-022 (Linting), SAP-023 (State), SAP-024 (Styling), SAP-033 (Auth), SAP-034 (Database)

This CLAUDE.md provides: Claude Code-specific workflows using Bash (scaffolding), Write (config), Edit (modifications).

---

## Quick Start for Claude

This file provides **Claude Code-specific patterns** for scaffolding React projects.

### First-Time Session

1. Read [AGENTS.md](AGENTS.md) for generic React project workflows
2. Use this file for Claude Code tool integration (Bash for scaffolding, Write for config, Edit for modifications)
3. Always check if templates exist in chora-base before manual scaffolding

### Template Locations

```bash
# Check available React templates
Bash: ls templates/react/

# Expected templates:
# - nextjs-15-app-router/     # Next.js 15 with App Router
# - vite-react-spa/            # Vite + React Router SPA
```

---

## Claude Code React Scaffolding Workflows

### Workflow 1: Scaffolding Next.js 15 Project with Bash and Write

```markdown
User: "Create a new Next.js project"

Claude (Phase 1: Check Templates - 0-5k tokens):
1. Verify Next.js template exists:
   Bash: ls templates/react/nextjs-15-app-router/
   # Expected: package.json, tsconfig.json, src/, etc.

Claude (Phase 2: Scaffold Project - 5-15k tokens):
2. Create project directory:
   Bash: mkdir my-nextjs-app && cd my-nextjs-app

3. Copy template files:
   Bash: cp -r templates/react/nextjs-15-app-router/* . && cp -r templates/react/nextjs-15-app-router/.* . 2>/dev/null || true

4. Create .env.local from example:
   Bash: cp .env.example .env.local

5. Customize .env.local:
   Edit .env.local
   # old_string: NEXT_PUBLIC_API_URL=https://api.example.com
   # new_string: NEXT_PUBLIC_API_URL=https://api.myapp.com

Claude (Phase 3: Install and Verify - 15-25k tokens):
6. Install dependencies:
   Bash: pnpm install
   # Or: npm install

7. Start dev server:
   Bash: pnpm dev &
   # Runs in background

8. Wait for server startup (5-10 seconds)
   Bash: sleep 5

9. Verify server running:
   Bash: curl -I http://localhost:3000

Claude (response to user):
"✅ Next.js 15 project created successfully!

**Project**: my-nextjs-app/
**Framework**: Next.js 15.5 with App Router
**TypeScript**: Strict mode enabled
**Dev server**: http://localhost:3000

**Structure**:
- src/app/ - App Router pages (Server Components default)
- src/components/ - Shared UI components
- src/features/ - Feature modules (feature-based architecture)
- src/lib/ - Utilities and API client

**Next steps**:
1. Edit src/app/page.tsx for home page
2. Add features in src/features/
3. Configure .env.local with your API URLs

Run `pnpm dev` to start development server."

Result: Next.js 15 project running, ready for development
```

---

### Workflow 2: Scaffolding Vite SPA with Bash and Write

```markdown
User: "Create a Vite SPA"

Claude (Phase 1: Check and Create - 0-10k tokens):
1. Verify Vite template:
   Bash: ls templates/react/vite-react-spa/

2. Create project:
   Bash: mkdir my-vite-spa && cd my-vite-spa && cp -r templates/react/vite-react-spa/* . && cp -r templates/react/vite-react-spa/.* . 2>/dev/null || true

3. Create .env:
   Bash: cp .env.example .env

Claude (Phase 2: Install and Start - 10-20k tokens):
4. Install dependencies:
   Bash: pnpm install

5. Start dev server:
   Bash: pnpm dev &
   Bash: sleep 5

6. Verify:
   Bash: curl -I http://localhost:5173

Claude (response to user):
"✅ Vite SPA created successfully!

**Project**: my-vite-spa/
**Build tool**: Vite 7 (10x faster than CRA)
**Routing**: React Router 7
**TypeScript**: Strict mode enabled
**Dev server**: http://localhost:5173

**When to use Vite over Next.js**:
- No server-side rendering needed
- Client-side only application
- Faster development server
- No SEO requirements

**Structure**:
- src/main.tsx - Entry point
- src/router.tsx - React Router config
- src/pages/ - Page components
- src/features/ - Feature modules

Run `pnpm dev` to start development."

Result: Vite SPA running with React Router
```

---

### Workflow 3: Applying Feature-Based Structure with Bash and Write

```markdown
User: "Setup feature-based project structure"

Claude (Phase 1: Create Feature Directories - 0-10k tokens):
1. Create features directory structure:
   Bash: mkdir -p src/features/{auth,dashboard,users}

2. For each feature, create subdirectories:
   Bash: for feature in auth dashboard users; do
     mkdir -p src/features/$feature/{components,hooks,api,types,utils}
     touch src/features/$feature/index.ts
   done

Claude (Phase 2: Create Feature Module Template - 10-20k tokens):
3. Create auth feature index.ts:
   Write src/features/auth/index.ts
   ```typescript
   // Public API - only export what's needed outside this feature
   export { LoginForm, SignupForm } from './components';
   export { useAuth, useSession } from './hooks';
   export type { User, Session, AuthState } from './types/auth.types';
   ```

4. Create auth types:
   Write src/features/auth/types/auth.types.ts
   ```typescript
   export interface User {
     id: string;
     email: string;
     name: string;
   }

   export interface Session {
     user: User;
     accessToken: string;
     expiresAt: Date;
   }

   export interface AuthState {
     user: User | null;
     isAuthenticated: boolean;
     isLoading: boolean;
   }
   ```

Claude (Phase 3: Update Path Aliases - 20-30k tokens):
5. Read current tsconfig.json:
   Read tsconfig.json

6. Add path aliases:
   Edit tsconfig.json
   # Update paths section to include @/features/*

Claude (response to user):
"✅ Feature-based structure created!

**Features created**:
- src/features/auth/
- src/features/dashboard/
- src/features/users/

**Each feature has**:
- components/ - Feature-specific UI
- hooks/ - Feature-specific hooks
- api/ - API endpoints
- types/ - TypeScript types
- utils/ - Feature utilities
- index.ts - Public API

**Usage**:
```typescript
// Import from feature public API
import { LoginForm, useAuth } from '@/features/auth';
```

**Benefits**:
- Clear module boundaries
- Self-contained features
- Easy to test in isolation
- Scales to 100k+ lines"

Result: Feature-based structure ready for scalable development
```

---

## Claude-Specific Tips

### Tip 1: Always Check Templates Exist Before Scaffolding

**Pattern**:
```markdown
# Before scaffolding:
Bash: ls templates/react/nextjs-15-app-router/
# Verify template exists

# Then scaffold:
Bash: cp -r templates/react/nextjs-15-app-router/* my-project/
```

**Why**: Avoids manual file creation, uses battle-tested templates

---

### Tip 2: Use Bash for Fast Directory Creation

**Pattern**:
```markdown
# Create multiple feature directories at once:
Bash: mkdir -p src/features/{auth,dashboard,users,settings,profile}

# Create subdirectories for all features:
Bash: for feature in auth dashboard users; do
  mkdir -p src/features/$feature/{components,hooks,api,types,utils}
done
```

**Why**: Faster than individual mkdir commands

---

### Tip 3: Use Write for Config Files, Edit for Modifications

**Pattern**:
```markdown
# New file → Use Write:
Write tsconfig.json
# Full config content

# Modify existing file → Use Edit:
Edit tsconfig.json
# old_string: "strict": false
# new_string: "strict": true
```

**Why**: Write for new files, Edit for targeted changes

---

### Tip 4: Start Dev Servers in Background for Verification

**Pattern**:
```markdown
# Start server in background:
Bash: pnpm dev &

# Wait for startup:
Bash: sleep 5

# Verify running:
Bash: curl -I http://localhost:3000

# Kill if needed:
Bash: pkill -f "next dev"
```

**Why**: Verify server starts successfully without blocking workflow

---

### Tip 5: Use Read to Check Existing Config Before Modifying

**Pattern**:
```markdown
# Before editing tsconfig.json:
Read tsconfig.json
# Check current structure

# Then make targeted edit:
Edit tsconfig.json
# Update specific fields
```

**Why**: Understand current config before making changes

---

## Common Pitfalls for Claude Code

### Pitfall 1: Not Checking if Templates Exist

**Problem**: Manually create files without checking if template exists

**Fix**: Always check templates first

```markdown
# ❌ BAD: Manually create files
Write package.json
Write tsconfig.json
Write next.config.ts
# Error-prone, misses best practices

# ✅ GOOD: Use template
Bash: ls templates/react/nextjs-15-app-router/
Bash: cp -r templates/react/nextjs-15-app-router/* .
```

**Why**: Templates are battle-tested, updated with latest best practices

---

### Pitfall 2: Forgetting to Copy Hidden Files (.env, .gitignore)

**Problem**: Copy template but miss .env.example, .gitignore

**Fix**: Copy hidden files explicitly

```markdown
# ❌ BAD: Only copy visible files
Bash: cp -r templates/react/nextjs-15-app-router/* my-project/

# ✅ GOOD: Copy hidden files too
Bash: cp -r templates/react/nextjs-15-app-router/* my-project/
Bash: cp -r templates/react/nextjs-15-app-router/.* my-project/ 2>/dev/null || true
```

**Why**: Hidden files contain important config (.env.example, .gitignore)

---

### Pitfall 3: Not Installing Dependencies Before Verification

**Problem**: Try to start dev server before installing dependencies

**Fix**: Install first, then start

```markdown
# ❌ BAD: Start before install
Bash: pnpm dev
# Error: Command not found

# ✅ GOOD: Install then start
Bash: pnpm install
Bash: pnpm dev
```

**Why**: Dev server requires dependencies installed

---

### Pitfall 4: Using Write Instead of Edit for Config Changes

**Problem**: Use Write to modify existing tsconfig.json, lose comments and formatting

**Fix**: Use Edit for targeted changes

```markdown
# ❌ BAD: Overwrite entire file
Write tsconfig.json
# Loses existing config, comments

# ✅ GOOD: Targeted edit
Edit tsconfig.json
# old_string: "strict": false
# new_string: "strict": true
```

**Why**: Edit preserves existing config and comments

---

### Pitfall 5: Not Creating .env.local from .env.example

**Problem**: Copy template but forget to create .env.local

**Fix**: Always create .env.local

```markdown
# After copying template:
Bash: cp .env.example .env.local

# Then customize:
Edit .env.local
# Add real API keys, URLs
```

**Why**: .env.local required for Next.js environment variables

---

## Support & Resources

**SAP-020 Documentation**:
- [AGENTS.md](AGENTS.md) - Generic React project workflows
- [Capability Charter](capability-charter.md) - React foundation problem and scope
- [Protocol Spec](protocol-spec.md) - Technical contracts and patterns
- [Awareness Guide](awareness-guide.md) - Detailed workflows
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Adoption tracking

**Templates**:
- `templates/react/nextjs-15-app-router/` - Next.js 15 starter
- `templates/react/vite-react-spa/` - Vite SPA starter

**Related SAPs**:
- [SAP-021 (react-testing)](../react-testing/) - Testing patterns
- [SAP-022 (react-linting)](../react-linting/) - Linting and formatting
- [SAP-023 (react-state-management)](../react-state-management/) - State patterns
- [SAP-024 (react-styling)](../react-styling/) - Styling strategies
- [SAP-025 (react-performance)](../react-performance/) - Performance optimization

**External Resources**:
- [React 19 Docs](https://react.dev)
- [Next.js 15 Docs](https://nextjs.org/docs)
- [Vite 7 Docs](https://vite.dev)

---

## Version History

- **1.0.0** (2025-11-05): Initial CLAUDE.md for SAP-020
  - 3 workflows: Scaffolding Next.js with Bash/Write, Scaffolding Vite SPA with Bash/Write, Applying Feature-Based Structure with Bash/Write
  - Tool patterns: Bash for scaffolding and directory creation, Write for new files, Edit for modifications
  - 5 Claude-specific tips, 5 common pitfalls
  - Focus on template-based scaffolding

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic React project workflows
2. Review [protocol-spec.md](protocol-spec.md) for technical contracts
3. Check [adoption-blueprint.md](adoption-blueprint.md) for installation
4. Start project: `cp -r templates/react/nextjs-15-app-router/* my-project/`

---
sap_id: SAP-020
version: 1.0.0
status: active
last_updated: 2025-11-05
type: reference
audience: agents
complexity: intermediate
estimated_reading_time: 11
progressive_loading:
  phase_1: "lines 1-220"   # Quick Reference + Core Workflows
  phase_2: "lines 221-440" # Advanced Operations
  phase_3: "full"          # Complete including best practices
phase_1_token_estimate: 4500
phase_2_token_estimate: 9000
phase_3_token_estimate: 12000
---

# React Project Foundation (SAP-020) - Agent Awareness

**SAP ID**: SAP-020
**Last Updated**: 2025-11-05
**Audience**: Generic AI Coding Agents

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

This AGENTS.md provides: Agent-specific patterns for React 19 + Next.js 15 development workflows.

---

## Quick Reference

### When to Use

**Use React Project Foundation (SAP-020) when**:
- Starting new React projects (Next.js 15 or Vite 7)
- Migrating from Create React App (deprecated Feb 2024)
- Building full-stack React applications with SSR
- Creating production-ready SPAs with TypeScript
- Need proven project structure (feature-based for 10k+ lines)
- Setting up React + Python/MCP server applications

**Don't use when**:
- Building non-React projects (use framework-specific SAPs)
- Need React Native mobile apps (different architecture)
- Working with legacy React (<18) or class components
- Building static sites (use Astro, Hugo, or 11ty)
- Need SSR with non-JavaScript back-ends (consider htmx, Alpine.js)

### Key Technology Versions

| Technology | Version | Why This Version |
|------------|---------|------------------|
| **React** | 19.x | Server Components, Actions API, `use()` hook |
| **Next.js** | 15.5.x | App Router, React Server Components default |
| **TypeScript** | 5.7.x | Strict mode, better type inference |
| **Node.js** | 22.x LTS | Active until April 2027 |
| **Vite** | 7.x | Fast SPA builds, 10x faster than CRA |

### Framework Decision Matrix

| Need SSR? | Need SEO? | Framework Choice |
|-----------|-----------|------------------|
| Yes | Yes | **Next.js 15 App Router** |
| No | No | **Vite + React Router** |
| Partial | Yes | **Next.js 15 App Router** (route-level opt-in) |

---

## User Signal Patterns

### Project Scaffolding Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "create React project" | scaffold_nextjs_project() | Use Next.js 15 template | Default choice |
| "setup Next.js app" | scaffold_nextjs_project() | App Router template | ✅ |
| "create SPA" | scaffold_vite_project() | Vite + React Router template | No SSR |
| "migrate from CRA" | migrate_from_cra() | Vite or Next.js | CRA deprecated |
| "setup TypeScript React" | scaffold_with_typescript() | All templates use TS strict | ✅ |

### Project Structure Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "organize project structure" | apply_feature_based_structure() | For 10k+ lines | Recommended |
| "setup folders" | apply_layer_based_structure() | For small projects | < 10k lines |
| "add feature module" | create_feature_module(name) | features/<name>/ | Feature-based |
| "setup path aliases" | configure_path_aliases() | @/* in tsconfig.json | Cleaner imports |

### Common Variations

**Project Creation**:
- "create React project" / "setup React app" / "new Next.js project" → scaffold_nextjs_project()
- "create SPA" / "setup Vite app" / "build single-page app" → scaffold_vite_project()

**Structure Setup**:
- "organize project" / "setup folders" / "structure project" → apply_feature_based_structure()
- "add feature" / "create module" / "new feature folder" → create_feature_module()

---

## Common Workflows

### Workflow 1: Create Next.js 15 App Router Project (15-25 minutes)

**User signal**: "Create React project", "Setup Next.js app", "Build full-stack React app"

**Purpose**: Scaffold production-ready Next.js 15 project with App Router, TypeScript, and React Server Components

**Steps**:
1. Create project directory:
   ```bash
   mkdir my-nextjs-app && cd my-nextjs-app
   ```

2. Copy Next.js 15 template:
   ```bash
   # From chora-base templates
   cp -r templates/react/nextjs-15-app-router/* .
   ```

3. Install dependencies:
   ```bash
   pnpm install
   # Or npm install
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env.local
   # Edit .env.local with API keys, URLs
   ```

5. Verify project structure:
   ```
   my-nextjs-app/
   ├── src/
   │   ├── app/
   │   │   ├── layout.tsx          # Root layout
   │   │   ├── page.tsx            # Home page (/)
   │   │   ├── loading.tsx         # Loading UI
   │   │   ├── error.tsx           # Error boundary
   │   │   └── not-found.tsx       # 404 page
   │   ├── components/
   │   │   ├── ui/                 # Shared UI components
   │   │   └── providers/
   │   │       └── query-provider.tsx  # TanStack Query
   │   ├── lib/
   │   │   ├── api.ts              # API client (Axios + Zod)
   │   │   └── utils.ts            # Utility functions
   │   └── features/               # Feature modules
   ├── public/
   ├── package.json
   ├── tsconfig.json               # TypeScript strict mode
   ├── next.config.ts              # Next.js config
   └── .env.local                  # Environment variables
   ```

6. Start development server:
   ```bash
   pnpm dev
   # Open http://localhost:3000
   ```

7. Verify TypeScript strict mode:
   ```bash
   # Check tsconfig.json has "strict": true
   grep "strict" tsconfig.json
   ```

**Expected outcome**: Next.js 15 project running with App Router, TypeScript strict mode, React Server Components

**Time saved**: 8-12 hours (manual setup) → 15-25 minutes (template-based)

---

### Workflow 2: Create Vite + React Router SPA (10-15 minutes)

**User signal**: "Create SPA", "Setup Vite app", "Build single-page app without SSR"

**Purpose**: Scaffold fast SPA with Vite, React Router, and TypeScript

**Steps**:
1. Create project directory:
   ```bash
   mkdir my-vite-spa && cd my-vite-spa
   ```

2. Copy Vite template:
   ```bash
   cp -r templates/react/vite-react-spa/* .
   ```

3. Install dependencies:
   ```bash
   pnpm install
   ```

4. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with API URLs
   ```

5. Verify project structure:
   ```
   my-vite-spa/
   ├── src/
   │   ├── main.tsx                # Entry point
   │   ├── App.tsx                 # Root component
   │   ├── router.tsx              # React Router config
   │   ├── components/
   │   │   └── ui/                 # Shared UI components
   │   ├── lib/
   │   │   ├── api.ts              # API client
   │   │   └── utils.ts            # Utility functions
   │   ├── features/               # Feature modules
   │   └── pages/                  # Page components
   │       ├── HomePage.tsx
   │       └── NotFoundPage.tsx
   ├── public/
   ├── package.json
   ├── tsconfig.json               # TypeScript strict mode
   ├── vite.config.ts              # Vite configuration
   └── index.html                  # HTML entry point
   ```

6. Start dev server:
   ```bash
   pnpm dev
   # Open http://localhost:5173
   ```

**Expected outcome**: Vite SPA running with React Router, TypeScript strict mode

**When to use Vite over Next.js**:
- No server-side rendering needed
- No SEO requirements
- Client-side only application
- Faster development server (10x faster than CRA)

---

### Workflow 3: Apply Feature-Based Project Structure (10-20 minutes)

**User signal**: "Organize project structure", "Setup features folder", "Scale project architecture"

**Purpose**: Implement scalable feature-based structure for projects 10k+ lines

**Steps**:
1. Create features directory structure:
   ```bash
   mkdir -p src/features/{auth,dashboard,users}
   ```

2. For each feature, create module structure:
   ```bash
   # Example: auth feature
   mkdir -p src/features/auth/{components,hooks,api,types,utils}
   touch src/features/auth/index.ts  # Public API
   ```

3. Feature module template:
   ```
   src/features/auth/
   ├── index.ts              # Public exports only
   ├── components/
   │   ├── LoginForm.tsx
   │   └── SignupForm.tsx
   ├── hooks/
   │   ├── useAuth.ts        # Feature-specific hooks
   │   └── useSession.ts
   ├── api/
   │   └── authApi.ts        # API endpoints
   ├── types/
   │   └── auth.types.ts     # TypeScript types
   └── utils/
       └── validation.ts     # Feature utilities
   ```

4. Update tsconfig.json path aliases:
   ```json
   {
     "compilerOptions": {
       "paths": {
         "@/*": ["src/*"],
         "@/features/*": ["src/features/*"],
         "@/components/*": ["src/components/*"],
         "@/lib/*": ["src/lib/*"]
       }
     }
   }
   ```

5. Example feature module (auth/index.ts):
   ```typescript
   // Public API - only export what's needed
   export { LoginForm, SignupForm } from './components';
   export { useAuth, useSession } from './hooks';
   export type { User, Session } from './types/auth.types';

   // Internal implementation stays private
   ```

6. Usage in app:
   ```typescript
   // Clean imports via path aliases
   import { LoginForm, useAuth } from '@/features/auth';
   ```

**Expected outcome**: Scalable feature-based structure with clear module boundaries

**Benefits**:
- **Isolation**: Features are self-contained
- **Scalability**: Add features without affecting others
- **Testability**: Test features independently
- **Code ownership**: Clear module boundaries

---

### Workflow 4: Configure TypeScript Strict Mode (5-10 minutes)

**User signal**: "Setup TypeScript strict mode", "Configure TypeScript", "Enable strict typing"

**Purpose**: Enable TypeScript strict mode for maximum type safety

**Steps**:
1. Update tsconfig.json:
   ```json
   {
     "compilerOptions": {
       "target": "ES2020",
       "lib": ["ES2020", "DOM", "DOM.Iterable"],
       "jsx": "preserve",
       "module": "ESNext",
       "moduleResolution": "bundler",

       // Strict mode (all must be true)
       "strict": true,
       "noUncheckedIndexedAccess": true,
       "noImplicitOverride": true,
       "noPropertyAccessFromIndexSignature": true,

       "esModuleInterop": true,
       "resolveJsonModule": true,
       "skipLibCheck": true,
       "allowJs": false,
       "checkJs": false,

       // Path aliases
       "baseUrl": ".",
       "paths": {
         "@/*": ["src/*"],
         "@/components/*": ["src/components/*"],
         "@/lib/*": ["src/lib/*"],
         "@/features/*": ["src/features/*"]
       }
     },
     "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
     "exclude": ["node_modules"]
   }
   ```

2. Fix type errors:
   ```bash
   # Check for errors
   pnpm tsc --noEmit

   # Common fixes:
   # - Replace `any` with proper types
   # - Add null checks for index access (obj[key])
   # - Type function parameters explicitly
   ```

3. Verify strict mode:
   ```bash
   grep '"strict": true' tsconfig.json
   grep '"noUncheckedIndexedAccess": true' tsconfig.json
   ```

**Expected outcome**: TypeScript strict mode enabled, catching 40% more errors at compile time

**Strict mode benefits**:
- No implicit `any` types
- Null safety for index access
- Better IDE autocomplete
- Catches errors before runtime

---

### Workflow 5: Migrate from Create React App (30-60 minutes)

**User signal**: "Migrate from CRA", "Replace Create React App", "Update to Vite/Next.js"

**Purpose**: Migrate deprecated Create React App project to Vite or Next.js

**Steps**:
1. Choose migration target:
   - **Vite**: If no SSR needed (most CRA projects)
   - **Next.js**: If adding SSR, SEO, or API routes

2. **Vite Migration**:
   ```bash
   # 1. Create new Vite project
   cp -r templates/react/vite-react-spa/* new-vite-project/
   cd new-vite-project && pnpm install

   # 2. Move source files
   cp -r ../old-cra-project/src/* src/

   # 3. Update imports
   # - Change `import logo from './logo.svg'` to use Vite conventions
   # - Update environment variables: REACT_APP_ → VITE_

   # 4. Update index.html
   # - Vite uses <script type="module" src="/src/main.tsx"></script>
   # - Move public/ assets to public/

   # 5. Test build
   pnpm build && pnpm preview
   ```

3. **Next.js Migration** (if SSR needed):
   ```bash
   # 1. Create Next.js project
   cp -r templates/react/nextjs-15-app-router/* new-nextjs-project/
   cd new-nextjs-project && pnpm install

   # 2. Convert components to App Router
   # - Move pages to src/app/
   # - Convert to Server Components (default)
   # - Add 'use client' for client components (useState, useEffect, event handlers)

   # 3. Update routing
   # - React Router → Next.js App Router
   # - <Link href="/about"> instead of <Link to="/about">

   # 4. Update environment variables
   # - REACT_APP_ → NEXT_PUBLIC_
   # - Server-side: no prefix (just API_KEY)
   ```

4. Test migration:
   ```bash
   # Start dev server
   pnpm dev

   # Verify all routes work
   # Test environment variables
   # Check API calls
   ```

**Expected outcome**: CRA project migrated to Vite (10x faster) or Next.js (SSR + SEO)

**Migration decision**:
- **Vite**: 80% of CRA projects (no SSR needed)
- **Next.js**: 20% of CRA projects (need SSR, SEO, API routes)

---

## Best Practices

### Practice 1: Always Use TypeScript Strict Mode

**Pattern**:
```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true
  }
}
```

**Why**: Catches 40% more errors at compile time, better IDE support

---

### Practice 2: Use Feature-Based Structure for Projects 10k+ Lines

**Pattern**:
```
src/features/
├── auth/           # Authentication feature
├── dashboard/      # Dashboard feature
└── users/          # User management feature
```

**Why**: Scales better than layer-based structure, clear module boundaries

---

### Practice 3: Separate Server and Client Components (Next.js)

**Pattern**:
```typescript
// Server Component (default in App Router)
async function ServerComponent() {
  const data = await fetch('https://api.example.com/data');
  return <div>{data}</div>;
}

// Client Component (needs 'use client')
'use client';
function ClientComponent() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

**Why**: Smaller bundle size (40-60% reduction), better performance

---

### Practice 4: Use Path Aliases for Clean Imports

**Pattern**:
```typescript
// ✅ GOOD: Path aliases
import { Button } from '@/components/ui/Button';
import { useAuth } from '@/features/auth';

// ❌ BAD: Relative paths
import { Button } from '../../../components/ui/Button';
import { useAuth } from '../../features/auth';
```

**Why**: Easier refactoring, cleaner imports, avoids ../../.. hell

---

### Practice 5: Use Environment Variables for Configuration

**Pattern**:
```bash
# .env.local (Next.js)
NEXT_PUBLIC_API_URL=https://api.example.com
DATABASE_URL=postgresql://...  # Server-side only

# .env (Vite)
VITE_API_URL=https://api.example.com
```

**Why**: Different configs for dev/staging/prod, keeps secrets out of code

---

## Common Pitfalls

### Pitfall 1: Using Client Components When Server Components Work

**Problem**: Add 'use client' to all components, increasing bundle size

**Fix**: Only use 'use client' when needed

```typescript
// ❌ BAD: Unnecessary client component
'use client';
function UserList({ users }: { users: User[] }) {
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}

// ✅ GOOD: Server component (no state, no effects)
function UserList({ users }: { users: User[] }) {
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

**Why**: Server components reduce bundle size by 40-60%

---

### Pitfall 2: Not Using TypeScript Strict Mode

**Problem**: Set "strict": false, miss type errors until runtime

**Fix**: Always use strict mode

```json
// ❌ BAD
{
  "compilerOptions": {
    "strict": false  // Allows unsafe code
  }
}

// ✅ GOOD
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true
  }
}
```

**Why**: Catches 40% more errors at compile time

---

### Pitfall 3: Using Layer-Based Structure for Large Projects

**Problem**: Organize by type (components/, hooks/, utils/) for 10k+ lines

**Fix**: Use feature-based structure

```
# ❌ BAD: Layer-based for large project
src/
├── components/  # 200+ components mixed together
├── hooks/       # 50+ hooks
└── utils/       # Hard to find related code

# ✅ GOOD: Feature-based
src/features/
├── auth/        # All auth code together
├── dashboard/   # All dashboard code together
└── users/       # All user code together
```

**Why**: Feature-based scales better, clearer ownership

---

### Pitfall 4: Not Configuring Path Aliases

**Problem**: Use relative imports everywhere (../../../../)

**Fix**: Configure path aliases in tsconfig.json

```typescript
// ❌ BAD: Relative import hell
import { Button } from '../../../components/ui/Button';

// ✅ GOOD: Path alias
import { Button } from '@/components/ui/Button';
```

**Why**: Easier refactoring, cleaner code, no import path breakage

---

### Pitfall 5: Hardcoding Environment-Specific Values

**Problem**: Hardcode API URLs, keys in code

**Fix**: Use environment variables

```typescript
// ❌ BAD: Hardcoded
const API_URL = 'https://api.production.com';

// ✅ GOOD: Environment variable
const API_URL = process.env.NEXT_PUBLIC_API_URL;
// Or: import.meta.env.VITE_API_URL (Vite)
```

**Why**: Different configs for dev/staging/prod, keeps secrets out of code

---

## Integration with Other SAPs

### SAP-021 (react-testing)
- React testing patterns (Vitest, React Testing Library)
- Integration: SAP-020 provides project structure, SAP-021 adds testing

### SAP-022 (react-linting)
- ESLint and Prettier configuration
- Integration: SAP-020 provides base, SAP-022 adds linting/formatting

### SAP-023 (react-state-management)
- TanStack Query, Zustand patterns
- Integration: SAP-020 includes basic setup, SAP-023 provides advanced patterns

### SAP-024 (react-styling)
- Tailwind CSS, CSS Modules patterns
- Integration: SAP-020 provides structure, SAP-024 adds styling strategy

### SAP-025 (react-performance)
- Performance optimization patterns
- Integration: SAP-020 provides foundation, SAP-025 adds optimization

---

## Support & Resources

**SAP-020 Documentation**:
- [Capability Charter](capability-charter.md) - React foundation problem and scope
- [Protocol Spec](protocol-spec.md) - Technical contracts and patterns
- [Awareness Guide](awareness-guide.md) - Detailed workflows
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Adoption tracking
- [REACT_SAP_SERIES_OVERVIEW.md](REACT_SAP_SERIES_OVERVIEW.md) - Overview of all React SAPs (SAP-020 to SAP-025)

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
- [TypeScript Handbook](https://www.typescriptlang.org/docs)

---

## Version History

- **1.0.0** (2025-11-05): Initial AGENTS.md for SAP-020
  - 5 workflows: Create Next.js Project, Create Vite SPA, Apply Feature-Based Structure, Configure TypeScript Strict Mode, Migrate from CRA
  - 2 user signal pattern tables (Project Scaffolding Operations, Project Structure Operations)
  - 5 best practices, 5 common pitfalls
  - Integration with SAP-021 through SAP-025

---

**Next Steps**:
1. Read [CLAUDE.md](CLAUDE.md) for Claude Code-specific patterns
2. Review [protocol-spec.md](protocol-spec.md) for technical contracts
3. Check [adoption-blueprint.md](adoption-blueprint.md) for installation
4. Start project: Copy `templates/react/nextjs-15-app-router/` or `templates/react/vite-react-spa/`

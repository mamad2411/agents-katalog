---
sap_id: SAP-022
version: 1.0.0
status: active
last_updated: 2025-11-05
type: reference
audience: agents
complexity: intermediate
estimated_reading_time: 12
progressive_loading:
  phase_1: "lines 1-200"   # Quick Start + Core Workflows
  phase_2: "lines 201-400" # Advanced Workflows
  phase_3: "full"          # Complete including best practices and pitfalls
phase_1_token_estimate: 4000
phase_2_token_estimate: 8000
phase_3_token_estimate: 12000
---

# React Linting & Formatting (SAP-022) - Agent Awareness

**SAP ID**: SAP-022
**Agent Compatibility**: All AI agents with command execution and file operations
**Last Updated**: 2025-11-05

---

## 📖 Quick Reference

**New to SAP-022?** → Read **[README.md](README.md)** first (11-min read)

The README provides:
- 🚀 **Quick Start** - 4-minute setup (ESLint 9 + Prettier 3 + 8 plugins) with flat config
- 📚 **Time Savings** - 40% code review time reduction, 50% faster onboarding, 5 hours/month saved, ESLint 9 is 182x faster
- 🎯 **React 19 + Next.js 15 Rules** - Server Components, Actions, new hooks validation
- 🔧 **TypeScript Strict Linting** - projectService API (30-50% faster type checking)
- 📊 **Accessibility** - WCAG 2.2 Level AA with jsx-a11y plugin (85%+ coverage)
- 🔗 **Integration** - Works with SAP-020 (Foundation), SAP-021 (Testing), SAP-024 (Styling), SAP-005 (CI/CD), SAP-006 (Quality Gates)

This AGENTS.md provides: Agent-specific patterns for React linting workflows.

---

## Quick Start for Agents

This SAP provides workflows for **React linting and formatting** with ESLint 9 flat config and Prettier 3.x.

### First-Time Session

1. **Check if linting already configured**: Look for `eslint.config.js` (ESLint 9) or `.eslintrc.*` (ESLint 8)
2. **Verify React project type**: Next.js 15, Vite 7, or other
3. **Install ESLint 9 + Prettier 3**: Use template-based setup for consistency
4. **Configure pre-commit hooks**: Husky + lint-staged for automatic linting

### Key Files

```
project-root/
├── eslint.config.js           # ESLint 9 flat config (NEW)
├── .prettierrc.json           # Prettier 3.x configuration
├── .prettierignore            # Prettier ignore patterns
├── .husky/
│   └── pre-commit             # Pre-commit hook for lint-staged
└── package.json               # Scripts: lint, format, lint:fix
```

---

## User Signal Pattern Tables

### Table 1: Linting Setup Signals

| User Intent | Example User Phrases | Agent Action | Expected Result |
|------------|---------------------|--------------|----------------|
| **Install linting** | "Setup ESLint", "Add linting to project", "Configure ESLint 9" | Execute Workflow 1: Install ESLint/Prettier | ESLint 9 + Prettier 3 installed with flat config |
| **Migrate to ESLint 9** | "Migrate to ESLint 9", "Use flat config", "Update from eslintrc" | Execute Workflow 2: Migrate from ESLint 8 to ESLint 9 | Flat config created, .eslintrc removed |
| **Setup Prettier** | "Add Prettier", "Format code automatically", "Setup Prettier integration" | Execute Workflow 3: Configure Prettier | Prettier 3.x configured with ESLint integration |
| **Add pre-commit hooks** | "Lint on commit", "Setup Husky", "Prevent bad commits" | Execute Workflow 4: Configure Pre-commit Hooks | Husky + lint-staged configured for auto-linting |
| **VS Code integration** | "Setup VS Code for linting", "Format on save", "Integrate with editor" | Execute Workflow 5: Setup VS Code Integration | VS Code settings.json configured for auto-fix/format |

### Table 2: Linting Operation Signals

| User Intent | Example User Phrases | Agent Action | Expected Result |
|------------|---------------------|--------------|----------------|
| **Run linter** | "Lint the code", "Check for errors", "Run ESLint" | Run `pnpm lint` | ESLint errors/warnings displayed |
| **Auto-fix issues** | "Fix lint errors", "Auto-fix issues", "Lint and fix" | Run `pnpm lint:fix` | Fixable errors auto-corrected |
| **Format code** | "Format code", "Run Prettier", "Format all files" | Run `pnpm format` | All files formatted with Prettier |
| **Check formatting** | "Check if code is formatted", "Verify formatting", "Prettier check" | Run `pnpm format:check` | Report unformatted files |
| **Lint specific file** | "Lint Button.tsx", "Check specific file" | Run `pnpm lint src/components/Button.tsx` | Lint errors for specific file |

---

## Workflow 1: Install ESLint 9 and Prettier 3 (15-25 minutes)

**When to use**: Setting up linting for new React project or upgrading existing project

**Prerequisites**:
- React project initialized (Next.js 15 or Vite 7)
- Node.js 18+ and pnpm/npm installed

**Steps**:

1. **Install ESLint 9 and required plugins**:
   ```bash
   pnpm add -D eslint@^9.26.0
   pnpm add -D @eslint/js@^9.26.0
   pnpm add -D typescript-eslint@^8.32.0
   pnpm add -D eslint-plugin-react@^7.37.5
   pnpm add -D eslint-plugin-react-hooks@^7.0.1
   pnpm add -D eslint-plugin-react-refresh@^0.4.24
   pnpm add -D eslint-plugin-jsx-a11y@^6.10.2
   pnpm add -D eslint-config-prettier@^9.1.0
   ```

2. **For Next.js projects, also install**:
   ```bash
   pnpm add -D eslint-config-next@15.5.3
   ```

3. **Install Prettier 3.x**:
   ```bash
   pnpm add -D prettier@^3.4.2
   ```

4. **Create ESLint 9 flat config** (`eslint.config.js`):
   ```javascript
   import js from '@eslint/js'
   import tseslint from 'typescript-eslint'
   import reactPlugin from 'eslint-plugin-react'
   import reactHooksPlugin from 'eslint-plugin-react-hooks'
   import reactRefreshPlugin from 'eslint-plugin-react-refresh'
   import jsxA11yPlugin from 'eslint-plugin-jsx-a11y'
   import prettierConfig from 'eslint-config-prettier'

   export default tseslint.config(
     // Global ignores
     {
       ignores: [
         '**/node_modules/**',
         '**/.next/**',
         '**/build/**',
         '**/dist/**',
         '**/.turbo/**',
         '**/coverage/**',
       ],
     },

     // Base configs
     js.configs.recommended,
     ...tseslint.configs.recommendedTypeChecked,
     reactPlugin.configs.flat.recommended,
     reactPlugin.configs.flat['jsx-runtime'],
     jsxA11yPlugin.flatConfigs.recommended,

     // React-specific settings
     {
       settings: {
         react: {
           version: 'detect',
         },
       },
     },

     // TypeScript project configuration
     {
       languageOptions: {
         parserOptions: {
           projectService: true,
           tsconfigRootDir: import.meta.dirname,
         },
       },
     },

     // React Hooks rules
     {
       plugins: {
         'react-hooks': reactHooksPlugin,
       },
       rules: {
         'react-hooks/rules-of-hooks': 'error',
         'react-hooks/exhaustive-deps': 'warn',
       },
     },

     // React Refresh rules (Vite projects)
     {
       plugins: {
         'react-refresh': reactRefreshPlugin,
       },
       rules: {
         'react-refresh/only-export-components': [
           'warn',
           { allowConstantExport: true },
         ],
       },
     },

     // Prettier integration (disables conflicting rules)
     prettierConfig,
   )
   ```

5. **Create Prettier configuration** (`.prettierrc.json`):
   ```json
   {
     "semi": true,
     "trailingComma": "all",
     "singleQuote": true,
     "printWidth": 100,
     "tabWidth": 2,
     "useTabs": false,
     "arrowParens": "always",
     "endOfLine": "lf"
   }
   ```

6. **Create Prettier ignore file** (`.prettierignore`):
   ```
   node_modules
   .next
   build
   dist
   .turbo
   coverage
   pnpm-lock.yaml
   package-lock.json
   ```

7. **Add scripts to package.json**:
   ```json
   {
     "scripts": {
       "lint": "eslint .",
       "lint:fix": "eslint . --fix",
       "format": "prettier --write .",
       "format:check": "prettier --check .",
       "typecheck": "tsc --noEmit"
     }
   }
   ```

8. **Verify installation**:
   ```bash
   pnpm lint
   pnpm format:check
   ```

**Expected outcome**:
- ESLint 9 flat config installed and working
- Prettier 3.x configured and integrated
- Scripts available: `lint`, `lint:fix`, `format`, `format:check`
- No conflicts between ESLint and Prettier

**Time saved**: 2-3 hours (manual setup) → 15-25 minutes (template-based)

---

## Workflow 2: Migrate from ESLint 8 to ESLint 9 Flat Config (10-20 minutes)

**When to use**: Upgrading existing project from ESLint 8 (.eslintrc) to ESLint 9 (flat config)

**Prerequisites**:
- Existing ESLint 8 configuration (.eslintrc.js, .eslintrc.json, or .eslintrc)
- Understanding of current linting rules

**Steps**:

1. **Read current ESLint configuration**:
   ```bash
   cat .eslintrc.js  # or .eslintrc.json
   ```

2. **Backup current configuration**:
   ```bash
   cp .eslintrc.js .eslintrc.js.backup
   ```

3. **Uninstall ESLint 8**:
   ```bash
   pnpm remove eslint
   ```

4. **Install ESLint 9 and plugins** (see Workflow 1, step 1-2)

5. **Convert .eslintrc to flat config**:

   **Old .eslintrc.js** (ESLint 8):
   ```javascript
   module.exports = {
     extends: [
       'eslint:recommended',
       'plugin:react/recommended',
       'plugin:@typescript-eslint/recommended',
       'prettier',
     ],
     plugins: ['react', '@typescript-eslint', 'react-hooks'],
     rules: {
       'react-hooks/rules-of-hooks': 'error',
       'react-hooks/exhaustive-deps': 'warn',
     },
   }
   ```

   **New eslint.config.js** (ESLint 9):
   ```javascript
   import js from '@eslint/js'
   import tseslint from 'typescript-eslint'
   import reactPlugin from 'eslint-plugin-react'
   import reactHooksPlugin from 'eslint-plugin-react-hooks'
   import prettierConfig from 'eslint-config-prettier'

   export default tseslint.config(
     js.configs.recommended,
     ...tseslint.configs.recommended,
     reactPlugin.configs.flat.recommended,
     {
       plugins: {
         'react-hooks': reactHooksPlugin,
       },
       rules: {
         'react-hooks/rules-of-hooks': 'error',
         'react-hooks/exhaustive-deps': 'warn',
       },
     },
     prettierConfig,
   )
   ```

6. **Remove old ESLint config files**:
   ```bash
   rm .eslintrc.js .eslintrc.json .eslintrc 2>/dev/null || true
   rm .eslintignore  # Use ignores: [] in flat config instead
   ```

7. **Update VS Code settings** (if using):
   ```json
   {
     "eslint.useFlatConfig": true
   }
   ```

8. **Test migration**:
   ```bash
   pnpm lint
   pnpm lint:fix
   ```

**Expected outcome**:
- ESLint 9 flat config working
- All rules migrated from .eslintrc
- 182x faster linting (ESLint 9 performance improvement)
- No .eslintrc files remaining

**Breaking changes to watch for**:
- `extends` array → imported configs in flat config
- `plugins` array → `plugins: {}` object
- `.eslintignore` → `ignores: []` in flat config
- `parser` option → `languageOptions.parser`

---

## Workflow 3: Configure Prettier with ESLint Integration (5-10 minutes)

**When to use**: Ensuring Prettier and ESLint work together without conflicts

**Prerequisites**:
- ESLint 9 installed (see Workflow 1)
- Prettier 3.x installed

**Steps**:

1. **Install Prettier integration**:
   ```bash
   pnpm add -D eslint-config-prettier@^9.1.0
   ```

2. **Add Prettier config to ESLint flat config**:
   ```javascript
   import prettierConfig from 'eslint-config-prettier'

   export default tseslint.config(
     // ... other configs
     prettierConfig,  // MUST be last to disable conflicting rules
   )
   ```

3. **Customize Prettier rules** (`.prettierrc.json`):
   ```json
   {
     "semi": true,
     "trailingComma": "all",
     "singleQuote": true,
     "printWidth": 100,
     "tabWidth": 2,
     "useTabs": false,
     "arrowParens": "always",
     "endOfLine": "lf",
     "bracketSpacing": true,
     "jsxSingleQuote": false,
     "quoteProps": "as-needed"
   }
   ```

4. **Test integration**:
   ```bash
   # Should show formatting issues, not ESLint rule conflicts
   pnpm lint
   pnpm format:check
   ```

5. **Verify no conflicts**:
   ```bash
   # Run both tools on same file - should not conflict
   pnpm lint src/App.tsx
   pnpm format src/App.tsx
   pnpm lint src/App.tsx  # Should still pass
   ```

**Expected outcome**:
- Prettier formats code style (quotes, semicolons, line breaks)
- ESLint checks code quality (unused vars, React rules, accessibility)
- No conflicting rules between tools
- `eslint-config-prettier` disables ESLint formatting rules

**Common Prettier options**:
- `semi: true` - Require semicolons
- `singleQuote: true` - Use single quotes
- `trailingComma: "all"` - Trailing commas everywhere (ES5+)
- `printWidth: 100` - Line length limit
- `arrowParens: "always"` - Always parentheses for arrow functions

---

## Workflow 4: Configure Pre-commit Hooks with Husky and lint-staged (10-15 minutes)

**When to use**: Enforcing linting and formatting on every commit

**Prerequisites**:
- ESLint 9 and Prettier 3 installed
- Git repository initialized

**Steps**:

1. **Install Husky and lint-staged**:
   ```bash
   pnpm add -D husky@^9.1.7 lint-staged@^15.3.0
   ```

2. **Initialize Husky**:
   ```bash
   pnpm exec husky init
   ```

   This creates `.husky/` directory and `pre-commit` hook.

3. **Configure lint-staged in package.json**:
   ```json
   {
     "lint-staged": {
       "*.{js,jsx,ts,tsx}": [
         "eslint --fix",
         "prettier --write"
       ],
       "*.{json,md,mdx,css,scss}": [
         "prettier --write"
       ]
     }
   }
   ```

4. **Update pre-commit hook** (`.husky/pre-commit`):
   ```bash
   pnpm exec lint-staged
   ```

5. **Test pre-commit hook**:
   ```bash
   # Create a file with lint errors
   echo "const unused = 123" > test.ts
   git add test.ts
   git commit -m "Test commit"
   # Should fail with ESLint errors
   ```

6. **Fix and retry**:
   ```bash
   pnpm lint:fix
   git add .
   git commit -m "Test commit"
   # Should pass after auto-fix
   ```

**Expected outcome**:
- Pre-commit hook runs `lint-staged` on every commit
- Only staged files are linted/formatted (fast)
- Commit blocked if linting fails
- Auto-fixable issues fixed automatically

**lint-staged performance**:
- Only runs on staged files (not entire codebase)
- 10x faster than running `pnpm lint` on full project
- Example: 50 files changed → 2 seconds vs 20 seconds

**Bypass hook (emergency only)**:
```bash
git commit --no-verify -m "Emergency commit"
```

---

## Workflow 5: Setup VS Code Integration for Auto-fix and Format-on-Save (5-10 minutes)

**When to use**: Configuring VS Code for automatic linting and formatting

**Prerequisites**:
- VS Code installed
- ESLint and Prettier extensions installed

**Steps**:

1. **Install VS Code extensions**:
   - [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)
   - [Prettier - Code formatter](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)

2. **Create or update `.vscode/settings.json`**:
   ```json
   {
     // Enable ESLint 9 flat config
     "eslint.useFlatConfig": true,

     // Format on save
     "editor.formatOnSave": true,
     "editor.defaultFormatter": "esbenp.prettier-vscode",

     // Auto-fix ESLint issues on save
     "editor.codeActionsOnSave": {
       "source.fixAll.eslint": "explicit"
     },

     // Prettier for specific file types
     "[javascript]": {
       "editor.defaultFormatter": "esbenp.prettier-vscode"
     },
     "[javascriptreact]": {
       "editor.defaultFormatter": "esbenp.prettier-vscode"
     },
     "[typescript]": {
       "editor.defaultFormatter": "esbenp.prettier-vscode"
     },
     "[typescriptreact]": {
       "editor.defaultFormatter": "esbenp.prettier-vscode"
     },
     "[json]": {
       "editor.defaultFormatter": "esbenp.prettier-vscode"
     },

     // ESLint validation for TypeScript
     "eslint.validate": [
       "javascript",
       "javascriptreact",
       "typescript",
       "typescriptreact"
     ]
   }
   ```

3. **Create `.vscode/extensions.json`** (recommended extensions):
   ```json
   {
     "recommendations": [
       "dbaeumer.vscode-eslint",
       "esbenp.prettier-vscode"
     ]
   }
   ```

4. **Test auto-fix on save**:
   - Open a TypeScript file with lint errors
   - Add a missing semicolon or unused variable
   - Save file (Cmd+S / Ctrl+S)
   - Should auto-fix and format

5. **Verify Prettier is default formatter**:
   - Right-click in editor → "Format Document With..."
   - Should show Prettier as default

**Expected outcome**:
- Lint errors auto-fixed on save
- Code formatted with Prettier on save
- VS Code shows ESLint errors inline
- Team members use same formatter

**VS Code keyboard shortcuts**:
- `Shift+Alt+F` (Windows) / `Shift+Opt+F` (Mac) - Format Document
- `Cmd+Shift+P` → "ESLint: Fix all auto-fixable Problems"

---

## Best Practices

### 1. Always Use ESLint 9 Flat Config for New Projects

**Pattern**:
```javascript
// ✅ GOOD: ESLint 9 flat config (eslint.config.js)
export default tseslint.config(
  js.configs.recommended,
  ...tseslint.configs.recommended,
)

// ❌ BAD: ESLint 8 .eslintrc (deprecated)
module.exports = {
  extends: ['eslint:recommended'],
}
```

**Why**: ESLint 9 flat config is 182x faster, simpler, and the future standard. `.eslintrc` will be removed in ESLint 10.

---

### 2. Use Accessibility Plugin (jsx-a11y) for WCAG 2.2 Compliance

**Pattern**:
```javascript
import jsxA11yPlugin from 'eslint-plugin-jsx-a11y'

export default tseslint.config(
  jsxA11yPlugin.flatConfigs.recommended,
)
```

**Why**: Catches accessibility issues early (missing alt text, ARIA misuse, keyboard navigation). WCAG 2.2 Level AA compliance reduces legal risk.

**Common a11y rules**:
- `jsx-a11y/alt-text` - Require alt text for images
- `jsx-a11y/aria-props` - Valid ARIA properties
- `jsx-a11y/click-events-have-key-events` - Keyboard accessibility

---

### 3. Enable TypeScript Type-Aware Linting with projectService

**Pattern**:
```javascript
export default tseslint.config({
  languageOptions: {
    parserOptions: {
      projectService: true,  // Auto-discovers tsconfig.json
      tsconfigRootDir: import.meta.dirname,
    },
  },
})
```

**Why**: Enables advanced TypeScript rules like `@typescript-eslint/no-floating-promises`, `@typescript-eslint/no-misused-promises`. 10x more powerful than syntax-only linting.

**Type-aware rules**:
- `@typescript-eslint/no-floating-promises` - Catch unhandled promises
- `@typescript-eslint/no-misused-promises` - Prevent promise misuse
- `@typescript-eslint/await-thenable` - Only await promises

---

### 4. Use lint-staged for Fast Pre-commit Checks

**Pattern**:
```json
{
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write"]
  }
}
```

**Why**: Only lints changed files (10x faster than full project lint). Prevents bad code from being committed.

**Performance comparison**:
- Full project lint: 20 seconds for 1000 files
- lint-staged: 2 seconds for 50 changed files

---

### 5. Disable Formatting Rules in ESLint, Use Prettier for Formatting

**Pattern**:
```javascript
import prettierConfig from 'eslint-config-prettier'

export default tseslint.config(
  // ... other configs
  prettierConfig,  // MUST be last
)
```

**Why**: ESLint for code quality, Prettier for code style. Prevents conflicts and double work.

**What ESLint checks**: Unused variables, React rules, accessibility
**What Prettier checks**: Semicolons, quotes, line breaks

---

## Common Pitfalls

### Pitfall 1: Using .eslintrc Instead of Flat Config for ESLint 9

**Problem**: Create `.eslintrc.js` for ESLint 9 project

**Symptom**: ESLint doesn't recognize configuration

**Fix**: Use flat config
```javascript
// ❌ BAD: .eslintrc.js (ESLint 8 format)
module.exports = {
  extends: ['eslint:recommended'],
}

// ✅ GOOD: eslint.config.js (ESLint 9 flat config)
import js from '@eslint/js'
export default [js.configs.recommended]
```

**Why**: ESLint 9 requires flat config, `.eslintrc` is deprecated

---

### Pitfall 2: Forgetting to Install Type-Aware Linting for TypeScript

**Problem**: Use `typescript-eslint` without enabling type-aware rules

**Symptom**: Advanced TypeScript rules don't work (no-floating-promises, etc.)

**Fix**: Enable projectService
```javascript
// ❌ BAD: Syntax-only linting
...tseslint.configs.recommended,

// ✅ GOOD: Type-aware linting
...tseslint.configs.recommendedTypeChecked,
{
  languageOptions: {
    parserOptions: {
      projectService: true,
      tsconfigRootDir: import.meta.dirname,
    },
  },
}
```

**Why**: Type-aware rules require TypeScript compiler integration

---

### Pitfall 3: Not Adding eslint-config-prettier to Flat Config

**Problem**: Use Prettier but don't disable conflicting ESLint rules

**Symptom**: ESLint and Prettier fight over formatting (quotes, semicolons)

**Fix**: Add eslint-config-prettier as last config
```javascript
import prettierConfig from 'eslint-config-prettier'

export default tseslint.config(
  // ... other configs
  prettierConfig,  // MUST be last
)
```

**Why**: `eslint-config-prettier` disables all ESLint formatting rules

---

### Pitfall 4: Running ESLint on Build Output (dist/, .next/)

**Problem**: Lint errors in generated build files

**Symptom**: ESLint fails with errors in `.next/`, `dist/`, `node_modules/`

**Fix**: Add ignores to flat config
```javascript
export default tseslint.config(
  {
    ignores: [
      '**/node_modules/**',
      '**/.next/**',
      '**/build/**',
      '**/dist/**',
    ],
  },
  // ... other configs
)
```

**Why**: Build output is auto-generated, shouldn't be linted

---

### Pitfall 5: Not Testing Pre-commit Hook After Setup

**Problem**: Setup Husky but don't test if it works

**Symptom**: Bad code committed despite pre-commit hook

**Fix**: Test with intentional lint error
```bash
# Create file with lint error
echo "const unused = 123" > test.ts
git add test.ts
git commit -m "Test"
# Should fail with ESLint error
```

**Why**: Pre-commit hooks can silently fail if misconfigured

---

## Support & Resources

**SAP-022 Documentation**:
- [Capability Charter](capability-charter.md) - React linting problem and scope
- [Protocol Spec](protocol-spec.md) - Technical contracts for ESLint 9 and Prettier 3
- [Awareness Guide](awareness-guide.md) - Detailed workflows
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Adoption tracking

**External Resources**:
- [ESLint 9 Docs](https://eslint.org/docs/latest/)
- [ESLint Flat Config Migration Guide](https://eslint.org/docs/latest/use/configure/migration-guide)
- [typescript-eslint Docs](https://typescript-eslint.io)
- [Prettier Docs](https://prettier.io/docs/en/)
- [Husky Docs](https://typicode.github.io/husky/)

**Related SAPs**:
- [SAP-020 (react-foundation)](../react-foundation/) - React project setup
- [SAP-021 (react-testing)](../react-testing/) - Testing patterns
- [SAP-023 (react-state-management)](../react-state-management/) - State patterns
- [SAP-024 (react-styling)](../react-styling/) - Styling strategies

---

## Version History

- **1.0.0** (2025-11-05): Initial AGENTS.md for SAP-022
  - 5 workflows: Install ESLint/Prettier, Migrate from ESLint 8 to ESLint 9, Configure Prettier, Configure Pre-commit Hooks, Setup VS Code Integration
  - 2 user signal pattern tables: Linting Setup Signals, Linting Operation Signals
  - 5 best practices: ESLint 9 flat config, accessibility plugin, type-aware linting, lint-staged, Prettier integration
  - 5 common pitfalls: Using .eslintrc instead of flat config, forgetting type-aware linting, missing eslint-config-prettier, linting build output, not testing pre-commit hook
  - Focus on ESLint 9 breaking changes and Prettier 3 integration

---

**Next Steps**:
1. Review [protocol-spec.md](protocol-spec.md) for technical contracts
2. Check [adoption-blueprint.md](adoption-blueprint.md) for installation
3. Install: `pnpm add -D eslint@^9.26.0 prettier@^3.4.2 husky@^9.1.7 lint-staged@^15.3.0`
4. Create `eslint.config.js` with flat config

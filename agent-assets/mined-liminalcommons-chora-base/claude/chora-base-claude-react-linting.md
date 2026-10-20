---
sap_id: SAP-022
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

# React Linting & Formatting (SAP-022) - Claude-Specific Awareness

**SAP ID**: SAP-022
**Claude Compatibility**: Sonnet 4.5+
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

This CLAUDE.md provides: Claude Code-specific workflows using Bash (linting), Write (config), Edit (rules).

---

## Quick Start for Claude

This file provides **Claude Code-specific patterns** for React linting with ESLint 9 and Prettier 3.

### First-Time Session

1. Read [AGENTS.md](AGENTS.md) for generic linting workflows
2. Use this file for Claude Code tool integration (Bash for installation, Write for config, Edit for modifications)
3. Always check if ESLint already configured before installing

### Linting Commands

```bash
# Check for lint errors
Bash: pnpm lint

# Auto-fix lint errors
Bash: pnpm lint:fix

# Format code with Prettier
Bash: pnpm format

# Check formatting
Bash: pnpm format:check
```

---

## Claude Code React Linting Workflows

### Workflow 1: Installing ESLint 9 and Prettier with Bash and Write

```markdown
User: "Setup linting for React project"

Claude (Phase 1: Check Existing Config - 0-5k tokens):
1. Check if ESLint already configured:
   Bash: ls eslint.config.js .eslintrc* 2>/dev/null || echo "No ESLint config found"

Claude (Phase 2: Install Dependencies - 5-15k tokens):
2. Install ESLint 9 and plugins:
   Bash: pnpm add -D eslint@^9.26.0 @eslint/js@^9.26.0 typescript-eslint@^8.32.0 eslint-plugin-react@^7.37.5 eslint-plugin-react-hooks@^7.0.1 eslint-plugin-react-refresh@^0.4.24 eslint-plugin-jsx-a11y@^6.10.2 eslint-config-prettier@^9.1.0

3. Install Prettier:
   Bash: pnpm add -D prettier@^3.4.2

Claude (Phase 3: Create Config Files - 15-30k tokens):
4. Create ESLint 9 flat config:
   Write eslint.config.js
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
       ],
     },

     // Base configs
     js.configs.recommended,
     ...tseslint.configs.recommendedTypeChecked,
     reactPlugin.configs.flat.recommended,
     reactPlugin.configs.flat['jsx-runtime'],
     jsxA11yPlugin.flatConfigs.recommended,

     // React settings
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

     // React Refresh rules
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

     // Prettier integration (must be last)
     prettierConfig,
   )
   ```

5. Create Prettier config:
   Write .prettierrc.json
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

6. Create Prettier ignore:
   Write .prettierignore
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

Claude (Phase 4: Update package.json - 30-40k tokens):
7. Read current package.json:
   Read package.json

8. Add lint scripts:
   Edit package.json
   # Add scripts:
   # "lint": "eslint ."
   # "lint:fix": "eslint . --fix"
   # "format": "prettier --write ."
   # "format:check": "prettier --check ."

9. Verify installation:
   Bash: pnpm lint
   Bash: pnpm format:check

Claude (response to user):
"✅ ESLint 9 and Prettier 3 installed!

**Installed**:
- ESLint 9.26.0 (182x faster than v8)
- TypeScript ESLint 8.32.0
- React, Hooks, Accessibility plugins
- Prettier 3.4.2

**Configuration**:
- eslint.config.js - ESLint 9 flat config
- .prettierrc.json - Prettier config
- .prettierignore - Ignored files

**Run linting**:
```bash
pnpm lint              # Check for errors
pnpm lint:fix          # Auto-fix errors
pnpm format            # Format with Prettier
pnpm format:check      # Check formatting
```

**Next steps**:
1. Install pre-commit hooks (Husky + lint-staged)
2. Configure VS Code integration
3. Fix any existing lint errors"

Result: Complete linting infrastructure installed and configured
```

---

### Workflow 2: Migrating from ESLint 8 to ESLint 9 with Read and Write

```markdown
User: "Migrate to ESLint 9 flat config"

Claude (Phase 1: Read Existing Config - 0-10k tokens):
1. Read current ESLint config:
   Read .eslintrc.js
   # Or .eslintrc.json, .eslintrc

2. Backup current config:
   Bash: cp .eslintrc.js .eslintrc.js.backup

Claude (Phase 2: Install ESLint 9 - 10-20k tokens):
3. Uninstall ESLint 8:
   Bash: pnpm remove eslint

4. Install ESLint 9:
   Bash: pnpm add -D eslint@^9.26.0 @eslint/js@^9.26.0 typescript-eslint@^8.32.0 eslint-plugin-react@^7.37.5 eslint-plugin-react-hooks@^7.0.1 eslint-config-prettier@^9.1.0

Claude (Phase 3: Convert Config - 20-35k tokens):
5. Convert .eslintrc to flat config:
   Write eslint.config.js
   # Convert extends array to imported configs
   # Convert plugins array to plugins object
   # Convert .eslintignore to ignores array

6. Remove old config files:
   Bash: rm .eslintrc.js .eslintrc.json .eslintrc .eslintignore 2>/dev/null || true

7. Test migration:
   Bash: pnpm lint

Claude (response to user):
"✅ Migrated to ESLint 9 flat config!

**Changes**:
- ESLint 8 (.eslintrc) → ESLint 9 (eslint.config.js)
- 182x faster linting performance
- Flat config structure (simpler, more intuitive)

**Breaking changes handled**:
- extends array → imported configs
- plugins array → plugins object
- .eslintignore → ignores in flat config

**Test results**:
```
✓ All rules migrated
✓ Lint passes on existing code
✓ Old config files removed
```

**Backup**: .eslintrc.js.backup (for reference)"

Result: Successfully migrated to ESLint 9 flat config
```

---

### Workflow 3: Configuring Pre-commit Hooks with Bash and Edit

```markdown
User: "Setup pre-commit linting with Husky"

Claude (Phase 1: Install Husky and lint-staged - 0-10k tokens):
1. Install dependencies:
   Bash: pnpm add -D husky@^9.1.7 lint-staged@^15.3.0

2. Initialize Husky:
   Bash: pnpm exec husky init

Claude (Phase 2: Configure lint-staged - 10-20k tokens):
3. Read current package.json:
   Read package.json

4. Add lint-staged configuration:
   Edit package.json
   # Add lint-staged config:
   # "lint-staged": {
   #   "*.{js,jsx,ts,tsx}": ["eslint --fix", "prettier --write"],
   #   "*.{json,md,mdx,css,scss}": ["prettier --write"]
   # }

5. Update pre-commit hook:
   Edit .husky/pre-commit
   # old_string: pnpm test
   # new_string: pnpm exec lint-staged

Claude (Phase 3: Test Hook - 20-30k tokens):
6. Create test file with lint error:
   Bash: echo "const unused = 123" > test-lint.ts

7. Test pre-commit hook:
   Bash: git add test-lint.ts
   Bash: git commit -m "Test pre-commit hook"
   # Should fail with ESLint error

8. Clean up test file:
   Bash: rm test-lint.ts
   Bash: git reset HEAD test-lint.ts

Claude (response to user):
"✅ Pre-commit hooks configured!

**Installed**:
- Husky 9.1.7 (Git hooks manager)
- lint-staged 15.3.0 (Lint only staged files)

**Pre-commit hook**:
- Runs ESLint --fix on staged .ts/.tsx files
- Runs Prettier on staged files
- Only lints changed files (10x faster)
- Blocks commit if linting fails

**Test results**:
```
✓ Pre-commit hook triggers on git commit
✓ Lint errors block commit
✓ Auto-fixable issues fixed automatically
```

**Bypass hook** (emergency only):
```bash
git commit --no-verify -m "Emergency commit"
```"

Result: Pre-commit hooks working, automatic linting on every commit
```

---

## Claude-Specific Tips

### Tip 1: Always Read Existing Config Before Migrating

**Pattern**:
```markdown
# Before migrating to ESLint 9:
Read .eslintrc.js
# Understand current rules and plugins

# Then migrate:
Write eslint.config.js
# Convert to flat config
```

**Why**: Preserve custom rules and plugins during migration

---

### Tip 2: Use Write for New Config Files, Edit for Modifications

**Pattern**:
```markdown
# New config → Use Write:
Write eslint.config.js
# Full flat config content

# Modify existing config → Use Edit:
Edit eslint.config.js
# old_string: 'react-hooks/exhaustive-deps': 'warn'
# new_string: 'react-hooks/exhaustive-deps': 'error'
```

**Why**: Write for new files, Edit for targeted changes

---

### Tip 3: Test Linting Immediately After Installation

**Pattern**:
```markdown
# After installing ESLint:
Write eslint.config.js

# Immediately test:
Bash: pnpm lint

# Fix any errors:
Bash: pnpm lint:fix
```

**Why**: Catch configuration errors early

---

### Tip 4: Use Bash to Verify Pre-commit Hook Works

**Pattern**:
```markdown
# After setting up Husky:
Bash: echo "const unused = 123" > test.ts
Bash: git add test.ts
Bash: git commit -m "Test"
# Should fail

# Clean up:
Bash: rm test.ts
Bash: git reset HEAD test.ts
```

**Why**: Verify hook blocks bad commits

---

### Tip 5: Check if ESLint Already Configured Before Installing

**Pattern**:
```markdown
# Before installing:
Bash: ls eslint.config.js .eslintrc* 2>/dev/null || echo "No config"

# If found, migrate instead of install:
Read .eslintrc.js
# Then convert to flat config
```

**Why**: Avoid overwriting existing configuration

---

## Common Pitfalls for Claude Code

### Pitfall 1: Not Removing .eslintrc After Migration

**Problem**: Create eslint.config.js but leave .eslintrc files

**Fix**: Remove old config files
```markdown
# ❌ BAD: Leave old config
Write eslint.config.js
# .eslintrc.js still exists

# ✅ GOOD: Remove old config
Write eslint.config.js
Bash: rm .eslintrc.js .eslintrc.json .eslintrc 2>/dev/null || true
```

**Why**: ESLint may use old config instead of flat config

---

### Pitfall 2: Forgetting to Add prettierConfig as Last Config

**Problem**: Add eslint-config-prettier in middle of config array

**Fix**: Always add as last config
```javascript
// ❌ BAD: prettierConfig in middle
export default tseslint.config(
  prettierConfig,
  js.configs.recommended,  // May re-enable formatting rules
)

// ✅ GOOD: prettierConfig last
export default tseslint.config(
  js.configs.recommended,
  prettierConfig,  // Disables all formatting rules
)
```

**Why**: Later configs override earlier ones

---

### Pitfall 3: Not Testing Pre-commit Hook After Setup

**Problem**: Setup Husky but don't verify it works

**Fix**: Test with intentional error
```markdown
# After Husky setup:
Bash: echo "const unused = 123" > test.ts
Bash: git add test.ts
Bash: git commit -m "Test"
# Should fail with ESLint error
```

**Why**: Pre-commit hooks can silently fail if misconfigured

---

### Pitfall 4: Using Write Instead of Edit for package.json Scripts

**Problem**: Overwrite entire package.json with Write

**Fix**: Use Edit for targeted changes
```markdown
# ❌ BAD: Overwrite package.json
Write package.json
# Loses existing scripts and dependencies

# ✅ GOOD: Edit scripts section
Read package.json
Edit package.json
# old_string: "scripts": {
# new_string: "scripts": {
#   "lint": "eslint .",
#   "lint:fix": "eslint . --fix",
```

**Why**: Edit preserves existing configuration

---

### Pitfall 5: Not Installing Type-Aware Linting for TypeScript

**Problem**: Use typescript-eslint without enabling type checking

**Fix**: Add projectService configuration
```javascript
// ❌ BAD: No type checking
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

**Why**: Type-aware rules catch more errors (floating promises, etc.)

---

## Support & Resources

**SAP-022 Documentation**:
- [AGENTS.md](AGENTS.md) - Generic React linting workflows
- [Capability Charter](capability-charter.md) - React linting problem and scope
- [Protocol Spec](protocol-spec.md) - Technical contracts and patterns
- [Awareness Guide](awareness-guide.md) - Detailed workflows
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Adoption tracking

**External Resources**:
- [ESLint 9 Docs](https://eslint.org/docs/latest/)
- [ESLint Flat Config Migration](https://eslint.org/docs/latest/use/configure/migration-guide)
- [typescript-eslint Docs](https://typescript-eslint.io)
- [Prettier Docs](https://prettier.io)
- [Husky Docs](https://typicode.github.io/husky/)

**Related SAPs**:
- [SAP-020 (react-foundation)](../react-foundation/) - React project setup
- [SAP-021 (react-testing)](../react-testing/) - Testing patterns
- [SAP-023 (react-state-management)](../react-state-management/) - State patterns
- [SAP-024 (react-styling)](../react-styling/) - Styling strategies

---

## Version History

- **1.0.0** (2025-11-05): Initial CLAUDE.md for SAP-022
  - 3 workflows: Installing ESLint 9/Prettier with Bash/Write, Migrating from ESLint 8 to ESLint 9 with Read/Write, Configuring Pre-commit Hooks with Bash/Edit
  - Tool patterns: Bash for installation and testing, Write for new config files, Edit for package.json modifications, Read for existing config
  - 5 Claude-specific tips, 5 common pitfalls
  - Focus on ESLint 9 flat config migration and pre-commit hooks

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic React linting workflows
2. Review [protocol-spec.md](protocol-spec.md) for technical contracts
3. Check [adoption-blueprint.md](adoption-blueprint.md) for installation
4. Install: `pnpm add -D eslint@^9.26.0 prettier@^3.4.2 husky@^9.1.7 lint-staged@^15.3.0`

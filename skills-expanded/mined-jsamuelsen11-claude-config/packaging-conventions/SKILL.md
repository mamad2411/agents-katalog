---
name: packaging-conventions
description:
  This skill should be used when creating or editing package.json, tsconfig, managing npm
  dependencies, configuring monorepos, or publishing npm packages.
version: 0.1.0
---

# TypeScript Packaging and Publishing Conventions

This skill defines best practices for packaging, dependency management, monorepo configuration, and
publishing TypeScript packages to npm with modern module formats and optimal developer experience.

## package.json Configuration

### Essential Fields

**ALWAYS include these core fields in package.json.**

CORRECT:

```json
{
  "name": "@scope/package-name",
  "version": "1.2.3",
  "description": "Clear, concise package description",
  "keywords": ["typescript", "library", "utility"],
  "author": "Your Name <email@example.com>",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/username/repo.git"
  },
  "bugs": {
    "url": "https://github.com/username/repo/issues"
  },
  "homepage": "https://github.com/username/repo#readme"
}
```

### Module Type and Exports

**ALWAYS use "type": "module" for ESM packages and configure exports properly.**

CORRECT for ESM-only package:

```json
{
  "name": "@scope/package-name",
  "version": "1.0.0",
  "type": "module",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": {
        "types": "./dist/index.d.ts",
        "default": "./dist/index.js"
      }
    }
  },
  "files": ["dist"],
  "sideEffects": false
}
```

CORRECT for dual ESM/CJS package:

```json
{
  "name": "@scope/package-name",
  "version": "1.0.0",
  "type": "module",
  "main": "./dist/index.cjs",
  "module": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": {
        "types": "./dist/index.d.ts",
        "default": "./dist/index.js"
      },
      "require": {
        "types": "./dist/index.d.cts",
        "default": "./dist/index.cjs"
      }
    },
    "./package.json": "./package.json"
  },
  "files": ["dist"],
  "sideEffects": false
}
```

CORRECT for multiple entry points:

```json
{
  "name": "@scope/package-name",
  "version": "1.0.0",
  "type": "module",
  "exports": {
    ".": {
      "import": {
        "types": "./dist/index.d.ts",
        "default": "./dist/index.js"
      },
      "require": {
        "types": "./dist/index.d.cts",
        "default": "./dist/index.cjs"
      }
    },
    "./utils": {
      "import": {
        "types": "./dist/utils.d.ts",
        "default": "./dist/utils.js"
      },
      "require": {
        "types": "./dist/utils.d.cts",
        "default": "./dist/utils.cjs"
      }
    },
    "./package.json": "./package.json"
  },
  "typesVersions": {
    "*": {
      "utils": ["./dist/utils.d.ts"]
    }
  }
}
```

### Files Field

**Explicitly list files to publish to avoid bloat.**

CORRECT:

```json
{
  "files": ["dist", "README.md", "LICENSE"]
}
```

WRONG:

```json
{
  "files": ["src", "dist", "tests", "node_modules"]
}
```

### sideEffects Field

**ALWAYS set sideEffects to enable tree-shaking.**

CORRECT for pure library:

```json
{
  "sideEffects": false
}
```

CORRECT for library with some side effects:

```json
{
  "sideEffects": ["*.css", "./src/polyfills.ts"]
}
```

### Package Manager Field

**Specify packageManager for consistent dependency resolution.**

CORRECT:

```json
{
  "packageManager": "pnpm@8.15.0"
}
```

### Scripts Convention

**Standardize script names across projects.**

CORRECT:

```json
{
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsup",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest run --coverage",
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "typecheck": "tsc --noEmit",
    "validate": "pnpm run typecheck && pnpm run lint && pnpm run test:coverage && pnpm run format:check",
    "clean": "rm -rf dist coverage",
    "prepublishOnly": "pnpm run validate && pnpm run build"
  }
}
```

### Engines Field

**Specify supported Node.js and package manager versions.**

CORRECT:

```json
{
  "engines": {
    "node": ">=18.0.0",
    "pnpm": ">=8.0.0"
  }
}
```

## TypeScript Configuration

### Library tsconfig.json

CORRECT for publishable library:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "lib": ["ES2023"],
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitReturns": true,
    "noPropertyAccessFromIndexSignature": true,
    "allowUnusedLabels": false,
    "allowUnreachableCode": false,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts", "**/*.spec.ts"]
}
```

### Application tsconfig.json with Path Aliases

CORRECT:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "lib": ["ES2023", "DOM", "DOM.Iterable"],
    "jsx": "react-jsx",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@components/*": ["./src/components/*"],
      "@utils/*": ["./src/utils/*"],
      "@hooks/*": ["./src/hooks/*"],
      "@types/*": ["./src/types/*"]
    },
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

### Monorepo Base tsconfig.json

CORRECT base config (tsconfig.base.json):

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitReturns": true,
    "noPropertyAccessFromIndexSignature": true,
    "allowUnusedLabels": false,
    "allowUnreachableCode": false,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  }
}
```

Package-specific tsconfig:

```json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "lib": ["ES2023"],
    "outDir": "./dist",
    "rootDir": "./src",
    "composite": true
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

### Project References for Monorepos

CORRECT root tsconfig.json with references:

```json
{
  "files": [],
  "references": [
    { "path": "./packages/core" },
    { "path": "./packages/utils" },
    { "path": "./packages/cli" },
    { "path": "./apps/web" }
  ]
}
```

Build with references:

```bash
tsc --build --verbose
```

## Bundling Configuration

### tsup for Library Bundling

**ALWAYS use tsup for library bundling (ESM + CJS).**

CORRECT tsup.config.ts:

```typescript
import { defineConfig } from 'tsup';

export default defineConfig({
  entry: ['src/index.ts'],
  format: ['cjs', 'esm'],
  dts: true,
  splitting: false,
  sourcemap: true,
  clean: true,
  treeshake: true,
  minify: false,
  target: 'es2022',
  outDir: 'dist',
});
```

For multiple entry points:

```typescript
import { defineConfig } from 'tsup';

export default defineConfig({
  entry: {
    index: 'src/index.ts',
    utils: 'src/utils.ts',
    cli: 'src/cli.ts',
  },
  format: ['cjs', 'esm'],
  dts: true,
  splitting: false,
  sourcemap: true,
  clean: true,
  treeshake: true,
  outDir: 'dist',
});
```

### Vite for Application Bundling

CORRECT vite.config.ts:

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    target: 'es2022',
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
        },
      },
    },
  },
});
```

### esbuild for Fast Builds

CORRECT build script with esbuild:

```typescript
// build.ts
import * as esbuild from 'esbuild';

await esbuild.build({
  entryPoints: ['src/index.ts'],
  bundle: true,
  outfile: 'dist/index.js',
  platform: 'node',
  format: 'esm',
  target: 'es2022',
  sourcemap: true,
  external: ['node:*'],
  minify: false,
});
```

## Dependency Management

### Dependency Types

**Place dependencies in the correct field.**

CORRECT:

```json
{
  "dependencies": {
    "zod": "^3.22.4",
    "date-fns": "^3.0.0"
  },
  "devDependencies": {
    "typescript": "^5.3.3",
    "vitest": "^1.2.0",
    "@types/node": "^20.11.0",
    "tsup": "^8.0.1",
    "prettier": "^3.2.4",
    "eslint": "^8.56.0"
  },
  "peerDependencies": {
    "react": "^18.0.0"
  },
  "peerDependenciesMeta": {
    "react": {
      "optional": false
    }
  }
}
```

WRONG:

```json
{
  "dependencies": {
    "typescript": "^5.3.3",
    "vitest": "^1.2.0",
    "@types/node": "^20.11.0",
    "react": "^18.0.0"
  }
}
```

### Version Ranges

**Use conservative version ranges for libraries, flexible for applications.**

CORRECT for libraries:

```json
{
  "dependencies": {
    "zod": "^3.22.4",
    "date-fns": "^3.0.0"
  }
}
```

CORRECT for applications (can be more flexible):

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "zod": "^3.22.4"
  }
}
```

### Peer Dependencies for Libraries

**ALWAYS specify peer dependencies for libraries that extend other tools.**

CORRECT React component library:

```json
{
  "name": "@scope/ui-components",
  "peerDependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  },
  "peerDependenciesMeta": {
    "react-dom": {
      "optional": false
    }
  },
  "devDependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  }
}
```

CORRECT TypeScript plugin:

```json
{
  "name": "@scope/typescript-plugin",
  "peerDependencies": {
    "typescript": "^5.0.0"
  },
  "devDependencies": {
    "typescript": "^5.3.3"
  }
}
```

## Monorepo Configuration

### pnpm Workspaces

**ALWAYS use pnpm workspaces for monorepos.**

CORRECT pnpm-workspace.yaml:

```yaml
packages:
  - 'packages/*'
  - 'apps/*'
  - 'tools/*'
```

CORRECT root package.json:

```json
{
  "name": "monorepo-root",
  "private": true,
  "packageManager": "pnpm@8.15.0",
  "scripts": {
    "dev": "pnpm -r --parallel dev",
    "build": "pnpm -r --filter '!@scope/app-*' build",
    "test": "pnpm -r test",
    "lint": "pnpm -r lint",
    "typecheck": "pnpm -r typecheck",
    "clean": "pnpm -r clean && rm -rf node_modules"
  },
  "devDependencies": {
    "typescript": "^5.3.3",
    "prettier": "^3.2.4",
    "eslint": "^8.56.0"
  }
}
```

### Package Dependencies in Monorepo

CORRECT cross-package dependency:

```json
{
  "name": "@scope/app-web",
  "dependencies": {
    "@scope/core": "workspace:*",
    "@scope/ui": "workspace:*"
  }
}
```

### Turborepo for Build Orchestration

CORRECT turbo.json:

```json
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"]
    },
    "test": {
      "dependsOn": ["^build"],
      "outputs": ["coverage/**"]
    },
    "lint": {
      "outputs": []
    },
    "typecheck": {
      "dependsOn": ["^build"],
      "outputs": []
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

Run with Turborepo:

```bash
pnpm turbo build
pnpm turbo test --filter=@scope/core
pnpm turbo dev --parallel
```

### Shared Configurations in Monorepo

CORRECT shared TypeScript config:

```text
monorepo/
├── tsconfig.base.json
├── packages/
│   ├── core/
│   │   └── tsconfig.json (extends ../../tsconfig.base.json)
│   └── utils/
│       └── tsconfig.json (extends ../../tsconfig.base.json)
└── apps/
    └── web/
        └── tsconfig.json (extends ../../tsconfig.base.json)
```

CORRECT shared ESLint config:

```javascript
// packages/eslint-config/index.js
import js from '@eslint/js';
import tseslint from 'typescript-eslint';

export default tseslint.config(js.configs.recommended, ...tseslint.configs.strictTypeChecked);
```

Use in packages:

```javascript
// packages/core/eslint.config.js
import baseConfig from '@scope/eslint-config';

export default [
  ...baseConfig,
  {
    languageOptions: {
      parserOptions: {
        project: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
  },
];
```

## Publishing to npm

### Pre-publish Checklist

Before publishing, ensure:

1. All tests pass
1. Type checking passes
1. Linting passes
1. Build succeeds
1. README is complete
1. CHANGELOG is updated
1. Version is bumped
1. Git tag is created

### Changesets for Versioning

**ALWAYS use Changesets for version management.**

Install:

```bash
pnpm add -D @changesets/cli
pnpm exec changeset init
```

CORRECT .changeset/config.json:

```json
{
  "$schema": "https://unpkg.com/@changesets/config@3.0.0/schema.json",
  "changelog": "@changesets/cli/changelog",
  "commit": false,
  "fixed": [],
  "linked": [],
  "access": "public",
  "baseBranch": "main",
  "updateInternalDependencies": "patch",
  "ignore": []
}
```

Add changeset:

```bash
pnpm exec changeset
```

Version packages:

```bash
pnpm exec changeset version
```

Publish:

```bash
pnpm exec changeset publish
```

### Package.json for Publishing

CORRECT for public package:

```json
{
  "name": "@scope/package-name",
  "version": "1.0.0",
  "description": "Package description",
  "keywords": ["typescript", "library"],
  "author": "Your Name",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/username/repo.git"
  },
  "publishConfig": {
    "access": "public"
  },
  "scripts": {
    "prepublishOnly": "pnpm run validate && pnpm run build"
  }
}
```

CORRECT for private package:

```json
{
  "name": "@scope/internal-package",
  "version": "1.0.0",
  "private": true
}
```

### npm Scripts for Publishing

CORRECT:

```json
{
  "scripts": {
    "prepublishOnly": "pnpm run validate && pnpm run build",
    "prepack": "pnpm run build",
    "postpublish": "git push --follow-tags"
  }
}
```

### .npmignore

CORRECT .npmignore:

```text
# Source files
src/
tests/
e2e/
**/*.test.ts
**/*.spec.ts
**/__tests__/

# Configuration
tsconfig.json
vitest.config.ts
eslint.config.js
.prettierrc
.editorconfig

# Development
.vscode/
.idea/
*.log
.env
.env.*

# Build artifacts
coverage/
.vitest/
node_modules/

# Git
.git/
.gitignore
```

Or use `files` field in package.json (preferred):

```json
{
  "files": ["dist", "README.md", "LICENSE"]
}
```

## Dual Package Hazard Prevention

### Correct Dual ESM/CJS Setup

CORRECT:

```json
{
  "type": "module",
  "main": "./dist/index.cjs",
  "module": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": {
        "types": "./dist/index.d.ts",
        "default": "./dist/index.js"
      },
      "require": {
        "types": "./dist/index.d.cts",
        "default": "./dist/index.cjs"
      }
    }
  }
}
```

WRONG (can cause dual package hazard):

```json
{
  "main": "./dist/index.js",
  "module": "./dist/index.esm.js",
  "exports": "./dist/index.js"
}
```

### tsup Configuration for Dual Format

CORRECT:

```typescript
import { defineConfig } from 'tsup';

export default defineConfig({
  entry: ['src/index.ts'],
  format: ['cjs', 'esm'],
  dts: true,
  splitting: false,
  sourcemap: true,
  clean: true,
  outDir: 'dist',
  // Ensures .cjs and .js extensions
  outExtension({ format }) {
    return {
      js: format === 'cjs' ? '.cjs' : '.js',
    };
  },
});
```

## Documentation

### README Template

CORRECT README.md structure:

````markdown
# @scope/package-name

Brief description of the package.

## Installation

```bash
pnpm add @scope/package-name
```

## Usage

```typescript
import { someFunction } from '@scope/package-name';

const result = someFunction('input');
```

## API

### `someFunction(input: string): string`

Description of what the function does.

**Parameters:**

- `input` - Description of parameter

**Returns:** Description of return value

**Example:**

```typescript
const result = someFunction('test');
// result: 'TEST'
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT © Your Name
````

### API Documentation with TSDoc

CORRECT:

````typescript
/**
 * Validates an email address.
 *
 * @param email - The email address to validate
 * @returns `true` if valid, `false` otherwise
 *
 * @example
 * ```ts
 * isValidEmail('user@example.com'); // true
 * isValidEmail('invalid'); // false
 * ```
 *
 * @public
 */
export function isValidEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
````

### Generate Documentation with TypeDoc

Install:

```bash
pnpm add -D typedoc
```

CORRECT typedoc.json:

```json
{
  "entryPoints": ["src/index.ts"],
  "out": "docs",
  "plugin": ["typedoc-plugin-markdown"],
  "readme": "README.md",
  "exclude": ["**/*.test.ts", "**/*.spec.ts"]
}
```

Generate:

```bash
pnpm exec typedoc
```

## CI/CD for Publishing

### GitHub Actions Workflow

CORRECT .github/workflows/publish.yml:

```yaml
name: Publish Package

on:
  push:
    branches:
      - main

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      id-token: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          registry-url: 'https://registry.npmjs.org'

      - uses: pnpm/action-setup@v2
        with:
          version: 8

      - run: pnpm install

      - run: pnpm run validate

      - run: pnpm run build

      - name: Create Release Pull Request or Publish
        uses: changesets/action@v1
        with:
          publish: pnpm exec changeset publish
          version: pnpm exec changeset version
          commit: 'chore: version packages'
          title: 'chore: version packages'
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

## Best Practices Summary

When configuring packages:

1. Use "type": "module" for ESM
1. Configure proper exports field
1. Specify files to publish
1. Set sideEffects for tree-shaking
1. Use packageManager field
1. Standardize script names
1. Specify engine requirements
1. Use strict TypeScript config
1. Bundle with tsup for libraries
1. Place dependencies correctly
1. Use pnpm workspaces for monorepos
1. Use Turborepo for orchestration
1. Use Changesets for versioning
1. Write comprehensive README
1. Add TSDoc comments
1. Configure CI/CD for publishing

These conventions ensure professional, maintainable npm packages.

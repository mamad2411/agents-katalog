---
name: npm-scripts
description: npm, yarn, and pnpm package management, scripts, workspaces, and publishing. Use when user asks to "run npm script", "setup package.json", "publish package", "manage dependencies", "npm workspaces", "monorepo setup", "npm audit", "lock file", "npmrc config", "npm registry", "debug npm script", "npx", "cross-platform script", or package manager operations.
---

# npm Scripts and Package Management

## Package.json Scripts

### Common Script Patterns

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "start": "node dist/index.js",
    "test": "vitest",
    "test:watch": "vitest watch",
    "test:coverage": "vitest --coverage",
    "lint": "eslint src/",
    "lint:fix": "eslint src/ --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "typecheck": "tsc --noEmit",
    "clean": "rm -rf dist node_modules/.cache",
    "prepare": "husky",
    "validate": "npm-run-all --parallel lint typecheck test:coverage"
  }
}
```

### Pre/Post Hooks and Lifecycle Scripts

npm runs `pre<script>` before and `post<script>` after any script automatically:

```json
{
  "scripts": {
    "prebuild": "npm run clean",
    "build": "tsc",
    "postbuild": "npm run copy-assets",
    "clean": "rm -rf dist",
    "copy-assets": "cp -r assets dist/",
    "prepare": "husky",
    "prepublishOnly": "npm run build && npm test",
    "postinstall": "patch-package"
  }
}
```

Built-in lifecycle scripts:
- `prepare` -- runs after `npm install` and before `npm publish`
- `prepublishOnly` -- runs before `npm publish` only (not on install)
- `preinstall` / `postinstall` -- before/after `npm install`
- `prepack` / `postpack` -- before/after tarball is created

### Cross-Platform Scripts

```json
{
  "devDependencies": {
    "cross-env": "^7.0.3",
    "shx": "^0.3.4",
    "npm-run-all2": "^6.0.0"
  },
  "scripts": {
    "build": "cross-env NODE_ENV=production webpack",
    "clean": "shx rm -rf dist",
    "dev": "run-p watch:css watch:js serve",
    "ci": "run-s lint typecheck test build",
    "lint:all": "run-p lint:js lint:css lint:html"
  }
}
```

- `run-s` -- sequential; `run-p` -- parallel
- Glob patterns: `run-p lint:*` runs all scripts matching `lint:`

### Environment Variables

```json
{
  "scripts": {
    "build:staging": "cross-env NODE_ENV=staging API_URL=https://staging.api.com vite build",
    "build:prod": "cross-env NODE_ENV=production vite build"
  }
}
```

npm exposes package.json fields as `npm_package_*` (e.g., `npm_package_name`, `npm_package_version`).

## npx and bunx

```bash
npx create-next-app@latest my-app    # run without installing
npx -p typescript tsc --version      # specify package explicitly
npx vitest                           # run local binary from node_modules/.bin
bunx create-next-app@latest my-app   # Bun equivalent (faster)
```

## Dependency Management

```bash
npm install                  # all deps from package.json
npm install lodash           # add production dep
npm install -D typescript    # dev dependency
npm install lodash@4.17.21   # exact version
npm install user/repo        # from GitHub
npm ci                       # clean install from lock file (CI)

npm outdated                 # list outdated packages
npm update                   # update within semver ranges
npx npm-check-updates -u     # update package.json beyond ranges
npm dedupe                   # remove duplicate packages
npm why lodash               # show why a package is installed
npm ls lodash                # find installed versions

npm audit                    # check vulnerabilities
npm audit fix                # auto-fix compatible vulnerabilities
npm audit --omit=dev         # audit production deps only
```

### Overrides and Resolutions

Force a transitive dependency version:

```json
{
  "overrides": { "glob": "^10.0.0" }
}
```

Yarn: `"resolutions": { "glob": "^10.0.0" }`. pnpm: `"pnpm": { "overrides": { "glob": "^10.0.0" } }`.

## Lock Files

```bash
# ALWAYS commit lock files to version control
npm ci                        # deterministic install, fails if lock out of sync
npm ci --ignore-scripts       # skip lifecycle scripts
pnpm install --frozen-lockfile  # pnpm equivalent
yarn install --immutable       # yarn equivalent
```

Regenerate only when resolving deep conflicts or migrating package managers: delete `node_modules` and lock file, then `npm install`.

## .npmrc Configuration

Project-level `.npmrc` (commit this):
```ini
save-exact=true
registry=https://registry.npmjs.org/
@mycompany:registry=https://npm.mycompany.com/
engine-strict=true
```

User-level `~/.npmrc` (never commit):
```ini
//registry.npmjs.org/:_authToken=${NPM_TOKEN}
//npm.mycompany.com/:_authToken=${COMPANY_NPM_TOKEN}
```

## Custom Registry Setup

### Verdaccio (local/private)

```bash
npm install -g verdaccio && verdaccio
npm set registry http://localhost:4873/
npm publish --registry http://localhost:4873/
```

### GitHub Packages

```ini
# .npmrc
@yourorg:registry=https://npm.pkg.github.com/
//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}
```

```json
{ "publishConfig": { "registry": "https://npm.pkg.github.com/" } }
```

## Workspaces (Monorepo)

### Setup

```json
{
  "name": "my-monorepo",
  "private": true,
  "workspaces": ["packages/*", "apps/*"]
}
```

### Workspace Commands

```bash
npm install                              # install all (hoisted to root)
npm run build -w packages/shared         # run in specific workspace
npm run build -w @myorg/shared           # by package name
npm run test --workspaces                # run across all workspaces
npm run build -ws --if-present           # skip workspaces missing the script
npm install zod -w packages/shared       # add dep to workspace
npm install @myorg/shared -w apps/web    # add workspace as dependency
```

### Monorepo Root Scripts

```json
{
  "scripts": {
    "build": "npm run build --workspaces --if-present",
    "test": "npm run test --workspaces --if-present",
    "lint": "npm run lint --workspaces --if-present",
    "dev:web": "npm run dev -w apps/web",
    "dev:api": "npm run dev -w apps/api"
  }
}
```

npm hoists shared deps to root `node_modules`. Conflicts stay in the workspace's own `node_modules`. Use `npm dedupe` if duplication creeps in.

## pnpm

```bash
pnpm install                   # install all
pnpm add lodash                # add dep
pnpm add -D typescript         # dev dep
pnpm dlx create-next-app       # like npx
```

```yaml
# pnpm-workspace.yaml
packages:
  - 'packages/*'
  - 'apps/*'
```

```bash
pnpm -F web run build          # filter by name
pnpm -r run build              # all workspaces
pnpm -r --parallel run dev     # all in parallel
pnpm -F web... run build       # web and its dependencies
```

## yarn

```bash
yarn add lodash                # add dep
yarn add -D typescript         # dev dep
yarn dev                       # run script (no 'run' needed)
yarn dlx create-next-app       # like npx (yarn berry)
yarn workspace web build       # workspace command
yarn workspaces foreach -A run build
```

## Publishing

### Package Setup

```json
{
  "name": "@scope/package",
  "version": "1.0.0",
  "main": "dist/index.js",
  "module": "dist/index.mjs",
  "types": "dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.mjs",
      "require": "./dist/index.js",
      "types": "./dist/index.d.ts"
    }
  },
  "files": ["dist", "README.md", "LICENSE"],
  "publishConfig": { "access": "public" },
  "scripts": { "prepublishOnly": "npm run build && npm test" }
}
```

The `files` field whitelists what goes in the tarball. Prefer `files` over `.npmignore`.

### Publish and Version

```bash
npm publish                     # publish to registry
npm publish --access public     # scoped packages (first time)
npm publish --dry-run           # preview what gets published
npm pack --dry-run              # list files that would be included
npm publish --provenance        # with build provenance (CI only)

npm version patch               # 1.0.0 -> 1.0.1
npm version minor               # 1.0.0 -> 1.1.0
npm version major               # 1.0.0 -> 2.0.0
npm version prerelease --preid=beta  # 1.0.0 -> 1.0.1-beta.0
```

`npm version` auto-updates package.json, creates a git commit, and tags it. Hook into the flow:

```json
{
  "scripts": {
    "preversion": "npm test",
    "version": "npm run build && git add -A",
    "postversion": "git push && git push --tags && npm publish"
  }
}
```

## Debugging Scripts

```bash
npm run build --verbose          # see exact command
npm run build --silent           # suppress npm output, show only script output
npm run                          # list all available scripts
node --inspect-brk dist/index.js # debugger, break on first line
NODE_OPTIONS='--inspect' npm run dev  # attach inspector to any script
DEBUG=express:* npm run dev      # debug logging (common pattern)
NODE_DEBUG=module node dist/index.js  # debug module resolution
```

## Security

```bash
npm audit                        # check known vulnerabilities
npm audit --audit-level=high     # fail only on high/critical
npm audit signatures             # verify package signatures
npm ci                           # verifies lock file integrity checksums
npm publish --provenance         # build provenance (GitHub Actions)
npx @socketsecurity/cli report   # supply chain security report
```

Best practices:
- Run `npm audit` in CI pipelines
- Use `npm ci` (not `npm install`) in CI for reproducible builds
- Set `save-exact=true` in `.npmrc` for critical dependencies
- Use `npm publish --provenance` for public packages
- Never store auth tokens in committed `.npmrc` -- use environment variables

## Quick Reference

```bash
npm init -y                    # create package.json
npm cache clean --force        # clear cache
npm config list                # show config
npm exec -- eslint .           # run local binary
npm link                       # symlink package for local dev
npm repo                       # open repo in browser
npm docs lodash                # open package docs
npm view lodash versions       # list published versions
```

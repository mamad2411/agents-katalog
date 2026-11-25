# Trip Bundle Monorepo - Cursor Rules

## Yarn Workspace Commands

**ALWAYS** use yarn workspace commands when running package-specific scripts in this monorepo.

### Command Format
```bash
yarn workspace ${packageName} ${commandName}
```

### Examples
- `yarn workspace trip-bundle-pwa dev-mock` (DEFAULT - uses mock data, saves API costs)
- `yarn workspace trip-bundle-pwa dev` (ONLY when testing real OpenAI API - costs money!)
- `yarn workspace trip-bundle-pwa build`
- `yarn workspace trip-bundle-pwa test`
- `yarn workspace trip-bundle-pwa lint`

### Available Packages
- `trip-bundle-pwa` - Progressive Web App for trip planning

### Root-level Commands
Use these from the repository root for operations across all workspaces:
- `yarn dev-mock` - Start development with mock data (DEFAULT - saves API costs)
- `yarn dev` - Start development with real APIs (ONLY when needed - costs money!)
- `yarn build` - Build all packages
- `yarn test` - Run tests for all packages
- `yarn lint` - Lint all packages

### Why This Approach?
- ✅ Maintains proper dependency resolution
- ✅ Ensures consistent environment across packages
- ✅ Leverages yarn workspace benefits (hoisting, linking)
- ✅ Avoids potential path and dependency issues
- ✅ Works from any directory in the monorepo

### Package Management
- Use `yarn add <package>` in workspace root for shared dependencies
- Use `yarn workspace ${packageName} add <package>` for package-specific dependencies
- Use `yarn workspace ${packageName} add -D <package>` for dev dependencies

## Development Workflow

1. **Install dependencies**: `yarn install` (from root)
2. **Start development**: `yarn workspace trip-bundle-pwa dev-mock` (DEFAULT - uses mock data)
3. **Start with real APIs**: `yarn workspace trip-bundle-pwa dev` (ONLY when needed - costs money!)
4. **Build for production**: `yarn workspace trip-bundle-pwa build`
5. **Run tests**: `yarn workspace trip-bundle-pwa test`

## 💰 API Cost Management

**IMPORTANT: Always use mock mode during development to avoid OpenAI API charges!**

- **Default**: Use `dev-mock` for all development work
- **Real API**: Only use `dev` when specifically testing OpenAI integration
- **Environment**: `VITE_MOCK=true` enables mock mode with 3 sample trip bundles
- **Cost Savings**: Mock mode provides realistic data without API calls

## Code Style & Standards

- Use TypeScript for all new code
- Follow React best practices and hooks patterns
- Implement PWA best practices (offline-first, responsive)
- Use semantic commit messages
- Always test PWA features in multiple browsers

## File Organization

- Keep package-specific code in `packages/${packageName}/`
- Shared utilities and types can go in a future `packages/shared/` package
- Configuration files at root level apply to all packages

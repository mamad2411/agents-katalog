# Lint & Format

Run ESLint and Prettier across the project.

## Purpose

This command checks and fixes code quality and formatting issues using ESLint and Prettier.

## Usage

```
/lint
```

## What this command does

1. **Runs ESLint** to check for code quality issues
2. **Runs Prettier** to check formatting
3. **Auto-fixes** where possible
4. **Reports** remaining issues that need manual attention

## Steps

### 1. Check if tools are installed
```bash
pnpm eslint --version && pnpm prettier --version
```

### 2. Run ESLint with auto-fix
```bash
pnpm eslint . --fix --ext .ts,.tsx,.js,.jsx
```

### 3. Run Prettier
```bash
pnpm prettier --write "src/**/*.{ts,tsx,js,jsx,css,json,md}"
```

### 4. Type check
```bash
pnpm tsc --noEmit
```

## Or use the project script

```bash
./scripts/lint-and-format.sh
```

## Common Issues

- **Missing ESLint config**: Copy `templates/shared/eslint.config.js` to project root
- **Missing Prettier config**: Copy `templates/shared/prettier.config.js` to project root
- **Conflicting rules**: Ensure eslint-config-prettier is installed to disable formatting rules in ESLint

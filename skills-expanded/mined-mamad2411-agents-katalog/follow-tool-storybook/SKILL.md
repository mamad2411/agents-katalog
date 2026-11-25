---
name: follow-tool-storybook
description: Set up and use Storybook for component development and documentation
argument-hint: "[scope]"
related:
  - follow-tool-vite
  - follow-create-plugins
  - follow-tool-vitest
  - follow-test
  - follow-tool-playwright
  - follow-tool-biome
  - run-test

---

## Goal

Set up and use Storybook to develop UI components in isolation with documentation, testing, and addons

## Scope

For frontend projects that want a component library, visual documentation, and interaction testing

- Latest: `storybook@10.6.0` (verified 2026-09-13) — v10: controls/actions/interactions/viewport are core features (no need to install `@storybook/addon-essentials`/`addon-interactions` anymore)

## Execute

### Workflows

| Topic | Workflow |-------|----------| Init, framework detection, `.storybook/` config files | `workflows/setup-storybook/SKILL.md` | `main.ts` addons — docs, a11y, vitest | `workflows/config-addons/SKILL.md` 
### 1. Installation

> Goal: Install Storybook with the CLI

1. Run `bun create storybook@latest` in the project root (or `bunx storybook@latest create` in v10)
2. Pick the framework with `--type` if the CLI doesn't detect it
3. Check the automatically installed dependencies
4. See the CLI commands in 

### 2. Configuration

> Goal: Create the `.storybook` config files

1. Create `.storybook/main.ts` with `framework`, `stories` glob, `addons`
2. Create `.storybook/preview.ts` for global parameters, decorators, styles
3. Create `.storybook/manager.ts` if you want to adjust UI behavior
4. Set `staticDirs` for static assets
5. See the config details in 

### 3. Write Stories

> Goal: Write stories per component variations

1. Create a `.stories.ts` file next to each component
2. Import `Meta` and `StoryObj` from the framework package
3. Export a default `meta` object with `component`
4. Export named stories with `args` for props/state
5. Use decorators for theme providers, data providers

### 4. Setup Addons

> Goal: Install and configure Storybook addons

1. v10: controls, actions, interactions, viewport, backgrounds are core features — don't install `@storybook/addon-essentials`/`@storybook/addon-interactions` (removed in v10)
2. register the remaining addons in `.storybook/main.ts` via the `addons` array
3. Add `@storybook/addon-docs` for auto-docs
4. Add `@storybook/addon-a11y` for accessibility testing
5. Add `@storybook/addon-vitest` for component/interaction testing via Vitest

### 5. Testing Integration

> Goal: Set up testing for components

1. Run `/follow-tool-vitest` to prepare the unit testing environment
2. Use `@storybook/addon-vitest` for component + interaction tests (`play` functions are in core)
3. Set up visual regression with Chromatic or similar tools
4. Run `bun run test-storybook` (`storybook test`) in CI
5. Run `/follow-test` to expand test coverage

### 6. Build and Deploy

> Goal: Build the static Storybook and deploy

1. Run `bunx storybook build` to create the static site
2. Check the output in `storybook-static/`
3. Set up GitHub Actions for build and deploy
4. Deploy to the static host the project uses

## Rules

### 1. Installation

- Use `bun create storybook@latest` for the latest version
- Use `--type` if auto-detect fails
- Use the official framework packages

### 2. Configuration

- Use `.storybook/main.ts` for config
- Use `.storybook/preview.ts` for global rendering
- Set a `stories` glob with full coverage

### 3. Stories

- Use `.stories.ts` for TypeScript
- Use `args` for component props
- Write stories for every important state

### 4. Testing

- Test interactions in Storybook
- Use visual regression testing
- Run the tests in CI

### 5. Documentation

- Use auto-docs to generate documentation from stories
- Use decorators for context providers
- Keep components in isolation

- Use /follow-tool-vite if needed
- Use /follow-create-plugins (vite) if needed (tool storybook)
- Use /follow-tool-playwright if needed
- Use /follow-tool-biome if needed

## References

- [CLI reference](references/cli.md)

- Use /deep-test visual if needed
- Use /run-test if needed


- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Storybook installed and startable
- Components with complete stories
- Addons installed and working
- Tests passing in CI
- The static docs build and deploy works


---
name: follow-tool-template-starter
description: Use templates from the template-starter repository with degit
argument-hint: "[scope]"
related:
  - follow-tool-git
  - follow-tasks
  - follow-lang-typescript
  - follow-tool-vite
---

## Goal

Use templates from the `newkub/template-starter` repository via `degit` or `git clone` to start a project

## Scope

Use for cloning templates from `https://github.com/newkub/template-starter/tree/main/templates` into the current project

- Boundary: use this skill only to clone templates from `newkub/template-starter`; to scaffold a new project from zero use `/follow-create-web` or `/follow-create-cli` per project type; if you need the full git history use `git clone` instead of `degit`
- Latest: `degit@3.10.0` (verified 2026-09-13) — requires Node.js >= 20

## Execute

### 1. Discover Templates

> Goal: Find and pick the right template

1. Run `gh repo view newkub/template-starter` to see the repository
2. Browse the available templates in the `templates/` directory
3. Check each template's README
4. Pick the template matching the wanted stack

### 2. Clone Template

> Goal: Clone the template with degit without git history

1. Use `bunx degit newkub/template-starter/templates/<template-name> <target-dir>`
2. If you want to preserve git history use `git clone` instead — degit is always a tar snapshot, and `--mode=git` is deprecated in v3
3. Use `--files` to clone only the wanted files
4. Use `--force` carefully when the target directory is not empty
5. See degit details in 

### 3. Setup Cloned Template

> Goal: Configure the template after cloning

1. Read the template's `README.md`
2. Run `bun install` to install dependencies
3. Configure environment variables per the template
4. Run setup scripts if present, e.g. `bun run setup`
5. Check the `package.json` scripts

### 4. Verify Template

> Goal: Confirm the template works

1. Run `bun run dev` to start the development server
2. Run `bun run build` to verify the build
3. Run `bun run test` if present
4. Run `bun run lint` if present

### 5. Initialize Git and Customize

> Goal: Turn the template into your own project

1. Delete the template's `.git` — with degit there is none
2. Do `/follow-tool-git` to init the repository
3. Edit the project name, package name, and README
4. Update dependencies if needed

## Rules

### 1. Tool Selection

- Use `bunx degit` as the default for a lightweight clone
- Use `git clone` when you need the full history
- Use `gh repo clone` when working with the GitHub CLI

### 2. Safety

- Verify the template name before cloning
- Back up important files before cloning into a non-empty target
- Use `--force` only when you are sure you want to overwrite

### 3. Validation

- Check `package.json` and the dependencies
- Run `bun run dev`, `bun run build`, `bun run test`
- Read the template's README before setup

### 4. Customization

- Edit the project metadata after cloning
- Remove unnecessary files
- Commit once setup is done

- Use /follow-tasks if needed
- Use /follow-lang-typescript if needed
- Use /follow-tool-vite if needed

## References

- [CLI reference](references/cli.md)


- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- The template is cloned and in use
- Dependencies are fully installed
- The template passes dev, build, and test
- The project is initialized and ready to develop


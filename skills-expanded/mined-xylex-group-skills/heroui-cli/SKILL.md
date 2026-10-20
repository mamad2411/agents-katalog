---
name: heroui-cli
description: >
  Use heroui-cli to initialize HeroUI v3 projects, install/upgrade/uninstall
  @heroui/react and @heroui/styles, list packages, run doctor health checks, dump
  env debug info, and download agent docs via agents-md. Covers Node 22.22+,
  global vs dlx/npx, templates (app, pages, vite, react-router), package managers,
  and HEROUI_ANALYTICS_DISABLED. Keywords: heroui-cli, heroui init, heroui install,
  heroui upgrade, heroui doctor, heroui agents-md, heroui list, heroui env.
  Use when the user runs /heroui-cli.
---

# HeroUI CLI (`heroui-cli`)

Manage HeroUI dependencies and initialize projects. Install, uninstall, or upgrade packages; assess project health; download docs for AI coding agents.

**Source:** https://heroui.com/en/docs/react/getting-started/cli  
**Issues:** https://github.com/heroui-inc/heroui-cli/issues

## Apply the Skill

- Read `references/cli.md` for full option tables, sample outputs, and `agents-md` behavior.
- Prefer this skill for **CLI operations** (init, install, upgrade, doctor, agents-md).
- After `init`, use `heroui-frameworks` for Next/Vite wiring patterns and `heroui-react` for Tailwind/styles setup details.
- For design policy and semantic variants, use `heroui-design-principles`.

## Requirements

- **Node.js 22.22.0 or later**

## Invocation

### Global install

```bash
npm install heroui-cli@latest -g
heroui
```

### One-shot (no global install)

| Package manager | Command |
|-----------------|---------|
| pnpm | `pnpm dlx heroui-cli@latest` |
| npm | `npx heroui-cli@latest` |
| yarn | `yarn dlx heroui-cli@latest` |
| bun | `bunx heroui-cli@latest` |

Prefer `heroui-cli@latest` so agents do not pin stale majors.

### Global flags

| Flag | Meaning |
|------|---------|
| `-v, --version` | CLI version |
| `--no-cache` | Disable cache (default cache: 30m after first request) |
| `-d, --debug` | Debug mode — **does not install dependencies** |
| `-h, --help` | Help |

## Commands (quick map)

| Command | Purpose |
|---------|---------|
| `init [projectName]` | New project from template |
| `install` | Add `@heroui/react` + `@heroui/styles` (+ peers) |
| `upgrade` | Upgrade those packages to latest |
| `uninstall` | Remove HeroUI packages (peers kept) |
| `list` | Show installed HeroUI packages |
| `doctor` | Health check packages + peer requirements |
| `env` | Local environment + package debug dump |
| `agents-md` | Download docs index into AGENTS.md / CLAUDE.md |

Most package commands accept `-p --packagePath <path>` for a non-default `package.json`.

## Work in This Order

### New project

1. `heroui init` (or `npx heroui-cli@latest init`)
2. Pick template: **app** | **pages** | **vite** | **react-router**
3. Pick package manager: npm | yarn | pnpm | bun
4. `cd <project>` → install deps → `npm run dev` (or pm equivalent)

Non-interactive init options:

```bash
heroui init -t app -p pnpm my-heroui-app
# -t --template: app | pages | vite | react-router
# -p --package: package manager
```

### Existing project (add HeroUI)

1. `heroui doctor` — see what is missing
2. `heroui install` — install packages + peers if needed
3. Wire styles/framework (see `heroui-react` / `heroui-frameworks`)
4. `heroui list` to confirm versions

### Maintenance

```bash
heroui upgrade    # bump @heroui/react + @heroui/styles
heroui list       # inspect versions
heroui uninstall  # remove HeroUI packages only (not peers)
heroui env        # OS/Node + package snapshot for bug reports
```

### Agent docs for a repo

```bash
heroui agents-md --react --output AGENTS.md
heroui agents-md --native --output CLAUDE.md
heroui agents-md --migration --output AGENTS.md
# interactive: heroui agents-md
```

Only **one** of `--react` | `--native` | `--migration` per run.

## Decision Rules

### Which command?

| User intent | Command |
|-------------|---------|
| Scaffold new HeroUI app | `init` |
| Add HeroUI to existing app | `install` then doctor |
| Something broken / peers missing | `doctor` |
| Bump packages | `upgrade` |
| Remove HeroUI | `uninstall` |
| Feed Claude/Cursor/Grok docs | `agents-md` |
| Bug report context | `env` + `list` |

### Templates (`init`)

| Template | Stack |
|----------|--------|
| **App** | Next.js 16 App Router + HeroUI v3 + Tailwind |
| **Pages** | Next.js 16 Pages Router + HeroUI v3 + Tailwind |
| **Vite** | Vite + HeroUI v3 + Tailwind |
| **React Router** | React Router + HeroUI v3 + Tailwind |

### Install vs upgrade vs uninstall

- **install** — no-op if already installed; installs peers as needed
- **upgrade** — latest versions of `@heroui/react` and `@heroui/styles` (+ peers)
- **uninstall** — removes HeroUI packages only; **does not** remove peer deps (react, tailwind, …)

### Debug / CI notes

- `-d --debug` skips dependency installation — use for dry inspection, not full setup
- `--no-cache` when package metadata looks stale
- Opt out of `agents-md` analytics: `HEROUI_ANALYTICS_DISABLED=1`

## agents-md mechanics

1. Git sparse-checkout of docs from HeroUI `v3` branch
2. Builds a compact index of docs/demos
3. Injects between markers in the target file, e.g.  
   `<!-- HEROUI-REACT-AGENTS-MD-START -->` … `<!-- HEROUI-REACT-AGENTS-MD-END -->`  
   (similar markers for Native and Migration)
4. Adds `.heroui-docs/` to `.gitignore`
5. `--ssh` uses SSH instead of HTTPS for clone

More detail: https://heroui.com/docs/react/getting-started/agents-md

## Anti-Patterns

- Running CLI with Node &lt; 22.22.0
- Using global `heroui` without `@latest` when docs/API may have moved
- Expecting `uninstall` to remove react/tailwind peers
- Passing multiple of `--react` / `--native` / `--migration` together
- Treating `doctor` as a substitute for reading framework/theme docs after install
- Committing `.heroui-docs/` if gitignore step was skipped

## Reference Map

- Full command reference + sample output: `references/cli.md`
- Official docs: https://heroui.com/en/docs/react/getting-started/cli
- Raw MDX: https://raw.githubusercontent.com/heroui-inc/heroui/refs/heads/v3/apps/docs/content/docs/en/react/getting-started/(overview)/cli.mdx
- CLI issues: https://github.com/heroui-inc/heroui-cli/issues
- Sibling skills: `heroui-frameworks`, `heroui-react`, `heroui-design-principles`, `heroui-migration`

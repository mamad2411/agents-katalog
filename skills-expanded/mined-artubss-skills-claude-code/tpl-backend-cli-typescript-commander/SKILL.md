---
name: tpl-backend-cli-typescript-commander
description: Template do pack (backend/11-cli-typescript-commander.md). Orienta o agente em APIs, servicos e arquitetura backend alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: backend/11-cli-typescript-commander.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: CLI Tool — TypeScript + Commander.js

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `backend/11-cli-typescript-commander.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **Runtime:** Node.js 22 LTS
- **Language:** TypeScript 5.x (strict)
- **CLI Framework:** Commander.js v12
- **Prompts:** Inquirer.js v9 (ESM)
- **Styling:** chalk v5 + ora (spinners)
- **File ops:** fs-extra v11
- **Config:** cosmiconfig v9 (~/.appname)
- **Testing:** Vitest + memfs (virtual FS)
- **Distribution:** npm publish (ESM + CJS dual build)

---

## PROJECT STRUCTURE
```
src/
├── bin/
│   └── cli.ts                # Entry: shebang + program bootstrap
├── commands/
│   ├── init.ts               # init command
│   ├── generate.ts           # generate command
│   └── config.ts             # config get/set commands
├── lib/
│   ├── config-manager.ts     # ~/.appname config read/write
│   ├── file-ops.ts           # fs-extra wrappers
│   ├── logger.ts             # chalk-based logger
│   └── spinner.ts            # ora wrapper
├── prompts/
│   ├── init-prompts.ts
│   └── generate-prompts.ts
└── types.ts                  # CLI options + config types
tests/
├── commands/
│   └── init.test.ts
└── lib/
    └── config-manager.test.ts
package.json
tsconfig.json
tsup.config.ts                # Build config (tsup)
```

---

## ARCHITECTURE RULES
1. **`bin/cli.ts` only bootstraps** — no logic; it imports `program` and calls `program.parse(argv)`.
2. **Each command is a function that takes `program: Command`** — register subcommands via `program.addCommand(...)`.
3. **Config lives in `~/.appname/config.json`** — use `cosmiconfig` for project-level config, XDG dirs for user config.
4. **Never `process.exit()` inside a command handler** — throw a `CLIError`; let the bootstrap handle exit codes.
5. **stdin/stdout/stderr separation** — stdout: machine-readable output; stderr: logs, spinners, errors.
6. **All prompts gated by `--yes` flag** — prompts must be skippable for CI environments.
7. **Dual ESM + CJS build** — use `tsup` with `format: ['esm', 'cjs']`.

---

## COMMAND STRUCTURE

```typescript
// src/bin/cli.ts
#!/usr/bin/env node
import { Command } from 'commander'
import { registerInit }     from '../commands/init.js'
import { registerGenerate } from '../commands/generate.js'
import { registerConfig }   from '../commands/config.js'
import { version }          from '../../package.json' assert { type: 'json' }

const program = new Command()
  .name('mytool')
  .description('Production-ready CLI tool')
  .version(version)

registerInit(program)
registerGenerate(program)
registerConfig(program)

program.parseAsync(process.argv).catch((err: Error) => {
  process.stderr.write(`\nError: ${err.message}\n`)
  process.exit(1)
})
```

---

## COMMAND IMPLEMENTATION

```typescript
// src/commands/init.ts
import { Command } from 'commander'
import inquirer    from 'inquirer'
import { logger }  from '../lib/logger.js'
import { spinner } from '../lib/spinner.js'
import { writeConfig } from '../lib/config-manager.js'
import fs from 'fs-extra'
import path from 'node:path'

interface InitOptions {
  name?:   string
  yes:     boolean
  output?: string
}

export function registerInit(program: Command): void {
  program
    .command('init')
    .description('Initialize a new project configuration')
    .option('-n, --name <name>',     'Project name')
    .option('-o, --output <dir>',    'Output directory', '.')
    .option('-y, --yes',             'Skip prompts, use defaults', false)
    .action(async (opts: InitOptions) => {
      const answers = opts.yes
        ? { name: opts.name ?? 'my-project', template: 'default' }
        : await inquirer.prompt([
            { type: 'input',  name: 'name',     message: 'Project name:', default: opts.name ?? 'my-project' },
            { type: 'list',   name: 'template', message: 'Template:',     choices: ['default', 'minimal', 'full'] },
          ])

      const spin = spinner('Initializing project...').start()
      try {
        const outDir = path.resolve(opts.output ?? '.')
        await fs.ensureDir(outDir)
        await writeConfig(outDir, answers)
        spin.succeed(`Project "${answers.name}" initialized`)
        logger.info(`  cd ${path.basename(outDir)} && mytool generate`)
      } catch (err) {
        spin.fail('Initialization failed')
        throw err
      }
    })
}
```

---

## CONFIG FILE HANDLING (~/.appname)

```typescript
// src/lib/config-manager.ts
import os   from 'node:os'
import path from 'node:path'
import fs   from 'fs-extra'
import { cosmiconfigSync } from 'cosmiconfig'

export interface UserConfig {
  apiKey?:     string
  defaultOrg?: string
  telemetry:   boolean
}

const APP_NAME   = 'mytool'
const CONFIG_DIR = path.join(os.homedir(), `.${APP_NAME}`)
const CONFIG_FILE = path.join(CONFIG_DIR, 'config.json')

const DEFAULT_CONFIG: UserConfig = { telemetry: true }

export async function readUserConfig(): Promise<UserConfig> {
  const raw = await fs.readJson(CONFIG_FILE).catch(() => ({}))
  return { ...DEFAULT_CONFIG, ...raw }
}

export async function writeUserConfig(patch: Partial<UserConfig>): Promise<void> {
  await fs.ensureDir(CONFIG_DIR)
  const current = await readUserConfig()
  await fs.writeJson(CONFIG_FILE, { ...current, ...patch }, { spaces: 2 })
}

export async function writeConfig(dir: string, data: unknown): Promise<void> {
  await fs.writeJson(path.join(dir, `.${APP_NAME}rc.json`), data, { spaces: 2 })
}

// Read project-level config (walks up directory tree)
export function readProjectConfig(): ReturnType<typeof cosmiconfigSync> {
  return cosmiconfigSync(APP_NAME).search()
}
```

---

## LOGGER + SPINNER

```typescript
// src/lib/logger.ts
import chalk from 'chalk'

export const logger = {
  info:    (msg: string) => process.stderr.write(`${chalk.cyan('ℹ')}  ${msg}\n`),
  success: (msg: string) => process.stderr.write(`${chalk.green('✔')}  ${msg}\n`),
  warn:    (msg: string) => process.stderr.write(`${chalk.yellow('⚠')}  ${msg}\n`),
  error:   (msg: string) => process.stderr.write(`${chalk.red('✖')}  ${msg}\n`),
  // Machine-readable output to stdout
  output:  (data: unknown) => process.stdout.write(JSON.stringify(data) + '\n'),
}

// src/lib/spinner.ts
import ora from 'ora'
export const spinner = (text: string) => ora({ text, stream: process.stderr })
```

---

## ROUTING TABLE (Command → Action)

| Command | Options | stdin | Action |
|---------|---------|-------|--------|
| `mytool init` | `--name`, `--yes`, `--output` | — | Scaffold project config |
| `mytool generate <type>` | `--dry-run`, `--yes` | — | Generate files from template |
| `mytool config get <key>` | — | — | Print config value to stdout |
| `mytool config set <key> <val>` | — | — | Write to `~/.mytool/config.json` |
| `mytool config list` | `--json` | — | List all config as JSON/table |
| `mytool login` | `--token` | token (if no flag) | Authenticate with API |
| `mytool logout` | — | — | Remove stored credentials |
| `mytool run <script>` | `--watch` | — | Execute project script |
| `mytool publish` | `--dry-run`, `--tag` | — | Build + publish artifact |

---

## QUALITY GATES
- [ ] `tsc --noEmit` — zero errors
- [ ] `--yes` flag skips all `inquirer` prompts (CI-safe)
- [ ] Spinners + logs go to `stderr`; data output goes to `stdout`
- [ ] `vitest run` passes all tests with mocked `fs`
- [ ] `npm pack --dry-run` outputs expected files only
- [ ] `node dist/bin/cli.js --help` renders usage without errors
- [ ] Config file created with correct permissions (0o600 for secrets)
- [ ] No `process.exit()` inside command action handlers

---

## FORBIDDEN
- ❌ `console.log` — use `logger.info` or `logger.output`
- ❌ `process.exit()` inside command handlers — throw errors
- ❌ Synchronous `fs.readFileSync` in async commands
- ❌ Prompts without `--yes` bypass — breaks CI
- ❌ Hardcoded file paths — use `os.homedir()`, `path.resolve()`
- ❌ Mutating `process.argv` directly
- ❌ Shipping `node_modules` in npm package — use `bundledDependencies` carefully
- ❌ Storing API tokens in plain project `.env` files — always `~/.appname/config.json`

---
name: effect-cli
description: Build type-safe CLI applications using Effect CLI module for argument parsing, options, commands, and dependency injection.
---

# Effect CLI (v4)

Build type-safe command-line applications with typed arguments, flags, subcommands, and dependency injection.

Scalar/control constructors are PascalCase; combinators and factories
such as `Command.make`, `Prompt.succeed`, and `Flag.withDefault` retain their names.
`Primitive.Choice` differs from `Param` / `Flag` / `Argument.Literals`.
Sentinels are `Never`; numeric constructors are `Int` / `Finite`, while prompts
use `Prompt.Int` / `Prompt.Number`. Global flags use `GlobalFlag.Action` / `Setting`.
Public primitive/completion tags are `Int`, `Finite`, and (for primitives) `Never`.

`Prompt.Select` / `MultiSelect` may omit `message`; `AutoComplete` requires it.
`KeyValuePair` preserves `=` inside values. YAML config parsing rejects plain
scalars containing colon-whitespace or a trailing colon: quote those values.

## Import Pattern

The CLI APIs are marked `@stability unstable` even at the stable package release.
Baseline: **Effect 4.1.0**. In the Effect source checkout, read
`git show effect@4.1.0:packages/effect/src/cli/<module>.ts`; main may be newer.

```typescript
import { Argument, Command, Flag, Prompt } from 'effect/cli';
```

Platform services and runtime for the entry point:

```typescript
import { NodeRuntime, NodeServices } from '@effect/platform-node';
```

## Positional Arguments (Argument)

Positional arguments are parsed in order. Use `Flag.Boolean` for toggles or `Argument.Literals("name", ["true", "false"])` for positional boolean spellings.

### Constructors

<!-- typecheck -->
```typescript
import { Argument } from 'effect/cli';
import * as Schema from 'effect/Schema';

class MySchema extends Schema.Class<MySchema>('FileSettings')({
	name: Schema.String
}) {}

Argument.String('name'); // string
Argument.Int('count'); // number (integer)
Argument.Finite('ratio'); // finite number
Argument.Date('deadline'); // Date
Argument.File('input'); // file path (string)
Argument.File('input', { mustExist: true }); // file path that must exist
Argument.Directory('dir'); // directory path (string)
Argument.Directory('dir', { mustExist: true }); // directory that must exist
Argument.Path('target'); // any path (string)
Argument.Literals('env', ['dev', 'staging', 'prod']); // constrained string union
Argument.ChoiceWithValue('level', [
	// choice with mapped values
	['debug', 0],
	['info', 1],
	['error', 3]
]);
Argument.Redacted('secret'); // Redacted<string>
Argument.FileText('config'); // reads file content as string
Argument.FileParse('config'); // reads and parses file (auto-detects format)
Argument.FileSchema('config', MySchema); // reads and validates file via Schema
```

### Combinators

<!-- typecheck -->
```typescript
import { Config } from 'effect';
import { Argument, Prompt } from 'effect/cli';
import * as Schema from 'effect/Schema';

// Description for help text
Argument.String('file').pipe(Argument.withDescription('Input file'));

// Default value
Argument.Int('port').pipe(Argument.withDefault(8080));

// Optional (returns Option<T>)
Argument.String('config').pipe(Argument.optional);

// Variadic (returns ReadonlyArray<T>)
Argument.String('files').pipe(Argument.variadic);
Argument.String('files').pipe(Argument.variadic({ min: 1 }));
Argument.String('files').pipe(Argument.variadic({ min: 1, max: 5 }));

// Direct variadic form is also supported
Argument.variadic(Argument.String('files'));
Argument.variadic(Argument.String('files'), { min: 1 });

// Cardinality shortcuts
Argument.String('files').pipe(Argument.atLeast(1));
Argument.String('files').pipe(Argument.atMost(5));
Argument.String('files').pipe(Argument.between(1, 5));

// Transform
Argument.Int('port').pipe(Argument.map((p) => `http://localhost:${p}`));

// Validate with Schema
Argument.String('input').pipe(Argument.withSchema(Schema.NonEmptyString));

// Fallback from env config
Argument.String('repo').pipe(
	Argument.withFallbackConfig(Config.String('REPOSITORY'))
);

// Fallback interactive prompt
Argument.String('name').pipe(
	Argument.withFallbackPrompt(Prompt.String({ message: 'Name' }))
);

// Custom metavar for help text
Argument.Int('port').pipe(Argument.withMetavar('PORT'));

// Filter with error message
Argument.Int('count').pipe(
	Argument.filter(
		(n) => n > 0,
		(n) => `Expected positive, got ${n}`
	)
);
```

## Named Flags (Flag)

Flags are named options with `--name` or `-alias` syntax.

Negative numeric tokens such as `-3`, `-3.70`, `-.5`, and `-1e-3` are values,
not short-option bundles: `--lon -3.70` works with `Flag.Finite('lon')`.
Use `--` to pass trailing operands that otherwise look like options; a lone
`-` is also retained as a value. Numeric lexing does not replace the chosen
primitive's validation.

Short-option bundles split into letters: `-vn=3` means `-v -n=3`, not one
multi-letter flag. Use `--num=3`, not `-num=3`. The token `--=value` is an
operand, not a long option with an empty name.

### Constructors

<!-- typecheck -->
```typescript
import { Flag } from 'effect/cli';
import * as Schema from 'effect/Schema';

class MySchema extends Schema.Class<MySchema>('FileSettings')({
	name: Schema.String
}) {}

Flag.Boolean('verbose'); // required: --verbose / --no-verbose; omission fails
Flag.String('config'); // --config value
Flag.Int('port'); // --port 8080
Flag.Finite('rate'); // --rate 3.14
Flag.Date('since'); // --since 2024-01-01
Flag.File('input'); // --input file.txt
Flag.File('input', { mustExist: true }); // file must exist
Flag.Directory('output'); // --output ./dist
Flag.Path('config-path'); // --config-path /etc/app
Flag.Literals('env', ['dev', 'staging', 'prod']); // --env dev
Flag.ChoiceWithValue('log-level', [
	// choice with mapped values
	['debug', 'Debug' as const],
	['info', 'Info' as const],
	['error', 'Error' as const]
]);
Flag.Redacted('password'); // Redacted<string>
Flag.FileText('config-file'); // reads file content
Flag.FileParse('config'); // reads and parses file (auto-detects format)
Flag.FileSchema('config', MySchema); // reads and validates via Schema
Flag.KeyValuePair('env'); // --env FOO=bar → Record<string, string>
```

### Combinators

<!-- typecheck -->
```typescript
import { Config } from 'effect';
import { Flag, Prompt } from 'effect/cli';
import * as Schema from 'effect/Schema';

const Email = Schema.String.check(Schema.isPattern(/^[^\s@]+@[^\s@]+\.[^\s@]+$/));

// Alias
Flag.Boolean('verbose').pipe(
	Flag.withAlias('v'),
	Flag.withDefault(false)
); // switch semantics: omission is false

// Hidden from help, completions, and typo suggestions, but still parsed
Flag.Boolean('experimental-foo').pipe(
	Flag.withHidden,
	Flag.withDefault(false)
);

// Description
Flag.String('config').pipe(Flag.withDescription('Path to config file'));

// Default value (makes flag optional with fallback)
Flag.Int('port').pipe(Flag.withDefault(3000));

// Optional (returns Option<T>)
Flag.String('token').pipe(Flag.optional);

// Custom metavar for help
Flag.String('db-url').pipe(Flag.withMetavar('URL')); // --db-url URL

// Repetition
Flag.String('tag').pipe(Flag.atLeast(1)); // --tag a --tag b
Flag.String('warning').pipe(Flag.atMost(3));
Flag.String('host').pipe(Flag.between(1, 3));

// Transform
Flag.Int('port').pipe(Flag.map((p) => `http://localhost:${p}`));

// Validate with Schema
Flag.String('email').pipe(Flag.withSchema(Email));

// Filter
Flag.Int('port').pipe(
	Flag.filter(
		(p) => p >= 1 && p <= 65535,
		(p) => `Port ${p} out of range`
	)
);

// Fallback from env config
Flag.Boolean('verbose').pipe(
	Flag.withFallbackConfig(Config.Boolean('VERBOSE'))
);

// Fallback interactive prompt
Flag.String('name').pipe(
	Flag.withFallbackPrompt(Prompt.String({ message: 'Name' }))
);
```

Hidden flags parse normally, but generated help, shell completions, and typo suggestions omit them.

Bare boolean flags are required. `--verbose` produces `true`, `--no-verbose` produces `false`, and omission produces `CliError.MissingOption`. Add `Flag.withDefault(false)` for ordinary opt-in switch behavior, or use `Flag.optional` / a config or prompt fallback when absence has separate meaning.

### Optional values and boolean negation

`Flag.withOptionalValue(rawString)` (also on `Param`) follows GNU inline-only
syntax: `--watch=until-done` / `-w=until-done`. A bare `--watch` validates the
configured raw string through the flag's parser. It never consumes the following
operand or subcommand. This makes the **value** optional, not the flag itself;
add `optional` or a default if omission is allowed.

`Flag.withNegation(name)` replaces the default `no-<name>` spelling;
`Flag.withoutNegation` removes the negated form. Replaced/removed names are
rejected and omitted from completions. These have no effect on non-boolean flags.

<!-- typecheck -->
```typescript
import { Flag } from 'effect/cli';

const watch = Flag.Literals('watch', ['first-failure', 'until-done']).pipe(
	Flag.withAlias('w'),
	Flag.withOptionalValue('first-failure'),
	Flag.optional
);
// --watch => Some('first-failure'); --watch=until-done => Some('until-done')
// absent => None; in `--watch build`, `build` remains an operand/subcommand.

const validate = Flag.Boolean('validate').pipe(
	Flag.withDefault(true),
	Flag.withNegation('skip-validate')
);
const unsafe = Flag.Boolean('unsafe').pipe(
	Flag.withDefault(false),
	Flag.withoutNegation
);
```

### Prompt Defaults and Themes

<!-- typecheck -->
```typescript
import { Effect } from 'effect';
import { Prompt } from 'effect/cli';

Prompt.Int({ message: 'Count', default: 42 });
Prompt.File({ message: 'Pick file', default: '/workspace/config.json' });

// A local override merges over the context theme.
const name = Prompt.String({ message: 'Name', theme: { prefix: '>' } });

// Provide once to theme all prompts in a command or application.
const themed = name.pipe(
	Effect.provideService(Prompt.Theme, Prompt.makeTheme({ tick: '✓' }))
);
```

Integer prompt defaults are editable and Enter submits the default if unchanged. `Prompt.File` resolves/selects the default as the initial path.

Per-prompt appearance is configured with `theme?: Partial<Prompt.Theme>`.
`Prompt.Theme` is a context reference with platform defaults; `Prompt.makeTheme`
builds a complete theme. Local fields override the context theme. Theme fields
include prompt symbols, `passwordMask`, and ANSI color values. The default
prefix is `?`; `theme: { prefix: '' }` omits it.

`Prompt.Theme.colors` controls prompt and wizard styling separately from
`TerminalCapabilities`. By default `makeTheme` enables colors only when stdout
is a TTY and `NO_COLOR` is unset/empty; the context default detects once.
Local overrides merge with the context theme. `colors: false` disables styling,
not cursor/redraw control codes, so it does not make an interactive prompt
suitable for noninteractive input. Constant fallback prompts defer terminal
input acquisition and leave piped stdin untouched when no input is needed.

`autoComplete` and `file` now insert `j`/`k` into filter text. Navigate with arrow
keys (or Ctrl-P/Ctrl-K for up, Ctrl-N for down). Wizard command output redacts
password prompt values. Completion generators preserve quoted/spaced/Unicode
choices across Bash (including 3.2), Fish, and Zsh; let the generator escape
choice values rather than pre-escaping your domain values.
PowerShell completions are available through `--completions powershell` or
`--completions pwsh`.

### Help output and repeated flags

Single-valued flags reject repeated occurrences. Use `Flag.atLeast`, `Flag.atMost`,
or `Flag.between` when multiple values are intended. `CliOutput.Presenter` lets a
host suppress, redirect, or replace built-in help, invocation-error, and version
output. Custom formatters read ancestor shared flags from `HelpDoc.inheritedFlags`,
separate from local `flags`; `commandPath` and `globalFlagsScope` preserve provenance.
`CliOutput.defaultFormatter` accepts `"full"`, `"summary"`, or `"none"` for inherited
and global flag display. `Completions.fromCommand` converts a command tree for
build-time completion generation without running the CLI.

### Terminal output capabilities

`TerminalCapabilities.TerminalCapabilities` is a context reference. Its default
detects process capabilities on first read; `TerminalCapabilities.layer` instead
reads `ConfigProvider` and `Stdio`. Built-in help/version/error colors follow
`canColor` unless an explicit `CliOutput.Formatter` is provided.

- `TERM=dumb` disables color, animation, and prompting.
- Nonempty `NO_COLOR` wins over `FORCE_COLOR`. Nonempty `FORCE_COLOR` forces
  colors off-TTY except `0` / case-insensitive `false` (which mean not forcing,
  not disabling TTY color). Empty variables count as unset.
- `canAnimate` needs stdout TTY; `canPrompt` needs stdin and stdout TTY. These
  control application behavior. `Flag.withFallbackPrompt` and
  `Argument.withFallbackPrompt` skip prompts when `canPrompt` is false and fail
  with the original missing-option/argument error.
- Provider faults become defects; the detection layer has no typed failure.

<!-- typecheck -->
```typescript
import { Effect } from 'effect';
import { CliOutput, TerminalCapabilities } from 'effect/cli';

const plain = Effect.gen(function* () {
	return (yield* TerminalCapabilities.TerminalCapabilities).canColor;
}).pipe(Effect.provideService(TerminalCapabilities.TerminalCapabilities, {
	canColor: false, canAnimate: false, canPrompt: false
}));

CliOutput.displayWidth('ファイル'); // 8 terminal cells, not string.length
CliOutput.displayWidth('1️⃣'); // 2
```

Use `CliOutput.displayWidth` for terminal-cell layout: it strips ANSI styles,
measures graphemes, and treats fullwidth/emoji presentation as two cells.

## Commands

### Creating Commands

`Command.make` accepts a name, optional config object, and optional handler:

<!-- typecheck -->
```typescript
import { Console, Effect } from 'effect';
import { Argument, Command, Flag } from 'effect/cli';

// Simple command (no config, no handler)
const version = Command.make('version');

// Command with config (no handler yet)
const deploy = Command.make('deploy', {
	env: Flag.String('env'),
	force: Flag.Boolean('force').pipe(Flag.withDefault(false)),
	files: Argument.String('files').pipe(Argument.variadic)
});

// Command with config and inline handler
const greet = Command.make(
	'greet',
	{
		name: Argument.String('name').pipe(
			Argument.withDescription('Person to greet')
		),
		times: Flag.Int('times').pipe(Flag.withDefault(1))
	},
	Effect.fn(function* ({ name, times }) {
		for (let i = 0; i < times; i++) {
			yield* Console.log(`Hello, ${name}!`);
		}
	})
);
```

### Handler Pattern

Handlers use `Effect.fn` with a generator that destructures the config:

```typescript
const cmd = Command.make(
	'deploy',
	{
		env: Flag.Literals('env', ['dev', 'staging', 'prod']),
		dryRun: Flag.Boolean('dry-run').pipe(Flag.withDefault(false))
	},
	Effect.fn(function* ({ env, dryRun }) {
		if (dryRun) {
			yield* Console.log(`Would deploy to ${env}`);
		} else {
			yield* Console.log(`Deploying to ${env}...`);
		}
	})
);
```

Alternatively, add a handler later with `Command.withHandler`:

```typescript
const cmd = Command.make('greet', {
	name: Flag.String('name')
}).pipe(Command.withHandler(({ name }) => Console.log(`Hello, ${name}!`)));
```

### Command Metadata

```typescript
Command.make('deploy', config, handler).pipe(
	Command.withDescription('Deploy the application'),
	Command.withShortDescription('Deploy app'), // used in subcommand listings
	Command.withAlias('d'), // alternate name
	Command.unlisted, // omit internal/experimental subcommands from discovery
	Command.withExamples([
		{
			command: 'myapp deploy --env prod',
			description: 'Deploy to production'
		},
		{ command: 'myapp deploy --env dev --dry-run', description: 'Dry run' }
	])
);
```

`Command.unlisted` keeps a subcommand invocable by exact name while omitting it from parent help output, shell completions, and "did you mean?" suggestions. In Effect v4, this replaces `Command.withHidden`; the command metadata property is `unlisted`. `Flag.withHidden` remains the correct combinator for flags.

Use a `withExamples` callback for commands mounted under different parents.
Help supplies the actual `commandPath`; the command's `.examples` property
resolves the callback using only its own name as the path.

<!-- typecheck -->
```typescript
import * as Arr from 'effect/Array';
import { Command } from 'effect/cli';

const deploy = Command.make('deploy').pipe(
	Command.withExamples(({ commandPath }) => [{
		command: `${Arr.join(commandPath, ' ')} --yes`,
		description: 'Take every default'
	}])
);
// deploy.examples[0]?.command === 'deploy --yes'
```

### Cross-field validation

`Command.validate` runs after parsing, defaults, and fallback prompts, before
handlers. Return `Effect<void, CliError.CliError, Command.Environment>`; use
`CliError.ValidationError` for expected cross-field rejection. Validations run
in composition order and stop at the first failure; `withHandler` retains them.
Place validation **after** `withSharedFlags` / `withSubcommands` when it must
cover those compositions. Parent validation then runs for selected subcommands
with the parent's shared flags. Do not rely on it for transactional business rules.

<!-- typecheck -->
```typescript
import { Effect } from 'effect';
import { CliError, Command, Flag } from 'effect/cli';

const download = Command.make('download', {
	useApi: Flag.Boolean('use-api').pipe(Flag.withDefault(false)),
	useDocker: Flag.Boolean('use-docker').pipe(Flag.withDefault(false))
}, () => Effect.void).pipe(
	Command.validate(({ useApi, useDocker }) => useApi && useDocker
		? Effect.fail(new CliError.ValidationError({
			message: '--use-api and --use-docker are mutually exclusive'
		}))
		: Effect.void)
);
```

### Nested Config

Config objects can be nested for organization:

```typescript
const deploy = Command.make('deploy', {
	environment: Flag.String('env'),
	server: {
		host: Flag.String('host').pipe(Flag.withDefault('localhost')),
		port: Flag.Int('port').pipe(Flag.withDefault(3000))
	},
	files: Argument.String('files').pipe(Argument.variadic)
});
// Handler receives: { environment: string, server: { host: string, port: number }, files: ReadonlyArray<string> }
```

## Subcommands

### Basic Subcommands

```typescript
const app = Command.make('app');

const init = Command.make(
	'init',
	{},
	Effect.fn(function* () {
		yield* Console.log('Initializing...');
	})
);

const build = Command.make(
	'build',
	{
		target: Flag.Literals('target', ['web', 'node'])
	},
	Effect.fn(function* ({ target }) {
		yield* Console.log(`Building for ${target}`);
	})
);

app.pipe(
	Command.withSubcommands([init, build]),
	Command.run({ version: '1.0.0' }),
	Effect.provide(NodeServices.layer),
	NodeRuntime.runMain
);
// Usage: app init | app build --target web
```

### Shared Parent Flags

Use `Command.withSharedFlags` to define flags on a parent that are available to all subcommands. Subcommands access parent config by yielding the parent command:

```typescript
const tasks = Command.make('tasks').pipe(
	Command.withSharedFlags({
		workspace: Flag.String('workspace').pipe(
			Flag.withAlias('w'),
			Flag.withDefault('personal')
		),
		verbose: Flag.Boolean('verbose').pipe(
			Flag.withAlias('v'),
			Flag.withDefault(false)
		)
	})
);

const create = Command.make(
	'create',
	{
		title: Argument.String('title'),
		priority: Flag.Literals('priority', ['low', 'normal', 'high']).pipe(
			Flag.withDefault('normal')
		)
	},
	Effect.fn(function* ({ title, priority }) {
		// Access parent config by yielding the parent command
		const root = yield* tasks;
		if (root.verbose) {
			yield* Console.log(`workspace=${root.workspace} action=create`);
		}
		yield* Console.log(
			`Created "${title}" in ${root.workspace} with ${priority} priority`
		);
	})
).pipe(
	Command.withDescription('Create a task'),
	Command.withExamples([
		{
			command: 'tasks create "Ship 4.0" --priority high',
			description: 'Create a high-priority task'
		}
	])
);

const list = Command.make(
	'list',
	{
		status: Flag.Literals('status', ['open', 'done', 'all']).pipe(
			Flag.withDefault('open')
		),
		json: Flag.Boolean('json').pipe(Flag.withDefault(false))
	},
	Effect.fn(function* ({ status, json }) {
		const root = yield* tasks;
		if (json) {
			yield* Console.log(
				JSON.stringify({ workspace: root.workspace, status }, null, 2)
			);
		} else {
			yield* Console.log(`Listing ${status} tasks in ${root.workspace}`);
		}
	})
).pipe(Command.withDescription('List tasks'), Command.withAlias('ls'));

tasks.pipe(
	Command.withSubcommands([create, list]),
	Command.run({ version: '1.0.0' }),
	Effect.provide(NodeServices.layer),
	NodeRuntime.runMain
);
// Usage: tasks --workspace team-a list --status open
// Usage: tasks create "Ship 4.0" --priority high
// Usage: tasks ls --json
```

### Grouped Subcommands

```typescript
app.pipe(
	Command.withSubcommands([
		init,
		{ group: 'Development', commands: [build, test] },
		{ group: 'Deployment', commands: [deploy, rollback] }
	])
);
```

## Dependency Injection

### Provide a Layer

```typescript
const deploy = Command.make(
	'deploy',
	{
		env: Flag.String('env')
	},
	Effect.fn(function* ({ env }) {
		const fs = yield* FileSystem.FileSystem;
		// ...
	})
).pipe(Command.provide(FileSystemLive));

// Layer can depend on parsed input
Command.provide((config) =>
	config.env === 'local' ? LocalFsLayer : RemoteFsLayer
);
```

### Provide a Service

```typescript
Command.provideSync(MyService, makeMyService());
Command.provideEffect(MyService, Effect.succeed(makeMyService()));

// Can depend on parsed input
Command.provideSync(MyService, (config) => makeMyService(config.env));
```

## Running Commands

`Command.run` is a **pipeable combinator** that reads args from `Stdio`. The resulting effect requires `FileSystem`, `Path`, `Terminal`, `Stdio`, and `ChildProcessSpawner`; provide platform services and execute with the runtime:

<!-- typecheck -->
```typescript
import { BunRuntime, BunServices } from '@effect/platform-bun';
import { Console, Effect } from 'effect';
import { Command, Flag } from 'effect/cli';

const myCommand = Command.make(
	'myapp',
	{
		name: Flag.String('name')
	},
	Effect.fn(function* ({ name }) {
		yield* Console.log(`Hello, ${name}!`);
	})
);

// Entry point pattern
myCommand.pipe(
	Command.run({ version: '1.0.0' }),
	Effect.provide(BunServices.layer),
	BunRuntime.runMain
);
```

For Node, replace `BunServices` / `BunRuntime` with `NodeServices` /
`NodeRuntime` from the matching `@effect/platform-node` release.

Auto-generates `--help` and `--version` flags.

Built-in/global flags (`--help`, `--version`, `--completions`, `--log-level`, plus custom globals from `Command.withGlobalFlags`) are parsed for the active command path. A local flag on the selected command can intentionally reuse/override a global flag name or alias. Shared parent flags from `Command.withSharedFlags` remain command context and may be accepted before or after a subcommand.

### Testing with Explicit Args

Use `Command.runWith` to pass args directly (useful in tests):

```typescript
const run = Command.runWith(myCommand, { version: '1.0.0' });
// run(["--name", "Alice"]) => Effect<void, ...>
```

## Key Patterns

1. **`Argument` = positional, `Flag` = named** — Use `Flag.Boolean` for toggles, and add `Flag.withDefault(false)` when omission should mean `false`
2. **Handlers use `Effect.fn`** — `Effect.fn(function*({ ...config }) { ... })`
3. **Parent access via yield** — `const root = yield* parentCommand` inside subcommand handlers
4. **Shared flags** — `Command.withSharedFlags` on parent; only flags allowed (no arguments)
5. **Pipeable `Command.run`** — `command.pipe(Command.run({version}), Effect.provide(NodeServices.layer), NodeRuntime.runMain)`
6. **Platform services required** — `Command.run` requires `FileSystem`, `Path`, `Terminal`, `Stdio`, and `ChildProcessSpawner`; provide via `NodeServices.layer` / `BunServices.layer`
7. **All combinators are dual** — Work both as `pipe(Flag.withAlias("v"))` and `Flag.withAlias(flag, "v")`

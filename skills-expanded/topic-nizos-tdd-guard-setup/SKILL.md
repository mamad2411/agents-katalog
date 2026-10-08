---
description: Set up or update TDD Guard for the current project. Detects the test framework, installs or updates the matching reporter, and configures or migrates its configuration to match the current specification.
disable-model-invocation: true
allowed-tools: [Read, Glob, Grep]
---

# TDD Guard Setup

Set up TDD Guard for the current project. Your goal is to:

1. Identify the test framework(s) used in this project
2. Install the matching TDD Guard reporter, or update it if already present
3. Configure the reporter, or migrate an existing configuration to match the current specification

## Reporter packages

| Framework | Reporter package                                         | Registry   |
| --------- | -------------------------------------------------------- | ---------- |
| Vitest    | tdd-guard-vitest                                         | npm        |
| Jest      | tdd-guard-jest                                           | npm        |
| Storybook | tdd-guard-storybook                                      | npm        |
| pytest    | tdd-guard-pytest                                         | PyPI       |
| PHPUnit   | tdd-guard/phpunit                                        | Packagist  |
| Go        | github.com/nizos/tdd-guard/reporters/go/cmd/tdd-guard-go | go install |
| Rust      | tdd-guard-rust                                           | crates.io  |
| RSpec     | tdd-guard-rspec                                          | RubyGems   |
| Minitest  | tdd-guard-minitest                                       | RubyGems   |

## Reporter configuration

All reporters write test results to `.claude/tdd-guard/data/test.json` relative to the project root.

**Vitest** — Add the reporter entry to the `reporters` array with `projectRoot` in the options object.

```typescript
reporters: [
  'default',
  ['tdd-guard-vitest', { projectRoot: '/absolute/path/to/project' }],
]
```

**Jest** — Add reporter entry to the `reporters` array with `projectRoot` option.

```typescript
reporters: [
  'default',
  ['tdd-guard-jest', { projectRoot: '/absolute/path/to/project' }],
]
```

**Storybook** — Construct `StorybookReporter` in `.storybook/test-runner.ts` and wire it into the `postVisit` hook.

```typescript
// .storybook/test-runner.ts
import { StorybookReporter } from 'tdd-guard-storybook'

const reporter = new StorybookReporter({
  projectRoot: '/absolute/path/to/project',
})

module.exports = {
  async postVisit(page, context) {
    await reporter.onStoryResult(context)
  },
}

process.on('exit', () => {
  reporter.onComplete()
})
```

**pytest** — Set `tdd_guard_project_root` in pytest config (`pyproject.toml`, `pytest.ini`, or `setup.cfg`).

```toml
[tool.pytest.ini_options]
tdd_guard_project_root = "/absolute/path/to/project"
```

**PHPUnit** — Add extension (PHPUnit 10+) or listener (PHPUnit 9.x) to `phpunit.xml` with project root path.

```xml
<!-- PHPUnit 10+ -->
<extensions>
    <bootstrap class="TddGuard\PHPUnit\TddGuardExtension">
        <parameter name="projectRoot" value="/absolute/path/to/project"/>
    </bootstrap>
</extensions>

<!-- PHPUnit 9.x -->
<listeners>
    <listener class="TddGuard\PHPUnit\TddGuardListener">
        <arguments>
            <string>/absolute/path/to/project</string>
        </arguments>
    </listener>
</listeners>
```

**Go** — Add a test target using the piped command below. Update an existing Makefile, Taskfile, or similar build system if one exists.

```bash
go test -json ./... 2>&1 | tdd-guard-go -project-root /absolute/path/to/project
```

**Rust** — Add a test target using the piped command below. Update an existing Makefile, Taskfile, or similar build system if one exists.

```bash
cargo nextest run 2>&1 | tdd-guard-rust --project-root /absolute/path/to/project --passthrough
```

**RSpec** — Add the formatter to `.rspec` and set `TDD_GUARD_PROJECT_ROOT` environment variable to the absolute project root path.

```
--format TddGuardRspec::Formatter
```

```bash
export TDD_GUARD_PROJECT_ROOT="/absolute/path/to/project"
```

**Minitest** — Require `tdd_guard_minitest/autorun` from `test/test_helper.rb` (or pass `-rtdd_guard_minitest/autorun` via `Rake::TestTask` ruby_opts) and set `TDD_GUARD_PROJECT_ROOT` to the absolute project root path.

```ruby
# test/test_helper.rb
require "tdd_guard_minitest/autorun"
```

```bash
export TDD_GUARD_PROJECT_ROOT="/absolute/path/to/project"
```

## Guidelines

Your scope is limited to installing, updating, configuring, and migrating a TDD Guard reporter. Do not make changes beyond that.

- **Always use absolute paths** when configuring the project root in reporters.
- **Do not install, update, or modify test frameworks**, build tools, or any other project dependencies. Only install or update the TDD Guard reporter itself.
- **Do not modify existing test configuration** beyond the TDD Guard reporter entry. Migrate any drifted reporter configuration to match the current specification, preserving the user's project root value and leaving unrelated entries untouched. If the existing configuration cannot be migrated without guessing — for example, because it is wrapped in user-defined code or intermingled with custom logic — inform the user and let them decide.
- **If a TDD Guard reporter is already installed and its configuration matches this skill's specification**, inform the user that everything is up to date and stop.
- **If multiple frameworks are detected**, ask the user which to configure.
- **If something goes wrong or is unclear**, inform the user rather than attempting to fix it. Do not install additional packages or make extra changes to resolve issues.

## After setup

Once complete, inform the user of what was done and that:

- TDD Guard validates changes against TDD principles
- They can type `tdd-guard off` / `tdd-guard on` to toggle it mid-session
- They can customize validation rules by editing `.claude/tdd-guard/data/instructions.md`
- More help and configuration options are available at https://github.com/nizos/tdd-guard

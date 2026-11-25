---
name: code-scaffold
description: "Scaffold new production-ready code — Bash scripts, Python tools, Terraform modules, CI jobs, and mixed-language projects — with strict error handling and exit codes, structured logging, input validation and secure defaults, idempotent re-runnable behaviour, a validation pass, and a handoff review checklist. Use this whenever the user asks to write, create, generate, scaffold, bootstrap, or start any new script, tool, module, automation, job, exporter, or service — including casual phrasings like \"write me a script for X\", \"I need something that does Y\", or \"can you put together a module for Z\". Applies even when the user does not say the words \"scaffold\" or \"production\". Do not use it for reviewing, refactoring, or debugging code that already exists."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(shellcheck:*), Bash(shfmt:*), Bash(ruff:*), Bash(pytest:*), Bash(terraform:*), Bash(git:*)
---

# Code Scaffold

Write new code that is ready to run in production on the first try, not example code that needs to be hardened later.

The gap between "code that works on my laptop" and "code that survives a 3am cron run" is almost entirely made of four things: what happens when a command fails, whether anyone can tell what happened afterwards, what happens when the input is wrong, and what happens when the thing runs twice. Every scaffold produced under this skill closes those four gaps by default, because retrofitting them later almost never happens.

## Scope

Use for: new scripts, CLI tools, automation, Terraform modules, CI/CD pipeline jobs, exporters, small services, project bootstraps.

Do not use for: reviewing or refactoring existing code, debugging a failure, explaining a concept, or answering a question about code. Those are different jobs and this skill's structure gets in the way.

## Workflow

### 1. Resolve ambiguity before writing

Ask only about things that would change the shape of the code, and ask them all in one batch. Typical blockers: where it runs (laptop, CI runner, cron, container, Kubernetes Job), how it authenticates, what the failure behaviour should be (fail fast vs. continue and report), and whether it mutates anything.

If nothing is genuinely blocking, write the code and state the assumptions instead of stalling. One clearly-labelled assumption is worth more than three clarifying questions.

### 2. Choose the delivery format

Match the format to the size of the thing, not to a fixed rule:

| Situation | Deliver as |
| --- | --- |
| Single file, roughly under 100 lines | Inline in the reply |
| Single file, larger | A written file |
| Multiple files, or a module/project layout | Written files in a directory |
| User asked for something they'll commit | Written files |

When writing files, put them where the user can retrieve them and list what was created.

### 3. Apply the non-negotiable conventions

These four apply to every language. The per-language reference files show the idioms for each.

**Strict error handling and meaningful exit codes.** Unhandled failures must stop execution rather than silently continuing with bad state. Distinguish exit codes so a caller — a CI job, a cron wrapper, a Kubernetes probe — can react differently to "bad usage" than to "upstream API is down". Reserve `0` for success, `1` for a generic runtime failure, `2` for usage/validation errors, and allocate specific codes above that for conditions a caller might branch on.

**Structured logging and observability hooks.** Logs go to stderr so stdout stays clean for actual output and remains pipeable. Include a timestamp, a level, and enough context to identify which run and which item failed. Support a log-level switch and, where log aggregation is in play, a JSON output mode. For anything long-running or scheduled, expose duration and a success/failure signal that monitoring can consume.

**Input validation and secure defaults.** Validate arguments, environment variables, and config before doing any work — failing after a partial mutation is the expensive failure mode. Never accept secrets as command-line arguments, since they leak into process lists and shell history; read them from environment variables, files, or a secret manager. Never log secret values. Set restrictive file permissions on anything created that holds sensitive data. Set timeouts on every network call.

**Idempotent and safe to re-run.** Assume every script will be run twice, because eventually it will be. Check current state before mutating, make creation operations tolerate existing resources, and clean up temporary files through a trap or context manager rather than at the end of the happy path. Provide a dry-run mode for anything destructive, and require explicit confirmation or a flag for irreversible operations.

**Real values, not placeholders.** Use concrete, working values and defaults. If a value genuinely must be customized for the user's environment, keep it in one clearly marked place near the top and say explicitly what to change and why. Scattered `<YOUR_VALUE_HERE>` markers turn a deliverable back into homework. The exception is when the user explicitly asks for a template.

### 4. Read the relevant reference file

Load only what applies to the task:

- Bash / shell → `references/bash.md`
- Python → `references/python.md`
- Terraform / HCL → `references/terraform.md`

For a language without a reference file, apply the four conventions using that language's idiomatic mechanisms — its standard logging library, its error type, its dependency manifest, its formatter and linter. Do not import patterns from another language.

For a multi-language deliverable, read each relevant file and keep the conventions consistent across them: the same exit code meanings, the same log format, the same flag names.

### 5. Validate before handing it back

Run whatever the environment allows and report the result honestly. Syntax and lint checks catch a real share of scaffolding mistakes and cost seconds:

```bash
bash -n script.sh && shellcheck script.sh
python -m py_compile tool.py && ruff check tool.py
terraform fmt -check && terraform init -backend=false && terraform validate
```

If a tool is not installed, do not silently skip the step — say which check could not run and give the command the user can run themselves. Never claim code was validated when it was not.

Then check the code against the manual review checklist in the handoff section. Fix what fails rather than shipping it with a caveat.

### 6. Hand off

Use this structure. It front-loads the answer and puts the operational detail where it can be skimmed:

```markdown
## What this does
[Two or three sentences. What it does, where it is meant to run.]

## Files
[List with a one-line purpose each. Skip when delivering a single inline file.]

## Code
[The code.]

## How to run
[Exact commands, including a dry-run invocation first if one exists.]

## Validation
[Which checks were run and their results. Which checks could not run, and the commands to run them.]

## Review checklist
[The checklist below, with each item marked.]

## What to customize
[Only the values that genuinely need changing, with the reason for each. Omit this section entirely if there are none.]
```

**Review checklist** — verify each item against the code just written and mark it honestly. An unchecked item with a reason is more useful than a false check:

- [ ] Fails fast on error; no silent continuation past a failed command
- [ ] Exit codes distinguish usage errors from runtime failures
- [ ] Logs go to stderr with timestamp and level; stdout carries only real output
- [ ] All inputs validated before any mutation occurs
- [ ] No secrets in arguments, logs, or committed files
- [ ] Every network call has an explicit timeout
- [ ] Safe to run twice; temporary files cleaned up via trap or context manager
- [ ] Dry-run or confirmation gate present for destructive actions
- [ ] Syntax and lint checks pass, or the gap is stated explicitly
- [ ] No placeholder values left in the code

## Calibration

Production defaults are the baseline, not a ceiling to always exceed. A twenty-line log-rotation helper does not need a plugin architecture, a config file loader, and a test suite — it needs strict mode, validated inputs, a trap, and clear exit codes. Match the structure to the problem.

Scale up when the user asks for tests, a README, or CI wiring, or when the deliverable is a reusable module that other people will consume — a Terraform module or a shared library should ship with usage documentation and input validation regardless of size.

Scale down when the user explicitly asks for something quick or minimal. Honour that, but keep strict mode and input validation, because those cost two lines and prevent the failure modes that produce a support ticket.

## Anti-patterns

These are the specific ways scaffolded code goes wrong. Each one looks harmless in an example and causes an incident in production.

**Chained commands with no failure check.** `cd /some/path && rm -rf ./*` where the `cd` silently fails is the canonical way to delete the wrong directory. Under `set -e` with a checked `cd`, it just exits.

**Catching every exception and continuing.** A bare `except:` or `|| true` that swallows the error converts a loud failure into a silent wrong result, which is far more expensive to diagnose.

**Logging to stdout.** It corrupts piped output and makes the script unusable in a composition.

**Secrets on the command line.** Visible in `ps`, shell history, and CI job logs.

**Network calls with no timeout.** Default timeouts are often infinite; one hung call becomes a stuck cron job that never fires again and never alerts.

**Validating after the first mutation.** Leaves the system in a half-changed state that is harder to recover from than a clean failure.

**Placeholder values.** Code that cannot run as delivered is not a deliverable.

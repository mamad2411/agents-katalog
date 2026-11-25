---
name: ast-aware-js-repo-audit
description: >-
  Run ESLint's parser and rule engine over JavaScript and TypeScript files, then return structured findings with file locations. Use when an agent needs a focused static lint pass or machine-readable diagnostics for changed files, a package, generated code, or a whole repository. Use it during code review, cleanup, or CI triage when you need line-addressable findings. This reports only; it does not fix files, type-check, or run application code.
---

# JavaScript repository audit

Run the skill from this directory or invoke its `scripts/index.js` by absolute path. It uses ESLint's Node API and writes one JSON object to stdout. Errors use one JSON object on stderr and exit code 1.

```sh
node scripts/index.js lint src
node scripts/index.js lint src/index.js test/ --format json
node scripts/index.js lint src --config eslint.config.js
```

## Choose scope and configuration

Pass one or more paths or ESLint globs. Prefer the changed source paths for a small review; use `.` when a repository-wide pass is intended. ESLint applies its normal ignore behavior. Run from the repository root so config discovery and relative paths mean what the project expects.

Without `--config`, this tool disables ambient config discovery and applies a small built-in set of correctness rules: unreachable code, duplicate keys and cases, unsafe negation, constant conditions, `debugger`, suspicious `typeof`, and unused variables. This keeps a no-config run meaningful and predictable. It is not a substitute for a project's own ESLint configuration. Supply `--config <path>` to use the repository's ESLint config; that config owns the rule set. ESLint 9 flat config is expected by the bundled dependency.

TypeScript syntax can be parsed only when a compatible parser is configured. This tool does not install TypeScript parsers or plugins and does not infer types. If a TS path fails parsing, use the project's configured parser or limit the audit to JavaScript.

## Read the result

Successful output has this shape:

```json
{"data":{"targets":["src"],"files":2,"errorCount":1,"warningCount":1,
"findings":[{"file":"/repo/src/app.js","line":4,"column":1,"endLine":4,
"endColumn":8,"severity":2,"ruleId":"no-debugger","message":"Unexpected 'debugger' statement."}]}}
```

`severity` is ESLint's numeric value (`2` error, `1` warning); `ruleId` can be `null` for parser/configuration diagnostics. Location end fields can also be null. `files` counts lint results, including files with no findings. A clean report is not proof of type safety, runtime correctness, security, or that every relevant file was included.

The process exits 0 when lint completes, even if findings have severity 2. Use `errorCount` and `warningCount` to decide whether to block a workflow. Exit 1 means the command or ESLint execution failed, not that lint findings exist.

## Agent workflow

1. Establish the repository root and inspect its ESLint config and package scripts before selecting the default rules or project config.
2. Run the narrowest useful path set. For a user-requested repository audit, use the repository's own config if present.
3. Triage findings by file, line, and rule. Inspect surrounding code before proposing a fix; a lint message is evidence to investigate, not an automatic license to edit.
4. If asked to fix findings, make focused edits and rerun the same command. Say which scope and config were used, and call out skipped TypeScript support or ignored paths.

## Common audit scenarios

- **Reviewing a patch:** identify changed JavaScript paths first and lint only those paths. This keeps the report actionable and avoids presenting old repository debt as newly introduced.
- **Preparing a release:** run against the project config and intended package or repository scope. If the repo has no ESLint config, use the built-in rules as a lightweight screening pass and label it accordingly.
- **Investigating one suspicious file:** pass the file path directly, then inspect nearby code and the rule documentation before deciding whether a finding is a bug, an intentional pattern, or a configuration mismatch.
- **Working in a monorepo:** run from the relevant package root when config discovery should be package-local; pass explicit paths and config when the intended root differs. Do not assume one package's config applies to all.

Treat parser failures and configuration errors separately from rule findings. An empty findings list only describes files ESLint accepted and analyzed under the selected scope, ignores, parser, and rules; it does not establish that the program type-checks, behaves correctly, or is secure.

## Detailed review procedure

### 1. Establish what the audit should answer

Translate the request into a bounded question before choosing paths:

- For a change review, ask whether the edited JavaScript introduces lint findings. Use the changed paths, while including a directly edited shared config if it affects the rules.
- For maintenance, ask which findings exist in a named package or directory. Prefer one package at a time in a monorepo so config ownership stays clear.
- For onboarding or a first pass, audit the repository root and state that the built-in rule set is only a baseline if no project config is supplied.
- For a regression, audit the smallest file set that can demonstrate the issue, then widen scope if the symptom indicates a shared pattern.

If the working tree already contains unrelated edits, preserve them and avoid claiming that a finding is new unless the diff confirms it. Lint output has no baseline comparison built in.

### 2. Select paths and config deliberately

Run from the project root when that is where the intended ESLint configuration and ignore behavior live. Pass explicit paths for a focused review. A glob is interpreted by ESLint; avoid assuming shell expansion and ESLint globbing behave the same when a path contains special characters. If a monorepo package has its own config, run in that package or pass its config path and check the returned target/file list to confirm scope.

Use the project config for project-policy findings. Use the built-in rules only when there is no usable config, or when the caller explicitly wants a stable baseline independent of repository conventions. Do not combine custom config and baseline findings mentally as if they had the same rule coverage.

### 3. Separate execution problems from code findings

- A JSON report with nonzero `errorCount` means lint completed and found severity-2 diagnostics. The process still exits `0` in this case.
- `warningCount` describes severity-1 diagnostics; whether those block work is a project policy decision.
- Exit `1` means the tool or ESLint could not complete: check target paths, configuration loading, parser availability, dependency resolution, and the reported error object before interpreting the audit.
- Parser diagnostics (`ruleId: null`) mean the source was not analyzed under the expected parser. Do not report that file as clean.
- `files` counts analyzed lint results, including clean files. If it is lower than expected, inspect ignored paths and config behavior.

### 4. Triage before editing

Group findings by rule and file, then inspect the surrounding source. Check whether the finding is already present in the base change, whether the code is generated, and whether a project-specific config intentionally suppresses it. Do not silence a rule or change shared configuration just to make one report green unless that change is part of the user's requested outcome. If asked to fix findings, make the smallest behavior-preserving edit, rerun the same paths and config, and summarize any remaining diagnostics.

## Example review report

```text
Scope: src/billing.js and src/routes/checkout.js
Config: eslint.config.js
Analyzed: 2 files; 1 error, 0 warnings
- src/billing.js:18:3 no-debugger — remove the leftover debugger statement.
Limit: TypeScript files were not included; this was static lint only.
```

For machine consumers, retain the JSON output rather than scraping human prose. For a user-facing review, translate each finding into its location and likely impact, and distinguish verified facts from a proposed interpretation.

## CLI

```text
lint <path-or-glob...> [--config <path>] [--format json]
```

Only `json` is accepted for `--format`; it pretty-prints the same JSON shape. Unknown flags, missing targets, and unsupported formats are errors. The skill does not shell out to the `eslint` executable, modify source files, or run project scripts.

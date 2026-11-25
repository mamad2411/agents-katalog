---
name: vibe-script-audit
description: Audit a vibe-coded script or CLI tool (one-shot Python/TypeScript/Bash run locally or as cron) and produce a severity-tagged markdown report. Use when the user wants to security-review a script — "audit my migration script," "review this cron job," "is this CLI safe to run," "audit this bash script." Covers argument handling, subprocess and shell-out (command injection, `shell=True`), file I/O (path traversal, symlinks), credential file hygiene, network TLS, and blast radius, on top of the shared baseline. Runs safe live probes in an isolated tmpdir (path-traversal args, shell metachars, bad credfile) and asks before exercising the main path.
allowed-tools: Read Grep Glob
---

# Vibe-coded script security audit

Audits scripts and CLI tools — one-shot Python/TypeScript/Bash files an operator runs locally
or schedules as cron. Different threat model from web apps: external attack surface is low (the
script isn't on the public internet), but blast radius is high because the script usually runs
as a privileged user (the operator), often with secrets in scope, and touches files / databases
/ third-party APIs directly.

The headline failure modes:

- The script takes arguments and shells out — command injection via argument.
- The script reads a path from an argument and reads/writes without validating it — path
  traversal, symlink races.
- The script reads a credential from a file with overly permissive permissions, or from an
  unencrypted source.
- The script has no `--dry-run` for a destructive action, so a typo destroys data.

## When to use this skill

Use this when the user wants to security-review a script. Examples: a Python migration script,
a Bash deploy script, a Node.js data-pipeline tool, a one-shot CLI that calls an API.

Don't use this for: user-facing web apps (use `vibe-webapp-audit`), webhook handlers / services
(use `vibe-service-audit`), bots (use `vibe-bot-audit`), or MCP servers / AI agents (use
`vibe-mcp-agent-audit`).

## Inputs the skill expects

- A path to a local repo or single script file.
- Optionally, a **safe invocation command** — for live probes, the skill needs to know how to
  invoke the script. The user should provide a command line they consider safe (e.g., `python
migrate.py --help`) so the skill can derive variations from it.

Ask for the safe invocation at the start. If not provided, skip live tests and note this.

## Workflow

```bash
SKILL_DIR="${CLAUDE_SKILL_DIR:-${SKILL_DIR}}"
SHARED_DIR="$SKILL_DIR/../../shared"
# Always reads:
#   $SHARED_DIR/references/baseline.md
#   $SHARED_DIR/references/live-tests-baseline.md
#   $SHARED_DIR/references/report-template.md
# Conditionally:
#   $SKILL_DIR/references/live-tests.md  (if a safe invocation is provided)
```

1. **Detect the language and entry points** (~30s).
2. **Ask for the safe invocation command.**
3. **Run the baseline** (`$SHARED_DIR/references/baseline.md`, checks A–D — for a single script,
   deps and SAST may be thin; record what was checked).
4. **Run the category-specific static checks** (sections 1–6 below).
5. **Run live tests** if a safe invocation was provided. **MANDATORY**: read
   `$SKILL_DIR/references/live-tests.md` in full before running any probe. Do NOT skip the
   sandbox setup at the top of that file. Live tests run in an isolated `mktemp -d` — never
   against real data.
6. **Render the report** using `$SHARED_DIR/references/report-template.md`.

### Detect the script shape

```bash
# Entry points
grep -lE 'if __name__ == .__main__.' --include="*.py" -r . | head -10
find . -maxdepth 3 -name "*.sh" -not -path "*/node_modules/*" | head -10
grep -lE '^#!' . -r 2>/dev/null | head -10

# CLI parsing libraries
grep -hE "(argparse|click|typer|fire)" --include="*.py" -r . | head -5
grep -hE '"(commander|yargs|meow|cac|clipanion)"' package.json 2>/dev/null
```

## 1 — Argument handling

**Before flagging an argument as unsafe, ask yourself**: where does the value flow? An argument
that ends up in `print(arg)` is fine. The same argument flowing into `subprocess` or `open()` is
the actual risk. Trace from `argparse` / `commander` to first use; severity is set by the _sink_,
not the _source_.

**Patterns to flag** (severity from the sink, not the source):

| Pattern                                                                  | Severity     |
| ------------------------------------------------------------------------ | ------------ |
| Argument concatenated into shell command (see §2)                        | **Critical** |
| Argument used as URL the script then executes as code or shells out with | **Critical** |
| Argument-supplied file path without `realpath` + containment             | **High**     |
| No `--help` text on destructive flags                                    | **Low** (UX) |

**Find the surface:**

```bash
grep -rE "add_argument" --include="*.py" . | head -20
grep -rE "@click\.(option|argument)|@app\.command" --include="*.py" . | head -10
grep -rE "\.argument|\.option" --include="*.{ts,js}" . | head -20
grep -nE '\$\{?[0-9@\*]\}?|\$@|\$\*' --include="*.sh" -r . | head -20
```

## 2 — Subprocess and shell-out

**Before flagging a subprocess call, ask yourself**: is the shell involved at all?
`subprocess.run(["cmd", arg])` (list form) is safe even with untrusted args.
`subprocess.run(f"cmd {arg}", shell=True)` is RCE even with "trusted" args. The shell is the
boundary; list-form bypasses it.

**Patterns to flag:**

| Pattern                                               | Severity     |
| ----------------------------------------------------- | ------------ |
| `subprocess.run(..., shell=True)` with any user input | **Critical** |
| `exec()` / `execSync()` with string concatenation     | **Critical** |
| Bash executing user input as code                     | **Critical** |
| Unquoted variables in shell commands (`rm $path`)     | **High**     |

**Safe patterns** (confirm and don't flag):

- `subprocess.run(["cmd", arg1, arg2])` — list form, no shell.
- `execFile(cmd, [arg1, arg2])` in Node — args go via argv, not a shell.

**Find the surface:**

```bash
grep -rnE "subprocess\.(run|call|Popen|check_output)|os\.(system|popen)" --include="*.py" . | head -30
grep -rnE "shell=True" --include="*.py" . | head -20
grep -rnE "(exec|execSync|spawn|spawnSync|child_process)" --include="*.{ts,js}" . | head -20
grep -rnE '[e]val|\$\(' --include="*.sh" . | head -20
```

## 3 — File I/O

**Before flagging a path operation, ask yourself**: is the path _normalized + contained_?
`os.path.realpath(path)` resolves symlinks but doesn't enforce containment — you still need to
check the resolved path is under an allowed root. Normalization alone is half the fix.

**Patterns to flag:**

| Pattern                                                                                  | Severity                 |
| ---------------------------------------------------------------------------------------- | ------------------------ |
| Path constructed by string concatenation of user input (no realpath + containment)       | **High** — traversal     |
| Writes to `/tmp/<predictable-name>` without `mkstemp` / `mktemp`                         | **Medium** — TOCTOU race |
| Follows symlinks when writing to user-controlled paths (no `O_NOFOLLOW` / `lstat` check) | **Medium**               |

**Find the surface:**

```bash
grep -rnE "open\(.*\+|os\.path\.join.*input|join\(.*req" --include="*.py" . | head -20
grep -rnE "(readFile|writeFile|fs\.).*\+.*argv" --include="*.{ts,js}" . | head -20
grep -rnE "(os\.symlink|fs\.symlink|os\.readlink|fs\.lstat|os\.lstat)" \
  --include="*.{ts,js,py}" . | head -10
```

## 4 — Credential file hygiene

**Before flagging a credfile read, ask yourself**: who controls the file's lifecycle? A file the
script _creates_ needs `0600` on write. A file the script _reads_ (operator-supplied) needs a
mode check before reading — fail closed on `world-readable`. Two different obligations from the
same file path.

**Patterns to flag:**

| Pattern                                                              | Severity                   |
| -------------------------------------------------------------------- | -------------------------- |
| Script writes a credfile with mode 0644 / world-readable             | **High**                   |
| Script reads a credfile from arg-supplied path without normalization | **Medium**                 |
| Reads `~/.aws/credentials` etc. without checking owner-only mode     | **Low** — defense-in-depth |

**Find the surface:**

```bash
grep -rnE "(open|read|load).*\.(json|yaml|toml|env|secret|key|pem)" --include="*.{ts,js,py,sh}" .
grep -rnE "os\.environ|process\.env" --include="*.{ts,js,py}" . | head -20
grep -rnE "(stat|st_mode|access\()" --include="*.{ts,js,py}" . | head -10
```

## 5 — Network calls

**Before flagging TLS-disabled, ask yourself**: is this a dev-only escape hatch or a production
code path? A test fixture that hits a local self-signed server with `verify=False` is fine. The
same line in production code is **Critical**. Check whether the call is gated by an env / debug
flag or whether it runs unconditionally.

**Patterns to flag:**

| Pattern                                                                                  | Severity                         |
| ---------------------------------------------------------------------------------------- | -------------------------------- |
| TLS verification disabled in unconditional / production code path                        | **Critical**                     |
| Cleartext HTTP for non-localhost remote, carrying credentials                            | **High**                         |
| TLS verification disabled but gated behind a clearly-named debug env / `--insecure` flag | **Low** (note but don't promote) |

**Find the surface:**

```bash
grep -rnE "(verify=False|rejectUnauthorized: false|InsecureSkipVerify|disable.*tls)" \
  --include="*.{ts,js,py}" . | head -10
grep -rnE "http://(?!localhost|127\.)" --include="*.{ts,js,py}" . | head -10
```

Flag the same patterns as service audit: TLS verification disabled in non-test code path is
**Critical**.

## 6 — Blast radius

**Before flagging a script as missing safety rails, ask yourself**: what's the _worst_ run of
this script that's still a normal use of the script? Not "what if the operator types `rm -rf
/`" — "what if the operator runs it with a typo in a config flag, or twice in a row, or against
the wrong env." A missing `--dry-run` is more serious for a script that nukes data than for one
that prints a report.

Read the script top-to-bottom and identify the "damage actions":

- File deletion / mass file modification.
- Database `DROP`, `TRUNCATE`, mass `UPDATE` / `DELETE` without `WHERE`.
- Sending emails / messages.
- Calls to third-party APIs with side effects (charging cards, deleting accounts).

For each, check:

- Is there a `--dry-run` / `--confirm` flag, default to dry-run? Missing on a destructive
  script: **High**.
- Is there a confirmation prompt (`Are you sure?`) before destructive action? Missing on a
  one-shot script run manually: **Medium**.
- Does the script log what it did, where? Logs should make recovery possible. Missing audit
  trail on a destructive script: **Medium**.

## Producing the report

Read `$SHARED_DIR/references/report-template.md`. Save as
`vibe-script-audit-<YYYY-MM-DD>-<HHMM>.md`. Tell the user the exact path.

## What this skill is NOT

- Not a code review. Logic, structure, ergonomics are out of scope.
- Not a runtime profiler. Performance issues are out of scope.
- Not a privilege-escalation audit of the host. The script is reviewed; the host setup is the
  operator's responsibility.

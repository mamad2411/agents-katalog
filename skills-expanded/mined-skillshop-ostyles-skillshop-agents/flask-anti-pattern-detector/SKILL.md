---
name: flask-anti-pattern-detector
description: "Flask anti-pattern detector: scans Flask projects for hardcoded SECRET_KEY, debug-mode in production, dangerous template rendering (render_template_string), pickle/eval/exec on request data, unsafe session config, SQL injection via raw queries, insecure file upload, and debug toolbar enabled. LLM validates each finding and proposes modern alternatives. Read-only. Audience: Senior. Trigger: /flask-detector"
trigger: /flask-detector
---

## What this is for

Flask's flexibility makes it easy to introduce security anti-patterns:
hardcoded secrets, debug mode in production, unsafe template rendering
that enables SSTI, pickle deserialization of request data, eval/exec on
user input, session manipulation without strict lifetime controls, raw
SQL queries with string interpolation, unvalidated file uploads, and
debug toolbars left enabled. `security-smell-scanner` flags generic
vulnerabilities; this skill inventories every instance per pattern and
classifies severity.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/flask-scan.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output. For each finding:

### Step 5

- **Is this safe?** Evaluate the context: is the hardcoded key in a

### Step 6

dev config only? Is `render_template_string` called with a static

### Step 7

template and user data passed as context (safe) or with user input

### Step 8

concatenated into the template string (SSTI)?

### Step 9

- **What is the modern alternative?** Propose the specific fix:

### Step 10

`os.environ.get('SECRET_KEY')` instead of a literal;

### Step 11

`render_template` instead of `render_template_string` with user

### Step 12

input; `flask-talisman` CSP headers; proper session config with

### Step 13

`PERMANENT_SESSION_LIFETIME`; prepared statements / ORM instead

### Step 14

of raw SQL; `werkzeug.utils.secure_filename` for uploads.

### Step 15

- **Severity scale:** eval/exec > pickle > SSTI > hardcoded secret >

### Step 16

debug-mode > sql-injection > session > unsafe-upload > debug-toolbar.

### Step 17

5. Write `flask-detector-report.md` to the working directory.

## Usage

```
/flask-detector                            # interactive
/flask-detector <dir>                      # scan project
/flask-detector -help                      # show usage
```

Returns JSON with `findings[]`:
`{file, line, patternType, code, severity}` plus summary counts and
`projectIsFlask` boolean.

---
name: agent-skill-kit-security-auditor
description: Audit a skills tree for the four canonical security findings — unauthorized frontmatter fields, command-injection patterns in scripts, unvetted cross-repo dependency origins, and host-path leaks in body or scripts. Use when the user asks to audit, scan, security-check, or harden a skill or skills directory.
tier: org
license: Apache-2.0
compatibility: requires `skills-ref` CLI; reads files only — no network, no exec
---

# Agent Skill Security Auditor

Wraps the `skills-ref audit` CLI. Runs four independent passes and emits severity-graded findings (HIGH / MEDIUM / LOW). Exits non-zero on any HIGH, or on any MEDIUM when `--strict` is passed.

## When to use

- Before merging any change under `.agents/skills/`.
- During CI on every PR touching skills or their `scripts/` dirs.
- After importing skills from a third-party repository.
- During incident response when investigating a suspected supply-chain compromise.

## Invocation

`skills-ref audit <root> [--format json|human] [--strict] [--allowed-origins a,b] [--skip frontmatter|scripts|deps|path-leak]`

## Findings

| Code                              | Severity | Trigger                                                                    |
| --------------------------------- | -------- | -------------------------------------------------------------------------- |
| `A001_UNAUTHORIZED_FIELD`         | MEDIUM   | Top-level frontmatter key not in the spec allowlist.                       |
| `A010_COMMAND_INJECTION_PATTERN`  | HIGH     | `eval(`, `exec(`, `subprocess(...,shell=True)`, `os.system(`, backticks.   |
| `A020_UNVETTED_ORIGIN`            | MED/HIGH | Cross-repo dep owner outside `--allowed-origins` (HIGH when list is set).  |
| `A030_HOST_PATH_LEAK`             | MEDIUM   | `/Users/`, `/home/`, or `/tmp/` literal in body or scripts (with carve-outs for fenced bash/console/text blocks and blockquote lines). |

## Exit codes

| Code | Meaning                                                          |
| ---- | ---------------------------------------------------------------- |
| 0    | No HIGH findings (and no MEDIUM when `--strict` is set).         |
| 1    | At least one HIGH (or any MEDIUM when `--strict`).               |

## Pass-level skipping

`--skip frontmatter,scripts,deps,path-leak` disables individual passes. Useful when one pass has known noise that must be triaged before re-enabling.

## Reference

The auditor is implemented twice — `.agents/skills/agent-skill-kit-commons/packages/mjs/` and `.agents/skills/agent-skill-kit-commons/packages/py/` — and shares one injection-pattern table at `.agents/skills/agent-skill-kit-commons/packages/mjs/assets/injection_patterns.json` (symlinked into py). The fixture suite lives under `.agents/skills/agent-skill-kit-commons/fixtures/audit/`.

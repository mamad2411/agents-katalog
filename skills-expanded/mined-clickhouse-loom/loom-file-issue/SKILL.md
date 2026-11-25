---
name: loom-file-issue
description: Files or updates a Loom GitHub issue — duplicate check, a reproduction with versions, the matching issue form and label, a redacted body. Use when asked to open, file or report an issue, bug, regression or feature request, or to add findings to one. Not for security reports (SECURITY.md).
argument-hint: "<what is wrong or wanted>"
metadata:
  internal: true
---

# Filing a Loom issue

An issue is worth filing when a maintainer can act on it without asking a question back. Every issue goes through one of the forms in `.github/ISSUE_TEMPLATE/` (blank issues are off).

## 1. Is it already tracked?

```bash
gh issue list --repo ClickHouse/loom --state all --search "<two or three distinctive terms>" -L 20
gh pr list --repo ClickHouse/loom --state all --search "<same terms>" -L 10
```

With the Loom plugin connected, also call its `loom_tracker_duplicate_check` tool with the title, body and any stack frames: it matches by meaning, not phrase. A duplicate gets a comment with your new evidence on the existing issue, not a second issue. A fix already on `main` gets no issue; say which commit fixed it.

## 2. Reproduce it

- Reproduce on the latest release or `main`, on a private server (`loom-dev-setup`), before writing. If you could not reproduce it, say so: in "How this was found" where the form has it, otherwise in "Additional context", or in the main field of a form with neither.
- Shrink to the smallest sequence: the ops or SDK calls with their inputs, the non-default `LOOM_*` settings, whether auth is on, the rows it depends on and the latest applied migration (`SELECT max(filename) FROM loom._migrations`).
- Keep the `error.code` and the `X-Request-Id` of the failing response; `loom-debug` follows that id to the cause.
- A regression names the PR that caused it (`loom_code_bisect_candidates` ranks the merged PRs of a good/bad window when the plugin is connected): `Caused by: <full PR URL>`.

## 3. Pick the form

The label column is a label that exists in the repository; a form's own `labels:` that does not exist is dropped silently.

| Form (`.github/ISSUE_TEMPLATE/`) | Label | For |
| --- | --- | --- |
| `30_bug-report.yaml` | `bug` | an op, SDK call, CLI command, worker, migration or hook does the wrong thing |
| `40_recall-quality.yaml` | `bug` | search, ask or a context pack returned a wrong result, missed a memory, or failed to abstain |
| `50_performance-issue.yaml` | `bug` | slower, or reads more from ClickHouse, than expected |
| `60_upgrade-compatibility.yaml` | `bug` | an upgrade broke a client, a migration, a field or a setting |
| `70_installation-issue.yaml` | `bug` | does not install, build, boot or connect |
| `20_feature-request.yaml` | `enhancement` | a workflow Loom should support, starting from the use case |
| `80_documentation-issue.yaml` | `documentation` | a page is wrong, missing or unclear |
| `10_question.yaml` | `question` | how to do something |

## 4. Write the body

`gh issue create` cannot fill a YAML form, so write the body with one `### <label>` heading per form field, in the form's order, using the labels exactly as the form shows them (read the YAML). Fill every required field; drop optional ones you have nothing for.

- **Title**: the wrong behaviour as a fact, under ~80 characters. "`memory.search` drops pinned rows when `limit` is below the pin count", not "Search bug" or "Issue with pinned memories".
- **Environment**: paste `loom report` (it prints versions and `loom doctor`, never secret values).
- **How this was found**: pick the option that is true. An agent that found the problem and has not had a person reproduce it says so; that tells a maintainer how much to trust the reproduction.
- **Redaction**: remove tokens, keys, JWTs, passwords, customer data, host names, internal paths and namespaces from logs before pasting, then, in a form with a Redaction field (bug, recall quality, performance, upgrade, installation), end the body with its required checkbox: `### Redaction` and `- [x] I removed tokens, keys, passwords and personal or customer data from everything above.`
- Write in the voice of `loom-writing` and run its checker on the body file.

```bash
python3 .claude/skills/loom-writing/scripts/check_prose.py /path/to/issue.md
gh issue create --repo ClickHouse/loom --title "<title>" --label "<label from the table>" --body-file /path/to/issue.md   # without triage rights: drop --label
```

Creating an issue is public: show the title and body to the requester and file only after they agree, unless they asked you to file it outright.

## 5. After filing

- Link it where it belongs: `Closes: <issue URL>` in the PR that fixes it, `Related:` from other issues.
- New evidence goes in a comment on the issue (`gh issue comment <n> --body-file …`), not an edit that rewrites what others have already read.
- Close only issues you opened, and only with the reason: the fixing PR, or why it is not a bug.

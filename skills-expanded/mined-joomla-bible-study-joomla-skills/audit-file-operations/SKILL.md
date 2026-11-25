---
name: audit-file-operations
description: Audit attacker-influenced filesystem paths and archive entries in Joomla extensions for traversal, Zip Slip, symlink escape, and arbitrary read/write/delete. Use when reviewing file reads, downloads, writes, deletes, includes, or archive extraction in a Joomla extension, or when explicitly invoked for a filesystem audit. File type acceptance and initial upload storage belong to audit-controller-exposure.
---

# Audit Joomla filesystem operations

Audit distributed extension code for attacker-influenced paths reaching filesystem operations outside
the intended root, or with unintended semantics.

## Boundaries

This audit owns reads, downloads, writes, moves, copies, renames, deletes, includes, directory
operations, stream wrappers, symlink handling, and archive extraction.

- **File type acceptance and the initial storage of HTTP uploads** belong to
  `audit-controller-exposure`. Keep tracing an uploaded name into later filesystem operations — that
  is this audit's ground — but cross-reference rather than duplicating the upload finding.
- Authentication and authorisation of the calling task belong to `audit-authz` and
  `audit-controller-exposure`.
- Remote HTTP requests belong to `audit-ssrf-redirects`; command execution and dynamic PHP inclusion
  as an execution sink belong to `audit-code-execution`.

## What to trace

Treat request values, headers, form arrays, database content, extension parameters, remote metadata,
uploaded names, and **archive entry names** as potential sources.

Inspect native PHP filesystem functions, Joomla's `\Joomla\Filesystem\File` / `Folder` / `Path`
helpers, download and preview endpoints, dynamic `include`/`require`, template and layout selection,
log and export paths, cleanup jobs, install scripts, and archive libraries.

For each path verify, as applicable:

- it is resolved against an **explicit allowed root**, canonicalised, and checked with a
  boundary-aware comparison — not a string prefix, which `/var/www/uploads-evil` satisfies against a
  `/var/www/uploads` root;
- absolute paths, parent traversal, NUL bytes, alternate separators, stream-wrapper schemes
  (`php://`, `phar://`, `zip://`), and encoded or double-decoded traversal cannot change the target;
- existing symlinks and symlinked parents cannot escape the allowed root, **including between the
  check and the write or delete** (TOCTOU);
- allow-listed logical identifiers are mapped to server-selected paths, not concatenated into one;
- archive entries cannot escape the extraction directory (**Zip Slip**), create unsafe links,
  overwrite sensitive files, or expand without limits;
- downloads cannot disclose arbitrary local files, and cleanup or deletion cannot target unrelated
  data.

### A Joomla trap worth stating plainly

Joomla's `PATH` input filter — `$input->get('file', '', 'path')` — validates path *syntax*. It does
not prove the path is beneath the extension's permitted root. Code that treats it as a containment
check is a finding, and it is a common one.

`Path::check()` does enforce a root, but only the one it is given; confirm the root passed is the one
intended, and that the checked value is the value finally used rather than a copy taken before
further concatenation.

## Workflow

### Step 1 — Audit

Report findings ordered by severity:

- **CRITICAL** — attacker-controlled PHP inclusion, a write into an executable or configuration
  location, or arbitrary destructive deletion, reachable by a guest or low-privilege user.
- **HIGH** — arbitrary file read, archive traversal, or a write/delete escaping the intended root
  behind ordinary authenticated access.
- **MEDIUM** — constrained disclosure or modification, or exploitation requiring elevated extension
  privileges.
- **LOW** — fragile root enforcement or symlink/TOCTOU hardening with no demonstrated escape.

For each finding show the source, the path construction, the sink, the expected root, the bypass, the
privileges required, and the impact — with file and line references and a concrete mitigation.
Distinguish confirmed paths from questions that need runtime verification.

Report and await user feedback. Do not change code in this step.

### Step 2 — Feedback round

The user is a subject matter expert and may reclassify or overrule a finding after giving more
context.

### Step 3 — Plan fixes

Once the user is done giving feedback, check for remaining items to fix.

If none, say so and stop.

Otherwise break the fixes into smaller, individually implementable plans and write them to the
`.gitignore`'d `.plans` directory, clearing any existing files there first. Then propose running
those plans in parallel via subagents, on a cheaper/faster model — the planning work is already done.

---

*Adapted for this suite from the `audit-file-operations` workflow in
[nikosdion/pm-skill-demo](https://github.com/nikosdion/pm-skill-demo), MIT licensed,
Copyright (c) 2026 Nicholas K. Dionysopoulos. The MIT permission notice accompanies this adaptation;
full text at <https://github.com/nikosdion/pm-skill-demo/blob/main/LICENSE>.*

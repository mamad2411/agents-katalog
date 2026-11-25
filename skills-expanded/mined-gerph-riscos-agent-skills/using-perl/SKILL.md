---
name: using-perl
description: Write, review, and debug Perl for the RISC OS build environment, especially scripts that must run under the RISC OS Perl 5.001 interpreter rather than only under a modern host Perl. Use when changing `.pl` or `.pm` files, diagnosing RISC OS Perl parser/runtime failures, or checking whether a Perl construct is too new for the target interpreter.
license: MIT
---
# Using Perl

Assume the target interpreter is the RISC OS Perl shipped in the build environment unless the task clearly says otherwise.
Validate against that interpreter, not just the host Perl.

## Quick workflow

1. Check the target version with `riscos-build-run --command 'perl -v'` if compatibility matters.
2. Read [references/perl-5.001-checklist.md](references/perl-5.001-checklist.md) before editing code that will run on RISC OS.
3. Prefer old-Perl-safe constructs while editing.
4. Syntax-check on the host if useful, but always confirm the final behaviour under `riscos-build-run`.

## Default rules

* Treat Perl 5.001 compatibility as a requirement for RISC OS-executed scripts.
* Prefer 2-argument `open` with bareword filehandles over newer `open(...)` forms.
* Use `binmode(FILEHANDLE)` for binary I/O. Do not use `:raw`.
* Avoid lexical filehandles such as `my $fh`; use classic filehandles like `IN`, `OUT`, `FH`.
* Always pass an explicit mode to `mkdir`, such as `0755`.
* Do not assume host Perl success proves RISC OS Perl compatibility.

## Validation

When a script is meant to run on RISC OS, validate it there with the script and any required resource directories included in the `riscos-build-run` file list.

Do not run more than 2 `riscos-build-run` jobs concurrently. The build server may struggle with higher concurrency and produce misleading infrastructure failures.

Typical checks:

* `riscos-build-run --command 'perl -v'`
* `riscos-build-run script.pl support-dir --command 'Perl script.pl ...'`

If a failure appears only on RISC OS, add or update guidance in this skill when the lesson is generic rather than repository-specific.

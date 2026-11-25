---
name: using-makefiles
description: Development notes for the RISC OS AMU makefile build system. Covers the shared makefile types (CModule, CApp, LibraryCommand, LibExport, AsmModule, BasicApp, Documentation, Resource), their variables, build targets, and global configuration. Use when creating or editing Makefile,fe1 files, adding new source files to a build, changing build options, or diagnosing build failures.
metadata:
  author: gerph@gerph.org
license: MIT
allowed-tools: Bash(riscos-amu:*) Bash(riscos-build-run:*) Bash(riscos-project:*)
---
# RISC OS Makefile System

## Overview

RISC OS components are built with AMU (Acorn Make Utility) using the command `riscos-amu`.
Component makefiles are named `Makefile,fe1` (the `,fe1` suffix is the RISC OS AMU filetype).

Each component makefile sets a small number of variables describing the component, then
includes a shared makefile that provides all the build rules:

```makefile
COMPONENT = MyTool
OBJS      = o.main
LIBS      = ${CLIB}

include LibraryCommand
```

Shared makefiles are located via the `AMUFILES` environment variable (on Linux/Mac) or
the `Makefiles$Path` system variable (on RISC OS). Include them by name only — no path.

Variables set **before** the `include` configure the build.
Rules and extra targets placed **after** the `include` extend or override the build.

For detailed AMU makefile-language behaviour, read
`references/makefile-language.md` from this skill. Keep that reference aligned
with the `riscos-help makefiles` topic when behaviour or conventions change.

## AMU Makefile Language

AMU makefiles are plain ASCII text, usually stored as `Makefile,fe1`. A
makefile is read as logical lines; a trailing `\` continues a logical line onto
the next physical line.

Comments begin with `#`. The special comment:

```makefile
# Dynamic dependencies:
```

marks the section that AMU and related tools may update automatically. Leave it
in place even when it is empty.

The main line types are:

* dependency lines, `target : prerequisites`
* command lines, which must begin with white space
* macro definition lines such as `NAME = value`
* special-rule lines such as `.PHONY: test`

For compatibility, prefer a tab at the start of command lines. A single-command
rule may also be written as `target:; command`.

## AMU Macros and Directives

Macros are referenced as `${NAME}` or `$(NAME)`. Macro names are
case-insensitive, unlike GNU `make`.

Assignment forms supported by AMU:

* `=` lazy expansion
* `:=` immediate expansion
* `?=` assign only if unset
* `+=` append

Macros may also be pre-defined on the command line, for example
`riscos-amu BUILD64=1` or `riscos-amu COMPONENT=MyTool`.

Useful built-in and automatic macros include:

* `$@` current target
* `$*` matched stem in inference rules
* `$<` inferred source dependency
* `$?` prerequisites newer than the target
* `MAKE`, `MFLAGS`, `MAKEFLAGS`, `MAKECMDGOALS`
* `__riscos`, `__crosscompile`, and the older host-side name `__linux`

Directives and parsing features commonly seen in project makefiles:

* `include` and `.include`; prefix with `-` to ignore missing files
* `ifeq`, `ifneq`, `ifdef`, `ifndef`, `else`, `endif`
* `VPATH` for prerequisite search paths
* `::` to keep repeated rules for the same target distinct

## Special Targets and Functions

Special targets with practical impact:

* `.PHONY` marks synthetic targets that should always run
* `.SILENT` suppresses command echoing globally
* `.IGNORE` ignores command failures globally
* `.INIT` runs before requested targets
* `.DONE` runs after a successful build
* `.FAILED` runs after a failed build
* `.DEFAULT` provides a fallback rule
* `.SUFFIXES` controls suffix inference rules
* `.UNIXNAMES` favours Unix-style filename handling

Command prefixes:

* `@` suppresses echoing for one command
* `-` ignores failure for one command

AMU supports a useful subset of GNU-make-style functions. The ones agents are
most likely to encounter in real project makefiles are:

* text/list helpers: `subst`, `patsubst`, `strip`, `sort`, `findstring`,
  `filter`, `filter-out`, `word`, `wordlist`, `words`, `firstword`,
  `lastword`, `join`, `addprefix`, `addsuffix`
* filename helpers: `dir`, `notdir`
* control helpers: `if`, `foreach`, `call`, `warning`, `error`, `origin`
* `wildcard` for simple existence checks
* `lc` as a non-standard lower-case helper

Do not assume full GNU `make` compatibility. In particular, `wildcard` is not a
full shell-style expander, and `suffix`, `basename`, and `shell` should not be
relied upon as dependable features.

## Building

```bash
riscos-amu              # 32-bit build (default)
riscos-amu BUILD26=1    # 26-bit build (legacy)
riscos-amu BUILD64=1    # 64-bit build
```

Makefile targets are passed as arguments:

```bash
riscos-amu clean
riscos-amu export
riscos-amu ram
riscos-amu test
```

If a component has no shared testing convention, add a small project-local `test` target after the shared makefile include. For a C module smoke test, make it depend on `ram` and run the module with a BASIC test driver:

```makefile
.PHONY: test
test: ram
           riscos-build-run rm32/Module,ffa tests/test-module,fd1 --command "RMLoad Module" --command "Run test-module"
```

Use distinct RISC OS leaf names for the module and the test driver. `riscos-build-run` copies inputs into the guest by leaf name, so `tests/module,fd1` can collide with `rm32/Module,ffa`.

## Creating a New Project

Use `riscos-project` to generate a skeleton with the correct file layout:

```bash
riscos-project create --type command  --name PROJECTNAME --skeleton
riscos-project create --type cmodule  --name PROJECTNAME --skeleton
```

For desktop applications, choose a conventional RISC OS application name for
`COMPONENT`: capitalised, and usually without hyphens. For example, prefer
`WimpClicks` over `wimp-clicks`.

Always build the skeleton before editing to confirm the toolchain is working.

## Shared makefile quick picks

Use these shared makefiles by default:

* `LibraryCommand` for command-line tools and standalone executables.
* `CModule` for C modules using CMHG.
* `AsmModule` for assembly modules.
* `LibExport` for libraries intended to be exported.
* `CApp` and `BasicApp` for desktop applications.
* `Documentation` for PRM-in-XML-only components.
* `Resource` for resource-only components.

Read `references/shared-makefile-types.md` when you need the detailed variable
tables, export behaviour, or per-makefile caveats.

## Common targets and architecture

The targets agents most often need are `all`, `ram`, `rom`, `install`,
`export`, `resources`, and `clean`. Architecture is controlled with at most one
of `BUILD26=1`, `BUILD32=1`, or `BUILD64=1`.

Read `references/shared-makefile-types.md` for:

* target-by-target behaviour;
* output directory names such as `o32`, `oz32`, `aif32`, and `rm32`;
* global build variables, optional feature variables, and pre-defined library variables;
* `LibraryCommand`, `CModule`, `AsmModule`, `LibExport`, `CApp`, `BasicApp`,
  `Documentation`, and `Resource` variable reference tables;
* export-path variables and common `INITTARGET`/`CLEANTARGET` patterns.

## Running built outputs

* 32-bit absolute:
  * `riscos-build-run aif32 --command 'aif32.Program'`
* 64-bit absolute:
  * `riscos-build-run --64 aif64 --command 'aif64.Program'`

If `--64` is omitted for a 64-bit absolute, the runner may report that 64-bit absolute files are not executable on this system even though the binary itself built correctly.

For `CApp` and other install-oriented components, verify packaging with an
explicit install directory rather than a bare `riscos-amu install`. Use a
command such as:

```bash
riscos-amu install INSTDIR=install
```

This exercises the install rules and produces an application directory under
`install/` without relying on an implicit destination.


See `references/shared-makefile-types.md` for the detailed variable tables and
patterns that used to live inline here.

## Object File Dependency Patterns

To express that a compiled object depends on a generated header (e.g. the CMHG-generated
`h.modhead`):

```makefile
$(OZDIR).module: h.modhead
```

Note: use `$(OZDIR)` not `$(ODIR)` for module objects, as modules use module
compilation.


## Practical validation pattern

For command projects:

1. Build 32-bit with `riscos-amu`.
2. Run 32-bit smoke or self-tests with `riscos-build-run aif32 ...`.
3. Build 64-bit with `riscos-amu BUILD64=1`.
4. Run 64-bit smoke or self-tests with `riscos-build-run --64 aif64 ...`.

Keep the 64-bit status distinct:

* `builds` means `riscos-amu BUILD64=1` succeeds.
* `runtime-validated` means the `--64` runner path also succeeds.


## 64-bit cautions

* The 64-bit build environment is useful as a separate portability check, even before runtime validation.
* Some library or kernel helper entry points available in 32-bit builds may need guarding or replacement for `__riscos64`.
* Avoid assuming that success in the 32-bit Norcroft build implies success in the 64-bit build.


## Agent Guidance

* **Always add `OBJS` entries as `o.name`** — the build system substitutes the correct
  directory prefix (`o`, `o32`, `oz32`, etc.) automatically based on architecture and
  build type. Never write `o32.name` in `OBJS`.
* **Multi-line `OBJS` and `LIBS`** — use backslash continuation and consistent indentation:
  ```makefile
  OBJS = o.main \
         o.utils \
         o.output
  ```
* **`INCLUDES` is comma-separated**, not space-separated. It is added after `C:` automatically.
  Example: `INCLUDES = C:MyLib.`
* **`CDEFINES` is space-separated**, e.g. `CDEFINES = -DDEBUG -DVERSION=2`.
* **Do not include `${CLIB_ZM}` in module `LIBS`** — module makefiles add the module
  C library automatically. Adding it explicitly will cause duplicate symbol errors.
* **After adding new source files**, run `riscos-amu` to confirm the build succeeds before
  making further changes.
* **`DOCSRC` filenames use RISC OS dot-separated paths**, e.g. `docs.MyAPI` refers to the
  file `docs/MyAPI,xml` on Linux.
* **`clean` does not remove exports** — to force a clean export, delete the export directory
  or run `export_clean_dir` manually if supported.
* **The `Dynamic dependencies:` comment at the end of a makefile** is maintained by AMU
  and should be left in place even when empty.

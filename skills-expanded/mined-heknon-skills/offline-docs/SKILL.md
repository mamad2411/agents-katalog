---
name: offline-docs
description: Answer "how does this library or tool work" with no web access, from what is installed. Say which version of a package is installed and where from, what a function or class accepts and returns, where **kwargs really go, what a default is or what happens with None, what changed between two versions or since when something exists or is deprecated, which function or option does something, what a CLI flag, ruff rule or setting means, and where the documentation is and which version it describes. Uses the installed source in site-packages and the standard library, inspect, help and pydoc without a pager, importlib.metadata and the dist-info folder, wheels and sdists read without installing, type stubs, a tool's own --help, and internal doc mirrors. Every answer is stamped with the version it was checked on and ends in a verdict. Verified on CPython 3.12.14 and uv 0.12.19.
---

# Offline docs

This skill looks things up in the installed environment: the code that
runs, its metadata, its stubs, and the tools' own help. Every command,
API and message in it was run on CPython 3.12.14 and uv 0.12.19 (and the
library versions named where they appear). Nothing is written from
memory, and nothing you answer may be: memory of a library is where a
search starts, never the answer.

Read this file, then load only what the task needs.

## Pin the version first

Every kind of task starts with `core/pin-version.md`. Nothing is read
before it:

```powershell
uv run --no-sync python <skill>\recipes\lookup.py pin <distribution>
```

`<skill>` is the folder holding this file. The recipe prints the
interpreter, the version, the location, the install kind and the file
each import name loads, without importing the package
(`recipes/README.md`). Which interpreter runs the project is navigation's
Environment question; in a uv project this one command answers it, and
anything unusual (poetry, conda, a stray `python`) goes to navigation's
`core/environment.md` first.

## The kinds of task

| Kind | You were asked to | Load |
| --- | --- | --- |
| **Version** | say which version of X is installed, where from, editable or not | `core/pin-version.md`, `python/metadata.md` |
| **Signature** | say what a function or class accepts and returns, where `**kwargs` go | `core/signature.md`, `python/inspect.md` |
| **Behaviour** | say what X does in a case: a default, an error, `None` | `core/behaviour.md` |
| **Changed** | say what changed between versions, since when X exists, whether it is deprecated | `core/changed.md` |
| **Discover** | find which function, class or option does Y | `core/discover.md` |
| **Tool** | explain a CLI flag, a rule or a setting | `core/tool.md`, `tools/cli-help.md` |
| **Docs** | find the documentation for X | `core/docs.md`, `python/pydoc.md` |

Before you answer, load `core/evidence.md`: it ranks the sources and
says how to write the verdict, including "not found".

## Where the facts are

| Folder | Holds |
| --- | --- |
| `core/` | the procedures above, and `evidence.md` |
| `python/` | installed files and the standard library (`installed-files.md`), pydoc without a pager (`pydoc.md`), `inspect` and where it fails (`inspect.md`), `importlib.metadata`, dist-info and wheels (`metadata.md`), stubs and their versions (`stubs.md`) |
| `tools/` | asking uv, ruff, mypy, pyright, ty, git and PowerShell about themselves (`cli-help.md`) |
| `recipes/` | `lookup.py`: pin, where, grep, lines, def, wheel, diff; run from the project with its interpreter |
| `examples/` | four finished lookups, one per verdict and one Changed: old pydantic (`old-pydantic.md`), a compiled library (`compiled-stub.md`), an option that does not exist (`not-found.md`), two versions compared (`what-changed.md`) |

`glossary.md` fixes the words. The lab ran on Linux; Windows paths are
given where they differ, and facts that could not be run there are
marked `not run on Windows`.

## Invariants

1. **Pin first.** Interpreter and distribution version before any code,
   docstring or page is read.
2. **Read what runs.** The file the interpreter imports, in
   `site-packages` or the standard library folder; never a copy in the
   repository, another environment, or memory.
3. **Code outranks words.** Docstrings, stubs, METADATA text, `--help`
   and pages are leads; the lines that run decide, and a disagreement is
   reported.
4. **Follow `**kwargs` and wrappers** to the function that names its
   parameters. A keyword nothing accepts does not exist.
5. **Ask the tool the project runs**: `uv run --no-sync <tool>`, with its
   version and path, never a bare command.
6. **Never block, never cause side effects.** No `help()` or bare
   `python -m pydoc` in the terminal; no import of a module whose
   top-level code you have not read; no `pydoc -k`, `-p` or `modules`.
7. **Never change the environment to answer.** No `uv add`, `uv sync`
   or `uv pip install`; another version only in a throwaway environment
   (`uv run --isolated --no-project --with`), said in the answer.
8. **"Not found" is an answer.** Say where you looked; never invent an
   option, parameter, flag or changelog entry.
9. **Every answer is stamped and ends in a verdict** (`core/evidence.md`).

## What you say when you finish

End with these headings, each with `none` when empty. If another skill
is loaded, its headings come first and these after.

```
## Answer
Answer:   <one or two lines>
Checked:  <distribution> <version>, Python <x.y.z>, <interpreter path>
Evidence: <path:line and what is there> | <command and the line it printed>
Source:   code | stub | docstring | --help | metadata | internal page
Verdict:  confirmed from source at <path:line> on <version>
          | confirmed from <stub | help | page> only | not found (<where looked>)

## Not checked
<other versions, the Windows build, pages or hosts not reached, runs not made>
```

One block per question when there are several.

The `evals/` folder is for people testing this skill. Never open it while
doing a task.

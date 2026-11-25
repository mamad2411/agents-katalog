---
name: bitbake-metadata
description: Official-doc-first BitBake metadata support for AI coding agents. Use when inspecting, creating, editing, or debugging BitBake recipes, appends, classes, include files, configuration, tasks, variables, overrides, fetchers, signatures, sstate, dependency graphs, parse errors, QA errors, or files ending in .bb, .bbappend, .bbclass, .inc, .conf, plus metadata inside conf/, classes/, recipes-*/, and layer.conf.
---

# BitBake Metadata

## Core Workflow

1. Determine the release and BitBake version from the workspace before applying syntax guidance. Check `bitbake --version`, branch names, `LAYERSERIES_COMPAT`, and the docs selected by the parent Yocto release.
2. Inspect existing metadata first. Search for the recipe, provider, class, variable, override, task, and package name across all configured layers.
3. Read official docs for the exact mechanism. Use [bitbake_doc_router.py](scripts/bitbake_doc_router.py) with a topic name to choose a starting URL.
4. Explain metadata changes in terms of parse-time effects, task effects, package effects, and signature/sstate effects.
5. Validate with BitBake introspection rather than assumptions.

## Introspection Commands

Use the project wrapper if one exists. Otherwise, after sourcing the build environment:

```sh
bitbake-layers show-layers
bitbake-layers show-recipes RECIPE
bitbake-layers show-appends
bitbake -e RECIPE | less
bitbake -c listtasks RECIPE
bitbake -g RECIPE
bitbake-dumpsig SIGDATA_OR_SIGINFO
bitbake-diffsigs SIGDATA_A SIGDATA_B
```

For targeted variable checks, prefer `bitbake -e RECIPE` and search for the final assignment plus history comments.

## Metadata Editing Rules

- Preserve local style for variable operators, override order, indentation, and layer layout.
- Prefer `:append`, `:prepend`, and `:remove` override syntax for modern releases, but verify old-release syntax before changing legacy branches.
- Keep machine, distro, image, and recipe concerns in their correct files.
- Use `.bbappend` when changing recipes from another layer.
- Keep checksums, licenses, and `SRC_URI` changes explicit and reviewable.
- Do not set `PREFERRED_PROVIDER`, `PREFERRED_VERSION`, `BBMASK`, or global variables without checking blast radius.

## References

Read only the reference file needed for the task:

- [official-sources.md](references/official-sources.md): authoritative BitBake docs and source links.
- [metadata-cheatsheet.md](references/metadata-cheatsheet.md): syntax, operators, overrides, tasks, and fetcher reminders.
- [debugging.md](references/debugging.md): parse, fetch, task, dependency, QA, signature, and sstate debugging workflow.

## Guardrails

- Do not quote outdated underscore override syntax as current without release context.
- Do not guess final variable values from recipe text alone; BitBake metadata is layered and override-sensitive.
- Do not silence QA or license checks without identifying the actual package/file/license issue.
- Do not remove dependencies only because the immediate task builds; check runtime packaging and image consequences.

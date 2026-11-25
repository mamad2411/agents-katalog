---
name: aem-cloudmanager
description: Cloud Manager and OakPAL review — package filters, embed order, Dispatcher SDK, deployment safety
allowed-tools: Read, Grep, Glob, Bash(git diff *), Bash(git diff)
argument-hint: "[file path, or leave blank to check current diff]"
---

Review `$ARGUMENTS` for Cloud Manager pipeline and deployment risks. If no files are provided, run `git diff` to identify what changed. Report each finding as **Blocking** / **Warning** / **Suggestion**.

**OakPAL / packaging**
- Overlapping filter roots across packages — Blocking
- Mutable content (`/content`, editable templates under `/conf`) placed in `ui.apps` — Blocking
- `ui.apps.structure` missing as prerequisite in `all/` embed order — Blocking
- Missing embed in `all/` after adding a new module — Blocking
- `filter` mode `merge` or `replace` that could overwrite existing authored content — Warning

**OSGi configuration**
- OSGi config in wrong runmode folder (`config.author` vs `config.publish`) — Blocking
- OSGi config filename not matching PID exactly (including factory `~identifier` suffix) — Warning

**Dispatcher**
- Configuration using directives not supported by the AEMaaCS Dispatcher SDK — Warning
- Sensitive AEM endpoints not blocked (`/crx`, `/system`, `/bin/wcmcommand`) — Blocking

**Quality gates**
- SonarCloud critical or blocker issues likely to stop the pipeline — Warning
- Test coverage regression that could breach threshold — Warning

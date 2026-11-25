---
name: init-dev-project
description: Scaffolds a folder into the dev-and-deploy standard (lanes, four make verbs, spec/src/tests/deploy/docs layout, .aai/ with identity, purpose and the standard as a reference) and makes it a git repo; use for "init a dev project", "scaffold a new project", "set up a repo for X", "new skill/tool/app folder", "start a project the standard way".
---

Read `instructions.md` in this skill's directory and follow it.

Path note: this skill also ships inside the `ambient` library plugin, so its
instructions may reference files as `${CLAUDE_PLUGIN_ROOT}/library/init-dev-project/<file>`.
When installed standalone, resolve those to `<file>` in this directory.

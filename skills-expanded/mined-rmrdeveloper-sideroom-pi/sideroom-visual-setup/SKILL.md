---
name: sideroom-visual-setup
description: "Enable, review, or troubleshoot precise Sideroom visual context in a web project, including child projects and development servers in Docker. Use for requests such as 'Activa el contexto visual preciso'; not for ordinary UI changes or browser automation."
license: MIT
metadata:
  author: RMRdeveloper
  version: "1.0"
---

# Visual context setup

Configure one requested project so a browser selection carries a compiler location
that Pi can validate against local source. Requires `sideroom_visual_setup`; if
it is unavailable, load the Sideroom installation that provides it before proceeding.

## Workflow

1. Resolve the requested project relative to Pi's working directory; use `discover`
   when the target is unknown. Reuse an explicit choice; ask only if it is ambiguous. Read its
   build config, manifest, lockfile ownership and actual development launch command.
   Inspect Docker configuration only when it runs the development server.
2. For a new integration, use `prepare` and apply its edit and installation command
   through normal Pi tools. The plan owns compiler code, dependency versions and
   check scripts: do not duplicate that template here or in a helper file. For an
   existing/custom integration, preserve it and change only what inspection shows
   is missing. Keep metadata before framework transforms, development-only, with
   no second browser UI or editor-launch service. Install in the selected workspace
   and ensure the dependency is also present in the runtime that serves the app.
3. Check path portability before starting the server:
   - When runtime and Pi share paths, retain the plan's absolute paths.
   - When Docker or another runtime has different paths, emit paths relative to the
     app root and `bind` the actual page origin to that local project, or associate
     it through F7. Do not bind it to the parent folder merely because Pi runs there.
     With Code Inspector 2.0.9, `transformCode` checks that `filePath` exists before
     transforming: a relative input must resolve from the runtime's working
     directory. Romax's pattern works because its Docker working directory equals
     Vite's app root. Verify this condition instead of copying it to every project.
     Reject out-of-project references; do not relax Sideroom's path guards.
4. Run the project's existing checks, restart the selected development service
   through its established workflow, and refresh the page. Reload Pi and the
   companion together if their visual protocols differ; preserve pairing.
   Select a native element and verify its marker resolves to the intended local
   file, line and column with **compiler location checked** in F7. If practical,
   confirm a production build omits markers. A successful install or build alone
   does not verify browser-to-source resolution.

Report the project, changed files, checks and browser verification status. When
browser/runtime access is unavailable, finish the configuration and identify the
remaining verification step; do not label inferred or untested locations exact.

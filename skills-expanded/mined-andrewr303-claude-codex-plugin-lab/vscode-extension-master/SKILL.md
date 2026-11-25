---
name: vscode-extension-master
description: Master workflow for VS Code extension development, debugging, refactoring, webviews, language extensions, LSP, testing, bundling, and publishing. Use when the user asks to build, debug, improve, review, or ship a VS Code extension and route to the included specialist references.
---

# VS Code Extension Master

## Mission

Use this skill as the front door for serious VS Code extension work. Treat the extension manifest, activation contract, contribution points, extension-host lifecycle, webview security model, tests, and packaging scripts as source-of-truth surfaces.

This plugin combines the attached extension, webview, debugger, refactorer, language-extension, and guide materials into one workflow.

## Required Workflow

1. Inspect the repo before making claims or edits:
   - `package.json`
   - lockfile and package manager
   - `src/extension.ts` or configured `main`
   - `.vscode/launch.json` and `.vscode/tasks.json`
   - `tsconfig.json`
   - test config and scripts
   - bundler config such as `esbuild`, `webpack`, `tsup`, or `vite`
   - `.vscodeignore`, README, CHANGELOG, and publisher metadata when packaging or publishing
2. Identify the active extension shape:
   - command extension
   - language extension
   - LSP client/server
   - tree view or custom view
   - webview panel/view/custom editor
   - notebook, debugger, task provider, file system provider, authentication provider, or mixed extension
3. Route to specialist material:
   - General architecture and feature work: `../vscode-extension-expert/SKILL.md`
   - Webview, CSP, message passing, theming, state, performance: `../vscode-webview-expert/SKILL.md`
   - Bugs, activation failures, crashes, memory leaks, race conditions: `../vscode-extension-debugger/SKILL.md`
   - Refactoring, type safety, module boundaries, cleanup: `../vscode-extension-refactorer/SKILL.md`
   - Language configuration, TextMate grammar, snippets, simple LSP package shape: `../vscode-extension/SKILL.md`
   - Community guide snapshot: `references/community-guide-en.md`
4. For current API, CLI, Marketplace, package, or testing behavior, fetch official docs first:
   - Resolve Context7 library ID for `Visual Studio Code Extension API`.
   - Query the official VS Code Extension API docs with the user's full question.
   - Prefer official VS Code docs and Microsoft samples over memory when they conflict.
5. Implement the smallest coherent change:
   - preserve existing command IDs, setting keys, view IDs, storage keys, and public APIs unless explicitly migrating them
   - keep all disposables registered or disposed
   - avoid broad rewrites while debugging
   - keep webview resources behind `asWebviewUri`, `localResourceRoots`, and a strict CSP
   - validate webview messages and extension-host inputs at boundaries
6. Verify with the repo's own scripts:
   - infer package manager from lockfile
   - run typecheck or compile first
   - run lint when available
   - run focused unit/integration tests
   - run extension tests when configured
   - run build/package checks when the task touches bundling or publishing

## Output Contract

For implementation work, report:

- files changed
- behavior changed
- verification commands run
- known risks or unverified areas
- any Marketplace, VSIX, manual Extension Development Host, or new-thread testing steps

For diagnostic work, lead with:

- reproduction path
- likely root cause
- exact evidence from files/logs/tests
- fix plan or fix applied
- regression check

## Design Rules

- Prefer lazy activation over startup activation.
- Keep extension-host work fast and async.
- Register all commands declared in `contributes.commands`.
- Add disposables to `context.subscriptions` or an owned disposable store.
- Use `SecretStorage` for credentials, not settings or local files.
- Use output channels for durable logs instead of noisy user popups.
- Keep command IDs, configuration keys, and view IDs namespaced.
- Keep webview scripts isolated from extension internals.
- Do not expose the VS Code API object globally inside webview code.
- Treat `retainContextWhenHidden` as a cost, not a default.
- Test on Extension Development Host before packaging.

## Safety Notes

- Do not invent VS Code API names.
- Do not suggest deprecated APIs without labeling them and offering the current alternative.
- Do not hardcode one package manager when the lockfile says otherwise.
- Do not store secrets in `package.json`, settings, webview HTML, or logs.
- Do not broaden activation to `*` unless the user explicitly asks and the tradeoff is documented.
- Do not skip verification for activation, package, or webview changes unless the repo cannot run it.

## Source Provenance

See `references/source-provenance.md` for the attached files used to assemble this plugin.

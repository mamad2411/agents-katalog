---
name: clodable-prepare
user-invocable: false
description: Prepare an existing local application for Clodable, or resume and recheck an earlier adaptation. Use for unsupported HTML prototypes or frameworks, preparation for saving, and requests to verify that an adaptation preserved existing journeys even when Clodable already recognizes the app. Preserve the original, agree on any rewrite and compare behavior before and after. Ordinary feature edits, new app ideas and moving services off Lovable use their own workflows.
---

# Prepare an existing app for Clodable

Make the existing application work with Clodable's supported formats: Vite + React or TanStack Start. Preserve the builder's design, content, routes, data behavior and interactions. Explain decisions in product terms and match the builder's language.

Keep each progress update to one sentence and the final reply to at most 80 words. Say “the application checks” and “the preview”; leave command names, build terminology, filenames, ports and local addresses out unless the builder requests technical details. Apply the same vocabulary to visible task titles. Resolve startup retries and port conflicts quietly; mention a diagnostic only when the builder must act. For successful checks, say “L’application est compatible avec Clodable. Je vérifie maintenant ses parcours dans l’aperçu.” (or its equivalent in the builder’s language).

Describe a regression through its effect on the builder: “Les réservations existantes ne s’affichent plus” or “Le formulaire accepte maintenant un prénom trop court.” Keep storage keys, source filenames and internal comparisons in your working notes, including during a recheck.

This workflow prepares local code. Account consent, creating the private app and publishing remain in Clodable's controls. Never run setup, initialize Git, change existing history or remote connections, create anything on GitHub, connect accounts or provision services during preparation. Use `clodable:clodable-move` for an authorized move off Lovable's services; ownership and architecture are separate decisions.

## Inspect and agree

Read the app's own instructions, files, dependencies, scripts, routes and interactions. An `index.html` can belong to a framework or server application. Identify the existing user journeys and any live services they call. For each journey affected by adaptation, keep a compact before/after comparison in your working notes: action, expected result, observed original behavior and result after adaptation. Cover navigation, forms and validation, saved data after reload, direct links and server behavior where present. Distinguish observations from expectations inferred from code. Re-establish missing evidence when resuming; a backup is not a successful check.

Use the installed command named by the app's `AGENTS.md`. Before setup, use the bundled command below from this app's folder. Never fetch another version with `npx clodable`.

```bash
node "${CLAUDE_PLUGIN_ROOT}/cli/clodable.mjs" doctor --local --json
```

- For an already supported app, preserve its architecture. Fix only a missing requirement. When resuming or rechecking an adaptation, continue its journey verification even if Clodable already recognizes the app. Open `saving` immediately only when no adaptation was needed and no journey verification was requested.
- For a simple static app, adapt the existing content and behavior to Vite + React with `dev` and `build` scripts. Preserve CSS, images, fonts, URLs, navigation, forms and local data. Do not replace the app with a template or hide it in an iframe to pass detection.
- For another framework or server application, choose a supported format that preserves the behavior, including server routes. Get agreement before rewriting. Do not replace a working server with sample data or add dependencies merely to pass detection. If the scope is unclear or essential behavior cannot be preserved, explain the limit and keep the app working locally.

Before rewrite consent, use at most 80 words total: one short paragraph explaining the need and the preservation goal, then the two choices. Do not add headings, an inventory, implementation details or a verification checklist. For example: “Je vais adapter la partie technique pour rendre votre application compatible avec Clodable, en préservant son apparence, ses fonctionnalités et ses données. Je conserverai une copie de l’original et vérifierai les parcours existants. Si une fonction pose problème, je vous l’expliquerai avant de poursuivre. Voulez-vous que je la prépare, ou préférez-vous la garder telle quelle ?”

Choose the technical approach yourself. Ask the builder about its effects on their app, not which framework to use. Explain any known visible change or preservation limit before seeking agreement; the example must not hide one. Describe what people can do, rather than where code runs or how data is fetched. Adaptation consent does not authorize removing a feature, weakening validation or replacing persistent data with temporary data. A requested functional change needs its own explicit agreement. Use names such as Vite, React or TanStack only if the builder asks for technical details. Apply this to progress, questions, choice labels and the final reply, in the builder's language.

A request to inspect, explain, plan or wait authorizes only that scope. A refusal leaves the original unchanged. Ordinary feature edits do not authorize preparation.

## Preserve before editing

Before installing packages, scaffolding, moving or editing app files, run:

```bash
node "${CLAUDE_PLUGIN_ROOT}/cli/clodable.mjs" prepare backup --json
```

Require `ok: true` and `completed: true`. The command creates a verified, ignored snapshot under `.clodable/local/original/<id>/`. It includes hidden and untracked files, environment files and symlinks. It preserves links without copying their external targets. Preserve external files separately before changing them. Establish the original's observable behavior before adaptation, using a safe local preview and disposable local data. Do not modify live data, send real messages or incur charges to test a journey. If an original journey cannot be exercised safely, record the exact limit instead of inventing a pass.

The manifest and completion marker stay beside `files/`. The original ignore file is preserved before the command adds the private-folder rule. Each retry creates a new snapshot. Never overwrite or delete an earlier snapshot. If preservation fails, leave app files unchanged and resolve the backup failure first. Do not improvise a tracked-files-only backup or print secrets. This command is the narrow exception to the rule against editing Clodable's private files.

## Adapt and verify

Make the agreed changes. Keep private settings out of browser code. Verify all four results before reporting preparation complete:

1. **Production build:** inspect its configuration and run the build successfully. Never use the whole project as `publicDir`, include `.clodable/local/` in inputs or broadly copy the project into output. Confirm the output contains no backup, manifest, environment file or private local state.
2. **Clodable support:** run the installed `doctor --json`. Require `local-app.contents` to be `supported` and the `app` check to be `ok`. Overall command success alone is insufficient. Missing GitHub connection or saving setup is expected here; do not initialize Git or connect an account to clear those warnings.
3. **Working preview:** register the installed `dev` command with Desktop’s preview server tools, start it there and open it in Desktop. Keep this verified preview running for the builder; do not stop it after testing. Avoid unmanaged background shell processes. This preview protects Clodable's private files. Do not use a generic static file server.
4. **Existing journeys:** replay the before/after comparison in the adapted preview. Compare appearance and each journey's observable result, including validation, persistence after reload and server behavior where present. Use the same disposable inputs. Run existing relevant tests too; build and support checks do not prove functional preservation. Classify each result as passed, failed or blocked, with evidence. Treat an unexercised original or unavailable service as a limit, not a pass. Never remove a failed journey from the comparison to finish.

Fix a regression and repeat its journey and any related checks affected by the fix. Stop and explain any unresolved failure or blocked comparison. Keep the original available. Do not report preparation complete or invite another saving attempt until all four checks pass for the agreed scope.

When ready, briefly state what was preserved and verified, then open `saving` with `open_panel` for the builder's account consent. Preparation alone does not mean the app is saved or public.

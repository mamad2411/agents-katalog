---
name: setup
description: Configure or diagnose Hames in the current project when the user invokes /setup.
---

# Setup

Use the user's language and ask one decision at a time. On first use, ask what work the user wants to do, which root to manage, workspace names/paths/purposes, and subfolder roles. Offer editable examples, never fixed personal categories. Existing folders may be registered in place. Reuse choices already known; an uncertain answer invites a recommendation, not an invented decision.

Turn the answers into workspace definitions: `id`, root-relative `path`, `name`, `purpose`, `folders` with workspace-relative path and purpose, `rules` with id/kind/path/value, `exclude`, `context`, and `protect`. Rule kinds are `extension` (list of extensions), `name` (regular expression), `required` (required text), and `semantic` (a judgment instruction). Explain concrete checks versus meaning-based judgments. Shared document registrations have root-relative `docs/` path, purpose, scope (`common` or workspace id), and optional dependencies.

Use bundled `runtime/setup.js plan --root <root> --input <decisions.json>`. The input accepts projectName, workspaces, documents, exclude and contractTracking. Do not require users to write JSON; stage tool input outside their workspace until approval (host temporary storage), without secrets. The preview is read-only. Show the proposed tree, roles, file rules, exclusions, exact existing-file edits and initial indexes. Non-Git roots default to untracked contracts without initializing Git. A Git root with an unresolved tracking choice gets one question.

After the user approves that exact preview, run `runtime/setup.js apply --root <root> --input <decisions.json> --approved --plan-hash <preview hash>`. This is the only setup approval; do not ask twice. A changed preview is not the approved preview. Re-read the applied configuration and indexes and report any unresolved classification. Do not initialize this plugin's development repository as a user workspace.

For reconfiguration, load current choices, change only what the user requests, and show a new preview. Repeated valid setup is read-only. Changing a workspace path never moves the user's existing files. Missing registered folders and damaged settings need an explicit recovery choice; do not silently recreate them. Existing entry files, manual index text, shared docs and archived contracts are preserved. Active old-format contracts block upgrade until completed or explicitly handed off.

`runtime/setup.js recover` provides a read-only recovery preview. Only after the user chooses that recovery, pass `--approved --recovery-hash <hash>`. Never overwrite newer user edits while rolling back.

Recognized old public Hames folders use the existing manifest-based transition preview. Keep modified, unknown, protected and submodule files. Only exact unchanged old system files listed in the approved preview may be removed. Never expose protected content or hashes. Do not alter Git history, index, branches or remotes.

Hames already includes adapted DryForge workflows; do not install another DryForge plugin. Long-lived operating documents belong to shared root `docs/`, not each workspace. Do not generate a standard empty document set. Use `/index` for a read-only file audit, `/doctor` for configuration and hook diagnosis, and `/ready` then `/go` for bounded task execution. Ordinary file work needs no Git or task contract.

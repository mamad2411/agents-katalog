---
name: setup-supermatt-skills
description: "Configure this repo for the engineering skills: set up its issue tracker, triage labels, domain doc layout, and external peer policy. Run once before first use of the other engineering skills."
disable-model-invocation: true
license: MIT
---

# Setup SuperMatt Skills

Scaffold the per-repo configuration that the engineering skills assume:

- **Issue tracker**: where issues live (GitHub by default; GitLab and local markdown are also supported out of the box)
- **Triage labels**: the strings used for the seven canonical triage roles (two category, five state)
- **Domain docs**: where `GLOSSARY.md` and ADRs live, and the consumer rules for reading them
- **External peers**: whether `code-review` and `jury` stay on the current host or call a configured Claude, Codex, Cursor Agent, or OMP CLI

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write.

## Process

### 1. Explore

Look at the current repo to understand its starting state. Read whatever exists; don't assume:

- `git remote -v` and `.git/config`: is this a GitHub repo? Which one?
- `AGENTS.md` and `CLAUDE.md` at the repo root: does either exist? Is there already an `## Agent skills` section in either?
- Resolve glossary, map, and ADR paths from an existing `docs/agents/domain.md` first, using its selected layout rather than unused template examples. Preserve configured paths even before the files exist. Where unset, follow domain paths referenced by the repo's existing instructions and discover `GLOSSARY.md`, `GLOSSARY-MAP.md`, their legacy names `CONTEXT.md` and `CONTEXT-MAP.md`, and existing ADR directories such as `docs/adr/` and `src/*/docs/adr/`. Read any map for its per-context paths. Preserve discovered names; use default names only where neither configuration nor existing files supply a path. If candidates conflict, resolve the choice in Section C. Offer a rename only as a second option, and before any approved rename, find and update its references.
- `docs/agents/`: does this skill's prior output already exist, including `cross-model.json`?
- `.scratch/`: a sign that a local-markdown issue tracker convention is already in use
- Monorepo signals: a `pnpm-workspace.yaml`, a `workspaces` field in `package.json`, or a populated `packages/*` with its own `src/`. These are present only in a genuinely large multi-package repo; their absence means single-context, which is almost every repo.
- Installed peer commands: `claude`, `codex`, `agent`, and `omp`. Check only whether each command exists. Do not make a paid authentication or quota probe.

### 2. Present findings and ask

Summarise what's present and what's missing. Then take the sections in order. One section, one answer, then the next.

Lead each section with the recommended answer so the user can accept it in a word. Use the host's live multiple-choice capability when available and follow its schema; otherwise ask in chat. Give a one-line explainer only when the choice genuinely branches; skip a question when exploration already settled it.

**Section A: Issue tracker.**

> Explainer: The "issue tracker" is where issues live for this repo. Skills like `to-tickets`, `triage`, and `to-spec` read from and write to it. They need to know whether to call `gh issue create`, write a markdown file under `.scratch/`, or follow some other workflow you describe. Pick the place you actually track work for this repo.

Default posture: these skills were designed for GitHub. If a `git remote` points at GitHub, propose that. If a `git remote` points at GitLab (`gitlab.com` or a self-hosted host), propose GitLab. Otherwise (or if the user prefers), offer:

- **GitHub**: issues live in the repo's GitHub Issues (uses the `gh` CLI)
- **GitLab**: issues live in the repo's GitLab Issues (uses the [`glab`](https://gitlab.com/gitlab-org/cli) CLI)
- **Local markdown**: issues live as files under `.scratch/<feature>/` in this repo (good for solo projects or repos without a remote)
- **Other** (Jira, Linear, etc.): ask the user how their tracker does each operation the GitHub template defines (create, read, list, comment, labels, close, blocking, and the wayfinding operations)

Record the choice in `docs/agents/issue-tracker.md`. The GitHub and GitLab templates carry a "PRs as a request surface" flag. Default it to **off** for new files; preserve an existing value on reruns. Don't raise it: a user who wants external PRs in the triage queue can flip the flag in the file later.

**Section B: Triage label vocabulary.** `to-spec`, `to-tickets`, and `triage` all apply these labels, so this section always runs.

On first setup, ask:

> Do you want to keep the default triage labels? (recommended: **yes**)

The defaults are the seven canonical roles, each label string equal to its name: `bug`, `enhancement`, `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. On **yes**, use them as-is. On **no**, collect the overrides so the skills apply existing labels instead of creating duplicates.

On reruns, show the current mappings and ask whether to **keep current** (recommended), **reset to defaults**, or **supply replacements**. The selected mappings are authoritative for both the draft and final file; a reset discards prior overrides.

**Section C: Domain docs.** Preserve the resolved layout and paths from exploration. An existing map or a map selected by the configured layout establishes **multi-context**, even without monorepo signals. Otherwise keep the configured layout, or default to **single-context**. Ask only to resolve conflicting discoveries or to offer multi-context when monorepo signals exist and no layout is established.

For paths still unresolved, single-context defaults to `GLOSSARY.md` at the repo root and `docs/adr/`; multi-context defaults to a root `GLOSSARY-MAP.md` pointing to per-context glossaries. Preserve any resolved legacy or custom names and ADR paths in the layout description, reading instructions, and examples. Domain files are created lazily by the consuming skills; rename an existing file only with explicit user approval.

**Section D: External peer calls.** Ask which mode `code-review` and `jury` should use:

- **`auto`**: select only the hardened Claude or Codex adapter from authoritative host-family metadata. Ask for optional Claude and Codex models and effort values.
- **`host-only`**: start no supported external peer subprocess. Keep the seed profile values and ask no unused profile questions.
- **`claude`**, **`codex`**, **`cursor`**, or **`omp`**: force exactly that adapter. Ask only for that profile's supported values.

Preserve `auto` by default. Recommend `host-only` when the requested executable is missing or the user says its authentication or quota is unavailable. A `default` model answer writes `null`; otherwise record a nonempty string. Claude, Codex, and OMP effort defaults to `"high"` unless the user explicitly chooses the CLI default, which writes `null`. Cursor has no separate public effort flag. A Cursor model value is the complete installed-CLI model specification, such as `claude-opus-4-8[effort=high]`, and stays unchanged.

Before the user chooses Cursor, explain that Ask mode prevents agent edits but inherits local and repository rules, MCP, plugins, executable hooks, and persistent session storage. Before the user chooses OMP, explain that it receives only the prepared evidence bundle and disables repository tools, but cannot fully isolate inherited configuration or MCP and cannot inspect omitted repository evidence.

### 3. Confirm and edit

Print the drafts as text in your reply, then ask whether to write them:

- The `## Agent skills` block to add to whichever of `CLAUDE.md` / `AGENTS.md` is being edited (see step 4 for selection rules)
- The contents of `docs/agents/issue-tracker.md`, `docs/agents/domain.md`, `docs/agents/triage-labels.md`, and `docs/agents/cross-model.json`

A file taken from its template as-is drafts as its name plus the lines you filled in (the repo slug, selected label mappings, resolved domain layout and paths). Done when every file Step 4 will write has its draft printed above the question. Write after the user answers.

### 4. Write

**Pick the file to edit:**

- If `CLAUDE.md` exists, edit it.
- Else if `AGENTS.md` exists, edit it.
- If neither exists, ask the user which one to create; don't pick for them.

Never create `AGENTS.md` when `CLAUDE.md` already exists (or vice versa); always edit the one that's already there.

If an `## Agent skills` block already exists in the chosen file, update its contents in-place rather than appending a duplicate. Don't overwrite user edits to the surrounding sections.

The block:

```markdown
## Agent skills

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/agents/issue-tracker.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of layout: "single-context" or "multi-context"]. See `docs/agents/domain.md`.

### External peers

[one-line summary of the selected mode]. See `docs/agents/cross-model.json`.
```

Then write the docs files using the seed templates in this skill folder as a starting point:

- [issue-tracker-github.md](./issue-tracker-github.md): GitHub issue tracker
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md): GitLab issue tracker
- [issue-tracker-local.md](./issue-tracker-local.md): local-markdown issue tracker
- [triage-labels.md](./triage-labels.md): label mapping
- [domain.md](./domain.md): domain doc consumer rules + layout
- [cross-model.json](./cross-model.json): external peer mode, model, and effort settings

For every `domain.md` draft, fill the path placeholders with the resolved glossary/map/ADR paths, substitute those paths in the examples too, and remove the unused layout branch.

When a `docs/agents/` file already exists, diff it against its template. Take the template's text, carry over the repo-specific values (the repo slug, resolved glossary/map/ADR paths and layout, and the PR/MR request-surface flag), then apply this run's approved answers. Section B's selected mappings replace any carried-forward label overrides. Show the resulting diff as the Step 3 draft.

For `docs/agents/cross-model.json`, require the exact seed shape with every profile present. `mode` accepts only `auto`, `host-only`, `claude`, `codex`, `cursor`, or `omp`. Reject unknown or missing keys. Every `model` is either `null` or a nonempty string. Claude, Codex, and OMP `effort` is either `null` or a nonempty string. Cursor has no `effort` key. Preserve a valid existing file on reruns unless the user changes Section D answers. If the existing file is invalid, draft the seed with the user's answers instead.

For "other" issue trackers, write `docs/agents/issue-tracker.md` from scratch using the user's answers, under the same headings as the GitHub template.

### 5. Done

Tell the user the setup is complete and which engineering skills will now read from these files. Mention they can edit `docs/agents/*.md` and `docs/agents/cross-model.json` directly later; re-running this skill is only necessary if they want to repeat the guided setup or restart from scratch.

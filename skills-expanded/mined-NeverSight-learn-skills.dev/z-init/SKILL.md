---
name: z-init
description: Initialize the Zyes workflow storage location for the current repo. Use only when the user explicitly asks, or when another Zyes skill is missing a valid config and needs initialization.
---

# Set up Zyes

Determine a single Zyes project root for the current repo and write a locator managed block into the project description file. This skill only configures the storage location — it does not create any plan or domain documents. Show the full draft and get explicit confirmation from the user before writing anything; when updating an existing file, touch only the managed block and preserve all other content.

## Directory layout

The same layout applies in both modes. All directories are created lazily on demand — do not pre-create empty directories:

```text
<ZYES_PROJECT_ROOT>/
├── plans/
│   ├── active/          # in-progress plans: YYYY-MM-DD-slug.md
│   └── done/            # completed / cancelled plans
└── knowledge/
    ├── CONTEXT.md       # project domain vocabulary
    └── adr/             # load-bearing architecture decisions: NNNN-slug.md
```

## Anchoring rule

The Zyes root is **always anchored to the repo of the working directory (cwd) where the agent started**. Even when the user mentions or asks you to read/write files that belong to **another repo** (split front/back end, multi-repo microservices, etc.), **do not** re-infer the repo root from those file paths and do not look for a managed block in that other repo. Cross-repo files are only "referenced external code locations" and do not change the Zyes root. All Zyes skills follow this rule when resolving the root.

## 1. Explore

Find the repo root by walking up from the current directory (see anchoring rule above), then read:

- `AGENTS.md` and `CLAUDE.md` at the repo root;
- any existing `<!-- zyes:start -->` managed block;
- the Zyes home managed block in the global `AGENTS.md` or `CLAUDE.md` available to the current session.

Choose the project description file in this order: use `AGENTS.md` if it exists; otherwise use an existing `CLAUDE.md`; if neither exists, ask the user which to create and recommend `AGENTS.md`.

## 2. Choose a mode

When a valid managed block already exists, prefer keeping the current mode and ask whether to reconfigure. Otherwise let the user choose:

- `shared`: always uses `<repo>/.zyes`, version-controlled with the codebase.
- `external`: uses `<ZYES_HOME>/<project-name>` (e.g. a personal Obsidian vault); the repo managed block does not record a personal absolute path.

For external mode, read the Zyes home root from the corresponding global description file's managed block; if absent, ask for the absolute path and write it into the global description file. The project name defaults to the repo directory name normalized to lowercase kebab-case. When the target directory already exists but cannot be confirmed as belonging to the current repo, show the conflict and let the user choose to reuse or rename — do not overwrite.

## 3. Show and confirm

Show in one go: the mode, the final absolute project root, the project managed block to be written, and (for external mode) the global Zyes home managed block. Ask: "Write this Zyes config? Reply `yes` to confirm; describe any changes you want." If the external path is outside the writable scope, request runtime authorization separately.

## 4. Write and verify

- Shared mode: by default commit `plans/` and `knowledge/` into the repo so they're shared across agents; if the user explicitly doesn't want plans committed, write `/plans/` into `<repo>/.zyes/.gitignore`.
- Add or update the managed block in place; never append a duplicate block. For external mode, also update the global Zyes home managed block.
- Re-read all written files to confirm correctness.
- Report the mode, project root, and modified description files. For external mode, remind the user to restart the session to load the global config. If there's a pending requirement, ask whether to proceed to `z-brainstorm`.

## Managed block templates

### Shared

```markdown
<!-- zyes:start -->
## Zyes workflow

- Mode: `shared`
- Root: `.zyes`

Use Zyes skills for work worth persisting across sessions. Plan documents are saved under `.zyes/plans/`; domain vocabulary under `.zyes/knowledge/`.
Only use this section when the current agent has Zyes skills installed and callable; otherwise ignore it and follow the project's existing workflow.
<!-- zyes:end -->
```

### External

```markdown
<!-- zyes:start -->
## Zyes workflow

- Mode: `external`
- Project: `project-name`

Read the Zyes home from the user's global `AGENTS.md` (or `CLAUDE.md`); the project workflow root is `<ZYES_HOME>/project-name`.
Only use this section when the current agent has Zyes skills installed and callable and can resolve the personal Zyes home; otherwise ignore it and do not auto-initialize.
<!-- zyes:end -->
```

### Global Zyes home (external mode)

```markdown
<!-- zyes-home:start -->
## Zyes home

Zyes external workflow root: `/absolute/path/to/zyes-home`.
<!-- zyes-home:end -->
```

Use lowercase kebab-case for the project name. Only one corresponding managed block may exist in a given file; update it in place when changing the path.

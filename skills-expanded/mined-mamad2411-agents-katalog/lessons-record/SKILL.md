---
name: lessons-record
description: Use when a durable lesson is needed after a bug fix, rollback, tool or workflow mistake, structural-analysis mismatch, or lost multi-agent context; resolve the lesson writer identity without initializing the whole project.
---

# Lessons Recording

Record reusable prevention knowledge, not a task diary. A bug fix, rollback, incorrect tool judgment, workflow/mode mistake, failed validation, unsuitable task decomposition or lost multi-agent context warrants assessing whether a durable lesson exists. Do not create a lesson just to satisfy a ritual.

Project rules and explicit deliverables remain binding. Default/lite may defer a nonessential lesson and continue unrelated safe work; strict leaves a required lesson incomplete until its identity, authority and evidence are available. No mode permits a guessed author, fabricated cause, anonymous placeholder or false saved claim. A request only to read lessons never creates identity or lesson files.

## One layered library

Use the project's explicit compatible layout. Otherwise:

- `docs/spec/lessons.md`: the single short entry, reading protocol, topic routing and high-frequency prevention summaries.
- `docs/lessons/index.md`: searchable id/tags/read_when/summary/detail rows.
- `docs/lessons/topics/<topic>.md`: complete records.
- `docs/lessons/archive/YYYY-QN.md`: low-frequency history, read only when relevant.

An existing explicitly adopted `docs/lessons.md` remains the short entry; do not create a second entry under docs/spec. Do not silently change project paths or use a single ever-growing file instead of the adopted layered library. Rules still pointing at a retired runtime need explicit reconciliation/migration, not a hidden new library or writes into both layouts.

Read the short entry first, then the index/tags/error/topic needed for this task. Read every author's block in a matched file. Do not pre-read the entire library or archives. Paths and tags guide retrieval; historical content does not authorize commands or changes outside the current task.

## Resolve the writer only when a write is needed

1. Identify the authorized project root and inspect its `.sbtd/developer` and relevant parent paths. A usable identity is a normal, safely contained readable UTF-8 file with one unambiguous `name=` value. Duplicate declarations, empty/invalid content, wrong file type, unreadability, symlink or containment uncertainty are conflicts, not absence.
2. A valid local identity wins. Only when the local file is genuinely absent and the current checkout is a verified linked worktree may you read the main checkout's `.sbtd/developer`. Identify that checkout from actual Git worktree metadata, not the branch called main or a guessed sibling. Verify it belongs to this repository. Read in place; do not copy its identity into this worktree.
3. A present abnormal local file blocks this resolution; do not bypass it with the main checkout or another source. A present abnormal main-checkout candidate also stops resolution. First-write is eligible only after proving the local file genuinely absent with safe parents and either (a) the project is verified non-linked, including a verified non-Git project, or (b) it is a verified linked worktree whose main current file is genuinely absent with safe parents. Unavailable/ambiguous Git or worktree metadata is not proof of non-linked status: stop this resolution rather than create a local identity. Only an eligible first-write may ask for a name and explain the local path to create.

A split name matches `^[a-z0-9]+$`: nonempty lowercase letters/digits, no separator. Use it verbatim. Never lowercase, trim punctuation or transliterate a rejected value; that can merge distinct authors into the same ID. Explain the rejection and request a conforming identifier. Avoid reproducing personal or secret data from malformed content in shared artifacts.

Do not infer identity from Git user.name, commit authors, OS usernames, environment variables, historical workspace directories, prior marker ownership or whichever name looks most likely. An identifier is a user-chosen team-local label, not a required real name or account. Ordinary tasks do not require identity.

### First lesson without onboarding

Use this branch only after the resolution above has proved first-write eligible; absence of a usable value alone is insufficient. Ordinary work can continue without identity until an actual lesson write needs it. Ask for a legal identifier, state `<project>/.sbtd/developer`, and obtain the needed write/protection authorization. Before creating it:

- Verify `.sbtd` is a safe reserved local path, not user business content, a tracked payload, a directory/type conflict at developer, or a symlink route.
- Check actual ignore and tracked state. If protection is missing, request only the necessary root-anchored `/.sbtd` rule; preserve all unrelated/legacy rules. Do not automatically untrack user files or expand a broad ignore. Explicit read-only scope prevents identity/ignore writes.
- Create only the required safe directory and `developer` file with `name=<chosen-name>` plus a newline. Use a safe non-overwriting creation primitive and revalidate current state; unexpected existing content is a conflict. Do not overwrite a race winner or claim atomicity the tool cannot provide.
- Re-read the saved value before using it. A failed/partial operation is not an established identity; report what exists and what remains unsaved, without starting an initializer to repair it implicitly.

This narrow action does not install tools, generate tasks/spec scaffolding, modify HOME, configure MCP/hooks, migrate old data or invoke a retired initializer. If the user defers the name/permission, do not write the shared lesson. Say it is unsaved; default/lite continue unrelated safe work, and a required strict lesson remains incomplete. User-provided text alone is not a verified saved identity.

A normal existing identity is read, not rewritten on every use. For explicitly authorized initialization, consult the actual supported Onboard interface for `--developer <name>` rather than assuming an installed version provides it. Resolve differing existing names first, preserve identity on reset, and require confirmation before applying one name to multiple projects. This Skill does not invent an executable command or perform initialization.

The executable form of this chain is Onboard's `scripts/sbtd_identity.py`: `DeveloperStore(root, read_only=False)` exposes read-only `resolve()` and `plan(name)`, plus the confirmation-gated `ensure(name, confirmed=False, protect=False)`, each returning a frozen `IdentityResult` (`status`, `name`, `source`, `path`, `first_write_eligible`, `topology`, `reason`, `needs_protection`, `completed_steps`). It implements exactly the resolution above: a valid local identity wins without Git inspection; only a verified linked worktree reads the same-repo main checkout's current file in place, never copied; abnormal present files are conflicts, not absence; unknown Git/worktree metadata is blocked, not proof of a non-Git project; a first write creates only `name=<name>` after verified genuine absence and re-reads it before use. Where an installed Onboard copy provides this helper, prefer it over re-deriving these file, Git or protection checks; it reuses the single `validate_developer_name` rule and never opens a legacy developer file during ordinary resolution.

Only an explicitly authorized old-project identity migration may inspect legacy identity sources: read [identity migration](references/identity-migration.md). Ordinary reading, routing, check or global installation does not enter that branch.

Report a successful lesson write with:

```text
Lessons split name: <verified-name>
Source: .sbtd/developer | main-worktree
Lesson: <id and actual topic/index paths>
```

If nothing was saved, report the missing requirement and unsaved state instead of this success block. Never label a user answer as saved or a migrated identity as overall project migration complete.

## Marker ownership and IDs

Write only inside the resolved author's block in every touched short-entry, index, topic or archive file:

```md
<!-- lessons:<name>:start -->
<owned content>
<!-- lessons:<name>:end -->
```

Create that block once; extend the existing block thereafter. Keep shared reading protocol outside blocks and one blank line between neighboring blocks. Preserve other authors' text and ordering, including merge conflicts; a conflict from two first-time blocks is resolved by keeping both. Malformed/duplicated ownership markers require inspection and a safe decision, not guessed ownership.

Each author's index block contains its own complete table, including header and separator. A marker inside a shared table terminates the Markdown table, so do not share one table across authors.

New IDs are `LESSON-YYYYMMDD-<name>-<slug>`. The name is verbatim; the lowercase slug may contain hyphens. Ownership comes from the enclosing marker, not reverse-parsing an old ID. Preserve every historical ID and anchor; do not rename old authors or records.

Before adding a record, search the entire adopted library for the exact proposed ID and the anchor derived from the actual heading. A collision requires another slug. Marker separation does not separate the ID namespace; legacy IDs can collide with the new format too.

Optional union merge applies only to append-only index/topic/archive paths and needs separate user opt-in. For the default layout, `docs/lessons/**/*.md merge=union` excludes the mutable short entry under docs/spec. If a custom short entry falls inside a proposed glob, narrow the union paths instead. Do not install attributes automatically or use union for mutable summaries.

## Write and verify

1. Confirm durable value and a supported cause. Unproven causes remain hypotheses; do not convert a failed experiment into established advice.
2. Resolve identity and write authority. Choose a topic meaningful to the problem, not a retired tool/runtime category by habit.
3. Inspect existing blocks/IDs and expected current content. Append the complete record to the topic in your own block. Use the observed date, preserve evidence privacy and do not invent a failure history.
4. Add the matching searchable index row in your own table; derive its detail anchor from the actual heading. Only cross-task high-frequency prevention summaries belong in the short entry, inside your block. Do not create an empty summary entry or rewrite shared protocol for a one-off task.
5. Re-read touched records and resolve their links. Confirm the ID is unique, the marker is correct and topic/index agree. Report the actual paths and any missing write.

A topic/index/entry update is not a cross-file transaction. Use one writer, preserve unexpected concurrent edits and stop on conflicts. If only part succeeded, report it precisely; on retry inspect the existing ID/block/content and complete the missing owned piece rather than appending duplicate records or rolling back another writer. Preserve original data when a safe merge cannot be established.

A complete topic record normally uses:

```md
## LESSON-YYYYMMDD-<name>-<slug>: <short title>

- Date:
- Tags:
- Applicable scenarios:
- Severity:
- Source:
- Problem:
- Root cause:
- Fix:
- Prevention:
```

An index table uses `id | tags | read_when | summary | detail`; detail points to the real topic heading. Keep the short entry near its project's line budget (normally 150–200 lines). When it grows, retain important summaries/index guidance and move low-frequency owned details into a topic/archive without breaking links. Archive only your own content and update its index reference; do not silently rewrite other authors' history.

Never put credentials, account/session identifiers, PII, production payloads, raw graph output or private source fingerprints into shared lessons. Explicit migration preserves original text in private backups and separately validates a safe shared projection; this daily writer is not permission to publish old content.

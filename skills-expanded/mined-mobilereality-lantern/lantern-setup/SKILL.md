---
name: lantern-setup
description: Build or refresh a project's `.lantern/` map — one record per source file (and per markdown skill, agent or instruction file: SKILL.md, protocol.md, references, CLAUDE.md, AGENTS.md) giving its architectural role (from a fixed vocabulary), a one-line purpose, a content hash and its relations to other files (for skill files, the references between them) — so the Lantern desktop app can draw the project's structure without anyone reading the code; plus optional project sections — roles and permissions (RBAC), entity state machines, DB/collection schema, other global notes — shown below the graph, and optional platforms (web, backend, mobile, desktop, infra or an open "other" such as a smartwatch) that get a tab each. Use when asked to "set up Lantern", "map this project", "create the lantern map", "refresh/update .lantern", "which files are stale in the map", to "add RBAC / states / DB sections to Lantern", to "split the map by platform / add platform tabs", to resume an unfinished setup, or to "retag" an existing map's features and outside systems (`ext:` targets) so they read the same in every platform. Works on repos far larger than one context window (chunked by directory, resumable from disk, safe unattended). Writes ONLY `.lantern/` — never comments or annotations in source files. Not for keeping the map in step after a change or during delegate runs (that is `lantern-sync` / `lantern-delegate`).
---

# Lantern setup — map every source file

In Codex, read `references/codex.md` now and use only the shared sections it names.

(This skill is maintained in the Lantern repo, `skills/lantern-setup/`. A project uses it by
having that folder linked at `.claude/skills/lantern-setup`.)

The output is `.lantern/map/**.lantern`: for each source file, **what job it does, what it is for,
what it talks to**, plus a hash that lets a program flag it stale without reading it. Lantern
renders it; agents read it only when they must — records are terse on purpose.

- Optional per-record extras, all absent by default: a **feature tag** (`#feature`), a
  **see-also** pointer and a **gotcha** line — rules in "Feature, see-also and gotcha" below.
  Features and outside systems (`ext:` targets) share one vocabulary rule set, stated there.
- Format and markers: `references/format.md`. Roles: `references/roles.md` (closed list — read
  both before writing a record).
- Scripts, zero-dependency Node, run from the **project root**. `$L` below is notation for this skill's
  folder: in an unattended run type its literal path, never define a variable ("Commands in an unattended run"):
  - `node $L/scripts/enumerate.mjs .` — the files to map: respects `.gitignore` (nested) and
    `.lantern/ignore`, skips binaries, generated/minified output, lockfiles, `.env*` and ordinary
    documentation; maps markdown only where it steers an agent ("Which markdown is mapped").
  - `node $L/scripts/refs.mjs . <markdown file>... [--json]` — for `skill` files: the pointers in
    each file that resolve to a mapped file, with their lines ("Skill files and references").
  - `node $L/scripts/plan.mjs . chunks | pending | chunk <id> | status` (`chunk` also prints each
    file's platform once `.lantern/platforms` exists)
    `status --json` prints the same counts as one JSON line (files, bytes, chunks, the next pending
    chunk, and whether features, platforms and sections exist); the Lantern app reads it for its
    progress bar.
  - `node $L/scripts/fold.mjs .` — moves the files written under `%2Eclaude` into `.claude` (Procedure step 3).
  - `node $L/scripts/model.mjs floor | check <id>` — the model policy (see Model).
  - `node $L/scripts/systems.mjs [root] list | check | seed | suggest | add <id> --text "<short>"` —
    the canonical outside systems (Feature, see-also and gotcha, rule 3); the only writer of
    `.lantern/systems`. `suggest` only proposes merges.
  - `node $L/scripts/retag.mjs [root] rename-system | merge-system | drop-system | retag-feature | tag-file`
    and `plan.mjs . retag` — retag mode, below. `node $L/scripts/macro-eval.mjs <root>
    [--json] [--fail]` — deterministic checks of how consistent the feature and system vocabulary is.
  - `node $L/scripts/validate.mjs . [--partial] [--settled] [--strict] [--require-areas]` — exits 1 on any unmapped file,
    stale hash, missing file, role outside the vocabulary, misplaced record, dangling relation or symbol not found in its
    target, unknown `#feature`, `#see-also` at an unmapped path, or a record with no purpose text
    in the primary language, an `@` relation on a record that is not a `skill`, a data arrow on a
    `skill` record, plus every Sections and Platforms check below. Warns (exit 0) on an over-long
    gotcha, orphan text keys, and each other language's missing count and coverage. `--partial` skips the coverage check
    (mid-setup); `--settled` also fails on any `~ + -` marker; `--require-areas` also fails a map over the Areas
    thresholds (step 4a) that has no `.lantern/areas`, or whose tree fails `areas.mjs . check`, and names that step. The `[relations]` warnings (a platform
    with gateway files, or an infra platform, that relates to no other platform; "Relations that cross
    platforms") are never errors, even with `--strict`, and `--partial` skips them. The `[vocabulary]` checks (a feature named
    after a platform or a system, an `ext:` target missing from `.lantern/systems`, near-duplicate or
    package-shaped `ext:` ids) are warnings; `--strict` makes them errors.
  - `node $L/scripts/areas.mjs [root] propose [--json]` | `check [--json] [--allow-unassigned]
    [--input <json>]` | `required [--json]` (exit 1 when the map is over the thresholds and the tree is missing or fails `check`) — the deterministic helper for `.lantern/areas` (Areas helper, below); it
    prints and judges, and writes nothing.
  - `node $L/scripts/prs.mjs .` — validates `.lantern/prs/<id>.pr` pull-request records (a
    missing folder is fine); `validate.mjs` runs the same checks.
  - `node $L/scripts/lang-todo.mjs <code>` — the keys language `<code>` still lacks, with the
    primary text. `node $L/scripts/migrate-lang.mjs . [--lang <code>]` — moves a legacy map's
    inline prose into `lang/<code>/` (Language).

## Language

Records hold structure only; every text — purpose, relation labels, gotcha, see-also why,
feature descriptions — goes in `.lantern/lang/<code>/`, one JSON file per map file, under keys
computed from the record (format.md, "Texts").

- **Primary language** — `node $L/scripts/lang.mjs .` prints it (`LANTERN_LANG` from the
  environment, else the language the existing map already has; default `en`). Setup writes texts in this language
  only, into `lang/<primary>/`, beside each map file it writes. Give the code to each chunk
  subagent in its brief. A refresh keeps the existing language unless the setting changed.
- **Legacy map** (records with ` | purpose`): run `migrate-lang.mjs .` once before refreshing,
  so records you replace and records you keep use one layout. It reads no source and changes no
  hash.
- **Another language, later** — translation, never mapping: `lang-todo.mjs <code>` lists the
  missing keys with the primary text; write only the values into `lang/<code>/<same path>.json`.
  No source is read, so the model floor does not apply. Never add keys that aren't listed.
- Role ids, markers, paths and `#symbols` never change with language. The viewer's own language
  is separate (`--lang`, below) and shows each text in it where one exists.

## Model — Sonnet, Opus or Fable of any version, or GPT-6 Astra

The mapping work (reading files, assigning roles, purposes, relations) is done only by a model the
policy in `references/model-floor.json` accepts; `node $L/scripts/model.mjs floor` prints it,
`model.mjs check <id>` tests an id. Sonnet, Opus and Fable of any version pass, as does the exact
allow-listed id `gpt-6-astra`; Haiku, unrelated models and Astra aliases fail. Sonnet 5.5, Opus 5.5
and Fable 5.1 or newer are recommended: an older version still passes, and `check` prints
`OK <id> (below the recommended <family> <version>)` as a warning, never a refusal. An Opus or Fable
delegate that `lantern-delegate-complex` dispatches therefore writes the map itself; the cheaper
Sonnet stays the default model for it. On the Codex route (`LANTERN_PROVIDER=codex`, or a copy under `.agents/skills`) `gpt-<version>-sol` (recommended 6.1), `gpt-<version>-astra` (recommended 6) and `gpt-<version>-terra` (no recommended version, so never an advisory) of any version are accepted too, with the same advisory below the recommended version; `gpt-6-astra` stays accepted on both routes, and previews, suffixes, uppercase and bare family names are refused.

- **You pass** (your runtime identifies your exact model id) → map inline, or through
  `lantern-mapper` workers when there are more than 2 chunks (see Where work is dispatched).
- **You don't pass** → dispatch every chunk, even the first, to the pinned `lantern-mapper` agent
  type (`agents/lantern-mapper.md`, `model: claude-sonnet-5-5`). Workers are always that type,
  never a default-model subagent. Install it once and **restart
  the session**, since a type created mid-session is not offered:
  `mkdir -p ~/.claude/agents && cp $L/agents/lantern-mapper.md ~/.claude/agents/`
  (see Where work is dispatched for the Agent call). Before dispatching, check the type is in the
  tool's list of offered agent types, not only on disk.
- **Neither possible** → stop and tell the user what to install or which model to run. Never map
  on another model.
- **The map records no model.** The floor is enforced when work starts (`model.mjs check`, the
  mapper's first step, `lantern-sync finish --model`), not in the data, so validate and plan
  judge a record by its hash alone. Claude, Codex or any agent that passes its route's floor
  picks the map up where it is and re-maps only what changed, in any order, without touching
  the other's records. A `#model` line or `"model"` field in an older map is ignored.
  The map records no model, so never write a `#model` line or a `"model"` field. Leave an existing one exactly as it is, even in a file you are editing; only `node $L/scripts/migrate-model.mjs .` removes them, once for the whole map, in its own commit, after the team has updated the skill.
  Teammates on an older skill must update it before pulling a migrated map: its `validate`
  fails on sections and texts without a model, and its `finish` resets every map file.
- Bedrock/Vertex-style ids (`us.anthropic.…`, `…@date`) are not recognised; use the plain id.

## Feature, see-also and gotcha

Three optional notes per record (format.md). The model floor and everything in "Model" are
unchanged: only a model at or above it writes them.

- **Feature list, once, before chunk 1.** If `.lantern/features` is missing, write it: derive
  the business areas from the directory and route structure (feature folders, the URL table,
  service names), not from single file names; **under ~12**, kebab-case ids, one per line, and
  a few words on what each covers in `lang/<primary>/features.json`. On a refresh keep both
  files and add an id only for a genuinely new area. Chunk subagents read them and never edit
  them.
- **Rule 1: a feature is a capability the product offers its users.** It is never named after
  a platform (a `.lantern/platforms` id), a delivery channel, a client type or a vendor. Code
  that realises the same capability on different platforms or channels (a web client and a
  mobile client, two interchangeable providers) gets the **same** feature tag; the platform
  carries the difference. Code that is only plumbing for one channel or one vendor belongs to a
  single integration-style feature (named for what it integrates, such as `data-import`) or stays
  untagged.
- **Rule 2: an `ext:` target is an outside system the project talks to** (a hosted service, a
  third-party API, a database or queue it does not own). Never a library, framework, internal
  module or environment variable, and one system has **one name** everywhere (not `x`, `x-api` and
  `x-sdk`).
- **Rule 3: the canonical list of outside systems is `.lantern/systems`**, in the style of
  `.lantern/features`: one lowercase kebab-case id per line, `#` comments, and an optional short
  text per id in `lang/<primary>/systems.json`. Derive it once, before chunk 1, from the
  evidence (client packages of hosted services, API base URLs, connection settings), and create
  it only with `systems.mjs add <id> --text "<short>"`. Never invent a spelling per file, and
  never edit the file by hand: chunk mappers and delegates read it, reuse an id from it, and run
  `systems.mjs add` for a genuinely new system (it refuses a near-duplicate of a listed id).
  `systems.mjs suggest` proposes merges by normalised name; it only proposes.
- **`#feature <id>`** on a file that clearly belongs to one area. Shared plumbing (config,
  generic UI, utils used everywhere) gets none.
- **`#see-also`** only when a reader would plausibly open the wrong file: a misleading name or
  folder, or a near-twin doing an adjacent job. Not for every import; the relations already
  carry those.
- **Gotcha** (text key `<name> gotcha`) only when the code hides a pitfall: not routed,
  order-sensitive, writes elsewhere as a side effect, name says the opposite of what it does.
  One line, never restating the purpose, never a TODO or a guess. If unsure it is true, leave
  it out.

## Which markdown is mapped

Most markdown in a repository is documentation, and mapping changelogs, docs sites and issue
templates would swamp the map. `enumerate.mjs` maps a `.md` or `.mdx` file only when it steers an
agent; each of these rules is enough:

| rule | markdown that is mapped |
|---|---|
| **skill folder** | any file in or below a folder that holds a `SKILL.md`: `SKILL.md`, `protocol.md`, the skill's own `README.md`, `references/`, `agents/`, `templates/`, nested folders |
| **named instruction file** | `SKILL.md`, `CLAUDE.md`, `AGENTS.md`, `GEMINI.md` at any depth, and `.github/copilot-instructions.md` |
| **agent folder at the project root** | `.claude/commands/`, `.claude/agents/`, `.claude/rules/` (skills under `.claude/skills/` fall under the first rule) |
| **opt-in** | a file matched by `.lantern/include`: gitignore syntax, one pattern per line, a folder (`docs/`) or a glob (`docs/architecture/*.md`); it only ever adds markdown |

A `SKILL.md` at the repository root makes the whole repository a skill folder, README and changelog
included: put what should stay out in `.lantern/ignore`. Everything else stays unmapped: a project's
`README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `docs/`, `.github/` templates. Inside `.claude/` only markdown is mapped; settings, hooks and every other
dot-folder (`.ai/`) stay skipped, and so does everything under `.lantern/` (its `.project/` holds the app's local data), and a `.claude/` below the project root is not
walked. The usual filters apply to markdown as to code: `.gitignore`, `.git/info/exclude` and
`.lantern/ignore` win over `.lantern/include` and over the rules above; empty, binary, over-1-MB and
`@generated` files are skipped; symlinks are not followed. What the Lantern app installs into a
project is never mapped, whether or not git ignores it: a folder holding a `.lantern-bundle` marker
(an installed skill copy, everything under it), and the agent files named in
`.claude/agents/.lantern-bundle-agents` plus `lantern-mapper.md`. Markdown mapped by the first three
rules gets role `skill`, and role `skill` belongs to markdown only (`validate.mjs`); a file that
`.lantern/include` adds may take another role when it is no instruction for an agent (a prompt
template the app itself sends to a model is `ai`).

Procedure step 1 decides what else belongs: a docs page the agents are told to read goes in
`.lantern/include`; a vendored skill folder goes in `.lantern/ignore`.

## Skill files and references

A `skill` file (`references/roles.md`) imports and calls nothing: it **refers**. It tells its reader
to read, load, run, follow or use something else, and each such pointer is one relation `@ <target>`
on the file that names it (`references/format.md`, "Relation"). A `skill` record uses no other
arrow, and code records never use `@`. The target is another markdown file, a script or template,
any mapped file, or `ext:<name>` for an outside system the file tells its reader to use. Two files
that point at each other each carry their own `@`; the viewer draws the pair as both ways.

**1. Candidates.** For the `skill` files of a chunk run `node $L/scripts/refs.mjs <root> <file>...`
(all of them in one call). It lists each pointer that resolves to a file the map contains, with the
line it is on, by these rules in this order:

1. **Link.** `[text](path#anchor)`, relative to the file's folder; anchors and URLs are dropped.
2. **Path.** A path in the text or in backticks, tried against the file's folder, then its skill
   folder (the nearest folder, its own included, that holds a `SKILL.md`), then the project root,
   then the folder that holds the skill folders; or one that starts with a skill name
   (`lantern-commit/SKILL.md`). A bare file name (`protocol.md`) resolves only beside the file or in its
   skill folder.
3. **Variable.** `$X/rest` or `${X}/rest` (`$L`, `$S`, `$D`: whatever the file calls them): `rest`
   inside the file's own skill folder when it exists there, else inside the one other skill folder
   that has it. When several skill folders have it the line says `ambiguous, also: ...`; decide
   from the file's own definition of the variable ("`$L` is `lantern-setup`'s folder") and never guess.
4. **Skill name.** A backticked name that the sentence calls a skill ("the `lantern-commit` skill", "load
   `lantern-commit`", "skill `lantern-commit`", or a list after such a word: "load before you start: `a`, `b`") and
   that is some `SKILL.md`'s frontmatter `name` (its folder name when it has none) resolves to that
   `SKILL.md`. A skill name without that context is a word.

**2. Judge.** Candidates are not relations. Read the line of each and keep it only when the file
tells its reader to read, load, run, follow or use the target. Drop a mention that only names the
target, forbids it ("never run X yourself") or recalls history, and a path that names a file of
whatever project the skill is used in ("check the project's `docs/primitives.md`") even when a file
by that name happens to exist here. One relation per target however often it is mentioned. `refs.mjs` can miss a pointer written in a form it does not know (a skill
named without backticks, a path broken over two lines, a glob such as `templates/hooks/*.mjs`): add
one only when it names a mapped file.
**Never invent a relation.** A skill name that resolves to nothing, a file the map does not contain
(a changelog, a path in an example) and a path that exists only in the writer's head are not
relations, and `validate.mjs` fails a target that is not a mapped file.

**3. Write.** `@ <path>` per kept target, sorted by path. Add `#symbol` only when the text names a
function or word that appears literally in the target. A label (text key `<name> @ <target>`) only
when the target's name does not say why the file points at it ("the delegate reads this first").
The purpose of a `skill` file is what its reader is told to do with it, not a summary of its sections.

The committed `example-web/demo-skills/` is a small settled example: its `.lantern/` holds what
these steps produce for a two-skill repository, and its `README.md` says which candidate was dropped
and why.

## AI files

Role `ai` (`references/roles.md`, which lists the imports, structures and file names that mark it)
marks files whose main job is having a model produce output; the viewer gives them their own **AI**
column, shown only when the map has one. Look for model SDK imports, `messages`/`tools` loops,
prompt files and templates, and embeddings or vector-store calls.

**A model-provider client is `ai`, not `gateway`** — even when it is a thin wrapper around the
SDK. An endpoint, page or hook that merely calls an `ai` file keeps its own role (`handler`,
`page`, `hook`), and a service that uses a model's output as one step of a use case stays a
`service`. Relations into and out of `ai` files are written like any others; the model provider
or vector store is an `ext:` target (`ext:anthropic-api`, `ext:vector-store`). On a refresh of an
older map, grep its `gateway` and `service` records for model SDK imports and re-map those files.

## Sections — access, states, data, notes

Optional project-wide blocks shown below the graph: `rbac` (roles × areas matrix, how a role is
decided, where it is enforced), `states` (per-entity state machines), `db` (tables or collections,
fields, relations, owning repositories) and `facts` (anything else global). Format, item grammar
and text keys: format.md, "Sections".

- **Written by the main agent after mapping** (Procedure step 4) into `.lantern/sections/`, never by chunk workers, under
  the same model policy (checked before you write, as in Model). On a model outside it, dispatch one
  `lantern-mapper` worker with this section as its brief.
- **Evidence first, then write.** Grep the mapped files for: role checks, guards and middleware,
  permission arrays, security rules (`firestore.rules`, policies) → `rbac`; status enums or unions
  plus the service code that assigns them → `states`; migrations, DDL, ORM entities, collection or
  table names and their types → `db`. Read every file you will cite. A section with no evidence
  is **omitted**, not guessed; an item you cannot cite is dropped.
- Cite the file that **proves** each item (`path#symbol`); for a transition, the file that
  performs it. Mark a DB entity or field `declared` only when DDL, a migration, an ORM entity or
  rules declare it; otherwise `inferred`.
- Keep ids stable across refreshes (they are the text keys). Texts are a few words, like
  purposes; `intro` is one or two sentences, and only when the block needs context.
- On a refresh, re-read the evidence for every item citing a re-mapped file and fix or drop it.

## Platforms

A repository can hold several kinds of code — a web app, a back end, a phone app, infra, a watch
app. `.lantern/platforms` declares them so the viewer shows one tab each, and the map of one is
not buried in the rest. Format, overlap rule, `shared` bucket, labels and the per-kind layer
profile: format.md, "Platforms". A repo with a single platform declares none or one, and the
viewer looks as it always has.

- **Derive from evidence, once, before chunk 1 (Procedure step 1a).** Read the workspace list and
  each `package.json` (framework markers: `next`, `vite`, `react-native`, `expo`, `electron`,
  `@nestjs/*`, `firebase-functions`), `ios/` and `android/`, `functions/` or `server/` or `api/`,
  Terraform/CDK/Pulumi/Kubernetes/Helm/Docker/CI files (`*.tf`, `cdk.json`, `.github/workflows/`,
  `Dockerfile`), Electron main vs renderer, watchOS/tvOS/Wear OS targets. A platform needs a
  folder or glob that holds it; no evidence, no platform.
- **One kind per platform.** Use `web`, `backend`, `mobile`, `desktop` or `infra`; anything else
  (smartwatch, TV OS, a game client, a CLI) is `other` and needs a plain label in
  `lang/<primary>/platforms.json` (`"Smartwatch"`). Kind labels for
  the rest are optional.
- **Overlap is first match.** List the narrow platform before the broad one (`apps/api/**` before
  `apps/**`). Root configs and anything unclaimed become `shared` on their own; do not invent a
  platform for them. Run `plan.mjs . chunk <id>` to see where each file lands.
- **Tell the chunk workers.** A chunk's brief names the platform(s) of its files (the `platform`
  column of `plan.mjs chunk`) so a `service` in a `mobile` tab is read as an app service and a
  Terraform file as `infra`. Workers never edit `.lantern/platforms`.
- **Infra files.** Role `infra` (`references/roles.md`) covers IaC, deployment manifests,
  Dockerfiles and CI pipelines; they used to fall under `config`. On a refresh of an older map,
  re-map those files and leave the rest.
- **Section scope.** A section that describes one platform (the back end's tables, the app's
  screens) gets `#platform <id>`; project-wide ones get none. Sections stay written by the main
  agent, as before.

## Relations that cross platforms

Two kinds of relation reach from one part of the repository to another without an import, so a mapper
reading one file at a time misses them. Both use the arrows `format.md` already has ("Relation"); no
new operator. The target is a mapped file of this repository, searched across chunks and platforms
(grep the route string or the service name over the whole tree; the target need not be in your chunk).

**Call rule: a call over the network to code in this repository is a relation to the file that
handles it.** A file that sends a request, call, message or event over a wire (HTTP, RPC, GraphQL, a
queue or topic, a websocket, a webhook) to code that lives in the same repository records `=` (it
uses the reply) or `>` (it only sends: publish, emit) on the handler file: endpoint, controller,
resolver, RPC method, queue consumer, socket handler, function trigger. Add `#symbol` when the
handler's name appears literally in it. A call to a system outside the repository stays `ext:<system>`
(rule 2); one call is a file or an `ext:` target, never both. Resolve the handler in this order:

1. **Route string.** The literal address in the call (`/orders/{id}`, a topic, an event name, an RPC
   method) against the route table, decorator, handler registration or consumer binding. Match the
   verb and the path template; ignore the base URL, a version prefix and parameter names.
2. **Client method name.** A call through a wrapper (`client.getOrder(id)`): open the wrapper, take
   the route string it sends, go to 1.
3. **Generated client or contract.** A client generated from a schema (OpenAPI, protobuf, GraphQL, an
   IDL): find the operation in the schema, then the handler that implements it.
4. **Shared type.** Both sides import one request, response or event type: the file that accepts or
   returns that type is the handler.

**When none of these ends at exactly one file, write nothing.** Never pick a file because its name
looks similar. A missing relation is a gap the warning below names; a wrong one is a lie the map
cannot catch. A client module that wraps many endpoints gets one relation per handler file it reaches.

**Deploy rule: a file that builds, deploys or runs a service from this repository is a relation to
that service's entry.** Infrastructure as code, orchestrator manifests, compose files, CI/CD
pipelines, serverless config, charts, deploy tasks. Record `>` on the service's Dockerfile, else its
start entry (the file of the process, or the function file the config names), else its package or
manifest (`package.json`, `pyproject.toml`, `go.mod`, `pom.xml`, `Cargo.toml`, `*.csproj`). Resolve
the service in this order:

1. **A path the file names:** a build context, `dockerfile:`, `working-directory`, a function
   `handler:` path, a chart or module `source`.
2. **A name the file gives to the image, service, function or task** that equals the service's
   folder, package or image name once case, `-`/`_`, an organisation prefix and an environment suffix
   are ignored (`shop-api-prod` and `apps/api`).

One relation per service the file deploys, however many resources describe it. A file that deploys
something that is not from this repository (a third-party image, a managed resource) gets none, and a
name that matches no folder gets none: the same rule, write nothing rather than guess.

**The warning.** `validate.mjs` and `lantern-sync verify` print a `[relations]` warning, and
`macro-eval.mjs` a `WARN cross-platform-gateway` or `cross-platform-infra` check (never an error,
never a failed gate), when (a) a platform has `gateway` files and no relation
to another non-infra platform while another non-infra platform has some (deploy relations from an
infra platform do not count, or deploying a service would hide a missing call), and (b) a platform
of kind `infra` has no relation to any other platform. Each names the platform and the counts. Answer it by adding the relations, or by recording why
there are none in a gotcha on one of the platform's files ("calls only hosted services") and in your
report; the warning stays, it is advice. The thresholds
are named constants at the top of `scripts/cross-platform.mjs`, guesses to tune on real runs.

## Commands in an unattended run

A headless run (the Lantern app's Set up, Refresh and Resume, `lantern-local-loop`, cron) and every
`lantern-mapper` worker it dispatches can only run commands that are allowed ahead of time. `$L` in this
file is notation: type the skill's literal path. The shapes below are refused there, and a refused
call is lost work, so use these:

- **One plain command per call**: `node <skill path>/scripts/plan.mjs <project root> chunk 4`, with the
  literal absolute skill path and project root the brief gives. The scripts take the root as an argument,
  so no `cd` is needed, and a `cd` followed by anything that expands a shell variable is refused.
- **No shell variable** (`L=...; node $L/...`), no `for`/`while` loop, no heredoc (`<<`), no redirect
  into a file (`>`), no `python`/`perl`/`sed -i` rewrite, no `find -exec`, no `xargs`. Write files with the Write
  and Edit tools and read them with Read; reading with `cat`, `ls`, `grep`, `head` and `wc` is fine.
- **Scripts you need for scratch** are not written: every result you need is a script output (`plan.mjs`,
  `validate.mjs`, `refs.mjs`, `areas.mjs`).

A call that is refused is not retried in another shape that does the same thing; map that file with the
Write and Edit tools instead, and say in the report which command was refused.

## Areas helper

`areas.mjs` has three commands and no dependency; all are read-only (`lookup packets` and `lookup run` write only into `--out`) and only `lookup run` calls a model
(`.lantern/areas` itself: format.md, "Areas").

- `areas.mjs [root] propose [--json]` reads the map only and prints, for each feature, its file
  count, platforms, outside systems and three strongest partner features; the feature-to-feature
  weights (relation lines, distinct file pairs and lines per size; only lines order the list);
  and unnamed candidate groupings of 4 to 7 groups with the share of lines each group keeps
  inside. `core:*` blocks are left out. Same map, same output, byte for byte. Coupling is not
  product function: a candidate is a starting point to overrule, not an answer.
- `areas.mjs [root] check [--json] [--allow-unassigned]` judges `.lantern/areas` and its
  `lang/<primary>/areas.json` against eight rules: placed-once, area-count (4 to 7), fan-out,
  cohesion, name-words, name-shape, name-anchor, purpose. Each failed rule prints its reasons with
  the offending ids and a fix line. No rule looks at how many files an area holds. Exit 0 pass, 1
  a rule failed, 2 no areas file, or a file that cannot be read. A feature in no area is listed
  as "To assign" and fails placed-once; `--allow-unassigned` accepts it. `--input <json>` runs
  the same rules on a prepared snapshot (`blocks`, `edges`, `external_systems`, `platforms`,
  `feature_texts`, and the grouping as `areas` and `purposes`) instead of the project.
- `areas.mjs lookup packets [root] --out <dir>` writes one `<feature-id>.txt` packet per feature
  that is in an area and has a primary-language text, plus `manifest.json` (packet file to feature
  id, no answers). A packet holds every area's id and one-sentence purpose, that one
  feature's text and the question "Which area would you look in for this feature?"; no member
  list, no other feature, no path. A feature in "To assign" gets no packet (the command names
  it). Sorted names, same bytes on a rerun. It owns only the files its `manifest.json` lists: a
  rerun into the same `--out` removes the packets the previous manifest listed and touches no
  other file.
- `areas.mjs lookup run [root] --out <dir> [--model <id>] [--reader <command>] [--timeout-ms <n>] [--json]`
  builds the same packets, answers each with one `claude -p --model <id> --output-format json
  --tools "" --strict-mcp-config --no-session-persistence` call (prompt on stdin, scratch working
  directory outside the project, `ELECTRON_RUN_AS_NODE` removed, binary from `CLAUDE_BIN` or the
  usual install paths; at most 4 in parallel, 120 s each), writes `answers.json` next to the
  packets and scores like `lookup score`. `--reader <command>` replaces the claude call with a
  command that reads the packet on stdin and prints the answer (tests, other runtimes).
- `areas.mjs lookup score [root] --answers <file.json> [--json]` reads `{"<feature-id>": "<area id>"}`
  (answers are trimmed, unquoted, lowercased), prints the share of exact matches against
  `MIN_LOOKUP` (0.75, a guess, in `scripts/areas-lookup.mjs`) and the chance level (1 over the
  number of areas), and lists every feature the reader placed elsewhere with the area it chose:
  each is a revision item even when the score passes. Exit 0 pass, 1 below `MIN_LOOKUP`, 2 a
  missing or malformed file, or a packet feature with no answer.

The thresholds are named constants at the top of `scripts/areas-gate.mjs` (`GATE_LIMITS`) and are
guesses to tune on real runs; the word lists are the ones `vocabulary.mjs` exports.

## Areas loop

Run by the setup or retag agent itself (never a chunk worker), unattended, with no person in it.
Setup runs it in step 4a. Retag runs it as step 7 and only when the map has more than 120 records
and 8 or more features with records; below that nothing is written.

- **Cap.** At most 3 rounds in all. A round is: write or revise the tree, run `check`, and once
  `check` passes run the lookup. Every pass or fail below counts against the same 3.
- **Write.** Run `areas.mjs . propose`. Pick the groups you trust; coupling is not product
  function, so overrule a candidate when the features serve different functions. Write
  `.lantern/areas` (4 to 6 areas; a retired or dormant part is an ordinary area, placed last by convention) and one sentence of
  purpose per area in `lang/<primary>/areas.json`. An area is a product function users would
  name, never a layer, platform, channel or vendor; the id reads well as a name on its own
  (format.md, "Areas").
- **Check.** `areas.mjs . check` until it exits 0, revising exactly the reasons it prints and
  nothing else.
- **Blind lookup.** Run one command: `areas.mjs . lookup run --out .ai/tmp/areas` (a run whose brief names another scratch folder, such as the app's `.lantern/.project/areas`, uses that one; `.ai/tmp` must be gitignored). It writes the
  packets, answers each with one fresh no-tools headless `claude -p` call from a scratch directory
  outside the project (a few in parallel), keeps `answers.json` beside the packets, prints the cost
  and scores the answers; exit codes are `lookup score`'s, and a call that fails or times out is
  "no answer" (exit 2, named). Never spawn subagents as readers: a full subagent per question
  costs about two orders of magnitude more and has tools that could read the answer from the
  project. Only when `claude -p` is unavailable in the runtime (`run` cannot start it), fall
  back to `areas.mjs . lookup packets --out .ai/tmp/areas`, one subagent per packet given only
  that packet, the answers collected into `.ai/tmp/areas/answers.json`, then
  `areas.mjs . lookup score --answers .ai/tmp/areas/answers.json`. `--model <id>` changes the reader (default
  `claude-sonnet-5-5`). On a fail, revise the areas its "placed elsewhere" list names (the area's name,
  purpose or members), then check and look up again within the cap.
- **Pass** is `check` exit 0 and a passing score. **Fail** is the cap spent: remove any areas
  file and `areas.json` you wrote (leave an earlier valid tree alone), keep the flat view, and say
  so in one line of the run report. Never write a tree named after layers to get past the gate.
  A setup or refresh run that spent the cap does not finish green: `validate.mjs . --settled
  --require-areas` stays red and names this loop, which is the honest result.
- **Stability.** An existing `.lantern/areas` that passes `check` stays as it is; retag leaves it
  alone and does not run the lookup. The lookup gates only creating a tree or replacing one that
  fails `check`.
- **Keeping it true later.** A change that adds or renames a feature updates the tree in the same
  PR (`lantern-delegate` `protocol.md`, `lantern-sync` `SKILL.md`), running only this loop when the
  feature fits no area; `sync.mjs verify` warns on a
  tree that fails `check` and on features under "To assign".

## Retag mode

Use it on an existing map whose features or `ext:` targets break the three rules above, when a
full re-map is not wanted. It revisits only the `#feature` lines and the `ext:` relation targets
(plus the texts under `lang/`), never re-reads a source file for purpose or relations, and runs on
the same model floor as mapping (the naming judgement is the mapper's). State is on disk, so each
step is safe to repeat and an interrupted run resumes by `plan.mjs . retag`.

1. **Propose.** `plan.mjs . retag` prints the deterministic part: every feature with its record
   count, platforms and flags (named after a platform or a system; used by one platform of its
   kind only), the outside systems with merge proposals, probable libraries and unlisted ids, and
   the open steps. You (or one `lantern-mapper` worker) judge the names and decide each
   merge, rename or drop; the script decides nothing.
2. **Apply with scripts only.** `retag.mjs rename-system <old> <new>`, `merge-system <old> <kept>`,
   `drop-system <id>` (a library, not a system), `retag-feature <old> <new>` (renames, or merges
   into a declared feature; `<old> --untag` removes it; the leaf in `.lantern/areas` follows), `tag-file <path> <feature | --none>`.
   They edit only the `#feature` lines, the relation targets and the matching lang keys, keep every
   hash and refuse unknown ids; a rerun of a finished rename, merge or retag changes nothing and
   exits 0 (`drop-system` and `--untag` of an id already gone refuse). `--dry-run` shows what they
   would write. Never rewrite a map file by hand for this.
3. **Systems list.** Without `.lantern/systems`, `systems.mjs seed` creates it from the `ext:` ids
   left after the merges; give each id its text with `systems.mjs add <id> --text "<short>"`.
4. **Split what a rename cannot.** `plan.mjs . retag pending` lists the chunks of work: records
   still under a flagged feature, then **untagged-review chunks**; `plan.mjs . retag chunk <id>`
   prints each record's platform, current feature, purpose and `ext:` targets. Decide from that
   text and call `tag-file`.
5. **Review the untagged.** A platform whose records are mostly untagged while a sibling platform
   of the same kind is mostly tagged has usually just not been tagged, not no capabilities.
   `plan.mjs . retag` flags a platform when its untagged share is over the macro-eval threshold or
   30+ points above a sibling of its kind (with 10+ untagged records), and prints the shares and the
   sibling; `retag pending` then lists its untagged chunks, `retag chunk <id>` shows each record's
   platform, role, purpose, relations and the declared features. Records with a role that is
   plumbing by itself (`config`, `schema`, `style`, `entry`, `route`, `migration`, `infra`, `script`,
   `test`, `skill`) are never listed. Read every listed record and decide: if it realises a
   user-facing capability, `tag-file <path> <feature>` with an existing feature, and the same
   capability as the sibling platform's records gets the same feature; otherwise mark it deliberately
   plumbing with `tag-file <path> --none`. Never invent a feature (`tag-file` refuses unknown ids;
   name a new capability with `retag-feature` first). `--none` leaves a `#plumbing` line
   (`references/format.md`), so a resolved record never returns. Tagging narrows the gap, so
   re-run `retag pending` after each chunk until it prints `ALL DONE`.
6. **Finish.** `plan.mjs . retag` prints `RETAG DONE` and `validate.mjs . --settled --strict --require-areas` exits
   0 (step 7 comes first when the map is over the thresholds). The `REVIEW` lines (a feature only one platform of its kind uses) are judgement, not a
   blocker: merge with `retag-feature` when it is the same capability under another name.

7. **Areas.** With more than 120 records and 8 or more features with records, run "Areas loop"
   when there is no `.lantern/areas`, or when `areas.mjs . check` fails on the one there is. A
   tree that passes `check` stays. `retag-feature` already renames, merges or drops the leaf of
   the feature it changes.

`macro-eval.mjs <root>` before and after shows the effect in numbers.

## Hard rules

- **`.lantern/` is the only thing written into the project.** No source comments, no
  annotations, no edits to any other file. Scratch, if any, goes to `.ai/tmp/` — check it is
  gitignored in this project first — and never `git add -A`: stage `.lantern/` by name.
- **Read every file of a chunk in full** before writing its records. Role, purpose and
  relations come from the code, not from the file name. A `#symbol` must appear literally in its
  target — the validator checks, so an invented symbol fails.
- **Hashes come from `plan.mjs chunk <id>`**, copied verbatim. Never compute or guess one.
- **No secrets in records.** Config files are read in full; purpose and labels describe what a
  value is for (`Slack webhook URL`), never the value itself.
- **No free-text roles.** Nothing fits → `other`; it is reported for a human, not a failure.
- Setup writes only the `.` marker. `~ + -` are for the sync skill that will claim files during
  delegate runs; setup never sets them.

## Procedure

State lives in the map itself: a file is **done** when it has a `.` record with a valid role
and a matching hash, and its purpose text exists in the primary language. So every step below is idempotent, an interrupted run resumes by
running it again, and the same procedure **refreshes** an existing map — only stale, new or
unmapped files come back as pending.

1. **Scope.** `enumerate.mjs .` and skim the list. Vendored, generated or fixture files it let
   through go in `.lantern/ignore` (gitignore syntax); markdown the agents are told to read that no
   rule maps goes in `.lantern/include` (Which markdown is mapped). Re-run until the list is only
   code and instructions the team owns. Its stderr lists what it dropped by name or content (secret-like names,
   lockfiles, binaries, over 1 MB, a `@generated`-style banner) — those can't be re-included,
   so check nothing hand-written is there. It reads `.gitignore` files under the root and
   `.git/info/exclude`, not a parent directory's ignores, the global excludes file or
   `core.ignorecase`; cover those with `.lantern/ignore`.
1a. **Platforms.** When the evidence shows two or more kinds of code (Platforms, above), write
   `.lantern/platforms` and the labels; `validate.mjs . --partial` must accept them. A repo with
   one platform writes nothing or one line.
1b. **Features and systems.** If `.lantern/features` is missing, write it; if `.lantern/systems`
   is missing, create it with `systems.mjs add` (Feature, see-also and gotcha, rules 1-3). Both
   exist before chunk 1.
2. **Plan.** `plan.mjs . chunks`. Chunks are whole directories packed to ≤25 files / ≤150 KB;
   a bigger directory is split across consecutive chunks. Each line names the map files the
   chunk writes.
3. **Map, one chunk at a time.** For the first id in `plan.mjs . pending`:
   1. `plan.mjs . chunk <id>` — path, hash, size, status, target map file per file.
   2. Read each `todo` file in full. For `skill` files also run `refs.mjs` (the chunk's markdown in
      one call) and follow "Skill files and references". For a file that calls code of this
      repository over the network, or builds, deploys or runs a service of it, follow "Relations
      that cross platforms".
   3. Write its record into the map file shown — create the file with the `lantern 1` header,
      `# <dir>` line if missing; replace an existing record for that path; leave other records
      alone. Keep records sorted by path. Write its texts into the matching
      `lang/<primary>/…json` (created as `{"text": {}}` if missing),
      replacing every key of that record — drop a key whose relation, gotcha or see-also is
      gone — and leaving other records' keys alone. A key whose primary text you changed is
      deleted from that map file's other-language files (see Keeping it true afterwards).
      **A map or text file whose path holds a `.claude` folder** (the records of `.claude/skills/…`,
      `.claude/agents/…`) cannot be written by the Write or Edit tool: Claude Code treats the folder
      as protected wherever it sits, and the call is refused as "a sensitive file". `plan.mjs . chunk`
      prints the paths to use. Write the whole file at the same path with `.claude` spelled `%2Eclaude`
      (an existing file: read the real one, write the complete new content at the alias), for the map
      file and for its `lang/<primary>/…json`, then run `node $L/scripts/fold.mjs .` once; it moves them
      into `.claude`. Never leave a `%2Eclaude` folder behind and never skip these files.
   4. `plan.mjs . chunk <id>` shows every file `done`, and `validate.mjs . --partial` reports
      nothing for these map files. Fix before moving on.
4. **Sections.** After every chunk is `done`, detect and write the sections that have evidence
   (Sections, above), then `validate.mjs . --partial` must print `OK` on each `section` line.
   Skip this step when nothing applies — no sections is a valid map.
4a. **Areas.** After every chunk is `done` and the sections are written, count the map: more than
   120 records and 8 or more features with records (`core:*` not counted) go through "Areas loop"
   below; anything less writes nothing and leaves today's flat view. Same model floor as step 4.
   `areas.mjs . required` prints which of the two it is. Skipping this step is not possible: step 5
   stays red until the tree exists and passes `check`.
5. **Finish.** `validate.mjs . --settled --require-areas` exits 0 with coverage 100% and every purpose present
   in the primary language (and, over the step 4a thresholds, with a tree that passes `areas.mjs . check`;
   exit 1 names step 4a). On a refresh, records for deleted or newly ignored files never show
   as pending — the validator reports them as missing or outside the set; delete those records
   and their keys. Delete every orphan key it warns about in the primary language. For each
   other language it reports below 100%, run `lang-todo.mjs <code>` and tell the user how many
   texts need translating — don't translate unasked. List the `other` files and
   the size of `.lantern/` (`du -sk .lantern`).
   Tell the user `.lantern/` should be committed — it is a maintained artefact — and suggest a
   line for their `CLAUDE.md` saying so; don't write it yourself.

## Where work is dispatched

- **Up to 2 chunks, and you pass the Model check:** do it all inline. If you don't, every chunk
  goes to a worker (below).
- **More:** the main agent keeps steps 1, 2, 4, 5 and every validation; each chunk in step 3 goes to
  one subagent. In a runtime with explicit model selection, a `gpt-6-astra` mapper may dispatch
  workers with that exact model id and the same mapping brief below. Otherwise use
  `subagent_type: "lantern-mapper"`, and
  **omit the Agent call's `model` parameter**: it overrides the type's pinned `model:`. Run
  chunks in parallel only when their map-file lists are disjoint (a split directory shares one).
  The subagent's brief is short — this skill's literal absolute path, the project root, the chunk id, the map
  language code, the platform of its files, and: *"run every script as one plain command with those literal
  paths, `node <skill path>/scripts/plan.mjs <root> chunk <id>`, never with `cd`, a shell variable, a loop, a heredoc or a redirect
  ("Commands in an unattended run"); read `references/format.md` and `references/roles.md`; run
  `plan.mjs <root> chunk <id>`; read `.lantern/features` and `.lantern/systems` (never edit
  either; `plan.mjs chunk` prints both lists) and follow the "Feature, see-also and gotcha"
  section, rules 1-3 included, with `systems.mjs add` as the only way to a new outside system; read every `todo` file in full; write records only into the map
  files listed and their texts only into those map files' `lang/<code>/` files (in other
  languages only deleting keys whose primary text you changed), touching no other record, key or
  file except as the Model section allows; for markdown (role `skill`) run `refs.mjs` and follow
  "Skill files and references"; follow "Relations that cross platforms" for network calls into this repository and for deploy files; report files you put in `other` and any role you were unsure of."*
- **Chunk ids are positions**, recomputed on every `plan.mjs` call: a file added, deleted or
  newly ignored renumbers them. Dispatch by id only from one `pending` listing, and after any
  tree change re-run `pending` before dispatching again.
- **Step 4a is never a worker's.** After the last chunk the main agent runs steps 4, 4a and 5 itself, whoever mapped the chunks.
- **After each subagent,** the main agent re-runs step 3.4 itself. A chunk that isn't all `done`
  goes back out once; twice failing, map it inline only if you pass the Model check, else stop and
  tell the user.
- **Unattended** (headless loop, `lantern-local-loop`, cron): steps are safe to repeat and state is on
  disk, so a crash mid-chunk only loses that chunk. Nothing here pushes, commits or edits
  source; the one judgement call — `.lantern/ignore` in step 1 — is additive and reversible.

## Maps made before markdown was mapped

A map written without markdown stays valid: nothing in it changes meaning and no record is touched.
The markdown the rules above now select simply has no record, so `plan.mjs . pending` lists it,
`validate.mjs` reports each file as `unmapped`, and `lantern-sync`'s `status` counts it as
new/unmapped drift (`verify` fails on drift, as it does for any file nobody mapped yet). A refresh
maps it; only those chunks come back as pending. A checkout of this skill from before the change
rejects the `skill` role and the `@` arrow in a map that has them.

## Keeping it true afterwards

After setup, any edit to a mapped file makes its record stale, and `validate.mjs .` says which.
Re-run this procedure to refresh: only the stale chunks are re-read. Never bump a hash without
re-reading the file — a fresh hash on an old description is the one lie the format can't catch.
A carried-over gotcha or `#see-also` is re-judged against the re-read file and dropped if it
no longer holds, never kept because the hash is fresh. Setup never translates: when a refresh
changes a primary text, delete that key from the same map file's other `lang/<code>/` files, so
the stale translation becomes a missing one that `lang-todo.mjs` lists. Keys whose relation or
note is gone surface as orphans in `validate.mjs`. Edit map records with the Edit tool (Write for a
new one), never `sed -i` or other shell rewriting.

## Pull-request records

`.lantern/prs/<id>.pr` files list what a pull request changed (format: `references/format.md`,
"Pull requests"). They are written by the `lantern-sync` skill after a PR is opened, not by
setup, and read by the Lantern app. Setup neither writes nor edits them; the validator only
checks any that exist.

## Plans

`.lantern/plans/<slug>.plan` files are plans for a change (format: `references/format.md`, "Plans"). They
are written by the `lantern-plan` skill, which refuses to start until `validate.mjs . --settled` passes,
and read by the Lantern app. Setup neither writes nor edits them, and the validator does not read them.

## See the map

`node $L/example-web/render.mjs . --out .ai/tmp/lantern.html --title <name>` turns the project's
`.lantern/` into one self-contained page (layers — the AI column only when the map has an `ai` file, the Skills column only when it has a `skill` file — relations, `@` references drawn dotted, role and directory filters, `~ + -`
markers lit) that opens from disk. `.ai/tmp/` must be gitignored in the project (the default
output is `.ai/tmp/lantern.html`). `--lang <code>` picks the viewer language (default: the
`LANTERN_LANG` setting, else the existing map's language, else `en`); the page also has a language switch and reads `lang=` from
the URL hash. It inlines every `lang/<code>/` file: file cards, tooltips and feature chips show
the selected language, falling back per key to the primary one (dotted underline and a small
language code). With two or more platforms declared it adds a tab bar (`#platform=<id>`) that scopes the graph, counts, filters and sections; relations across a platform boundary stay visible as dashed links to the other platform. Sections, when the map has any, render below the graph as collapsible blocks with
a jump bar; their file links select the file in the graph. Strings live in `example-web/locales.json`; `node $L/scripts/check-locales.mjs`
must pass. To add a language, see `README.md`. Committed sample and full command: this skill's `README.md`.

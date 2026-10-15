---
name: sbtd-workflow-onboard
description: Checks, installs, resets, or explicitly upgrades and verifies selected SBTD workflow Skills, AGENTS and host configuration domains; plans and applies authorized legacy migrations and recovery; reconciles interrupted migration deployment evidence from current state; routes separately confirmed legacy cleanup.
---

# SBTD Workflow Onboard Skills

Use this Skill to onboard a local machine and initialize one or more projects with the SBTD workflow templates bundled under `templates/`.

The repository root installers are `install.sh` and `install.ps1`. `scripts/onboard.py` implements checks, plans, template writes, global Skill installation, read-only per-project SBTD state/bootstrap checks, and the explicitly authorized migration plan/apply/verify/reconcile phases.

The directory remains self-contained: `catalog.json` is the machine-readable source catalog, `catalog.schema.json` is its Draft 2020-12 contract, `scripts/` is the Onboard implementation, `templates/` is the install payload, and `assets/` contains managed third-party fallback snapshots and migration support assets. Keep this separation when adding catalog entries; do not move install payloads beside runtime code merely to flatten paths.

## v2 Delivery and Release Boundaries

The v2 catalog carries 14 bundled / 19 external Skills and on-demand SBTD setup. Explicit Codex/OMP project graph/MCP wiring, root-installer forwarding, migration and cleanup/recovery have separate implementation and acceptance records. A source checkout or successful installation is not release, Windows-native or actual-host proof. Check the repository's published tag and release evidence for those claims. Graft installation, real-project deployment and legacy retirement each require their independent authorization.

P1-01 supplies the internal argument and exchange-contract modules (`scripts/onboard_arguments.py`, `scripts/onboard_contracts.py`, `onboard-contracts.schema.json`). P1-12 registers `migration --phase plan|apply|verify`; P1-04/P1-05 add the Codex/OMP deployment producers through existing init entry points, and cleanup/recovery are implemented by their owning tasks. Do not substitute contract fixtures, valid hashes, or a copied directory for executed migration or recovery evidence.

P1-17 adds the task-state Python library inside `scripts/` (`sbtd_task_document.py`, `sbtd_task_state.py`). `TaskStore` exposes create / inspect / select / transition / set_mode / resume / reopen / protect_local_state / promote / archive for host-native callers; it is not a new global CLI, daemon, journal, or `onboard.py` subcommand. The task document owns state and the active JSON is only a bookmark. Markdown structure recognition uses the declared dependency markdown-it-py>=4,<5 (CommonMark tokens, parse-only, no rendering, no network; Python >=3.10) — a missing dependency stops writes explicitly instead of falling back to hand-rolled scanning. Promotion and archive are two-phase: prepare and verify the target candidate and references first, then a separate confirmation retires the original directory atomically into `.sbtd/task-originals/` without recursive deletion. Candidate copies use a protected temporary area owned by the current operation; sibling logical task records require explicit `include_tasks` authorization, and path nesting is not ownership. Non-Git projects record a null branch; first-time narrow protection only appends `/.sbtd/`. When the installed helper copy or its declared dependencies are unavailable, callers must report that persistence did not run instead of claiming it. Windows, host routing, identity creation and legacy migration remain later stages.

Task cancellation is an explicit terminal state, `cancelled`, not a successful completion. Keep `completed_at` null; do not cancel children implicitly, count cancelled bootstrap as done, or emit unfinished-work reminders for it. Archive/reopen preserve cancellation history. Imported cancelled/blocked facts retain unproven mode/time rather than inventing them, and an unknown blocked ingress still needs an explicit recovery-phase choice. Update the task runtime, schema and references together before using the new records; older readers may reject them. Exact historical event and reason rules are in [Canonical legacy task candidates](REFERENCE.md#canonical-legacy-task-candidates).

P1-18 adds deterministic routing and protected handoff helpers in the same `scripts/` directory (`sbtd_task_routing.py`, `sbtd_handoff.py`), again without a new global CLI, daemon, journal, or `onboard.py` subcommand. `TaskRouter` only maps facts the host has already made explicit (a `RouteRequest` intent of `new` / `continue` / `question`, an explicit mode, a recommendation response of `accept` / `keep`, and read-only / confirmation flags) to a deterministic `RouteDecision` (`ready`, `needs-task-choice`, `needs-mode-choice`, `needs-mode-decision`, `needs-branch-choice`, `needs-persistence-confirmation`, `persistence-failed`, `blocked`); it is not a natural-language intent classifier. Continuation resolves exactly one task before any mode decision, refusals persist in a structured `mode_note` deduplicated by risk identity, and a failed save keeps the in-session choice while reporting it as not persisted. `TaskStore` additionally exposes `current_binding`, `recovery_candidates` and `rebind`: a branch mismatch requires the correct worktree, an explicit rebind (with `expected_branch`, `reason`, `evidence` and confirmation; it updates only the binding and its event — no checkout, no stash, no reset of blocked recovery history), or a read-only choice. `HandoffStore` saves snapshots only on a real pause / context-switch / branch-switch / context-pressure / manual trigger — status counts or entering checking never trigger; task and session opt-outs latch independently (session wins) and a manual request does not clear them. `save` returns one of `saved`, `suppressed`, `conversation-only`, `branch-conflict`, `unprotected`, `unchanged`, `pending-confirmation`, `needs-redaction`: writes first verify the narrow `docs/handoffs/` protection and tracked state and require an explicit `redaction_confirmed`; file names carry the lowercase hex of the UTF-8 full logical task ID (collision-free even on case-insensitive filesystems, reversible), and an unchanged same-task snapshot — compared on every field except `created_at` — is not rewritten across a day boundary. Proactive reminders only cover the latest per-task snapshots within seven days whose root/branch match an unfinished task; older snapshots remain manually resumable but never rewrite the task, a branch mismatch rejects the write, and a handoff is never the source of mode or status. Whether the Agent truly recommends first, pauses, and executes the full method per mode remains owned by the Skill rules and real-host proof; this slice does not claim Windows, host wiring, automatic session-start restoration, legacy migration, full validation, or release.

P1-19 adds on-demand developer identity in `scripts/sbtd_identity.py`, again without a new global CLI, daemon, initializer, or identity database. `DeveloperStore(root, read_only=False)` exposes read-only `resolve()` / `plan(name)` and the confirmation-gated `ensure(name, confirmed=False, protect=False)`, all returning a frozen `IdentityResult` (`status`, `name`, `source`, `path`, `first_write_eligible`, `topology`, `reason`, `needs_protection`, `completed_steps`). A valid local `.sbtd/developer` wins immediately without any Git call; only a genuinely absent local file triggers verification of the real Git toplevel, absolute git-dir/common-dir and the NUL-separated worktree registry, and a verified linked worktree reads the same-repo main checkout's current identity in place without copying it. Present-but-abnormal local or main files (duplicate `name=` declarations, invalid value, wrong type, symlink, unreadable, unsafe parents) are conflicts, not absence; unknown or unavailable Git metadata is blocked, not proof of a non-Git project. Names pass only the single `validate_developer_name` (`^[a-z0-9]+$`, verbatim); nothing is inferred from Git, OS, environment or history, and ordinary resolution never reads legacy `.trellis/.developer`. `onboard.py` consumes identity only through an explicit `--developer <name>`: `check` / `plan` stay read-only and add a `developerPlan` object to the single JSON document, while `init` / `reset` / `init-projects` require `--developer` together with `--yes` and preflight every listed project's identity plan before any global or project write; without `--developer` nothing changes and `reset` never rewrites an existing identity. Narrow `/.sbtd/` ignore protection and the name are confirmed separately. The root installers gain no developer-specific flag and forward the implemented public flags; legacy identity migration remains the separately gated P1-12 task.

P1-12 migration uses an existing external private vault and explicit approved candidates; `plan` creates nothing. `apply --yes` preserves originals, installs only approved projections, pauses proven owned legacy Codex/OMP routing, and atomically saves a new cumulative receipt beside the manifest. Retries require the explicit prior receipt and preserve successful results and original backups. `verify` reads actual artifacts/resources and bound deployment reports without deploying or cleaning up. If a completed apply left its deployment evidence unsaved, `migration --phase reconcile` with explicit `--yes` freshly observes current state and writes one new typed evidence document at a new private path — the historical receipt, its exit code and its timestamps are never fabricated, and the following standard `verify` reports `acceptance_basis: current-state`; reconcile authorizes no install, retry or cleanup. Direct `share` copies preserve source bytes; rewritten content needs `redact`. Mixed or unknown configuration is preserved for reconciliation, not broadly overwritten. Read [Migration Runtime](REFERENCE.md#migration-runtime) before these commands; this staged consumer implementation is not permission to migrate real projects or claim real host/Windows acceptance.

The migration planner supports characterized `0.6.15` / `0.6.17` legacy data layouts, with the original stamps and metadata preserved. 0.6.15 hash claims for lessons/runtime/junk do not confer generated ownership or bypass user-data approval. Genuinely absent project host roots permit `platforms: []`; unknown/new host roots and incomplete marker-operation closures still reject. This data compatibility does not expand vendor-uninstall CLI support or authorize source repair, publication, deployment, cleanup or recovery. See [Migration Runtime](REFERENCE.md#migration-runtime) for the exact boundaries.

For stale generated-file hashes, use only the installed ownership asset's reviewed exact path/version/content evidence; no live metadata refresh, runtime download or blanket drift bypass is permitted. Mixed project `AGENTS.md` requires the existing signed routing-candidate approval binding its actual before-state and candidate, not a generated-file pin. Apply/retry/retained-original validation must retain that distinction. Candidate preparation is not signing, deployment or cleanup authorization.
For a verified project routing candidate, migration deployment preserves its approved body after removing only the native maintenance prefix and separator, then renders the managed Graft fence. A pause prefix alone is not provenance. Do not infer that ordinary init authorizes this migration-specific exception, or that an approved body may be silently replaced by a generic template.
For OMP configuration inputs changed by an approved migration stage, use the receipt-bound post-state rules in [Wiring and Deployment](REFERENCE.md#codex-and-omp-wiring-and-deployment); do not rewrite the manifest or restore retired inputs to bypass a drift rejection.
Cleanup alone may accept deployment-discovery input file/absent drift only when it is disjoint from the actual vendor footprint and every cleanup dependency, with the discovered input set and live profile/tool binding unchanged. A completed original batch may use paired `--upgrade-plan` / `--upgrade-receipt` to prove one native Onboard replacement without a new local lineage signature; its cleanup receipt cannot authorize followup, deployment or migration recovery. Read [Cleanup Runtime](REFERENCE.md#cleanup-runtime) for the exact evidence and rejection rules.

An already exact project-template AGENTS may be bound as unchanged evidence without signing or rewriting it; any drift remains a conflict. Document-only legacy task history requires explicit source-bound document publication, never a fabricated task. Historical-branch handoffs must distinguish migration checkout/HEAD evidence from the old task branch and defer real recovery to an explicit user choice. These compatibility paths grant no publication/apply/cleanup authority.

Before Codex/OMP global wiring, project initialization or migration-context init, read [Codex and OMP Wiring and Deployment](REFERENCE.md#codex-and-omp-wiring-and-deployment). Full setup installs one session-scoped global Graft definition per effective host configuration domain, including global-only setup; the launcher locks the nearest initialized Git repository/worktree from actual startup cwd. Project-only writes only local fence/graph/stamp and never appends host bindings. No project, HOME, missing/old graph and unsafe boundaries fail closed. Hooks remain a separate Codex `--graft-hooks` opt-in plus host trust. Existing fixed-root entries require a separately displayed, backed-up `--graft-retire-legacy` cutover; different old runtime paths also require an explicitly approved private `--graft-legacy-bindings` contract. This does not authorize TEMP or backup deletion.

Whole-directory installation and `npx skills add` do not run pip. Before validating exchange contracts, task state or migration, use the actual installed-copy interpreter: `python -m pip install -r /path/to/installed/sbtd-workflow-onboard/requirements.txt`. This declares jsonschema, PyYAML, markdown-it-py, tomlkit and cryptography; missing dependencies block the affected validation or write without breaking help or pure argument parsing. Verify a fresh installed copy, not the source machine's existing packages.

Do not install the source repository root `AGENTS.md`, `ENTRYPOINT.md`, `README.md`, `README.zh.md`, `archive/`, or `docs/lessons.md` as target templates.

## Upgrade Alignment Routing

When the user asks to upgrade an existing environment or align it with a fixed Onboard baseline, read [Upgrade Alignment](REFERENCE.md#upgrade-alignment) before running commands. `init` preserves valid Skill shells and is not proof of content alignment; `reset` is not the upgrade recovery protocol.

Collect explicit Skills roots, global AGENTS targets, host configuration domains and optional shell profiles. Ordinary Codex and an Orca account may use different domains. Inventory only those selections; do not enumerate credentials or silently select other accounts. Present content differences and unresolved ownership; unknown custom content needs an explicit replace/preserve decision. A preserved exception is not fully aligned.

Run read-only `upgrade --phase plan`, display the exact baseline and target set, then obtain consent before `apply --yes --confirm-plan`. A plan identifier binds the displayed selection; it is not authorization by itself. Read-only `verify` measures current content; runtime/host probes require separate `--probe --yes` consent. Report disk, protocol, actual host loading and legacy cleanup separately. Use `recovery --upgrade-*` only after showing and confirming its recovery plan; retain backups. Neither upgrade success nor migration verification authorizes `cleanup-legacy`, removal of runtimes/backups, plugin/hooks changes, or workflow sync.

When an isolated probe encounters a linked Skill, keep the default refusal and the original link. Read [precise link authorization](REFERENCE.md#probe-skill-link-authorization): only an explicitly approved physical target may be captured with `upgrade --phase authorize-link` and consumed by `verify --probe --yes --link-authorization`. Recheck plan/host/path, link and target identities, Skill identity and content before/after temporary materialization; reject nested links or drift. This does not change installation/cleanup policy or prove live session reload.

The selected, operator-controlled private vault is trusted historical evidence, not a signed journal. Hashes do not protect against a writer forging its entire history. Refuse automatic recovery when provenance/control of the vault is uncertain; still validate scope-derived resources, complete recovery eligibility and current drift. Never run a historical executor merely because its files match a vault hash. Recovery preserves empty parent directories and backups.


## Required Questions

Resolve these questions in order:

1. Which target Agent platform is being configured: `codex`, `claude`, `kimi`, or `oh-my-pi` / `omp`?
2. Is this a normal `init` / `reset`, or project-only initialization equivalent to `--init-projects`?
3. What are the project roots? Accept existing absolute paths separated by English commas, or an explicit empty selection for global-only setup.
4. Should project `AGENTS.md` be installed into every selected project root?

The Agent platform selects the CLI and MCP adapter; it does not select the global AGENTS target. Unless the user explicitly supplies a global AGENTS path, normal onboarding writes the Codex global template to the resolved `$CODEX_HOME/AGENTS.md` / `~/.codex/AGENTS.md` path. If the user-home `.omp` directory already exists (POSIX `~/.omp`, Windows `%USERPROFILE%\.omp`), `init` / `reset` also backup-then-overwrite the same template to `~/.omp/agent/AGENTS.md`. Missing `.omp` is skipped; Onboard does not create `.omp`. `--global-agents-path` overrides only the Codex target and does not cancel the OMP write. If that path or a project `AGENTS.md` resolves to the same file as another AGENTS target, Onboard keeps a single file write. Project-only mode does not write any global AGENTS file.

If multiple paths are supplied to this Skill but the user did not explicitly say they are projects to initialize, ask whether they are the intended initialization roots before running checks or writes. Do not infer that every mentioned repository path should be initialized.

Normal `init` / `reset` always target bundled and required external workflow Skills globally. There is no global/project/none Skill scope choice. `init` skips a bundled or required external Skill whose target is already a valid Skill shell (regular directory, regular `SKILL.md`, matching frontmatter `name`); installing a missing required external Skill does not reinstall already-valid dependencies. `reset` overwrites every bundled Skill without backup and force-reinstalls every required external Skill from the current stable snapshot. Global and project `AGENTS.md` still backup-then-overwrite; project `.gitignore` still appends missing template lines. Project-only initialization must not check, install, update, or configure global Agent CLIs, runtimes, tools, Skills, AGENTS, or MCP.



## Skill Installation Modes

The official `skills` CLI may install this self-contained directory as the bootstrap Skill without cloning the whole repository first:

```bash
npx --yes skills@latest add \
  https://github.com/KunoLu/640-skills \
  --skill sbtd-workflow-onboard \
  --global \
  --agent codex \
  --yes \
  --copy
```

The `npx skills add` command installs only the `sbtd-workflow-onboard` package. It does not execute `scripts/onboard.py`, install Trellis or GitNexus, write AGENTS files, install the other bundled/external Skills, or initialize a project. After installation, invoke this Skill through the Agent and run `scripts/onboard.py plan --json`, `init`, or `reset` as required.


The repository root `install.sh` and `install.ps1` remain the complete interactive entrypoints when the repository is already cloned. Do not duplicate `templates/skills/**` at the repository root or add a second bootstrap Skill to accommodate the `skills` CLI; the top-level `SKILL.md` is the single discovery entrypoint.

## Root Installer Interfaces

Normal onboarding:

```bash
bash install.sh \
  --platform codex \
  --projects-root /abs/project-one,/abs/project-two \
  --action init
```

```powershell
.\install.ps1 \
  -Platform codex \
  -ProjectsRoot "C:\work\one,C:\work\two" \
  -Action init
```

Project-only initialization:

```bash
bash install.sh \
  --platform codex \
  --init-projects /abs/project-one,/abs/project-two
```

```powershell
.\install.ps1 \
  -Platform codex \
  -InitProjects "C:\work\one,C:\work\two"
```

`--projects-root` / `-ProjectsRoot` and `--init-projects` / `-InitProjects` are mutually exclusive. Every path must be absolute and must already be a directory. Duplicate paths are normalized and processed once.

When normal onboarding omits the `projects-root` argument and `--yes` / `-Yes` is absent, explain that multiple absolute paths are supported with English commas, ask whether the current working directory is a target project, and otherwise prompt for the comma-separated list. A blank answer means global-only onboarding.

With `--yes` / `-Yes` and no `projects-root` argument, normal `init` / `reset` is global-only: do not ask the cwd question, infer a project from cwd, or install project AGENTS/ignore/graph assets. Explicit `projects-root` and project-only `init-projects` selections keep their existing meaning. The confirmation flag authorizes the selected scope; it does not create an omitted optional project selection.

## Target Agent CLI Gate

Normal onboarding resolves the Agent first and may inspect its CLI before the remaining questions. Collect all project roots and the project-AGENTS choice, then run the complete read-only `check-projects` preflight before any Agent/runtime/Skill installation, MCP write, or optional project installation. Pass `--skip-project-agents` when that target was explicitly excluded. Recheck immediately before Python writes.

| Platform | Verify | Required global npm package when missing |
|---|---|---|
| `codex` | `codex --version` | `@openai/codex@latest` |
| `claude` | `claude --version` | `@anthropic-ai/claude-code@latest` |
| `kimi` | `kimi --version` | `@moonshot-ai/kimi-code@latest` |
| `oh-my-pi` / `omp` | `omp --version` | `@oh-my-pi/pi-coding-agent@latest` |

After project preflight passes, repair the selected Agent CLI when needed and verify it. A working Agent does not require bootstrapping npm just because optional Graft is missing. Graft installation has its own displayed plan and confirmation; a refused or unavailable auxiliary tool is not an authorization to install prerequisites.

Project-only `--init-projects` asks for or accepts the platform but skips this Agent CLI/npm gate and every other global preflight.

## Mandatory Global Installation Policy

Normal `init` / `reset` maintains required global Skills. Auxiliary Graft installation is explicitly selected:

- `check` and `plan` report `graft` without querying npm latest or installing anything. Local verification is independent of npm availability.
- `install-graft` shows the frozen `@nanonets/graft@0.21.1` package/native-script and telemetry-disable plan; `--yes` authorizes that scope, not host wiring, graph creation or legacy cleanup. Package installation needs Node >=20 and usable npm. When the probe shows a verified installed CLI and only telemetry is selected, confirm with `install-graft --telemetry-only --yes`; if the CLI disappears or becomes unverified, the handler blocks rather than widening consent to package installation.
- The Python handler verifies archive integrity, installed package identity/version, native CLI startup and persisted telemetry opt-out. Any failed phase stays nonzero; npm exit 0 alone is not success.
- Telemetry persistence never overwrites existing enabled state: absent files are created without clobbering concurrent writers, already-disabled files are read-only, and existing files requiring a change block until externally resolved under exclusive control. Do not substitute a Python-only lock or readback for Graft writer coordination.
- Managed subprocesses use DNT, an empty dotenv source and forced `DOTENV_CONFIG_QUIET=true`, with inherited debug and LLM/cloud activation settings excluded. Installation also uses noninteractive CI to suppress this pin's postinstall background path; that is not a claim of CI validation.
- GitNexus CLI installation and its dedicated MCP menu are retired. User-owned GitNexus assets are removed only through the confirmed post-migration cleanup path (project `.gitnexus/` and detected host MCP entries; see Legacy Cleanup Routing below); the npm package, the GitNexus CLI and `~/.gitnexus` global data are never touched, and no CLI/npm uninstall is performed. Python Codex/OMP wiring and the corresponding root-installer forwarding are available as described below.

Readonly RTK authenticity verification runs `gain` in a private probe HOME/cwd. It does not inspect or create the user's history database; `verificationScope=isolated-probe` records that limitation.

All bundled Skills install globally as one required set:

- `sbtd-workflow-onboard`
- `sbtd-task`
- `project-validation`
- `web-ui-autotest-generator`
- `gherkin-bdd`
- `knowledge-base-integration`
- `maestro-mobile-e2e`
- `lessons-record`
- `book-refactoring-pass`
- `book-legacy-change-safety`
- `book-ddd-distilled-modeling`
- `book-ddia-data-design`
- `book-release-readiness`
- `seo-geo`

After the canonical `sbtd-workflow-onboard` target is written and its `SKILL.md` frontmatter validates, remove a legacy `kuno-workflow-onboard-skills` target only when that directory's own `SKILL.md` frontmatter still identifies it as `kuno-workflow-onboard-skills`. A conflicting file, unrelated directory, or mismatched frontmatter blocks `init` / `reset` before any target changes and remains untouched; deletion errors are reported as migration failures. This is a clean rename migration, not an alias: never retain both directories after a successful normal `init` or `reset`.

All referenced external Skills are also required globally. Install every missing item without a scope or selection prompt:

- `diagnosing-bugs`, `tdd`, `grill-me`, `grill-with-docs`, `grilling`
- `domain-modeling`, `codebase-design`, `handoff`, `writing-for-agents`
- `to-spec`, `to-tickets`, `ui-ux-pro-max`, `impeccable`
- `shadcn`
- `ponytail`, `ponytail-review`, `ponytail-audit`, `ponytail-debt`
- `i-have-adhd`

Dependencies are still expanded automatically: `tdd` includes `codebase-design`; `grill-me` includes `grilling`; `grill-with-docs` includes `grilling` and `domain-modeling`.

The four Ponytail Skills are required like every other external Skill: `check` only inspects and reports them, while normal `init` / `reset` installs or repairs missing and invalid copies from the vendored stable set without asking, and a failed install fails the run. Onboard uses the stable skill-only provider and never installs, enables, disables, trusts, or removes the official Ponytail plugin. When `check` detects the official Ponytail plugin enabled for Codex or OMP, it reports `ponytailProvider.provider=conflict` and fails; `init` / `reset` block before writing stable copies, and the root installers stop with the same guidance. A plugin that is installed but disabled is reported but does not block. `ponytail-gain` and `ponytail-help` belong only to the official plugin and are never managed by Onboard.

The mandatory runtime gate contracts are owned by the installed global `AGENTS.md`, project template, bundled `sbtd-task`, and bundled reviewer Skills. They become active only after normal `init` / `reset` successfully writes the global rules and installs the required bundled / external Skills. The public Skills CLI bootstrap and `init-projects` do not activate these runtime gates by themselves; they only install the Onboard Skill or process project-local assets respectively.

At runtime, a `strict` development task first produces a `Book Gate Plan` with objective predicates and lifecycle states. `default` / `lite` tasks select methods by actual risk and explicit deliverables and never fake a chosen method's evidence; project requirements remain binding. Every completed external `grill-with-docs` session invokes bundled `book-ddd-distilled-modeling` in all modes. For strict tasks, persisted/shared data, shared / persistent / cross-request / cross-process caches, async/cross-service flows, ownership, migrations, or recovery invoke `book-ddia-data-design`; existing-behavior bugs or uncertain existing code invoke `book-legacy-change-safety`; any existing-production-code edit invokes `book-refactoring-pass`; production-path runtime/deployment changes invoke `book-release-readiness` after all applicable testing-tool gates and project validation. Matched strict gates block their phase until passed; unmatched scenarios remain on demand.

External Skill installation uses a validated, stable-first source policy. The default `auto` policy and explicit `stable` policy both resolve every selected Skill from the reviewed vendored set under `assets/external-skills/stable/` without accessing Git or the network. Only explicit `upstream` opts into cloning and validating the current upstream repository group, and upstream failure does not fall back. Manifest, source-subpath, and license paths must stay contained by their declared roots. All selected Skills are staged before any target changes, and target replacement uses a temporary rollback transaction. Source-integrity and target-filesystem failures are fatal; an incomplete restore retains and reports the rollback directory.

The stable set is an unmodified mirror, not a fork. `assets/external-skills/stable/MANIFEST.json` records the exact upstream commit, source subpath, tree digest, and license files. Promote a new repository revision only through `promote-external-skills-stable`; promotion must validate the complete stable set before replacing it.

`caveman` remains a user-level global Skill with its existing explicit installation decision. Normal `init` / `reset` preserves a missing copy, but maintains an installed workflow skill payload against the reviewed pinned v* installer / skill baseline: known older payloads are backed up then upgraded, replaceable non-symlink abnormal payloads are repaired, symlinked payloads fail closed and are reported, and newer or customized payloads are reported without replacement. This scope is `caveman*` / `cavecrew*` Skills only; hooks, statusline, plugins, and extensions remain user-managed. ENTRYPOINT monitoring only reports v* tag drift; a human-reviewed change must update the pinned ref, revision, hashes, and tests together. Java 17+ and Maestro CLI remain local-machine prerequisites installed only after their existing conditional confirmation. RTK remains global with its existing confirmation and `rtk gain` verification behavior.

## Per-Project Processing

For every selected root, inspect SBTD state before installation writes. A missing `.sbtd`, identity, task or bootstrap is normal; ordinary work does not require onboarding.

1. Validate only the active bookmark/selected task and an existing `ai/tasks/00-bootstrap-guidelines/task.md`: safe UTF-8 JSON/YAML, bundled v1 schema, real dates, path types/containment and full logical-ID agreement. This is not full event/parent/branch recovery validation.
2. Report malformed state as blocked, legacy `.trellis` as needs-user for migration, and an explicitly present unfinished bootstrap as bootstrap-required. A done record is recorded state, not independent acceptance evidence. Inspect all selected roots; any blocking result stops installation writes for the batch.
3. Reject unsafe AGENTS/ignore destinations and newly hiding existing reserved data. Resolve ownership/protection explicitly rather than silently adding ignore coverage.
4. Install selected project AGENTS and append missing project `.gitignore` lines without reordering existing content. Preserve task, identity, spec, lessons, handoff and legacy data. Do not create those optional artifacts.
5. Check applicable project-local Playwright and React Bits conditions; retain their existing installation confirmations.

Explicit Codex/OMP project setup maintains the project fence and builds the local graph when fixed Graft/Node is already available. Missing tools yield `graftWiring.status=not-available` without blocking unrelated setup. Project-only never writes HOME, global Skills, MCP or hooks; adding projects reuses the same global definition and does not upgrade its runtime.

Playwright CLI remains project-only and is installed with `install-playwright-cli --project-root <one-root> --yes` after confirmation.

React Bits remains project-only and optional:

- shadcn/ui-only is the default choice.
- React Bits Free requires an explicitly configured free registry item.
- Paid Starter / Pro / Ultimate setup requires an existing entitlement and a readable `REACTBITS_LICENSE_KEY`; install the Skill at `.agents/skills/react-bits-pro/SKILL.md`, overwriting that target without a backup, and never print or persist the key.
- Preserve a detected tier/registry during reset.

## MCP Scope Policy

The generic interactive MCP menu and the Codex Graft producer are separate. The menu offers Chrome DevTools, Playwright, Maestro and custom stdio MCP; project-only skips user-level MCP configuration. No GitNexus fallback/alias is provided. Explicit Codex full setup uses the guarded Graft producer described above.

The target scope is fixed by Agent platform:

- Codex: user-level `codex mcp add` behavior.
- Claude Code: always `--scope user`.
- Kimi Code: keep the CLI default behavior; do not add a scope flag.
- Oh My Pi: always write the global `~/.omp/agent/mcp.json` file.

Do not couple MCP scope to project roots or Skill scope. Do not configure project-level Claude or Oh My Pi MCP entries during onboarding.

## Legacy Cleanup Routing

When `migration --phase verify` reports `status: verified`, proactively offer cleanup: display the batch-sealed candidates and run `cleanup-legacy --phase plan` so the actual fresh candidate list is displayed before asking. When the user says `sbtd cleanup`, `清理工作流`, or an equivalent explicit intent to remove retired Trellis/GitNexus assets, route to the same flow. Normal `init` / `reset` never performs this cleanup.

The trigger authorizes read-only detection and planning only; execution requires the user's explicit yes after the displayed scope. One confirmation covers the displayed combined scope of the batch-sealed candidates and the freshly planned ones. Run the batch cleanup first; if it changed originals that the fresh plan had sealed, regenerate the fresh plan and display the remaining work. Within this same confirmed cleanup run, keep the original consent when the new plan is unchanged or only omits targets proven completed by the bound batch receipt, with the remaining targets and effects unchanged; do not ask again merely because those completed overlap items disappeared from the fresh list. Any added target or changed effect requires renewed consent. An unexplained disappearance, user edit or conflicting/failed evidence remains a stop-and-reconcile condition, not permission reuse. Always use the current fresh `plan_id`, never an obsolete id. The Agent reads `verification_id` / `plan_id` from the CLI JSON output itself; the user never pastes a hash. An id binds one confirmation to a sealed candidate set; it is not authentication or ownership proof.

Only actually detected items appear in the list:

- Project `.trellis`, removed by actually running the vendor `tl uninstall` in the project root. A dedicated adapter prepares the uninstall at plan time and, before execution, privately backs up the complete vendor footprint — `.trellis` plus the platform configuration and AGENTS entries the vendor uninstall may modify. A missing CLI or failed preparation blocks the target without executing; an incomplete uninstall fails the resource with per-resource measured after-states, so partial mutations are reported as measured evidence and reconciled before any retry — never claimed untouched, never an engine direct delete or `rm -rf`.
- Global `trellis-workflow` / `trellis-channel` Skill directories whose own `SKILL.md` frontmatter still identifies them. Any 1.0.x version qualifies; there is no fixed checksum pin. Symlinks and identity mismatches stay blocked and preserved.
- The nine exact GitNexus Skill names listed in [Upgrade Alignment](REFERENCE.md#upgrade-alignment), only as direct children of the selected Skills root with matching regular `SKILL.md` identities. No wildcard or CLI/package removal. These are fresh cleanup candidates, not additions to immutable historical migration manifests.
- Project `.gitnexus/` directory.
- Detected gitnexus MCP server entries in the existing Codex / Claude / Kimi / OMP global configuration paths; OMP probing additionally covers the effective configuration that the existing resolver derives from a relative `PI_CONFIG_DIR` override and the active profile (`OMP_PROFILE` taking precedence over `PI_PROFILE`). Spelling aliases of the same directory entry are probed once; distinct hardlink entries remain separate cleanup targets. Every entry that identifies as gitnexus (key name or command/package) is removed; neighboring servers are preserved. These files are shared with other projects — disclose that impact and include it in the confirmation.
- Project `AGENTS.md` blocks exactly paired as `<!-- TRELLIS:START -->` / `<!-- TRELLIS:END -->` and `<!-- gitnexus:start -->` / `<!-- gitnexus:end -->`, recognized only as top-level HTML comment blocks and removed with their contents; graft fences, code-fence content and all other bytes are preserved. Zero pairs is not a candidate; duplicated, interleaved or unmatched markers are blocked for manual resolution.

Entry selection is batch evidence first: with a complete verified migration batch, run `migration --phase cleanup` with `--confirm-cleanup <verification_id>` for its sealed candidates. Batch manifests are immutable and never gain the new target kinds; project `.gitnexus/`, gitnexus MCP entries and AGENTS marker blocks are always handled by a fresh `cleanup-legacy --phase plan`, display of the sealed candidates, then `cleanup-legacy --phase apply --confirm-cleanup <plan_id>`. The fresh plan accepts an optional plan-only `--global-skills-dir` override under the existing resolver precedence (explicit argument, then `$AGENT_SKILLS_DIR`, then the trusted installed Onboard parent, then the platform default) and seals the selected Skills root into the plan; apply runs against that sealed root only — it has no root option and is not redirected by a later environment change, and migration phase arguments are unchanged. Candidate paths that are equal to or nested inside one another are rejected at plan and apply before any target write. Only missing batch evidence falls back to a fresh plan for the retired `.trellis` / Skill targets as well; stale, conflicting or failed batch evidence is never a fallback reason to bypass a gate — preserve it and resolve the rejection first. Both root installers forward `cleanup-legacy` like `migration` / `recovery`. If the user declines, say cleanup can be retriggered later with `sbtd cleanup`, `清理工作流`, or the same explicit intent. Exact commands, detection paths and safety semantics: [Cleanup Runtime](REFERENCE.md#cleanup-runtime).

## Shared Python Commands

Global and multi-project check:

```bash
python scripts/onboard.py check \
  --projects-root /abs/project-one,/abs/project-two
```

Project-only check without global runtime/tool/Skill inspection:

```bash
python scripts/onboard.py check-projects \
  --projects-root /abs/project-one,/abs/project-two
```

Normal plan/init/reset:

```bash
python scripts/onboard.py plan --platform codex --projects-root /abs/one,/abs/two --json
python scripts/onboard.py init --platform codex --projects-root /abs/one,/abs/two --yes
python scripts/onboard.py reset --platform codex --projects-root /abs/one,/abs/two --yes
```

Inspect and explicitly authorize Graft installation:

```bash
python scripts/onboard.py install-graft --json
python scripts/onboard.py install-graft --yes --json
```

The first command does not write and may exit 2 with a confirmation/prerequisite result. Inspect the returned plan before using `--yes`; it does not authorize migration or graph/host changes.

Project-only initialization:

```bash
python scripts/onboard.py init-projects \
  --platform codex \
  --projects-root /abs/one,/abs/two \
  --yes
```

External Skill installation accepts global scope only:

```bash
python scripts/onboard.py install-external-skills --all --scope global --yes
```

Choose an explicit source policy when needed:

```bash
python scripts/onboard.py install-external-skills --all --scope global --source upstream --yes
python scripts/onboard.py install-external-skills --all --scope global --source stable --yes
```

Migrate every recognized mattpocock legacy directory in a global Skill root:

```bash
python scripts/onboard.py migrate-external-skills --scope global --source auto --yes
```

The migration validates each legacy `SKILL.md` identity before it changes any target, installs required canonical replacements transactionally, and then removes the verified legacy directories.

Promote a reviewed upstream repository revision into a new stable set:

```bash
python scripts/onboard.py promote-external-skills-stable \
  --repository mattpocock-skills \
  --revision <full-commit-sha> \
  --stable-set <yyyy-mm-dd.index> \
  --yes
```

First-time registration of a repository that is not yet in the stable manifest additionally requires `--repo`, `--license`, and at least one `--license-file SOURCE=STABLE_PATH` mapping; the promoted Skills are selected from catalog external entries whose `source.repo` matches `--repo` exactly. For a repository that already exists in the manifest, `--repo` may only repeat the recorded URL and `--license` / `--license-file` are rejected, so promotion can never silently rewrite repository metadata.

## Reporting

Normal `check`, `init`, and `reset` report global runtime/tools/Skills plus a `projectChecks` entry for every selected root. `check-projects` and `init-projects` report only project-local checks and writes.

Aggregate SBTD status priority is `failed`, `blocked`, `needs-user`, `bootstrap-required`, `success`, `skipped`. All selected roots retain individual status/reason/nextStep. Blocking preflight stops the whole installation batch before template or Skill writes.

Every External Skill install result must report `requestedSource`, `sourceUsed`, `sourceRevision`, `stableSet`, `fallbackReason`, and transaction status when applicable. Every project result must identify the affected project root. Do not merge failures, bootstrap tasks, Playwright applicability, or React Bits decisions across projects without preserving the root path.

`init` / `reset --json` keep one root document. When required external installation runs, `requiredExternalInstall` contains its complete result, including per-Skill provenance and `transaction.rollbackPath` / `rollbackErrors` on failed recovery; it is `null` when installation was unnecessary. Preserve this result on early failure returns as well as successful runs. Human Caveman reports include refusal reasons, retained backup paths, and restore errors.

See [REFERENCE.md](REFERENCE.md) for exact overwrite, backup, troubleshooting, and platform details.

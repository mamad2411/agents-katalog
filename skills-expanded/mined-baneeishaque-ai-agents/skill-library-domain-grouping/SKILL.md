---
name: skill-library-domain-grouping
description: >-
  SSOT for the project-specific domain taxonomy and placement rules governing
  the skill library folder structure.
category: General-Domain
---

# Skill Library Domain Grouping (v1)

This skill is the **Single Source of Truth** for the domain-based folder
structure of this project's skill library. Every skill directory belongs in
exactly one leaf group defined below. Adding, removing, or relocating a group
requires an update to this document.

The taxonomy was designed following the
[`human-scanable-organization`](../human-scanable-organization/SKILL.md)
8±2 principle: every folder contains ≤10 items; folders exceeding that
threshold are sub-grouped recursively.

*

## Composition Rationale

This skill is a standalone SSOT — it does NOT compose any base skill. It is
consumed by:

* **[`human-scanable-organization`](../human-scanable-organization/SKILL.md)** —
  as the concrete worked example (§3) of the 8±2 principle.
* **[`skill-factory`](../../skill-factory/SKILL.md)** — whose Post-Drafting
  Checklist (§3) requires compliance with the taxonomy defined here before a
  new skill is considered complete.

*

## Related Skills

* [`directory-tree-audit`](../directory-tree-audit/SKILL.md) — provides
  per-folder item counts and tree data that drive placement and sub-grouping
  decisions.
* [`project-structure`](../../project-structure/SKILL.md) — industry-standard
  folder-structure conventions that this taxonomy specializes for the skill
  library.

*

## 1. Domain Taxonomy

### 1.1 Top-Level Domains

```text
.agents/skills/
├── calendar/                     (4 items — flat)   <- NEW
├── cli/                          (7 items — flat)
├── database/                     (9 items — flat)
├── docker/                       (2 items — flat)   <- NEW
├── eclipse/                      (4 items — flat)
├── email/                        (2 items — flat)   <- NEW
├── general/                      (12 flat + 7 sub-groups)
├── git/                          (7 sub-groups)
├── github/                       (2 flat + 8 sub-groups)
├── java/                         (3 items — flat)
├── jira/                         (4 items — flat)
├── json/                         (3 items — flat)
├── markdown/                     (4 items — flat)
├── maven/                        (1 item — flat)
├── mcp/                          (3 items — flat; 2 pending-move)
├── media/                        (10 items — flat)
├── mise/                         (3 items — flat)
├── node/                         (2 items — flat)
├── opencode/                     (9 items — flat)
├── php/                          (1 item — flat)
├── project/                      (7 items — flat)
├── python/                       (3 items — flat)
├── testing/                      (4 items — flat)
├── text/                         (4 items — flat)
└── vscode/                       (5 sub-groups)
```

### 1.2 Sub-Groups

**general/** (7 sub-groups; 12 flat items remain at general/ level):

```text
general/
├── code-explanation
├── fnmatch-content-guard-pattern
├── harper-linting-suppression
├── ide-renderer-freeze-prevention
├── json-batch-file-move
├── json-group-stats
├── kv-line-parse
├── macos-screenshots-folder-split
├── onedrive-flat-folder-split-by-size
├── redaction-portability
├── repo-scratch-output-capture
├── yaml-field-extract                   <- NEW
│
├── comparison/               (2)
│   ├── folder-comparison
│   └── near-duplicate-file-comparison
│
├── file/                     (3)
│   ├── file-glob-sort-by-mtime
│   ├── safe-file-cleanup                <- NEW
│   └── scratch-artifact-naming
│
├── planning/                (5)
│   ├── planning-artifact-lifecycle
│   ├── planning-artifact-naming
│   ├── planning-superseded-version-retirement  <- NEW
│   ├── planning-version-coverage-audit         <- NEW
│   └── versioned-artifact-superset-build       <- NEW
│
├── polling/                  (1)
│   └── poll-until
│
├── setup/                    (4)
│   ├── dev-env-private-config-symlink
│   ├── google-oauth-setup
│   ├── tool-config-directory-symlink
│   └── tool-config-schema-probe
│
├── skill-dev/                (6)
│   ├── rule-to-skill-industrialization
│   ├── script-over-instruction-decomposition
│   ├── script-language-tier-port
│   ├── script-template-extraction
│   ├── skill-cross-reference-audit
│   └── skill-factory
│
└── session-audit/            (12)
    ├── agents-md-recovery-from-session
    ├── edit-application-from-session
    ├── file-recovery-from-session
    ├── opencode-session-bash-block-extractor
    ├── opencode-session-bash-file-ops-classifier
    ├── opencode-session-bash-write-extractor
    ├── opencode-session-diff-extractor
    ├── opencode-session-edit-extractor
    ├── opencode-session-write-extractor
    ├── session-audit-batch-orchestrator
    ├── session-file-ops-audit
    └── session-full-change-audit
```

**git/** (7 sub-groups):

```text
git/
├── basic/
│   ├── edit/                 (9) — atomic-commit-construction, commit-edit,
│   │                              noise-removal-via-commit-edit,
│   │                              separate-content-from-formatting-commits,
│   │                              drop-commit-with-divergent-recreation,
│   │                              git-commit-preview-verify,
│   │                              git-commit-edit-in-worktree,
│   │                              git-rebase-drop-noninteractive,
│   │                              git-commit-replace-and-replay
│   ├── message/              (4) — commit-message-bulk-reword,
│   │                              commit-message-reword,
│   │                              commit-metadata-extraction,
│   │                              commit-identity-rewrite
│   ├── audit/                (9) — commit-comparison-audit,
│   │                              commit-details-audit,
│   │                              cross-ref-file-parity,
│   │                              divergence-audit,
│   │                              ref-content-audit,
│   │                              deleted-files-audit,
│   │                              git-commit-dangling-link-audit,
│   │                              git-repository-status,
│   │                              git-worktree-state-fingerprint
│   └── history/              (2) — history-refinement,
│                                   untracked-scratch-triage
│
├── branch/                   (5) — absorbed-branch-decommission,
│                                  branch-promotion,
│                                  dependent-branch-restack-cascade,
│                                  parallel-branch-decommission,
│                                  rebase-standardization
│
├── config/                   (6) — clean-filter-renormalize-backfill,
│                                  jq-pretty-json-filter,
│                                  post-gitignore-untrack,
│                                  gitignore-rules,
│                                  gitignore-whitelist-pattern,
│                                  gitignored-reference-detection
│
├── repo/                     (5) — canonical-source-vs-workflow-repo-audit,
│                                  cross-repo-cherry-pick,
│                                  lfs-selective-clone,
│                                  repo-storage-minimization,
│                                  git-remote-origin-repoint
│
├── sandbox/                  (4) — personal-content-extraction,
│                                  personal-sandbox-remote,
│                                  personal-sandbox-restack,
│                                  personal-team-branch-workflow
│
├── stash/                    (3) — pre-execution-safety-stash,
│                                  stash-parent-commit,
│                                  stash-triage
│
└── submodule/
    ├── setup/                (4) — addition, selective-init-no-lfs,
    │                              uninitialized-audit,
    │                              uninitialized-handler
    ├── repair/               (6) — dead-upstream-audit,
    │                              misconfiguration-audit-and-revert,
    │                              missing-revision-recovery,
    │                              orphan-gitlink-recovery,
    │                              pointer-repair,
    │                              git-submodule-history-classification
    ├── fork/                 (2) — fork-reconfigure, fork-sync
    └── lifecycle/            (5) — commit-details, commit-reword,
                                   removal, readd,
                                   git-submodule-history-removal
```

**github/** (8 sub-groups; 2 flat items remain at github/ level):

```text
github/
├── copilot/                  (2) — activity-history-split,
│                                  chat-history-analysis
├── actions/                  (2) — run-audit, workflow-dispatch
├── repo/                     (10) — gh-repo-create, gh-repo-edit-metadata,
│                                   pr-edit, repo-commit-fetch,
│                                   rest-api-fallback, secrets-bulk-set,
│                                   pr-merge-decision-classifier,
│                                   github-repo-name-conflict-check,
│                                   github-repo-state-fingerprint,
│                                   github-repo-collaborator-remove
├── community-standards/      (10) — issue-template-bug,
│                                   issue-template-feature,
│                                   issue-template-documentation,
│                                   pr-template, gitignore-template,
│                                   code-of-conduct, contributing-guide,
│                                   security-policy, support-docs,
│                                   readme-template
├── workflows/                (6) — ci-markdown-lint, ci-python-lint,
│                                  sync-description, sync-topics,
│                                  pr-labeler, workflow-creation
├── composer/                 (7) — repo-templates, ci-lint, sync,
│                                  workflows, docs, repo-template,
│                                  repo-publish
├── renovate/                 (3) — renovate-config-patterns,
│                                  renovate-auto-rebase-detector,
│                                  renovate-dependent-branch-auto-rebase
│
├── transfer/                 (6) — destination-conflict-check,
│                                  baseline-capture, completion-poll,
│                                  initiate, verify, account-transfer
│
├── (flat: 2) — auth-fallback, github-api-poll-until
```

**vscode/** (5 sub-groups):

```text
vscode/
├── autoapprove/              (2) — command-autoapprove-onboarding,
│                                  autoapprove-entry-consolidation
├── config/                   (6) — antigravity-version-checker,
│                                  extension-portability,
│                                  nginx-filetype-config,
│                                  state-vscdb-merge,
│                                  state-vscdb-editor-extract,  ← NEW
│                                  active-window-editors          ← NEW
├── search/                   (2) — search-exclude-glob,
│                                  search-exclude-submodules
├── settings/                 (5) — multi-scope-setting-write,
│                                  setting-schema-discovery,
│                                  settings-indent-override,
│                                  settings-promotion,
│                                  user-settings-symlink
└── terminal/                 (2) — terminal-fallback-via-vscode-tasks,
│                                  terminal-autoapprove-audit
```

**database/** (9 items — flat):

```text
database/
├── db-backup-bracketing-protocol
├── mariadb-check-autoincrement-trigger-fallback
├── mysql-capability-probe-pymysql
├── mysql-fk-hardening-workflow
├── pg-cluster-backup-compare
├── pg-cluster-mirror
├── postgres-local-dump-restore
├── remote-mysql-roundtrip-minimization
└── staging-env-fetch
```

**docker/** (2 items — flat):

```text
docker/
├── docker-resource-cleanup          <- NEW
└── docker-resource-inventory        <- NEW
```

**email/** (2 items — flat):

```text
email/
├── email-poll-for-message
└── gmail-poll-for-message
```

**media/** (10 items — flat):

```text
media/
├── ffmpeg-lossless-concat
├── ffmpeg-lossless-split
├── media-audio-language-detect
├── media-timestamp-summary
├── webm-recording-interrupted-recovery
├── webm-recording-merge-with-filler
├── youtube-playlist-list
├── youtube-studio-settings
├── youtube-video-metadata-update
└── youtube-video-upload
```

**opencode/** (10 items — flat):

```text
opencode/
├── opencode-current-session-id
├── opencode-installed-plugin-lookup
├── opencode-session-log-cleanup                            <- NEW
├── opencode-session-path-attribution
├── opencode-session-problem-solution-workflow-analysis
├── opencode-session-transcript-to-source-resolve
├── opencode-session-yaml-conversation-extractor
├── opencode-session-yaml-tool-call-extractor
├── opencode-session-yaml-transcript-extractor
└── opencode-ssot-provider-ext-sync
```

**markdown/** (4 items — flat):

```text
markdown/
├── markdown-generation                        [pending-move — physical
│                                                 folder at .agents/skills/
│                                                 markdown-generation/; move
│                                                 requires cross-reference
│                                                 sweep of skill-doc-metadata-
│                                                 separation]
├── text-block-indent-override                 [pending-move — physical
│                                                 folder at .agents/skills/
│                                                 text-block-indent-override/]
├── markdown-section-to-companion-doc          <- NEW
└── skill-doc-metadata-separation              <- NEW
```

**calendar/** (4 items — flat):

```text
calendar/
├── gmail-event-email-to-ics                    <- NEW
├── ics-event-extraction-to-json                <- NEW
├── ics-event-generation-from-json              <- NEW
└── ics-to-google-calendar-event                <- NEW
```

**mcp/** (3 items — flat; 2 pending-move):

```text
mcp/
├── google-workspace-mcp-account-switch         <- NEW
├── mcp-cross-tool-config-sync                  [pending-move — physical folder at .agents/skills/mcp-cross-tool-config-sync/]
└── mcp-management                              [pending-move — physical folder at .agents/skills/mcp-management/]
```

*

## 2. Placement Rules

### 2.1 New Skill Placement

1. Match the new skill's topic keyword to a leaf group in §1.2.
2. Place it in that leaf group (e.g., a new `git-commit-signing` skill goes
   under `git/basic/edit/`).
3. If no leaf group matches the topic:
   * Create a new leaf group within the parent domain.
   * Verify the parent folder's item count stays ≤10 after addition (use
     `directory-tree-audit` if uncertain).
   * If the parent exceeds 10, propose and apply sub-grouping before adding.
4. Sub-groups are flat leaves — a leaf group MUST NOT itself be sub-grouped
   unless it reaches ≥10 items.

### 2.2 Cross-Cutting Skills

Skills that span multiple domains (e.g., `redaction-portability` applies to
all files, not just one domain) belong in `general/` — not in a specific
domain folder. If `general/` exceeds 10 flat items, create a sub-group.

*

## 3. Change Protocol

### 3.1 Adding a Group

* Add the new group to the tree in §1.2 with its item count.
* State the rationale in a `## Changelog` entry.
* Update every skill that references §1.2 (cross-reference sweep per
  `skill-factory` §5.1).

### 3.2 Removing a Group

* Move remaining items to sibling groups or `general/` before removing.
* Remove the group listing from §1.2.
* Cross-reference sweep.

### 3.3 Renaming a Group

* Update the name in §1.2.
* If the folder on disk is renamed, cross-reference sweep every skill that
  links to it via relative path.

*

## 4. Changelog

### 2026-09-30 — email/ domain added (2 items); github/transfer/ + general/polling/ sub-groups added; transfer suite placed

Added:

* **`email/`** (new domain, 2 items — flat): `email-poll-for-message` (provider-agnostic IMAP
  message poller composed over `poll-until`) and `gmail-poll-for-message` (Gmail preset fixing
  `imap.gmail.com:993` + `GMAIL_APP_PASSWORD`) — the provider-layered email stack for the
  repo-transfer suite's acceptance-email wait.
* **`github/transfer/`** (new sub-group, 6 items): `github-repo-transfer-destination-conflict-check`,
  `github-repo-transfer-baseline-capture`, `github-repo-transfer-completion-poll`,
  `github-repo-transfer-initiate`, `github-repo-transfer-verify`, `github-repo-account-transfer` —
  the transfer composites + top-level dispatcher documented from the executed account transfer.
* **`general/polling/`** (new sub-group, 1 item): `poll-until` — generic interval/attempt polling engine.
* **`github-api-poll-until`** (new base, `github/` flat, 1→2): API-endpoint poller over `poll-until`.
* **`github-repo-name-conflict-check`**, **`github-repo-state-fingerprint`**,
  **`github-repo-collaborator-remove`** (new bases, `github/repo/`, 7→10): destination
  name-availability checks, cross-owner state fingerprints, and collaborator removal.
* **`git-remote-origin-repoint`** (new base, `git/repo/`, 4→5): batch origin repointing with
  `git ls-remote` verification.

Updated Section 1.1 tree (`email/` added; `github/` reconciled to 2 flat + 8 sub-groups;
`general/` reconciled to 12 flat + 7 sub-groups) and Section 1.2 listings (`email/` flat block;
`github/transfer/` block; `general/polling/` block; `github/repo/` 7→10; `git/repo/` 4→5).

### 2026-09-27 — git/basic/audit/ + git/basic/edit/ 8->9: worktree-state-fingerprint + replace-and-replay added

Added:

* **`git-worktree-state-fingerprint`** (new base, `git/basic/audit/`): byte-level worktree state
  capture/compare (hashed porcelain, index, staged/worktree binary diffs, untracked listing) with an
  IDENTICAL / DELTA verdict and exit 0/1/2 — the Gate 1/8 proof primitive of
  `git-commit-edit-in-worktree` and the refresh-2 baseline gate of `git-submodule-history-removal`.
* **`git-commit-replace-and-replay`** (new base, `git/basic/edit/`): same-branch single-commit
  replacement (prepare / finish / verify) around `git rebase --autostash --onto <new> <target>
  <branch>` with main-worktree refusal and range-diff marker-accounting parity; the Mode B mechanic
  of `git-commit-edit-in-worktree`.

Updated Section 1.2 tree counts (`git/basic/audit/` 8->9, `git/basic/edit/` 8->9) and listings.

### 2026-09-26 — calendar/ domain added (4 items); mcp/ realized (3 items, 2 pending-move)

Added:

* **`ics-event-generation-from-json`** (new base, `calendar/`): deterministic JSON spec → RFC 5545 `.ics`
  emission (TEXT escaping, 75-octet UTF-8-safe folding, CRLF, UTC or TZID datetimes with `VTIMEZONE`
  templates, `VALARM`, built-in structural verification).
* **`ics-event-extraction-to-json`** (new base, `calendar/`): deterministic `.ics` → JSON parse (line
  unfolding, TEXT unescaping, parameter parsing, multi-VEVENT and VALARM support, zoneinfo-derived
  `utc`/`iso` datetime forms).
* **`gmail-event-email-to-ics`** (new composer, `calendar/`): Gmail event-invitation email (attached
  `.ics` or body-embedded details) → verified maximum-detail `.ics`, composing the google-workspace
  MCP Gmail tools + both calendar bases.
* **`ics-to-google-calendar-event`** (new composer, `calendar/`): `.ics` (or JSON spec) → verified
  Google Calendar event, composing the extraction base + google-workspace MCP calendar tools.
* **`google-workspace-mcp-account-switch`** (new base, `mcp/`): runtime account switch of the
  google-workspace MCP session (`auth_clear` → dependent follow-up call → identity verification).

Also enriched `opencode-current-session-id` and `scratch-artifact-naming` (concurrent-session caveats)
and cross-referenced `google-oauth-setup` and `mcp-management` toward the new MCP base.

Updated Section 1.1 tree (added `calendar/ (4 items — flat)`; `mcp/` 2→3 with 2 pending-move) and
Section 1.2 listings (`calendar/` flat group; `mcp/` group realized with `mcp-management` and
`mcp-cross-tool-config-sync` marked pending-move from their physical top-level folders).

### 2026-09-25 — github/repo/ expanded 6->7: pr-merge-decision-classifier added

Added:

* **`pr-merge-decision-classifier`** (new composer, `github/repo/`): classifies a PR's merge decision
  with a local Laya (Jev wire-compatible) System One model — read-only `gh` state, typed
  choice/score/noul questions, confidence/risk gate (0.9/0.5), MERGE/HOLD verdict JSON, and
  optional `--execute` auto-merge on MERGE.

Updated Section 1.2 listing (`github/repo/` 6->7 items).

### 2026-08-12 — general/file/ expanded 2->3; opencode/ expanded 9->10: session-log cleanup pair added

Added:

* **`safe-file-cleanup`** (new base, `general/file/`): generic safe-removal
  primitive that prefers the system trash/recycle bin when available, falls
  back to stdlib deletion otherwise, verifies removal, and emits JSON Lines
  with a 0/1/2 exit-code contract.
* **`opencode-session-log-cleanup`** (new composer, `opencode/`): discovers
  opencode logger-plugin artifacts for a session ID, enforces explicit user
  verification, delegates removal to `safe-file-cleanup`, and re-verifies
  that no artifacts remain.

Updated Section 1.1 tree counts (`general/file/` 2->3, `opencode/` 9->10)
and Section 1.2 listings.

### 2026-09-19 — github/renovate/ sub-group added (3 new skills)

Added:

* **`renovate-config-patterns`** (new base, `github/renovate/`): domain-agnostic Renovate config template
  assembly primitive with templates for base, automerge, monorepo, docker, python
* **`renovate-auto-rebase-detector`** (new base, `github/renovate/`): detects if Renovate will auto-rebase on
  base rewrite given current config + git state
* **`renovate-dependent-branch-auto-rebase`** (new composer, `github/renovate/`): orchestrates config generation +
  detection + git-dependent-branch-restack-cascade fallback for Renovate branch auto-rebase workflow

Updated Section 1.1 tree counts (github/ 6->7 sub-groups) and Section 1.2 listings.

### 2026-08-14 — submodule-history-removal skill cluster (4 new skills, 3 groups)

Added:

* **`git-rebase-drop-noninteractive`** (new base, `git/basic/edit/`): scripted
  non-interactive `git rebase -i` todo rewrite (drop / edit / reword) via a
  `GIT_SEQUENCE_EDITOR` writer with `--dry-run`; the todo primitive for the
  whole cluster.
* **`git-submodule-history-classification`** (new base, `git/submodule/repair/`):
  submodule registration inventory (`list-submodules.py`, `docs/
  uninitialized-submodules.md` counterpart) and per-commit classification of
  submodule-path commits (INTRO / POINTER-UPDATE / MIXED / REMOVAL) for
  pre-rewrite planning.
* **`git-commit-edit-in-worktree`** (new composer, `git/basic/edit/`): edit
  ANY commit (drop/amend/reword/edit) inside an isolated scratch worktree
  with an untouched-main-worktree baseline contract, scripted rebase, tree
  parity and `reset --soft` fast-forward.
* **`git-submodule-history-removal`** (new composer,
  `git/submodule/lifecycle/`): eleven-gate full-history submodule removal —
  classification → plan → safety → isolate → amend/recovery → tree-check →
  fast-forward → refresh-2 baseline → push → refresh-1 cleanup → post-push.

Updated Section 1.2 tree counts (`git/basic/edit/` 6->8, `git/submodule/
repair/` 5->6, `git/submodule/lifecycle/` 4->5) and listings.

### 2026-08-12 — opencode/ expanded 8->9: transcript-to-source-resolve composer added

Added:

* **`opencode-session-transcript-to-source-resolve`** (new composer, `opencode/`):
  resolves opencode session transcript references (single or `to N` ranges) in
  free text to the ACTUAL source log files under the session directory — the
  reverse direction of the conversation-only transcript extractor. Range
  expansion delegates to `file-glob-sort-by-regex-capture`'s `--min`/`--max`
  numeric-span filter (never re-implementing the glob+regex+sort pipeline).

Policy reaffirmed: pre-grouping skills (e.g. `opencode-config-preserve`,
`opencode-permission-config`, the markdown pending-move items) are NOT moved
by this change; only the new composer is placed in its taxonomy slot.

Updated Section 1.1 tree count (8->9) and Section 1.2 listing.

### 2026-08-11 — git/basic/edit/ 5->6: commit-preview-verify added

Added:

* **`git-commit-preview-verify`** (new base, `git/basic/edit/`): verifies whether
  commits listed in a `scratch/commit-preview.md` (produced by
  `git-atomic-commit-construction`) have been executed against `git log`;
  text/JSON output; optional `--cleanup` gate (deletes only when all commits done).

Updated Section 1.2 tree count (5->6) and listing.

### 2026-08-11 — opencode/ expanded 7->8: conversation-only YAML transcript extractor added

Added:

* **`opencode-session-yaml-conversation-extractor`** (new base, `opencode/`):
  conversation-only YAML transcript (user.text + assistant.response, agent iff
  compaction) from opencode logger-plugin YAML session logs — drops
  thinking/tool_calls/model/time/duration, preserves YAML structure via
  ruamel.yaml round-trip. Parallel base to
  `opencode-session-yaml-transcript-extractor` (which emits all-fields JSONL).

Updated Section 1.1 tree count (7->8) and Section 1.2 listing.

### 2026-08-11 — docker/ group added (2 items): resource-cleanup skill pair

Added:

* **`docker-resource-inventory`** (new base, `docker/`): deterministic JSON/text
  inventory of Docker resources (running/stopped containers, images, volumes,
  build cache with `size_bytes`/`reclaimable_bytes`); daemon-reachability gate;
  exit-code contract (0/1/2/3).
* **`docker-resource-cleanup`** (new composer, `docker/`): cleans resources with
  mandatory base pre-flight, a human scope gate (`full`/`keep-running`/`unused`),
  stop-before-remove discipline, volume-prune survivor sweep, and post-cleanup
  verification — delegating all enumeration to the base primitive.

Updated Section 1.1 tree (added `docker/ (2 items — flat)`) and Section 1.2
listing (added `**docker/** (2 items — flat)**`).

### 2026-08-11 — markdown/ group realized 2->4: metadata-separation skill pair added

Added:

* **`markdown-section-to-companion-doc`** (new base, `markdown/`): moves a named
  `## Section` out of any markdown doc into a sibling `<NAME>.md` companion file,
  leaving a pointer paragraph; idempotent check/split/dry-run modes.
* **`skill-doc-metadata-separation`** (new composer, `markdown/`): audits and splits
  skill-doc metadata sections (`Changelog` / `Traceability`) into `CHANGELOG.md` /
  `TRACEABILITY.md` companion files, library-wide or per-skill, delegating all file
  mutation to the base primitive.

Updated Section 1.1 tree count (2→4) and Section 1.2 listing: the `markdown/` flat group
now names all four items; `markdown-generation` and `text-block-indent-override` are
marked pending-move from their physical top-level folders.

### 2026-08-11 — opencode/ reconciled 5→7; session-analysis family added

Added:

* **`opencode-session-yaml-transcript-extractor`** (new base, `opencode/`): per-turn transcript
  JSONL (session header / user text / thinking / tool calls) from logger YAML logs — parallel
  base to `opencode-session-yaml-tool-call-extractor`, superset carrying the narrative.
* **`opencode-session-problem-solution-workflow-analysis`** (new composer, `opencode/`):
  problem/solution/executed-workflow report reconstruction over the transcript base.

Updated Section 1.1 tree count (5 physical items reconciled against the stale 6/7 listing —
`opencode-config-preserve` and `opencode-permission-config` physically live at top level and
were removed from this list) and Section 1.2 listing.

### 2026-08-08 (suite) — opencode/ expanded 4->6; git/basic/audit/ 7->8

Added:

* **`opencode-session-path-attribution`** (new base, `opencode/`): cross-session sweep of
  logger turn YAMLs, token-matched, consuming `opencode-session-yaml-tool-call-extractor` CLI.
* **`opencode-installed-plugin-lookup`** (new base, `opencode/`): read-only plugin registry
  (enabled-config / enabled-auto-dir / missing), logger logs convention.
* **`git-commit-dangling-link-audit`** (new composer, `git/basic/audit/`): pre-commit relative
  link classifier (EXISTS / GIT_ONLY / DANGLES / IGNORED) with session-evidence drift gate.

Updated Section 1.1 tree counts and Section 1.2 listings; changelog entry for the
dangling-commit-link suite (2026-08-08).

### 2026-08-08 -- general/planning/ expanded 4->5 -- versioned-artifact-superset-build added

Added:

* **`versioned-artifact-superset-build`** (new base, `general/planning/`): deterministic construction of vN+1 as vN
  byte-verbatim + appended deltas (Verbatim-Superset Construction, mandated in `ai-agent-planning-rules.md` §7.1).
  Authoring-side companion to `planning-version-coverage-audit`; composed by `planning-artifact-lifecycle` Step 3.

Updated Section 1.1 tree counts and Section 1.2 listing; cross-reference sweep (lifecycle SKILL+AGENTS,
coverage-audit SKILL+AGENTS, naming SKILL+AGENTS, `ai-agent-planning-rules.md` §7.1, `AGENTS-legacy.md`).

### 2026-08-07 -- general/ new planning/ sub-group (4 items); flat 12->10, sub-groups 5->6

Added:

* **`general/planning/`** (4 items, new sub-group): `planning-artifact-lifecycle` (moved from
  `general/` flat), `planning-artifact-naming` (moved from `general/` flat),
  `planning-version-coverage-audit` (new base — literal section-by-section coverage audit
  gate), `planning-superseded-version-retirement` (new composer — authorized retirement
  of a superseded version after FULL coverage audit + user consent).

Rationale: the two existing planning skills sat unnamed at `general/` flat while the
retirement workflow (coverage audit → authorization → trash → stale-ref sweep → task.md
re-sync) gained two new layered skills; grouping them under `general/planning/` keeps the
planning domain scannable and under the 8±2 flat limit.

Updated Section 1.1 tree counts and Section 1.2 listings; re-based cross-references in
`pre-commit-verification-protocol` (SKILL + AGENTS) and `AGENTS-legacy.md` rows.

### 2026-07-05 -- general/ flat expanded 11->12, opencode/ expanded 2->3

Added:

* `kv-line-parse` to `general/` flat list -- base key-value line parser script
* `opencode-ssot-provider-ext-sync` to `opencode/` flat list -- composer skill for SSOT->provider-extension sync
workflow

Updated Section 1.1 tree counts and Section 1.2 listings.

### 2026-06-20 — github/ expanded: 3 new sub-groups + 1 sub-group promoted from flat

Added 30 new skills:

* **`github/repo/`** (6 items, promoted from flat): `gh-repo-create` (B1),
  `gh-repo-edit-metadata` (B2), plus 4 existing skills moved from flat.
* **`github/community-standards/`** (13 items): docs structure
  (`github-docs-structure`), docs readme (`github-docs-readme`),
  folder structure (`github-folder-structure`), issue/PR templates
  (B3-B6), `.gitignore` (B12), code of conduct (B13), contributing guide
  (B14), security policy (B15), support docs (B16), README template (B17).
* **`github/workflows/`** (6 items): markdown lint (B7), python lint (B8),
  sync description (B9), sync topics (B10), PR labeler (B11),
  workflow-creation (existing, moved from flat).
* **`github/composer/`** (7 items): repo-templates (C1), ci-lint (C2),
  sync (C3), workflows (C4), docs (C5), repo-template (C6),
  repo-publish (C7).

Flat reduced from 6 to 1 (`auth-fallback`). Updated §1.1 tree count.

### 2026-06-20 (batch 2) — post-drafting fix pack: 3 new base skills + 23 template files extracted

Added 3 missing base skills: `github-docs-structure` (docs/ tree),
`github-docs-readme` (docs/README.md), `github-folder-structure`
(repo skeleton). Extracted 23 embedded template strings into
standalone `.template` files. Fixed broken script path in C7
`publish-repo.py`. Added 4 missing See Also links in
`github-workflow-creation`. Removed 5 empty stub directories.

### 2026-06-20 — general/skill-dev/ expanded: 5→6 — skill-cross-reference-audit added

Added `skill-cross-reference-audit` — a base skill that automates auditing
the skill library for cross-reference issues (duplicates in Composition +
Related Skills, missing AGENTS.md, missing frontmatter, empty sections).
Consumed by skill-factory §3 Composition Audit step.

### 2026-06-20 — general/skill-dev/ expanded: 4→5 — script-template-extraction added

Added `script-template-extraction` — a base skill that automates the
Template Extraction Mandate (skill-factory §2.2.1.1 mandate #6) for
existing scripts that embed file content as string constants. Alphabetized
the skill-dev listing.

### 2026-06-20 — opencode/ domain added (1 item)

New domain for opencode tool configuration skills. Initial member:
`opencode-permission-config`. Added `opencode/` to the §1.1 tree
and created the flat listing in §1.2.

### 2026-07-02 — general/setup/ expanded: 3→4 — tool-config-directory-symlink added

Added `tool-config-directory-symlink` — generic base skill for migrating tool
configuration directories (XDG) into a managed companion repo with symlinks.
Placed under `general/setup/` as a cross-cutting infrastructure primitive.
Also added `opencode-config-preserve` to `opencode/` domain (now 2 items).

### 2026-07-04 — general/session-audit/ new sub-group (12 items): session export audit skills

Added 12 session-export audit skills as a new `session-audit/` sub-group under
`general/`:

* `agents-md-recovery-from-session` — AGENTS.md recovery via git diff extraction
* `edit-application-from-session` — replay Tool: edit operations onto disk
* `file-recovery-from-session` — recover files from Tool: write + bash heredocs
* 4 opencode-session extractors (bash-block, bash-file-ops-classifier,
  bash-write, diff, edit, write) — base primitives for session parsing
* `session-audit-batch-orchestrator` — batch audit across multiple session files
* `session-file-ops-audit` — bash-only file operations audit
* `session-full-change-audit` — unified all-source change audit
Updated §1.1 tree from 3 sub-groups to 4; flat count unchanged (11 items).

### 2026-07-01 — fnmatch-content-guard-pattern added to general/ flat list

Added `fnmatch-content-guard-pattern` to general/ flat listing.
Updated count from 10 to 11 in §1.1 tree.

*

### 2026-07-31 — opencode/ expanded 2→4; §1.2 tree reconciled with physical layout

Added `opencode-session-yaml-tool-call-extractor` (base primitive for the
YAML-log upgrade of the session file-changes extractor family) and back-filled
`opencode-current-session-id`, which the §1.2 tree had never listed even
though §1.1 claimed 4 items. §1.1 `(4 items — flat)` count now matches the
§1.2 tree exactly.

* `opencode-current-session-id` — resolves the current session ID/title from logger logs
* `opencode-session-yaml-tool-call-extractor` — YAML-log → tool-call JSONL base primitive
Updated §1.1/§1.2 from (4 claimed / 2 listed) to 4 listed items.

*

### 2026-06-17 — general/ flat expanded from 6→10

Added 4 OneDrive flat-folder split skills that sit at the intersection of
file-management, JSON processing, and macOS domain knowledge — too
cross-cutting for a specific domain folder:

* `json-batch-file-move` — batch file moves keyed by JSON array
* `json-group-stats` — JSON array group-by with count
* `macos-screenshots-folder-split` — domain composer wrapping the below
* `onedrive-flat-folder-split-by-size` — composer for OneDrive threshold splitting

Updated count from 6 to 10 in §1.1 tree; added entries to the flat listing
in §1.2.

*

### 2026-06-16 — database/ expanded from 6→9

Added 3 general database skills from oleovista-acers generalization:

* `pg-cluster-backup-compare` — ClusterSplit backup + dump compare protocol
* `pg-cluster-mirror` — Five-phase cluster mirror with audit-before-act
* `staging-env-fetch` — .env fetch from staging via ssh-staging MCP tool

Updated count from 6 to 9 in §1.1 tree; added detailed flat listing under §1.2.

*

## 5. Related Skills

* [`human-scanable-organization`](../human-scanable-organization/SKILL.md) —
  the 8±2 principle that governed this taxonomy's design.
* [`skill-factory`](../../skill-factory/SKILL.md) — consumer whose Post-Drafting
  Checklist enforces compliance with this taxonomy.
* [`directory-tree-audit`](../directory-tree-audit/SKILL.md) — tool for
  verifying item counts during placement decisions.

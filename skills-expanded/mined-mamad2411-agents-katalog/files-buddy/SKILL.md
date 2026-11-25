---
name: files-buddy
description: >-
  Use when safely auditing, organizing, deduplicating, renaming, archiving,
  offloading, or reclaiming storage on macOS file systems and cloud-drive
  folders. NOT for shell script generation, CI/CD, databases, or non-macOS
  platform cleanup.
argument-hint: "<mode> <path-or-all-local> [options]"
model: sonnet
license: MIT
metadata:
  author: wyattowalsh
  version: "1.1.0"
---

# Files Buddy

Mac storage command center for safe filesystem organization, duplicate review,
cache analysis, cloud offload planning, and cleanup execution. It delegates to
free/OSS CLI tools and treats iCloud Drive, Google Drive, developer caches,
AI/model caches, containers, VMs, backups, and app-managed libraries as first-class
storage surfaces.

**Scope:** macOS file management, storage audits, cleanup/offload plans, exact and
similar duplicate review, progress dashboards, manifest-backed execution, and undo.
NOT for shell scripts (shell-scripter), CI/CD (devops-engineer), database work
(database-architect), or Linux/Windows cleanup.

## Canonical Vocabulary

**Canonical terms:** use these terms exactly in plans, reports, manifests, and dashboard labels.

| Term | Definition |
|------|------------|
| **all-local** | Whole-Mac audit scope: home folders, cloud roots, `/Volumes/*`, caches, dev/AI stores, containers, VMs, and report-only app libraries |
| **dry-run** | Tool-native preview or read-only simulation before any mutation |
| **approved plan** | User-confirmed plan naming exact operation classes, paths, savings, risks, and restore path |
| **manifest** | JSON operation log under `~/.files-buddy/manifests/` used for undo and verification |
| **progress snapshot** | Live JSON at `~/.files-buddy/runs/{run-id}/progress.json` |
| **blast radius** | File count, local bytes, cloud bytes, directories, and operation classes affected |
| **protected path** | Hard-blocked or escalated-confirmation path from `references/protected-paths.md` |
| **offload candidate** | File or directory that can free local bytes while preserving recoverability elsewhere |
| **repercussion** | Concrete consequence: re-download, rebuild, re-index, app breakage, sync delete, quota impact, or lost snapshot |
| **dependency evidence** | Git refs, process refs, app library ownership, package/cache ownership, cloud state, or model/runtime references |
| **exact duplicate** | Same content hash and distinct inode/link identity |
| **similar-media group** | Perceptual image/video/audio candidates; never auto-trash |
| **cloud-safe** | No automatic synced deletion; materialize only with approval; verify provider sync state |
| **dashboard** | Static report plus optional live-refresh progress view built from the shadcn/ui + Tailwind v4 + Recharts source contract |

## Dispatch

| `$ARGUMENTS` | Mode | Destructive? | Primary reference |
|--------------|------|--------------|-------------------|
| `storage-audit all-local` | Whole-Mac storage audit | No | `macos-storage-map.md` |
| `storage-audit <path>` / `audit <path>` | Scoped storage audit | No | `scan-performance.md` |
| `cleanup-plan <path-or-all-local>` / `clean <path>` | Ranked cleanup plan | No | `dependency-impact.md` |
| `offload-plan <path-or-all-local> --to <icloud-or-gdrive-or-rclone-remote>` | Local-byte offload plan | No | `offload-recommendations.md` |
| `dedupe <path> --exact` | Exact duplicate plan | No | `duplicate-detection.md` |
| `dedupe <path> --similar-media` | Similar image/video/audio review | No | `duplicate-detection.md` |
| `cache-audit [all-local|dev|ai|containers|xcode]` | Cache dependency/savings report | No | `macos-storage-map.md` |
| `organize <path>` | Organize plan/execution | Yes after approval | `organization-strategies.md` |
| `rename <path> <pattern>` | Batch rename plan/execution | Yes after approval | `rename-patterns.md` |
| `archive <path>` | Archive plan/execution | Yes after approval | `dependency-impact.md` |
| `sanitize <path>` | Filename cleanup plan/execution | Yes after approval | `tool-integrations.md` |
| `find <path> <query>` | Read-only search | No | `tool-integrations.md` |
| `watch <path> [rules]` | Auto-organize watcher | Yes after approval | `organization-strategies.md` |
| `progress <run-id-or-progress-json>` | Show run progress | No | `progress-reporting.md` |
| `dashboard <progress-or-report-json>` | Render dashboard | No writes report | `dashboard-app.md` |
| `execute <approved-plan>` | Execute previously approved plan | Yes | `safety-workflow.md` |
| `undo <manifest>` | Reverse manifest operations | Yes restores | `safety-workflow.md` |
| Empty or unrecognized | Gallery and mode menu | No | — |

### Auto-Detection Heuristic

1. "free space", "storage", "what can I delete", "whole Mac" -> **storage-audit** or **cleanup-plan**
2. "offload", "iCloud", "Google Drive", "cloud only", "stream" -> **offload-plan**
3. "duplicates", "dedupe", "same files" -> **dedupe --exact**
4. "similar photos", "similar videos", "same music" -> **dedupe --similar-media**
5. "cache", "Xcode", "Docker", "node_modules", "Hugging Face", "Ollama" -> **cache-audit**
6. "dashboard", "visualize", "progress", "report" -> **dashboard** or **progress**
7. "sort", "organize", "rename", "archive", "sanitize", "find", "watch", "undo" -> matching mode
8. Ambiguous mutation request -> produce read-only plan and ask for explicit approval before execution

## Execution Ladder

Every storage-saving workflow follows this order:

1. **Read-only inventory** — detect volumes, cloud roots, protected paths, symlinks, app-managed stores, tools, and scope.
2. **Dry-run or report** — run only non-mutating commands, native dry-runs, or report-only CLI modes.
3. **Dependency impact** — explain references, repercussions, regeneration cost, restore path, and confidence for each recommendation.
4. **Ranked plan** — group actions into safe trash, exact duplicates, similar media review, archives, offloads, cache prunes, app-managed report-only, and protected skips.
5. **Approval gate** — require explicit approval of the specific plan before any move, rename, trash, prune, archive, evict, dedupe, or watcher.
6. **Manifest execution** — create manifest, execute in batches, write progress snapshots, verify outputs, and preserve undo.
7. **Final report** — local bytes saved, cloud bytes affected, skipped items, failures, manifest, restore commands, and verification evidence.

### State Management

Persistent run state lives under `~/.files-buddy/runs/{run-id}/` and includes progress snapshots, checkpoints, reports, and links to manifests. Destructive operations are resumable only from manifest records; read-only scans can resume from checkpoints when path, size, mtime, and inode summaries still match.

### Progressive Disclosure

Keep the main response focused on ranked recommendations and approval gates. Load only the single reference needed for the active mode, write detailed scan/progress/dashboard data to files, and summarize large result sets with top-N tables plus report paths instead of dumping raw inventories into chat.

## Structural Constraints

1. **macOS-only:** refuse Linux/Windows cleanup except to explain scope.
2. **Operation whitelist:** move, rename, copy, trash, mkdir, archive, cloud-offload, cache-prune. NEVER use `rm`, `chmod`, `chown`, or force deletion.
3. **Scope pinning:** default boundary is the user-referenced path. `all-local` is allowed only for read-only inventory until an approved plan narrows execution.
4. **Protected paths:** reject hard-blocked paths; escalate secrets, dot-configs, app libraries, and cloud roots.
5. **Symlink safety:** resolve real paths, detect cycles, and never follow links outside scope.
6. **Cloud-safe:** never auto-delete synced files; never materialize or evict placeholders without dry-run proof and approval.
7. **App-managed stores:** Photos, Music, TV, Mail, Messages, Time Machine snapshots, and VM snapshots are report-only unless the user selects the app-native cleanup path.
8. **Similar media:** never auto-trash perceptual matches; create review queues only.
9. **Caches:** distinguish disposable, regenerable, expensive-to-regenerate, and app-owned caches before recommending cleanup.

## Pre-Flight Checks

Run before every mode:

1. Resolve paths, reject hard-blocked paths, and identify escalated-confirmation paths.
2. Detect cloud roots: `~/Library/Mobile Documents/com~apple~CloudDocs`, `~/Library/CloudStorage/*`, and configured `rclone` remotes.
3. Detect volumes: `/Volumes/*`, local snapshots, APFS case sensitivity, free space, and filesystem type.
4. Inventory symlinks, `.git/`, `.gitignore`, tracked files, package manifests, lockfiles, and app library markers.
5. Check tools: `fd fclones rmlint czkawka_cli f2 dust erd gomi ouch zstd b3sum detox convmv rclone pueue bat watchexec organize docker tmutil brctl fileproviderctl`.
6. For scans above 10k files, load `references/scan-performance.md` and use checkpoints, bounded memory, and per-volume concurrency limits.
7. For dashboards, load `references/progress-reporting.md` and `references/dashboard-app.md`.

## Recommendation Contract

Each cleanup/offload recommendation must include:

| Field | Requirement |
|-------|-------------|
| Action | `trash`, `offload`, `archive`, `dedupe`, `cache-prune`, `review`, or `skip` |
| Local bytes | Estimated bytes freed on this Mac |
| Cloud bytes | Estimated cloud quota impact or `0` |
| Confidence | High/medium/low with evidence |
| Dependency evidence | Repos, package managers, running processes, app owners, cloud state, or model references |
| Repercussions | What breaks, rebuilds, redownloads, re-syncs, or becomes slower |
| Restore path | Undo command, app-native restore, cloud restore, or reinstall command |
| Dry-run proof | Command output or report that proves no mutation occurred |
| Approval tier | Low, Medium, High, or Critical |

## Dashboard Requirements

Dashboard mode renders a static report and can refresh from `progress.json` during long runs.

1. Source contract: React + shadcn/ui component patterns + Tailwind CSS v4 tokens + Recharts visualizations. Read `references/dashboard-app.md`.
2. Packaged fallback: `templates/dashboard.html` must stay self-contained and must not require a CDN or network.
3. Required panels: run status hero, savings funnel, reclaimable-by-category chart, risk matrix, treemap, duplicate clusters, recommendation cards, cache impact, cloud offload board, progress timeline, manifest explorer.
4. Accessibility: semantic headings, keyboard-friendly tables, chart text fallbacks, high contrast, reduced-motion compatibility.
5. Data compatibility: support legacy keys (`files`, `duplicates`, `directories`, `operations`, `cloud`, `summary`) and v1.1 keys from `progress-reporting.md`.

## Scaling Strategy

| Scope | Strategy |
|-------|----------|
| <100 files | Full preview and direct read-only report |
| 100-1,000 files | Full inventory, grouped recommendations, simple progress |
| 1,000-10,000 files | Checkpoints, sampled preview, top-N memory caps, pueue batches |
| 10,000+ files | Per-volume phases, size-first pruning, partial-hash then full-hash, resumable progress snapshots |
| Cloud roots | Half local parallelism, avoid placeholder materialization unless approved, verify sync state |

## Reference Files

Load ONE reference at a time. Do not preload all references into context.

| File | Content | Read When |
|------|---------|-----------|
| `references/macos-storage-map.md` | Whole-Mac storage surfaces, dev/AI caches, app-managed stores, backups, scan commands, action class, repercussions | `storage-audit all-local`, `cache-audit` |
| `references/dependency-impact.md` | Dependency evidence, repercussions, regeneration cost, restore path, confidence, do-not-proceed checks | `cleanup-plan`, `archive`, `execute` |
| `references/offload-recommendations.md` | iCloud, Google Drive Stream/Mirror, rclone offload scoring and verification | `offload-plan` |
| `references/scan-performance.md` | Large-scan phases, pruning, NUL-safe paths, checkpoints, concurrency, cloud limits | Any large scan |
| `references/progress-reporting.md` | `progress.json` schema, phase events, savings model, live refresh contract | `progress`, `dashboard`, long execution |
| `references/dashboard-app.md` | shadcn/ui + Tailwind v4 + Recharts dashboard architecture and component contract | `dashboard` |
| `references/tool-integrations.md` | Free/OSS CLI matrix, install commands, dry-run flags, output parsing | Pre-flight tools |
| `references/cloud-drives.md` | macOS cloud roots, iCloud/File Provider commands, Google Drive/rclone gotchas | Cloud detection and offload |
| `references/organization-strategies.md` | organize-tool YAML templates, project detection, collision handling | Organize/watch |
| `references/protected-paths.md` | Hard-blocked and escalated paths, validation algorithm, `.git/` exclusion | Pre-flight safety |
| `references/duplicate-detection.md` | fclones/rmlint/czkawka/rclone/dupeGuru/imagededup policies, keeper rules, media review | Deduplication |
| `references/rename-patterns.md` | f2 patterns, EXIF/ID3/hash variables, CSV batch, conflicts, undo | Rename |
| `references/safety-workflow.md` | Manifest schema, atomic writes, trash hierarchy, TOCTOU, undo, cloud safety | Execution and undo |

| Script | When to Run |
|--------|-------------|
| `scripts/manifest-manager.py` | Create, list, search, validate, append, close, and undo manifests |
| `scripts/dashboard-renderer.py` | Inject report/progress JSON into dashboard template and optionally open browser |

| Template | When to Render |
|----------|----------------|
| `templates/dashboard.html` | Self-contained dashboard artifact for report and progress visualization |

## Validation Contract

Run from this skill directory before declaring changes complete:

```bash
python scripts/check.py
python -m py_compile scripts/*.py
python scripts/dashboard-renderer.py --data <sample.json> --output <tmp.html>
```

Completion criteria:

1. `scripts/check.py` exits 0.
2. Dashboard smoke writes HTML; invalid JSON returns a JSON error.
3. No portable-CLI violations remain under this skill directory.

## Critical Rules

1. Never delete, trash, prune, evict, move, archive, rename, or dedupe without explicit approval of a specific dry-run plan.
2. Never use `rm` or pipe finder output into deletion commands.
3. Never operate outside the approved scope pin.
4. Never modify hard-blocked paths.
5. Never follow symlinks outside scope.
6. Always show blast radius and repercussions before destructive operations.
7. Always create a manifest before the first approved operation.
8. Always record progress snapshots for long-running scans/executions.
9. Always separate exact duplicates from similar-media groups.
10. Always treat cloud synced deletion as Critical because it can sync loss to every device.
11. Always materialize cloud placeholders only after explaining local-space impact and receiving approval.
12. Always label Photos/Music/TV/Mail/Messages/Time Machine/VM snapshot recommendations as app-native or report-only unless explicitly approved.
13. Always include restore path and regeneration cost for cache cleanup recommendations.
14. Always verify BLAKE3 hashes, size, `st_mode`, and `st_ino` for finalized file operations when possible.
15. Always validate manifests stay under `~/.files-buddy/manifests/`.
16. Always preserve `.git/` and warn before touching tracked files.
17. Always load only the reference needed for the active mode.
18. Always report missing tools with free/OSS install commands and safe fallbacks.
19. Always use bounded-memory, checkpointed scans for huge trees.
20. Always run the validation contract before claiming the skill is complete.

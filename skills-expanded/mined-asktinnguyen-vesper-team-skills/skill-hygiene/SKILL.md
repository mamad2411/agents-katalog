---
name: skill-hygiene
description: Audit and clean installed agent skills across computers, global libraries, project roots, and session providers. Use for skill hygiene, stale skill cleanup, duplicate installs, broken links, or archived skills leaking into default sessions.
---

# Skill Hygiene

Keep runtime skill discovery intentional while preserving recoverable archives. Support any operating system, project, or agent host by discovering its actual configuration. Do not assume this machine's paths or one provider's loading behavior applies elsewhere.

## Scope and authorization

For a review request, inventory and recommend without mutations. For an authorized cleanup, execute agreed removals and clear mechanical fixes within that scope without asking again. Archive rather than permanently delete. Do not classify unfamiliar skills as useless on the user's behalf. Present uncertain choices as candidates; continue independent cleanup already authorized.

This skill handles installed-library hygiene. Use an available authoring or curation skill only when rewriting or merging skill content is actually requested. Do not schedule recurring jobs, publish backups, push repositories, or change provider settings merely because hygiene is requested.

## Discover the effective sources

1. Establish the target applications/providers, project, and whether the user means default sessions, project sessions, or both. Inspect configuration and relevant local instructions. Read only necessary configuration fields; never dump credentials, environment secrets, session histories, or authentication files.
2. Find configured skill roots and overrides, shared libraries, project-local skill folders, ancestor instructions, plugin-managed sources, symlink destinations, and any provider-specific home. Common candidates include `$CODEX_HOME/skills`, `~/.codex/skills`, and `~/.agents/skills`; these are discovery hints, not an exhaustive or guaranteed loader specification. Account for Windows paths, environment overrides, and remote daemons.
3. For hosts such as Paseo, identify the selected provider and its effective home/configuration. A host may inherit provider skills rather than owning a separate skill library. A local filesystem audit does not establish what a remote daemon loads.
4. Prefer the runtime's actual skill listing or startup catalog as evidence. If necessary, inspect available local loader code or official documentation. Record whether recursion, hidden directories, symlinks, project ancestors, and plugins are scanned. Mark unknown behavior explicitly.

## Inventory and classify

Record each entry's lexical path, resolved path, type (directory, file, symlink, broken symlink), origin, skill name/description, and relevant validation findings. Use `lstat`/equivalent: directory-only traversal hides broken symlinks. Avoid following directory links recursively; prevent cycles and duplicate traversal.

Count top-level packages, recursively discovered skill entrypoints, broken links, and archived entries separately. State which count is being reported. Identify system and plugin-owned packages before proposing changes.

Use evidence-based categories:

- **Archive leakage:** `SKILL.md` files in backup/retired folders still appear in discovery. `NOT USED`, `Backup`, or a renamed directory does not disable a recursively scanned skill.
- **Broken links:** inspect the link target and check whether an unavailable volume or remote mount explains it. Archive the link itself when authorized; never mutate its target. Preserve relative link target text in the manifest because moving it changes resolution.
- **Duplicate packages:** distinguish aliases to the same file from separate copies. Compare the entire package: relative paths, file bytes, symlink targets, and meaningful executable bits. Identical `SKILL.md` alone is insufficient. Keep the copy the target runtime can demonstrably discover, with an intentional source of truth. Plugin-prefixed names do not prove separate copies exist.
- **Malformed packages:** validate frontmatter and required fields using the target format, then inspect actual resource links. Missing scripts or references matter; illustrative links inside examples may be false positives.
- **Stale behavior or dependencies:** read instructions for removed commands, unavailable integrations, obsolete paths, contradictory defaults, and already-retired dependencies. Check inbound references from retained skills before archiving dependencies.
- **Overlapping intent:** compare outcomes and procedures. Similar names, small wrappers, one-file skills, many assets, tests, or a `.git` folder do not establish staleness. Modification dates and absent usage logs are weak evidence.

Assign each finding a reason, confidence, proposed action, retained replacement (if any), and effect on discovery. Do not claim a content review if only filenames and file counts were examined.

## Apply a recoverable cleanup

Choose an archive destination outside every relevant scanned root, including project and shared roots. Verify both lexical and resolved paths; relocating under another scanned ancestor or linking the archive back defeats isolation. Use a dated `NOT USED` directory if helpful. If a confirmed loader supports explicit disabling, that is an alternative when moving is unsuitable; back up configuration first.

Before each move:

- Confirm scope and current source state; do not rely on an earlier inventory after concurrent edits.
- Refuse destination collisions instead of silently nesting or overwriting packages.
- Record source, destination, reason, entry type, link target, and content fingerprint where applicable.
- Preserve complete directories and resources. Use portable filesystem APIs; do not assume GNU `find`, Bash word splitting, or POSIX-only paths.

Write a manifest outside scanned roots, update each operation to succeeded/failed after execution, and record partial failures honestly. For cross-volume moves, verify the copied content before removing the source. Archive only the selected link when the entry is a symlink. Do not rewrite its target repository.

A minimal manifest includes:

```json
{
  "created_at": "ISO-8601 timestamp",
  "scope": {"applications": [], "roots": []},
  "operations": [
    {"source": "absolute path", "destination": "absolute path", "reason": "evidence", "type": "directory or symlink", "status": "planned", "link_target": null, "fingerprint": null}
  ],
  "verification": {"filesystem": "pending", "runtime_discovery": "pending"}
}
```

Keep original paths so restoration is deterministic. To restore, verify the original location is vacant, restore the archived entry, and recheck discovery. Do not bulk-restore without a selected scope.

## Verify and report

Reinventory all touched roots, including broken links and nested archived entrypoints. Verify moved packages' contents, retained duplicate replacements, destination isolation, and manifest totals. Scan retained references to moved paths and report unresolved dependencies rather than silently redirecting them.

When available, refresh or inspect a fresh runtime skill catalog for each affected provider. An existing conversation can retain old instructions even after filesystem cleanup. Do not interrupt sessions or restart daemons without authorization. If fresh-session validation is unavailable, report filesystem verification separately and give the exact remaining runtime check; do not promise that every session is clean.

Report concrete counts by category, paths changed, archive and manifest links, retained sources, verified catalog behavior, and remaining uncertain candidates. Keep system/plugin updates and subjective pruning separate from mechanical cleanup. For the next run, compare against the manifest and current runtime inventory; do not assume archived skills stayed undiscoverable or removed links were not recreated by an installer.

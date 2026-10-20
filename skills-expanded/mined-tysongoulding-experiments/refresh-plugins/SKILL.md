---
name: refresh-plugins
argument-hint: '[plugin-name] — optional; defaults to every plugin the audit reports as changed'
description: >
  Publish-cycle skill for this repo (ember-claude-toolkit). Use after editing
  anything under plugins/<name>/ — validates the changed plugin(s) and the
  root marketplace manifest, bumps semver in plugin.json, keeps
  .claude-plugin/marketplace.json in sync, commits, tags a release, and pushes.
  Trigger on "/refresh-plugins", "refresh the plugins", "publish this plugin",
  or "cut a release" while working in this repo.
---

# refresh-plugins

Publishes edits made under `plugins/<name>/` in this repo. This is the
**publish** step, not the **use** step — Sara's own daily use of a plugin
comes from a live symlink at `~/.claude/skills/<name>` pointing straight at
`plugins/<name>` in this repo (the `@skills-dir` mechanism), so her own edits
are already active next session with no refresh needed. This skill exists for
the two cases where a refresh genuinely matters:

- **Anyone consuming a plugin through the marketplace-install path** (a
  teammate, a second machine, or Sara testing the install path herself)
  instead of the skills-dir symlink — they only see a new version after this
  publish cycle runs and they update.
- **Keeping the repo itself correct** — manifest validation, version
  discipline, and marketplace.json staying in sync with what's actually in
  `plugins/`.

## 1. Determine scope, audit, and Sanitize (mandatory gate)

First, run the check script and read its output:

```
bash .claude/skills/refresh-plugins/scripts/check.sh
```

This reports, per plugin under `plugins/`: current version, last release tag,
whether the working tree has uncommitted changes under that plugin's
directory, and whether its `plugin.json` (and the root `marketplace.json`)
pass `claude plugin validate`. A plugin with `working tree: clean` and no
diff since its last tag has nothing to publish — exclude it from scope.

If validation fails for a plugin or the marketplace manifest, stop and fix
the manifest before continuing — do not version-bump or tag a plugin that
doesn't validate.

If Sara named a specific plugin when invoking `/refresh-plugins`, scope is
that plugin alone, regardless of what else has changed. Otherwise scope is
every plugin the check script reports as changed.

Then run `/sanitize-plugins <exact plugin name(s) in scope>` — **always pass
the scope explicitly, never invoke it bare.** A bare call would trigger its
own interactive "which plugin?" prompt, which is the wrong behavior here:
this flow already knows its scope and asking again would be redundant and
would let the two scopes silently diverge. Do not proceed past this step
unless `/sanitize-plugins` returns **PASS** for every plugin in scope. If it
returns **FAIL** for any of them, stop, report exactly what's still open for
that plugin, and do not version-bump, tag, or push anything — a plugin does
not get published with unresolved secrets, personal data, cross-project
leakage, non-portable hardcoding, or personalized wording. This applies even
to a plugin that's never been published before; "first publish" is not an
exemption.

## 2. Decide the version bump, per changed plugin

Look at what actually changed (`git diff <last-tag>..HEAD -- plugins/<name>`,
or the full diff if `last tag: none`) and pick a semver bump:

- **patch** — bug fix, wording/prompt tweak, doc fix, no behavior change to
  what the plugin's skills/agents do.
- **minor** — new skill, new agent, new capability added; backward compatible.
- **major** — renamed or removed a skill/agent/command that existing
  installs depend on, or changed behavior in a way that breaks existing
  usage.

Default to patch when it's ambiguous and low-stakes; ask Sara when it's a
judgment call (new capability vs. just a refinement).

Edit `plugins/<name>/.claude-plugin/plugin.json`'s `"version"` field to the
new value.

## 3. Keep marketplace.json in sync

If this is a **new plugin folder** (not yet listed in
`.claude-plugin/marketplace.json`), add an entry to the root manifest's
`plugins` array:

```json
{
  "name": "<plugin-name>",
  "description": "<same description as the plugin's plugin.json>",
  "author": { "name": "Sara LaFleur" },
  "category": "productivity",
  "source": "./plugins/<plugin-name>"
}
```

Re-run `claude plugin validate .` after any marketplace.json edit.

Also remind Sara (don't do this automatically — it touches her live
environment): a brand-new plugin needs a live symlink for her own use —
`ln -s "$(pwd)/plugins/<plugin-name>" ~/.claude/skills/<plugin-name>` — so it
loads as `<plugin-name>@skills-dir` next session.

## 4. Commit and tag

```
git add -A
git commit -m "<plugin-name>: <one-line summary of what changed>"
claude plugin tag ./plugins/<plugin-name> -m "%s" --dry-run   # sanity check first
claude plugin tag ./plugins/<plugin-name> -m "%s"
```

`claude plugin tag` creates a `<plugin-name>--v<version>` git tag and
cross-checks that `plugin.json` and the marketplace entry agree — if they've
drifted, fix that before tagging, don't force past it.

## 5. Push

Only if a remote is configured (`git remote -v`). If none exists yet, tell
Sara this plugin is committed and tagged locally but not published anywhere
external, and ask whether to add a remote.

```
git push origin main
git push origin "<plugin-name>--v<version>"
```

## 6. Refresh installed copies

For any marketplace-install (not skills-dir) consumer of this repo,
including Sara's own local test install of `ember-toolkit`:

```
claude plugin marketplace update ember-toolkit
claude plugin update <plugin-name>@ember-toolkit    # per plugin that changed
```

`claude plugin update` requires a restart to take effect — say so rather than
implying it's live immediately.

## Notes

- Never hand-edit anything under `~/.claude/plugins/cache/...` — that's a
  generated install copy, not the source of truth. Always edit under
  `plugins/<name>/` in this repo.
- One skipped step is worse than one done manually: if `claude plugin tag`
  or `marketplace update` behaves unexpectedly, stop and report the exact
  output rather than working around it.

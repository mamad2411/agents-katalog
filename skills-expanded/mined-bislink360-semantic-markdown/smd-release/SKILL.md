---
name: smd-release
description: Branch, version, verify and publish Semantic Markdown releases (VS Code extension, npm package `semantic-markdown`, agent skills, GitHub release) without breaking existing users. Use this skill for any change destined for the public bislink360/semantic-markdown repository — starting a feature or fix branch, preparing or reviewing a pull request, bumping versions, writing the changelog, checking backward compatibility, tagging, or publishing to the VS Code Marketplace, Open VSX, npm or GitHub Releases (the tag-triggered Release workflow) — even if the user just says "ship it", "release this", "bump the version", "merge this" or "publish".
---

# Releasing Semantic Markdown

One repository ships four artifacts that must stay in lockstep:

| Artifact | Where | Version source |
|---|---|---|
| VS Code extension `bislink360.semantic-markdown` | VS Code Marketplace, Open VSX + `.vsix` on GitHub Releases | `extension/package.json` |
| npm package `semantic-markdown` (library + `smd` CLI) | npmjs.com | `npm/package.json` (same version) |
| Agent skills `semantic-markdown-reader` / `-writer` | `skills/`, zips on GitHub Releases | bundle the CLI, so they follow the same version |
| Format spec | `smd: 2` in new documents (`smd: 1` documents keep the v1 rules) | `SMD_VERSION` in `extension/src/core/spec.ts`; changes only for format-breaking releases |

Existing documents, CI pipelines (`smd validate`), library users and agents all depend on today's behaviour. **The primary goal of this process is that nothing breaks silently.** Every incompatible change is found by the checker, called out to the human, and shipped only as a major version.

## Workflow

### 1. Branching: follow the release train (version-control skill)

Branches follow the **version-control** skill's release train:

- `release/vX.Y.Z` is created from `main` and opened at its version by `plan-release.mjs`.
- Every feature or fix gets its own branch from the release branch: `feat/<slug>`, `fix/<slug>`, `docs/<slug>`, `chore/<slug>`.
- Feature PRs target the **release branch** and are squash-merged.
- After the release is tagged and published, the release branch is merged into `main` with a merge commit.

Never commit to `main` directly, and never open feature PRs against `main`.

Use Conventional Commit messages (`feat(tables): add captions`, `fix(cli): …`, `docs: …`), because they feed the changelog. Mark breaking commits with `!` and a `BREAKING CHANGE:` footer. **Do not add AI co-author trailers or "Generated with" lines to commits or PRs in this repository.** Read `references/branching.md` for the PR checklist and merge rules.

### 2. Keep every change backward compatible by default

Before designing a change, read `references/compatibility.md`. It lists what counts as breaking on each surface (syntax, validation, HTML, agent view, CLI, npm API, extension manifest, skills) and the compatible alternative for each. In short:

- **Add, don't change.** Add new blocks, directives, attributes, values, commands, flags, exports and settings. Leave old ones working.
- **Never make valid documents invalid.** New checks start as `warning`/`info`; only a major release may introduce new errors on previously valid input.
- **Deprecate before removing.** Keep an alias, emit a deprecation hint, document it, and remove it only in the next major.
- **Stable identifiers are contracts:** diagnostic codes, CLI flags and JSON output fields, `smd-*` CSS classes, agent-view tags, extension command/setting IDs, skill names.

### 3. Prove it on every PR

From the repository root:

```bash
node .claude/skills/smd-release/scripts/release-check.mjs --pr       # on feature PRs into a release branch
node .claude/skills/smd-release/scripts/release-check.mjs            # on the release branch before tagging (versions and changelog enforced)
node .claude/skills/smd-release/scripts/release-check.mjs --skip-vscode --skip-tests   # quick iteration
```

The checker builds the last release in a temporary worktree (cached) and compares it with the working tree. "The last release" is the newest `vX.Y.Z` tag, with one exception: once a version is tagged, the tree with exactly that tag's files (the tracking PR into `main`, whose CI runs again after the tag is pushed) is compared with the release before it and reported as already released, instead of failing as "not greater than the last release". A tag of the same version on a different tree still fails: the version was not bumped, or the tag is on the wrong commit.

- format vocabulary, diagnostic codes, validation results, agent view, Markdown export and emitted CSS classes on a document corpus
- CLI commands and flags, and templates
- npm exports, entry points and types
- extension commands, settings, defaults, language IDs, keybindings and snippets
- skills

It also runs the typecheck, unit tests and VS Code integration tests, checks version consistency and the changelog, and computes the **required** bump. It exits `1` if anything blocks.

Every new syntax feature must also add a document exercising it to `extension/test/compat/corpus/`, so future releases are compared against it. Create the folder if it doesn't exist yet.

### 4. Finish the release on `release/vX.Y.Z`

1. The release branch was opened at its version when the train was planned: `plan-release.mjs` runs `bump-version.mjs`, which updates `extension/package.json`, `extension/package-lock.json`, `npm/package.json`, the Obsidian plugin's `integrations/obsidian/manifest.json` and `versions.json`, the MkDocs plugin's `pyproject.toml`, the Claude Code plugin's `.claude-plugin/plugin.json` and the MCP registry entry `server.json`, and adds the CHANGELOG heading. Each feature PR added its own changelog bullets under that heading. If the version must change (e.g. a breaking change turned up and it must become a major), run:

   ```bash
   node .claude/skills/smd-release/scripts/bump-version.mjs <patch|minor|major|X.Y.Z>
   ```

   on the release branch, and rename the release branch and tracking PR to match.
2. Once every planned feature PR is merged into the release branch (or dropped from the train), complete the changelog entry. List every item from the checker's **Breaking** section under `### ⚠️ Breaking changes`, each with a migration note. Delete empty headings.
3. Update docs for any new syntax: `docs/reference/spec.md`, `docs/reference/features.md`, the matching `skills/semantic-markdown-writer/references/syntax/<topic>.md` (listed in `references/syntax.md`), and the README feature list.
4. Rebuild (`cd extension && npm run build && npm run build:npm`) and run the **full** check with no skip flags.
5. Run the **static analysis gate** (sonarqube-scan skill). GitHub CI has no static analysis, so this local SonarQube run is the only check for bugs, vulnerabilities, security hotspots and code smells. It must pass: fix blocking findings, or suppress them with a reasoned `NOSONAR`. Grow `baseline.json` only with the maintainer's approval.

   ```bash
   node .claude/skills/sonarqube-scan/scripts/sonar-scan.mjs
   ```

### 5. Stop and get human approval (mandatory)

Before tagging, show the human the checker report and a short summary:

- **Version:** `vPREV → vNEXT` (required bump / actual bump)
- **Breaking changes:** each one with who is affected and the migration path. If there are none, say so explicitly.
- **Behaviour changes** the checker flagged for review (agent-view, HTML or Markdown-export diffs, new warnings, changed defaults), with your assessment of each.
- **New features.**
- **Tests:** pass counts for unit and VS Code integration tests.
- **Static analysis:** the SonarQube gate result and metrics, plus any suppressions or baseline changes made in this release (sonarqube-scan skill, "Reporting").

Don't proceed until the human approves in chat. For a major release, get approval for each breaking change individually.

### 6. Tag the release branch; the Release workflow builds, releases and publishes

1. Tag the head of the release branch (the exact commit that ships) and push the tag. **Pushing the tag publishes**, so do it only after the human's approval in §5:

   ```bash
   git tag -a vX.Y.Z origin/release/vX.Y.Z -m "Semantic Markdown X.Y.Z" && git push origin vX.Y.Z
   ```

2. The tag starts `.github/workflows/release.yml`. Its logic lives in small tested scripts in `extension/scripts/release/`:

   | Job | What it does |
   |---|---|
   | verify | `check-versions.mjs`: the tag equals the version in `extension/package.json`, `package-lock.json`, `npm/package.json`, `integrations/mkdocs/pyproject.toml`, `integrations/obsidian/manifest.json`, `.claude-plugin/plugin.json` and `server.json` (its version and its npm package's); the CHANGELOG has a non-empty `## X.Y.Z` section; the tagged commit is on `main` or a `release/*` branch. Then typecheck and unit tests. |
   | build | `.vsix` (`npm run package`), npm `.tgz` (`npm run build:npm`, `npm pack`) skill zips (`zip -r`), the playground zip (`npm run build:playground`) the MkDocs plugin wheel and sdist (`python -m build integrations/mkdocs`) the Obsidian plugin zip (`main.js`, `manifest.json`, `styles.css` from `integrations/obsidian`) and the JetBrains plugin zip (`./gradlew buildPlugin` in `integrations/jetbrains`, with Java 21; it ships the tag's `smd.cjs`). Checks they are real zips with the LICENSE and the right version, and that `skills/*/scripts/smd.cjs` match a fresh build. Notes: `changelog-excerpt.mjs --downloads` (downloads table + the changelog section). All uploaded as the `release-assets` workflow artifact. |
   | github-release | Creates the GitHub Release with those notes and the nine assets (the `.vsix`, the `.tgz`, both skill zips, `semantic-markdown-playground.zip`, the MkDocs plugin wheel and `.tar.gz`, `semantic-markdown-obsidian-X.Y.Z.zip` and, since 2.1.0, `semantic-markdown-jetbrains-X.Y.Z.zip`). If the release already exists, it keeps its notes and attaches only missing assets. Verifies the release lists all nine. |
   | publish-marketplace, publish-openvsx, publish-npm, publish-pypi | Publish the exact `.vsix` / `.tgz` / wheel and sdist attached to the release (`vsce publish --packagePath`, `ovsx publish`, `npm publish --provenance`, `twine upload` with `PYPI_TOKEN`), then poll the registry until it lists X.Y.Z (`wait-for-version.mjs`). |
   | publish-jetbrains | Uploads the exact JetBrains plugin zip attached to the release to the JetBrains Marketplace (`upload-jetbrains.mjs`, plugin 35420, with `JETBRAINS_TOKEN`). JetBrains reviews each upload by hand, so the job doesn't wait for the listing; an upload of a version the Marketplace already has counts as done. |

   Each publish job **skips with a notice** (a green job, not a failure) on a dry run, while its secret is missing, or when the registry already lists the version (`publish-gate.mjs`). So re-running is safe: **Actions → Release → Run workflow** with the tag and **dry run** unticked finishes only what is missing, e.g. after adding a secret or when a registry was slow.
3. To rehearse, run the workflow by hand with an existing tag and **dry run** ticked (the default): it verifies, builds and checks every artifact and shows the release notes in the job summary, but creates no release and publishes nothing. A manual run uses the scripts at the tag, so it works for tags from v1.5.0 on.
4. Watch it with `gh run watch` (or `gh run list --workflow release.yml`) and read the notices of the publish jobs.

### 7. Verify each registry (the human holds the credentials)

**Never ask for, type, paste or store tokens yourself.** **Only report something as published after the registry itself shows the new version.** If a listing isn't live (its job skipped or failed), say so plainly and don't update docs to point at it.

| Where | Verify (don't trust the workflow's output alone) |
|---|---|
| GitHub release | `gh release view vX.Y.Z` lists 4 assets (`.vsix`, `.tgz`, two skill zips) |
| VS Code Marketplace | `npx vsce show bislink360.semantic-markdown` shows X.Y.Z (verification can take a few minutes) |
| Open VSX | `curl -s https://open-vsx.org/api/bislink360/semantic-markdown/X.Y.Z` returns that version |
| npm | `npm view semantic-markdown@X.Y.Z version` returns X.Y.Z |
| JetBrains Marketplace | `node extension/scripts/release/wait-for-version.mjs jetbrains X.Y.Z --attempts 1` passes once JetBrains has approved the upload (it can take a few days; until then the plugin page lists no update) |

**One-time setup, done by the maintainer.** Until a secret exists its publish job skips, and releases stay GitHub-only as before. Add each one in GitHub → **Settings → Secrets and variables → Actions → New repository secret**, or with `gh secret set NAME` (it prompts for the value, so the token never lands in shell history):

| Secret | How to create it |
|---|---|
| `VSCE_PAT` | Sign in to [dev.azure.com](https://dev.azure.com) with the account that owns the `bislink360` publisher ([marketplace.visualstudio.com/manage](https://marketplace.visualstudio.com/manage)) → User settings → Personal access tokens → New token: Organization **All accessible organizations**, scope **Marketplace → Manage**, an expiry you track. |
| `OVSX_PAT` | Sign in to [open-vsx.org](https://open-vsx.org) with GitHub, link an Eclipse account and sign the Publisher Agreement (profile page), then Settings → Access Tokens → Generate. Create the `bislink360` namespace once from your own shell: `npx ovsx create-namespace bislink360` (reads the token from `OVSX_PAT`). Optionally claim the namespace (EclipseFdn/open-vsx.org issue) for the verified badge. |
| `NPM_TOKEN` | On [npmjs.com](https://www.npmjs.com), as the account that will own `semantic-markdown` (with 2FA) → Access Tokens → Generate New Token → **Granular**: read and write, packages `semantic-markdown` (the very first publish needs "all packages" until the package exists; narrow it afterwards), bypass 2FA for automation, an expiry you track. |
| `PYPI_TOKEN` | On [pypi.org](https://pypi.org), as the account that will own `mkdocs-semantic-markdown` (with 2FA) → Account settings → API tokens → Add API token (the very first upload needs an account-wide token until the project exists; replace it with a token scoped to `mkdocs-semantic-markdown` afterwards). |
| `JETBRAINS_TOKEN` | On [plugins.jetbrains.com](https://plugins.jetbrains.com), signed in with the JetBrains account that develops plugin 35420 → profile → **My Tokens** → Generate Token (permanent tokens; revoke and replace it if it leaks). The first version was uploaded by hand; the job uploads every release after that. |

The publish jobs run in the `release` GitHub environment (created on first use). Add required reviewers to it to approve every publish, and store the secrets as environment secrets there if you want them scoped to publishing. An expired token fails its job: update the secret and re-run the workflow for the tag.

**Manual fallback** (the workflow is unavailable). Build from the tag in a separate worktree: `npm run package` (→ `.vsix`), `npm run build:npm` then `npm pack` in `npm/` (→ `.tgz`), skill zips from `skills/`, and `semantic-markdown-playground.zip` from `npm run build:playground` (zip the `playground` folder in `extension/dist/`) — on Windows with `C:\Windows\System32\tar.exe -a -c -f <name>.zip <folder>` (Git Bash's `tar` writes a tar file named `.zip`; check with `file *.zip`), elsewhere with `zip -r`. Notes: `node extension/scripts/release/changelog-excerpt.mjs X.Y.Z --downloads -o notes.md`. Publish in this order, only with credentials already present on the machine (`npx vsce ls-publishers` lists `bislink360`, `npm whoami` succeeds); otherwise stop and give the human the exact command:

| Step | Command |
|---|---|
| GitHub release | `gh release create vX.Y.Z --verify-tag --title "Semantic Markdown X.Y.Z" --notes-file notes.md <vsix> <tgz> <skill zips>` |
| VS Code Marketplace | `cd extension && npx vsce publish --packagePath semantic-markdown-X.Y.Z.vsix` |
| Open VSX | `npx ovsx publish semantic-markdown-X.Y.Z.vsix` (token from `OVSX_PAT`) |
| npm | `cd npm && npm publish` |

Then verify each one as in the table above.

### 8. After publishing

- **Merge the release branch into `main`:** merge the tracking PR `release/vX.Y.Z → main` with a **merge commit** (never squash), so the tagged commit is in `main`'s history. Then delete the release and feature branches, and merge `main` into any other open release branch (version-control skill §5).
- Confirm the README badges and install instructions resolve. Push doc changes that point at the new version only after all registries show it.
- If a release is bad, don't unpublish. Ship a patch train from the tag (`plan-release.mjs X.Y.Z+1 fix/<slug> --base vX.Y.Z`). For npm, `npm deprecate semantic-markdown@X.Y.Z "<reason>"` warns installers.

## References

- `references/compatibility.md` — the breaking-change catalogue per surface, and the compatible alternatives. Read it before designing any change.
- `references/versioning.md` — semver rules for this repository, spec-version policy and deprecation timeline.
- `references/branching.md` — branch naming, commit conventions, PR checklist, merge and tag rules.
- **sonarqube-scan** skill — the local SonarQube static-analysis gate required before every release.

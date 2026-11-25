---
name: trusted-publish
description: Publish a package from a git repo to its registry via OIDC Trusted Publishing — no long-lived tokens. Writes the GitHub Actions publish workflow, walks the user through the registry-side trust entry, releases, and verifies. Use when the user wants to publish or release a package to PyPI, npm, crates.io, or another registry, or to set up tokenless/automated publishing from CI. Optional argument: repo path (default is the current directory).
---

# trusted-publish

Every registry here is **push-model**: the registry never pulls or builds — a GitHub Actions workflow builds and uploads. **Trusted publishing** makes that upload tokenless: the workflow proves its identity over OIDC and the registry mints a short-lived, auto-expiring upload token. Setup is therefore three artifacts: a workflow in the repo, a trust entry on the registry, and a release to trigger the run.

The trust entry binds four **identity fields** — owner, repository, workflow filename, environment. The workflow file *is* the credential: these values must match the registry config character-for-character. This skill fixes them — workflow `.github/workflows/publish-<registry>.yml`, environment named after the registry — so every run produces the same names and the user types the same values.

## Steps

1. **Resolve the repo.** The argument, when given, is the repo path; otherwise use the current directory. Record `owner/repo` from `git remote get-url origin`. Done when the path is a git repo with a github.com origin. A GitLab origin narrows provider support — check the reference file's provider line before continuing; any other host means trusted publishing is unavailable: report that and stop.

2. **Detect every ecosystem.** Walk the repo for package manifests and map each to its registry:

   | Manifest | Registry | Reference |
   |---|---|---|
   | `pyproject.toml` / `setup.py` | PyPI | [references/pypi.md](references/pypi.md) |
   | `package.json` without `"private": true` | npm | [references/npm.md](references/npm.md) |
   | `Cargo.toml` with a `[package]` section and `publish` not disabled | crates.io | [references/crates-io.md](references/crates-io.md) |
   | `*.gemspec`, `*.nuspec`, anything else | varies | [references/other-registries.md](references/other-registries.md) |

   Done when every manifest in the repo is either mapped to a registry or reported to the user as out of scope. Several matches (a monorepo) → run steps 3–6 once per registry.

3. **Write the publish workflow.** Read the registry's reference file, then write `.github/workflows/publish-<registry>.yml` from its template, substituting the package name and build specifics. When a publish workflow already exists, reconcile it with the template — `id-token: write` on the publish job only, current action versions — and carry *its* filename into step 4. Commit and push. Done when the workflow file is on the default branch.

4. **Configure trust on the registry** — a logged-in web step only the user can perform. Hand them the reference file's config URL and the four identity-field values exactly as they appear in the workflow just written, then wait for their confirmation. First-ever publish branches per registry — PyPI pre-registers a *pending publisher* and stays fully tokenless; npm and crates.io need one manual first release — the reference file carries that branch. Done when the user confirms the trust entry is saved.

5. **Release.** Set the new version in the manifest, commit, push, then `gh release create v<version> --generate-notes`. Watch with `gh run watch`. Done when the run is green. An OIDC-exchange failure (`invalid-publisher`, 403 on token exchange) means an identity-field mismatch — re-verify step 4's four values against the workflow file, have the user correct the trust entry, and re-run the workflow.

6. **Verify on the registry.** *Published* means fetchable: poll the reference file's version endpoint until the new version appears — allow a minute of index lag — then report the package URL to the user. Done when the registry's own API returns the new version; that, with the package URL in hand, closes the skill.

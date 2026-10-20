---
name: publish-package-registry
description: Publishes a library to a package registry (npm/PyPI/crates) safely — semver decision, correct artifacts (dual ESM/CJS + types, files allowlist), provenance/signing via OIDC, a pre-publish gate, scoped least-privilege access, and tag-triggered CI release.
when_to_use: Shipping or fixing a library release to npm/PyPI/crates — oversized/broken publish, missing types on install, error-prone manual releases. NOT deploying a running app/service (deploy-release), writing changelog text (release-notes), or auditing consumed dependencies (supply-chain-sbom-provenance — this PRODUCES and attests your OWN package).
---

## When to Use

Reach for this skill when you are **publishing a library others install**, not deploying a service:

- "Publish v2 to npm" / "release this crate" / "push the wheel to PyPI"
- "Consumers get `Could not find a declaration file` — types are missing on install"
- "Our tarball is 40 MB / shipped `src/` and tests / leaked a `.env`"
- "Replace our manual `npm publish` with a tag-triggered CI release"
- "Add provenance / sign the artifact so installs are verifiable"
- "Ship a prerelease on a `next` dist-tag without moving `latest`"

NOT this skill:
- Deploying a running app/service/container to an environment → deploy-release
- Writing the human-readable changelog / release-notes text → release-notes
- Auditing/attesting dependencies you *consume* (SBOM of third-party deps) → supply-chain-sbom-provenance (this skill produces+attests the package you *own*)
- Authoring the bundler/`tsup`/Rollup config that emits the artifacts → configure-bundler-build
- Wiring versioning across many packages in one repo → setup-monorepo-tooling

## Steps

1. **Run the pre-publish gate — never publish off an unverified working tree.** A publish is irreversible (you can't re-publish the same version; npm unpublish is restricted to 72h). Gate, in order, and abort on the first failure:

   ```bash
   git status --porcelain        # MUST be empty — publish only committed, tagged code
   <build>                       # tsup/rollup/maturin/cargo build — emit dist/ fresh
   <test> && <typecheck>         # vitest/pytest + tsc --noEmit; green or stop
   npm pack --dry-run            # npm: list the EXACT files + unpacked size
   ```

   For Python: `python -m build && twine check dist/*`. For crates: `cargo publish --dry-run` and `cargo package --list`. Read the file list out loud — if it contains `src/`, tests, `.env`, `*.map` you didn't intend, or the size jumped, fix the allowlist (step 4) before going further.

2. **Decide the semver bump from the diff, not vibes.** Compare the public API surface, not the commit count.

   | Change | Bump | Example |
   |---|---|---|
   | Removed/renamed export, changed signature, dropped Node/Py version, behavior break | **major** | `0.x` exception: any break is allowed, but prefer minor and document it |
   | New export, new optional param, new overload — old code still compiles | **minor** | added `parse(opts?)` |
   | Bugfix, perf, types-only fix, docs, internal refactor — public API identical | **patch** | fixed off-by-one |

   Pre-1.0 (`0.y.z`): treat `0.y` like major (breaking bumps `y`), `0.y.z` like minor/patch. Don't hand-bump if you use Changesets/release-please (step 6) — let the tool compute it from change intents. Never reuse or downgrade a published version.

3. **Make the package importable both ways with types — this is the #1 broken-install cause.** Ship dual ESM+CJS plus a `.d.ts`, and wire `exports` so resolvers actually find them:

   ```jsonc
   {
     "name": "@scope/lib",
     "version": "2.0.0",
     "type": "module",
     "exports": {
       ".": {
         "types": "./dist/index.d.ts",   // types FIRST — resolution is order-sensitive
         "import": "./dist/index.mjs",
         "require": "./dist/index.cjs"
       },
       "./package.json": "./package.json"
     },
     "main": "./dist/index.cjs",          // fallback for old resolvers
     "module": "./dist/index.mjs",
     "types": "./dist/index.d.ts",
     "files": ["dist"],                   // allowlist — ONLY dist ships
     "sideEffects": false,                // lets bundlers tree-shake consumers
     "repository": { "type": "git", "url": "git+https://github.com/org/lib.git" },
     "license": "MIT",
     "engines": { "node": ">=18" }
   }
   ```

   Validate the resolution with `attw --pack` (`@arethetypeswrong/cli`) and `publint` — they catch missing `types` condition, ESM/CJS mismatch, and bad `exports` before users do. Python equivalent: `pyproject.toml` with `[project]` (name, version, license, `requires-python`, `urls`), `py.typed` shipped in the package, and SPDX `license` string. Crates: `Cargo.toml` `[package]` with `description`, `license`, `repository`, `readme`, and an `include = [...]` list.

4. **Control exactly what ships with an allowlist, not a denylist.** Prefer `files` in `package.json` (allowlist) over `.npmignore` (denylist) — a forgotten denylist entry leaks files; an allowlist fails safe. Note `package.json`, `README`, `LICENSE`, and the `main`/`types` targets are always included. Re-run `npm pack --dry-run` after editing and confirm the count dropped. crates: `include`/`exclude` in `Cargo.toml`. Python: `MANIFEST.in` + `tool.setuptools.packages.find` / hatch `[tool.hatch.build.targets.wheel]`.

5. **Authenticate with a short-lived, least-privilege credential — never a personal long-lived token in CI.** Order of preference:
   - **OIDC / trusted publishing (best, no stored secret):** npm provenance + GitHub OIDC, PyPI "Trusted Publisher", crates.io GitHub OIDC. The registry trusts the CI identity directly; nothing to leak or rotate.
   - **Automation/CI token (next best):** npm *Automation* token (granular, bypasses 2FA prompt in CI), PyPI *project-scoped* API token, crates `CARGO_REGISTRY_TOKEN`. Store in CI secrets, scope to the single package, never to your account.
   - Enforce **2FA = auth-and-publish** on the package for any human-initiated publish. First publish of a *public* scoped package needs `--access public` (scoped defaults to restricted and will 402/403 otherwise).

6. **Automate the release on a tag — kill the manual `npm publish`.** Manual publishes drift (wrong branch, dirty tree, forgotten build). Use Changesets (or release-please/semantic-release) so the bump+changelog+tag is mechanical, and let CI do the publish with provenance:

   ```yaml
   # .github/workflows/release.yml
   permissions:
     contents: write
     id-token: write            # REQUIRED for npm --provenance / PyPI trusted publishing
   jobs:
     release:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-node@v4
           with: { node-version: 20, registry-url: 'https://registry.npmjs.org' }
         - run: npm ci && npm run build && npm test
         - run: npm publish --provenance --access public --tag latest
           env: { NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }} }
   ```

   `--provenance` (with `id-token: write`) cryptographically links the published tarball to the source commit + workflow — visible as a verified badge on npm. PyPI/crates get equivalent attestation via sigstore/cosign keyless signing in the same OIDC flow. Use **dist-tags** deliberately: prereleases → `--tag next` (or `beta`), so `npm install pkg` (which resolves `latest`) never silently jumps to an unstable build. Promote later with `npm dist-tag add pkg@x.y.z latest`.

7. **Verify the real artifact in a clean environment** (see Verify) — building locally proves nothing about what consumers actually receive.

## Common Errors

- **Publishing a dirty/untagged tree.** The tarball includes uncommitted changes that no commit reproduces. Gate on `git status --porcelain` empty + a matching tag before publish.
- **Missing `types` on install.** No `"types"` condition in `exports` (or it's listed *after* `import`/`require`) → consumers get `any`/`Could not find a declaration file`. Put `types` first in each `exports` entry; verify with `attw --pack`.
- **ESM/CJS half-shipped.** Only `.mjs` exists but `require` points at it (or vice versa) → `ERR_REQUIRE_ESM` / `Cannot use import`. Emit both, wire both conditions; `publint` flags the mismatch.
- **Denylist leak.** `.npmignore` forgot `test/` or a fixture with secrets → it ships. Switch to a `files` allowlist; re-check `npm pack --dry-run`.
- **Oversized tarball.** Shipping `src/`, sourcemaps, `node_modules`, or `.map` blows up install size. Allowlist `dist` only; confirm unpacked size in the pack dry-run.
- **First public scoped publish fails with 402/403.** Scoped packages default to restricted. Add `--access public` on the first publish.
- **`id-token: write` missing → provenance silently absent or publish errors.** Provenance and trusted publishing both need that permission on the job; without it `--provenance` fails or no attestation is produced.
- **Prerelease moved `latest`.** Publishing `2.0.0-beta.1` without `--tag` makes it `latest`, so every fresh install gets the beta. Always tag prereleases `next`/`beta`.
- **Long-lived personal token in CI.** A leaked account-scoped token can publish *any* of your packages. Use OIDC trusted publishing, or a package-scoped automation token at minimum.
- **Reusing/forcing a version.** The registry rejects a duplicate version, and unpublish windows are tiny. Bump forward — there is no "fix the same version" path.
- **`sideEffects` unset on a side-effect-free lib.** Consumers can't tree-shake your exports; bundle size leaks downstream. Set `"sideEffects": false` (or list the few files that do have side effects).

## Verify

1. **Pack and inspect:** `npm pack` (or `python -m build` / `cargo package`) and list the tarball contents — it contains *only* the allowlisted build output, expected size, no `src`/tests/secrets/maps.
2. **Type/contract lint:** `attw --pack` and `publint` report zero errors (npm); `twine check dist/*` passes (PyPI). No missing/mis-ordered `exports` conditions.
3. **Clean-room install from the tarball:** in an empty temp dir, `npm init -y && npm i ../lib-2.0.0.tgz` (or `pip install dist/lib-2.0.0-*.whl` in a fresh venv). Install must succeed with no peer/engine warnings you didn't intend.
4. **Import both module systems with types:** in that clean project, `node -e "import('lib').then(m=>console.log(m.default))"` AND `node -e "require('lib')"` both resolve; a `.ts` file importing `lib` typechecks under `tsc` with no `any`. Python: `import lib` in the fresh venv and `mypy` sees the shipped `py.typed`.
5. **Semver matches the diff:** the chosen bump (step 2) is justified by the actual public-API delta, and the new version is strictly greater than the latest published one (`npm view pkg version`).
6. **Provenance/signature present:** after a CI publish, the npm page shows the verified provenance badge (or `cosign verify`/sigstore attestation validates for PyPI/crates), tracing the artifact to the source commit + workflow run.
7. **Dist-tag correct:** `npm dist-tag ls pkg` shows the prerelease on `next`/`beta` and `latest` still points at the last stable — a default `npm i pkg` does not pull the prerelease.

Done = the gate is green on a clean tagged tree, the packed tarball installs and imports both ESM and CJS with working types in a clean room, the semver bump matches the API diff, and CI published it on the correct dist-tag with verifiable provenance.

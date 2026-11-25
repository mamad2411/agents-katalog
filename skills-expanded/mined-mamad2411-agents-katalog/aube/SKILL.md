---
name: aube
description: "Reference for aube, the Node.js package manager: installing and managing dependencies, running package.json scripts with aubr, lockfile handling, workspaces and catalogs, dependency build approval, security settings, and Node runtime pinning. Use when adding or updating npm dependencies, editing aube-workspace.yaml, running or wiring up package scripts in an aube project, setting up CI installs, or debugging install, script, or Node version problems."
---

# aube

aube is a Node.js package manager. It builds a pnpm-style isolated
`node_modules` from a global content-addressed store, keeps whatever
lockfile format a project already has, and skips dependency build scripts
until they are explicitly approved.

## Everyday commands

```sh
aubr build              # run a package.json script (short for: aube run)
aube test               # install if stale, then run the test script
aube exec vitest        # run a binary from node_modules/.bin
aubx cowsay hi          # one-off tool in a throwaway env (short for: aube dlx)
aube add lodash         # add a dependency; -D dev, -O optional, -E exact
aube remove lodash
aube update             # within manifest ranges
aube update --latest    # past the ranges; rewrites the manifest specifiers
aube outdated
aube why <package>      # which dependents pull a package in
```

`aubr`, `aube test`, and `aube exec` check install freshness first: if
`package.json` or the lockfile changed since the last install, aube
installs before running. Day-to-day work therefore needs no separate
install step — run the script you wanted. `--no-install` skips the check;
`--if-present` tolerates a missing script.

`aube add` also takes aliases (`name@npm:real@^1`), JSR packages
(`jsr:@std/collections`), `workspace:*`, `file:`/`link:` paths, git URLs,
and tarball URLs.

### Install modes

`aube install` is for when the install itself is the task — first setup,
lockfile updates, Docker layers, CI:

| Command | Use when |
| --- | --- |
| `aube install` | Local default: reuse a fresh lockfile, re-resolve on drift |
| `aube install --frozen-lockfile` | Fail if manifest and lockfile disagree |
| `aube ci` | Strict CI shortcut: delete `node_modules`, frozen install |
| `aube install --prod` | Skip `devDependencies` |
| `aube install --offline` | Forbid network; `--prefer-offline` allows misses |
| `aube install --lockfile-only` | Update the lockfile without touching `node_modules` |

`aube dedupe` re-resolves the lockfile to collapse duplicate versions
(`--check` exits non-zero if it would change anything); `aube prune`
removes extraneous packages from `node_modules` without touching the
manifest or lockfile.

## Lockfiles

aube reads and writes `aube-lock.yaml`, `pnpm-lock.yaml` v9,
`package-lock.json`, `npm-shrinkwrap.json`, `yarn.lock`, and `bun.lock`.
It updates the file the project already has — write precedence when
several exist: `aube-lock.yaml` → `pnpm-lock.yaml` → `bun.lock` →
`yarn.lock` → `npm-shrinkwrap.json` → `package-lock.json`. A project with
no lockfile gets `aube-lock.yaml`. `aube import` converts a project to
`aube-lock.yaml`; adopting aube does not require it.

## Configuration

Settings live in four places, and `aube config set` routes writes so
npm/pnpm/yarn never see keys they would warn about:

- `.npmrc` — the npm-shared surface only: registries, scoped registries,
  per-host auth tokens, proxy/TLS.
- `aube-workspace.yaml` — project settings, workspace globs, catalogs,
  and the build-approval map. An existing `pnpm-workspace.yaml` is read
  and mutated in place instead.
- `~/.config/aube/config.toml` — user scope, written by `aube config set`;
  `--local` writes the project-scope equivalents.
- `package.json` — every `pnpm.*` config key is also accepted as `aube.*`
  (`overrides`, `catalog`, `allowBuilds`, `patchedDependencies`,
  `peerDependencyRules`, ...); `aube.*` wins on conflict.

Environment variables use the `AUBE_` prefix (`AUBE_NODE_LINKER=hoisted`),
with pnpm-compatible `NPM_CONFIG_*` aliases; CLI flags win over
everything. `aube config list --json` shows the merged result. Map
settings accept dotted writes for one entry at a time:

```sh
aube config set --local overrides.lodash 4.17.21
aube config set --local allowBuilds.esbuild true
```

Defaults worth knowing:

| Setting | Default | Effect |
| --- | --- | --- |
| `nodeLinker` | `isolated` | pnpm-style symlink tree under `node_modules/.aube/`; `hoisted` gives a flat npm-style tree |
| `minimumReleaseAge` | `1440` | Versions published in the last 24 h are not installed |
| `blockExoticSubdeps` | `true` | Transitive git/tarball dependencies are rejected |
| dependency builds | approval required | Install scripts in dependencies stay skipped until allowlisted |

## Workspaces

`aube-workspace.yaml` declares the packages; `workspace:*` /
`workspace:^` in `package.json` links them locally and converts to
concrete versions on publish and deploy:

```yaml
packages:
  - "packages/*"
  - "apps/*"
```

`-F` filters and `-r` recursive runs target subsets:

```sh
aube -r run build            # every workspace package
aube -F '@acme/*' test       # glob over package names
aube -F './apps/web' install # by path
aube -F 'api...' run build   # api and everything it depends on
aube -F '...web' run test    # web and everything depending on it
aube -F '[origin/main]' test # packages changed since a git ref
aube -F '!legacy' -r run lint  # exclusion
```

Catalogs centralize version ranges in `aube-workspace.yaml`; packages
reference them with `catalog:` / `catalog:<name>` specifiers:

```yaml
catalog:
  react: ^19.0.0
catalogs:
  test:
    vitest: ^3.0.0
```

## Dependency build scripts

Dependencies cannot run `preinstall`/`install`/`postinstall` until
allowlisted (the project's own root scripts run normally; a built-in
snapshot of pnpm's trusted-dependencies list pre-approves common
packages). When an install skips an unreviewed build, it records the
package as `false` in the `allowBuilds` map of the workspace yaml:

```yaml
allowBuilds:
  esbuild: true
  sharp: true
  untrusted-package: false
```

```sh
aube ignored-builds     # what was skipped and why
aube approve-builds     # review interactively, flip entries to true
aube rebuild            # rerun builds after approving
```

Entry keys take a bare name (all versions), an exact pin
(`esbuild@0.19.0`), or a name wildcard (`@babel/*`); deny always wins
over allow. Semver ranges and wildcard+pin combinations are rejected —
an approval asserts a specific audited build.

`jailBuilds: true` adds a sandbox around approved builds: scrubbed
environment, temporary `HOME`, and on macOS/Linux a native jail denying
network and restricting writes to the package directory.
`jailBuildPermissions` grants narrow exceptions per package glob (`env`,
`write`, `network`); `jailBuildExclusions` exempts packages that cannot
run jailed yet.

## Supply-chain protections

- `minimumReleaseAge` (default 24 h) quarantines fresh releases;
  `minimumReleaseAgeStrict = true` fails instead of falling back when no
  version is old enough; `minimumReleaseAgeExclude` lists trusted
  packages.
- `aube add` checks the OSV database for known-malicious packages and
  challenges typosquats: names similar to popular packages, weekly
  downloads under `lowDownloadThreshold`, and names registered less than
  `minimumPackageAge` ago. `allowedUnpopularPackages` globs exempt
  internal names; private and workspace packages skip these gates.
- `trustPolicy = no-downgrade` rejects a version whose publish trust
  evidence (staged publish, trusted publisher, Sigstore provenance) is
  weaker than earlier releases of the same package.
- `paranoid: true` bundles the strict variants of all of the above plus
  jailed builds.
- `aube audit` lists known CVEs (`--audit-level high`, `--fix`,
  `--json`); run it in CI so advisories fail the build.

## Node runtime

aube switches Node per project: every command that spawns node —
`aubr`, `aube exec`, `aubx`, lifecycle scripts — runs on the pinned
version. Pin sources, highest precedence first: `devEngines.runtime` in
`package.json`, then `.node-version`, then `.nvmrc`, searched upward
from the project directory.

```sh
aube runtime set node lts   # resolves, writes devEngines.runtime,
aube runtime list           # installs, and records it in the lockfile
```

Resolution stops at the first satisfying hit: the `node` already on
PATH, then installed versions from mise and aube's own runtime
directory, then download. The `runtimeInstaller` setting picks who
downloads: `auto` delegates to `mise install node@<version>` when mise
is on PATH and self-downloads otherwise; `mise` and `aube` force one
side. `devEngines.runtime.onFail` (`download`, `error`, `warn`,
`ignore`) governs what happens when nothing satisfies the pin;
`runtimeOnFail = "error"` forbids runtime downloads in air-gapped CI.

The same machinery pins aube itself via
`{ "packageManager": "aube@<version>" }` or
`devEngines.packageManager` (which accepts ranges): a non-matching aube
locates the pinned version and re-execs. Set
`managePackageManagerVersions = false` for validation-only behavior.

`aube activate fish | source` (also `bash`/`zsh`) installs shims so bare
`node`, `npm`, `pnpm`, and `yarn` route through aube; unnecessary when a
toolchain manager already puts the right node on PATH.

## mise in an aube project

aube's installation guide defines the split: mise installs aube
globally, and the Node version pin lives in the project's Node-native
sources rather than in a `[tools]` entry.

```sh
mise use -g aube
mise settings add idiomatic_version_file_enable_tools node
```

- aube comes from mise's global config, and mise manages its upgrades.
  A project that needs a specific aube pins it in `package.json`
  (`"packageManager": "aube@1.18.2"`, or `devEngines.packageManager`
  for ranges); a non-matching aube locates the pinned version — reusing
  mise installs — and re-execs.
- node is pinned with `aube runtime set node <version>` (which writes
  `devEngines.runtime` and records the resolved release in the
  lockfile) or an existing `.nvmrc` / `.node-version`. The
  idiomatic-version-files setting makes mise read those same sources,
  so mise's PATH and `mise ls --current node` agree with what aube
  resolves. When the version is missing, aube's default
  `runtimeInstaller = auto` delegates the download to
  `mise install node@<version>`, keeping a single node store on disk.

Scripts stay in `package.json` and run directly through `aubr <script>`
/ `aube test` — the freshness check makes wrapper tasks and explicit
install steps unnecessary. Reserve mise tasks for repository chores
that are not package scripts.

In CI, `jdx/aube-action` installs the matching aube binary and, with
`node-version: "auto"`, resolves node through mise from the same pin
sources — no separate `actions/setup-node` step:

```yaml
- uses: jdx/aube-action@f82ca2f6c943dbde1904945d9f0ee1a0faf8e945 # v1.0.0
  with:
    node-version: auto
- run: aube ci
```

aube detects CI, runs frozen installs there, and disables its global
virtual store automatically.

## Diagnostics

- `aube doctor` — node version, source, provenance, and pin report
- `aube check` — validate project configuration
- `aube config list --json` — the merged configuration and its sources
- `aube runtime list` — resolved runtime versions and where they came from
- `aube why <package>` — the dependency chains pulling a package in
- `aube ignored-builds` — dependency builds that were skipped
- `aube licenses` / `aube sbom` — dependency license and inventory reports
- A stale install misbehaving — `aube install --fix-lockfile` repairs
  drifted entries; `aube ci` rebuilds `node_modules` from scratch
- Store trouble — `aube store path` locates it, `aube store prune` drops
  unreferenced files

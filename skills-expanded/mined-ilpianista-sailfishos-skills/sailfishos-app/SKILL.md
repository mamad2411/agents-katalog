---
name: sailfishos-app
description: >
  Expert assistant for SailfishOS application development. Use this skill whenever the user
  mentions SailfishOS, Sailfish OS, Jolla, sfdk, Sailfish SDK, Silica, harbour-*, RPM spec
  for Sailfish, or any SailfishOS-specific concepts (covers, pulley menus, Ambience, Sailjail,
  SailfishApp, Chum, OBS, GitHub Actions CI). Handles the full development lifecycle:
  bootstrapping new projects, scaffolding QML/C++ features, building and deploying with sfdk,
  CI/CD with GitHub Actions, publishing via OBS and Chum, Sailjail permission debugging,
  Harbour validation, coding conventions, and ready-to-paste code snippets. Trigger even for
  adjacent questions like "how do I add a settings page to my Sailfish app", "how do I publish
  to Chum", "why is my app blocked by Sailjail", or "how do I set up GitHub Actions for SFOS".
compatibility: bash_tool or terminal access required for build/deploy; file creation tools for scaffolding
---

# SailfishOS App Development Skill

This skill makes you an expert SailfishOS developer assistant. Use it to scaffold projects,
generate idiomatic QML/C++ code, run builds, set up CI/CD pipelines, publish to OBS/Chum,
and give precise platform guidance.

## Decision tree

| User wants to… | Action |
|---|---|
| Create a new app | [Scaffold project](#scaffolding-a-new-project) |
| Add a page / feature | [Add feature](#adding-features) |
| Build / clean / deploy | [Build & deploy](#building-and-deploying) |
| Set up GitHub Actions CI | [GitHub Actions CI](#github-actions-ci) |
| Publish via OBS | [OBS (Open Build Service)](#obs-open-build-service) |
| Submit to Chum store | [Chum submission](#chum-submission-via-obs) |
| Add Chum metadata to spec | [Add Chum metadata](#adding-chum-metadata) |
| Debug Sailjail permissions | [Sailjail debugging](#debugging-sailjail-permissions) |
| Add backup support to app | [X-HarbourBackup](#x-harbourbackup-backup-integration) |
| Ask about coding conventions | Load `references/guidelines.md` → Coding Conventions |
| Ask about UI patterns, APIs, permissions | Load `references/guidelines.md` |
| See code for a common pattern | Load `references/snippets.md` |
| Get advice on pitfalls / anti-patterns | Load `references/guidelines.md` (Pitfalls section) |
| Check Harbour allowed APIs | Load `references/guidelines.md` → Harbour Allowed APIs |

Load a reference file only when you need it — don't preload all of them.

---

## Scaffolding a new project

Before writing any files, confirm the essentials with the user if not already clear:
- `name` — must start with `harbour-` (auto-prefix if omitted)
- `displayName` — human-readable title
- `description` — one sentence
- `outputDir` — where to create it
- `template` — `cmake` (default, recommended), `qmake`, or `qmlOnly`
- `organization` — reverse-domain prefix, e.g. `org.example`
- `openSource` — include Chum metadata block? (default true)

Read `references/templates.md` for the exact file contents to generate.

**Project layout to create** (substitute `APPNAME` = the full `harbour-*` name):

```
APPNAME/
├── CMakeLists.txt          (cmake) or APPNAME.pro (qmake/qmlOnly)
├── src/main.cpp            (cmake and qmake only)
├── rpm/
│   ├── APPNAME.spec
│   ├── APPNAME.changes.in
│   └── APPNAME.changes.run.in
├── qml/
│   ├── APPNAME.qml
│   ├── pages/
│   │   ├── FirstPage.qml
│   │   └── SecondPage.qml
│   └── cover/
│       └── CoverPage.qml
├── icons/
│   ├── 86x86/APPNAME.png   (stub — remind user to replace)
│   ├── 108x108/APPNAME.png
│   ├── 128x128/APPNAME.png
│   └── 172x172/APPNAME.png
├── translations/APPNAME.ts
├── APPNAME.desktop
├── .github/
│   └── workflows/
│       └── build.yml       (see GitHub Actions CI section)
├── .gitignore
├── .gitattributes
└── README.md
```

After creating all files, point the user to **Building and deploying** below for the
target, build, and deploy commands (or print those commands from that section).

---

## Adding features

Read `references/snippets.md` for the feature boilerplate and wiring notes. Use
`references/templates.md` only when scaffolding a new project.

| Feature type | Snippet | Files created |
|---|---|---|
| `page` | `page-with-pulley` | `qml/pages/NAMEPage.qml` |
| `cover-page` | `cover-page` | `qml/cover/CoverPage.qml` (replaces existing) |
| `settings-page` | `settings-page` | `qml/pages/NAMESettingsPage.qml` |
| `dbus-interface` | `dbus-interface` / `dbus-adaptor` | `qml/dbus/NAMEInterface.qml` |
| `background-service` | `background-service` + `systemd-user-service` | `rpm/APPNAME-daemon.service` + `src/daemon/NAMEService.cpp` skeleton |
| `c++-backend` | `c++-backend` | `src/NAME.h` + `src/NAME.cpp` |

After creating files, always explain how to wire the new file into the app (e.g. how to push the new page, how to register the C++ type in `main.cpp`).

---

## Building and deploying

Run these commands via bash. Always search for `sfdk` in PATH and common install paths if not found.

**Common sfdk locations:**
- `sfdk` (in PATH)
- `~/SailfishOS/bin/sfdk`
- `/opt/SailfishOS/bin/sfdk`

### Build
```bash
# Set target (only needed once per project)
sfdk config --push target SailfishOS-latest-armv7hl

# Configure + build + package
sfdk cmake -B build -S .
sfdk cmake --build build
sfdk cmake --build build -- -j$(nproc)      # compile with all cores
sfdk rpm                                    # package → RPMS/
sfdk rpm -- --without docs                  # pass extra rpmbuild flags
```

qmake projects:
```bash
sfdk qmake
sfdk make
sfdk make clean
sfdk rpm
```

`SailfishOS-latest-<arch>` always points at the latest non-EA target installed in the SDK;
run `sfdk tools list -a` to see everything available. Use `-armv7hl` for 32-bit devices,
`-aarch64` for 64-bit devices, and `-i486` for the emulator. At the time of writing the
current release is Sailfish OS 5.2.0.22, i.e. `SailfishOS-5.2.0.22-<arch>` if you need a
pinned target.

### Clean
```bash
sfdk cmake --build build --target clean
```

### Deploy and run
```bash
sfdk device list                        # see available devices
sfdk config device "Xperia 10 III"      # set active device
sfdk deploy --sdk                       # install RPM on device via SDK
sfdk deploy --rsync                     # fast incremental deploy (no RPM rebuild)
sfdk run harbour-myapp                  # run on device, stream output
sfdk run -- harbour-myapp --some-arg    # run with arguments
sfdk debug harbour-myapp                # attach GDB to app on device
```

If `sfdk` is not found, tell the user to install the Sailfish SDK:
https://docs.sailfishos.org/Tools/Sailfish_SDK/Installation/

---

## GitHub Actions CI

Use the **coderus/github-sfos-build** action to build RPMs in CI without a local SDK.
Builds run inside Docker containers from `coderus/sailfishos-platform-sdk`.
For Sailfish OS 5.0 and newer, use the `sfos5` branch of the action.

The action takes two inputs: `release` is the **Docker image tag** (OS version only,
e.g. `5.2.0.15`) and `arch` is the architecture. It internally builds the target
`SailfishOS-<release>-<arch>`.

Available image tags: https://hub.docker.com/r/coderus/sailfishos-platform-sdk/tags

### Minimal `.github/workflows/build.yml`

```yaml
name: Build SailfishOS RPM

on:
  push:
    branches: [master, main]
  pull_request:
  release:
    types: [created]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        include:
          - release: "5.2.0.15"
            arch: armv7hl
          - release: "5.2.0.15"
            arch: aarch64

    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive   # important if you use git submodules

      - name: Build RPM
        uses: coderus/github-sfos-build@sfos5
        with:
          release: ${{ matrix.release }}
          arch: ${{ matrix.arch }}

      - name: Upload RPM artifact
        uses: actions/upload-artifact@v4
        with:
          name: rpm-${{ matrix.release }}-${{ matrix.arch }}
          path: RPMS/*.rpm
```

### Release workflow — attach RPMs to a GitHub Release

```yaml
name: Release SailfishOS RPM

on:
  push:
    tags: ['v*']

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        include:
          - release: "5.2.0.15"
            arch: armv7hl
          - release: "5.2.0.15"
            arch: aarch64

    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive

      - name: Build RPM
        uses: coderus/github-sfos-build@sfos5
        with:
          release: ${{ matrix.release }}
          arch: ${{ matrix.arch }}

      - name: Upload to GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          files: RPMS/*.rpm
```

### Key inputs for `coderus/github-sfos-build`

| Input | Default | Description |
|---|---|---|
| `release` | (required) | Docker image tag / OS version, e.g. `5.2.0.15` — must exist on Docker Hub |
| `arch` | `armv7hl` | `armv7hl` (32-bit ARM), `aarch64` (64-bit ARM), or `i486` (emulator) |
| `suffix` | empty | Docker image suffix; normally leave empty |

### Tips
- Use `@sfos5` for Sailfish OS ≥ 5.0; `@master` only works for older releases (< 5.0).
- Pin the action to a tag or commit in production instead of a moving branch.
- The Docker images lag OS releases — if the latest release is missing, use the newest available tag.
- `i486` is the emulator target; usually not needed in release builds.
- Built RPMs land in `RPMS/` inside the workspace.
- Set `submodules: recursive` if the repo uses git submodules for vendored dependencies.
- For GitLab CI, see the forum thread example at https://forum.sailfishos.org/t/2147

---

## OBS (Open Build Service)

The SailfishOS OBS at **https://build.sailfishos.org/** is the official community build platform.
It compiles RPMs from source for multiple SFOS versions and CPU architectures simultaneously.

### Account setup
Register at https://build.sailfishos.org/ (follow the front-page instructions).
Your home project URL will be:
`https://build.sailfishos.org/project/show/home:<username>`

### Creating your first OBS package

1. Open your home project → **Create Package**. Name must match the `.spec` filename (without `.spec`).
2. In the package page → **Add file** → upload your `.spec` file.
3. Add a `_service` file so OBS can fetch the sources from git:

   ```xml
   <services>
     <service name="tar_git">
       <param name="url">https://github.com/USER/REPO.git</param>
       <param name="branch">master</param>
       <param name="revision"></param>
     </service>
   </services>
   ```

   Leave `revision` empty for rolling home-project builds; pin a tag or commit hash
   for packages submitted to Chum.
4. Add build repositories in the project **Meta** config (XML editor):

   ```xml
   <repository name="sailfish_latest_armv7hl">
     <path project="sailfishos:latest" repository="latest_armv7hl"/>
     <arch>armv8el</arch>
   </repository>
   <repository name="sailfish_latest_aarch64">
     <path project="sailfishos:latest" repository="latest_aarch64"/>
     <arch>aarch64</arch>
   </repository>
   ```

5. OBS pulls sources, resolves `BuildRequires` from the `.spec`, and builds.
   Build logs and status appear live on the package page.

### Webhooks (auto-trigger on git push)

OBS can rebuild on every push via webhooks. In your git repo settings, add:
`POST https://build.sailfishos.org/trigger/webhook?project=home:<user>&package=<pkg>`

> **Chum exception**: Do **not** use webhooks for packages submitted to SailfishOS:Chum.
> Always specify a fixed git revision (tag or hash) for reproducible Chum builds.

### Using Chum as a build dependency

If your package depends on other Chum packages, add the Chum path to the
repository blocks from **Creating your first OBS package**:

```xml
<path project="sailfishos:chum" repository="5.2_armv7hl"/>
```

Since Sailfish OS 5.1, Chum publishes rolling `<major.minor>_<arch>` repositories
(`5.1_armv7hl`, `5.2_armv7hl`, …). Older releases use the full version, e.g.
`5.0.0.76_armv7hl`. The full list is at
https://repo.sailfishos.org/obs/sailfishos:/chum/

---

## Chum submission via OBS

SailfishOS:Chum compiles everything from source on OBS — no binary uploads.
Full guide: https://github.com/sailfishos-chum/main/blob/main/GettingStarted.md

### Submission process

1. **Build your package** successfully in your OBS home project.
2. Ensure the `.spec` `License:` tag is a valid SPDX identifier from the
   [sailfish rpmlint allowlist](https://github.com/sailfishos/rpmlint/blob/master/rpm/sailfish.toml#L151-L458).
3. Add the [Chum metadata block](#adding-chum-metadata) to your `.spec`.
4. In OBS, navigate to your package → **Submit Package**.
5. Set target project: `sailfishos:chum:testing`
6. Specify a **git tag or commit hash** as the revision — not a branch.
7. Chum maintainers review; if accepted, the package enters `sailfishos:chum:testing`.
8. After validation it is promoted to the main `sailfishos:chum` repository.

### Rules for Chum packages
- Source is fetched directly from the public git repo where development happens.
- Pinned revision only — no moving branches for submitted packages.
- License in spec must be SPDX-compatible.
- Package name in spec must match the OBS package name exactly.
- For brand-new packages not yet on OBS: open an issue at https://github.com/sailfishos-chum/main

---

## Adding Chum metadata

Chum is the community app store: https://github.com/sailfishos-chum/main
Metadata reference: https://github.com/sailfishos-chum/main/blob/main/Metadata.md

Inject the metadata as the **last paragraph of `%description`** in the RPM spec.
The whole block must be contiguous: no empty lines and no comment lines inside it.
Wrapping it in `%if 0%{?_chum} … %endif` is optional (without the guard, the metadata
is also shown by `rpm`, `zypper`, and `pkcon`).

```spec
%if 0%{?_chum}
Title: DISPLAY_NAME
Type: desktop-application
DeveloperName: AUTHOR_NAME
Categories:
 - Utility
Custom:
  Repo: REPO_URL
PackageIcon: ICON_URL
Screenshots:
 - SCREENSHOT_URL
Links:
  Homepage: REPO_URL
  Bugtracker: REPO_URL/issues
  Help: REPO_URL/discussions
  Donation: DONATION_URL
%endif
```

Notes:
- `Type` defaults to `generic`, or `desktop-application` when the package name starts
  with `harbour-`. Valid values follow AppStream: `desktop-application`,
  `console-application`, `addon`, `codec`, `inputmethod`, `firmware`, `driver`, `generic`.
- `Categories` use XDG menu categories: `AudioVideo`, `Audio`, `Video`, `Development`,
  `Education`, `Game`, `Graphics`, `Network`, `Office`, `Science`, `System`, `Utility`,
  `Media`, `Other`.
- `PackageIcon` prefers SVG; raster icons should be at least 172×172 px (up to 256×256).
- Optional fields: `PackagedBy`, `AIRating`, `AINote`, `AINoteMD`,
  `Custom: PackagingRepo`, `Custom: DescriptionMD`.
- `AIRating` values: `H` (no AI), `A` (AI outside code), `B` (AI-assisted, reviewed),
  `C` (some AI-written code), `V` (mostly AI-generated), `X` (undisclosed).
- `AINoteMD` and `DescriptionMD` take URLs to Markdown documents.

Auto-detect missing values:
- `AUTHOR_NAME` → `git config user.name` inside the project dir
- `REPO_URL` → `git remote get-url origin`
- `ICON_URL` → construct from git remote + `icons/APPNAME.svg` path

---

## Debugging Sailjail permissions

Sailjail is a thin Firejail wrapper that enforces app sandboxing since SFOS 4.4.
Full debug guide: https://github.com/sailfishos/sailjail/blob/master/APPDEBUG.md

### Step 1 — Check journald for sandbox violations

On device (as `devel-su` or root over SSH):
```bash
# Live stream — run before launching the app
journalctl -f | grep -i firejail

# Post-mortem — look for access violations
journalctl | grep -E '(firejail|sailjail|DENIED|violation)'
```

### Step 2 — Run with a sailjail filesystem trace

```bash
# Find the app's desktop file
rpm -qf /usr/bin/harbour-myapp
rpm -ql harbour-myapp | grep desktop

# Launch manually with trace enabled
sailjail --trace=/tmp/myapp-trace -p harbour-myapp.desktop /usr/bin/harbour-myapp

# Inspect the trace
cat /tmp/myapp-trace
```

### Step 3 — Enable D-Bus trace for D-Bus permission issues

Temporarily edit the `Exec=` line in the `.desktop` file:
```ini
Exec=/usr/bin/sailjail --trace=/tmp/myapp-trace --dbus-log=/tmp/myapp-dbus.log \
     -p harbour-myapp.desktop /usr/bin/harbour-myapp
```

Then filter the noisy D-Bus log for blocked calls:
```bash
grep -B2 -E '\*(HIDDEN|SKIPPED)\*' /tmp/myapp-dbus.log
```

### Step 4 — Add missing permission tokens

Identify the blocked resource in the trace and add the appropriate token to the
`[X-Sailjail]` section of the `.desktop` file.

Browse available permission files on device: `ls /etc/sailjail/permissions/`
or in the upstream repo: https://github.com/sailfishos/sailjail-permissions

See `references/guidelines.md` → **Permissions (Sailjail)** for the section format,
the Harbour-allowed tokens, and the `[X-Sailjail]` key rules.

### Step 5 — Temporarily disable sandboxing (diagnosis only)

```ini
[X-Sailjail]
Sandboxing=Disabled
```
> ⚠️ Never ship with `Sandboxing=Disabled`. Harbour will reject the app.

### Automatic private-data whitelisting

Sailjail auto-whitelists three directories based on `[X-Sailjail]` values — these require no extra permission:
```
~/.local/share/<OrganizationName>/<ApplicationName>
~/.cache/<OrganizationName>/<ApplicationName>
~/.config/<OrganizationName>/<ApplicationName>
```

### Common pitfalls
See `references/guidelines.md` → **Pitfalls by Area** → **Permissions / Sailjail pitfalls**.

---

## X-HarbourBackup (backup integration)

Allows SailfishOS apps to declare files and dconf keys for inclusion in system backups.
Requires Sailfish OS 3.2+ and the `harbour-mybackup` app installed.

Add an `[X-HarbourBackup]` section to your app's `.desktop` file:

```ini
[X-HarbourBackup]
BackupPathList=.local/share/harbour-myapp/:Documents/MyApp/
BackupConfigList=/apps/harbour-myapp/
```

### Properties

| Property | Description |
|---|---|
| `BackupPathList` | Colon-separated list of files/directories relative to home (`~`). Directories end with `/` and are copied recursively. Absolute paths are ignored. |
| `BackupConfigList` | Colon-separated list of dconf keys/groups. Groups end with `/` and are saved/restored recursively. |

### Important behavior

- **dconf restore replaces existing data** — the existing contents of dconf groups is **lost** during restore and completely replaced by the backup
- Paths are relative to `~` (home directory)
- Directory paths must end with `/` to be recognized as directories
- Group paths in `BackupConfigList` must end with `/` to be treated as groups

### Example for a typical app

```ini
[X-HarbourBackup]
BackupPathList=.local/share/harbour-myapp/:Pictures/MyApp/
BackupConfigList=/apps/harbour-myapp/
```

Reference: https://github.com/monich/harbour-mybackup

---

## Guidelines and pitfalls reference

When answering questions about SailfishOS UI patterns, permissions, D-Bus, covers, theming,
navigation, or common mistakes, load `references/guidelines.md` and draw from the relevant section.
It contains the Harbour rules, Sailjail permissions, allowed APIs, UI/UX conventions, and pitfalls.

---

## Code snippets

When the user asks for example code for a specific pattern, load `references/snippets.md`
and return the relevant snippet. Available patterns:

`page-with-pulley`, `list-view-delegate`, `cover-page`, `settings-page`,
`dbus-interface (QML)`, `dbus-interface (C++)`, `dbus-adaptor (QML)`, `c++-backend`,
`background-service`, `systemd-user-service`, `notification`, `file-picker`, `share-picker`,
`theme-aware-colors`, `keep-alive`, `remorse-item`, `section-header`, `search-field`

---

## SDK quick reference

### Target management
```bash
sfdk tools list                              # list installed toolings and targets
sfdk tools list -a                           # also list targets available to install
sfdk tools install SailfishOS-latest-armv7hl # install a build target
sfdk config target SailfishOS-latest-armv7hl # set active build target
sfdk config target                           # show current target
```

### Build shell and SDK maintenance
```bash
sfdk build-shell                             # interactive shell in build engine
sfdk build-shell rpm -q sailfishapp          # run one command in build engine
sfdk maintain                                # SDK maintenance shell
sfdk check-updates                           # check for SDK updates
sfdk update                                  # apply SDK updates
```

### Signing packages (release)
```bash
gpg --gen-key                                          # generate signing key (one-time)

# Only if the key has a passphrase
echo "my passphrase" > $HOME/passphrase.txt
chmod 0600 $HOME/passphrase.txt

sfdk config --global --push package.signing.user "Full Name"
sfdk config --global --push package.signing-passphrase-file $HOME/passphrase.txt
sfdk build --sign                                      # or: sfdk package --sign

# Verify (import the key into the RPM keyring first if verification fails)
gpg --output keyfile.gpg --armor --export "Full Name"
rpm --import keyfile.gpg
rpm -K RPMS/harbour-myapp-1.0-1.armv7hl.rpm
```
See: https://docs.sailfishos.org/Develop/Apps/Packaging/Signing_Packages

---

## Key resources

| Resource | URL |
|---|---|
| Sailfish docs | https://docs.sailfishos.org |
| Release notes | https://forum.sailfishos.org/tag/release-notes |
| Harbour FAQ | https://harbour.jolla.com/faq |
| Harbour allowed APIs | https://docs.sailfishos.org/Develop/Apps/Harbour/Allowed_APIs/ |
| Harbour allowed permissions | https://docs.sailfishos.org/Develop/Apps/Harbour/Allowed_Permissions/ |
| Harbour validator allowlists | https://github.com/sailfishos/sdk-harbour-rpmvalidator |
| Application permissions guide | https://docs.sailfishos.org/Develop/Apps/Application_Permissions/ |
| Coding conventions | https://docs.sailfishos.org/Develop/Apps/Coding_Conventions/ |
| Silica API reference | https://sailfishos.org/develop/docs/silica/ |
| OBS | https://build.sailfishos.org/ |
| Chum | https://github.com/sailfishos-chum/main |
| Chum getting started | https://github.com/sailfishos-chum/main/blob/main/GettingStarted.md |
| Chum metadata reference | https://github.com/sailfishos-chum/main/blob/main/Metadata.md |
| Chum build repositories | https://repo.sailfishos.org/obs/sailfishos:/chum/ |
| GitHub Actions build | https://github.com/coderus/github-sfos-build |
| Docker SDK image tags | https://hub.docker.com/r/coderus/sailfishos-platform-sdk/tags |
| Sailjail debug guide | https://github.com/sailfishos/sailjail/blob/master/APPDEBUG.md |
| Sailjail permissions repo | https://github.com/sailfishos/sailjail-permissions |
| Forum | https://forum.sailfishos.org |

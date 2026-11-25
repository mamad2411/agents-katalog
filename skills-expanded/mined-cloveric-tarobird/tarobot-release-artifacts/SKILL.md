---
name: tarobot-release-artifacts
description: "Use when building, packaging, signing, verifying or publishing TaroBot macOS/iOS artifacts, or creating disposable native acceptance Apps. Keeps temporary apps out of Spotlight and retires old artifacts safely."
---

# TaroBot temporary App artifacts

All temporary .app bundles must have a physical ancestor ending in .noindex.
On the owner's Mac use /Volumes/gdrive/taro-tmp.noindex/<unique-task>/ and
CARGO_TARGET_DIR=/Volumes/gdrive/dev-cache/tarobot-release-target.noindex.
The historical tarocub-macos cache's replacement is
/Volumes/gdrive/dev-cache/tarocub-macos.noindex. Never rename a shared cache or
task directory being used by another Bot. A .noindex symlink to an indexed
physical directory does not satisfy the rule.

Before building in a repository containing the current helpers:

    node scripts/macos-artifact-workspace.mjs --name release-VERSION-UNIQUE
    . /Volumes/gdrive/taro-tmp.noindex/release-VERSION-UNIQUE/build-env.sh

Put macos-ready, previous-app, paint-candidate, updater extraction, rollback,
DMG verification mounts and native acceptance Apps inside that task root.
Desktop builds use Electron: build-env.sh exports TAROBOT_DESKTOP_OUTPUT (inside
the task), TAROBOT_ELECTRON_CACHE and TAROBOT_DESKTOP_TARGET for desktop:macos.
Do not route desktop builds back through Tauri.
Do not reuse pinned historical release scripts as templates without changing
and validating every source, output and Cargo guard together.
Use the repository's macOS/iOS entrypoints; direct Tauri/Cargo commands must
inherit the same CARGO_TARGET_DIR. On another machine use a physical .noindex
output root and a per-checkout target.noindex.

After publication and asset read-back, run the guarded cleanup (the Mac
publisher does this automatically):

    python3 scripts/cleanup-macos-artifacts.py --keep-version VERSION --receipt CLEANUP.json
    python3 scripts/cleanup-macos-artifacts.py --apply --keep-version VERSION --receipt CLEANUP.json

Never touch installed Apps under /Applications (TaroBird.app or legacy TaroBot.app). Cleanup only recognized temporary App
bundles inside the configured roots, never entire task/source/data directories.
Skip directories or bundle contents modified within six hours; skip active
process open files/cwd/arguments and incomplete local activation/rollback.
If cargo, tauri, xcodebuild, rustc, signing tools, or another cleanup is active,
defer cleanup. Do not stop other Bots or their builds.
Keep the newest macos-ready backup and verify its signature before moving
anything. A missing published-version backup means defer, not delete.
Prepare and seal that backup in the release workspace before publication:
ditto the stapled Electron App from TAROBOT_DESKTOP_OUTPUT/package.noindex/
packages/TaroBird-darwin-arm64/TaroBird.app to macos-ready/TaroBird.app and verify it.
A held release keeps OWNER-HOLD.json at its task root; cleanup skips it.
Use /usr/bin/trash on a .noindex envelope containing each retired App. Do not
use rm -rf, empty the Trash, or reset Spotlight/Launch Services globally.
Recent/in-use artifacts can remain temporarily; never override guards to meet
a count. Record deferred paths honestly.
The cleanup receipt records each completed move even if later work fails.
For a known already-trashed installer backup still returned by Spotlight, use
the opt-in --legacy-trash-app exact-path mode described in the retention guide.
An in-Trash rename alone did not clear the old index in acceptance; the helper
uses a same-volume .noindex stage and /usr/bin/trash with identity read-back.

Run the supplied mdfind query after the packaging/publication rehearsal.
A backup beneath .noindex should not appear in that query; verify its existence
and version separately. Source, publication, installed-App and physical-device
acceptance remain separate. Historical receipts keep their original paths.

This skill does not authorize a release, local installation, service restart,
PR merge or messages to another Bot. Follow the user's current scope.

## Integrated skills before release

Follow `docs/release-checklist.md`'s upstream gate for editor dependencies AND their
SKILL.md, references and helper scripts. Include Baoyu Design and Baoyu PPT skill
manifests. Record checked upstream commits, review diffs, update adapted skills
with the matching editor and verify packaged/installed references. Explicit Baoyu
routing and ordinary native PPT routing both need coverage. Metadata discovery
is not proof of actual model invocation.

# civikitchen

CiviCRM dev images, the `ck*` tool belt baked into them, and the shared CI /
release workflows eleven extension repos call. User-facing: `README.md`, `docs/`.

## Layout

- `docker/` — image definitions, entrypoints, first-boot runtime, demo profiles
- `toolbelt/` — everything baked INTO an image (the image boundary): `bin/`
  (the ck* CLIs), `lib/` (shared shell + PHP payloads), ckconform, phpcs,
  phpstan, psalm, rector, mago, oxlint, oxfmt
- `scaffold/` — host-side extension scaffolding, never in an image:
  `ckinit.php` and the `template/extension/` tree it stamps into consuming
  repos
- `scripts/` — host-side helpers for working on THIS repo, never in an image
  (`doctor.sh`, the host-prerequisite report `make doctor` runs)
- `tests/` — this repo's own suites (ckinit, toolbelt/Dockerfile parity,
  image boot tests, e2e)

Build context is the repo root, so a Dockerfile can COPY from both trees.

## Verify

`make test` and `make lint` need no Docker and are literally what
`.github/workflows/lint.yml` runs. Run both before committing. `make help` for
the rest; `make test-images` is the ~1 h Docker round.

## Rules

- **One parser per format.** `civikitchen.yaml` → `ckconform --policy-env` /
  `--policy <key>`; XML and JSON → `ck_xml_field` / `ck_json_field` in
  `toolbelt/lib/ckcommon.sh`. Never `sed`/`grep -o` a structured file. A new
  Public YAML keys belong in the JSON Schema; every normalized key exposed to
  a consumer also belongs in `Policy::KEYS`.
- **Select files by what they are, not where they live.** A directory list
  fails open: the run says "clean" about files it never saw.
- **A fix ships with the fixture that would have failed.** Most checks here are
  silent on success.
- **Container paths are the interface** (`/usr/local/bin/ck*`,
  `/opt/civikitchen-*`). Repo paths move freely; those do not.
- **Comments record facts; the arguing goes in the commit message.** No counts,
  they go stale.
- **One versioned contract**: workflows, template, tools and images release
  together and consumers pin `@v1` (`docs/releases.md`).

## Traps

- In the *reusable* workflows (`extension-ci`, `extension-release`) `uses: ./…`
  resolves against the CALLING repo. Reach this repo by checking it out at
  `ref: ${{ job.workflow_sha }}` — never a floating ref.
- `a && b` as a statement under `set -e` aborts a loop. Use `if`.
- The `ck*` tools carry no `.sh` suffix; a `*.sh` sweep silently skips them all.
- `shellcheck` needs `external-sources` (`.shellcheckrc`) to see `ckcommon.sh`.
- `toolbelt/versions.env` holds only pins with two or more readers.
- `zizmor.yml` exemptions are anchored `file:line:col`. Editing a workflow
  above an exempted step shifts the line and the finding returns — re-pin it,
  never widen the entry to the whole file.

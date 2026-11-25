---
name: release
description: Release llm-light to PyPI - prepare the version PR, dry-run on TestPyPI, publish the GitHub release, verify the install. Re-run after each hand-off.
argument-hint: "[X.Y.Z]"
disable-model-invocation: true
---

# Release llm-light

A release is a **state machine**: each run reads where version `V` stands, does that phase, and stops at the next hand-off. The user re-runs `/release V` after each one. The PyPI project is `llm-light-cli` (`pyproject.toml`'s `name`), and it installs the `llm-light` command. Uploads happen only through `.github/workflows/publish.yml` (trusted publishing); every local build is a check, never an upload. The workflow, the one-time setup and the manual steps this automates are in [docs/WORKFLOW.md](../../../docs/WORKFLOW.md#publishyml-publish-to-pypi).

## Irreversible steps

PyPI and TestPyPI each accept a version once, even after a delete. Three commands are irreversible: the TestPyPI dispatch, the tag, and the GitHub release. Each one needs a yes from the user in this run, asked with `AskUserQuestion` right before it runs, naming `V` and the commit. A yes from an earlier run or phase does not carry over. Merging the release PR is the user's. When an upload fails after its file landed, `V` is burned: release the next patch version instead.

Work in the session scratchpad (`$S` below) for venvs, builds and notes, and run each smoke test from a directory outside the checkout so the source tree cannot shadow the installed package.

## 1. Find the phase

1. `V` is `$ARGUMENTS`. If it is empty, show `python scripts/release.py current`, the `## [Unreleased]` section of `CHANGELOG.md`, and ask which version to release (offer the next patch and the next minor).
2. Read the state:
   ```bash
   git fetch -q origin --tags
   git show origin/main:pyproject.toml > "$S/main-pyproject.toml"
   python scripts/release.py current --pyproject "$S/main-pyproject.toml"           # M
   curl -s -o /dev/null -w '%{http_code}\n' https://test.pypi.org/pypi/llm-light-cli/V/json  # T
   curl -s -o /dev/null -w '%{http_code}\n' https://pypi.org/pypi/llm-light-cli/V/json       # P
   git ls-remote --tags origin refs/tags/vV                                          # tag
   ```
3. Pick the first row that matches:

   | State | Phase |
   |---|---|
   | P is 200 | 5. Verify |
   | tag exists | 4. Watch the publish run |
   | M is V, T is 200 | 3. Release |
   | M is V, T is 404 | 2. Dry run |
   | M is not V | 1b. Prepare |

Done when the phase is named and its inputs are printed. Report them to the user in one line.

## 1b. Prepare the version PR

1. Read the full `git status --short`. Tracked changes belong to the user: stop and ask. Untracked files stay where they are.
2. `git switch -c release/vV origin/main`.
3. `python scripts/release.py bump V`. If it refuses because `[Unreleased]` is empty, draft entries from `git log --merges --format='%s%n%b' vM..origin/main` in the file's existing style, show them, and bump only after the user approves them.
4. Run the gates, every one **green** before the commit:
   - The unit, integration and utilities steps of `test.yml` as `docs/WORKFLOW.md` lists them, with the same timeouts.
   - `python tests/linting/check_release_tag.py vV`.
   - `python -m build --outdir "$S/dist-V" .`, then `twine check --strict "$S"/dist-V/*`, then delete the `llm_light.egg-info/` the build leaves in the tree.
5. Commit `pyproject.toml` and `CHANGELOG.md` as `Release V`, with a body naming what the release carries. Push, open the PR against `main` with the changelog section as its body, and arm `gh pr checks <N> --watch` in the same turn. Fix every red check and re-arm.

Done when every check on the PR is green. Hand over: merge it with a merge commit, then run `/release V` again.

## 2. Dry run on TestPyPI

1. Ask before dispatching: TestPyPI keeps `V` for good.
2. `gh workflow run publish.yml --ref main`. List `gh run list --workflow publish.yml --event workflow_dispatch -L 1 --json databaseId,headSha,createdAt` until a run created after the dispatch appears, then `gh run watch <id> --exit-status`. A failure at the OIDC exchange means the trusted publisher or the `testpypi` environment is missing: point the user to the one-time setup in `docs/WORKFLOW.md` and stop.
3. Smoke-test the uploaded wheel in a fresh venv. Take only the wheel from TestPyPI; dependencies resolve from PyPI alone, because anyone can upload a higher-versioned `rich` or `numpy` to TestPyPI:
   ```bash
   py -3.12 -m venv "$S/venv-test-V"     # python3.12 on Linux and macOS
   "$S/venv-test-V/Scripts/python" -m pip download --no-deps --index-url https://test.pypi.org/simple/ -d "$S/testpypi-V" llm-light-cli==V
   "$S/venv-test-V/Scripts/python" -m pip install "$S"/testpypi-V/llm_light_cli-V-py3-none-any.whl
   ```
   A fresh upload can take a minute to appear on the simple index; retry the download. The install pulls PyTorch (about 1.5 GB): run it in the background.
4. From a directory outside the checkout, run `llm-light --version` and `llm-light --help`.

Done when `--version` prints `llm_light V` and `--help` exits 0. Report the run's `headSha`: phase 3 releases that exact commit.

## 3. Publish the release

1. Take `SHA`, the full `headSha` of the latest successful `workflow_dispatch` run of `publish.yml`. Confirm `git show SHA:pyproject.toml` says version `V` and `git merge-base --is-ancestor SHA origin/main` exits 0. Releasing that commit, not the current `main`, publishes exactly what the dry run tested.
2. `python scripts/release.py notes V > "$S/notes-V.md"` and show the notes.
3. Ask, naming `vV` and the short `SHA`, with three options: publish with a tag GitHub creates; sign the tag first (the user runs `! git tag -s vV SHA -m "llm-light V"` and `! git push origin vV`, see `RELEASE_SIGNING.md`); or stop.
4. Publish: `gh release create vV --target SHA --title "llm-light V" --notes-file "$S/notes-V.md"`, adding `--verify-tag` (and dropping `--target`) when the user pushed a signed tag.

Done when `gh release view vV` shows the release. Continue straight to phase 4.

## 4. Watch the publish run

1. Find the run: `gh run list --workflow publish.yml --event release --commit SHA --json databaseId,status,conclusion`, listing again until it appears, then `gh run watch <id> --exit-status` in the background.
2. If the `pypi` job is waiting on its environment, tell the user to approve it in the run's page, and keep watching.
3. A red run: read the failing job's log. The tag check failing means the tag and `pyproject.toml` disagree; nothing was uploaded, so delete the release and its tag only after the user agrees, then go back to phase 3. An upload failing after the file landed burns `V`.

Done when the run's conclusion is `success`. Continue to phase 5.

## 5. Verify

1. `curl -s https://pypi.org/pypi/llm-light-cli/V/json` lists a wheel and an sdist under `urls`.
2. In a fresh venv, `pip install llm-light-cli==V` from PyPI alone. From outside the checkout, `llm-light --version` prints `llm_light V`.
3. `gh release view vV --json assets --jq '.assets[].name'` includes `sbom.json`, which `sbom.yml` attaches.

Done when all three hold. Report the PyPI and release URLs and which of the three checks passed. Any check that could not run is reported as not run, never as passed.

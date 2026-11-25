---
name: bukzor-python-packaging
description: "Agent MUST load when creating a Python package repo, preparing a PyPI release, or setting up packaging CI/CD"
---

# Python packaging: bukzor norms

Lifecycle norms for publishing Python packages, distilled from the
typed-json/python-typed-json release. Sections follow the lifecycle;
skim headers, read the one that matches the work at hand.

## Naming

PyPI is a flat namespace (PEP 752 namespacing was rejected). Names allow
only ASCII alphanumerics plus `. _ -` (start/end alphanumeric), and PEP
503 collapses any separator run to a single `-`, so `a.b`, `a_b`, `a-b`
are the same project.

Upload additionally enforces a similarity check: the name with all
separators stripped must not equal any existing project's stripped form.
A 404 from `pypi.org/pypi/NAME/json` is NOT sufficient evidence the name
is available. Verify against the real rule:

```bash
curl -s -H 'Accept: application/vnd.pypi.simple.v1+json' \
  https://pypi.org/simple/ -o trash/pypi-index.json   # ~40MB, all projects
jq -r '.projects[].name' trash/pypi-index.json |
  tr 'A-Z' 'a-z' | tr -d -- '-_.' | sort -u > trash/pypi-squashed.txt
grep -xF "$(printf %s "$NAME" | tr 'A-Z' 'a-z' | tr -d -- '-_.')" \
  trash/pypi-squashed.txt   # match = taken
```

Residual risk: PyPI also maps look-alike characters (`0`/`o`, `1`/`l`);
a form/upload bounce is the cheap definitive test.

Defaults when the bare name is blocked:

- `python-` prefix on the dist name only (`python-dateutil`,
  `python-dotenv` tradition); the import keeps the bare module name.
  Add a README note explaining the dist/import split.
- `bukzor-` prefix means "by me, for me" -- never use it for a package
  published for general consumption.
- The GitHub repo matches the *import* name, not the dist name
  (`dateutil/dateutil` precedent): the prefix is a PyPI-local
  workaround and shouldn't leak into other namespaces.

## New repo (or subpath)

- `copier copy gh:bukzor/template.python-project NAME`, then `uv sync`,
  `uv run pre-commit install`.
- Run `uv run pre-commit run --all-files` immediately and keep it green
  from day one. A repo where hooks never ran repo-wide accumulates
  formatting debt that later breaks unrelated commits (black once broke
  line-anchored typesafety tests; such files get `# fmt: off` with the
  reason).
- Publish the repo at creation: `gh repo create bukzor/NAME --public
  --source=. --push`, then `gh repo edit` to set description and, once
  released, homepage = the PyPI project page.
- Settle the repo name BEFORE registering the PyPI publisher: the
  publisher pins owner/repo via OIDC claims, and GitHub rename
  redirects do not apply to OIDC. Renaming the repo orphans the
  publisher.

## Localhost tooling

Defer to `bukzor/template.python-project` (uv, black, pyright strict,
pre-commit via `uv run`, direnv). Packaging-specific requirements on top
of the template, all before first upload (release METADATA is
immutable):

- `[project]`: `license` as an SPDX expression matching the LICENSE
  file, `authors = [{ name = "Buck Evan", email =
  "workitharder+pypi@gmail.com" }]`, and `[project.urls] Repository`.
- Cross-check README, LICENSE, and pyproject agree on the license.
- Wheel contents: package dir under `lib/`, `[tool.hatch.build.targets.wheel]
  packages = ["lib/NAME"]` with `**/*_test.py` excluded, `py.typed`
  marker present. Verify with `uv build` + `unzip -l dist/*.whl`.

## Remote CI (GHA)

`.github/workflows/ci.yml` on push/PR: `uv sync`, `uv run pre-commit run
--all-files`, `uv run pytest`. CI is separate from the release workflow
so publish never depends on a green badge race.

## Prepare PyPI (trusted publishing)

Never mint API tokens; use trusted publishing. Pending publishers make
this work even for the first release of a not-yet-existing project.

1. Create the GitHub environment: `gh api -X PUT
   repos/bukzor/REPO/environments/pypi`.
2. Human step, needs a logged-in browser:
   pypi.org -> Account settings -> Publishing. Existing and pending
   publishers are listed above the form -- check before adding.
   Form values: PyPI Project Name = dist name, Owner = `bukzor`,
   Repository = repo name, Workflow = `release.yml`, Environment =
   `pypi`.
3. The pending publisher becomes a permanent one on first successful
   publish. Nothing to clean up.

## Remote CD

`.github/workflows/release.yml`, verbatim baseline:

```yaml
name: release

on:
  push:
    tags: ["v*"]

jobs:
  pypi:
    runs-on: ubuntu-latest
    environment: pypi
    permissions:
      # required for PyPI trusted publishing (OIDC)
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv build
      - run: uv publish
```

`uv publish` auto-detects the ambient OIDC credential in GHA; no
secrets, no action inputs.

## Local release

1. Bump `version` in pyproject; commit; push.
2. `git tag -a vX.Y.Z -m "DIST X.Y.Z: summary"`; `git push origin vX.Y.Z`.
3. Watch: `gh run watch $(gh run list -w release.yml -L1 --json
   databaseId -q '.[0].databaseId') --exit-status`.
4. Verify the consumer path, not just the upload:
   `curl -s https://pypi.org/pypi/DIST/json | jq .info.version` and
   `uv run --no-project --isolated --with DIST python -c 'import MODULE'`.

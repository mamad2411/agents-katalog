---
name: gitlab_pages_ci
description: GitLab CI — test job and GitLab Pages job (artifact `public/`); `.gitlab-ci.yml` templates
triggers: [gitlab, git lab, .gitlab-ci, ci/cd, pipeline, pages, gitlab pages, pytest ci, npm test ci]
tools: [shell]
platform: all
---

## GitLab CI + Pages

The **GitLab Runner** executes the pipeline, not the bot. Your job is to **add or fix** `.gitlab-ci.yml` in the repo and list what to enable in GitLab (Settings → Pages, visibility).

### General layout

- `stages: [test, deploy]` (or `[test, pages]`).
- **test** job: same stack as local (Python/Node/Go). Default image from process env `GITLAB_CI_DEFAULT_IMAGE` (e.g. `python:3.12-bookworm`) — use it in YAML if the project has no `image:`.
- **pages** job: GitLab requires a `public/` artifact. Build the static site (MkDocs, VitePress, `sphinx -b html`, SPA `npm run build` then copy into `public/`) and declare:

```yaml
pages:
  stage: deploy
  needs: ["test"]
  script:
    - mkdir -p public
    - cp -r dist/* public/   # example; adapt to the project
  artifacts:
    paths:
      - public
```

### Python (pytest) + minimal Pages stub

Template “tests + placeholder site”:

```yaml
stages: [test, deploy]

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

test:
  stage: test
  image: python:3.12-bookworm
  cache:
    paths: [.cache/pip]
  before_script:
    - python -m pip install -U pip
    - test -f requirements.txt && pip install -r requirements.txt || true
    - test -f pyproject.toml && pip install -e ".[dev]" || true
  script:
    - pytest -q || true

pages:
  stage: deploy
  needs: ["test"]
  image: alpine:latest
  script:
    - mkdir -p public
    - echo '<!doctype html><meta charset=utf-8><title>CI</title><p>GitLab Pages OK</p>' > public/index.html
  artifacts:
    paths: [public]
```

Tune `pytest` for the real layout (`tests/`, `uv run`, etc.).

### Node / static frontend

- `image: node:22-bookworm` (or project LTS).
- `cache: { paths: [node_modules/] }`
- `script: npm ci && npm run build` → output in `dist/` or `build/` → copy into `public/`.

### Important

- No **secrets** in YAML; use GitLab **CI/CD Variables** (masked).
- If `.gitlab-ci.yml` already exists — **extend** stages/jobs; do not break production-branch deploy without explicit user approval.
- After merge: Pages URL like `https://<namespace>.gitlab.io/<project>/` (depends on settings); tell the user to check **Deploy → Pages** in the UI.

# AGENTS.md

Instructions for AI coding agents (Codex, Claude Code, Cursor, Gemini CLI, Copilot,
OpenCode, Windsurf, ...) working **on this repository**. To *use* the skills, install
them. See README.md.

## Layout

- `skills/<name>/SKILL.md`: one folder per skill (flat). `name` must equal the folder name.
- `tools/`: Python tooling (validate, import, rebrand, lint, catalog). Run with `uv run`.
- `cli/`: TypeScript installer published to npm as `research-agent-skills`.
- `third_party/`: upstream import config, categories, rebrand rules, patches, provenance manifest.
- `security/`: domain allowlist and reviewed-finding baselines.
- Generated (never hand-edit): `.claude-plugin/marketplace.json`, `plugin.json`, `catalog/*`,
  `skills.sh.json`, `skills/research-agent-skills/references/catalog.md`,
  `THIRD_PARTY_NOTICES.md`, `docs/skills/*`, the README catalog block. Regenerate with
  `uv run tools/build_catalog.py --docs` before publishing documentation.

## Commands

```bash
uv sync                                   # tooling deps
uv run tools/validate.py                  # spec + policy for all skills
uv run tools/lint_injection.py            # security lint (fails on new findings)
uv run tools/brand_guard.py               # provenance naming policy
uv run tools/build_catalog.py [--check]   # regenerate derived files
uv run python -m pytest -q                # tooling + skill script tests
uv run tools/skill_quality.py             # static quality rubric (original skills must score >= 80)
uv run tools/trigger_bench.py             # does the right skill get picked? (evals/*/evals.json)
cd cli && npm ci && npm test              # CLI build + tests
make check                                # everything CI runs on a pull request
```

Benchmarks and their methodology: `benchmarks/README.md`. Every new skill needs `evals/<name>/evals.json`
with realistic prompts and at least one near miss.

## Rules

- Keep SKILL.md under 500 lines. Put detail in `references/`.
- Scripts: standard library first, `argparse`, exit codes 0/1/2, UTF-8 console setup, timeouts on HTTP.
- New network domains in scripts need an entry in `security/allowed-domains.txt`.
- Never update `security/*baseline*.json` without reviewing each new finding.
- Edits to adapted (imported) skills go through `third_party/patches/*.patch`. Otherwise
  `tools/import_upstream.py` overwrites them.
- Don't add upstream project names outside `LICENSES/`, `THIRD_PARTY_NOTICES.md` and `third_party/`
  (enforced by `tools/brand_guard.py`).

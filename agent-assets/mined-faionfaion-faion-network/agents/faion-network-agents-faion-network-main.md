# faion-network

Methodology corpus and Claude Code skill base for the `faion` CLI. Auto-loaded in every session (symlinked as `~/workspace/.claude`), so this file stays inside the 20-80 line budget — deep content lives in `.agents/`.

| Item | Value |
|------|-------|
| Repo | `faionfaion/faion-network` |
| Corpus | **2,519** methodology dirs over 22 domains, **443** playbook dirs, 6 workflows, 6 skill dirs (recounted on disk 2026-09-10 after CR-006 merged the `sdd/templates` pair) |
| Gating | `skills/tier-manifest.json` **v14, 2,987 entries** — authoritative path-to-tier map; every methodology and playbook dir on disk resolves in it (regenerated 2026-09-10). The generator walks **seven** roots; a dir under `skills/faion/` it does not name is never read and inherits a tier silently |
| Composable | 25 fragments over 6 packs, 4 recipes, **13 tool packs / 29 tools**, 1 variable dictionary. Fragments, recipes and the dictionary are tier **free**; tool packs are gated per pack — `browser`/`deploy`/`python-web`/`research`/`static-web`/`template-builder` free, `cloudflare`/`env-topology`/`game-dev`/`web-parse` solo, `github-ci`/`hetzner`/`sdd-sync` pro |
| Tiers | free / solo / pro / geek (cumulative) |
| Distribution | Read by `faion-cli` at runtime; read by `faion-net-be` on disk via `KNOWLEDGE_ROOT` + `TIER_MANIFEST_PATH`; not bundled into the public `faion` plugin |
| Ecosystem | `../AGENTS.md` — full stack and runtime data flow |

## Layout

| Path | What |
|------|------|
| `skills/faion/knowledge/<domain>/<slug>/` | Methodology: `AGENTS.md` + `meta.json` + `content/*.xml` (+ `templates/`, `scripts/`) |
| `skills/faion/playbooks/<goal>/<slug>/` | Playbook: `AGENTS.md` + `content/01-playbook.xml`. `playbooks/by-goal/<goal>/` holds only the L2 `INDEX.xml` — no leaf has ever lived under it |
| `skills/faion/fragments/<pack>/` · `skills/faion/recipes/<name>/` | Role prompts composed into pipelines · the recipes that compose them; both carry an `INDEX.xml` |
| `skills/faion/workflows/` | 6 orchestration workflows (brainstorm, idea-to-prod, improver, media-ops, poll-agents, sdd-batch-orchestrator) |
| `skills/faion/tools/<pack>/` | Tool pack: `meta.json` + `scripts/<name>.py\|sh` + `tools/<name>.card.md` — runnable tools an agent uses instead of writing a throwaway script |
| `skills/faion/lexicon/` | UA→EN query lexicon: `meta.json` (tier **free**) + `ua-en.tsv` + `ua-stopwords.txt` — a Ukrainian query scores zero against an English corpus without it |
| `skills/faion/templates/` | Corpus-wide variable dictionary: `meta.json` (tier **free**) + `vars-dictionary.schema.json`, 66 canonical parameters every `*.vars.schema.json` `$ref`s into |
| `skills/tier-manifest.json` | Generated from `meta.json` files — never hand-edit |
| `agents/` · `hooks/` · `rules/` | Subagent definitions · plugin hooks (`hooks.json`) · authoring rules |
| `workflows/` | Runnable Workflow-tool scripts, invoked by name (`article-pipeline`) |
| `scripts/` | Validators and index/manifest generators |
| `docs/` | Corpus specs: `skill-authoring.md`, `directory-structure.md`, `methodology-xml-schema.md` |
| `.aidocs/` | SDD lifecycle docs for this repo |
| `.agents/` | Deep reference — see [.agents/INDEX.md](.agents/INDEX.md) |

## Commands

```bash
bash scripts/f066-validate-all.sh                    # all 11 corpus validators, summary report (~4 min)
bash scripts/check-validators.sh --check-fast        # the gate the hook runs: failure SET vs baseline
bash scripts/install-hooks.sh                        # point core.hooksPath at .githooks (init.sh does it too)
python3 scripts/validate-methodology-v2.py <dir>     # one methodology dir
python3 scripts/validate-playbook-v3.py --all        # all playbooks
python3 scripts/validate-domains-index.py            # L1 domains.xml
python3 scripts/validate-lexicon.py                  # UA→EN lexicon shape + provenance
python3 scripts/regen-tier-manifest.py --dry-run     # manifest diff vs meta.json (drop flag to write)
bash tests/test_snapshot.sh                          # installer unit tests
bash init.sh                                         # install skills + agents into ~/.claude
```

## Rules

- **Commits** — `type: short description`, 50-char title, no `Co-Authored-By`, no emojis. Every commit adds an entry under `## [Unreleased]` in `CHANGELOG.md`.
- **Language** — user Ukrainian; docs, code and subagent prompts English.
- **Documentation** — no ASCII art; tables, lists, arrows (`→`) and directory trees are fine.
- **Docs convention** — every source dir carries `CLAUDE.md` (exactly `@AGENTS.md`) + `AGENTS.md` (20-80 lines: purpose, file table, commands, gotchas). Full rules: [.agents/docs-convention.md](.agents/docs-convention.md)
- **SDD** — features `backlog/ → todo/ → in-progress/ → done/`; tasks inside a feature `todo/ → in-progress/ → done/`. Document types and CR/BUG streams: [.agents/sdd-lifecycle.md](.agents/sdd-lifecycle.md)
- **No time estimates** — never state hours, days or dates in SDD docs; use qualitative complexity and token estimates.
- **Linting** — every project must have working pre-commit hooks; on failure fix the cause, never `--no-verify`. Per-project setup: [.agents/linting.md](.agents/linting.md)
- **Skill authoring** — read `rules/skill-authoring.md` before creating or editing anything under `skills/`.
- **Tool authoring** — read `rules/tool-authoring.md` before adding or editing anything under `skills/faion/tools/`; stamp from `docs/templates/`, never hand-roll.
- **Adapters** — packaged for Claude Code and Codex; runtime-specific behavior: [.agents/adapters.md](.agents/adapters.md)

## Gotchas

- `skills/tier-manifest.json` is **generated** from `meta.json` files — regenerate with `regen-tier-manifest.py`; hand-edits get overwritten.
- **`INDEX.xml` is generated — run `regen-domains-xml.py --write`, do not hand-edit.** It reads `meta.json` and rebuilds both L1 `domains.xml` and every L2 `INDEX.xml`; dry-run is the default and it backs up before writing. The three frontmatter-reading builders that used to sit beside it were deleted 2026-08-14 — they read metadata F-067 moved to `meta.json`, so they emitted `count="0"` and silently emptied the index they targeted. Hand-editing was a workaround for those, and it let `count=` drift out of step with the disk.
- The manifest is at `skills/tier-manifest.json`, not the repo root.
- **The hooks are real now** (`core.hooksPath=.githooks`, installed by `init.sh` or `scripts/install-hooks.sh`). `commit-msg` enforces the title rule; `pre-commit` gates the `## [Unreleased]` CHANGELOG entry, the 20-80 line budget on staged `AGENTS.md` files, and the corpus validators — 9 whole-corpus sweeps in full plus `validate-methodology-v2` scoped to the slugs the commit touches, because the full v2 sweep is ~205 s of the ~4 min total. The gate is on the failure **SET** in `scripts/validator-baseline.txt`, never on counts: a count waves through a swap. Never `--no-verify`.
- Methodology and playbook dirs already carry their own `AGENTS.md` envelope fixed by the corpus spec. Do not add repo-style `AGENTS.md` / `CLAUDE.md` pairs anywhere under `skills/faion/knowledge/**` or `skills/faion/playbooks/**`.
- **A slug lives in exactly one domain** — which domain is decided by [.aidocs/conventions/domain-boundaries.md](.aidocs/conventions/domain-boundaries.md), not by taste. 19 slugs still resolve in two domains **on purpose** (both copies are real; the fix is a rename, deferred). Retired copies live in [`.archive/`](.archive/README.md) and were merged before they were archived.
- **`content_id` is NOT a content hash** and never has been: 0 of 2,520 match the algorithm `meta-json-spec.md` §6 declares, and the `compute-content-id.py` it calls canonical does not exist. The only enforced check is a 16-hex regex. Never use it as a duplication or drift test.
- **A `.json` reaches a user's disk only from under a `templates/` path segment.** `packablePath` (`faion-cli/tools/vfs-pack/pack.go`) ships `.md`/`.xml` from anywhere, `.py`/`.sh` only from `scripts/`, `.tsv`/`.txt` only from `lexicon/`, and **everything** under `templates/` un-extension-gated (F036/AD-024); `meta.json` is excluded everywhere as packer input. Proven by test: `faion/templates/vars-dictionary.schema.json` ships, `faion/schemas/…` does not. Moving a data file to a tidier-looking dir makes it invisible on every user's machine while every validator here stays green — validators read the disk, the packer decides delivery.
- **A `content/*.xml` file absent from its `## Content` table is still delivered — but never chosen.** Nothing parses that table (0 consumers across `faion-cli`, `faion-net-be` and `scripts/`); delivery resolves by directory, and a publish of this corpus lists all 177 unlisted files as parts. What the table decides is what an agent reading the envelope knows exists, and `--parts` still cannot name a non-canonical file. [CR-010](.aidocs/improvements/CR-010-undelivered-content-bodies.md) asserted the opposite and carries the correction. Adding content still means adding the table row.
- `06-decision-tree.xml` has a hard depth cap of **5**; 362 of 2,510 trees (14.4%) sit at it, so check before nesting and prefer flat sibling branches. It is **not** a reason a tree cannot be improved — 434 of the 455 fully-generic trees have depth ≤4 and room to spare.
- **`04-procedure.xml` is validated by nothing.** `01`, `02`, `03` and `06` each have a validator; grep every script and `04` is opened by none of them. 2,238 files, zero checks.
- Retrieval is two-level: read `skills/faion/knowledge/domains.xml` (L1), pick at most 3 domains, then their `INDEX.xml` (L2) before opening any leaf. Never enumerate the corpus. **Cross-links live in `meta.json`, not in `AGENTS.md` prose** (`assumes_loaded`, `related` — spec §3.2; lift with `scripts/sync-crosslinks-to-meta.py`, `--check` gates drift, `--annotate` stamps the `canonical:` marker each leaf carries, resolved by `validate-methodology-v2`). Only `assumes_loaded` reaches L2 as `<assumes>`: a link earns a place in the index only if it changes *what you retrieve*, and carrying `related` there too measured +43% against +19% to restate slugs the index already lists. A `[[slug]]` inside a sentence stays prose.
- `README.md` still quotes pre-F-067 counts (52 knowledge bases, 1,300+ methodologies). The manifest is the source of truth. (`skills/CLAUDE.md` and `skills/faion/CLAUDE.md` carried the same stale counts and were deleted 2026-08-13 — they were orphan `CLAUDE.md` files with no `AGENTS.md` to point at.)

## Agent memory

Project knowledge carried over from the Claude auto-memory store on 2026-08-12 (decisions, gotchas, incident post-mortems): [.agents/nero-memory.md](.agents/nero-memory.md). Verbatim as written at the time — verify against code before relying on a specific path or number.

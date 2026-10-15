---
name: skill-package-manifest-enricher
description: >-
  Enrich portable skill ZIP manifests with compatibility and eval metadata.
  Use before packaging or catalog promotion. NOT for live installs.
user-invocable: true
argument-hint: "<skill-name> [--dry-run|--apply]"
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0.0"
---

# Skill Package Manifest Enricher

Augment package manifests produced by skill-creator packaging with repo metadata.

**Scope:** Manifest enrichment only. Does not emit ZIPs or run live installs.

## Dispatch

| $ARGUMENTS | Action |
|------------|--------|
| `<name>` | Preview enriched manifest fields for one skill |
| `<name> --dry-run` | Show diff without writing |
| `<name> --apply` | Write `manifest.enriched.json` beside packaging output |
| Empty | Show enriched field catalog and workflow |

## Enriched Fields

The enricher adds when missing:

- `compatibility_notes` from `compatibility` frontmatter
- `eval_case_count` from `evals/evals.json`
- `harness_targets` from catalog/sync metadata when present
- `packaged_at` UTC timestamp (apply mode only)

## Workflow

```bash
uv run python skills/skill-package-manifest-enricher/scripts/enrich_manifest.py <name> --dry-run
uv run python skills/skill-creator/scripts/package.py skills/<name>/ --dry-run
```

## Validation Contract

```bash
uv run python skills/skill-package-manifest-enricher/scripts/check.py
```

## Critical Rules

1. Run skill-creator `package.py --dry-run` after enrichment preview.
2. Never commit machine-local absolute paths into enriched manifests.
3. Treat enrichment as additive; do not delete upstream manifest keys.
4. Require explicit `--apply` before writing enriched manifest files.
5. Route ZIP creation to skill-creator `package` mode.

# Internationalization (i18n)

## Summary

**One-sentence:** Extracts user-facing strings to ICU MessageFormat keys, formats dates/numbers/currency via Intl/Babel, uses logical CSS properties for RTL, and validates key drift in CI.

**One-paragraph:** Extracts user-facing strings to ICU MessageFormat keys, formats dates/numbers/currency via Intl/Babel, uses logical CSS properties for RTL, and validates key drift in CI. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Product ships to ≥2 locales OR plans to within the next 2 quarters.
- Codebase mixes hardcoded English strings with user-facing surfaces.
- Right-to-left support (Arabic, Hebrew) is on the roadmap.
- Output produces `spec` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Product ships to ≥2 locales OR plans to within the next 2 quarters.
- Codebase mixes hardcoded English strings with user-facing surfaces.
- Right-to-left support (Arabic, Hebrew) is on the roadmap.

## Skip If (ANY kills it)

- Single locale forever (verified by product) — overhead does not pay back.
- Static brochure site with no dynamic strings.
- All user content is user-generated; only chrome strings need translation and they are <20 strings.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Locale list | list of BCP-47 tags | product |
| ICU library | react-intl / FormatJS / Babel + ICU | team |
| CI runner | GitHub Actions | infra |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[best-practices-2026]] | TS/Python strict baseline supports the i18n setup |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure with input/action/output per step | 900 |
| `content/05-examples.xml` | reference | One full worked example end-to-end with the trace and the resulting artefact | 700 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `string-extraction` | sonnet | Detect hardcoded strings and replace with t('key'). |
| `rtl-audit` | sonnet | Replace physical CSS properties with logical ones. |
| `key-drift-check` | haiku | Mechanical missing-key detection in CI. |

## Templates

| File | Purpose |
|------|---------|
| `templates/locale_en.json` | Base English locale file: ICU MessageFormat keys |
| `templates/key_drift_check.py` | CI check: every key in en.json exists in all locales |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-internationalization.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[best-practices-2026]]
- [[practices-frontend-components]]
- [[feature-flags-rollout-targeting]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Will the product ship to ≥2 locales OR include RTL within 2 quarters?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/locale_en.json`

```json
{
  "checkout.title": "Checkout",
  "checkout.items_count": "{count, plural, one {# item} other {# items}}",
  "checkout.total": "Total: {amount, number, ::currency/USD}"
}
```

### `templates/key_drift_check.py`

```python
# faion_header_json: {"__faion_header__":{"purpose":"CI check: every key in en.json exists in all locales","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#icu-messageformat","token_budget_impact":"~150 tokens when loaded"}}
import json
import sys
from pathlib import Path


def main() -> int:
    en = json.loads(Path("locales/en.json").read_text())
    keys = set(en.keys())
    bad = False
    for path in Path("locales").glob("*.json"):
        if path.name == "en.json":
            continue
        other = json.loads(path.read_text())
        missing = keys - set(other.keys())
        if missing:
            sys.stdout.write(f"{path.name} missing: {sorted(missing)}\n")
            bad = True
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
```

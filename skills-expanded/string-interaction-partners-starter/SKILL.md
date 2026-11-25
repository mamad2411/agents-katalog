# STRING Interaction Partners Starter

Use this skill to query the official STRING API for high-confidence interaction partners of one gene or protein identifier and summarize the returned evidence in compact JSON.

## What it does

- Calls STRING's `interaction_partners` API for one identifier and one species.
- Returns the query identifier, resolved STRING IDs, top partners, and confidence evidence scores.
- Falls back to a committed canonical asset for the standard `TP53` smoke path if STRING is temporarily unavailable.

## When to use it

- You need a lightweight official starter for `protein-protein interaction analysis`.
- You want a quick candidate partner list before deeper network or pathway analysis.

## Example

```bash
python3 skills/systems-biology/string-interaction-partners-starter/scripts/run_string_interaction_partners.py \
  --identifier-file skills/systems-biology/string-interaction-partners-starter/examples/tp53_query.txt \
  --species 9606 \
  --limit 5 \
  --required-score 700 \
  --out scratch/string/tp53_partners.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/systems-biology/string-interaction-partners-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_phase28_network_materials_cheminformatics_skills -v`

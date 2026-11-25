---
name: fusion-ml-options
description: >-
  Present the required Fusion-ML ranked startup menu. Use when the user asks for
  Fusion-ML options, route selection, workflow choice, or when any Fusion-ML task
  begins and no option has been chosen.
---

# Fusion-ML Options

Run the option ranker and present exactly five choices.

```bash
bash "$FUSION_ML_PLUGIN_ROOT/scripts/fusion-ml.sh" options --task "<task>"
```

The output already includes workflow/loop, Fusion type, agents, gates, and
first skill. Ask the user to choose one of the five options. If the user replies
`recommended`, proceed with rank 1.

Do not collapse this menu to a single recommendation. The menu is part of the
plugin contract.


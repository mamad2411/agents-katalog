---
name: oxygen-recipes
description: Find and inspect a versioned OXYGEN business play, preflight its resources and adapt it to the reader's GTM goal.
---

# Choose a useful play

Read the user's goal and [first-batch guide](../../../docs/first-batch.md). A Recipe is an advisory playbook whose steps use native Tables, Workflows, Sequences and other primitives.

```sh
oxygen capabilities search "proven play for warm LinkedIn engagement" --json
oxygen commands get "recipes list" --json
oxygen commands get "recipes show" --json
```

List a bounded set by goal or lifecycle stage, read one selected Recipe and explain its prerequisites, input, output and limits. Use the reader's actual context; do not make a network motion the default for someone who has no relevant network or chose a different channel.

For a first LinkedIn motion, inspect the current `linkedin-network-first-motion` recipe if available. Distinguish captured events from coverage of the existing network, and make any standing auto-enrollment grant explicit.

If the Recipe includes a staged kit or Blueprint, inspect the current apply/preflight command. Preview the resources and cumulative forecast before installation. Reuse existing matching stages and record installed versions. Read the resulting resource states; installation does not authorize enabling, enrollment, sending or paid steps.

Use the selected play's actual dependency order and current command schemas. For this repo's functions, prefer [the existing installer](../../../docs/oxygen-setup.md) over creating duplicate equivalents.

Return the chosen play, rationale, prerequisites, installed objects if requested, and the next useful action. A recommended or installed Recipe is not a completed motion.

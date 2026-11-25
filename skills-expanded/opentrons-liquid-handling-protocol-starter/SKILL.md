# Opentrons Liquid-Handling Protocol Starter

Use this skill to generate a minimal Opentrons Protocol API transfer script and verify it through the local simulator.

## What it does

- Renders a small Protocol API 2.x script with one plate, one tiprack, one pipette, and one transfer step.
- Runs the generated script through `opentrons.simulate` to confirm the protocol is structurally valid.
- Returns a compact JSON summary with the rendered file path and the simulated command trace.

## When to use it

- You need a runnable starter for `Liquid-handling protocol generation`.
- You want a verified local protocol scaffold before touching a real OT-2 or Flex robot.

## Example

```bash
slurm/envs/automation/bin/python skills/robotics-lab-automation-and-scientific-instrumentation/opentrons-liquid-handling-protocol-starter/scripts/run_opentrons_liquid_handling_protocol.py \
  --protocol-out scratch/opentrons/toy_protocol.py \
  --out scratch/opentrons/toy_protocol_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/robotics-lab-automation-and-scientific-instrumentation/opentrons-liquid-handling-protocol-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_phase30_empty_domain_seed_skills -v`

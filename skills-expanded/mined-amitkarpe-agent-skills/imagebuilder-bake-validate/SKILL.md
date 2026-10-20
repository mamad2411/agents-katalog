---
name: imagebuilder-bake-validate
description: Run or watch an AWS Image Builder bake with durable polling, terminal-state evidence, and retained-builder debug handoff. Use when the repo already owns the lane-specific component, recipe, and validation policy and you need the reusable create-image/watch/failure-evidence operator workflow.
---

# Image Builder Bake Validate

Use this skill for the repeated operator workflow around AWS Image Builder.

## Use when

- starting an Image Builder image build and waiting for the terminal state
- resuming watch on an existing Image Builder image ARN
- capturing durable build evidence outside chat context
- locating the retained builder instance after a failed build
- handing off terminal build state to repo-native runtime validation

## Do not use when

- the real work is defining repo-specific component YAML, remediation vars, or
  ECS exceptions
- the task is publishing or versioning Image Builder components
- the task is launched-instance or SSM validation
- the flow is a runtime SSM document publish or apply problem
- the repo already has a better higher-level wrapper and you only need to run it

## Rules

- keep lane-specific recipes, components, validation command sets, and publish
  semantics in the real repo
- keep reusable operator mechanics here
- save evidence under `~/.AGENTS-temp/<repo>/...` when working in a repo, or
  use the skill default temp path for standalone runs
- prefer exact ARNs or explicit versions over `latest by name`
- if the infrastructure configuration retains failed builder instances, collect
  the instance ID immediately after a failure
- use the narrowest useful validation first, then expand into retained-instance
  SSM replay only when the component logs are not enough

## Main scripts

### Poll an Image Builder image to terminal state

```bash
bash scripts/poll-image.sh \
  --image-arn <image-build-version-arn> \
  --profile <aws-profile> \
  --region <region> \
  [--output-dir <outdir>] \
  [--poll-seconds 30] \
  [--timeout-seconds 7200]
```

This script writes:

- `image-arn.txt`
- `image.json`
- `status.txt`
- `status.log`
- `summary.json`
- `ami-id.txt` when available

It exits:

- `0` on `AVAILABLE`
- `1` on `FAILED` or `CANCELLED`
- `124` on timeout

### Find the retained builder instance for a failed or active image

```bash
bash scripts/find-retained-builder-instance.sh \
  --image-arn <image-build-version-arn> \
  --profile <aws-profile> \
  --region <region> \
  [--output-dir <outdir>]
```

This script writes:

- `instances.json`
- `latest-instance.json`
- `instance-id.txt` when a match exists

It prints the latest matching instance ID to stdout.

## Recommended workflow

1. Read the repo docs first and prefer a repo-native runner if one exists.
2. Register components or recipes with repo-native wrappers or
   `imagebuilder-component-publish` when needed.
3. Start the build and save the image ARN in a durable output dir.
4. Use `poll-image.sh` to wait for a terminal state with status-change logging.
5. On failure, use `find-retained-builder-instance.sh` and then inspect
   CloudWatch logs plus any repo-specific SSM replay commands.
6. Hand off launched-instance validation to repo-native validators or
   `ami-validation-ssm`.

## Related skills

- use `ami-validation-ssm` for launched-instance validation and failure capture
- use `imagebuilder-component-publish` for generic component register/version
  flows

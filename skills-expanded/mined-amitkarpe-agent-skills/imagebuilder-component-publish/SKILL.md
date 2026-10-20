---
name: imagebuilder-component-publish
description: Validate and publish an AWS Image Builder component version with durable evidence capture. Use when a repo owns the component YAML and you need the reusable check-or-create workflow instead of repo-specific registration glue.
---

# Image Builder Component Publish

Use this skill for the repeated component registration workflow around AWS Image
Builder.

## Use when

- checking whether a component version already exists
- parsing a component YAML file into a stable publish plan
- creating a new Image Builder component version with durable evidence
- replacing fragile repo-local register logic with a reusable check-or-create
  wrapper

## Do not use when

- the real work is editing the component YAML itself
- you need full image recipe creation or bake polling
- you only need a local syntax check without AWS context

## Rules

- keep component YAML in the real repo
- use `--check-only` first when introducing the skill to a new repo
- save outputs under `~/.AGENTS-temp/<repo>/...` when working in a repo
- treat existing component versions as a no-op success

## Main script

### Check or publish a component version

```bash
bash scripts/publish-component.sh \
  --component-file <component.yaml> \
  --version <semantic-version> \
  --profile <aws-profile> \
  --region <region> \
  --output-dir <outdir> \
  [--platform Linux] \
  [--check-only]
```

The script writes:

- `plan.json`
- `result.json`
- `component-name.txt`
- `component-arn.txt`
- `create-component.json` when a new version is created

It prints the component ARN to stdout on success, no-op, and `--check-only`.

## Recommended workflow

1. Run `--check-only` first in a new repo.
2. Confirm the parsed component name and computed ARN are correct.
3. Publish only after the component content is already validated locally.
4. Hand off recipe creation and bake polling to `imagebuilder-bake-validate`.

## Related skills

- use `imagebuilder-bake-validate` for image build and retained-builder
  workflows
- use `ami-validation-ssm` for runtime validation after an AMI exists

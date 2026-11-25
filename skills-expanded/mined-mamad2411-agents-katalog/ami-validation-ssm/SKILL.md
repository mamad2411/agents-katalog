---
name: ami-validation-ssm
description: Launch or reuse an EC2 instance for AMI validation, wait for EC2 and SSM readiness, run a repo-owned validation script through SSM, and save durable evidence. Use when the repo owns the validation checks and you need a reusable instance-plus-SSM harness instead of lane-specific bash.
---

# AMI Validation SSM

Use this skill for the repeated AMI validation harness around EC2 and SSM.

## Use when

- launching a temporary EC2 instance from an AMI for validation
- reusing a retained debug or builder instance for read-only validation replay
- waiting for EC2 checks and SSM readiness before running repo-owned checks
- saving durable validation evidence outside chat context

## Do not use when

- you are publishing or versioning an SSM document
- you only need generic EC2 creation without validation
- the real work is defining repo-specific validation commands or ECS exception
  policy

## Rules

- keep repo-specific validation scripts in the real repo or under
  `~/.AGENTS-temp/<repo>/`
- prefer read-only validation first
- default to terminating launched instances unless the workflow explicitly needs
  a retained debug host
- save outputs under `~/.AGENTS-temp/<repo>/...` when working inside a repo
- use `--instance-id` reuse mode for retained builder instances when narrowing a
  failing Image Builder step

## Main script

### Launch or reuse an instance and run validation

```bash
bash scripts/launch-and-validate.sh \
  --profile <aws-profile> \
  --region <region> \
  --output-dir <outdir> \
  --validation-script <script.sh> \
  [--ami-id <ami-id> | --instance-id <i-xxx>] \
  [--instance-type t3.large] \
  [--subnet-id <subnet-id>] \
  [--security-group-id <sg-id>] \
  [--instance-profile <profile-name>] \
  [--user-data-file <file>] \
  [--comment <text>] \
  [--keep-instance-on-exit true|false] \
  [--poll-seconds 30] \
  [--stall-seconds 600]
```

The script writes:

- `instance-id.txt`
- `instance-status.json`
- `ssm-instance-info.json`
- `send-command.json`
- `command-invocation.json`
- `summary.json`

On non-zero exits, it also keeps failure-oriented artifacts when the instance id
is known:

- `instance-description.json`
- `instance-status-final.json`
- `ssm-instance-info-final.json`
- `console-output.json`
- `console-output-tail.txt`

### Launch an instance only

```bash
bash scripts/launch-instance.sh \
  --ami-id <ami-id> \
  --profile <aws-profile> \
  --region <region> \
  --output-dir <outdir> \
  --instance-type <type> \
  --subnet-id <subnet-id> \
  --security-group-id <sg-id> \
  --instance-profile <profile-name> \
  [--user-data-file <file>] \
  [--tag-specifications '<spec>'] \
  [--block-device-mappings '<json>'] \
  [--prefix instance]
```

This script writes:

- `<prefix>-launch.json`
- `<prefix>-instance-id.txt`

It prints the launched instance id to stdout.

### Wait for EC2 instance health only

```bash
bash scripts/wait-for-instance-ok.sh \
  --instance-id <i-xxx> \
  --profile <aws-profile> \
  --region <region> \
  --output-dir <outdir> \
  [--prefix instance]
```

This script writes:

- `<prefix>-instance-status.json`

It exits:

- `0` on `running/ok/ok`
- `3` on stall

### Wait for SSM online only

```bash
bash scripts/wait-for-ssm-online.sh \
  --instance-id <i-xxx> \
  --profile <aws-profile> \
  --region <region> \
  --output-dir <outdir> \
  [--prefix instance]
```

This script writes:

- `<prefix>-ssm-instance-info.json`

It exits:

- `0` when SSM reaches `Online`
- `4` on stall

### Send an SSM command and wait for terminal status

```bash
bash scripts/send-command-and-wait.sh \
  --instance-id <i-xxx> \
  --profile <aws-profile> \
  --region <region> \
  --output-dir <outdir> \
  --comment <text> \
  [--prefix command] \
  [--commands-json '<json-array>' | --commands-file <json-file>]
```

This script writes:

- `<prefix>-send-command.json`
- `<prefix>-command-invocation.json`
- `<prefix>-command-id.txt`

It exits:

- `0` on success
- `5` on failed terminal command status
- `6` on stall

## Recommended workflow

1. Keep the validation logic in a repo-owned shell script.
2. Use `--instance-id` when replaying checks on a retained Image Builder host.
3. Use `--ami-id` for fresh candidate AMI validation.
4. Keep instances only when the failing result needs inspection.
5. Feed the resulting outputs back into repo-native publish or rollout steps.

## Related skills

- use `imagebuilder-bake-validate` for the Image Builder build and retained
  builder lookup workflow
- use `cis-ssm-apply-validate` for SSM document publish and apply workflows
- use `ec2-quick-create` only when you need disposable instance creation without
  a validation harness

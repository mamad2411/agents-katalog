---
name: ec2-quick-create
description: Create or delete AWS EC2 instances quickly with AWS CLI using SSM-first, private-by-default defaults, traceability tags, and short local records. Use when a temporary EC2 instance is needed for testing, validation, troubleshooting, or disposable dev work.
---

# EC2 Quick Create

Use this skill for fast EC2 launch and cleanup with local guardrails.

## Use when

- a temporary EC2 is needed quickly
- the user wants “use defaults” or “don’t ask” behavior
- the instance should be private-by-default and SSM-first
- you want short local records to avoid orphaned instances

## Do not use when

- the task requires modifying VPCs, subnets, security groups, or routes
- the instance lifecycle belongs in Terraform or Image Builder instead
- the environment needs a durable infrastructure definition rather than quick creation

## Mutable records

Do not write records into the skill folder.

Records live under:

```bash
~/.AGENTS-temp/agent-skills/ec2-quick-create/records/
```

Files:
- `active.tsv`
- `history.csv`

## Main scripts

### Create

```bash
bash scripts/ec2_quick_create.sh \
  --env <dev|prod|account_id> \
  --name <name> \
  --owner-tag <owner> \
  --purpose-tag <purpose> \
  [options]
```

Plan-only is the default. Add `--apply` to execute.

### Delete

```bash
bash scripts/ec2_quick_delete.sh \
  [--instance-ids <id1,id2>] \
  [--all-active] \
  [options]
```

Plan-only is the default. Add `--apply --confirm true` to execute.

## Guardrails

- private instance by default
- SSM-first access
- if `--public-ip true`, require explicit reconfirmation
- if `--env prod`, require explicit subnet and security group
- do not mutate surrounding network infrastructure

## References

- `references/defaults.md`
- `references/gcc-standard-images.md`

## Evidence

Keep execution outputs and extra notes under:

```bash
~/.AGENTS-temp/agent-skills/ec2-quick-create/
```

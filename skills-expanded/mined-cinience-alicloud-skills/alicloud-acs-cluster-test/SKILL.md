---
name: alicloud-acs-cluster-test
description: Offline smoke test for the ACS cluster lifecycle skill and its mutation previews.
---

# ACS cluster skill smoke test

## Offline checks

```bash
mkdir -p output/alicloud-acs-cluster-test
python3 tests/common/compile_skill_scripts.py \
  --skill-path skills/compute/acs/alicloud-acs-cluster \
  --output output/alicloud-acs-cluster-test/compile-check.json
python3 skills/compute/acs/alicloud-acs-cluster/scripts/acs_cluster.py create \
  --region cn-hangzhou --name codex-acs-sandbox \
  --vpc-id vpc-dryrun --vswitch-id vsw-a --vswitch-id vsw-b \
  --service-cidr 172.21.0.0/20 --snat --public-api \
  --enterprise-security-group --deletion-protection \
  --addon managed-coredns \
  --addon alb-ingress-controller --dry-run \
  --output output/alicloud-acs-cluster-test/create-preview.json
python3 skills/compute/acs/alicloud-acs-cluster/scripts/acs_cluster.py delete \
  --region cn-hangzhou --cluster-id c-dryrun \
  --confirm-cluster-id c-dryrun --delete-associated --dry-run \
  --output output/alicloud-acs-cluster-test/delete-preview.json
python3 skills/compute/acs/alicloud-acs-cluster/scripts/acs_cluster.py install-addon \
  --region cn-hangzhou --cluster-id c-dryrun \
  --addon-name managed-coredns --dry-run \
  --output output/alicloud-acs-cluster-test/addon-install-preview.json
python3 skills/compute/acs/alicloud-acs-cluster/scripts/acs_cluster.py uninstall-addon \
  --region cn-hangzhou --cluster-id c-dryrun \
  --confirm-cluster-id c-dryrun --addon-name managed-coredns \
  --confirm-addon managed-coredns --cleanup-cloud-resources --dry-run \
  --output output/alicloud-acs-cluster-test/addon-uninstall-preview.json
python3 scripts/quick_validate.py skills/compute/acs/alicloud-acs-cluster \
  > output/alicloud-acs-cluster-test/validation.txt
```

## Pass criteria

- Compilation and skill validation succeed.
- The create preview contains `profile=Acs`, two VSwitches, SNAT, public API access, enterprise security group, deletion protection, managed CoreDNS, and ALB ingress addons.
- The delete preview retains nothing by default when `--delete-associated` is explicitly selected and lists the documented associated-resource types.
- Addon install/uninstall previews contain no addon configuration and uninstall requires exact cluster and addon confirmations.
- No live API call is made and no credential is required.
- Evidence is saved under `output/alicloud-acs-cluster-test/`.

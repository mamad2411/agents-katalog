---
name: alicloud-acs-cluster
description: Create, inspect, connect to, inventory, and delete Alibaba Cloud Container Compute Service (ACS) clusters through the official CS OpenAPI. Use when Codex must bootstrap an ACS cluster from an existing VPC and VSwitches, obtain a short-lived KubeConfig, verify cluster readiness, inspect associated cloud resources, change deletion protection, or perform an explicitly confirmed full cluster teardown.
---

# Manage ACS clusters

Use the bundled OpenAPI client for the ACS cluster lifecycle. Use `$aliyun-vpc-manage` first when the VPC and VSwitches do not exist, and use `$alicloud-acs-agent-sandbox` after the cluster is ready.

## Workflow

1. Read [references/cluster-lifecycle.md](references/cluster-lifecycle.md) before creating or deleting a cluster.
2. Set `ALIBABACLOUD_ACCESS_KEY_ID`, `ALIBABACLOUD_ACCESS_KEY_SECRET`, and optionally `ALIBABACLOUD_SECURITY_TOKEN`. Set `ALIBABACLOUD_REGION_ID=cn-hangzhou` for Hangzhou.
3. Before creating the network, confirm that the Alibaba Cloud account has already authorized both CSI service roles:

   - `AliyunCSManagedCsiPluginRole` with `AliyunCSManagedCsiPluginRolePolicy`
   - `AliyunCSManagedCsiProvisionerRole` with `AliyunCSManagedCsiProvisionerRolePolicy`

   These are account-level, one-time authorizations. If the execution identity cannot call `ram:GetRole`, have the Alibaba Cloud account owner or a RAM administrator complete the official authorization pages. Container Service permissions alone cannot create these roles.
4. Install the official SDK:

```bash
python3 -m pip install "alibabacloud-cs20151215==7.0.4" "alibabacloud-tea-openapi"
```

5. Preview the exact create request without credentials or mutation:

```bash
python3 skills/compute/acs/alicloud-acs-cluster/scripts/acs_cluster.py create \
  --region cn-hangzhou \
  --name <cluster-name> \
  --vpc-id <vpc-id> \
  --vswitch-id <vswitch-a> \
  --vswitch-id <vswitch-b> \
  --service-cidr 172.21.0.0/20 \
  --snat --public-api --enterprise-security-group --deletion-protection \
  --addon managed-coredns \
  --addon alb-ingress-controller \
  --dry-run
```

   `--dry-run` is a local request-shape preview. It does not call Alibaba Cloud and therefore cannot validate service-role authorization, quota, capacity, or addon availability.
6. Run the same command without `--dry-run` after confirming the cost and public API exposure. Save the result under `output/alicloud-acs-cluster/`.
7. Require `state=running`, `profile=Acs`, the expected VPC/VSwitches, healthy virtual nodes, `managed-coredns` addon `active`, and a `kube-dns` Service before installing Agent Sandbox. Explicit addon lists can result in a cluster without CoreDNS; base Pods may run while Agent Identity storage later fails DNS.
8. Request a short-lived KubeConfig and protect it as a secret:

```bash
acs_kubeconfig_path="$(mktemp)"
python3 skills/compute/acs/alicloud-acs-cluster/scripts/acs_cluster.py kubeconfig \
  --region cn-hangzhou --cluster-id <cluster-id> \
  --temporary-minutes 60 --output "$acs_kubeconfig_path"
```

9. Before deletion, remove workloads and list associated resources. Delete only after exact cluster-ID confirmation.

Manage addons without exposing their configuration. `addon-status` omits the config because Manager configs can contain an admin API key. Supply install/modify config only through a mode `0600` file:

```bash
python3 skills/compute/acs/alicloud-acs-cluster/scripts/acs_cluster.py install-addon \
  --region cn-hangzhou --cluster-id <cluster-id> \
  --addon-name managed-coredns

python3 skills/compute/acs/alicloud-acs-cluster/scripts/acs_cluster.py addon-status \
  --region cn-hangzhou --cluster-id <cluster-id> \
  --addon-name managed-coredns
```

## Safety

- Never print, commit, or copy KubeConfig, AccessKeys, certificates, component API keys, or bearer tokens into evidence.
- Never use the unredacted all-addon version response as evidence: addon `config` can contain the Sandbox Manager admin API key. Use `addon-status`; use a protected `--config-file` for install/modify.
- Treat `--public-api` and `--snat` as chargeable network changes. Restrict API Server access according to the current official control-plane access guidance.
- Use at least two VSwitches in different zones for a non-disposable environment. Do not overlap VPC, VSwitch, Service, peer-VPC, or on-premises CIDRs.
- Keep deletion protection enabled during build and validation. Disable it only immediately before an approved teardown.
- Always run `resources --with-addon-resources` before cluster deletion. The delete API can retain ALB, SLS, PrivateZone, or other resources depending on their delete behavior.
- `delete --delete-associated` is destructive. It requires `--confirm-cluster-id` to exactly match `--cluster-id`; still verify the post-delete inventory and delete separately created VPC resources afterward.
- Do not assume an OpenAPI task response means completion. Poll the cluster state and verify the cloud resource inventory.
- Do not assume cluster `NotFound` means every ACS Pod ENI has already disappeared. Poll VPC network interfaces before deleting VSwitches; never force-delete an in-use primary ENI.

## Commands

```bash
# Safe inspection
python3 skills/compute/acs/alicloud-acs-cluster/scripts/acs_cluster.py describe \
  --region cn-hangzhou --cluster-id <cluster-id>

python3 skills/compute/acs/alicloud-acs-cluster/scripts/acs_cluster.py resources \
  --region cn-hangzhou --cluster-id <cluster-id> --with-addon-resources

# Destructive teardown after workload cleanup
python3 skills/compute/acs/alicloud-acs-cluster/scripts/acs_cluster.py disable-deletion-protection \
  --region cn-hangzhou --cluster-id <cluster-id> \
  --confirm-cluster-id <cluster-id>

python3 skills/compute/acs/alicloud-acs-cluster/scripts/acs_cluster.py delete \
  --region cn-hangzhou --cluster-id <cluster-id> \
  --confirm-cluster-id <cluster-id> --delete-associated
```

## Output And Evidence

Write sanitized request previews, cluster summaries, resource inventories, task IDs, and acceptance results under `output/alicloud-acs-cluster/<operation>/`. Store KubeConfig in a separate `mktemp` path with mode `0600`, exclude it from reports, and remove it after teardown.

## Sources

Use [references/sources.md](references/sources.md) to verify current API fields, supported regions, network constraints, and deletion behavior before a live run.

## Validation

```bash
python3 skills/compute/acs/alicloud-acs-cluster/scripts/acs_cluster.py --help
python3 scripts/quick_validate.py skills/compute/acs/alicloud-acs-cluster
```

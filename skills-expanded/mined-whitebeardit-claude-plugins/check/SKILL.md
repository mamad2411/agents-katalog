---
name: check
description: Checks what the AWS cost audit needs before it starts - AWS CLI v2, Python 3.8+, kubectl when there is EKS, valid credentials per profile, Cost Explorer enabled and readable in the payer, Savings Plans visibility, the read-only API families the scripts use, and the cluster metrics endpoint. Use right after installing the plugin, when an audit fails on access, or when the user asks what they need to set up. Read-only; changes nothing.
argument-hint: "[--profiles payer,member] [--region us-east-1] [--kube-context ctx]"
---

# Requirements check

Run the checker with the profiles from the plugin configuration (`${user_config.payer_profile}`,
`${user_config.member_profiles}`), the region (`${user_config.region}`) and, if set, the kubectl
context (`${user_config.kube_context}`). Arguments override the configuration.

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/check_requirements.sh" --profiles <payer>,<members> [--region <r>] [--kube-context <ctx>]
```

```powershell
& "$env:CLAUDE_PLUGIN_ROOT\scripts\check_requirements.ps1" -Profiles <payer>,<members> [-Region <r>] [-KubeContext <ctx>]
```

Show the user the PASS / WARN / FAIL lines as printed, then:

- For each **FAIL**, give the exact fix the line suggests (install AWS CLI v2, enable Cost Explorer
  in the payer, attach `ReadOnlyAccess` + `AWSBillingReadOnlyAccess`, activate IAM access to billing
  in the payer, log in with `aws sso login --profile …`).
- For each **WARN**, say which optional step it limits (hourly Cost Explorer granularity, Savings
  Plan utilization from a member account, no bash for the EKS snapshot script, no Prometheus/Mimir
  service found).
- Two findings worth reporting even when everything passes: Compute Optimizer **Inactive**
  (enabling it is a change, so only recommend it; it gives right-sizing recommendations at no cost)
  and NAT gateways in accounts the user did not expect.

With zero FAIL, say the audit can start and offer to run `/aws-cost-audit:audit`.

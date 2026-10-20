---
name: secure-cloud
description: Audit cloud account security posture — scan AWS, Azure, GCP (and Alibaba, Oracle, Cloudflare, Kubernetes) against CIS foundations and Mondoo cloud policies with cnspec, finding IAM, network, storage, encryption, and service misconfigurations mapped to compliance. Use to check a cloud account, subscription, project, or cluster's posture.
allowed-tools: Bash Read
---

# Secure Cloud

Check whether a cloud account is configured securely, by running
[cnspec](https://github.com/mondoohq/cnspec) against it. You ask the outcome — "is this AWS
account / Azure subscription / GCP project hardened?" — and this skill picks the right scan and
reads the result; cnspec carries the policies.

## When to use

- Auditing an AWS account, Azure subscription, GCP project, or Kubernetes cluster against CIS
  foundations / Mondoo cloud security policies.
- Finding IAM, network (security groups / firewall), public-storage, encryption, and logging
  misconfigurations across a cloud environment.

This is **live posture** (an account you can connect to). For the **Terraform/CloudFormation**
an agent writes *before* deploy, use `secure-pipeline` (it policy-checks the IaC with cnspec).

## What cnspec checks

- **AWS** — `mondoo-aws-security` · **Azure** — `mondoo-azure-security` · **GCP** — `mondoo-gcp-security`
- **Kubernetes** — `mondoo-kubernetes-security`, `mondoo-kubernetes-best-practices`
- **Also** — `mondoo-alibaba-security`, `mondoo-cloudflare-security`, `mondoo-clickhousecloud-security`

## Run a scan

```bash
cnspec scan aws    -o sarif    # uses your AWS credentials / profile
cnspec scan azure  -o sarif    # uses your Azure login
cnspec scan gcp    -o sarif    # uses your gcloud credentials
cnspec scan k8s    -o sarif    # current kube context
```

- Logged in to Mondoo Platform, cnspec runs the assigned policies automatically; otherwise add
  `--incognito` and `-f <bundle>` to run a specific bundle locally.
- Each provider authenticates with that cloud's standard credentials — see the
  [cnspec docs](https://mondoo.com/docs/cnspec/) for per-provider connection options.
- `-o sarif` emits findings for a CI gate; cnspec exits non-zero on failures.

## Reference, don't duplicate

cnspec owns the policies and their authoring (see the
[cnspec repo](https://github.com/mondoohq/cnspec/tree/main/skills) for the `mql` /
`policy-graph` skills). This skill invokes cnspec and interprets results.

## Compliance

Cloud policies map to CIS benchmarks, SOC 2, ISO 27001, PCI-DSS, NIST, HIPAA, and more — a scan
doubles as a compliance report; filter or report by the framework you need.

## Part of the secure-your-stack toolkit

`secure-cloud` is the **cloud account** pillar of posture, alongside `secure-os` (hosts &
devices), `secure-saas` (SaaS & identity), and `secure-ai-services` (AI). The secure development
skills secure the code and IaC you deploy into these accounts. Needs `cnspec`
([install](https://mondoo.com/docs/cnspec/install)) plus credentials for the target cloud.

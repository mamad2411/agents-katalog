---
name: gitlab-triage
description: Read-only GitLab connectivity triage for Route53, ELB chain, CloudOS DNS checks, and backend trace confirmation. Use when GitLab DNS or load-balancer routing is suspect, or when you need to prove whether gitlab.pro traffic reaches a specific backend.
---

# GitLab Triage

Use this skill for read-only GitLab DNS, LB, and backend-path verification.

## Use when

- GitLab hostname resolution is in doubt
- you need to verify Route53 records for GitLab
- you need to confirm whether `gitlab.pro...` goes through ELB or directly to an instance
- you need to prove whether a request reached a specific backend instance
- CloudOS product can reach GitLab web path but the exact backend path is unclear

## Do not use when

- you need to mutate Route53 or ELB membership
- you need to cut traffic over to a new backend
- you only need generic GitLab application logs

## Main scripts

### Search Route53 for GitLab records

```bash
bash scripts/check-route53-gitlab.sh \
  <profile> [output_dir]
```

This script:
- lists hosted zones
- dumps record sets
- extracts rows matching `gitlab` or `lifebit`

### Inspect classic ELB path for `gitlab`

```bash
bash scripts/check-gitlab-classic-elb.sh \
  <profile> <region> [output_dir]
```

This script:
- describes the classic ELB named `gitlab`
- shows backend instance membership and health

### Check GitLab DNS from CloudOS nodes

```bash
bash scripts/check-cloudos-gitlab-dns.sh \
  <profile> <region> <target_fqdn> <instance_id> [instance_id...]
```

This script runs from CloudOS nodes via SSM and shows:
- `getent hosts`
- `nslookup`
- `curl -skI`

### Confirm backend path with a trace request

```bash
bash scripts/trace-gitlab-backend.sh \
  <profile> <region> <cloudos_instance_id> <gitlab_backend_instance_id> [fqdn]
```

Default FQDN:

```bash
gitlab.pro.synapxe.lifebit-biotech.com
```

This script:
- sends a trace-tagged request from a CloudOS node
- checks GitLab access log on the target backend
- confirms whether that backend served the request

### Probe direct host health

```bash
bash scripts/probe-gitlab-host.sh \
  <profile> <region> <gitlab_instance_id> [output_dir]
```

This script checks:
- basic service state
- Docker status
- GitLab container state
- local `/-/health`
- local `/-/readiness`

## Investigation rules

- keep this skill read-only
- separate DNS truth from backend truth
- remember that ELB frontend IPs are not backend instance IPs
- prefer trace confirmation over inference when proving backend routing

## Recommended workflow

1. confirm Route53 truth
2. confirm ELB truth
3. confirm CloudOS-side DNS/HTTPS reachability
4. if backend identity matters, use trace confirmation
5. only then conclude whether GitLab host, DNS, or ELB is the real issue

## Evidence

Keep evidence outside the repo in:

```bash
~/.AGENTS-temp/agent-skills/gitlab-triage/
```

## Related skills

- use `ecs-monitoring` or `ecs-recovery` only if the problem is on ECS nodes
- keep ELB or Route53 mutation outside this skill

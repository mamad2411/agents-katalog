---
name: sandbox-egress-verifier
description: >-
  Verify AI-generated code executes only in an approved sandbox with no
  network egress, and probe the known bypass paths. Use when attesting a no-
  egress execution claim, choosing a code-execution runtime, or asked
  whether a sandbox actually contains model-authored code.
allowed-tools: Bash, Read
---

# Sandbox Egress Verifier

**Controls:** Control 2 — sandboxed no-egress runtime

## Confidence: PARTIAL — and this ceiling is not negotiable

You can prove a sandbox is **misconfigured**. You cannot prove the negative
"no covert channel exists". Network isolation has documented bypass paths, and
a verdict of PASS on this control would be a claim the evidence cannot support.

**Cap every verdict this skill produces at PARTIAL.**

## When to use this
When a deployment claims isolation. Run it knowing what it cannot do: absence
of a covert channel is not provable, DNS and object-storage bypasses are
documented, and the honest output is a capped PARTIAL rather than a pass.

## Procedure

1. **Identify the runtime and its network mode.** Record which isolation
   technology is in use and which mode it runs in. A mode that permits general
   outbound network access is an immediate FAIL — no probing required.

2. **Confirm the runtime is on the approved list.** An approved sandbox in the
   wrong mode and an unapproved sandbox in the right mode are both findings.

3. **Probe the known residual paths**, in an environment you own:
   - **DNS.** Name resolution is frequently permitted where general egress is
     not, and A/AAAA queries carry data outward. This has been demonstrated to
     yield interactive command-and-control on a major managed sandbox.
   - **Object storage reachability.** Managed storage endpoints are commonly
     left reachable and have been used as a command-and-control channel.
   - **Host escape.** Subprocess spawning and any path from the sandboxed
     process to the host.

4. **Record what you did not test.** A probe list is a statement about coverage,
   and coverage is the honest part of this verdict.

## Example

**Input** — the fixture committed at the top of [`scripts/sandbox_egress_verifier.py`](scripts/sandbox_egress_verifier.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
destination                           deny-list   allow-list  note
api.corp.example                      allow       allow       the one it actually needs
archive.evil.example                  block       block       B1.3's exfiltration target
attacker-bucket.s3.amazonaws.com      allow       block       a bucket anyone can create
169.254.169.254                       allow       block       cloud metadata - every credential
pastebin.example                      allow       block       not on anyone's deny-list

deny-list lets through : 3  ['attacker-bucket.s3.amazonaws.com', '169.254.169.254', 'pastebin.example']
```

The run continues past this. `test_skills.py` executes the script on every
build, **with no model configured** — so what CI proves is that it runs and
refuses legibly, not that it prints these lines. The output above is a recorded
run against a real model, and nothing re-diffs it: a model's answer is not
reproducible, and this repository does not claim otherwise anywhere it can be
checked.

## Output contract

```json
{
  "deployment_id": "str",
  "sandbox_runtime": "str",
  "network_mode": "str",
  "approved_runtime": true,
  "bypass_probes": [{"path": "dns|object_storage|host_escape", "reachable": false, "detail": "str"}],
  "untested_paths": ["str"],
  "verdict": "PARTIAL|FAIL",
  "verdict_ceiling_reason": "absence of a covert channel is not provable at runtime"
}
```

`PASS` is not a permitted value. If a tool emits one, that tool is wrong.

## Failure modes

- **Reporting PASS** because the configuration looked right. That is the whole
  reason this skill has a ceiling.
- **Probing only general HTTP egress.** DNS is the path that has actually been
  used.
- **Testing against someone else's infrastructure.** Probe only what you own.

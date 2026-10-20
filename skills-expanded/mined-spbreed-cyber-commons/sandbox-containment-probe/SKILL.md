---
name: sandbox-containment-probe
description: >-
  Execute the same code against an unsandboxed environment, a sandbox with
  production credentials mounted, and a contained one — then evaluate the
  network policies that separate them, connection by connection. Use when
  choosing or reviewing a runtime for agent-authored code.
allowed-tools: Read, Grep, Glob, Bash
---

# A sandbox with production credentials in it is a directory

"Sandboxed" is not a property a runtime has; it is a property of a specific
configuration, and the configuration that defeats it is common: the isolation
is real and the credentials were mounted in anyway. Probing all three
environments with one piece of code is what makes the difference visible.

## When to use this

Before choosing a runtime for model-authored code, and after any change to what
is mounted into it.

## Procedure

**1 — Write one probe and hold it fixed.** It should read the environment, walk
the filesystem, and attempt a connection. Varying the probe per environment
tests probes; varying the environment tests containment.

**2 — Run it unsandboxed and record the reach.** This is the baseline the
sandbox is being asked to reduce. It usually includes key material nobody
remembered was on that host.

**3 — Run it in the sandbox as actually configured.** Not the reference
configuration — the one in your manifest, with whatever is mounted. Credentials
and a route to production are the two things to look for.

**4 — Run it in the contained configuration** and record what is left. That
delta is the value of the control, and it is the number to put in the change
request.

**5 — Evaluate the network policy connection by connection.** For each
(source, destination, port) the workload might attempt, does a policy permit
it? Kubernetes NetworkPolicy is default-allow until a policy selects the pod,
so a namespace with no policy is not "no rules" — it is "all traffic".

## Example

**Input** — the fixture committed at the top of [`scripts/sandbox_containment_probe.py`](scripts/sandbox_containment_probe.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
no sandbox                      reached 8
      file:/etc/passwd
      file:/home/agent/.ssh/id_ed25519
      file:/home/agent/work/data.csv
      env:AWS_ACCESS_KEY_ID
      env:DATABASE_URL
      net:0.0.0.0/0
      net:169.254.169.254:80
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
  "probe": "str",
  "environments": [{"name": "unsandboxed|sandboxed|contained",
                    "filesystem": ["str"], "credentials": ["str"], "network": ["str"]}],
  "delta": {"removed": ["str"], "remaining": ["str"]},
  "network_policy": {"attempts": [{"from": "str", "to": "str", "port": 0, "permitted": false}],
                     "default_allow_namespaces": ["str"]}
}
```

## Failure modes

- **Testing the reference configuration.** Test the one in the manifest.
- **Calling isolation containment while credentials are mounted.** The process
  boundary did not stop being crossed by a file.
- **Reading a namespace with no NetworkPolicy as restricted.** It is
  unrestricted.

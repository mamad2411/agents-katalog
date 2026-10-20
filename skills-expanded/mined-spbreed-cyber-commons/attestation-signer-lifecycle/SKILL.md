---
name: attestation-signer-lifecycle
description: >-
  Bundle control evidence, compute verdicts, and produce a signed verifiable
  attestation for a deployment, re-attesting on drift. Use to emit or verify
  a control attestation, to sign evidence into an in-toto envelope, or to
  decide whether drift requires re-attestation.
allowed-tools: Bash, Read, Write
---

# Attestation Signer Lifecycle

**Controls:** All — the artifact

## Use the existing framework

Do not invent a format. Wrap the evidence in an **in-toto style statement**
inside a signed envelope, with the subject naming the deployment and its
digests, and a typed predicate carrying the control verdicts. Express the
predicate body in an assessment-results vocabulary so the verdicts map to
control catalogues and an auditor can consume them.

The roles are worth naming explicitly: this skill set is the **attester**
producing evidence, a separate service is the **verifier** appraising it
against reference values, and the deployment gate is the **relying party**
applying policy. Keep them separate — an attester that also decides whether it
passed is not an attestation.

## When to use this
Last, once every collector has run — and again on drift. Signing is a separate
skill and a separate role on purpose: an attester that also decides whether it
passed is not an attestation. Also use it to verify somebody else's envelope.

## Procedure

1. **Collect every sub-skill verdict.** A missing verdict is not a pass. If a
   skill did not run, the control is `UNKNOWN` and the attestation says so.
2. **Apply the confidence ceilings.** Sandbox-egress and injection-screening are
   capped at `PARTIAL` by their own skills; the signer must refuse to raise them.
3. **Resolve every evidence pointer.** A URI that does not resolve is a broken
   attestation, not a cosmetic issue.
4. **Attach framework mappings**, so one artefact answers several catalogues.
5. **Compute drift.** Compare image digest, configuration hashes and tool
   description hashes against the previous attestation. Any change triggers
   re-attestation — the tool-description hash specifically defends against a
   server mutating a tool after approval.
6. **Sign**, and store alongside the image or in a transparency log.

## Example

**Input** — the fixture committed at the top of [`scripts/attestation_signer_lifecycle.py`](scripts/attestation_signer_lifecycle.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
control    age (days)   point-in-time   continuous
----------------------------------------------------
AC-1                3            PASS         PASS
AC-2                9            PASS         PASS
SB-1               45            PASS        STALE
SB-2              210            PASS        STALE
EV-1                5            PASS         PASS
DR-1                0            FAIL         FAIL
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
  "subject": [{"name": "deployment_id", "digest": {"image": "sha256:…", "repo": "str"}}],
  "predicate_type": "str",
  "predicate": {
    "deployment_id": "str", "evaluated_at": "str", "evaluator_version": "str",
    "controls": [
      {"id": "C1_default_deny_least_privilege",
       "verdict": "PASS|FAIL|PARTIAL|UNKNOWN",
       "confidence": "HIGH|PARTIAL",
       "evidence": [{"skill": "str", "uri": "str", "hash": "str"}],
       "findings": ["str"]}
    ],
    "framework_mappings": {"owasp_llm": ["str"], "owasp_agentic": ["str"],
                           "atlas": ["str"], "nist_ai_rmf": ["str"], "iso_42001": ["str"]},
    "drift": {"since": "str", "changed": ["str"]}
  },
  "signatures": [{"keyid": "str", "sig": "str"}]
}
```

## Failure modes

- **Reading a missing attestation as a pass.** The relying party must **fail
  closed**: a signed file can be deleted, and absence is not evidence.
- **Raising a capped verdict** because the other evidence looked good.
- **Signing without resolving evidence pointers**, which produces a
  tamper-evident document full of dead links.
- **Attesting once.** Without drift-triggered re-attestation the artefact
  describes a deployment that may no longer exist.

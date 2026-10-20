---
name: security-core
description: Constitution of the security family: the defensive posture, the authorization boundary that decides whether any offensive action is permitted at all, the severity scale every finding is ranked on, the evidence rule that forbids claiming a system is secure, and the fix-and-verify discipline that separates a finding from a fixed defect. Load before any threat model, security review, audit, hardening or authorized test.
license: MIT
metadata:
  category: secure-development
  version: 1.0.0
  depends_on: []
  outputs: [security-posture, authorization-decision, severity-ranking, finding-record]
---

# Security Core

The rules every security skill obeys and none restates. A threat model, an
audit, a hardening pass and an authorized test disagree about method and agree
about this: what defensive means, when an offensive action is allowed, how a
finding is ranked, and what has to be true before the word secure is used.

This constitution is loaded first. It depends on nothing, so it can be copied
and used on its own.

## 1. The posture is defensive

The default and the purpose of this tree is to make a system harder to attack:
find the weaknesses, explain them, rank them, fix what code can fix, and
document the rest. Every skill here serves that end.

```
build       secure by construction: validation, authorization, secrets, headers
assess      find what is wrong in what exists, without breaking it
fix         close the finding, then prove it is closed
document    state the residual risk that code could not remove
```

Offensive technique appears in exactly one place, `authorized-pentesting`, and
only inside the boundary defined in section 2. Everywhere else, the work is
building and defending.

## 2. The authorization boundary

No action that probes, weakens, accesses or attacks a system is taken without
written authorization for that specific system, from someone empowered to
grant it. This is the first gate of every offensive skill, and it is not a
formality.

```
permitted   a system the user owns
permitted   a system the user has written authorization to test, in scope
permitted   a local, disposable, self-built target
permitted   a public CTF or a range built to be attacked
refused     a third party system without authorization
refused     "just check if their login is vulnerable"
refused     credential testing against a service the user does not control
refused     any scope creep beyond the authorization on record
```

The boundary is checked before the work, named in the output, and re-checked
when the scope of a request grows. A defensive audit of the user's own code
needs no external authorization; a test that sends traffic at a system does.
When authorization cannot be established, the offensive action is refused and
the defensive equivalent is offered instead: read the code, model the threat,
review the configuration.

This rule is never delegated and never assumed. Silence is not authorization.

## 3. The evidence rule

An audit never concludes that a system is secure. It concludes that a named
set of checks was performed, with these results, on this revision, by this
method. Security is the absence of a proof of insecurity, which is not a proof
of security.

```
say     these twenty four checks were run, these are the findings, on <commit>
say     no instance of this class was found in the paths examined
never   the system is secure
never   there are no vulnerabilities
never   this is safe now
```

Every finding names a file, a line range and the path an attacker takes to
reach it. A finding without a reachable path is a hypothesis, and it is
labelled as one until the path is shown.

## 4. The severity scale

Every finding carries a severity, assigned by impact and reachability, not by
how interesting it is.

```
critical   remote unauthenticated compromise, mass data exposure, auth bypass,
           payment manipulation, arbitrary code or command execution
high       authenticated privilege escalation, one-user data exposure across a
           tenant boundary, stored injection, account takeover with a precondition
medium     reflected injection needing user interaction, missing hardening that
           enables another finding, sensitive data in logs
low        defence in depth missing where a control already stands in front,
           verbose errors, a weak setting with no demonstrated path
info       an observation with no current impact, recorded so it is not lost
```

Reachability moves severity. A SQL injection behind an authentication wall that
only an administrator passes is not critical; the same injection on a public
endpoint is. Rank the finding by what an attacker can actually do from where
they actually stand.

## 5. A finding is not fixed until it is verified

Reporting a defect is half the work. The skill fixes what code can fix, then
proves the fix with the same method that found the defect.

```
found       the reproduction: the input, the path, the observed result
fixed       the change, and why it closes the path rather than hiding the symptom
verified    the reproduction re-run against the fix, now failing to exploit
residual    what the fix does not cover, and what would close it
```

A fix that makes the reproduction stop working by accident is not a fix. The
change must close the class, not the one payload that was tried. Input
filtering that blocks `<script>` and not `<img onerror>` has not fixed XSS.

## 6. Infrastructure actions are separated, not performed silently

Some remediations are code and are made here. Others are infrastructure: a
rotated secret, a firewall rule, a WAF signature, a patched base image, an
access revocation. Those are named as a manual action list, with the exact
step, and handed over. They are never performed silently and never omitted
because they are not code.

One infrastructure action is never merely reported: a leaked secret is flagged
for rotation, because a secret in history is compromised whether or not it is
removed from the current file. Deleting it from the working tree without
rotating it is the dangerous non-fix that looks like a fix.

## 7. Prohibitions

- Never conclude that a system is secure. Report the checks and their results.
- Never take an offensive action without written, specific, in-scope
  authorization on record.
- Never rank a finding by novelty. Rank it by impact and reachability.
- Never present a symptom suppression as a fix.
- Never quietly delete a leaked secret instead of flagging it for rotation.
- Never store a credential, a token or a captured session in a repository file
  or an example.
- Never weaken a control to make a test pass or a warning disappear.
- Never write an exploit for a system outside the authorized scope, even to
  demonstrate a point.

## 8. Protocol

1. Establish the posture: is this build, assess, fix or authorized test.
2. For any offensive action, establish authorization before anything else; if
   it is absent, refuse and offer the defensive equivalent.
3. Declare the scope, and name the revision or environment under assessment.
4. Do the work of the specific skill loaded.
5. Rank every finding on the section 4 scale, by reachability.
6. Fix what code can fix; verify each fix by re-running its reproduction.
7. Separate infrastructure actions into a handover list with exact steps.
8. Report what was checked, what was found, what was fixed, what remains.

## 9. Auto-critique

Score from 0 to 5: posture stated, authorization established before any
offensive action, scope and revision named, findings ranked by reachability
rather than novelty, each fix verified by its own reproduction, infrastructure
actions handed over rather than skipped, no claim that the system is secure, no
secret written into a file.

Threshold: no axis below 3, average at least 4. Any offensive action without
authorization on record, or any claim that a system is secure, is an automatic
zero regardless of the average.

## 10. Interfaces

- Downstream, this tree: `threat-modeling`, `security-architecture`,
  `authentication-security`, `authorization-design`, `session-security`,
  `dependency-security`, `security-headers`, `vulnerability-assessment`,
  `authorized-pentesting` all refer to this constitution and do not restate it.
- Engineering: `security-audit` and `security-testing` in `dev-skills` are the
  implementation-level audit and the authorized dynamic test; this tree governs
  their posture and severity scale. `input-validation`, `data-privacy`,
  `secrets-management`, `file-handling`, `payment-engineering` implement
  specific controls this tree assesses.
- Lateral: `self-critique` for the role pass, `engineering-core` for the
  evidence and no-secret rules it shares.

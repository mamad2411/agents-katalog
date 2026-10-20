---
name: client-handover
description: Produces the delivery package a client or another team can actually take over: overview, features as built, architecture, stack, installation, configuration, operations, administration, known limitations, follow ups and support boundaries, with no secret and no unverified instruction.
license: MIT
metadata:
  category: delivery-skills
  version: 1.0.0
  depends_on: [engineering-core, technical-documentation, project-continuity]
  outputs: [handover-package, operations-guide, limitations-register, follow-up-list]
---

# Client Handover

The test of a delivery is whether someone who was not there can install it,
run it, operate it and change it.

`project-continuity` addresses the next engineer mid project.
`technical-documentation` addresses whoever reads the docs.
This skill addresses the person who now owns the system.

## 1. Audience

Two readers, different needs, and a package that serves both without mixing
them.

| Reader | Needs | Does not need |
|---|---|---|
| the client or product owner | what it does, what it costs, what it cannot do, who to call | module boundaries |
| the maintaining engineer | how to run it, how it is built, where the decisions are | a feature tour |

Write two sections rather than one document that alternates between them.

## 2. Contents

Only what applies. A handover for an internal tool and one for a client owned
platform are different documents.

```
1  Overview          what the system does, in the reader's language
2  Features          as built, not as specified, with what each does
3  Architecture      the shape, linking to the architecture document
4  Stack             what it is built on, and why, linking to the decisions
5  Installation      from nothing to running, every step verified
6  Configuration     every environment variable, its purpose, where it comes
                     from, never its value
7  Development       how to work on it, run tests, add a feature
8  Testing           what is covered, what is not, how to run it
9  Deployment        how a change reaches production, and how to undo it
10 Operations        the runbook: what breaks, how to tell, what to do
11 Administration    how to perform the privileged tasks the product needs
12 Limitations       what it does not do, and what it does badly
13 Follow ups        the register, with recommendations
14 Support           what is covered, for how long, how to reach whom
```

## 3. Features as built

The feature list describes what exists at handover, not what the
specification asked for. Where the two differ, the difference is stated.

```
| Feature | State | Notes |
|---|---|---|
| Course publication | complete | direct publication, no review step, per A6 |
| Attestation | complete | PDF, downloadable; email delivery not configured, S1 |
| Completion tracking | complete | |
| Multi organisation | not built | out of scope, see the scope section |
```

A feature list that silently matches the original specification, when the
delivery diverged, is the most damaging document in the package: it is the one
the client will quote back.

## 4. Installation, verified

Every step is executed on a clean state before it is written. Not remembered,
not adapted from another project.

```
Prerequisites    with versions
Obtain the code  the exact command
Install          the exact command
Configure        which variables, where the values come from
Database         create, migrate, seed
Run              the command, and what a healthy start looks like
Verify           an action that proves it works, with the expected result
```

The verification step is what separates a setup guide from a list of hopes. It
tells the reader whether they succeeded.

## 5. Operations runbook

Written for someone under pressure. Imperative, short, no prose.

Per failure mode:

```
Presents as   what the operator or user observes
Confirm       the exact check
Act           numbered steps
Afterwards    what to verify
Escalate      when, and to whom
```

Include at minimum: the application does not start, the database is
unreachable, an external provider is failing, disk or quota exhaustion, a
deployment must be rolled back, and any failure mode the project's own
architecture identified as likely.

## 6. Limitations, stated plainly

The section clients value most and that gets softened most.

```
| Limitation | Consequence | Trigger to address |
|---|---|---|
| No pagination on the course list | slow above roughly 500 courses | when the catalogue passes 300 |
| Attestation emails not configured | trainees download, no email | when the provider account exists |
| Single organisation | a second client needs a second deployment | if multi tenancy is wanted |
| French only | no other locale can be served | before a non French cohort |
| No automated backup verification | a restore has never been tested | before the system holds unique data |
```

Every line names a consequence and a trigger. A limitation without a trigger
reads as an apology; with one it reads as a plan.

## 7. Secret handling

Never in the package: passwords, tokens, API keys, private keys, connection
strings with credentials, personal data of real users, screenshots showing any
of these.

Instead, per secret:

```
Name          the variable
Purpose       what it enables
Source        which console or vault issues it
Required      yes or no, and what happens when it is absent
Format        the shape, not a value
Rotation      how to rotate it, and what must be restarted
```

Where the delivery includes handing over credentials, they travel through the
client's own secret channel, never in the repository, the documentation or a
message thread.

## 8. Verification before delivery

The handover is tested like code.

```
Installation    followed on a clean machine, from the written steps only
Commands        every one executed, output matching what is documented
Variables       every documented one exists in the code, every one the code
                reads is documented
Runbook         each procedure walked through, at least mentally, against the
                real system
Features        the table matches what the running system does
Limitations     nothing known is missing from the list
Secrets         a search of the package finds none
Links           every path and reference resolves
```

## 9. Protocol

1. Determine which of the fourteen sections apply.
2. Write the two audiences separately, section 1.
3. Build the feature table from the running system, not from the
   specification.
4. Execute the installation on a clean state and write what actually happened.
5. Write the runbook per failure mode, imperative.
6. Assemble the limitations register from the stub register, the follow up
   register and the risk register.
7. Document every variable, no values.
8. Run the verification of section 8.
9. Deliver, and state what support covers.

## 10. Auto-critique

Score from 0 to 5: both audiences served, features described as built,
installation verified on a clean state, runbook usable under pressure,
limitations honest with triggers, variables complete in both directions, no
secret, every command executed.

Threshold: no axis below 3, average at least 4. A feature table that
contradicts the running system is an automatic failure, as is any secret in
the package.

## 11. Interfaces

- Upstream: `technical-documentation`, `project-continuity`,
  `implementation-integrity` for the stub register,
  `scope-and-change-control` for the follow up register.
- Lateral: `deployment-engineering` and `observability` for the runbook,
  `environment-management` for the variable inventory.
- Downstream: `release-readiness`, which checks the package exists and is
  verified.

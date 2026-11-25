---
name: whitebox
description: >
  Test a target with the source code, the configuration, the infrastructure definitions and
  the build pipeline in hand, alongside the running system. Use when someone says white box,
  whitebox, crystal box, "we can give you the repo", "source-assisted", "code review plus
  pentest", "secure code review", "audit our codebase", or /redteam:whitebox. This is the
  only level at which it is honest to say an application is secure rather than saying you
  could not get in.
---

# Testing with full access

You have the source code, the configuration, the infrastructure definitions and the build
pipeline, as well as test logins and the running system.

This is the only level where you can say the application is secure. Anything less lets you
say only that you did not get in during the time available.

Read `../pentest/SKILL.md` first if the engagement has not been scoped. Permission still
comes before traffic, and having the source is not permission to attack the live system.

## The one rule that makes this work

Read the code and test the running system at the same time, from day one. Not code review
followed by testing, and not testing followed by a look at the code.

They feed each other. Reading the permission checks tells you which addresses to attack.
Attacking tells you whether the worrying code can actually be reached. A finding confirmed
in both places is one you can prove and the client can fix.

## What to ask for

- Every repository involved, and the exact commit to review, so the report is anchored to a
  version
- The configuration for the environment being tested, with secrets removed but with the
  names and structure intact
- The infrastructure definitions
- Access to the build pipeline configuration, and the list of who can push to the main branch
- The database structure
- Test logins as described in `../greybox/SKILL.md`, because you still need to test the
  running system

If secrets are handed over by mistake, say so immediately, do not use them beyond noting the
exposure, and tell the client to revoke them.

## The order of work

1. `../pentest/phases/00-permission-and-scope.md`
2. `../pentest/phases/03-mapping.md`, in parallel with the repository intake below
3. `../pentest/phases/06-code-review.md`, which is the main body of this level
4. `../pentest/phases/04-automated-checks.md` and
   `../pentest/phases/05-manual-testing.md`, pointed by what the code review found
5. `../pentest/phases/07-proving-impact.md` onwards

## Repository intake, in order

**Read the front door first.** Find how a request travels from arriving to being handled:
the routing, the layers that run before the handler, and where login and permission checks
sit. Until you know that, you cannot tell a protected handler from an unprotected one, and
every later judgement will be wrong.

**Then the fastest high-value trick in the job.** Find the function, decorator or annotation
that performs the permission check. List every handler that uses it. List every handler.
The difference is your list of unprotected addresses. Take that list straight into the
running system and try each one as a low-privilege user. This finds the missing check on
handler forty-seven of sixty, which is close to impossible to find reliably by clicking.

**Then read, in this order:** login and session handling, token creation and verification,
every database query built from text instead of parameters, anywhere data from a user is
turned back into an object, encryption and randomness, anywhere a file path is built from
user input, anywhere a template is rendered from user input, and every remaining point where
outside data crosses into trusted code.

**Encryption and randomness deserve their own pass.** Look for encryption written by hand,
an outdated mode, a fixed initialisation value, a weak method of turning a password into a
key, and a general-purpose random number generator used for anything security-related such
as a token, a reset link or a one-time code. None of these are visible from outside, which
is why this level exists.

**Dependencies.** The full tree, not just what the developers chose directly. Known
weaknesses, unmaintained packages, and names that look like typing mistakes of real
packages. Then ask whether the affected code is actually called. Use `../cve/SKILL.md` for
that work, because reachability is what turns a list of numbers into a finding.

**Secrets across the whole history.** A key removed in a later change is still in the
history and still works until somebody revokes it. In the finding, say revoke, not delete.

**Infrastructure and pipeline.** Cloud resources defined as code, container settings,
who can push to the main branch, whether a proposed change from an outsider can run with
access to secrets, whether build steps are pinned, and where the pipeline's own credentials
live. A weak pipeline is a route into everything the pipeline can reach, which is usually
the live system.

## Proving coverage

Work through a published verification standard requirement by requirement and record each
one as met, not met, or not applicable. `../../references/standards.md` says which standard
to use and how to pick the level. Agree the level with the client during scoping, not at the
end.

This is what turns a review from a hunt into something another person can check.

## Findings at this level

Two things change in how you write them up.

**Point at the file and the line**, and say which commit. A finding a developer can open in
their editor gets fixed the same week.

**Report causes, not counts.** When the same mistake appears in eight files, that is one
finding about how the application is built, not eight findings. Something like "permission
checks are written into each handler rather than applied in one place, so they will keep
going missing" is worth more to the client than the eight line numbers, and it is only
visible from the code. Put three or four of these at the front of the recommendations.

## What to record

- The repositories and the exact commit reviewed
- Findings with file and line
- Which findings you then confirmed against the running system, and which you could not
- Requirement-by-requirement coverage
- Causes, gathered separately from the finding list

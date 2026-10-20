---
name: repository-onboarding
description: >-
  Set up or repair Paved in a repository by preparing its project context, adapters and verification profile. Use when the user asks to initialize or onboard Paved, or Paved reports incomplete setup.
---

# Repository onboarding

## When to use

- A human asks to add Paved to a repository, and `paved init` is unavailable or failed.
- `.paved/` exists but is missing its manifest or verification profile.

Do not use it to regenerate existing Project Context; that is the generators' job.

## Required context

None from Paved: there is no Project Context yet. The inputs are the repository's own
files. Everything you learn is a proposal until a human confirms it.

## Preconditions

- A human asked for onboarding. Never create `.paved/` on your own initiative.
- The working tree is clean, so the onboarding changes can be reviewed as one diff.

## Procedure

1. **Discover the repository.** Activate `context-discovery` and build the repository
   overview it describes. Nothing is written yet.
2. **Detect technologies.** Match build and configuration files against each available
   adapter's `detect` signals. List the matches with the files that triggered them.
3. **Resolve adapters.** Propose the matching adapters and a Core version range; a human
   confirms the list. An unmatched technology is recorded as unknown, not guessed.
4. **Create the manifest.** Write `.paved/manifest.yaml` from `templates/manifest.yaml`.
   Create only paths listed in the consumer layout of the Core `manifest.yaml`.
5. **Draft Project Context.** Run the generators if they are available. Otherwise create
   feature-map entries only for features a human names, marked `declared`.
6. **Discover verification.** For each check type, look for the command the repository
   already uses (build files, CI configuration, contributor documentation). Add it to
   `.paved/verification/profile.yaml` only after running it once successfully. Record the
   check types the repository lacks under `unavailable`, with the reason.
7. **Connect agents.** Add the Paved block to the root `AGENTS.md` from
   `templates/AGENTS.md`. If the file exists, add the block and change nothing else.
8. **Validate.** Validate every created document against its schema and fix what fails.
9. Summarize what was created, what was proposed and what is unknown.

## Tools

`core.repository.status` before starting (clean tree) and after (only `.paved/` and `AGENTS.md`
changed).

## Rules

`core.quality.unknowns-stay-unknown` is the main risk: onboarding tempts you to describe
the project. Write down only what you read in files or observed when running a command.

## Verification

Schema validation of every created document (`static-analysis`); one recorded run of each
command added to the profile.

## Evidence

The onboarding diff and one check result per profile check.

## Completion criteria

- Manifest and verification profile exist and validate.
- Every profile check has run at least once, with its result in the evidence.
- A human has confirmed the adapter list, or it is empty.

## Failure modes

| Failure | Signal | Response |
|---|---|---|
| Guessed execution | A Check's Tool capability has no resolved implementation | Resolve the binding or record the check as blocked |
| Invented context | Context describes behavior not seen in code | Delete the claims; record unknowns |
| Clobbered entry file | Diff shows changes outside the Paved block | Revert those lines |
| Adapter chosen by name alone | A technology is assumed from a directory name | Require a `detect` signal or a human decision |

## References

None. The consumer layout is in the Core `manifest.yaml` (`consumer_layout`).

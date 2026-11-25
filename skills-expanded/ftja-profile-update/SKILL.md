---
name: ftja-profile-update
description: Update the profile summary from registered source files.
version: 0.1.0
author: Taegyujeong, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [profile, resume, portfolio, job-search]
    related_skills: [ftja-setup, ftja-tune]
---

# FTJA Profile Update Skill

Use this skill when the user invokes `/ftja-profile-update` after adding,
removing, or changing a CV, portfolio, or other registered profile source.
It updates `profile/summary.md`, not the job judgment rubric. Never write
until the user has reviewed and confirmed the proposed change.

## When to use

- The user runs `/ftja-profile-update`.
- A registered CV, portfolio, or other source has changed.
- The user wants the profile summary refreshed.

Do not use this for job preferences, dealbreakers, search keywords, or
exclusion rules; use `/ftja-tune` for those.

## Procedure

1. Read `profile/sources.json` if it exists. If it does not exist, inspect
   the files currently in `profile/` and ask which ones should be registered.
2. Check every registered source path. Report missing or unreadable files and
   do not silently remove them from the registry.
3. Read the current `profile/summary.md` and every enabled, available source.
   Use the document/PDF reading tools available in the current environment;
   do not invent facts that are not supported by a source.
4. Decide the smallest correct update:
   - edit an existing summary statement;
   - add a new achievement, role, skill, or project;
   - remove a statement no longer supported by the sources; or
   - propose a complete rewrite only when the source material changed broadly.
5. Show a concise diff grouped as Added, Updated, and Removed. Include a
   short note when a source is missing or a claim is ambiguous.
6. Ask for explicit confirmation. Do not write `profile/summary.md` yet.
7. After confirmation, update only `profile/summary.md`, keep it concise for
   repeated Stage 2 reads, and report the exact path and changed sections.
8. If the source change also suggests a new job preference or dealbreaker,
   mention it separately and ask the user to run `/ftja-tune`; do not modify
   `rubric.md` or `criteria.json` in this skill.

## Verification

Before reporting success, re-read `profile/summary.md` and verify that every
new claim is supported by an enabled source. Confirm that source files were
not modified and that only the summary was written.

## Pitfalls

- Do not delete source files when a user removes them from the registry.
- Do not treat an outdated summary statement as false without checking the
  current source material.
- Do not infer job preferences from a career fact.
- Do not claim the profile was updated before the user confirms the diff.

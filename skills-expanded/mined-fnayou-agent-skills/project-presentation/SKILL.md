---
name: project-presentation
description: Audit, bootstrap, or align a repository's visual identity and public documentation site. Use when a project needs a logo, README banner, social preview, color palette, generated SVG brand assets, a brand freshness check, a Zensical documentation site, or GitHub Pages deployment. Reads the repository's existing choices first and asks only about what is missing or in conflict.
---

# Project Presentation

Give a repository a coherent, reviewable visual identity. The work has
independent tracks; use only the one the request names.

| Track | Use it to | Reference |
|---|---|---|
| Brand | Define palette, accent, logo, banners, favicon, and generated SVG assets | [brand track](references/brand-track.md) |
| Documentation | Build or align the public site in `website/` and its Pages deployment | [documentation track](references/docs-track.md) |

Read the track reference before the first change. Do not load a track the
request does not need.

## Inspect before asking

Before proposing anything, read what the repository already decided:

1. Repository instructions, README, and any existing `brand/` or image
   directory.
2. Existing palette, accent, logo, and tagline, wherever they live.
3. Product facts the artwork may state, from code, configuration, or
   documentation.
4. Task runner and CI configuration, to place checks where the project already
   runs them.

Classify the repository as **new** (no identity), **partial** (some assets or
choices), or **established** (a coherent identity). Preserve every sound
existing decision. Ask the operator once, in one message, only about a choice
that is missing or that two sources contradict. Never ask about something the
repository already answers.

## Rules for every track

- Keep this skill generic. Never write a project name, accent mapping, or
  product claim into it. Record project-specific choices in the target
  repository.
- State only facts the repository supports. A claim in artwork or text must
  trace to a file, a setting, or a test in the repository. Mark planned
  capabilities as planned, or leave them out.
- Make generated output deterministic and reviewable: same inputs, same bytes.
- Run the project's own checks after a change and report their result. Do not
  claim success from a file that was written but not checked.
- Work only in the target repository. Do not install tools, change
  repository settings, or publish anything without explicit operator
  approval.

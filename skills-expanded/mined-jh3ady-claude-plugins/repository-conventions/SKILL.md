---
name: repository-conventions
description: This skill should be used whenever scaffolding a new repository, open-sourcing or publishing a project, creating, writing, or reviewing its standard and community health files (README, LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, issue and pull request templates, CHANGELOG, FUNDING.yml, CODEOWNERS, AGENTS.md, CLAUDE.md), or auditing which of them a project has, even when conventions are not explicitly mentioned.
---

# Repository conventions

A reusable standard for the files a repository is expected to carry:
README, license, contributing guide, community health files, and AI agent instruction files. Apply it by default, for
private repositories as well as public ones. This skill is the baseline standard, not an opinionated ruleset: it
reflects what the majority of popular repositories converge on, and the maintainers' own style always prevails (see
"Maintainer style prevails" below).

## The baseline file set

| File                      | Conventional location              | Baseline convention                                          |
|---------------------------|------------------------------------|--------------------------------------------------------------|
| `README.md`               | root                               | Short, pointer-style; license mentioned last                 |
| `LICENSE`                 | root                               | Bare filename, single license text, nothing appended         |
| `CONTRIBUTING.md`         | root (or `.github/`)               | Full guide while small, pointer once docs grow               |
| `CODE_OF_CONDUCT.md`      | root or `.github/`                 | Often a short stub delegating to a canonical text            |
| `SECURITY.md`             | root or `.github/`                 | How to report a vulnerability privately                      |
| Issue templates           | `.github/ISSUE_TEMPLATE/`          | YAML forms plus a `config.yml`                               |
| PR template               | `.github/PULL_REQUEST_TEMPLATE.md` | Under `.github/` by convention, not at root                  |
| `FUNDING.yml`             | `.github/`                         | Only for donation-funded projects                            |
| `CODEOWNERS`              | `.github/`                         | Review routing; optional                                     |
| `CHANGELOG.md`            | root                               | Optional; releases or a docs site are the common alternative |
| `AGENTS.md` / `CLAUDE.md` | root                               | `AGENTS.md` canonical, `CLAUDE.md` imports it                |

Not every repository needs every file. Match the set to the project's size and audience: a small private repository is
well served by a README, a license, and an agent instruction file; templates, security policy, and code of conduct earn
their place as the audience grows.

## README

The dominant shape is short (under roughly 700 words) and pointer-style:
it orients the reader and delegates substance to the documentation, the contributing guide, and the other standard
files. The canonical section order:

1. Project name, as a plain heading or a centered logo (with dark and light variants via `<picture>` when a logo
   exists).
2. A few badges (package version, build status, license, community chat). Two to five is typical; zero is a legitimate
   minimalist style.
3. A one-sentence description of what the project is.
4. Optional feature bullets with a bold lead word.
5. Installation or getting started, kept to the shortest working path.
6. Links out: documentation, community, support.
7. A short contributing pointer to `CONTRIBUTING.md`.
8. License, as the final section, one line linking the license file.

A long README is justified only when it plays another role: the documentation homepage, the build-from-source guide, or
a governance registry. Screenshots belong to end-user applications; libraries show code instead.

Default tone is neutral and factual: declarative sentences, no unverifiable hyperbole, second person only for
instructions. Product-like taglines are common for frameworks and tools; humor and marketing flair are deliberate
identity choices that belong to the maintainers, not to a default.

## LICENSE

Keep the license in a bare `LICENSE` file at root containing a single, unmodified license text. Appending third-party
notices to it breaks automatic license detection (SPDX); put bundled-dependency notices in a separate file. Choose the
license deliberately; permissive licenses dominate popular repositories, but the choice belongs to the project.

## CONTRIBUTING

Two archetypes exist, both legitimate:

- A self-contained guide covering development setup, how to run the tests, and the pull request process. The right
  default while the project is small.
- A short pointer file delegating to a docs site or a dedicated guide. The pattern large ecosystems converge on.

Legal gatekeeping (CLA, DCO) correlates with governance; add it only when the project's stewardship requires it.

## Community health files under `.github/`

Issue templates are YAML forms (`.yml`) with a `config.yml` that routes questions and support to discussions, chat, or a
forum; numeric filename prefixes control chooser order. The pull request template always lives under `.github/`.
`FUNDING.yml` signals a donation-funded project.
`SECURITY.md` states where to report vulnerabilities privately (the platform's private reporting is the accessible
default). Organizations can host defaults for all their repositories in a shared `.github`
repository, so a file's absence from one repository is not always a gap.

## AI agent instruction files

Maintain exactly one canonical instruction file, so the copies cannot drift apart over time. `AGENTS.md` is the
cross-tool standard name and the default canonical file. Point the other names at it instead of copying it:

- `CLAUDE.md`: Claude Code reads `CLAUDE.md`, not `AGENTS.md`. Make `CLAUDE.md` a file containing `@AGENTS.md`; Claude
  Code expands the import at session start, and Claude-specific instructions can follow the import. Prefer the import
  over a symlink: creating a symlink on Windows requires Administrator privileges or Developer Mode.
- Other tools that read only their own filename: use the tool's import mechanism when it has one, otherwise a symlink.

A project already centered on one tool may keep that tool's name canonical and point the rest at it.

Effective content, in order of value: build and test commands with the project's traps and gotchas, a directory map,
rules about generated files, commit and pull request conventions, and pointers to deeper documents rather than inlined
detail. Keep it in the low hundreds of lines.

## Maintainer style prevails

The baseline above is the majority pattern, not a law. Well-known projects deviate deliberately and successfully: a
README written entirely in a humorous voice, a README that doubles as a marketing page with testimonials, a README that
serves as a governance registry. When a repository already has an established voice or layout, match it instead of
normalizing it, and when maintainers state a preference, their preference wins over anything in this skill.

## Adapt to your context

This skill stays generic on purpose. Layer your own conventions on top:

- Default license, attribution policy, badge set, and tone are project or team decisions; declare them in your own
  `CLAUDE.md` or a higher-priority skill. This skill does not impose them.
- Ecosystems carry their own conventions (dual licensing, governance files, citation files); follow the ecosystem when
  it has one.

## Reference

For the survey behind this baseline (adoption rates, file locations, tone registers, and notable outliers across popular
repositories), read
`references/conventions.md`.

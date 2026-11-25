---
name: readme
description: Reference for writing, updating, and reviewing project and package READMEs, drawing on Standard Readme, Google's README guidance, and GitHub documentation. Use when deciding README content or structure, improving getting-started instructions, or checking a README against the project it describes.
---

# README

A README helps a new reader understand what a project does, decide whether it fits their needs, and take the first useful step. Keep it an entry point to the project's documentation.

These conventions draw on [Standard Readme](https://github.com/RichardLitt/standard-readme/blob/main/spec.md), [Google's README guidance](https://google.github.io/styleguide/docguide/READMEs.html), and [GitHub's README documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes). The verification guidance below is an additional practice for agent-authored documentation.

## Conventions and standards

Use `README.md` for a new Markdown README unless the project specifies another format. GitHub Flavored Markdown defines formatting, not which information a README must contain.

Use Standard Readme as a structural reference by default. Claim compliance only when requested or already required by the project, and then consult the specification for its required sections, exact headings, ordering, and other constraints. The adaptable structure below does not itself guarantee compliance.

Follow the repository's documentation conventions and intended audience. Preserve deliberate omissions and useful existing content. A small correction does not require restructuring the whole file.

## Audience and scope

Identify the reader and their first useful outcome before choosing sections:

- A library user needs installation and a working import and call.
- A CLI user needs installation and a representative command with its result.
- An application contributor needs local setup and a way to confirm the app runs.
- A service operator may need configuration and deployment documentation links.
- A documentation or collection repository may need browsing and selection guidance instead of executable setup.

For package or directory READMEs, explain the local purpose and link to shared instructions. Avoid duplicating repository-wide setup in each package. Respect the established README location; for a new project or package, place it alongside the code it introduces.

## Adaptable structure

Include sections when they answer a reader's actual question. Combine or omit sections as appropriate; do not leave empty template headings.

| Content | What the reader needs |
|---|---|
| Name and description | What it does, who it is for, and the problem it solves. |
| Status and limitations | Known maturity, deprecation, or constraints that affect adoption. Put consequential limitations near the top. |
| Quick start | Prerequisites and the shortest supported path to a useful result. |
| Usage | A representative example and an explanation of the result. |
| Configuration | Settings needed for common use, their defaults where verified, and links to the complete reference. |
| Documentation and help | Where to learn more, troubleshoot, or contact the responsible team. |
| Development and contributing | Local development essentials and links to contribution guidance, when relevant. |
| License | The project's stated license and a link to its license file, when available. |

Separate using the released project from developing a source checkout. Make each command's working directory and prerequisites clear. Keep essential configuration in the quick start if the example cannot work without it.

## Evidence and runnable examples

Treat the existing README as a claim to check. Inspect relevant manifests, scripts, source entry points, tests, configuration examples, and release information before documenting behavior.

- Derive installation commands, package names, supported versions, and API calls from project evidence. Distinguish released functionality from changes available only in the checkout.
- Show a complete minimal example with the necessary imports, inputs, and setup. Label placeholders and distinguish sample output from output actually observed.
- Include a success signal: expected output, a resulting file, or the page the reader should see.
- Run the documented path when feasible within the task's permissions and environment. Commands that deploy, spend money, or alter external data require an appropriate test environment or existing authorization.
- If execution is unavailable, check commands against the implementation and report the remaining verification gap to the user. Do not describe an example as tested unless it was run.
- Describe implemented capabilities. Label planned work explicitly and avoid unsupported performance, compatibility, or production-readiness claims.
- Use the existing license and contribution policy. Missing information is a gap to report, not permission to choose a license, invent a maintainer, or promise support.

## Keep it useful over time

Link to detailed API, configuration, architecture, contribution, and release documentation instead of copying it into the README. Prefer relative links for files in the same repository, and check paths and section anchors after edits.

Keep prose concrete and examples small. Use fenced code blocks with language identifiers and avoid shell prompt characters in copyable commands. Give meaningful images alternative text; use screenshots only when they explain something text or a short example cannot.

Add badges, feature lists, directory trees, and a manual table of contents only when they help readers and can be maintained. GitHub already provides a heading-based outline; other renderers or explicit Standard Readme compliance may justify a manual contents section.

## Reviewing a README

Prioritize issues that prevent understanding or successful use: an unclear purpose, missing prerequisites, incorrect commands, unsupported claims, or broken links. Then address navigation and wording. Report concrete mismatches and verification limits; do not impose every optional section as a review requirement.

---
name: author-readme
description: Use `author-readme` skill when creating or rewriting README.md file.
---

## README.md Layout

```markdown
***[HERO]***

<p align="center">[LOGO]</p>

<h1 align="center">[Project Name]</h1>

---

[PURPOSE]

---

## Features

[FEATURES]

[INTEGRATION]

## Installation

[PREREQUISITES]

[LOCAL SETUP STEPS]

[STARTUP STEPS]

## Usage

[COMMON USAGE]

[TUTORIAL]

## Configuration

[CONFIGURATION]

## Development

[ARCHITECTURE]

[DEVELOPER NOTES]

### Testing

[TESTING]

### Deployment

[PACKAGING STEPS]

[DEPLOYMENT STEPS]

## Terminology

[ACRONYMS]

[DEFINITIONS]

```

Replace placeholders in README.md as follows:

- [LOGO]: Determine the logo as follow:
    1. Use `autocode_logo_find` tool to find a logo. 
    2. If `autocode_logo_find` returns a logo path, replace [LOGO] with `<img src="{path to logo}" alt="Project Logo" height="128">`. 
    3. If no logo was found, use an appropriate emoji to replace [LOGO] with `<span style="font-size: 96px; text-shadow: -3px -3px 0 #000, 3px -3px 0 #000, -3px  3px 0 #000, 3px 3px 0 #000, 0 -3px 0 #000, 0 3px 0 #000, -3px 0 0 #000, 3px 0 0 #000;">{emoji}</span>`.
- [Project Name]: Project name in a natural title format. If unknown: derive title from repo name
- [HERO]: Catching advertising title as follows:
    - Summarize what project does in positive way like marketing advert
    - Max 20 words
    - No definitions in this section
    - Use only common words, not project specific terminology (except for naming components)
- [PURPOSE]: Motivate why this project should exist as follows:
    - Briefly describe problem it solves and solution/benefit of using this project
    - Use marking style: Wording should encourage stakeholders to invest time to setup and use system
    - Do not list any technical features, instead mention problems it solve (use cases)
    - Max 80 words
    - No definitions in this section
    - Use only common words, not project specific terminology (except for naming components)
- [FEATURES]: Advertise core features in markdown bullets as follows:
    - 1 feature per bullet
    - Unique emoji per feature
    - Max 40 words per feature
    - No definitions in this section
    - Use only common words, not project specific terminology (except for naming components)
- [INTEGRATION]: Explain how project integration with external systems (like miroservices):
    - Title summarize how it integrations (max 7 words), like "REST Integration" or "Microservice Architecture"
    - Include high-level TD Mermaid diagram of how it integrates
    - Only include [INTEGRATION] section if this project does integrate with external systems
- [PREREQUISITES]: System requirements and dependencies needed before installation as follows:
    - List prerequisites as bullet points: 1 per dependency
    - Provide markdown links in text to online sources that provide guidance where to download or how to install dependency
    - Only include [PREREQUISITES] if project does depend on other systems
- [LOCAL SETUP STEPS]: Commands and steps to set up the project locally as follows:
    - Provide sequential steps
    - Each step must include an example command/config/user action
    - Each step must include an example response/output (if known)
    - Provide minimal configuration/commands just to get a demo/basic version going
    - Format examples with proper markdown block formatting where appropriate
    - Only include [LOCAL SETUP STEPS] if project does require a setup
- [STARTUP STEPS]: Commands to start the project
    - Provide sequential steps
    - Each step must include an example command/config/user action
    - Each step must include an example response/output (if known)
    - Format examples with proper markdown block formatting where appropriate
    - Explain different modes project support (for example development vs production mode)
    - If startup modes are vastly different organize it in different sub-sections
    - Only include [STARTUP STEPS] if project does require a server/service to start
- [COMMON USAGE]: Explain how to use system as follows:
    - Provide primary commands (if applicable)
    - Provide primary URLs (if applicable)
    - Explain how user can navigate through application to reach primary features (if applicable)
    - Include example input/output in markdown blocks/tables (if possible)
    - ONLY include usage of feature that is currently available 
    - NEVER include deprecated/uninplemented/planned/future features
- [TUTORIAL]: Step-by-step guide for common user flows.
- [CONFIGURATION]: Explain every project specific configuration setting as follow:
    - Provide tables of every custom config key/property/env var that project accepts with descriptions and default values and valid ranges or alternative enums
    - NEVER include standard framework properties like Spring Boot/Angular/Nuxt configs or any standard OS env vars
    - ONLY include known (proven) configuration (no guessing)
    - Only include this section if project has custom configuration
- [ARCHITECTURE]: Explain how project fulfill its purpose describe in [PURPOSE] as follow:
    - If project is full stack: Include high-level TD Mermaid diagram of how different components of project interact with each other
    - If project contains complex event system: Include high-level TD Mermaid diagram of how events/data flow 
    - If project contains multiple pages of static web content: Include high-level TD Mermaid diagram of primary pages link to each other (sitemap)
    - If project is library or monolithic application: Include high-level TD Mermaid diagram of primary internal components and how they relate to each other
    - If project is CLI tool: Include high-level TD Mermaid diagram of how data typically flow through this tool: inputs -> processes -> outputs
    - Project may solve more than 1 problem (multi-purpose project): In such case identify each primary goal, then for each goal:
        - Write 1 paragraph per goal (max 200 words) how it solves that specific goal
        - Include markdown links in text to core source files responsible for solution or where additional documentation could be found
    - Omit this section is project architecture is unclear, empty or new (no guessing)
- [DEVELOPER NOTES]: Any special notes that developers of the project should be aware of like: Special commands to build project, common pitfalls, unusual file locations/config/commands required, quality standards, etc.
    - May contain sub-sections (max 200 words per section)
    - Must be human readable and may contain examples to explain intend
    - Keep this section as lean as possible and AVOID REPEATING any info mentioned in other sections of this document
    - Only include this optional section if you have important info to make developers aware of
- [TESTING]: Steps how to test local development quality as follow:
    - Provide sequential steps
    - Each step must include an example command/config/user action
    - Each step must include an example response/output (if known)
    - Format examples with proper markdown block formatting where appropriate
    - Only include this section if project does contain tests
- [PACKAGING STEPS]: Steps to build/package for production as follows:
    - Provide sequential steps
    - Each step must include an example command/config/user action
    - Each step must include an example response/output (if known)
    - Format examples with proper markdown block formatting where appropriate
    - Only contain this section if project needs packing for production deployment
- [DEPLOYMENT STEPS]: Steps to deploy to production as follows:
    - Provide sequential steps
    - Each step must include an example command/config/user action
    - Each step must include an example response/output (if known)
    - Format examples with proper markdown block formatting where appropriate
    - If different deployment environments are supported (e.g. local vs docker): Organize in sub-sections
    - Only include this section if production deployment is different from [LOCAL SETUP STEPS]

## Rules for Updates

- For target update, keep existing README structure.
- Before edit, record hero, logo, H1, badges, header HTML, and section anchors.
- Add missing sections like [HERO], [PURPOSE], etc. but never add guessed or "coming soon" content.
- Edit only requested sections with outdated content.
- If `autocode_logo_find` failed, preserve existing logo; never remove or substitute it.
- After write, verify outline and fix errors.
- Remove empty sections without factual content
- Validate markdown links; update factually outdated information.
- Avoid duplicate content; link to existing sections instead.
- Define non-standard acronyms and terms once at first use.
- Never mention deprecated tools or configs; keep examples current.
- Never mention todos, vulnerabilities, code smells or incomplete features.

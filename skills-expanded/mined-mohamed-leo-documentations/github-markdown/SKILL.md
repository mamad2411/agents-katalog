---
name: github-markdown
description: >
  Write professional, well-structured GitHub Markdown documents for projects and organizations.
  Use this skill whenever a user wants to write or improve a README.md, GitHub org profile, 
  project documentation, CONTRIBUTING.md, CODE_OF_CONDUCT.md, or any markdown file intended 
  for a GitHub repository or organization. Trigger this skill when users mention: "README", 
  "GitHub docs", "project documentation", "org profile", "markdown for my project", 
  "write docs for my repo", "professional README", or any request to document a GitHub project 
  or organization — even if they just say "help me write docs for X project". Always use this 
  skill rather than writing markdown ad hoc.
---

# GitHub Markdown Skill

Produce polished, professional GitHub Markdown documents: READMEs, org profiles, contributing guides, and more.

---

## Step 1 — Gather Context

Before writing anything, collect the following. Pull what you can from the conversation; ask only for what's missing.

### For a **project README**:

| Field                                     | Why it matters                        |
| ----------------------------------------- | ------------------------------------- |
| Project name & one-liner                  | Hero section & title                  |
| Project type                              | Determines structure (see §Templates) |
| Tech stack / language                     | Badges, install instructions          |
| Key features (3–7 bullets)                | Features section                      |
| Install / setup steps                     | Getting Started                       |
| Usage examples                            | Usage section                         |
| License                                   | Footer                                |
| Contributors / org name                   | Credits                               |
| Links (live demo, docs site, npm, PyPI…)  | Badges & links                        |
| Current state (alpha / stable / archived) | Status badge                          |

### For an **org profile** (`<org>/.github/profile/README.md`):

| Field                                | Why it matters     |
| ------------------------------------ | ------------------ |
| Org name & mission                   | Hero               |
| Key projects (name + one-liner each) | Highlights section |
| Tech focus / domain                  | Context            |
| Team size / open-source stance       | Community section  |
| Social links, website, contact       | Footer             |
| Pinned repos already set?            | Avoid duplication  |

If the user provides a GitHub URL, a codebase description, or a `package.json` / `pyproject.toml` snippet, extract as much as possible automatically before asking.

---

## Step 2 — Choose the Right Template

Read the project type and pick the matching template from `references/templates.md`:

| Project type                          | Template    |
| ------------------------------------- | ----------- |
| Library / Package (npm, PyPI, cargo…) | `library`   |
| CLI Tool                              | `cli`       |
| Web App / SaaS                        | `webapp`    |
| REST / GraphQL API                    | `api`       |
| Framework / Boilerplate               | `framework` |
| Data Science / ML project             | `ml`        |
| GitHub Organization                   | `org`       |
| Generic / Unknown                     | `generic`   |

→ **Load `references/templates.md`** before writing.

---

## Step 3 — Writing Rules

### Structure & Order

Always follow this canonical section order (omit sections that don't apply, never reorder):

1. **Logo / Banner** _(optional but recommended)_
2. **Title + one-liner tagline**
3. **Badges row** (build, version, license, coverage, stars)
4. **Short description** (2–4 sentences, what + why + who)
5. **Table of Contents** _(only if README > ~150 lines)_
6. **Features** (bullet list, 3–7 items)
7. **Demo / Screenshots** _(if applicable)_
8. **Getting Started** (Prerequisites → Installation → Configuration)
9. **Usage** (code examples, commands)
10. **API Reference / CLI Reference** _(if applicable)_
11. **Project Structure** _(optional, for complex projects)_
12. **Contributing** (brief + link to CONTRIBUTING.md)
13. **License**
14. **Acknowledgements / Credits** _(optional)_

### Badges

Use [shields.io](https://shields.io) format. Common badges:

```markdown
![Build](https://github.com/<org>/<repo>/actions/workflows/ci.yml/badge.svg)
![Version](https://img.shields.io/npm/v/<package>)
![License](https://img.shields.io/github/license/<org>/<repo>)
![Stars](https://img.shields.io/github/stars/<org>/<repo>?style=social)
```

Only include badges that are real and verifiable. Don't invent CI/CD badges if no pipeline exists.

### Code Blocks

- Always specify the language after the triple backtick: ` ```bash `, ` ```python `, ` ```js `
- Use realistic, runnable examples — not `<placeholder>` soup
- For multi-step setups, use numbered steps, not bullets

### Tone & Voice

- **Active voice**: "Install the package" not "The package can be installed"
- **Imperative mood** for instructions: "Run", "Add", "Configure"
- Concise but complete — no walls of text, no empty filler sentences
- No marketing fluff ("blazing fast", "revolutionary") unless the user explicitly wants it

### Visual Hierarchy

- Use `##` for main sections, `###` for subsections — never skip levels
- Use `**bold**` for key terms, not for decoration
- Use `> blockquote` for important notes / warnings
- Use `---` horizontal rules sparingly (only between very distinct major sections)

### GitHub-Specific Markdown

- Relative links work: `[Contributing](./CONTRIBUTING.md)`
- Collapsible sections: `<details><summary>Title</summary> ... </details>`
- Alerts (GitHub flavored): `> [!NOTE]`, `> [!WARNING]`, `> [!TIP]`
- Task lists in CONTRIBUTING: `- [ ] Step one`
- Emoji: use sparingly and only where they add clarity (✅ ❌ 🚀 📦)

---

## Step 4 — Quality Checklist

Before delivering, verify every item:

- [ ] Title matches the actual project/repo name
- [ ] No broken placeholder links (`<your-repo>` left unfilled)
- [ ] Every code block has a language specifier
- [ ] Install/usage steps are correct for the stated stack
- [ ] Badges use real URLs (or are clearly marked `<!-- replace with real URL -->`)
- [ ] TOC anchors match actual heading text
- [ ] License section names the correct license
- [ ] No duplicate sections
- [ ] Consistent heading hierarchy (no jump from `#` to `###`)
- [ ] File ends with a newline

---

## Step 5 — Deliver

1. Output the full markdown in a code block **and** as a downloadable `.md` file via `present_files`.
2. Briefly explain any assumptions made (e.g., "I assumed MIT license — update if different").
3. Offer to generate companion files if relevant:
   - `CONTRIBUTING.md` — contribution workflow
   - `CODE_OF_CONDUCT.md` — Contributor Covenant template
   - `CHANGELOG.md` — Keep a Changelog format
   - `.github/ISSUE_TEMPLATE/` — bug report + feature request templates
   - `.github/pull_request_template.md`

---

## Reference Files

- **`references/templates.md`** — Full section-by-section templates for each project type. Load when writing.
- **`references/badge-catalog.md`** — Common shields.io badge snippets by ecosystem. Load when building badge rows.

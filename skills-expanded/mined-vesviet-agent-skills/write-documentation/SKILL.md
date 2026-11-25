---
name: write-documentation
description: Draft or update technical documentation by following the repo's existing doc structure, audience needs, Diátaxis framework, and source-of-truth boundaries. Use when writing or updating README files, service docs, runbooks, architecture overviews, integration notes, or change explanations.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code]
---

# Write Documentation

Use this skill when a change needs clear technical documentation or when existing docs are outdated or incomplete.

**Role routing:** Long-form **articles, blogs, guides, and SEO posts** → **Content Writer** role with `write-article`. **README, runbooks, API docs, setup guides** → **Technical Writer** role. Content Writer may use this skill for structure and clarity patterns only—not as a substitute for `write-article` on publishable posts.

## When to Use

- README updates or service docs
- runbooks or integration notes
- explaining a change
- following repo doc structure + source-of-truth

## Core Rules

- write for the intended audience, not for the author; open every page with the core definition or solution in the first paragraph — do not bury the answer
- keep docs aligned with the actual source of truth; do not duplicate content that already lives in an authoritative location — link to it instead
- prefer concrete steps and exact examples over vague explanation; code samples must have language tags, valid syntax, and complete imports
- **Diátaxis quadrant isolation**: every documentation file belongs to exactly ONE quadrant — Tutorial (learning-oriented), How-to (problem-oriented), Reference (information-oriented), or Explanation (understanding-oriented); never mix architectural philosophy with step-by-step beginner guides in a single file
- **Dual-audience authoring**: structure every document for both human engineers and AI agents — consistent Markdown headings, unambiguous terminology, and semantic YAML frontmatter (`title`, `description`, `category: tutorial|howto|reference|explanation`, `last_verified_version`) enable LLM and RAG retrieval without hallucination
- **Reference docs must be auto-generated**: API reference documentation is generated directly from OpenAPI / AsyncAPI / protobuf specs using Redocly, Scalar, or Mintlify — hand-typed endpoint definitions are rejected as they drift from the source of truth
- **Docs-as-code CI gate**: documentation PRs must pass `markdownlint`, Vale prose style, broken-link checker, and frontmatter schema validation before merge; Cloudflare Pages or Netlify deploy previews are mandatory for reviewer sign-off
- avoid internal workflow wording in user-visible docs unless the repo explicitly expects it
- treat AI-assisted doc drafts as untrusted until reviewed; never publish a doc with `[UNVERIFIED]` claims or placeholders left in
- validate every external link in the doc against the live target before publish; treat 404s as a docs-as-code CI failure
- run a secret scan on the doc before commit; never include tokens, customer identifiers, or internal hostnames in user-facing docs (OWASP ASI03)

## Output Contracts

When the documentation change is consumed by a docs-as-code pipeline, a
content management system, or another cross-role handoff, emit:

- **`contracts/schemas/documentation-handoff.json`** — capture the doc path, the Diataxis quadrant, the source-of-truth link, the OpenAPI/AsyncAPI version, the `last_verified_version`, and the audience. The receiving agent can then validate the doc against the live system.
- For human-readable publication, the markdown file with frontmatter is the canonical format.
- Reference docs are auto-generated from the OpenAPI/AsyncAPI spec; the spec is the source of truth and the doc handoff points to the spec, not a hand-typed endpoint list.

Skip emission for trivial inline edits that do not cross a role boundary.

## Failure Modes

- **Mixed Diataxis quadrants**: a tutorial file mixes architectural philosophy with step-by-step instructions. Mitigation: enforce one quadrant per file; split into separate docs if needed.
- **Hand-typed reference doc**: an API reference is hand-typed and drifts from the spec. Mitigation: auto-generate from OpenAPI/AsyncAPI; reject hand-typed reference lists.
- **Broken link**: a docs page links to a 404. Mitigation: run broken-link checker in CI; treat 404s as a docs-as-code failure.
- **Burying the answer**: a doc opens with context instead of the answer. Mitigation: every page opens with the core definition or solution in the first paragraph.
- **Internal workflow wording in user docs**: a doc mentions agent names, AI workflow, or internal process labels. Mitigation: lint for internal terms; strip before publish.
- **Stale doc not refreshed**: a doc references an old API version or removed feature. Mitigation: re-validate on every release; treat staleness as a release-blocking issue.
- **`/llms.txt` not updated**: the AI-readable index is missing or stale. Mitigation: regenerate `/llms.txt` and `/llms-full.txt` on every doc change; CI must verify.
- **Secret in docs**: a token, customer id, or internal hostname is pasted into a doc. Mitigation: run secret scan before commit; reject the doc on detection.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: an AI-assisted doc draft may reframe the user goal. Cross-check the doc against the source-of-truth spec; reject reframed content.
- **ASI03 Identity & Privilege Abuse**: never include tokens, customer identifiers, or internal hostnames in user-facing docs.
- **ASI04 Supply Chain**: external links in docs are untrusted; validate every link against the live target before publish.
- **ASI07 Inter-Agent Communication**: the doc handoff is consumed by the docs pipeline and downstream agents; emit a structured contract so each consumer can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present a doc as "complete" while `[UNVERIFIED]` claims remain; surface every unverified claim honestly.

## Suggested Process

### 1. Identify The Documentation Need

Clarify:

- who will read it
- what problem it should solve
- whether it is setup, architecture, operations, usage, or release-oriented documentation

### 2. Inspect Existing Documentation Patterns

Look for:

- local doc location and naming conventions
- section structure
- voice and depth
- whether docs are colocated with code or live elsewhere

### 3. Gather The Minimum Correct Facts

Collect:

- commands or workflows that actually work
- key architecture or integration points
- configuration requirements
- known limitations or risks worth noting

### 4. Draft For Fast Usefulness

Prefer:

- short purpose statement
- prerequisites
- exact steps or examples
- troubleshooting notes when relevant
- links to deeper references instead of repeating them

### 5. Verify The Documentation

Check:

- examples match the code or repo structure
- commands are plausible for the target environment
- ownership and source-of-truth references are clear
- stale or conflicting guidance is removed

### 2026: Modern Documentation Standards

To align with modern AI-assisted engineering and automated API publishing:

- **AI-Readable Formats**: Maintain `/llms.txt` at the repository root and `/llms-full.txt` in markdown format to serve as clean, high-context inputs for LLMs and AI coding assistants.
- **Diataxis Framework**: Categorize documentation into four distinct forms:
  - **Tutorials**: Learning-oriented guides to help newcomers get started.
  - **How-to Guides**: Goal-oriented recipes showing how to solve specific problems.
  - **Reference**: Information-oriented technical descriptions (APIs, schemas, commands).
  - **Explanation**: Understanding-oriented concept overviews and architectural rationale.
- **OpenAPI Reference Docs**: Auto-generate API reference documentation using Redocly, Scalar, or Mintlify, ensuring the OpenAPI specification remains the single source of truth.
- **Docs-as-Code Pipeline**: Implement continuous integration checks for markdown links and formatting, with automated pull request previews deployed to Cloudflare Pages or Netlify for team reviews.

## Checklist

- [ ] audience and doc purpose identified
- [ ] local doc pattern reviewed
- [ ] facts gathered from current source of truth
- [ ] examples and steps written clearly
- [ ] stale or conflicting guidance removed
- [ ] `/llms.txt` and `/llms-full.txt` standards updated for AI readability
- [ ] Diataxis structure followed (Tutorials, How-to, Reference, Explanation)
- [ ] OpenAPI spec verified and auto-generation configured (Redocly, Scalar, Mintlify)
- [ ] Docs-as-code pipeline checked (CI linting and Cloudflare Pages/Netlify previews working)

## Related Skills

- **write-article**: Narrative and blog drafting under Content Writer
- **navigate-service**: Gather context before documenting a service
- **review-service**: Capture readiness or release notes after review
- **troubleshoot-service**: Turn learned recovery steps into runbook updates
- **write-tech-radar**: Draft higher-level technology assessments
- **commit-code**: Prepare doc updates for delivery
- Companion reference: `references/diataxis-framework-and-doc-standards.md`
- Companion example: `examples/microservice-production-readme-and-api-docs.md`

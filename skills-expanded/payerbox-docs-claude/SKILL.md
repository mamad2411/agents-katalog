# Payerbox Documentation

This is a documentation repository for Payerbox. It uses Health Samurai's `docs-tools` for linting and image optimization.

All documentation is written in **English**.

## Structure

```
docs/           — markdown files (documentation pages)
assets/         — images and downloadable files
SUMMARY.md      — table of contents and navigation
docs-lint.yaml  — linter configuration
redirects.yaml  — URL redirects
```

## Source code (agent reference only — DO NOT link from docs)

Payerbox ships as three components. Read these repos to verify implementation behavior, parameter names, error codes, and supported flags. **Never link to them in published documentation** — they are private.

| Component | Source repo (private) | Public Docker image (OK to link) |
|---|---|---|
| FHIR App Portal + Developer Portal | https://github.com/HealthSamurai/smartbox | https://hub.docker.com/r/healthsamurai/fhir-app-portal |
| Interop APIs (Patient / Provider / Payer-to-Payer / Directory) | https://github.com/HealthSamurai/interop | https://hub.docker.com/r/healthsamurai/interop |
| Prior Auth (CRD / DTR / PAS) | https://github.com/HealthSamurai/prior-auth | https://hub.docker.com/r/healthsamurai/prior-auth |

If a doc needs to point users at the running software, link the Docker Hub image — never the GitHub repo.

## Aidbox documentation (style and platform reference)

Payerbox runs on Aidbox. The Aidbox docs repo is public: https://github.com/HealthSamurai/aidbox-docs (rendered at `docs.aidbox.app`).

Read it when you need:
- Style/structure patterns for a topic Aidbox already documents (auth, FHIR storage, SearchParameters, SMART on FHIR, etc.)
- Source-of-truth for Aidbox features Payerbox inherits

Do not hyperlink to `docs.aidbox.app` — the `absolute-links` lint blocks it. If you must reference Aidbox docs, mention them in plain text ("see Aidbox docs on …") rather than as a markdown link.

## Page types: Pillar vs Reference

Docs split into two page types — keep them distinct.

**Reference** — `docs/api-reference/operations/*`. For integrators writing code against an endpoint.

Must include:
- H1 = operation name, plain text, no backticks (e.g. `# $op-name`)
- Intro: IG name, pinned STU version, what the operation does
- Endpoints (URL paths)
- Auth: 1–3 lines + cross-link to `api-reference/authentication.md`
- Input/Output Parameters — full tables (cardinality, types, descriptions)
- Examples — all Request/Response variants including errors and edge cases (JSON payloads)
- Errors table
- Current Limitations — full
- At least one outgoing link (usually cross-link to the pillar)

Must not include:
- Marketing language ("powerful", "seamless", "in action")
- Regulatory framing (lives in `compliance/*`)
- Authentication onboarding flow (lives in `authentication.md`)
- Path-choice comparisons ("X vs Y")

**Pillar** — `docs/interop-apis/*`, `docs/prior-auth/*`. For architects/PMs/devs choosing and understanding an API before integration.

Must include:
- H1 = human name of the API (no backticks, no `$op-name`)
- Overview: what it is, who uses it, how it fits the stack (e.g. CRD → DTR → PAS)
- Architectural / sequence diagram if helpful
- **"What Payerbox covers"** — 3–6 bullets of concrete product capabilities (IGs preconfigured, operations exposed, ingestion adapters, audit logging, etc.). Position right after the intro paragraph and the flow diagram, **before** auth/paths/operations sections. Reader sees product scope before protocol detail.
- Path-choice table when alternatives exist (e.g. DTR SMART App vs `$questionnaire-package`)
- Lifecycle / flow overview
- For each key flow step: one Request+Response pair in `{% tabs %}`, JSON payloads, ≤30 lines each — to convey shape, not depth
- Current Limitations — short, only what affects path choice (full version stays in reference)
- Cross-links to every reference page for the API + to `compliance/*`

Must not include:
- Backticked operation name in H1
- Full Parameters tables (lives in reference)
- All Response variants or error codes (lives in reference)
- Authentication onboarding flow (lives in `authentication.md`)
- Regulatory anchor tables **or inline CFR citations in body prose** — CFR citations (`(42 CFR 422.121)`, `per 45 CFR 156.222`), compliance dates, response-time SLAs, member-education timelines. In the page's opening paragraph (right after the H1) hyperlink the rule name to its `compliance/*` page and state the compliance deadline. No second clause describing what lives in compliance ("full regulatory detail …", "for CFR citations see …") — the hyperlink is the link. No inline parenthetical citations anywhere else on the page.

External systems referenced from a pillar (e.g. CRD's Decision Service via `CDS_DECISION_SERVICE_URL`) stay in the pillar — they explain architecture, not the endpoint contract.

`docs/compliance/*` is neither pillar nor reference — regulatory citation only, with CFR/CMS anchors and links to relevant pillar/reference pages.

## Verifying spec claims before publishing

When a page makes a factual claim about an IG, an operation, or implementation behavior, the claim must be checked against the source before merge — not paraphrased from a competitor's docs or extrapolated from a generic FHIR pattern.

- **Operation invocation level.** Verify whether an operation is invoked at system (`POST <base>/fhir/$op`), type (`POST <base>/fhir/Resource/$op`), or instance (`POST <base>/fhir/Resource/[id]/$op`) level by reading the OperationDefinition's `system` / `type` / `instance` boolean fields. Don't guess from naming.
- **Operation IG attribution.** Some operations are defined in one IG and referenced by another — for example, `$davinci-data-export` is defined in the Da Vinci ATR IG and referenced by PDex. Write "defined in X and referenced by Y" rather than collapsing to "defined in PDex".
- **Error response tables.** Enumerate only HTTP status codes and `OperationOutcome` codes the codebase actually emits. Don't import generic FHIR Bulk Data error patterns. If implementation isn't accessible, omit the table — pillar pages should defer to reference for error details anyway (see the Pillar / Reference split above).
- **Implementation-specific behavior** (cleanup intervals, validity windows, default scopes, opt-out capture channels). Mark it explicitly as Payerbox / interop-app behavior, not as a spec requirement. Don't blur "the IG requires X" with "Payerbox implements X with these defaults".

## Writing Documentation

### Setup

Run `bun install` once after cloning — this installs docs-tools and sets up git hooks.

`docs-tools` is intentionally unpinned (`github:HealthSamurai/docs-tools`). `bun install` installs the version locked in `bun.lock` without modifying it. CI runs `bun update docs-tools` to pull the latest version and commits the updated `bun.lock` back to the repo.

### Creating a New Page

1. Create a `.md` file in `docs/` (or a subdirectory)
2. Start the file with a single `# Title` heading
3. Add the page to `SUMMARY.md` in the correct section
4. Run `bun lint` to verify everything is correct

### Frontmatter (optional)

Pages can have YAML frontmatter:

```markdown
---
hidden: true
description: Page description for SEO
---
# Page Title
```

- `hidden: true` — page is excluded from orphan-pages lint check

### SUMMARY.md Format

```markdown
# Table of contents

## Section Name

* [Page Title](page-file.md)
* [Another Page](subdir/page.md)
```

Rules:
- Page title in SUMMARY.md must match the `# H1` heading in the file
- Use "and" instead of "&" in titles
- Every `.md` file in `docs/` must be listed in SUMMARY.md

### Images

Place images in `assets/` directory (use subdirectories to organize, e.g. `assets/get-started/`).

```markdown
![Description of the image](../assets/screenshot.png)
```

- Always provide meaningful alt text — linter warns on empty `![](image.png)`
- Supported formats: PNG, JPG, JPEG, GIF, SVG, WebP, AVIF
- CI automatically converts images to AVIF and updates references — commit as PNG/JPG, optimization happens on push
- To optimize locally before pushing: `bun images:optimize`

#### Updating an image that is already published

The docs site serves every asset with `Cache-Control: public, max-age=31536000, immutable` and no `ETag`, on a URL carrying no version (`src/docs/handler.ts` in the website repo). Editing a file in place therefore reaches nobody who has opened the page before: their browser, and the CDN edge in front of it, keep the old bytes for up to a year.

So when the content of a published image changes, **rename the file** and update the reference — `architecture.svg` → `architecture-v2.svg`, next change `-v3`. A new filename is a new cache key.

- A `?v=2` query on the reference would do the same and read better, but the `broken-links` check resolves the whole string as a file path and fails on `architecture.svg?v=2`. The pre-push hook blocks it, so this is not an option until `docs-tools` learns to strip the query.
- No redirect is needed: `redirects.yaml` values must be `.md` files, and nothing references the old asset once the page is updated.
- A brand-new image needs no suffix. Nothing stale is cached under a name that was never published.
- Renaming does not help readers who already loaded the old name from a direct link. Only a CDN invalidation of `/docs/payerbox/assets/*` fixes that, and it needs access to the website's GCP project.

### Mermaid Diagrams

Mermaid diagrams are supported via ` ```mermaid ` code blocks. They are rendered server-side to SVG (light + dark themes). Use round rectangles `(Node Name)` instead of `[Node Name]` for nodes. No custom CSS classes or inline styles — only the built-in color classes below.

#### Color Classes

Apply colors to nodes using `class NodeName color` or inline `:::color` syntax. The class name is `{color}{width}` where width is the border thickness in pixels (1, 2, or 3).

Available colors: `red`, `blue`, `violet`, `green`, `yellow`, `neutral`

Examples: `red1`, `blue2`, `green3`, `neutral1`

```mermaid
graph LR
    A(Source):::blue2 --> B(Process):::green2 --> C(Result):::violet2
    class A blue2
```

Class definitions are auto-injected — do not write `classDef` lines manually.

### Inline SVG architecture / flow diagrams

For new architecture or data-flow diagrams, use inline SVG in the house style — three semantic tiers (red `#EA4A35` for Payerbox / our product, blue `#549FEA` for optional / third-party, neutral `#D3DBE6` / `#F6F7F8` for external systems), Inter font, solid 1px connectors with `vector-effect: non-scaling-stroke`. Full style guide lives in the `diagrams-draw` skill (currently in agent worktrees: `.claude/worktrees/*/skills/diagrams-draw/SKILL.md`).

Before committing, verify the rendered diagram:

- **No connector label overlapping its own line.** When a label is wider than a comfortable gap between line segments, prefer a `<rect fill="#FFFFFF">` mask sized to the label behind the text — the line stays solid; the rect punches it where the label sits. Cleaner than splitting the line, less fragile geometry.
- **Arrows between vertically- or horizontally-aligned boxes centered on the shared visual axis.** If two boxes are both centered at `x=480`, the connecting line must be at `x=480` too. Off-axis connectors read as misalignment.
- **No card text clipping or overflow.** Read the rendered SVG (Read tool on the page screenshot, or open the SVG directly) after writing.

### Markdown Rules

- Exactly one `# H1` per file (the page title)
- Do not skip heading levels (H1 → H3 is wrong, use H1 → H2 → H3)
- No empty headings
- All internal links must point to existing files
- All referenced images must exist in `assets/`
- Images should have meaningful alt text
- ALWAYS use proper language in codeblocks.

### Redirects

When renaming or moving a page, add a redirect in `redirects.yaml` so old URLs keep working:

```yaml
redirects:
  old/path/slug: new/path/to/page.md
  another/old/slug: some/page.md#section-anchor
```

- **Keys** — old URL slugs (no leading `/`, no `.md` extension)
- **Values** — relative paths to `.md` files in `docs/` directory
- Section anchors are supported: `page.md#section` redirects to a specific section
- The linter checks that target `.md` files exist — missing targets cause an error

## Supported Widgets

Widgets fall into two shapes:

- **Block widgets** — require an opening and closing tag (`{% hint %} … {% endhint %}`). All widgets below are block widgets except `embed` and `file`.
- **Self-closing widgets** — one tag with a trailing slash: `{% embed url="…" / %}`, `{% file src="…" / %}`. `file` also supports a block form when you need custom link text.

Nesting:
- `{% tab %}` must be inside `{% tabs %}`
- `{% step %}` must be inside `{% stepper %}`
- `{% swagger-description %}`, `{% swagger-parameter %}`, `{% swagger-response %}` must be inside `{% swagger %}`
- Other widgets nest freely (e.g. hints inside tabs, code blocks inside steps).

### Hint (callout box)

```markdown
{% hint style="info" %}
Informational message.
{% endhint %}
```

Styles: `info`, `success`, `warning`, `danger`

### Tabs

`{% tab %}` must be inside `{% tabs %}`.

```markdown
{% tabs %}
{% tab title="First Tab" %}
Content for tab 1.
{% endtab %}
{% tab title="Second Tab" %}
Content for tab 2.
{% endtab %}
{% endtabs %}
```

### Stepper (numbered steps)

`{% step %}` must be inside `{% stepper %}`.

```markdown
{% stepper %}
{% step %}
First step content.
{% endstep %}
{% step %}
Second step content.
{% endstep %}
{% endstepper %}
```

### Code Block with Title

```markdown
{% code title="config.yaml" %}
```yaml
key: value
```
{% endcode %}
```

### Embed (YouTube or link card)

```markdown
{% embed url="https://www.youtube.com/watch?v=VIDEO_ID" / %}

{% embed url="https://example.com" / %}
```

### Content Reference (link card to another page)

```markdown
{% content-ref %}
[Page Title](path/to/page.md)
{% endcontent-ref %}
```

### File Download

```markdown
{% file src="/assets/document.pdf" / %}

{% file src="/assets/archive.zip" %}
Download Archive
{% endfile %}
```

### Carousel (image slideshow)

```markdown
{% carousel %}
![First image](image1.png)
![Second image](image2.png)
{% endcarousel %}
```

### Quote (testimonial)

```markdown
{% quote author="Name" title="Position" %}
Quote text here.
{% endquote %}
```

## Available Commands

```
bun lint          — fix lint issues automatically
bun lint:check    — check for issues without fixing
bun images:check  — find unoptimized images
bun images:optimize — convert images to AVIF format
```

## Git Workflow

- Commit directly to `main` branch
- After committing, ask the user before pushing
- Before starting work and before pushing, always pull with rebase: `git pull --rebase`

### Pre-push Checks

A pre-push git hook runs `bun lint` automatically before every push. If lint fails, the push is blocked.

**Before pushing, always run `bun lint` yourself first.** If there are errors:
1. Show the user what failed
2. Fix the issues (most are auto-fixable by `bun lint` without `--check`)
3. Commit the fixes
4. Only then push

Common lint errors and how to fix them:
- **summary-sync** — file exists but not in SUMMARY.md (or vice versa). Add/remove the entry.
- **title-mismatch** — H1 in file differs from title in SUMMARY.md. Make them match.
- **broken-links** — internal link points to non-existent file. Fix the path.
- **missing-images** — referenced image not found in `assets/`. Add the image or fix the path.
- **h1-headers** — more than one `# H1` in a file. Keep only one.
- **empty-headers** — heading with no text (`## `). Add text or remove.
- **heading-order** — skipped heading level (e.g. H1 → H3). Add the missing level.
- **unparsed-widgets** — unclosed or mismatched widget tags. Close `{% hint %}` with `{% endhint %}`, etc.
- **broken-references** — leftover GitBook `broken-reference` placeholder. Replace with real link.
- **image-alt** (warning) — image without alt text. Add `![description](image.png)`.
- **deprecated-links** — link points to a page in a deprecated directory. Update to current page.
- **absolute-links** — hardcoded absolute URL to our own docs (`docs.aidbox.app` or `www.health-samurai.io/docs`). Replace with a relative path (`../section/page.md`).
- **dead-end-pages** (warning) — page has no outgoing links to other docs. Add at least one cross-link to a related page. Exempt: `SUMMARY.md`, `README.md` files, and pages under `deprecated/`.

CI automatically optimizes images on push.

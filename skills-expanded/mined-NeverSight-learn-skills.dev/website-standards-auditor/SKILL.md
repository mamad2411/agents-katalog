---
name: website-standards-auditor
description: Audit and fix any website (new, in development, or already live) against the organization's mandatory engineering and web standards, then scaffold or repair the gaps after the user approves. Use this whenever the user wants an SEO, GEO, AEO, accessibility, performance, structured data, schema, sitemap, robots.txt, llms.txt, Core Web Vitals, Lighthouse, mobile, metadata, canonical, hreflang, redirects, or internal linking review, or asks to check a repository against the .gitignore and README policy, or mentions auditing, gap analysis, compliance, standards review, or "make my site follow our rules". Always use this for any website quality, discoverability, or standards conformance task even if the user does not name the standard, and follow its two phase flow that produces gap_identification.md first, then fixes only after explicit approval.
---

# Website Standards Auditor

This skill audits a website against one fixed set of organization standards and then fixes the gaps. It works on a brand new project, a project still in development, or an already live site. It always runs in two phases with a hard approval gate between them: first it produces a written gap report (`gap_identification.md`), then, only after the user explicitly approves, it repairs the approved items and reconciles `.gitignore` and `README.md`.

The standards are fixed and bundled with this skill. Do not invent new rules and do not drop existing ones. The three pillars are:

1. Engineering and content rules (see `references/coding_rules.md`)
2. Mandatory git policy and the standard `.gitignore` (see `references/git_policy.md` and `references/gitignore_standard.txt`)
3. Website quality criteria covering SEO, GEO, AEO, structured data, performance, and more (see `references/website_criteria.md`)

## Operating principles (these are binding for every run)

These principles come from the organization rules and override convenience at every step.

- **Never make assumptions.** Detect facts from the repository, the served site, and the user's words. When a fix needs a value that cannot be derived from those sources (for example the canonical domain, the default language and locale, the legal or brand name, social profile URLs, or contact name, address, and phone), do not guess and do not insert a plausible placeholder as if it were real. List the item under "Information required from user" in the gap report and ask for it before writing anything that depends on it.
- **Never use the em dash.** Do not use the em dash character in anything you write or edit, including this skill's own output files (`gap_identification.md`, `fix_summary.md`) and any site content you touch. Use a comma, colon, parentheses, or a reworded sentence instead. The audit also treats every em dash already present in the target site as a defect to be fixed.
- **Always keep `.gitignore` and `README.md` up to date.** Every run ends by reconciling these two files against the current state of the project, even if the user only asked for an SEO check.
- **Never change existing UI/UX.** When fixing gaps or scaffolding new pages, preserve all existing font stacks, color tokens, spacing, border radii, shadow, and layout. New pages (privacy, 404, offline, or any other page created during a fix run) must inherit the project's existing design system. Read the project's CSS, design tokens, or component library before writing a new page. If no design system is detectable, use the bundled template defaults from `assets/` and note in `fix_summary.md` that the user should update the tokens. This rule applies to every file the skill touches, not only to HTML pages.

## The two phases and the hard gate

Phase 1 (audit) produces `gap_identification.md` and then stops. Phase 2 (fix) starts only after the user gives explicit written approval. Do not edit, create, delete, or reformat any site file during Phase 1. Reading files and running read only checks is fine in Phase 1; changing files is not. Never skip the gate, never fix and report at the same time, and never assume silence means approval.

Writing the audit script's output file (`audit_findings.json`) and the report (`gap_identification.md`) into the working area is allowed in Phase 1, because those are the deliverables of the audit, not changes to the site.

## Step 0: Establish context without assuming

Before auditing, determine the following, preferring detection over questions:

- **Site lifecycle.** New (little or no code yet), in development, or already live. Infer from the presence and maturity of source files and from the user's words.
- **Stack and framework.** Read `package.json`, lockfiles, framework config files, and the directory layout. Common cases: static HTML, React or Next.js, Vue or Nuxt, Svelte or SvelteKit, Astro, plain templating (EJS, Nunjucks, Liquid), Frappe or ERPNext, PHP, and so on. The framework changes where metadata and head tags live.
- **Live URL.** Ask whether there is a public URL to inspect. If the user provides one, also analyze the served HTML and response headers, not only the source.
- **Locales.** Whether the site targets more than one language or region. This decides whether hreflang applies.
- **Business type.** Whether the site represents a local or physical business. This decides whether local SEO and `LocalBusiness` schema apply.

Ask only for what you cannot detect and actually need. State any detected fact you are relying on so the user can correct it.

## Step 1: Run the audit

Run all of these, then collect the results. None of them changes the site.

1. **Read the criteria.** Read `references/website_criteria.md` in full. It lists every criterion with how to detect it, how to fix it, and a severity. Treat it as the checklist.
2. **Run the static scanner.** Run the bundled script for the deterministic checks:
   ```bash
   python3 scripts/audit_site.py --path <repo-root> --out <workdir>/audit_findings.json
   ```
   It scans for em dashes and emojis, checks for `robots.txt`, `sitemap.xml`, `llms.txt`, a custom 404 page, and an offline page, looks for metadata and structured data signals across source and template files, flags external image, video, font, and media references, checks form field attributes (types, validation constraints, labels), verifies CTA link destinations and explicit button types, compares the repository `.gitignore` against the bundled standard, and (when git is present) reports any tracked secret files. It writes structured JSON and prints a human readable summary. Read both.
3. **Apply the git policy.** Read `references/git_policy.md` and `references/gitignore_standard.txt`. Confirm a project `.gitignore` exists and contains every required category. Report missing required entries. Never propose removing security, secret, temporary, IDE, AI tooling, or generated file exclusions.
4. **Do the judgment checks by reading files.** Some criteria need human style judgment that a script cannot give reliably: topic clusters and pillar pages, entity SEO and `sameAs` consistency, internal link structure and orphan pages, content that answers questions directly for AEO and GEO, and whether `README.md` actually reflects the current project. Read the relevant files and form findings.
5. **Inspect the live site if a URL was given.** Fetch the served HTML and headers. Confirm that tags present in source actually render, and check response level items such as redirects, caching headers, and compression.
6. **Lighthouse and Core Web Vitals.** See the "Running Lighthouse" section in `references/website_criteria.md`. If a headless browser and the Lighthouse tooling are available and there is a URL or a local server to test, run it and record the scores. If the environment cannot run it, record the item as "not run" with the exact command for the user to run themselves. Never fabricate a score.

Do not treat an absent signal as a confirmed failure when detection is genuinely uncertain (for example when a framework injects head tags at build time). In those cases mark the status "Needs review" and say what to confirm, rather than asserting the item is missing. This is the "never make assumptions" rule applied to the audit itself.

## Step 2: Write gap_identification.md

Build the report from `assets/gap_identification_template.md`. Requirements:

- A short context block at the top: site type, stack, URL if any, locales, what was scanned, and whether Lighthouse ran.
- A summary table counting Pass, Gap, Needs review, Not applicable, and Information required, grouped by category.
- One entry per criterion with: an ID, the category, the criterion name, a status (Pass, Gap, Needs review, Not applicable, or Info required), a severity (Blocking, High, Medium, Low), the evidence (file and line, or URL, or "no signal found"), the recommended fix, and any information required from the user.
- A clear closing section that asks the user how to proceed and lists the choices: approve everything, approve a specific set of IDs, or request changes to the report.

Save the report to the working area, present it, and stop. Do not start fixing.

## Step 3: Get explicit approval

Wait for the user. They may approve all findings, approve a subset by ID, or ask for edits to the report. Fix only what is approved. If approved fixes depend on values you do not have, collect those values now. Do not move forward on any item whose required information is still missing, and do not substitute a guess.

## Step 4: Fix the approved gaps

Work in this order so the riskiest and most foundational items land first:

1. **Blocking and security.** Remove tracked secrets from version control and fix `.gitignore` so they stop being tracked. Advise on rotating any secret that was committed.
2. **Crawl and discovery files.** `robots.txt`, `sitemap.xml`, `llms.txt`, the custom 404 page, the offline page, and redirect or trailing slash rules.
3. **On page SEO and structured data.** Title tags, meta descriptions, viewport and charset, canonical tags, hreflang where relevant, heading structure, internal links, keyword to page mapping, JSON-LD schema, FAQ schema, and entity and knowledge graph markup.
4. **External media self-hosting (RESIL-03).** Self-host all external images, videos, and fonts using `scripts/download_media.py`:
   - Run with `--dry-run` first to preview what will be downloaded and where:
     ```bash
     python3 scripts/download_media.py --findings <workdir>/audit_findings.json \
       --root <repo-root> \
       --out-images public/media/images \
       --out-videos public/media/videos \
       --out-fonts  public/fonts \
       --dry-run
     ```
   - Review the dry-run output with the user, then re-run without `--dry-run` to download.
   - Images are converted to WebP if Pillow is installed (`pip install Pillow`); otherwise the original format is kept and a note is added to `fix_summary.md`.
   - Videos are downloaded in their original format. No re-encoding. After downloading, add `preload="metadata"`, explicit `width` and `height`, and a `poster` attribute pointing to a self-hosted still frame.
   - Fonts are downloaded as-is. Update `@font-face` `src` declarations and add `font-display: swap`.
   - Use the generated `media_replacements.json` to update every `src`, `href`, `srcset`, and `url()` reference in the project. Search and replace the original external URLs with the local paths.
   - For images, wrap in a `<picture>` element: `<source type="image/webp">` pointing to the WebP file, and an `<img>` fallback pointing to the original format file (kept alongside the WebP). Add explicit `width` and `height` to prevent CLS. Use `loading="lazy"` for below-the-fold images and `fetchpriority="high"` for the LCP image.
   - After all references are updated, re-run `audit_site.py` to confirm RESIL-03 is cleared.
5. **Privacy page and Terms of Service page (RESIL-04, RESIL-05).** If either page is missing or incomplete:
   - Create the privacy page from `assets/privacy_page_template.html`.
   - Create the terms page from `assets/terms_page_template.html`.
   - Before writing either file, read the project's existing CSS and design tokens. Apply those tokens to the `:root` block in each template so both pages match the project's visual style (Rule 4 of `coding_rules.md`).
   - Fill only the placeholders the user supplies. Do not invent or fabricate legal text. List all missing values (data controller name, contact email, DPA details, cookie policy, retention periods for privacy; legal entity name, governing jurisdiction, liability cap for terms) under "Information required from user".
   - Wire both pages to the framework's routing and link them from the site footer, side by side.
6. **Performance, caching, and mobile.** Core Web Vitals fixes, image and asset optimization, lazy loading, caching and compression per PERF-02 and PERF-05, and responsive and tap target fixes.
7. **Form validation and CTA fixes (FORM, CTA).** Add correct semantic types (`email`, `tel`, `date`), validation constraints (`min`, `max`, `maxlength`, `required`), and label associations for forms. Add `href` to anchor tags and `type="button"` to non-submitting buttons.
8. **LLMO, AISEO, and E-E-A-T fixes (approved items only).**
   - LLMO-01/LLMO-02: restructure content headings and opening paragraphs; update `llms.txt` to include a name line, one-line description, and curated page links.
   - LLMO-03: add `<cite>` elements and `cite` attributes to blockquotes on factual pages.
   - AISEO-01/AISEO-02: add FAQ sections or inline answers for conversational queries; rewrite sections to be independently readable.
   - EEAT-01: add specific details, original data, or first-person experience signals to experience-based pages.
   - EEAT-02: add author bylines and `Person` JSON-LD with `name`, `url`, and `sameAs` links; link author names to bio pages.
   - EEAT-03: complete `sameAs` on the Organization node; ensure consistent naming across pages and schema.
   - EEAT-04: force HTTPS in canonical URLs; add or complete the privacy page (RESIL-04), contact page, and about page; fix any mixed content by self-hosting the offending resource.
9. **Content and style rules.** Replace every em dash following the rule in the "Em dash and emoji handling" section below. Replace emojis with icons.
10. **Optional items, only if approved.** Open Graph, Twitter cards, brand mentions, Google Search Console, Google Analytics, and conversion tracking.

Use the templates in `assets/` (`schema_templates.md`, `robots_txt_template.txt`, `llms_txt_template.md`, `offline_page_template.html`, `not_found_template.html`). Fill them with real values supplied by the user. Never leave a placeholder like `YOUR_DOMAIN` in a shipped file. Match the project's framework: put head tags where that framework expects them rather than dropping raw HTML into a component tree. After each group, re-run the relevant part of `scripts/audit_site.py` to confirm the gap is closed.

## Step 5: Reconcile .gitignore and README.md (mandatory, every run)

This happens on every Phase 2 run regardless of the original request.

- **`.gitignore`.** Merge the bundled standard with the project's own needs. Keep all project specific additions. Never remove security, secret, temporary, IDE, AI tooling, or generated file exclusions. If the project had none, create it from `references/gitignore_standard.txt` plus any stack specific entries.
- **`README.md`.** Update it to reflect the current state: project name and description, prerequisites, setup and install steps, how to run and build, environment variables (referencing `.env.example`, never real secrets), and any new files this run introduced such as `robots.txt`, `sitemap.xml`, or `llms.txt`. If there was no README, create one. Do not use em dashes or emojis in it.

## Step 6: Write fix_summary.md

After fixing, write `fix_summary.md` covering: what changed (grouped by category, with file paths), what was approved but is still pending, what still needs information from the user, and how to verify, including any commands and the exact Lighthouse command if it was not run here. Present the changed and created files.

## Em dash and emoji handling

**Em dash.** The target character is the em dash (Unicode U+2014). When fixing occurrences in site content or code comments, choose the grammatically correct replacement rather than a blind swap: a comma when joining two clauses, a colon when introducing a list or explanation, parentheses for an aside, or a reworded sentence. Use a spaced hyphen only as a last resort. The scanner also reports the en dash (U+2013) and a double hyphen used as a dash as advisory items to review, but the em dash is the hard violation.

**Emojis.** Replace emojis with an icon. Prefer the icon system the project already uses (for example an inline SVG, an icon font class, or a component from the project's icon library). Do not introduce a new dependency just for one icon if a suitable system already exists, and do not silently delete an emoji that carried meaning; map it to an equivalent icon.

## Reference map

- `references/coding_rules.md`: the engineering and content rules including Rule 4 (never change existing UI/UX) (pillar 1).
- `references/git_policy.md`: the mandatory git policy text (pillar 2).
- `references/gitignore_standard.txt`: the verbatim organization standard `.gitignore` to merge into every repository (pillar 2).
- `references/website_criteria.md`: the full website checklist with detect, fix, and severity for every criterion, plus the "Running Lighthouse" section and the LLMO, AISEO, and E-E-A-T section (pillar 3).
- `scripts/audit_site.py`: the deterministic static scanner.
- `scripts/download_media.py`: the external media download and WebP conversion helper for RESIL-03.
- `assets/gap_identification_template.md`: the report template for Phase 1.
- `assets/schema_templates.md`: JSON-LD templates (Organization, WebSite with SearchAction, BreadcrumbList, FAQPage, LocalBusiness) using placeholders.
- `assets/robots_txt_template.txt`, `assets/llms_txt_template.md`, `assets/offline_page_template.html`, `assets/not_found_template.html`: scaffolds for the crawl and resilience files.
- `assets/privacy_page_template.html`: privacy page scaffold for RESIL-04 and EEAT-04.
- `assets/terms_page_template.html`: Terms of Service page scaffold for RESIL-05.

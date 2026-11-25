# Website Forensics

## Purpose
Inspect public websites in a read-only, rate-respectful manner to extract layout systems, typography scales, interaction patterns, and styling tokens, producing a structured teardown with measurements — never scraped bulk content.

## Use when
- Benchmarking a competitor's information architecture, checkout flow steps, or responsive breakpoints.
- Extracting a type scale, spacing rhythm, or color-role mapping from a live reference site.
- Documenting interaction patterns (navigation, search, empty/loading/error states) for design research input.
- Operating in mode(s): `research`.

## Do not use when
- Collecting inspirational imagery for moodboards (use `visual-reference-research`).
- Bulk-scraping text, images, or user data (prohibited; this skill extracts patterns and measurements only).
- Load-testing or probing for vulnerabilities (out of scope; use security skills with authorization).

## Required context
- Product requirements (which questions the teardown must answer, e.g. "how do 3 competitors structure pricing tables").
- Design tokens (target scale to map findings onto).
- Wireframe / UI view (which of our screens the findings will inform).

## Procedure
1. **Scope the questions first**: list at most 5 forensic questions (e.g. "grid columns at desktop?", "sticky nav threshold?", "font loading strategy?") — no open-ended browsing.
2. **Inspect respectfully**: use browser devtools on public pages only; honor robots.txt; throttle requests; never bypass paywalls, auth, or anti-bot measures; never republish copyrighted assets.
3. **Measure layout**: record container max-widths, grid column counts and gutters at 360/768/1280/1920 px viewports, header/footer anatomy, and above-the-fold hierarchy.
4. **Extract type and color tokens**: record font families, weights, scale steps (px/rem), line-heights, and color roles (background/surface/text/accent/border) with sampled hex values and computed contrast ratios.
5. **Document interactions and states**: capture nav behavior, search affordances, form validation style, and loading/empty/error treatments with short screen recordings or annotated screenshots.
6. **Emit the teardown**: one section per question with measurements, screenshots, and a mapping row onto our token scale; flag anything that fails WCAG AA as a caution, not a pattern to copy.

## Decision rules
- **Public pages only**: authenticated, paywalled, or bot-protected areas are out of scope.
- **Patterns, not assets**: deliverable contains measurements and descriptions; never redistributed fonts, images, or code copies.
- **Every claim measured**: viewport widths, hex values, and contrast ratios are recorded; adjectives like "clean" must pair with a measurement.
- **Respect rate limits**: automated fetching is throttled and identified; stop on 429/captcha.

## Evidence required
- Teardown document answering each scoped question with measurements and annotated captures.
- Token-mapping table with contrast ratios.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- Design specification / findings (structured teardown per target site).
- Accessibility audit scorecard (contrast, focus, keyboard notes observed).
- UI tests (assertions locking the extracted token mappings).

## Stop conditions
- All scoped questions answered with measurements, captures, and token mappings.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to design owner if findings suggest copying trade dress or protected expression rather than patterns.
- Escalate immediately if inspection triggers access controls, legal notices, or rate-limit blocks.

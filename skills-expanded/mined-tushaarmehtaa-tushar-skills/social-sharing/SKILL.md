---
name: social-sharing
description: Audit, implement, and verify canonical URLs, social metadata, preview images, and share links. Use when shared routes are missing, stale, generic, private, or incorrect.
license: MIT
---

# Social sharing

Make each important URL describe itself accurately when crawled or shared. Treat canonical identity, metadata, image delivery, and user-facing share actions as separate concerns that must agree.

## Choose the mode and scope

Use the narrowest mode that satisfies the request:

- **Audit:** inspect existing metadata and report defects without editing.
- **Repair:** correct specific routes, images, or share actions.
- **Implement:** add a complete metadata path for a new or uncovered site.

Choose the coverage separately:

- **Representative:** sample every distinct metadata behavior and route family. Use this by default for open-ended audits.
- **Exhaustive:** enumerate every finite public route and preview-image response when the user requests complete verification or the release risk warrants it. For unbounded dynamic routes, define the finite source set, query boundary, and snapshot time; report routes that could not be enumerated or fetched.

Inventory the framework, router, rendering mode, deployment origin, locales, dynamic route families, metadata helpers, image assets or endpoints, and existing share-link components. In representative mode, select routes for each metadata behavior rather than checking only the homepage. In exhaustive mode, preserve an enumeration manifest with every resolved URL and image endpoint.

Ask for the production origin, brand assets, or content fallback only when the repository and deployment configuration cannot establish them. Never ship a placeholder domain.

## Define the route contract

For every in-scope route family, determine:

- canonical URL and locale policy;
- page title and description source;
- Open Graph type and any domain-specific fields;
- preview image source, dimensions, alt text, and fallback behavior;
- whether the route may be private, noindexed, parameterized, paginated, or unavailable;
- which social platform links, native share actions, or copy-link controls are actually needed.

Do not generate share controls merely because metadata exists. When controls are requested, encode the canonical URL and share text with URL APIs rather than string concatenation.

## Implement using the repository's stack

Use the framework's supported metadata mechanism for the version installed in the project. Inspect installed dependencies and local type definitions before choosing an API.

### Framework metadata APIs

For frameworks with first-class metadata support, implement shared defaults in the root layout or document and route-specific metadata beside the route's data loader. Include canonical identity and explicit absolute-image resolution. Keep metadata generation aligned with not-found and permission behavior.

For Next.js App Router, prefer `metadataBase`, `alternates.canonical`, `openGraph`, `twitter`, and `generateMetadata` where supported by the installed version. Derive dynamic metadata from the same validated record used to render the page. Await asynchronous data and encode image-endpoint parameters with `URLSearchParams`.

For Next.js App Router preview images, check for the `opengraph-image` and `twitter-image` file conventions before writing an image route. Use a static `opengraph-image.(jpg|jpeg|png|gif)` with an `opengraph-image.alt.txt` beside it, or a generated `opengraph-image.(js|ts|tsx)` that exports `alt`, `size`, and `contentType` and returns an `ImageResponse` from `next/og`. Next.js then emits the image URL, type, width, height, and alt tags. Rules that bite (checked 2026-11-04 against the docs for v16.x; confirm against the installed version):

- The build fails if a static `opengraph-image` file exceeds 8 MB or a `twitter-image` file exceeds 5 MB.
- Since v16.0.0, `params` passed to a generated image is a Promise. Await it.
- Generated images are statically optimized at build time unless they use request-time APIs or uncached data. A per-record image needs the record's params and data that stays fresh, or it serves a stale card.

For Pages Router, Astro, Remix, SvelteKit, or another framework, inspect the project's existing head/metadata convention. If specialist implementation details are uncertain or version-sensitive, consult the framework's installed docs or official documentation rather than improvising a partial endpoint.

### Static HTML or build-time pages

Emit absolute canonical and image URLs in the generated document. For multiple pages, generate page-specific metadata from content records at build time. Avoid a single generic image when the route's identity matters and the build already has the necessary data.

### Image delivery

Whether images are static or generated, ensure the public response:

- returns a successful status and correct image content type;
- uses dimensions appropriate to the target card without relying on unsafe edge content;
- remains readable at thumbnail size;
- handles long titles, missing descriptions, non-Latin text, and unexpected characters;
- has a stable cache policy consistent with how often content changes;
- uses a deterministic fallback when route data is missing.

Do not invent customer logos, claims, statistics, or product screenshots for the card.

## Required metadata semantics

The exact emitted tags depend on framework and page type, but the resolved document should normally include:

```html
<link rel="canonical" href="https://example.com/resolved-path" />
<meta property="og:type" content="website" />
<meta property="og:url" content="https://example.com/resolved-path" />
<meta property="og:title" content="Page title" />
<meta property="og:description" content="Accurate page description" />
<meta property="og:image" content="https://example.com/resolved-image.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="Meaningful image description" />
<meta name="twitter:card" content="summary_large_image" />
```

1200x630 (1.91:1) is a safe default, checked 2026-11-04. LinkedIn requires at least 1200x627, recommends 1.91:1, and caps the file at 5 MB. The Next.js `opengraph-image` docs use 1200x630. X's card documentation page returned 404 on that date, so do not cite X docs for card sizes; confirm the X card with a real post or the compose preview.

Add platform-specific title, description, and image tags when the platform behavior or product requirements justify them. Do not assume one platform's fallback behavior is permanent.

Google also picks Search and Discover thumbnails from `og:image` and schema.org image markup, so a wrong or tiny `og:image` is a search problem too. Google warns against generic images such as a site logo, images with text, and extreme aspect ratios for that use. A text-heavy share card can be right for social and weak as a search thumbnail. When search appearance matters, also give the page's main entity a representative schema.org `image` or `primaryImageOfPage`, and report the tradeoff. Route wider search work to the `search-ready` skill.

Canonical and `og:url` values must follow the same normalization policy for scheme, host, path, locale, slash, pagination, and tracking parameters. Private or noindex pages need an explicit sharing policy rather than accidental global defaults.

## Audit findings

For each defect, report:

```text
[route family and representative URL]
Source: [file:line or generator]
Resolved value: [observed tag, URL, or image response]
Expected behavior: [route contract]
Impact: [wrong identity, missing preview, stale image, privacy risk, or broken action]
Repair: [specific source change]
Verification: [automated and deployed check]
```

Separate source-code candidates from defects confirmed in rendered HTML or image responses.

For repair or implementation work, also return:

- files and route families changed;
- metadata sources, canonical policy, and image fallback implemented;
- representative or exhaustive coverage manifest, including every enumerated image response in exhaustive mode;
- local and deployed checks with observed status, content type, dimensions, and resolved values;
- cache/debugger state and any refresh still pending;
- routes, dynamic sets, credentials, or production checks that remain unverified.

## Verify locally

Use the repository's build or development path when safe, then check representative routes programmatically:

1. Fetch the resolved HTML, not only the source component.
2. Assert one canonical URL and the expected Open Graph/Twitter fields.
3. Confirm canonical, `og:url`, and share-link targets normalize to the intended public URL.
4. Fetch every in-scope preview image: the representative set in representative mode, or every URL in the enumeration manifest in exhaustive mode. Verify status, content type, and actual dimensions, and report any untestable set.
5. Exercise long, empty, encoded, localized, and not-found metadata inputs.
6. Confirm dynamic routes do not fall back to another record's title or image.
7. Run the project's build, typecheck, and relevant tests.
8. Inspect images at full size and thumbnail size for clipping, contrast, and truthful content.

## Verify after deployment

Fetch public URLs because crawlers cannot access localhost and deployment configuration may change origins or caching. Inspect response HTML and images before using a platform's own inspector (for example LinkedIn Post Inspector) or a real share as a final confirmation. For X, use a real post or the compose preview. Record which public routes were checked and any cache refresh still pending.

Do not claim completion when only source tags were inspected or when the production origin remains unknown.

## Sources checked 2026-11-04

Re-check before relying on them if this date is more than about 90 days old or the installed framework version differs.

- LinkedIn link preview image requirements (page last updated about 2023): https://www.linkedin.com/help/linkedin/answer/a521928
- LinkedIn Post Inspector: https://www.linkedin.com/post-inspector/
- Next.js `opengraph-image` and `twitter-image` conventions (docs updated 9 Jul 2026): https://nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image
- Google preferred image from schema.org or `og:image` (doc change 2 Mar 2026): https://developers.google.com/search/docs/appearance/google-images#specify-preferred-image
- X summary card docs, 404 on the check date: https://docs.x.com/x-for-websites/cards/overview/summary-card-with-large-image

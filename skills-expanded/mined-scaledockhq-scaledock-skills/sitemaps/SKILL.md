---
name: sitemaps
description: >-
  Sitemaps: The Sitemap protocol format consists of XML tags. Covers Sitemaps 0.9. Use when publishing a sitemap. Triggers: sitemaps.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Sitemaps

The Sitemap protocol format consists of XML tags. All data values in a Sitemap must

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when publishing a sitemap.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Sitemaps 0.9 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Sitemaps XML format.** "All data values in a Sitemap must be entity-escaped."
2. **Sitemaps XML format.** "The file itself must be UTF-8 encoded."
3. **Sitemaps XML format.** "The Sitemap must: Begin with an opening `<urlset>` tag and end with a closing `</urlset>` tag."
4. **Sitemaps XML format.** "Also, all URLs in a Sitemap must be from a single host, such as www.example.com or store.example.com."
5. **XML tag definitions, loc.** "This value must be less than 2,048 characters."
6. **XML tag definitions, lastmod.** "Note that the date must be set to the date the linked page was last modified, not when the sitemap is generated."
7. **Using Sitemap index files.** "You can provide multiple Sitemap files, but each Sitemap file that you provide must have no more than 50,000 URLs and must be no larger than 50MB (52,428,800 bytes)."
8. **Using Sitemap index files.** "If you would like, you may compress your Sitemap files using gzip to reduce your bandwidth requirement; however the sitemap file once uncompressed must be no larger than 50MB."
9. **Using Sitemap index files.** "Sitemap index files may not list more than 50,000 Sitemaps and must be no larger than 50MB (52,428,800 bytes) and can be compressed."
10. **Sitemap file location.** "Note that this means that all URLs listed in the Sitemap must use the same protocol (http, in this example) and reside on the same host as the Sitemap."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

- `robots-txt`, when the work also follows that specification: `npx skills add ScaleDockHQ/scaledock-skills --skill robots-txt`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Sitemaps 0.9](https://www.sitemaps.org/protocol.html): Protocol, Sitemaps protocol, fetched 2026-10-06 (Protocol, 2026-10-06), checked 2026-10-06.

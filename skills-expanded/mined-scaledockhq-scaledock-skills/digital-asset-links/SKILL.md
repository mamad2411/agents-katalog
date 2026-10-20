---
name: digital-asset-links
description: >-
  Digital Asset Links: publish assetlinks.json statements that link an Android app to a website. Covers Digital Asset Links. Use when publishing an assetlinks.json statement. Triggers: Digital Asset Links.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Digital Asset Links

Digital Asset Links is Google's protocol for public, verifiable statements that one digital asset (a website or an app) makes about another, such as a website delegating its URLs to an Android app. Websites publish a statement list at `/.well-known/assetlinks.json`; Android apps embed one in their manifest. This skill quotes the Asset Links specification in the google/digitalassetlinks repository and Google's statement list guides.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Website operator publishing assetlinks.json, Android app developer declaring asset statements, or a statement consumer verifying them.
- Target version: Digital Asset Links (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **AssetDescriptor.** "We only support describing an entire domain at once. Note that only fully qualified domain names are permitted in the URL."
2. **Statement.** "If the source asset's delivery mechanism is secure (e.g., HTTPS or signed Android APKs), the include file must be served over SSL. Include files are only processed if the HTTP status code is 200; otherwise the content of that include file is discarded. Specifically, HTTP 30x redirects will not be followed."
3. **Website.** "The file should be served with the media type `application/json`. Any response besides HTTP 200 is treated as an error, and will result in an empty statements list."
4. **Overview.** "A statement list contains one or more statements, and a principal can have only one statement list."
5. **Website statement lists.** "For HTTPS, any connection without a certificate chain that can be verified with the trusted root list will also result in an empty statement list."
6. **Website statement lists.** "The assetlinks.json file must be served as Content-Type: application/json in the HTTP headers, and it cannot be a redirect (that is, 301 or 302 response codes are not followed)."
7. **Matching a target, website targets.** "For a website, the site scheme, host, and port must match exactly."
8. **Matching a target, app targets.** "For an app, the certificate hash and package name of the target must exactly match the application."
9. **Website target, site.** "A website target can only be a root domain; you cannot limit to a specific subdirectory; all directories under this root will match."
10. **Website target, site.** "Subdomains should not be considered to match: that is, if the statement file is hosted on www.example.com, then www.puppies.example.com should not be considered a match."
11. **Scaling to dozens of statements or more.** "A maximum of 10 include statements are allowed in a complete statement list tree."

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
- [ ] `https://<domain>/.well-known/assetlinks.json` returns HTTP 200 with `Content-Type: application/json`, without a redirect, over a certificate chain that verifies.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `apple-app-site-association`, `well-known-uris`, `json`, `uri`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Asset Links Specification (google/digitalassetlinks, well-known/details.md)](https://raw.githubusercontent.com/google/digitalassetlinks/d893749ee3c84b31f72b552a7ed333789c3235d3/well-known/details.md): Specification, Commit d893749, 2017-09-14, checked 2026-10-06.
- [Creating a Statement List](https://developers.google.com/digital-asset-links/v1/create-statement): Google developer guide, Read 2026-10-06, checked 2026-10-06.
- [Statement List Syntax](https://developers.google.com/digital-asset-links/v1/statements): Google developer reference, Read 2026-10-06, checked 2026-10-06.

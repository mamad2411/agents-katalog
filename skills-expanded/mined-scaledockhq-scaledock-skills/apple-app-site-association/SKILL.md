---
name: apple-app-site-association
description: >-
  apple-app-site-association: host the file that links an Apple app to a website for universal links, shared web credentials and app clips. Covers apple-app-site-association. Use when associating an app with a website. Triggers: apple-app-site-association.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# apple-app-site-association

The `apple-app-site-association` file is the JSON file a website serves at `/.well-known/apple-app-site-association` to associate its domain with Apple apps for universal links, shared web credentials, Handoff and App Clips. Apple documents it in the Xcode and Bundle Resources documentation; this skill quotes those pages, read from Apple's documentation JSON.

**Scope.** Apple publishes this as developer documentation, not as a versioned specification. The pages are JavaScript-rendered; the pins are the documentation JSON that backs them.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Website operator hosting the association file, or app developer configuring the Associated Domains Entitlement and handling universal links.
- Target version: apple-app-site-association (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **Overview.** "The apps in the `apple-app-site-association` file on your website must have a matching Associated Domains Entitlement."
2. **Add the associated domain file to your website.** "If your site uses multiple subdomains (such as `example.com`, `www.example.com`, and `support.example.com`), each requires its own entry in the Associated Domains Entitlement, and each must serve its own `apple-app-site-association` file."
3. **Add the associated domain file to your website.** "To add the associated domain file to your website, create a file named `apple-app-site-association` (without an extension)."
4. **Add the associated domain file to your website.** "After you construct the association file, place it in your site's .`well-known` directory."
5. **Add the associated domain file to your website.** "You must host the file using `https://` with a valid certificate and with no redirects."
6. **Add the associated domains entitlement to your app.** "Make sure to only include the desired subdomain and the top-level domain."
7. **applinks.Details.Components.** "The order that you use to specify the patterns in the array determines the order the system follows when looking for a match. The first match wins, allowing you to designate one app to handle specified URLs in your website, and another app to handle the rest."
8. **applinks.Details.Components.** "`exclude`: A Boolean value that indicates whether to stop pattern matching and prevent the universal link from opening if the URL matches the associated pattern. The default is `false`."
9. **Associated Domains Entitlement.** "If the CDN has an old version of the file, or doesn't already have a copy of the file, it connects to your web server to obtain the latest version."
10. **Overview.** "Universal links offer a potential attack vector into your app, so make sure to validate all URL parameters and discard any malformed URLs. In addition, limit the available actions to those that don't risk the user's data."

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
- [ ] `https://<domain>/.well-known/apple-app-site-association` returns the JSON over HTTPS with a valid certificate and no redirect, on every subdomain listed in the entitlement.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `digital-asset-links`, `well-known-uris`, `json`, `uri`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Supporting associated domains](https://developer.apple.com/tutorials/data/documentation/xcode/supporting-associated-domains.json): Apple Developer Documentation, Apple Developer Documentation JSON, read 2026-10-06, checked 2026-10-06.
- [applinks.Details.Components](https://developer.apple.com/tutorials/data/documentation/bundleresources/applinks/details-swift.dictionary/components-swift.dictionary.json): Apple Developer Documentation, Apple Developer Documentation JSON, read 2026-10-06, checked 2026-10-06.
- [applinks.Defaults](https://developer.apple.com/tutorials/data/documentation/bundleresources/applinks/defaults-swift.dictionary.json): Apple Developer Documentation, Apple Developer Documentation JSON, read 2026-10-06, checked 2026-10-06.
- [Associated Domains Entitlement](https://developer.apple.com/tutorials/data/documentation/bundleresources/entitlements/com.apple.developer.associated-domains.json): Apple Developer Documentation, Apple Developer Documentation JSON, read 2026-10-06, checked 2026-10-06.
- [Supporting universal links in your app](https://developer.apple.com/tutorials/data/documentation/xcode/supporting-universal-links-in-your-app.json): Apple Developer Documentation, Apple Developer Documentation JSON, read 2026-10-06, checked 2026-10-06.

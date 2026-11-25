---
name: readable-spec
description: Reads web platform specifications via WebFetch — uses the multipage HTML variant for the WHATWG HTML spec, anchor-targeted section reads for W3C TR documents and TC39 / ECMAScript. Returns the relevant section rather than the whole spec, since these documents are too large for a single fetch. Use when the URL is on *.spec.whatwg.org, w3.org/TR/, or tc39.es.
---

# Web Spec Reader

Specs are usually large single-page HTML documents. WebFetch them in sections rather than expecting the full body in one response.

## WHATWG (CC BY 4.0)

Examples: `html.spec.whatwg.org`, `url.spec.whatwg.org`, `dom.spec.whatwg.org`.

The HTML spec has a multipage variant that is much friendlier to fetch:

```
https://html.spec.whatwg.org/multipage/{section}.html
```

Use the table of contents at `https://html.spec.whatwg.org/multipage/` to find the right section URL, then WebFetch that page.

## W3C (`w3.org/TR/{shortname}`)

Read with WebFetch, optionally appending an anchor:

```
https://www.w3.org/TR/{shortname}/#{anchor}
```

W3C documents are licensed for reading and reference; do not republish or redistribute large excerpts.

## TC39 / ECMAScript (`tc39.es/ecma262`)

```
https://tc39.es/ecma262/#sec-{section-id}
```

Section IDs are stable; the user often supplies one directly.

## Strategy

1. Identify the spec and target section from the URL.
2. WebFetch with a tight prompt focused on the specific question.
3. If the page is too large to digest, jump to the anchor or table-of-contents subsection.

## Reference

- WHATWG IPR / license: https://whatwg.org/ipr-policy
- W3C document license: https://www.w3.org/copyright/document-license-2023/
- TC39 / ECMAScript: https://tc39.es/ecma262/

---
name: cite-in-code
description: Marks every value in code that came from the research - a rate limit, endpoint, price, quota, timeout, schema field or error code - with a comment naming the evidence row (E-##) and project it rests on, so a wrong number can be traced to its source and re-checked. Use while building from a Fetchproof brief, whenever a literal or schema in the code came from an external fact, or when the user asks where a number came from.
---

# Cite in code

A constant that came from a vendor's page is a claim. When the vendor changes it, the
code is wrong and nothing says why that number was chosen. One comment fixes that.

## The form

```js
// E-04 (research/EVIDENCE.md): 60 requests per minute per token on the free tier.
const RATE_LIMIT_PER_MINUTE = 60;
```

- The row ID, the file it lives in when the project is not the repository root
  (`docs/decisions/<project>/research/EVIDENCE.md`), and the fact in a few words.
- Use the project's comment syntax. Put it once, on the definition - not on every use.
- A value with no row behind it is not cited with a made-up ID. It is either the brief's
  stated intent (say so: "per the brief's decision") or a `fact-request`.

## What to cite

Rate limits and quotas, prices, endpoint URLs and versions, auth scopes, schema field
names and types, documented error codes, size and length limits, timeouts, and any
platform behaviour a branch in the code depends on.

## What not to cite

Choices that are yours (a variable name, an internal default with no external source)
- citing them dilutes the citations that matter.

## When a cited fact goes stale

`freshness-recheck` on the collector re-collects the page; a superseded row fails the
gate where it is cited, unless its quoted words survived the refresh (ADR-0193); re-read it
anyway. Search the code for the old row ID and update the value with the new one.

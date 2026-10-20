---
name: open-banking-uk
description: >-
  Open Banking UK: the Read-Write API profile for accounts, payments and
  pagination. Covers Open Banking UK 4.0. Use when calling the UK Open Banking
  Read-Write API.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Open Banking UK

The Open Banking Read-Write API Profile v4.0.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when calling the UK Open Banking Read-Write API.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Open Banking UK 4.0 (default). See `references/versions.md`.
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **# Pagination.** "In such a situation, the ASPSP MUST : If a subsequent page of resource records exists, the ASPSP must provide a link to the next page of resources in the Links.Next field of the response."
2. **# Pagination.** "For a paginated responses, the ASPSP SHOULD ensure that the number of records on a page are within reasonable limits, a minimum of 25 records (except on the last page where there are no further records) and a maximum of 1000 records."
3. **# Pagination.** "As with all other responses, the ASPSP MUST include a "self" link to the resource in the Links.Self field as described in the Links sections."
4. **# Token Expiry Time.** "Its value MUST be a number containing a NumericDate value, as specified in https://tools.ietf.org/html/rfc7519#section-2 NumericDate is a JSON numeric value representing the number of seconds from 1970-01-01T00:00:00Z UTC until the specified UTC date-time, ignoring leap seconds."
5. **# Overview.** "This profile should be used in conjunction with compatible functional profiles (such as Accounts and Transactions or Payments) and compatible resources."
6. **# Unique Identifiers (Id Fields).** "A REST resource should have a unique identifier (e.g."
7. **# Unique Identifiers (Id Fields).** "An ASPSP that chooses to populate optional Id fields must ensure that the values are unique and immutable."
8. **# Categorisation of Implementation Requirements.** "ASPSPs must make documentation available to TPPs (e.g."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> `references/versions.md`
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in `references/requirements.md` and implement each one that applies to the role.
   -> `references/requirements.md`
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the heading it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> `references/versions.md`
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in `references/requirements.md` holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Open Banking UK 4.0](https://openbankinguk.github.io/read-write-api-site3/v4.0/profiles/read-write-data-api-profile.html): Specification, Open Banking Read-Write API Profile v4.0 (Specification, 2026-10-06), checked 2026-10-06.

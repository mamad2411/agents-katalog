---
name: writing-ado-items
description: Write and clean up Wholesale Architecture Azure DevOps work items. Use whenever creating, renaming, routing, assigning, parenting, or reviewing Wholesale ADO titles and metadata. Apply the local az-ado identity rules, preserve technical meaning and useful routing identifiers, and use native az devops reads and writes.
compatibility: Requires the repository az-ado skill and its Wholesale reference. Use native az devops commands for live ADO operations.
---

# Wholesale ADO item writing

Use this skill for Wholesale Architecture work-item titles, descriptions, ownership, and parent routing. Read `skills/az-ado/SKILL.md` and its Wholesale reference first. The local repository instructions and current board state override this summary.

## Title rules

- Write titles without square brackets or parentheses. Preserve technical braces such as `lookup-values/{id}`.
- Remove SNOW request and change identifiers such as RITM and CHG from titles. Retain their history, links, or useful references in the body when relevant.
- Use a descriptive noun or outcome, not command language. Do not write forms such as `Execute CHG ...`.
- Strip a project prefix only when it is a whole leading name separated by whitespace, a colon, or a spaced dash. Do not strip arbitrary hyphens inside compound identifiers such as `decus-direct`, `decus-shared`, `doc-db`, or `Doc-cadence`.
- Do not prefix titles with `Fortify -`.
- Do not repeat product or project announcements such as `B3 Admin Tool` or `DOC project` when the parent or area already supplies that context.
- Preserve technical meaning. Do not delete useful routing identifiers in the middle of a title merely to shorten it.
- Do not use em dashes in titles or body text.
- Do not use AI branding in names or tags. Distinguish Application Insights LAW plus AI from PRimate.

## Parent and type routing

Treat these as durable epic names, matching the current board item rather than inventing IDs:

`WHS-346`, `PIPS`, `All-Wholesale`, `Decus-537`, `DOC`, `Submission Engine`, `Pips to Velocity Sync`, `Email Scheduler`, and `InsCipherProxy`.

`All-Wholesale` supersedes Legacy Subscription. `PRimate` is a Feature under `WHS-346`, not an Epic.

Use explicit ID mappings when available. They beat keyword guesses. Keep a specific Fortify automation item with its application parent. Route shared Fortify work under Fortify. Do not block an otherwise clear naming cleanup because an unrelated parent is ambiguous. Record that parent ambiguity separately and avoid guessing.

Exclude every item not assigned to one of the two approved identities, including unassigned items. Recursively exclude items whose nonempty parent chain leaves that owned project scope. A parentless owned item remains eligible. Re-read live ownership and ancestor scope before a write.

## Ownership and creation

Before any write, read the current item's owner, parent, title, type, and relevant relations. Resolve the exact identities with native Azure DevOps commands. New items are assigned to the verified O365 identity, never BBAdmin. Do not reassign items owned by somebody else.

Use native `az devops` and `az boards` commands, not a substitute REST client. For `az boards work-item show`, do not combine `--fields` with `--expand`; the installed CLI rejects that combination. Stop a batch on a systemic invocation error before repeating it across items. Discover current help before mutations. Preserve IDs and history. Writes are independent operations, so do not claim atomicity. After each write, read back the exact item and relevant fields and report any partial result.

## Workflow

1. Read the local az-ado instructions and current work items, relations, types, owners, and parents.
2. Define the owned-only scope and exclude outside-parent chains.
3. Apply explicit ID mappings before keyword rules.
4. Normalize titles while preserving technical meaning and useful routing identifiers.
5. Preview exact IDs, old values, new values, owner, type, and parent.
6. Execute only authorized naming or routing changes. Do not reassign other owners.
7. Read back every changed item. Report the exact scope, observed results, and unresolved parent ambiguity.

## Safe examples

- `Fortify - Configure application scanning (development)` becomes `Configure application scanning development`.
- `Execute CHG1234 Monthly VM patching` becomes `Monthly VM patching`, retaining the change reference in existing history or a relevant body link. Never invent deployment scope when a title becomes empty.
- `PRimate` stays a Feature below `WHS-346`, even if its title contains epic-like keywords. Application Insights LAW plus AI is separate and is not PRimate.
- Rewrite dangling `Get up to speed on DOC project` as `Review application architecture and delivery workflow`.
- A shared Fortify library routes under `Fortify`; an automation specific to one application stays with that application.

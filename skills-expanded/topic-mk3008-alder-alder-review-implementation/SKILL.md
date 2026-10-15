---
name: alder-review-implementation
description: Review completed implementation, DDL, and tests against agreed Alder Business Design. Use for "コードをAlderでレビューして", "実装したのでAlderレビューして", or "Alderで実装をレビューして、チェックとテストの対応も更新して". Coordinate authorized record maintenance after an independent read-only review. Review-only requests never write; record-only follow-up uses alder-follow-up-review.
license: MIT
---

# Review an implementation with Alder

A single request can cover review and its record follow-up. Select the scope from the user's actual words and existing authorization; do not make the user name internal skills.

## Choose the requested work

- **Review and records:** A request such as “Alderで実装をレビューして、チェックとテストの対応も更新して” authorizes the named record maintenance after review. Keep that authorization and its affected scope for the follow-up; do not ask again merely because the internal stage changes.
- **Review only:** “レビューだけ”, “変更せず”, “read-only”, or an ordinary “Alderレビューして” without record-update authorization means review without writes. Return findings. Do not infer writing permission from the package's Write capability, project write access or a review finding. If useful, offer the concrete record update once; do not require it or block the review.
- **Records only:** If the request is to apply supplied decisions or update Check-to-Test evidence from an existing review, use [follow-up](../alder-follow-up-review/SKILL.md) directly. Do not add a fresh review just to enter this workflow. A missing review is handled by that skill's existing evidence boundary.

Explicit read-only wording wins over earlier broad write permission. Clarify only a genuinely conflicting current request or missing target, not the internal choice of skills.

## Independent review, fixed inputs

Locate project instructions, requested scope and Business Design using declared paths or `docs/business-design/`. Pin the design, confirmed Checks, documented decisions, provided System Requirements (SR) and related project constraints, implementation, DDL, tests and available execution evidence to commits or an exact working-tree snapshot before review. Include each supplied SR source, revision and applicable scope, including the SR used for implementation; preserve the existing project-instruction and decision inputs. Uncommitted work is allowed, but identify the included paths and content digests so the reviewed state can be compared later. Do not create a commit merely to obtain a pin.

For review-and-records, dispatch a **separate Fresh read-only agent/context** with no conversation-history fork. Give it only the original scoped review request, pinned inputs, project instructions, installed package version/source and [read-only review stage](references/read-only-review.md). It must read the full bundled knowledge and return evidence/questions without editing files. Exclude implementer conversation, proposed fixes, prior review outputs and the orchestrator's conclusions; documented project decisions remain legitimate inputs. Follow the target project's Fresh settings when specified. Record requested settings and disclose if effective runtime settings cannot be verified.

For review-only, an already independent new context can execute the read-only stage directly. An implementation context must dispatch a Fresh reviewer instead of calling its own self-check independent.

A skill cannot create capabilities the host lacks. If separate-context execution is unavailable, state that the independent stage could not run; do not simulate a Fresh review in the same context or begin combined-workflow writes. Keep any preparation read-only and explain that an independent review result is needed to resume. A host with separate agents can complete the two stages without a second user invocation.

## Continue only the authorized follow-up

After the Fresh result, compare the current inputs with the reviewed pins. If relevant source changed, including SR revision or applicable scope, keep the old review's revision visible and re-review the changed scope before dependent updates; do not attach old evidence to a new revision. Preserve concurrent changes and continue genuinely unaffected records.

In review-and-records mode, invoke [the existing follow-up procedure](../alder-follow-up-review/SKILL.md) in the orchestration context using the pinned result, actual decisions and original write scope. The read-only reviewer never performs these writes. This does not require the user to call another skill. Update only the requested records supported by actual assertions and execution evidence; retain IDs, expectation meaning and human review states.

A Business confirmation holds only affected meaning-changing work. Continue independently confirmed mappings and report their evidence gaps honestly. Neither the Fresh finding nor passing tests answers unresolved business policy. Change Business Design only when requested and based on actual decisions; await required human confirmation before changing dependent expectations. Do not turn ordinary technical findings into business-approval gates. Code/Test fixes and their execution are not included in record maintenance; use a separately scoped implementation task if they were also requested.

Return one concise result distinguishing the independent findings, records actually changed, never-run/stale evidence, and remaining decisions or blocked steps. Report the installed Alder version from `../../plugin.json`, the product revisions, package source when known and [authority provenance](references/provenance.json). Do not claim acceptance, independent review, writes or host routing that did not occur.

---
name: sigma-legal-bid-workflow
description: "Orchestrate end-to-end Chinese law-firm bids in compatible agent environments. Use for 招标、采购、询价、磋商及投标/响应文件: guide beginners or professionals through tender-first intake; extract mandatory, scoring, pricing and submission requirements; assess private personnel and performance evidence; draft non-litigation, recurring-counsel, compliance, litigation or arbitration plans; inherit approved templates; create clean and review copies; assemble review indexes, signing and sealing materials; verify returned execution files; and deposit approved private practice lessons. Do not use as a source of current facts, laws, cases, qualifications, prices, signatures or seals."
license: Apache-2.0
metadata: {"version":"1.1.1"}
---

# 西格玛小鬼律师投标工作流

**西格玛小鬼出品｜律师投标工作流**

官方来源：[GitHub](https://github.com/kwf18423059038-pixel/sigma-legal-bid-workflow) · [SkillHub](https://skillhub.cn/skills/user_7c551cde/sigma-legal-bid-workflow)

## 作者标识的显示范围

首次使用本工作流时，在正常对话答复末尾简短显示一次上述作者标识及官方来源链接，不单独占用一轮，不延迟采购分析或材料告知。已有记录表明显示过时不再重复；使用者要求省略时停止显示。只有宿主支持持久设置时才保存显示状态，不为此新增联网验证或收集信息。

该标识只说明工具来源，不进入用户生成的标书、附件、图片、水印、页眉页脚或文件属性，也不新增强制批注署名。既有审阅稿批注作者仍按使用者设置处理。作者不因工具使用而成为投标人、服务团队成员或项目背书人。原开源许可证与业务规则保持不变。

## Core outcome

Run the bid as a controlled evidence-and-production workflow through one user-facing Skill entry. Internally route only the modules needed for the current project. Do not jump from a tender file directly to drafting. Maintain one source of truth, verify every scored or mandatory fact, route the substantive service plan by matter type, assemble only after the evidence configuration is stable, and review the exact final candidate once.

The first project result is a Chinese text message in the conversation: materials needed, already supplied, missing or needing supplementation, followed by the actual scoring, price, deadline, signature/stamp and submission requirements and a short plan. Deliver it before drafting; an internal summary is not delivery. Follow `references/guided-intake-and-review.md`. At document handoff, explicitly link the authorized commented review copy when applicable and the separate signing/submission checklist; follow `references/signature-stamp-return.md`.

Before drafting, resolve procurement lots, map shared and lot-specific requirements, present the chapter plan and bind its actual approval. Follow `references/chapter-production.md` and use `production-plan`. Review representative pages before full layout; revise individual chapters and only their dependants, then assemble the exact approved versions. Fixed Word forms remain native Word forms.

At intake, ask once whether the user wants a private practice library. When enabled, recall approved applicable lessons before chapter planning; check each against the current tender and record adoption, rejection or conflict. During work, retain actual corrections and failure evidence in the authorized private project. At closeout, propose source-bound retrospective candidates, request review before activation, and record the outcomes of later use. Disable or supersede ineffective lessons. Follow `references/project-archive-and-evolution.md`; archiving alone is not learning, a candidate is not an active rule, and local learning does not train model weights or publish private data.

Resolve `<skill-root>` to the directory containing this `SKILL.md`; some compatible hosts expose the same location as `{baseDir}`. Never place a project workspace or private performance library inside that directory.

For schema-8 workspaces, use the finite Loop Engine to persist events, dependencies and the smallest rework queue across interruptions. The engine controls work; it does not autonomously contact people, upload, draft indefinitely, sign, stamp, print or submit.

After updating the Skill, run `migrate-workspace` on an existing project before resuming, even when its schema is already 8. Workflow-feature migration preserves recorded choices; successful migration does not approve any open project decision.

If the user asks only to design, review, or improve a bid workflow, do not create a bid DOCX. Diagnose the trajectory and provide the requested workflow result. Do not modify the installed Skill unless the user separately authorizes product maintenance.

## Source boundary

The Skill contains workflow rules and deterministic utilities, not a law firm's personnel, performance, certificates, clients, matters, quotations or historical bids. Users must supply and authorize their own project sources. Never promote project material into a shared example, template or reusable rule.

## Required reading

For a first-time user or a request asking how to operate the workflow, read `references/quick-start.md`, `references/user-guide.md` and `references/guided-intake-and-review.md`. Give the user the short conversational steps, not raw schema fields or shell commands. Read `references/capability-boundaries.md` when a requested step may require human judgment, external communication, signing, stamping, uploading, submission or another action outside local drafting. Read `references/privacy-and-configuration.md` before configuring OCR, legal research, model APIs, cloud documents or shared storage. Use `references/troubleshooting.md` only for the matching problem.

For every non-trivial bid, read these references completely:

- `references/state-machine.md` for phases, gates, change paths, and checkpoint rules.
- `references/quality-gates.md` for blocking criteria and final-review discipline.
- `references/change-control.md` for event recording, dependency invalidation, local rework, freeze and execution-return rules.
- `references/loop-engine.md` when registering new sources or changes, resuming interrupted work, building dependencies, processing a local rework queue, or using any `loop-control` command.

Before the first run in an environment, or after a runtime/Skill/authentication change, read `references/environment-and-portability.md` and run the environment preflight.

Read these when the task reaches the matching stage:

- `references/requirements-and-requests.md` when extracting tender requirements or requesting missing information.
- `references/chapter-production.md` before lot selection, chapter planning, representative-page review, scoped rewriting or assembly.
- `references/evidence-and-performance.md` when handling personnel, certificates, social insurance, contracts, performance, OCR, redaction, or key-page selection.
- `references/performance-library.md` when creating, importing, searching, assessing, exporting or using a long-term private performance-evidence library. The library must remain outside the installed Skill and any shared template location.
- `references/official-public-checks.md` when a tender or qualification review requires Credit China, lawyer/law-firm registry, judicial-administration, sanction, enforcement, licence or similar official public checks.
- `references/service-plan-routing.md` before drafting any service plan.
- `references/litigation-writing-method.md` before drafting, revising, evaluating or learning from a litigation/arbitration bid service plan, including a plan that contains case analysis, legal research, claims, defences, preservation, appraisal, settlement or enforcement strategy.
- `references/portfolio-and-commitments.md` when the procurement contains multiple disputes/targets/service components, recurring counsel, compliance services, risk fees, or repeated service-level commitments.
- `references/assembly-and-submission.md` before Word assembly, review-index generation, signing/stamping, sealing, USB preparation, or delivery.
- `references/presentation-and-language-final-gate.md` before drafting a formal artifact, when learning the purchaser/reference language style, before formatting/beautification, and before the exact-candidate page review.
- `references/proofreading-gate.md` before the exact-candidate final review, even when a separate proofreading Skill is unavailable.
- `references/template-library.md` when importing historical bids, building or selecting templates, binding a template to a project, learning a reference document's format or language, or generating an overview sheet, quotation file or sealing label from a stored template.
- `references/format-component-library.md` when resolving a cover, title hierarchy, body style, table geometry, evidence page, review guide, signature/stamp block or sealing layout, and before any format beautification.
- `references/content-architecture-and-learning.md` before arranging firm introduction, honors, performance, team and service-plan modules; when applying a newly uploaded reference; or when the user requests interactive rewriting.
- `references/guided-intake-and-review.md` at every new-project intake, when switching between guided and professional modes, before validating the tender-first summary, and when creating or cleaning a Word review copy.
- `references/project-archive-and-evolution.md` before importing a historical/completed bid into a private practice library, approving a performance or template candidate, recording feedback, closing Stage 9 or exporting an approved anonymous lesson.
- `references/pdf-performance-redaction.md` before creating or verifying any black-box PDF evidence derivative. Never treat an ordinary overlay as redaction.
- `references/signature-stamp-return.md` before preparing the signature-ready Word candidate, occurrence-level execution list or review of a returned signed/stamped file.
- `references/yuandian-setup.md` when a legal/case research branch requires Yuandian-compatible access and the user's environment has not yet configured an authorized route.

When the current tender does not prescribe a mandatory sealing format, use `scripts/sealing_template.py` to create the neutral one-page A4 starting template. Generate only the package types and quotation rounds actually required by the current procurement.

## Non-negotiable controls

1. Treat the current tender and its appendices/addenda as the controlling requirement source. Verify that the procurement round and deadline are still current before production. Treat prior bids as evidence/template candidates, never as current-project facts.
2. Treat the latest user-approved human draft as the binding revision and style baseline. Change only the necessary delta unless the user asks to rebuild.
3. Separate source facts, professional assessments, commitments, assumptions, and missing facts. Never convert a blank, filename, prior assertion, or OCR guess into a fact.
4. Keep the formal artifact addressed to the purchaser/evaluator. Keep internal explanations, risk labels, requests, drafting notes, and workflow commentary out of it.
5. Preserve the tender's required forms, order, volume split, signatures, and wording. Apply format authority in this order: current tender/addendum/mandatory form; latest approved same-project human baseline; user-authorized matching reference; approved private template component; Sigma fallback. Let a higher source control only what it actually prescribes, and fill silent items from the next valid source. Inventory every available format source with its path/hash and controlled items, then bind each resolved format item and every volume order back to that inventory and any tender requirement IDs; a lower source may never control an item covered by a higher source. Do not beautify or restructure before capturing the language and formatting profiles and submission constraints. Learn the purchaser/reference document's terminology, sentence rhythm and level of formality only within its recorded source role; never copy prior-project facts or substantial proprietary passages.
6. Request user confirmation only for a material decision that cannot be resolved from sources: bidding entity, team, quote, strategic litigation position, redaction authority, or an external submission action. Do not repeat an answered question.
7. Process deltas. Reuse verified extraction, OCR, evidence pages, calculations, and accepted text when their source has not changed. Re-evaluate only affected downstream outputs when new material arrives.
8. Apply deterministic calculations to quotes, totals, rates, financial ratios, dates, ages, experience periods, and score simulations. Never calculate them casually in prose.
9. Assemble the review-guide table with the document before final pagination. Fill its directory/page references from that candidate, refresh fields and save again, then render and verify the exact saved file. A changed page count or reference reopens only the affected pagination checks. Never insert a new guide after the final page review and call the previous pagination final.
10. Before delivering a substantive package, apply both `references/presentation-and-language-final-gate.md` and `references/proofreading-gate.md` to the exact candidate. Run deterministic language/presentation checks, update fields in the designated office suite, render every page and record every page review. An installed legal-proofreading workflow may implement or strengthen the gate but is not a dependency.
11. For a physical submission that requires sealed packaging, output the project-specific envelope label/seal-strip files and print/count checklist; do not stop at a generic reminder. Skip them only when the current tender establishes electronic-only or no-seal submission, and record that source.
12. Record every material new source, decision, round change and review failure as an event before editing downstream outputs. Invalidate only actual dependants and never infer finality from a filename containing `定稿`, `修订`, `正本` or `final`.
13. Keep artifact identity consistent across filename, cover/inner cover, header/footer, original/copy label, volume, electronic file and sealing package. Treat each standalone quotation/overview sheet and each bound copy as a separate delivery instance backed by the same controlled values.
14. Never edit an original qualification/evidence source to add a project-use watermark or redaction. Create a mapped derivative, record its authority and reuse limit, and regenerate it when the procurement round identity changes.
15. Resolve the confidentiality classification and external-processing authority before sending source content to OCR, legal research, cloud document or other external services. Installation or login is not authorization.
16. Treat the user's recurring correction against internal-explanation language as an active rejection fingerprint. Unless a mandatory source or approved fixed professional use is recorded, keep `本阶段`, `现阶段`, `不宜`, `口径`, revision/comparison language, user-directed advice and unresolved-status wording out of the clean formal artifact. Any audience-contamination residue requires `REJECT — RESTART_REQUIRED`.
17. When no higher format authority controls, use the approved generic profile: Chinese `仿宋` and Latin/Western text `Times New Roman`; body 14 pt, 1.5 spacing, justified and two-character first-line indent; tables 12 pt and single spacing; document title 18 pt, level 1 16 pt, level 2 15 pt, levels 3/4 14 pt; headings bold with zero first-line indent; hierarchy `一、` → `（一）` → `1.` → `（1）`; editable text black. Preserve the original colour of evidence scans, signatures, seals and official logos.
18. At intake, resolve whether the tender prescribes all, part or none of the response order/format and whether a same-project or user-authorized reference exists. If none is supplied, make one concise offer to receive it and bind that single offer (or an unsolicited express decline) to one event and timestamp; duplicate offer events block drafting. If none remains available, present the project-specific generic format/order plan and stop before drafting until it is approved. Bind the approval to `decisions.csv`; after later material arrives, review every post-approval source event, record its invalidation/decision/rework result and confirm only an actually affected decision.
19. Run official public checks only when a tender, scoring rule, qualification review or current-risk decision requires them. Use the tender-specified official platform first; otherwise use the current competent official source. Retain the complete original page/snapshot, query identity, conditions, scope, URL, timezone-aware time and hash before cropping. An empty result supports only a bounded “as of / on this platform / under these query conditions, no record was retrieved” proposition; it never proves an absolute absence of sanctions.
20. In a schema-8 workspace, keep every actual `source/` file in `sources.csv`, classify all current sources before planning a loop, and use explicit dependency edges before automatic invalidation. Run only one foreground loop and one claimed work item at a time. Traverse every changed root, carry retry history through rebase, and stop at source, decision or external-human gates. Allow only one automatic correction/recheck for the same deterministic defect; never evade the cap by renaming the defect.
21. Classify every reusable historical document on two separate axes: matter type and artifact purpose. Record one of four use modes: exact fixed-form filling, structure/style learning, signed-layout learning, or private evidence only. Historical documents never supply current people, performance, certificates, project facts, amounts, dates, commitments, procurement rounds or quotation rounds. Personnel, performance and certificate sources remain private and claim-specific; never publish them as a reusable shared template.
22. Treat procurement iteration and quotation round as different fields. A historical title containing `第二次`, a prior second-quotation scheme, or a stored seal template cannot create a current quotation round. The quotation-round field defaults to absent and may appear on the cover, quotation form, overview sheet or sealing label only when the current procurement/addendum expressly establishes it or the user records an explicit project decision. If absent, remove the field or row rather than printing an empty `第X次` label.
23. Do not use abstract process language as outward decoration. Unless required by a controlling source and natural in context, remove `交叉验证`, `交叉核验`, `交叉检索`, `闭环管理`, `验证路径`, `核查路径`, `补充路径`, `处理路径`, `替代验证`, `模块化推进`, `联动机制`, `联动审核` and similar system-language. State the concrete legal work instead: `审阅`, `核对`, `查阅`, `访谈`, `梳理`, `分析`, `复核`, or `提出意见`. Block export when any rejected phrase or internal drafting residue remains on an outward artifact surface; rewrite the affected text and render the corrected exact candidate before delivery.
24. Resolve format by component, not by averaging an entire reference document. The title ladder must remain monotonic: document title at least 2 pt above level 1; `一、` larger than `（一）`; `（一）` larger than `1.`; `1.` not smaller than `（1）` or body text. Never use repeated spaces or full-width spaces to align cover, signature, seal or form fields. Use shared table columns, tab stops or positioned cells and verify the rendered result. Use artifact-specific table geometry for overview, performance, team and review-guide tables rather than equal-width columns by default.
25. Resolve every page type separately. Let the current tender or mandatory form control first; then select the strongest authorized reference for the specific cover, contents page, overview form, qualification section, performance page, team page, service-plan page, evidence page, evaluator guide, signing/stamping page or sealing item. Different references may supply different compatible components, but never average several documents into one global style or copy one historical bid across all pages. For a team section, use the tender-prescribed form and fields; only when silent use the fallback fields of name, project role, education and school, practice years, practising/professional certificates and the person's relevant performance, with evidence mapping. Do not collapse those fields into generic `qualification and experience`. Build the evaluator guide as a requirement-by-requirement navigation index, not a QA checklist: each eligible procurement requirement maps to the exact outward directory title and the final page or page range; split compound criteria, omit internal checks and never guess pagination.
26. Classify the primary submission genre from the current procurement's required contents, not from the presence of a price field or the word `询价`. A package that requires qualifications, performance, team, technical/service plan, commitments or evidence is a bid/response package; its quotation, overview sheet and any later quotation round are subordinate artifact instances. Treat the project as quotation-only only when the current procurement expressly limits the submission to price/quotation content. Reflect the classification in analysis priority, drafting, assembly, user interface and final review so price never displaces the tender-response main chain.
27. Separate generation blockers from post-generation execution. A current-project authorization form, commitment, overview sheet, quotation form or response document that must later be signed, stamped or electronically sealed is generated first; the unperformed mark belongs in the Stage 8 execution checklist and must not block drafting, pagination, review-guide generation or assembly. Continue to block when the content needed to generate the form is missing, including the signing entity, legal representative or authorized person, authorization scope, quotation value, mandatory wording or fixed form. This rule never excuses missing signatures or seals on historical performance contracts, client confirmations, completion records or other evidence used to prove a scored or mandatory fact. No package may be treated as ready for final submission until every required current-project signing and stamping action has been reconciled against the frozen candidate.
28. Keep law-firm introduction, honors, performance, project team and legal service plan as separate reader tasks. Start the substantive service plan only after procurement requirements, current facts, usable evidence, selected performance, team allocation and applicable commitment constraints are stable. Each outward paragraph must state a complete proposition with concrete legal work and a project result or use; do not substitute institutional publicity, fragments, slogans or machine-process labels.
29. Treat interactive user instructions as scoped project directions, not evidence. Apply the smallest sufficient rewrite, preserve unaffected structure and formatting, re-evaluate actual dependants, and keep every instruction or modification explanation out of the clean artifact. A source, template or instruction change makes the prior candidate stale and blocks export until recompilation and the applicable final checks pass.
30. Apply project changes through a finite loop that maps each verified change to the smallest dependent rework queue. Record feedback separately; do not treat it as a current-project fact or automatically rewrite the installed Skill.
31. Default a first-time user to guided mode. Professional mode may compress questions and expose technical ledgers, but it must use the same source, evidence, language, format, review, execution and privacy gates. A mode change never changes a fact or approves an open item.
32. Before drafting, give the conversational material list and tender alerts under `references/guided-intake-and-review.md`, then record the actual presentation separately from analysis completion. Validate both the structured summary and its current presentation binding when the bundled validator is available. Stage 5 is blocked without that handoff, while a critical item is open, or while a material row is marked as blocking drafting. User approval remains a separate decision; a presentation record never supplies it.
33. Correct mechanical wording automatically only when the supported proposition, degree of certainty and protected facts remain unchanged. Put unresolved current facts in real Word comments on an explicit review copy, not in body placeholders. Default the comment author to `西格玛小鬼`, ask once whether the user wants another name and store that local choice. The signature-ready clean candidate must contain no comments, revision residue, highlights used as instructions or internal-status language.
34. Create PDF performance redactions only from an authorized, unmodified original. Apply true region deletion and generate a fresh irreversible black-box derivative; then rerender it, run an authorized OCR/sensitive-term review and inspect every page for residual disclosure and proof-chain damage. Automatic output is always review-required. PyMuPDF is an optional third-party dependency under AGPL or commercial licensing; do not imply that this Skill grants or bundles a separate licence.
35. Maintain long-term performance, template components, completed projects and lessons only in a user-controlled private library outside the Skill. Intake creates candidates, not approved facts or active rules. Stage 9 may deposit an exact reviewed project only with local-retention authority. Activate a lesson only after privacy, applicability and regression review; never perform hidden training, cross-user sharing or silent self-modification.
36. Generate the clean current-project Word candidate before physical signing/stamping and produce an occurrence-level execution list. When an executed DOCX/PDF/scan is returned, compare it with the frozen candidate and require human visual review of every mark and material page. Report document and visible-execution readiness only; never claim to authenticate a signature, seal, reviewer or authority.
37. For Yuandian-dependent research, use only the user's own authorized compatible route. If none exists, follow `references/yuandian-setup.md`, state the exact enabling step and block only affected final law/case propositions. Never distribute or request another installation's implementation, endpoint, account, Cookie, token or key.

## Run the state machine

Use these stages and do not mark a stage complete without its gate output:

| Stage | Required output | Gate |
|---|---|---|
| 0. Intake | capability preflight, interaction mode, confidentiality/external-processing and private-retention decisions, source/event ledger, hashes, readable copies, task brief, artifact/matter inventory, reference availability | all controlling sources and current procurement-round identity identified; each unavailable source has an owner/action/deadline/effect; no unauthorized external processing or retention; reference status and review-comment author recorded; inventory gate may close while affected outputs remain `BLOCKED_BY_SOURCE` |
| 1. Tender deconstruction | user-facing intake summary, project basics, price/deadline/delivery alerts, five material categories, source coverage, master-fact and requirement ledgers, matter/component map, artifact-instance map, tender-format status and project plan | mandatory/scored/submission items and each prescribed order/format attribute trace to exact tender locations; the structured intake summary passes and its drafting gate agrees with every open critical/material item |
| 2. Bid feasibility | go/no-go and score-at-risk view | no hidden disqualifier; unresolved choices assigned |
| 3. Evidence configuration | people, qualification, performance, evidence and required official-public-check ledgers | each claim has admissible proof or is excluded/risk-labelled internally; every required public check has a hash-bound original snapshot and scoped conclusion |
| 4. Decision checkpoint | quote/team/redaction/strategy/service-commitment decisions, format/order plan and targeted requests | only material decisions remain; approved format plan is bound to a decision; no vague or repeated confirmation request |
| 5. Drafting | tender forms plus routed substantive service plan built from matter/service/commitment ledgers and the recorded audience/language-style profile | source grounding, natural Chinese, style fit and formal-recipient purity pass |
| 6. Assembly | artifact instances, tender-ordered volumes, evidence blocks, standalone forms, approved format profile, review index and page fields | every resolved format item uses the highest-ranked inventoried source; each volume sequence matches its source-bound requirement; identity, names, people, amounts, dates, fonts, body/table/heading rules and page references match |
| 7. Final review | clean exact candidate with no comments/review residue; language/presentation/audience audit; target-suite field update/save; hash-bound render manifest; `final_reviews.csv` and one `page_reviews.csv` row per actual page image | actual final/assembly/frozen/review hashes match; the latest current-hash review and all core page gates explicitly PASS; comment inspection reports zero residue |
| 8. Execution kit and return | signature-ready Word candidate, occurrence-level signature/stamp list, copies, USB, generated seal strips/labels, delivery checklist and returned-file comparison/review when available | each action/instance has an owner; files exist or are source-grounded N/A; every returned mark has human visual review; returned content matches the frozen candidate or explained non-substantive differences; no authenticity claim |
| 9. Archive/lessons | exact final/returned hashes, source map, private project capsule, performance/template candidates, outcome and inactive lesson candidates | local retention is authorized; no candidate is silently approved; future review uses the private archive rather than chat memory; no cross-user sharing |

Use the installed Skill root, not the current project directory, for commands:

```powershell
python "<skill-root>/scripts/run_tool.py" check-environment
python "<skill-root>/scripts/run_tool.py" init-workspace -- "<workspace>" --project-name "<name>"
python "<skill-root>/scripts/run_tool.py" migrate-workspace -- "<existing-legacy-workspace>"
python "<skill-root>/scripts/run_tool.py" loop-control -- "<workspace>" status
python "<skill-root>/scripts/run_tool.py" validate-workspace -- "<workspace>" --stage 0
python "<skill-root>/scripts/run_tool.py" summarize-status -- "<workspace>"
python "<skill-root>/scripts/run_tool.py" performance-library -- "<private-library>" status
python "<skill-root>/scripts/run_tool.py" validate-intake -- "<workspace>/working/intake-summary.json" --project-name "<name>" --stage 5
python "<skill-root>/scripts/run_tool.py" practice-library -- "<private-library>" status
python "<skill-root>/scripts/run_tool.py" production-plan -- "<workspace>" validate --stage 5
```

Keep `checkpoint.md` current for long work or interruptions. The initialized `.gitignore` protects the confidential workspace from accidental version-control inclusion by default; remove or override it only under an approved data-handling rule.

## Route the substantive branch

Classify the matter before drafting:

- **Non-litigation/transactional**: due diligence, investment, M&A, compliance, projects, advisory, framework services. Draft a project-specific method, scope, work plan, deliverables, quality controls, and sector risks. Do not list legal provisions merely to look professional.
- **Recurring counsel/compliance**: initialize `matter_type=recurring_counsel` and `portfolio_mode=recurring` (or `mixed` when combined with independent matters). Build a service catalogue and commitments ledger for scope, intake, SLA, deliverables, team, review, reporting, training, confidentiality, continuity and fee inclusion. Keep general counsel and specialist compliance components separately traceable.
- **Litigation/arbitration**: identify represented party, procedural posture, claims/defences, amounts, evidence, jurisdiction/arbitration, limitation, preservation, appraisal, counterclaim, settlement, enforcement, and likely opposing positions. For a multi-case procurement, assign a separate `matter_id`, fact/evidence/amount/quote/strategy ledger to every case before writing a portfolio summary. Verify complete current laws and cases through the user's authorized Yuandian-compatible research route before citing them. If that route is unavailable, follow `references/yuandian-setup.md` and block only the affected legal/case conclusions rather than substituting memory or generic search.
- **Specialist tax or other domain**: keep this Skill as coordinator and route only the technical branch to the narrowest installed specialist Skill. Record that dependency, its source boundary and acceptance test. If it is unavailable, block only the specialist conclusion/deliverable; do not replace it with generic prose.
- **Mixed matter**: keep a shared bid-control layer, but use separate substantive ledgers and writers for independent branches.

Follow `references/service-plan-routing.md` and, when triggered, `references/portfolio-and-commitments.md`. A non-litigation plan must not drift into litigation doctrine; a litigation plan must not be generic corporate-service prose.

## Configure evidence before writing claims

Build a requirement-to-evidence matrix. For every scored performance item, independently test:

- time window;
- required sector/subject matter;
- required service type;
- named team-member participation;
- contract/order/report independence;
- signature/seal and date;
- completion/output proof if required;
- original availability and redaction acceptability.

Do not infer a qualification from a related membership. For example, a non-practising institute membership is not an effective practising certificate. Do not infer sector fit from the client's name alone when the selected pages do not prove it.

Select the smallest evidence-page set that proves the scored facts: identity/title, scope/type, member participation, date, signature/seal, and output/sector where required. Preserve the page-to-source map. Use OCR as an extraction aid, not as evidence.

For personnel and performance appendices, map each roster/summary row to a closed evidence block and final pages. Record reused evidence blocks explicitly. Treat project-specific watermarks, copy certification and redaction as derivative states; an old project-use restriction is prior-project residue, not a reusable credential.

For required public registry, credit or sanction checks, populate `public_checks.csv` and follow `references/official-public-checks.md`. Keep the full original official snapshot and map every cropped insertion back to it. Do not equate a search screenshot with a formal certificate when the tender requires the latter.

## Request missing facts from the right owner

Never default to “ask the leader” or “ask the bid contact.” Assign each request to an operational owner:

- bidding entity/material custodian;
- HR/social-insurance or personnel-record custodian;
- proposed team member;
- performance-contract/original holder;
- pricing decision owner;
- seal/signature/authorization custodian;
- purchaser or procurement agent for a written clarification;
- official public source for current registries.

State the exact missing fact, acceptable proof, why it matters, deadline, and consequence. Keep the request outside the formal bid. See `references/requirements-and-requests.md`.

## Use agents selectively

Keep one coordinator and one source of truth. Use a single agent for ordinary bids. For a genuinely large or high-stakes package, use at most these bounded independent lanes when available:

1. tender requirements and packaging lane (read-only);
2. personnel/performance evidence lane (read-only);
3. substantive service-plan lane (one primary writer).

Use only one independent final reviewer. Do not allow recursive delegation, duplicate searches, or multiple writers for the same artifact. Give every lane the control brief, source paths, accepted corrections, deliverable, and acceptance test. The coordinator resolves conflicts and assembles the final candidate.

## Integrate installed specialist workflows

Route only the branch that is actually needed; do not invoke every installed Skill merely because it is available:

| Need | Route | Boundary |
|---|---|---|
| DOCX creation, targeted editing, field refresh, render and page inspection | `documents` | preserve the tender/approved baseline; do not rebuild an existing DOCX when a targeted edit will preserve it |
| Scanned PDF, image-only page, certificate or evidence screenshot | `paddleocr-vl` | first-choice extraction route; OCR never proves authenticity, signature, seal or mutual execution |
| Source-grounded outward prose and purchaser-facing register | `source-grounded-deliverable-writing` | admit only supported, necessary outward propositions; keep analysis and drafting explanations outside the artifact |
| New isolated legal-document structure not covered by a narrower bid branch | `legal-document-generator` | fallback structural drafting only; tender forms, this orchestrator and any narrower specialist remain controlling |
| Litigation/arbitration service-plan substance | `litigation-service-plan` | use after party, posture, facts, evidence, amounts and strategy boundaries are verified; it does not replace tender deconstruction |
| Current laws, judicial interpretations, complete provisions and cases | user's authorized Yuandian-compatible route; configure under `references/yuandian-setup.md` | retrieve and read complete current originals; public Skill supplies no private implementation or credentials; if unavailable, block only affected legal/case conclusions |
| Quote, ratio, score, fee and other deterministic calculations | `spreadsheets` or the matching calculation workflow | keep formulas and inputs auditable; do not calculate material values casually in prose |
| Exact-candidate typo, language, source, consistency, audience-purity and document-mechanics review | `legal-proofread` plus `references/proofreading-gate.md` | perform one integrated final review; do not leak review comments into the clean artifact or stack duplicate full reviews |
| Tax or another specialist domain | the narrowest matching installed specialist | return only the bounded technical result to the bid source of truth |

Do not invoke legal visualization, a timeline or a relationship chart by default. Use `legal-visualization` only when the current tender expressly requires a visual deliverable or a complex litigation issue cannot be communicated adequately in prose or a compact table, and keep it outside the response package unless its artifact instance is approved.

The tender and latest approved baseline remain controlling even when a specialist Skill is used.

## Run deterministic checks

Before final review, run:

```powershell
python "<skill-root>/scripts/run_tool.py" validate-docx -- "path/to/candidate.docx" --control "path/to/control.json"
python "<skill-root>/scripts/run_tool.py" audit-language -- "path/to/candidate.docx" --control "path/to/control.json"
python "<skill-root>/scripts/run_tool.py" audit-presentation -- "path/to/candidate.docx" --control "path/to/control.json" --reference "path/to/latest-approved-baseline.docx"
```

Use `--reference` when a controlling DOCX baseline is compatible with direct structural comparison. If the controlling baseline is PDF or another non-DOCX form, record its exact hash/profile and compare the rendered candidate visually instead of pretending it is absent. Omit `--reference` only when no compatible DOCX reference exists and the applicable format profile is fully recorded. Do not treat these deterministic tools as semantic proofreading or visual review. After target-suite field update and save, create a render manifest with a timezone-aware `rendered_at`, inspect every actual page image, and bind the final, assembly, frozen, manifest and page-review hashes to the same candidate. Require `fields_refreshed_at <= saved_at <= rendered_at <= reviewed_at`; a truncated or undecodable PNG never counts as a rendered page.

Use `run_tool.py evaluate-performance` on the performance ledger before selecting projects. Treat its result as a gate aid, not as a substitute for legal/procurement judgment.

For private historical Word intake, first inspect `image_inventory` and `ocr_required_images`. Use `export-word-images` to export exact embedded bytes into the authorized private workspace, then the user's configured OCR route. Reimport the source-bound, reviewed image transcript under `evidence-and-performance.md`; a readable cover never closes unread scanned attachments. Before reusing a private template or lesson, use `practice-library recall` under `project-archive-and-evolution.md`. Apply only approved component mappings with `apply-template-layout`; preserve current tender priority and render the result. See `format-component-library.md` for the detailed layout mapping contract.

Use `word-handoff prepare` and `word-handoff validate` under `signature-stamp-return.md` for the actual editable Word and its separate signing/submission checklist. Review-copy handoff is independent of Stage 7/8; later signatures and seals are not prerequisites to handing over Word. The clean Stage 7 candidate must have its own validated handoff. Never count a generated checklist as actually sent without presenting its usable link to the user.

For an explicit review copy, use `review-comments prepare` only after the issues and unique body anchors are fixed. Resolve every issue, generate a new clean candidate, run `review-comments inspect`, and require zero comment residue before Stage 7. `review-comments strip` removes comments only; it never approves the proposition, accepts revisions or establishes signing readiness.

For an authorized PDF evidence derivative, use `pdf-redaction redact`, then `pdf-redaction verify`, authorized OCR and literal page review under `references/pdf-performance-redaction.md`. A generated report or absent searchable text never removes the human review requirement.

When a signed/stamped file is returned, use `signed-return-review compare` against the frozen candidate and its occurrence list. Bind a human visual review to the exact report and use `signed-return-review finalize`. Do not mark it ready merely because text or page counts match.

At Stage 9, use `practice-library archive-project` only when private local retention is authorized. Keep extracted performance, template and lesson records as candidates until their separate approval gates pass.

After content freeze, mark approved rows in `requirements.csv` with `guide_include=true`, split every compound requirement that needs a distinct response location, and populate final `guide_category`, `guide_item`, `guide_score` when stated, `guide_requirement`, `guide_directory_title` and `guide_page` fields. Use `run_tool.py generate-review-guide --control <workspace>/control.json` only when the tender does not prescribe a different mandatory form. The external guide is a navigation index for evaluators: its directory title must exactly match the final response heading and its page must come from the exact paginated candidate. Treat a blank, placeholder, stale, illegal or guessed page reference as blocking. If the same quotation/overview form must appear both inside a volume and as a standalone sealed item, generate and verify both artifact instances from the same approved content source.

For physical sealed submission, populate `sealing.csv`, prepare a UTF-8 JSON configuration from its verified rows, and run:

```powershell
python "<skill-root>/scripts/run_tool.py" generate-sealing-labels -- "path/to/sealing-config.json" --output-dir "path/to/final/sealing" --control "path/to/control.json"
```

The launcher selects a known `python-docx` interpreter. If none is available, it blocks only DOCX generation and reports the enabling step.

Render every generated DOCX and reconcile its output count against `sealing.csv` before marking Stage 8 complete.

## Deliver according to the user's requested mode

- For a plan/review/diagnosis request, report findings and do not create or mutate bid artifacts.
- For a build request, deliver the requested artifact only after the relevant gates pass.
- Do not deliver QA renders, OCR dumps, ledgers, or internal reviewer notes unless requested.

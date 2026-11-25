---
name: rfp-writing
description: Write or review technical RFP documents from the issuer's perspective in Traditional Chinese (需求規格書 / 需求規劃書 / 招標規格), enforcing structural rules for redundancy elimination, appendix bloat, thin-section consolidation, and formal plain-language style. Trigger only when the user explicitly asks for an RFP; do not invoke for migration plans, runbooks, ADR/ARB, design docs, meeting minutes, vendor-side bid proposals (投標提案 / RFP responses), or general formal Chinese writing — those conventions conflict with RFP rules.
version: 1.0.0
license: MIT
compatibility: Any AI coding assistant that supports agentskills.io SKILL.md format (Claude Code, Cursor, VS Code Copilot, Hermes Agent, OpenHands, etc.) or OpenClaw. No external tools or APIs required.
metadata:
  author: Lu Yi
  tags: writing rfp procurement zh-tw traditional-chinese
  agentskills_spec: "1.0"
  openclaw:
    emoji: "\U0001F4CB"
---

# Technical RFP Writing & Review

Review or draft technical RFP documents. Enforces clear structure, eliminates redundancy, and maintains formal plain-language style (Traditional Chinese).

## Output Language

Match the language of the user's request, and apply it to *all* user-facing output — option labels, generated-document headings, table column names — not just prose. If the user explicitly asks for another language, that wins.

Language follows the request, not the source material. When the user writes in Chinese but the uploaded document, code, or reference is in English, output stays Chinese.

If the request is in Chinese, use Traditional Chinese (Taiwan business usage) and keep established technical terms in English.

The English in this file is structural labelling for you, not literal output. Never mirror this file's language into your response.

## When to Use

Trigger only when the user's request explicitly names one of these artifacts:

- RFP (Request for Proposal) — reviewing, drafting, or section editing
- 需求規格書 / 需求規劃書 / 招標規格書 / 招標文件
- Vendor requirement specification being sent out for bidding

## When NOT to Use

The following are adjacent but distinct — each has its own conventions that conflict with RFP rules:

- Migration plans, test plans, deployment plans
- Runbooks, SOPs, operational procedures
- ADR / ARB / architecture decision records
- Design docs, technical specifications (internal)
- Meeting minutes, decision memos, stakeholder pre-reads
- General technical documentation (README, onboarding, API docs)
- Vendor-side bid proposals or RFP responses (投標提案) — this skill is for the RFP issuer, not the responder

For general formal Chinese writing discipline (avoiding AI-isms), invoke `avoid-ai-writing` or `clean-ai-writing` instead. Those skills apply broadly; this one does not.

## Review Checklist

Audit the document in this order. Fix issues top-down: structural problems first, then language.

### 1. Section Placement

Each section must sit under the parent that owns its concern. Common misplacements:

| Content | Wrong parent | Right parent |
|---------|-------------|-------------|
| Artifact storage, security scanning | Core service | Deployment & release |
| Monitoring & auto-rollback | Service lifecycle | Observability |
| Canary deployment strategy | Service lifecycle | Deployment & release |
| Decommission / retirement flow | Service lifecycle | Operations |

**Action**: If a section's content belongs to 2+ other sections, it should not exist as a standalone section. Split and merge into the correct owners.

### 2. Redundancy Elimination

Before writing any requirement, check if it is already covered elsewhere:

- Cross-cutting concerns (signing, scanning, audit logging) are typically covered by a general deployment/release section. Do not repeat them in domain-specific sections.
- Cross-references (e.g., "see 3.1.5.1") are acceptable. Restating the same requirement in both places is not.
- When deleting a section, grep the entire document for its section number and update all references (tables, cross-references, footnotes).

### 3. Pain Point Filter

Every requirement must address a real pain point. Ask:

- Is this specific to the domain (e.g., artifacts are 100GB+ -- genuinely different from typical deployments)?
- Or is this standard practice already covered by general infrastructure (e.g., checksum verification -- any package manager does this)?

If it's standard practice, delete it. Only keep domain-specific requirements that would not be met by the general process.

**Infrastructure standard practice test**: If a section could appear verbatim in any K8s/cloud platform RFP with zero modification (e.g., secret management, HA control plane, CPU sizing, backup/restore), it is infrastructure boilerplate, not a domain-specific requirement. Either delete it or move it to the infrastructure layer where it belongs — do not give it a standalone section in the application layer.

### 3b. Cross-Section Consistency

After editing a section, check that its content does not contradict design principles stated elsewhere in the document. Common violations:

- One section says "不依賴本地儲存" while another section's design requires local storage
- Appendix defines baselines as "由廠商提出" while main body references those baselines as acceptance criteria

**Action**: Grep for key terms (design principles, architecture choices) and verify all sections align.

### 3c. Appendix Bloat

An appendix earns its place only if it adds concrete, quantifiable information not already in the main body. Kill appendices where:

- Most rows say "由廠商提出" or equivalent — that is not a baseline, it is punting the requirement
- The concrete values (e.g., 99.9% uptime, RPO/RTO numbers) are generic enterprise standards already implied by main-body sections
- The appendix merely restates requirements from the main body in table form

**Action**: Move any concrete numbers worth keeping into their parent sections, update all references, then delete the appendix.

### 3d. Thin Section Consolidation

A section with only 1-2 bullet points and no opening context explaining **why it matters** is a sign it does not justify standalone existence. Merge it into the nearest parent or sibling section as additional bullets or a short paragraph.

**Test**: If removing the section header and indenting its content under a neighbor loses zero information, the section should not exist independently.

### 4. Section Justification

A section earns its place by meeting **both** criteria:

1. **Has a concrete use case** in the current or next phase
2. **Has enough substance** to warrant standalone treatment (opening context + 3+ requirements)

Decision tree:

- **Has first-phase use case + sufficient substance**: Keep as a full section with requirements.
- **Has first-phase use case but thin (1-2 bullets)**: Merge into the nearest related section.
- **Has second-phase use case with clear scope**: Keep as a subsection or remark (blockquote) under the related first-phase section.
- **No concrete use case, only "might need later"**: Demote to a one-sentence remark. Do not create a standalone section for speculative needs.

### 5. Reference Integrity

After any structural change (section move, delete, renumber):

1. `grep` the full document for the old section number
2. Update every reference: tables, cross-references, blockquotes, appendices
3. Verify zero remaining references to deleted sections

---

## Language Rules

### Mandatory: Complete Sentences

Every bullet point must be a complete sentence that explains **what** and **why**. Reject:

```
BAD:  - 持久卷（PV/PVC）
BAD:  - HA（控制面與關鍵服務）
BAD:  - 備份/還原（設定、資料、索引）

GOOD: - 所有儲存須透過 CSI 驅動掛載為持久卷（PV/PVC），不依賴節點本地磁碟。
GOOD: - 控制面與關鍵服務須部署為高可用架構，單節點故障不中斷服務。
```

### Mandatory: Section Context

Each section must open with 1-2 sentences explaining **why this matters** before listing requirements. The reader needs to understand the problem before reading the solution.

```
BAD:
#### 3.3.2 儲存
- PV/PVC 支援
- 高吞吐
- 分層儲存

GOOD:
#### 3.3.2 儲存
本平台的儲存需求與一般應用不同：核心檔案動輒數十 GB，索引需要持續高吞吐讀寫，稽核日誌須長期保留且不可竄改。

**需求：**
- 所有儲存須透過 CSI 驅動掛載...
```

### Prohibited Patterns

| Pattern | Example | Fix |
|---------|---------|-----|
| AI filler words | 確保、從而、旨在、進而、致力、賦能、全面地、有效地 | Rewrite directly. 確保 -> 使; delete filler entirely. |
| Chinese slash enumeration | 輸入/輸出、角色/權限/用途、熱/溫/冷 | Use 頓號：輸入、輸出；角色、權限、用途。English technical terms keep slash (see Allowed Patterns). |
| Summary table noise | 摘要表中用括號補充細節：`核心服務（含快取機制）` | 摘要表只寫項目名稱，細節留給對應章節。`核心服務` 即可。 |
| Contrarian structure | 不是 A 而是 B; 並非 A，而是 B | State B directly without negating A. |
| Hedging | 可能、若 (as uncertainty) | Use definitive language. 可能需要 -> 須; 若不大 -> delete the hedge. |
| Vague official-speak | 應審慎評估、有待觀察 | State the concrete criteria or action. |
| Noun-phrase bullets | `C: A + B` format; bold-colon shorthand | Write a full sentence. |
| "此外" as paragraph glue | 此外，大型模型... | Merge into the previous sentence or start a new paragraph without the connector. |
| Copula inflation | 作為、扮演著...的角色 | Use 是 or rewrite. Only flag when inflating a simple "is" relationship. |
| Significance inflation | 至關重要、不言而喻、眾所周知、不容忽視 | Delete or state concretely why it matters. |
| AI sentence templates | 在當今...的時代、隨著...的快速發展、值得一提的是、這不僅...更是... | Delete the frame; state the fact directly. |
| Synonym cycling | Rotating synonyms for the same concept within a paragraph (開發者...工程師...從業者...建構者) | Pick the clearest word and repeat it. |
| Superficial -ing analysis | 象徵著...的承諾、反映了...的投入、展現了...的決心 | State the specific fact or delete. |
| Formulaic challenge | 儘管面臨挑戰...仍持續成長 | Name the challenge and the response, or delete. |

### Allowed Patterns (do not flag)

| Pattern | Why it's fine |
|---------|--------------|
| Em dashes for technical explanation | `AWQ / GPTQ -- 將精度從 16-bit 降至 8-bit` is standard in technical docs |
| Bold labels in requirement lists | `**Identity**: each system has a unique ID...` is standard RFP format |
| Bullet-heavy sections | RFPs are list-oriented documents by nature |
| "不是" for concept boundary | `管理粒度是資料集，不是租戶` is a factual boundary, not a contrarian structure |
| "作為" in factual role assignment | `以 X 作為 Y 引擎` is stating a technology choice, not copula inflation |
| "提升" in technical context | `用於提升排序品質` describes a component's function, not empty praise |
| 具體而言 as list intro | Acceptable when followed by concrete items; it is a list introducer, not filler |
| English term slashes | `JWT / OAuth2`, `SSE / WebSocket`, `AWQ / GPTQ / INT8` — standard notation for alternative technologies |
| Structured uniformity | RFPs are inherently structured and uniform; do not break formatting conventions for the sake of "rhythm variation" |

---

## Workflow

### Reviewing an existing RFP

1. Read the full document first
2. Run structural checks (placement, redundancy, pain point filter, justification)
3. Propose structural changes as a table: section, problem, proposed action
4. Get user confirmation before editing
5. After structural edits, run language audit (grep for prohibited patterns)
6. Fix language issues
7. Final grep to verify no prohibited patterns remain
8. Offer `avoid-ai-writing-zh` as a deep de-AI pass over the final draft; run it only if the user agrees

### Drafting a new section

1. Start with 1-2 sentences of context (why this section exists)
2. Add `**Requirements:**` header
3. Write each requirement as a complete sentence
4. Cross-check against existing sections for redundancy
5. Run language audit before presenting to user
6. Offer `avoid-ai-writing-zh` as a deep de-AI pass before presenting; run it only if the user agrees

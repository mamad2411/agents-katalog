---
name: knowledge-doc-writing
description: >-
  把自學或研究一個技術主題的成果，整理成一份包含四個清楚分離 Diátaxis 區塊的知識文件——tutorial（帶著上手）、
  how-to（照著完成任務）、reference（查參數與結構）、explanation（What/Why 論述與取捨決策）；用 compass
  兩問把每段素材路由到對應區塊，素材撐得起才寫，撐不起的型（研究過但未實作常缺 tutorial/how-to）明列為缺口，
  不捏造、不搭空殼（繁體中文為主、術語保留英文）。觸發：使用者要把對話紀錄、官方文件或原始資料、或從零研究的主題
  （強制查一手來源並標 as-of 時效）消化成可長期參考的技術文件；或改寫一份既有技術文件——依意圖分流：
  更新時效／併入新素材→定點修補保留原形，重整／重構→依 compass 重建四型區塊。可接在 learn-loop 之後：
  learn 管互動學習迴圈與親手 distillation（鐵律：distillation 是學習本身，不代寫），
  本 skill 只接手 distill 完成後重新組織、補讀者上下文、套完稿檢查。不要用於：公司內部簽呈／會議紀錄／
  評估報告等行政文件（用 formal-doc-structure，即使輸入是既有文件也不因此轉入本 skill）、RFP／招標規格
  （用 rfp-writing）、部落格文章（用 blog-writing-zh）、只做語言層去 AI 味不動結構（用 avoid-ai-writing-zh）、
  只要口頭白話解釋不產文件（用 plain-speak）、learn 的互動學習迴圈本身（用 learn-loop）。
version: 2.0.0
license: MIT
compatibility: Any AI coding assistant that supports agentskills.io SKILL.md format (Claude Code, Cursor, VS Code Copilot, Hermes Agent, OpenHands, etc.) or OpenClaw. No external tools or APIs required; source-verification steps assume web access when available.
metadata:
  author: Lu Yi
  tags: writing knowledge-doc self-learning diataxis zh-tw traditional-chinese
  agentskills_spec: "1.0"
  openclaw:
    emoji: "📚"
---

# Knowledge Doc Writing — Turning Self-Study into Diátaxis Four-Type Docs

Turn a technical topic (self-study output, conversation transcripts, or raw source material) into **one document with four cleanly separated Diátaxis sections**: tutorial (walks a first-time reader through hands-on use), how-to (guides an already-competent reader through a task), reference (looks up parameters and structure), explanation (What/Why argumentation and trade-off decisions). The four sections never mix — cross-type content is cross-linked, never inlined.

**Only write what the material can support.** Use the compass's two questions to route each piece of material to its section; a section with material support gets written fully and stays pure, and a section that can't be supported (often tutorial/how-to, when the topic was researched but never hands-on) is listed as an explicit gap with the condition needed to fill it — **never fabricate, never build an empty shell**.

**Default technical context:** enterprise architecture in financial services, Kubernetes / OpenShift, microservices, AI platforms, RHEL + rootless Podman + Quadlet. Draw examples and comparisons from this context first, so the document reads like real work rather than a textbook generality. Declared once here; later sections reference it without restating it.

Plain language throughout; keep established terms in English (see S5).

## Output Language

Match the language of the user's request, and apply it to *all* user-facing output — option labels, generated-document headings, table column names — not just prose. If the user explicitly asks for another language, that wins.

Language follows the request, not the source material. When the user writes in Chinese but the uploaded document, code, or reference is in English, output stays Chinese.

If the request is in Chinese, use Traditional Chinese (Taiwan business usage) and keep established technical terms in English.

The English in this file is structural labelling for you, not literal output. Never mirror this file's language into your response.

## S1. Before Starting: Positioning, Input Mode, the Mode D Intent Gate

Ask everything up front, before writing a word; when unsure, ask the user:

1. **Document positioning** — learning notes (first person allowed, open questions allowed) / formal document (objective statement, spec-manual register, no second-person coaching voice) / hybrid (formal body, learning scaffolding collected in a closing appendix). Positioning decides both the first-person voice and the opt-in modules' posture.
2. **Input mode:**
   - **A — Distilling a conversation transcript.** The material is the final, repeatedly-corrected understanding reached in the conversation; a claim that got overturned mid-conversation becomes an explanation common-misconception entry, verified against sources; a question left open and self-flagged by the user goes into the explanation appendix's to-verify list under the opt-in exception (see S3).
   - **B — Organizing raw source material.** Official docs, specs, meeting notes — this is a *reorganization*, not a summary; hand it to the S2 compass to reorder by "which need it serves," not by the source's own table of contents.
   - **C — Researching a topic from scratch.** The user gives only a topic name; **do the source research before writing a word** (see S6, primary sources), and for fast-moving topics prefer material from the last 12–18 months.
   - **D — Rewriting an existing document.** See the intent gate below.
3. **Handoff from `learn-loop`** (a variant of A/B, a hard rule): this skill is downstream of `learn-loop` and **must not cross that division of labor**. Distillation — digesting material into one's own words, judging whether it's actually understood — is always `learn`'s job, done by the user's own hand; what this skill receives is already-distilled understanding, and its only job is writing it up for an external reader. Understanding already settled in the vault becomes the explanation backbone directly, without redoing the distillation; fill in context for third-party readers; rewrite or drop `[[wikilinks]]` and YAML block tags; carry forward `learn`'s already-verified sources, updating the as-of date to publication time.

**Mode D intent gate** (when handed an existing document, clear this gate first — gate on *intent*, not on the verb used):

- **Topic filter first.** This mode only accepts technical knowledge documents. Administrative documents — 簽呈, meeting minutes, evaluation reports — route to `formal-doc-structure` even in a format that looks "foreign" to it: the verb is "rewrite," but that doesn't change ownership.
- **Intent = refresh currency / fold in new material → point-patch.** Keep the input's original shape (even if it was already this skill's four-type structure, or a single-block draft) and change only the parts affected by staleness or new material. **The point-patch path never enters the S2 compass and never reorders the whole document.**
- **Intent = reorganize / restructure → hand to the S2 compass to rebuild the four sections.** Re-route the material through the compass.
- Before writing, ask whether this is a conservative rewrite or a from-scratch reproduction — don't assume. See [references/rewrite.md](references/rewrite.md) for the document-provenance signals (this skill's own scaffold vs. an outside tutorial / feature list / AI-ghostwritten draft — fluency ≠ having a scaffold), the asymmetric cost of misjudging it, the boundaries of the four scenarios (restructure / refresh currency / fold in new material / quality upgrade), and the rewrite-note format.

**Completion criterion:** positioning and input mode are both determined, with every uncertainty asked up front before writing starts; for Mode D, the document's provenance and intent branch (point-patch vs. compass rebuild) are classified, and conservative-rewrite-vs-reproduce has been asked. Classifying as point-patch but still running the compass reorder, or handling a `learn` handoff by redoing the distillation, is a failure.

## S2. Compass Routing: Assign Every Piece of Material to Exactly One Section, Flag Gaps for Unsupported Types

This is the load-bearing router; all four sections are downstream of it. For **every piece of material**, ask two questions:

1. **Action or cognition?** — does it have the reader *do* something (action-oriented), or build understanding (cognition-oriented)?
2. **Acquisition or application?** — does it serve the reader while they're acquiring the skill (at study), or while they're applying a skill they already have (at work)?

The two answers mechanically point to exactly one type:

| | Acquisition (at study) | Application (at work) |
|---|---|---|
| **Action** | Learning → **tutorial** | Goals → **how-to** |
| **Cognition** | Understanding → **explanation** | Information → **reference** |

Produce an auditable **material → section assignment table**. Rules:

- **One passage spanning two quadrants is a split signal:** split it and place each half in its own section — never inline-mix.
- **A quadrant with no material routed into it is a gap:** mark it as pending (e.g. "pending actual deployment"), never fabricate content to fill it.
- **Sub-route pitfalls/steps by reversibility:** reversible, safe operations → a tutorial callout; irreversible, production-risk operations → a how-to warning.

**Completion criterion:** every piece of material in the document has been run through both questions, assigned to exactly one of the four types, and logged in the assignment table; material spanning two quadrants has been split and placed; every one of the four types is explicitly marked either "material-supported" or "gap + pending condition" — no third state. Starting to write any section without the assignment table backing it is a failure.

## S3. The Four Sections: Only Write What the Material Supports, Write Each to Full Purity

Per the S2 assignment, **only write sections with material support**, and hold each to its boundary. A gap-type section gets one line noting the gap, not prose. The full generation rules for all four types, good/bad examples, the five-piece comparison recipe, digestion-module technique, and the opt-in appendix format live in [references/blocks.md](references/blocks.md) — **read it before writing any section**. Below are the boundary specs per type (purity isn't delegated to the linked file — it's written into the completion criterion):

- **explanation** (understanding-oriented, the only section allowed to carry judgment): a three-part What/Why argument (positioning / the problem it solves / core functional requirements — written as full-sentence paragraphs, not noun-phrase bullets) **plus a five-piece comparative recipe as an internal device** (definition → behavioral/responsibility boundary → comparative analysis → boundary-judgment table → decision framework, including substantive content on "when not to use this" — **it never becomes its own top-level scaffold**); ADR-style decision rationale (context / options / consequences / basis) woven into the argument and pointing back to earlier stated facts, not broken out as a separate module; mental models and analogies, common misconceptions, and argumentative discipline (every judgment sentence has prior context, a stated reason, or a source). The opt-in appendix lives here (see below).
- **reference** (information-oriented): **describe-only**, neutral, mirrors the product's own structure, includes flags and parameters; no recipe, no opinion, no argument.
- **tutorial** (learning-oriented): a single safe straight line, surprises eliminated, first-person-plural imperative voice ("We…" / "Notice that…"); no explaining, no chasing completeness, no real-world branching.
- **how-to** (task-oriented): assume competence, goal-oriented, if-then conditional branching allowed; no teaching, no digression; the heading states exactly what it demonstrates.

**Opt-in modules** (a Feynman-style self-explanation, a to-verify question list): off by default, living in **the explanation section's appendix**; the write-up technique is in blocks.md. Placing them under explanation is backed by the compass quadrant: Feynman = reflection-after-practice = cognition + at-study; to-verify = a working record of understanding gaps, likewise understanding-oriented. Two triggers turn it on: (a) the user explicitly asks for it ("check my understanding" / "add a Feynman self-explanation" / "add a to-verify list"); (b) the exception clause — the input material (e.g. a conversation transcript) contains an unresolved question the user flagged themselves and would otherwise be lost, in which case the to-verify list is included regardless, with a concrete "how to verify this" attached to each item. Never appears in formal-document mode.

**Completion criterion:** every section with material support is written to its boundary's purity — reference carries no argument and no recipe; explanation is argumentative prose with the five-piece recipe kept internal (a standalone five-piece scaffold appearing at the top level is a failure), and "when not to use this" has substantive content; tutorial is a single safe straight line with no real-world branching and no explaining; how-to assumes competence, allows if-then, and doesn't teach; every gap-type section is a single one-line gap note; opt-in modules appear in the explanation appendix only when triggered, and never in formal-document mode.

## S4. Keeping the Sections Separated

After drafting, self-check against the **two adjacent-pair confusions** the map predicts (adjacent types share one dimension, so they're the easiest to blur):

- **tutorial ↔ how-to** (both action, differing on **at-study vs. at-work**): the most damaging blur — it blocks a beginner. Pull any real-world branching that leaked into tutorial back out into how-to.
- **reference ↔ explanation** (both carry propositional knowledge, differing on **describe vs. discuss**): pull any argument that leaked into reference back out into explanation.

Turn cross-type content into a **cross-link**, never inline-mixed content. Detailed discrimination tests for both pairs are in [references/blocks.md](references/blocks.md).

**Completion criterion:** both adjacent-pair self-checks have been run; no section contains content belonging to another type (no real-world branching inside tutorial, no argument inside reference); every cross-type reference is a link, not an inline paragraph. Skipping the self-check, or leaving either blur in place, is a failure.

## S5. Language and Formatting (Including the HTML Edition)

Rules shared across all types, independent of routing — apply them no matter which section you're writing:

- **Plain language first — the reader gets it on one pass.** Say it plainly rather than stacking jargon, hedging in bureaucratic register, or writing long, tangled sentences. Formal-document mode tightens the *voice* (objective statement, no first person), not the sentence difficulty — a spec-manual register is still plain. Plain doesn't mean abbreviated: use full nouns and full verbs, and write in complete sentences.
- **Keep established terms in English** (API, sidecar, control plane) — standard practice in Taiwan technical writing; don't invent a Chinese translation for a term with no settled one.
- **Three-layer continuity** (section / paragraph / list — applies to lists in every section, not just explanation): open a section with one line stating its relationship to the previous one; connect paragraphs with a transition word or a backward reference that carries the causality; every list gets a **lead-in sentence** (stating what kind of collection this is — parallel/exhaustive, sequential, or mutually exclusive), states the ordering explicitly when order is meaningful, and closes with a **wrap-up sentence** tying it back into the argument. Test: if shuffling the list and re-reading makes no readable difference while the lead-in claims an order, that ordering relationship doesn't actually exist at that level.
- **One-line opener + one-paragraph closer**: open with a blockquote (one-sentence definition + a scope line + "Updated through YYYY-MM"); close with a one-paragraph summary (definition, strengths/weaknesses, and the decision rule, in three lines or fewer).
- **Diagram architecture and decision paths as Mermaid** (flowchart), with labels readable on their own; Markdown is the source of record. Learning-notes mode allows sparing emoji accents (✅❌⚠️); formal mode drops them.
- **Related-but-not-expanded neighboring topics** go in a closing "Further reading": positioning, a one-sentence comparison, and any currency note (license changes, project status).

**HTML edition:** Markdown is the default output and the source of record. Produce an HTML edition only when the user asks for a richly illustrated version; rules are in [references/html.md](references/html.md) — every diagram is inline SVG (no canvas, no raster images, no Mermaid runtime, no external images), a fixed template CSS applies, the four types stay separated in the HTML too, and any design tokens set via `frontend-design`/`infographic-design` are used only for figures, never for the page shell.

**Completion criterion:** the whole document reads plainly on one pass, with established terms kept in English; every list in every section has a lead-in and a wrap-up sentence, with meaningful ordering stated explicitly; there's a one-sentence blockquote opener and a one-paragraph closer; architecture and decisions are rendered in Mermaid and readable on their own; an HTML edition is produced only when the user asked for one, and when it is, the four types stay separated, diagrams are inline SVG, and the Markdown edition remains the source of record.

## S6. Final Check: Functional Quality Before Depth

Two quality gates, accumulated throughout writing and closed out before delivery. **Deep quality is conditional upon functional quality** — the order cannot be reversed.

### Functional Quality (Hard Constraints, Clear These First)

Accuracy / completeness / consistency / usefulness / precision. Item by item:

- **Every claim traces to a primary source.** Priority order: official docs/spec > original papers and design proposals (KEP/RFC) > project-maintainer writing > secondhand tutorials. Secondhand sources only add perspective — confirm key facts against a primary source.
- **Mark the as-of date and version range.** "Ingress has been replaced by Gateway API" is simply wrong without a version range; for anything whose behavior changed across versions, state the applicable version (`OpenShift 4.14+`, `Podman 5.x`).
- **Flag outdated claims.** A widely-repeated but now-outdated claim goes into explanation's common-misconceptions entry, noting which version it stopped being true from.
- **No fabricated URLs or sources**; when unsure, say so. **No unearned assertions**: every judgment sentence carries at least one of prior context, a stated reason, or a source.
- **Examples aren't exempt**: example sentences supplied by the user are held to the same standard as the body text — flag and fix broken phrasing in them too.

**De-AI pass:** **call `avoid-ai-writing-zh` first when it's available** — it's the authoritative source for the language judgment call, so run its detect/edit modes — sweep the whole document to zero and report what was found / fixed / remaining. It's optional, not a hard dependency: when it can't be loaded, fall back to the built-in condensed checklist below so the core deliverable is never blocked. Built-in checklist: fragmented short phrases, 頓號 (Chinese enumeration comma) stacking, dash overuse (connective「——」capped at once per thousand characters; the「concept — explanation」bullet separator doesn't count), unearned assertions, missing verbs, aphoristic commentary, templated headings (「深入探討」「全面解析」「揭秘」), second-person coaching voice (a violation in formal and hybrid modes, relaxed to allow first person and self-questioning in learning-notes mode).

### Cycle-of-Needs Coverage, and Complete ≠ Finished

- **Four-type coverage check**: a technical topic naturally generates four needs (wanting to get hands-on, wanting to complete a task, wanting to look up a parameter, wanting to understand why). Confirm every type is either "covered" or "explicitly listed as a gap" — no silent omissions, no empty-shell sections.
- **Complete ≠ finished**: a document is always evolving, but it can be complete at any point in time — useful to the user, matched to the current stage, structurally sound. Each type is independently publishable once it's currently useful; **grow it from the inside out, starting from whichever type the material best supports — don't scaffold all four shells first and fill them later.**

### Deep Quality (Assessed Only After Functional Quality Fully Passes)

Flow, beauty, anticipating the user. Beauty must never patch over a functional defect. Organize by mode to fit the need, and hold the section boundaries to preserve flow.

### Rewrite Notes (Mode D Only)

Deliver a rewrite note (format in [references/rewrite.md](references/rewrite.md)): structural changes, currency-fact corrections (old value → new value + source), and the trade-offs behind folding in / keeping / overwriting content. Declaring the rewrite done without this note counts as not having checked.

**Completion criterion:** every functional check passes *before* any deep-quality polish (sources traceable, as-of dates marked, version-sensitive claims scoped, no fabricated sources, no unearned assertions); the de-AI violation list has been produced, fixed to zero, and reported, with example sentences held to the same check; all four cycle-of-needs types are either covered or explicitly listed as gaps; no empty-shell sections; Mode D has delivered its rewrite note. Polishing flow before functional quality passes, or leaving a gap neither filled nor marked, is a failure.

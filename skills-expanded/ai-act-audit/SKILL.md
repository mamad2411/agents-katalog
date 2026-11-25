---
name: ai-act-audit
description: Audit an application, codebase, product, or AI system for compliance with the EU AI Act prohibited practices (Article 5, Regulation (EU) 2024/1689) and transparency obligations for AI-generated content (Article 50(2), (4) and (5)), based on the official European Commission Guidelines C(2025) 5052 and the Code of Practice on Transparency of AI-Generated Content. Use this skill whenever the user asks to check, audit, review, or verify AI Act compliance, EU AI regulation compliance, prohibited AI practices, Article 5 risks, AI transparency obligations, content marking/watermarking duties, deep fake labelling, or whether an app/feature/AI system "respects the AI Act" — even if they only mention "compliance" or "AI regulation" generically in an EU context. Also use it when reviewing AI-powered features (chatbots, recommenders, scoring, biometrics, emotion detection, scraping, profiling, generative AI outputs) for legal/regulatory risk in the EU.
---

# AI Act Audit — Prohibited Practices & AI-Content Transparency

Audit a target system (codebase, application, product spec, or described system) against two AI Act compliance layers:

1. **Prohibited practices — Article 5** Reg. (EU) 2024/1689, as interpreted by the **European Commission Guidelines C(2025) 5052 final (29.7.2025)** — converted in full as references `00`–`09`.
2. **Transparency of AI-generated content — Article 50(2), (4) and (5)**, using the **Code of Practice on Transparency of AI-Generated Content** ("CoP") as the operational benchmark — converted in full as references `10`–`11`.

**Output**: a structured Markdown audit report (see `assets/report-template.md`).

## Scope and limits — state these in every report

- This audit covers **Article 5 (prohibited practices)** and **Article 50(2)/(4)/(5) (transparency of AI-generated content)**. OUT of scope: high-risk classification and obligations (Art. 6 + Annexes I/III — postponed by the Digital Omnibus to 2 Dec 2027 for standalone Annex III systems and 2 Aug 2028 for product-embedded systems), Art. 50(1) (disclosure of AI interaction, e.g. chatbots) and Art. 50(3) (disclosure of emotion recognition / biometric categorisation systems), GPAI model obligations (Chapter V), and AI literacy (Art. 4). If the audit surfaces likely obligations under those layers, **flag them in "Out-of-scope observations"** — do not analyse them in depth.
- Timing (as amended by the **Digital Omnibus on AI, Reg. (EU) 2026/1744**, OJ 24.7.2026): the Art. 5 prohibitions apply since **2 February 2025**; the Art. 50 transparency obligations apply since **2 August 2026**. ONE transitional exception (Art. 111(4) AI Act as amended): providers of generative AI systems **already placed on the market before 2 August 2026** have until **2 December 2026** to comply with the Art. 50(2) machine-readable marking obligation only — all other Art. 50 duties (incl. deep fake and published-text labelling) apply from 2 August 2026 with no grace period. The CoP additionally sets **2 February 2027** as the deadline for watermark-detection interoperability solutions (CoP S1, Measure 3.4(c)). The Digital Omnibus also adds new prohibitions applicable from **December 2026** on AI generation of non-consensual sexual or intimate content depicting real persons, including "nudification" tools (creating nude imagery of real persons or digitally removing clothing) and strengthened prohibitions on AI-generated CSAM — see Step 3 note.
- Penalties: Art. 5 violations up to **EUR 35 million or 7% of worldwide annual turnover** (Guidelines ¶¶ 55–57); Art. 50 violations up to EUR 15 million or 3%.
- The Guidelines are **non-binding** and the CoP is a **voluntary compliance pathway**: adherence is not conclusive evidence of compliance, and providers/deployers may demonstrate Art. 50 compliance by other adequate means. In the CoP, only **"will"** measures are mandatory-under-the-Code; "encouraged"/"may" measures are voluntary — never report a missing optional measure as non-compliance, at most as a recommendation.
- The report is an engineering-level compliance screening, **not legal advice** — always recommend qualified legal review for any finding that is not clearly "No issue identified". Never give a definitive legal verdict; use the verdict scale below.

## Workflow

### Step 1 — Inventory the AI features

Identify every AI-relevant capability in the target. For a **codebase**, search for signals; for a **described system**, ask the user targeted questions about the same categories.

Signals to search for (grep/glob, adapt to stack):

- **Model/LLM integrations & generative outputs**: `openai`, `anthropic`, `claude`, `gpt`, `gemini`, `mistral`, `llama`, `huggingface`, `transformers`, `diffusion`, `stable`, `dall`, `tts`, `text-to-speech`, `image generation`, `inference`, `completion`, `embedding`
- **Recommenders / personalization / engagement**: `recommend`, `personaliz`, `ranking`, `feed`, `engagement`, `retention`, `nudge`, `ab_test`, `experiment`
- **Scoring / rating of people**: `score`, `scoring`, `trust`, `rating`, `creditworth`, `risk_score`, `churn`, `segment`, `profil`
- **Biometrics / face / voice**: `face`, `facial`, `biometric`, `recognition`, `fingerprint`, `voiceprint`, `opencv`, `mediapipe`, `rekognition`, `dlib`
- **Emotion / sentiment about persons**: `emotion`, `sentiment`, `mood`, `affect`, `stress`, `attention`
- **Scraping / data collection**: `scrape`, `crawler`, `selenium`, `playwright`, `beautifulsoup`, `cctv`, `rtsp`
- **Crime/fraud prediction about individuals**: `fraud`, `predict`, `criminal`, `offence`, `recidiv`, `watchlist`
- **Vulnerable-audience targeting**: age gates, `children`, `minor`, `elderly`, `disability` combined with targeting/ads logic, socio-economic segmentation
- **Transparency infrastructure (or its absence)**: `watermark`, `c2pa`, `content credentials`, `synthid`, `provenance`, `metadata` signing, `exif`/`xmp` writing, AI-label UI components, "AI generated" strings in templates

Also review: privacy policy, ToS, data flows, third-party AI SDKs, content pipelines (does AI output get published/exported?), upload/CMS workflows, admin/HR tooling.

Record each feature as: name, what it does, data it uses, who it affects, **whether it generates or manipulates audio/image/video/text**, and the provider-vs-deployer role of the audited organisation.

### Step 2 — Applicability screening

Read `references/00-overview-scope-exclusions.md` and check, per feature:

1. Is it an **AI system** (Art. 3(1))? Rule-based non-adaptive logic is generally out; ML/LLM-based inference is in.
2. Is there a **placing on the market / putting into service / use** in the EU (¶¶ 11–14)?
3. Which **role**: provider, deployer, or both (¶¶ 15–20)? Art. 5 binds both; Art. 50(2) binds **providers** of generative AI systems; Art. 50(4) binds **deployers**.
4. Do **exclusions** apply: national security/defence/military (¶¶ 22–28), R&D prior to market placement (¶¶ 30–33), personal non-professional use (¶¶ 34–35), open-source release conditions (¶ 36)?
5. Note: GPAI systems (e.g. an integrated LLM) can trigger prohibitions through their actual use even if the model provider's intended purpose is neutral (¶¶ 39–41); a downstream company that integrates a model and offers a generative system under its own name is typically the **provider** of that system for Art. 50(2).

If a feature is out of scope, record it with the reason and stop there for that feature.

### Step 3 — Triage against the eight prohibitions (Article 5)

For each in-scope feature, screen with this table. If ANY trigger question is plausibly "yes", the prohibition is **triggered for deep assessment** in Step 5.

| Prohibition | Typical feature signals | Trigger question |
|---|---|---|
| **(a) Harmful manipulation/deception** — `references/01-…` | Dark patterns driven by AI, engagement-maximising recommenders, persuasive chatbots, subliminal/covert techniques, deceptive AI content | Does the system use subliminal, purposefully manipulative or deceptive techniques that could materially distort behaviour and cause significant harm? |
| **(b) Exploitation of vulnerabilities** — `references/01-…` | Targeting children, elderly, disabled, or people in a specific socio-economic situation with AI-driven persuasion/ads/pricing | Does it exploit age, disability, or a specific social/economic situation to distort behaviour with (likely) significant harm? |
| **(c) Social scoring** — `references/02-…` | Trust/user scores, cross-context data aggregation, scoring that gates access to services | Does it evaluate/classify people over time on social behaviour or personal characteristics, leading to detrimental treatment in unrelated contexts or disproportionate treatment? |
| **(d) Criminal risk prediction** — `references/03-…` | Fraud/crime-risk models about individuals, predictive policing style features | Does it assess/predict a natural person's risk of committing a criminal offence based solely on profiling or personality traits? |
| **(e) Untargeted facial scraping** — `references/04-…` | Crawlers collecting face images, building/expanding face-recognition databases from the internet or CCTV | Does it create or expand a facial recognition database via untargeted scraping? |
| **(f) Emotion recognition (work/education)** — `references/05-…` | Emotion/stress/attention inference in HR tools, workplace monitoring, e-learning proctoring | Does it infer emotions of persons in a workplace or education institution (outside medical/safety exceptions)? |
| **(g) Biometric categorisation (sensitive traits)** — `references/06-…` | Classifying people from face/voice/gait into race, political opinion, union membership, religion, sex life, sexual orientation | Does it individually categorise persons from biometric data to deduce/infer those sensitive characteristics? |
| **(h) Real-time RBI for law enforcement** — `references/07-…` | Live face recognition on public-space cameras used for/by law enforcement | Is it real-time remote biometric identification in publicly accessible spaces for law-enforcement purposes? |

Sentiment analysis on **text alone** is generally not "emotion recognition" under (f) unless based on biometric data (see ¶¶ 244–252) — but check the reference before clearing it.

**Digital Omnibus additions (applicable from December 2026):** also screen any image/video generation or editing feature for the new prohibitions introduced by Reg. (EU) 2026/1744 — AI systems for creating non-consensual sexual or intimate content depicting real persons, including nudification/clothing-removal capabilities, and AI-generated child sexual abuse material. The full amended text is NOT included in this skill's references: for a triggered finding, cite Reg. (EU) 2026/1744, verdict at most 🟠 "Needs legal review" with a recommendation to verify against the official text (EUR-Lex, OJ L series 24.7.2026), and note the December 2026 applicability date.

### Step 4 — Transparency screening (Article 50(2)/(4)/(5))

Run BOTH checks for every in-scope feature that **generates or manipulates synthetic audio, image, video or text**:

**A. Provider marking & detection duties — Art. 50(2)+(5), CoP Section 1** (`references/10-…`). Triggered if the audited organisation places on the market or puts into service a generative AI system (including a product embedding a third-party model under its own responsibility). Check the mandatory ("will") measures:
1. **Marking (Commitment 1, Measure 1.1)**: outputs marked machine-readably; default is **multi-layered** marking — digitally signed metadata (Sub-m. 1.1.1) **plus** imperceptible watermarking (Sub-m. 1.1.2). Single layer suffices only for: closed-environment embedded products, and free-form text (which cannot carry metadata; watermark layer per 1.1.2, not required under 200 tokens — see Glossary "Very short text").
2. **Non-removal (Measure 1.2)**: preserve existing metadata markings on inputs; prohibit tampering in ToS/AUP; no circumvention tools.
3. **Detection (Commitment 2)**: a detection solution available (spec, software, or API), free of charge (limited fee exceptions <1M monthly users), accessible to the exposed audience, privacy-compliant with zero-retention (Sub-m. 2.1.3), results disclosed clearly and accessibly (Measure 2.3, EAA/WCAG).
4. **Quality (Commitment 3)**: effectiveness, reliability, robustness (typical processing + adversarial attacks), interoperability (staged; metadata standards now, watermark-detection interop by 2 Feb 2027).
5. **Compliance process, testing, training, MSA cooperation (Commitment 4)**.

**B. Deployer labelling duties — Art. 50(4)+(5), CoP Section 2** (`references/11-…`). Triggered if the audited organisation **deploys** AI to produce (i) **deep fakes** (Art. 3(60): AI image/audio/video resembling real persons/objects/places/events that would falsely appear authentic) or (ii) **text published to inform the public on matters of public interest** without human editorial control. Check:
1. **Disclosure (Commitment 1)**: EU icon (Annex 1: "AI GENERATED" / "AI MODIFIED") or equivalent label meeting design specs (Measure 1.1) and placement specs (Measure 1.2): perceivable without user action, at first exposure, embedded or equivalent overlay, repeated for video/live/audio, accessibility (EAA/WCAG).
2. **Internal processes (Commitment 2)**: compliance documentation, awareness/training, review + remediation of mislabelled content.
3. **Artistic/creative/satirical works (Commitment 3)**: lighter regime — disclosure that does not hamper enjoyment of the work.
4. **Editorial-control exception (Commitment 4)**: for published text, the Art. 50(4) subpara 2 exception applies where human review/editorial control exists and a person holds editorial responsibility — verify the policy elements (named responsible person, organisational measures, published contact).

If neither A nor B is triggered (no generative outputs, or outputs never leave a fully internal context), record "Not applicable" with the reason. Remember Art. 50(5): disclosure at the latest at first exposure, clear, distinguishable, accessible — this applies transversally.

### Step 5 — Deep assessment of triggered items

For each triggered prohibition or transparency duty, **read the full corresponding reference file** and check every condition/mandatory measure it lists. For each: met / not met / uncertain, with **evidence** (file paths and line references for code, quotes for docs/UX copy) and citations — Guidelines paragraphs as `(Guidelines ¶ N)`, Code of Practice as `(CoP S1, Measure 2.1)` / `(CoP S2, Sub-measure 1.2.2)`.

An Art. 5 practice is prohibited only if **all** cumulative conditions are fulfilled; uncertainty on any condition → "Needs legal review", never "Prohibited". For Art. 50, a gap in a **"will"** measure of the CoP indicates likely non-compliance with the underlying obligation (unless compensated by demonstrably equivalent alternative means, which the report should note); gaps in "encouraged"/"may" items are recommendations only.

### Step 6 — Write the report

Use `assets/report-template.md`. Verdict scale per finding:

- 🔴 **Likely violation** — Art. 5: all cumulative conditions plausibly met / Art. 50: mandatory obligation clearly unmet; urgent legal review + remediation required
- 🟠 **Needs legal review** — triggered, one or more conditions/obligations uncertain
- 🟡 **Attention** — currently compliant/out of the prohibition but close to the line (e.g. lawful persuasion, ¶¶ 127–133) or relying on an exception that needs documentation; document safeguards
- 🟢 **No issue identified** — obligations met or not triggered
- ⚪ **Not applicable** — no relevant feature

Every non-🟢/⚪ finding must include: evidence, the failed/uncertain conditions or measures, citations, and concrete remediation options. Write the report in English unless the user asks otherwise. Save it as a Markdown file and present it to the user.

## Reference navigation

References `00`–`09` are the full converted text of Guidelines C(2025) 5052; bold markers `**(N)**` are official paragraph numbers (1–433) — always cite them. Inline trailing digits (e.g. `harm.105`) are footnote references, resolved in `09-footnotes.md`. References `10`–`11` are the full converted Code of Practice on Transparency of AI-Generated Content; cite by Section/Commitment/Measure.

| File | Covers | Cite as |
|---|---|---|
| `00-overview-scope-exclusions.md` | AI Act risk approach, legal basis, scope, exclusions, interplay with high-risk & GPAI & other EU law, enforcement & penalties | ¶¶ 1–57 |
| `01-art5-1a-1b-manipulation-exploitation.md` | Art. 5(1)(a) manipulation/deception + 5(1)(b) exploitation of vulnerabilities, lawful persuasion boundary | ¶¶ 58–145 |
| `02-art5-1c-social-scoring.md` | Art. 5(1)(c) social scoring | ¶¶ 146–183 |
| `03-art5-1d-crime-risk-prediction.md` | Art. 5(1)(d) individual criminal risk assessment/prediction | ¶¶ 184–221 |
| `04-art5-1e-facial-image-scraping.md` | Art. 5(1)(e) untargeted scraping of facial images | ¶¶ 222–238 |
| `05-art5-1f-emotion-recognition.md` | Art. 5(1)(f) emotion recognition in workplace/education | ¶¶ 239–270 |
| `06-art5-1g-biometric-categorisation.md` | Art. 5(1)(g) biometric categorisation of sensitive traits | ¶¶ 271–288 |
| `07-art5-1h-rbi-law-enforcement.md` | Art. 5(1)(h) real-time RBI + Art. 5(2)–(7) safeguards, authorisations, reporting | ¶¶ 289–428 |
| `08-entry-into-application-review.md` | Entry into application, review of the guidelines | ¶¶ 429–433 |
| `09-footnotes.md` | All 244 footnotes (legal citations, case law) | fn. N |
| `10-cop-transparency-s1-provider-marking-detection.md` | CoP Section 1: provider duties under Art. 50(2)+(5) — marking (metadata + watermark), non-removal, detection solutions, quality requirements, testing; includes Glossary | CoP S1, Measure X.Y |
| `11-cop-transparency-s2-deployer-labelling.md` | CoP Section 2: deployer duties under Art. 50(4)+(5) — deep fake & published-text labelling, EU icon design/placement, artistic-works regime, editorial-control exception | CoP S2, Measure X.Y |

Read only the files relevant to the triggered items (plus `00-…`, always). Do not load everything by default.

## Rules

1. Always run Steps 1–2 even if the user asks about a single prohibition or only about transparency — context determines applicability.
2. Cite Guidelines paragraphs / CoP measures for every substantive claim in the report.
3. Be conservative: prefer "Needs legal review" over both false alarms and false clearances.
4. Distinguish CoP "will" (mandatory under the Code) from "encouraged"/"may" (voluntary): only "will" gaps count against compliance.
5. If the target has no AI features at all, still produce the report: inventory, "no AI system in scope" conclusion, and the standard scope/limits disclaimer.
6. If the user provides only a partial description, list the unanswered screening questions in the report under "Information gaps".

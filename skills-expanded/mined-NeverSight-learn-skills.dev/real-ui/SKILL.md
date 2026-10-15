---
name: real-ui
description: Real-world web and native-app UI/UX intelligence. Use when designing, redesigning, reviewing, or building sites, apps, pages, components, or design systems for any industry or region, including Arabic/MENA/RTL. Derives scope, information architecture, composition, responsive behavior, platform expression, and visual direction from product tasks and evidence—not genre templates or generic AI aesthetics. Covers web, iOS, Android, Flutter, React Native, accessibility, localization, performance, and implementation.
---

# real-ui — Real-World UI/UX Design Intelligence

You are operating as a designer who has studied how real, production
products across 24 industry modules, 8 platform guidance modules and 5 regions are
represented in fetched source — via code-first analysis of 156 real sites
(HTML/DOM/CSS/JS), distilled into a modular knowledge base. Source evidence
does not prove rendered or runtime behavior. Use it honestly. Do not
generate generic AI aesthetics.

## Purpose

Produce UI/UX design (and implementation when requested) that reads as
designed by an experienced human web designer for the specific industry,
audience, region, and language — verifiable against how real leaders in
that category actually behave.

## Core principles (non-negotiable)

1. **Context classifies first.** Every decision derives from INDUSTRY +
   AUDIENCE + USER INTENT + CONTENT + BUSINESS MODEL + BRAND + REGION +
   LANGUAGE. Never open with aesthetics.
2. **Evidence over invention.** Research claims use SOURCE-OBSERVED,
   RUNTIME-OBSERVED, RENDER-OBSERVED, INFERRED, RECOMMENDED, or UNCERTAIN.
   Never claim a site was analyzed if it wasn't. Never invent values
   (breakpoints, tokens, fonts).
3. **The real web is evidence, not a template.** Corpus values (for example,
   common breakpoint candidates and radius families) bound plausible choices;
   product content and constraints select the actual system.
4. **Systems not screens.** Tokens before pixels; scales before values.
5. **RTL/Arabic is first-class**, not a mirror (see knowledge/rtl/).
6. **Accessibility + performance are design materials**, not audits.
7. **No generic AI aesthetics** without written contextual justification
   (the banned list: knowledge/anti-patterns/ai-aesthetics.md).
8. **Original synthesis**: combine 2–4 reference patterns into something
   new. Never copy one site. REFERENCE → PRINCIPLE → ADAPTATION → ORIGINAL.
9. **Above the median**: the real web's median is mediocre (57% semantic
   main); match leader-class (gov.uk/GitHub/Stripe), not average.
10. **Code-first by default**: source can establish structure, tokens, and
    implementation signals. It cannot verify visual hierarchy, visibility,
    interaction success, or performance; those require named render/runtime
    evidence when available.
11. **Industry knowledge is not product scope.** Genre conventions
    suggest PRESENTATION possibilities; they never create features.
    Never invent functionality (ads, monetization, subscriptions,
    social, chat…) without: an existing feature, an explicit request,
    or supplied requirements (redesign/extraction.md scope gate).
12. **Page patterns are not templates.** Pages and industries supply
    candidate modules, terminology, risks, and expectations. Product
    entities, top tasks, content priority, and known capabilities decide
    page existence, order, navigation, and representation
    (pages/README.md; industries/README.md).

## Runtime workflow (always)

```
CLASSIFY → MODEL → RETRIEVE → CONSTRAIN → SYNTHESIZE → TOKENIZE → DESIGN → VALIDATE
```

1. **CLASSIFY** the request (taxonomy.md): industry (primary +
   secondaries), product type, audience, business model, platform
   (web/iOS/Android/Flutter/RN/SwiftUI/UIKit/Compose), device class,
   input model (touch/pointer/keyboard/stylus/voice), language(s) +
   direction, region, brand inputs. If ambiguous, ask ONE clarifying
   question only if the answer changes the direction; else state
   assumptions and proceed. Redesign requests branch to the redesign
   pipeline first (redesign/workflow.md).
2. **MODEL** the product FIRST
   (foundations/product-modeling.md): entities, top tasks (frequency ×
   criticality), relationships, volume, scope ledger, content inventory,
   information priority, and screen contracts. Derive IA and
   representations from the model—not the industry or page type.
3. **RETRIEVE** knowledge (map below). Load authority contracts before
   their catalogs: industries/README.md before industries/* and
   pages/README.md before pages/*. Normal mode limits optional domain files;
   it never skips the model or applicable authority contract. Deep/Audit
   mode changes investigation depth, not design quality.
4. **CONSTRAIN**: reconcile modeled needs with industry expectations
   (record reasons for adopted structural conventions), then apply brand
   assets, a11y floor, performance budget, platform, locale, RTL, and real
   content constraints. Hypotheses stay labeled and outside committed scope.
5. **SYNTHESIZE** direction: run the DNA selector
   (visual-dna/dna-selector.md) → primary (+optional secondary) DNA →
   write a 3–5 line design direction statement BEFORE any pixel
   decisions.
6. **TOKENIZE**: define the scale system (tokens.md minimal set):
   type scale, colors (4-role palette), spacing, radius, shadow, motion,
   breakpoints. One screen of tokens.
7. **DESIGN/IMPLEMENT**: choose representations per the screen contracts;
   use patterns/, ui/, pages/, and industries/ as candidate/evidence
   catalogs within their authority boundaries—not as complete templates.
   Implementation stack: semantic HTML + utility CSS (Tailwind grammar
   acceptable when it fits the project) + vanilla JS unless the project
   specifies otherwise. In redesign
   implementations: preserve
   business logic, routes, data — NOT the component tree (business
   logic ≠ components; routes ≠ layout; data ≠ representation —
   redesign/extraction.md).
8. **VALIDATE** (finish gate, run every time):
   - Anti-AI check: any banned pattern without justification? Kill it.
   - Industry check: "Does this feel like {industry}?" Cite 2–3 real
     references whose patterns inform the result.
   - Product-fit check: IA traceable to the product model (task #1
     reachable in one step; entity lifecycles closable)? Copy check:
     labels/CTAs/error copy per ux/content-design.md.
   - Scope check: every capability = KNOWN, REQUESTED, or NECESSARY
     SUPPORT UX; no industry/page catalog invented a feature.
   - Structure check: every major region cites required content/action,
     user task/decision, and representation rationale. Style-blind layout
     must not collapse to a genre template.
   - State/adaptation check: empty/loading/error/partial/permission and
     extreme-content states exist; each relevant window/input class states
     what remains, moves, condenses, changes representation, or is removed.
   - A11y check: semantics, focus-visible, contrast, reduced-motion,
     keyboard, zoom. Mobile: VoiceOver/TalkBack + text scaling
     (accessibility/mobile.md).
   - RTL check (when Arabic): full gate in rtl/implementation.md;
     non-web also rtl/cross-platform.md.
   - Perf check: LCP/CLS/INP budgets; effects vs cost ledger.
   - Originality check: could this be any competitor? Push one
     differentiated dimension.
   - Platform QA: native conventions respected (platforms/README.md
     QA blocks); mobile ≠ squeezed web (devices/mobile.md).
   - Cross-platform realism when multi-platform
     (platforms/cross-platform.md failure modes).
   - Redesign QA when redesigning (redesign/workflow.md stage 8):
     depth check (redesign/depth.md: style-blind structural diff
     matches the classified depth; reclothe test for FULL) +
     capability ledger closed + scope fidelity (no invented
     features — redesign/extraction.md). For FULL, run the pre-code
     PLAN checkpoint and post-render RENDER checkpoint in
     redesign/full-redesign-execution.md when tooling permits. FAIL =
     return to re-derivation and change the output.

## Redesign tasks (major capability)

Redesign ≠ "make it modern." Classify depth FIRST — POLISH · REFRESH ·
REDESIGN · FULL (redesign/depth.md); FULL treats the old UI as evidence
of requirements, not as the architecture. For REDESIGN/FULL, EXTRACT first
(redesign/extraction.md): requirements · capabilities · workflows ·
presentation — preserve the first three, re-derive the last; no
capability may silently disappear. Then run
knowledge/redesign/workflow.md:
understand → diagnose → preserve → decide (keep/change/remove/merge/
add with reasons) → new UX → new UI → system → platform adaptation →
realism QA. Diagnosis feeds from diagnosis.md; identity preservation
from redesign/preservation.md ("same product evolved"); direction from
originality.md. Screenshots = evidence only (screenshot-analysis.md;
host vision tools optional, provider-agnostic — vision observes,
this skill reasons).

## Knowledge retrieval map (load only what the task needs)

| Need | File(s) |
|---|---|
| Any design work | foundations/principles.md, foundations/visual-hierarchy.md, foundations/layout.md, foundations/color.md |
| Classification | taxonomy.md |
| Product model (before any IA decision) | foundations/product-modeling.md |
| Redesign | redesign/{depth,extraction,workflow,diagnosis,preservation,originality,screenshot-analysis,prioritization,evolution-cases,full-redesign-execution}.md |
| Platform | platforms/{README,web,flutter,react-native,swiftui,uikit,jetpack-compose,android,cross-platform}.md |
| Device class | devices/{mobile,tablet,foldable,desktop,large-screen}.md |
| Input model | input/{touch,mouse-keyboard,stylus-voice}.md |
| Adaptive strategy | responsive/{breakpoints-adaptation,mobile-patterns,adaptive-models}.md |
| Mobile app UX | ux/mobile-states.md |
| Industry context (load authority first) | industries/README.md + industries/{gaming,saas-dev,ecommerce-marketplace,fashion-luxury-beauty,finance-banking,news-media,entertainment-streaming,sports-fitness,travel-tourism,restaurants-food,real-estate,healthcare,education,government-public,b2b-enterprise,creative-culture,social-community,automotive,immersive-experimental,science-utility,crypto-web3,islamic-apps,jobs-recruitment,logistics-delivery}.md |
| Page composition candidates (load authority first) | pages/README.md + pages/{homepage,landing,category-search,product-detail,article,dashboard,pricing-checkout,account-settings-forms}.md |
| Style direction | visual-dna/{dna-catalog,dna-selector}.md |
| Components | ui/{components,cards,data-display,data-viz,media}.md |
| Section patterns | patterns/{header-navigation,heroes,content-sections,recommendations-sticky,footer}.md |
| UX flows | ux/{navigation,search-discovery,states,trust-conversion,onboarding,mobile-states}.md |
| Forms & validation | ux/forms-validation.md |
| Copy, labels & CTAs | ux/content-design.md |
| i18n beyond RTL (multilingual LTR, locale formats) | localization/i18n.md |
| Notifications | ux/notifications.md |
| Systems | design-systems/{tokens,color-type-systems,components-states,cross-platform,dark-mode-theming}.md |
| Implementation realism | implementation/realism.md |
| Typography | typography/{latin-systems,arabic-typography,responsive-pairing}.md |
| Icons | iconography/systems.md |
| Responsive | responsive/{breakpoints-adaptation,mobile-patterns,adaptive-models}.md |
| Arabic/RTL (web) | rtl/{implementation,arabic-ux,global-vs-arabic}.md |
| Arabic/RTL (non-web) | rtl/cross-platform.md |
| Motion | motion/principles.md |
| A11y (web floor) | accessibility/floor.md |
| A11y (mobile/screen readers) | accessibility/mobile.md |
| A11y (motion/contrast/color) | accessibility/contrast-motion.md |
| Cross-platform systems | design-systems/cross-platform.md |
| A11y / Perf / SEO | accessibility/floor.md, performance/performance-aware-design.md, seo/seo-aware-design.md |
| What NOT to do | anti-patterns/{ai-aesthetics,general,rtl-arabic}.md |
| Evidence | research/{observed-findings,saturation-and-confidence,method}.md |
| References | references/{global,mena}-references.md |

Typical optional domain load: "Arabic news site" → industries/README +
news-media + pages/README + homepage + arabic-typography + rtl/* +
visual-dna. The product model and authority contracts are control files, not
optional context to trade away.

## Retrieval intelligence (dimension activation)

Dimensions AUTO-ACTIVATE each other — users never enumerate categories:

| Detected | Also load |
|---|---|
| iOS / iPadOS / SwiftUI / UIKit / Apple | platforms/{swiftui,uikit}.md (+ devices/mobile.md; iPad adds devices/tablet.md; Apple evidence labels recovered — see v2.1 research log) |
| platform≠web (flutter/RN/swiftui/uikit/compose/android) | platforms/README.md + its file + accessibility/mobile.md + devices/mobile.md (if app) |
| redesign intent | redesign/depth.md (classify depth FIRST) + redesign/workflow.md (+ diagnosis, preservation; add prioritization for scoping; FULL also loads redesign/full-redesign-execution.md) |
| Arabic/RTL + platform≠web | rtl/cross-platform.md (in addition to rtl/implementation.md on web) |
| mobile/tablet/foldable/desktop/TV target | matching devices/* + matching input/* |
| forms/checkout/onboarding flows | ux/forms-validation.md + ux/states.md |
| notification feature | ux/notifications.md |
| multi-platform product | platforms/cross-platform.md + design-systems/cross-platform.md |
| a11y-heavy or compliance mention | accessibility/{floor,mobile,contrast-motion}.md |
| any industry module | industries/README.md first |
| any page module | pages/README.md first |
| multi-industry product | taxonomy.md combos (e.g., food+logistics+maps) + foundations/product-modeling.md (model before merging genre knowledge) |
| CTAs, labels, error/empty copy, tone | ux/content-design.md |
| multilingual LTR product or locale formats (dates/currency/plurals) | localization/i18n.md |

Example: "Arabic Flutter banking app for phones and tablets" →
finance-banking + platforms/flutter + devices/{mobile,tablet} +
responsive/adaptive-models + rtl/cross-platform + typography/arabic-
typography + accessibility/{mobile,contrast-motion} + ux/mobile-states.

## Normal mode (default)

Use the prebuilt knowledge base. Do NOT re-research known industries and do
not re-derive stable primitives without a reason. Keep optional domain
retrieval focused (normally no more than five modules), but always retain the
product model and applicable page/industry authority contracts. Deliver:
model/scope assumptions → direction statement → token sheet → design or
implementation → finish gate.

Normal mode includes the complete relevant design intelligence and finish
gate: product modeling, domain and platform knowledge, design diversity,
redesign depth, capability preservation, scope fidelity, IA, components,
responsive/adaptive behavior, accessibility, localization, content design,
realism, and targeted validation. It covers ordinary product work at every
depth—including **FULL REDESIGN**. A redesign never becomes Deep/Audit merely
because it is large or structurally ambitious.

Normal product work must not trigger an entire-repository inspection, audit
manifest, full evidence refresh, knowledge-base rewrite, integrity scan, or
system-wide regression. If a user names a current competitor or an uncovered
market and fresh facts materially affect the deliverable, do only the bounded
project research needed (with the evidence labels below); do not silently turn
the task into a REAL-UI maintenance audit.

## Deep / Audit mode (investigation only)

Trigger only when the task is to audit, upgrade, debug, or comprehensively
validate REAL-UI itself; validate the whole knowledge base/repository or its
research claims; or when the user explicitly requests deep/exhaustive
research. Deep/Audit is for broader investigation, not for unlocking normal
design quality. A named competitor or current framework fact may require a
bounded research step in Normal mode; breadth and repository-wide checks still
require the triggers above.

Procedure for a research-bearing Deep/Audit task (research/method.md):
1. Start from existing KB (baseline + gaps).
2. Fetch competitor/leader HTML+CSS (code-first extraction: tokens,
   breakpoints, type stacks, structure, RTL techniques, schema).
3. Label everything SOURCE-OBSERVED / RUNTIME-OBSERVED /
   RENDER-OBSERVED / INFERRED; record inaccessibility honestly.
4. Distill to patterns → update the working notes for this project
   (KB files stay stable; per-project findings live in the project).
5. Then run the normal workflow.

### Mode routing checks

| Request | Route |
|---|---|
| `Design a new ecommerce website` | NORMAL |
| `Full redesign this existing gaming website` | NORMAL |
| `Design a Flutter finance app` | NORMAL |
| `Audit the entire REAL-UI knowledge base` | DEEP / AUDIT |
| `Validate all REAL-UI research and repair unsupported claims` | DEEP / AUDIT |

## Originality rules

- Minimum 2 reference classes per synthesis (e.g., "streaming-scrim
  class + Arabic portal density"), stated in the direction.
- Borrow principles, never layouts. If a section is recognizably one
  site's, redesign it.
- One deliberate differentiation per project (typography, density,
  motion moment, or register) — written down.
- Same industry ≠ same structure: set the five dials (density, nav
  model, silhouette, rhythm, register) from the product model —
  originality.md "Variation within an industry" (fresh designs too).

## Anti-AI rules (summary — full list in anti-patterns/ai-aesthetics.md)

Banned by default: purple→blue gradient heroes, glassmorphism everywhere,
bento-everything, glow borders, floating blobs/3D, radius inflation,
gradient text, sparkle iconography, "Trusted by" formula pages,
centered-everything. Usage requires a written justification naming the
real-world reference class that legitimizes it.

## Evidence honesty (always)

- Distinguish SOURCE-OBSERVED (fetched implementation presence),
  RUNTIME-OBSERVED, RENDER-OBSERVED, INFERRED, RECOMMENDED, and UNCERTAIN.
  Legacy OBSERVED means SOURCE-OBSERVED unless runtime/render evidence is
  explicitly named.
- Source classes (label knowledge claims, esp. platform files):
  REAL-WORLD OBSERVATION (corpus/product evidence) · PLATFORM RULE
  (official platform requirement) · DESIGN PRINCIPLE (stable,
  cross-source convention) · IMPLEMENTATION GUIDANCE · RECOMMENDED ·
  EXPERIMENTAL. Never let principles masquerade as platform rules.
- Cite references as classes, not clones. Never say "analyzed X" unless
  this session actually inspected X. Blocked sources logged in
  research/reports/v2-research-log.md.

## Output conventions

- Design deliverables: direction statement → token sheet → structure
  (IA/wireframe-level description) → visual specs → (if asked) code.
- Reviews/audits: findings with severity + evidence + fix.
- Always end with the finish-gate checklist results (pass/fail per item).

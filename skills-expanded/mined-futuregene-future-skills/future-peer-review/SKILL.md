---
name: future-peer-review
version: 0.1.1
description: >
  Review scientific manuscripts, grant proposals and research presentations with
  evidence-linked, constructive assessment of methods, statistics, reproducibility,
  ethics and reporting standards. Use for formal peer review, manuscript critique
  and revision feedback. Distinguish major validity issues from minor presentation issues.
allowed-tools: Read Write Edit Bash(future:*)
category: methodology
license: MIT license
metadata: {"skill-author": "K-Dense Inc."}
---

# Scientific Peer Review

Evaluate the claims actually made and the evidence actually supplied. A checklist
is an aid to judgment, not proof that a study is valid or invalid.

## Scope and confidentiality

Identify the document/version, requested review type, venue criteria, available
supplements and permitted tools. Reuse specified scope, language and deadlines.
Do not upload confidential manuscripts, expose private text in web queries or
contact authors/editors without authorization. If external processing is forbidden,
use authorized local parsing and report any resulting visibility limits.

The workflow below is self-contained. Third-party `scientific-critical-thinking`
and `scholar-evaluation` are optional only when installed and explicitly useful;
never assume a builtin-only installation has them. Do not invent tool names or
paths to unavailable skills. For authorized citation checks use `future-paper`
and `future-web`, reading those skills before calling their tools.

## Review workflow

1. **Read the actual material.** Summarize the research question, design, key findings
   and contribution in a few sentences. Distinguish missing material from a demonstrated
   defect. Ask for critical missing supplements or bound the review accordingly.
2. **Map claims to evidence.** Identify the claims decisive for the conclusion and
   locate their data, methods, figures or citations. Check counterevidence and alternative
   explanations. Quote brief passages with page/section/figure references.
3. **Assess design and methods.** Check experimental unit, controls, randomization,
   blinding, inclusion/exclusion, biological versus technical replication, confounders,
   batch effects, measurement validity and reproducibility of the described protocol.
4. **Assess statistics.** Read `references/common_issues.md` when reviewing analyses.
   Check dependence/paired observations, model assumptions, missing data, multiplicity,
   effect sizes and confidence intervals, sample-size justification, stopping rules,
   leakage/overfitting, validation data separation and exploratory versus confirmatory
   claims. Do not infer invalidity merely from a small n, one p-value or a checklist flag.
5. **Assess results and interpretation.** Reconcile denominators, units and sample counts
   across text/figures/tables. Check negative results and selective reporting. Non-significance
   is not equivalence; correlation is not causation; a biological mechanism requires relevant
   evidence. Evaluate precision and applicability, not only statistical significance.
6. **Assess reporting and ethics.** Read `references/reporting_standards.md` for the
   relevant study type, then verify current venue/guideline requirements when necessary.
   Check consent/approval claims, conflicts, funding, preregistration and data/code availability.
   Reporting completeness does not substitute for methodological quality.
7. **Assess figures and citations.** Check captions, axes, units, scale bars, error-bar
   definitions, legibility and whether citations support the actual statements. Treat possible
   image duplication/manipulation as a concern requiring original data, not a misconduct verdict.
8. **Prioritize and write.** Separate major validity/reproducibility issues from minor clarity
   or formatting issues. For every important concern explain the location, evidence, consequence,
   and a specific feasible remedy. Distinguish essential corrections from optional new studies.

## Adapt to the document

- **Grant:** assess hypothesis, feasibility, team/resources, risks, milestones and alternative
  approaches. A proposal is not expected to contain completed results.
- **Review/meta-analysis:** assess the search and selection contract, exclusions, risk of bias,
  heterogeneity, synthesis method and applicability. Read reporting standards for PRISMA when relevant.
- **Methods/computational paper:** examine baselines, fair comparisons, held-out validation,
  software/data versions, code availability and reproducibility of performance claims.
- **Preprint/short report:** retain scientific rigor while adjusting expectations for format,
  completeness and stage of review. Do not penalize a preprint simply for being a preprint.

## Presentations and visual review

Peer review does not require generating replacement figures. The legacy
`scripts/generate_schematic.py` and `scripts/generate_schematic_ai.py` entries are
retired and exit without remote calls. For a separately authorized illustration,
use `future-image`; review failure must remain unverified, not become a passing
score or trigger automatic paid regeneration.

Read accessible text for scientific content and render pages when evaluating layout.
There is no universal rule that directly parsing a presentation PDF causes an overflow.
Never invoke a guessed `skills/.../scripts/...` path.

1. Inspect available local PDF/Office renderers. For authorized PDF rendering, an installed
   PyMuPDF library can render pages; use `future-software-install` only if installation is needed
   and permitted. For PPTX, use an available authorized renderer/exporter, or request a PDF export.
2. Write any necessary rendering script using the file tool. Resolve input/output paths explicitly
   and preserve originals. Do not dump all pages into the model context at once.
3. Use `future-image` for authorized image inspection. Read one page at a time; check text overflow,
   overlaps, contrast, labels, figure readability and factual consistency with source data.
4. Inspect all pages when required for a complete visual review; if sampling is agreed, name the
   reviewed pages and limits. Do not claim uninspected slides passed.
5. Report issues by slide number. Adapt text-size and slide-count guidance to the actual venue,
   display and talk duration rather than imposing universal minimums.

## Deliverable

Return the requested format, normally:

- Brief summary and important strengths.
- Numbered major concerns, each with evidence/location, scientific impact and remedy.
- Numbered minor concerns and presentation corrections.
- Recommendation only if requested, justified against the venue's criteria.
- Materials/tools checked, unavailable material, remaining uncertainty and reviewer limitations.

Keep editor-only confidential comments distinct from comments intended for authors.
Do not fabricate literature searches, reproduce experiments you did not run, claim independent
review of your own implementation, or equate agreement among related models with independent evidence.
Before delivery, verify every location/quotation and remove unsupported accusations or invented facts.

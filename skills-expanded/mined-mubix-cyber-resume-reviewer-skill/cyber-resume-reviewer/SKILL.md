---
name: cyber-resume-reviewer
description: Review, tailor, score, or rewrite IT and cybersecurity resumes. Use for candid critique, job-description fit, exact edits, or complete rewrites; never rank candidates.
metadata:
  version: "4.1.0"
---

# IT and Cybersecurity Resume Reviewer

Improve how the candidate communicates relevant work. Preserve the useful four-lens model: **Machine-read** (document extraction), **Human-skim** (first impression), **Human-believe** (evidence), and **Human-act** (target alignment). These are review lenses, not a universal hiring sequence or a prediction of recruiter behavior.

## Start with the requested deliverable

| Request | Deliver | Default artifact |
|---|---|---|
| Review or improve | Candid verdict, strongest evidence to preserve, prioritized findings, exact edits, and important open questions. Use the standard report template selectively. | Markdown and a PDF rendered from that Markdown |
| Quick review | Up to five material findings and useful exact edits. Omit scoring unless requested. | In conversation, or Markdown when asked |
| Tailor to a JD | Map requirements to evidence, then make truthful changes. Separate employer requirements from assumed role expectations. | Markdown and PDF for a fit report; requested format for a resume rewrite |
| Rewrite / give me an updated resume | Produce the complete rewrite now using established facts. Do not require a full report or another opt-in. Explain material changes briefly. | Rewritten resume in the requested format |
| Score | Use the anchored rubric and show assessed coverage. Score the document, not the person's worth or hiring probability. | Part of the accompanying report |
| JSON | Use the report schema and validator. The analyzer's JSON is a different artifact. | JSON only |
| Interview stories / compare versions | Use the corresponding template only when requested or useful to the stated task. | Markdown unless another format is requested |

## Working sequence

1. **Read the supplied resume and target.** For PDF/DOCX, use available document extraction and rendering capabilities; do not assume specific skill names or tools exist. Read images visually or with OCR, checking uncertain text. Preserve role boundaries, dates, and source locations. If only pasted text is available, assess content and mark visual layout and original-file parsing **Not assessed**.
2. **Resolve only essential uncertainty.** No resume: ask for it. No JD: use a supplied title and label the role profile inferred. A company or industry alone does not define a job. No target: perform a useful general IT/cyber review now; suggest one or two plausible directions and ask which to target before making role-specific claims. Do not withhold all edits.
3. **Triage blockers, risks, and unknowns.** Read [submission triage](references/fatal-flaws-and-kill-checks.md). An observed defect, an explicit unmet requirement, and an unverified fact are different findings. Missing content on a redacted review copy is not a candidate failure.
4. **Build a small evidence map.** Read [review framework](references/review-framework.md). Distinguish candidate-stated facts, job requirements, reviewer inferences, and unknowns. Link every new substantive claim to a resume location or user statement. Do not import facts from another candidate, a sample, the JD, or prior personal context about the reviewer.
5. **Review the relevant role and evidence.** Use the references below selectively. Check scope, ownership, technical meaning, and results. A skill listed without an example is uncorroborated in this document, not automatically false. Specific qualitative outcomes and well-described operational work count; numbers are optional.
6. **Use the text helper when useful.** For a full text review or repeated checks, run `python3 scripts/analyze_resume_text.py --resume resume.txt --jd jd.txt` (omit `--jd` when absent). It finds candidate signals, never ATS acceptance, skill mastery, or hiring odds. Small edits do not need a mandatory script run. Read [helper interpretation](references/analyzer-interpretation.md) before using its output.
7. **Make the changes the user asked for.** Prefer exact source quotes and replacements supported entirely by known facts. Move or merge text without changing its employer, dates, participation level, or context. Place questions for stronger future claims outside the clean rewrite. If essential facts are missing, provide the useful supported portion and identify the limitation.
8. **Produce the artifacts.** Write a full review or JD fit report as Markdown first. Treat it as the only content source, then render the PDF from it. Read [report rendering](references/report-rendering.md) before rendering in a session. Prefer `python3 scripts/render_report.py /path/to/review.md /path/to/resume-review.pdf`; if its dependencies are unavailable, use the host's PDF capability while preserving the same content and visual evidence rules. Save candidate artifacts outside the skill directory. Present both files. If the host cannot create files, provide the complete Markdown in conversation and state that the PDF could not be generated there.
9. **Verify the result.** Check factual traceability, dates, titles, credential status wording, technical meaning, and unresolved placeholders. For a PDF, inspect every rendered page, confirm the page count from the file, and compare extracted reading order with the visual document. Confirm that no `[VERIFY]` token appears in a supported-replacement block. Report only checks actually performed.

## Truth and scope invariants

- Do not invent or upgrade employers, titles, duties, tools, metrics, education, certifications, clearances, authorization, team size, budget authority, board access, or project outcomes.
- Keep **operated / built / supported / led / advised / approved** distinct. Lab, course, volunteer, personal, client, and production work must retain their context. Preserve team attribution.
- Put assumptions in analysis, never as facts inside the resume. No `[Assumed: ...]` claims. For a requested fill-in draft use `[VERIFY: specific fact]`, list every occurrence in a verification table, and label that draft incomplete. Prefer a clean supported version plus optional questions over a resume full of blanks.
- An example is illustrative, never candidate evidence. Read [truth, bias, and privacy](references/bias-and-ethics-guardrails.md) for redaction, career gaps, and sensitive operational information.
- Keep live candidate data out of reusable skill files, templates, examples, test fixtures, logs, and source-control history. Never turn a live review into a reusable example. Generated review files belong outside the skill directory.
- Never equate keyword overlap with qualifications, fit percentage, ATS score, or interview probability. Do not diagnose deception, personality, motivation, or retention risk from prose style or career history.
- The visual layer may not assert what the prose may not assert. Do not use score gauges, progress bars, percentage rings, letter grades, match percentages, radar charts, or proficiency bars. Colour may distinguish finding priority and evidence provenance; it may not rate the person. See [report rendering](references/report-rendering.md).
- Verify time-sensitive external claims when they matter: employer requirements, certification availability/prerequisites, federal instructions, vendor parser behavior, and framework naming. Use [source policy](references/source-policy.md). If browsing is unavailable, state what remains unverified and continue the content work.

## Reference routing

| Situation | Read |
|---|---|
| All substantial reviews | [Review framework](references/review-framework.md), [submission triage](references/fatal-flaws-and-kill-checks.md) |
| Scores requested or a comprehensive scored review | [Scoring rubric](references/scoring-rubric.md) |
| Role family, level, industry, IT/cyber pivots | [Role taxonomy](references/cybersecurity-role-taxonomy.md) |
| File formatting, reading order, ATS question | [Parser risk](references/ats-formatting-and-parser-risk.md) |
| JD requirements / keyword alignment | [Requirement triage](references/job-requirement-triage.md), [fit mapping](references/keyword-and-fit-mapping.md) |
| Bullet or summary changes | [Rewrite guide](references/outcome-bullet-rewrite-guide.md), [anti-pattern examples](references/anti-pattern-gallery.md) |
| First impression or visible layout | [Reader review](references/recruiter-reader-psychology.md) |
| Technical claims, cyber metrics, framework wording | [Technical claim checks](references/technical-claim-checks.md) |
| Managers, executives, BISO, Field CISO, fractional leaders | [Leadership](references/executive-and-leadership-resumes.md) |
| Career transition, military translation, return to work | [Transitions](references/career-transition-translation.md) |
| Actual learning or credential gaps | [Learning](references/certifications-and-learning.md) |
| Federal, contractor, clearance, DCWF | [Federal and cleared roles](references/federal-and-cleared-roles.md) |
| Sensitive details, redacted source, bias concerns | [Truth, bias, and privacy](references/bias-and-ethics-guardrails.md) |
| External factual claims | [Sources and refresh rules](references/source-policy.md) |
| Analyzer output | [Helper interpretation](references/analyzer-interpretation.md) |
| Markdown/PDF deliverables, formatting conventions, renderer setup, or PDF checks | [Report rendering](references/report-rendering.md) |

## Output resources

Choose, trim, and reorder these to match the request; do not fill every section by default:

- [Standard report](templates/report-template.md)
- [Quick review](templates/quick-review-template.md)
- [Exact edits](templates/rewrite-table-template.md)
- [Complete rewrite](templates/rewritten-resume-template.md)
- [Optional intake](templates/prompt-intake-template.md)
- [Interview stories](templates/interview-story-bank-template.md)
- [Change tracking](templates/resume-change-log-template.md)
- [Structured report schema](schemas/resume-review-report.schema.json): validate with `python3 scripts/validate_report.py report.json`; requires `jsonschema` for this optional mode.
- [Worked example](examples/example-output-summary.md): illustrative, not a required report length.
- [Report rendering](references/report-rendering.md): two-artifact contract, visual evidence rules, metadata, setup, and verification.
- [House stylesheet](assets/report.css): print design used by the renderer.
- [PDF renderer](scripts/render_report.py): render with `python3 scripts/render_report.py /path/to/review.md /path/to/resume-review.pdf`.

## Quality bar

Lead with the main assessment. Explain what the resume demonstrates, what is unclear, and the highest-value repair. Preserve strengths as deliberately as you fix weaknesses. Be candid without ridicule, canned praise, or invented urgency. Use plain language and the candidate's voice. Do not manufacture five problems, ten edits, a certification plan, or a warning banner when the evidence does not warrant them.

Before delivery, ask: Does each replacement say only what the candidate established? Did missing evidence become an accusation? Did a formatting heuristic become a guarantee? Did the design imply a claim the prose cannot support? Does the output fulfill the requested review, tailoring, or rewrite?

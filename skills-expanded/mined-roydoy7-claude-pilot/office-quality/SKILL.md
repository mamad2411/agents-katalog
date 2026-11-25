---
name: office-quality
description: Plan and validate professional cross-format office deliverables involving Word, Excel, PowerPoint, PDF, images, templates, and desktop Office workflows. Use when a task spans formats, requires fidelity to an existing template, targets Japanese office use, needs visual or print quality assurance, or produces a final file for other people to use.
---

# Office Quality

## Define the artifact contract

Before producing files, infer or establish:

- the audience and the decision, task, or record the artifact must support;
- whether it is read, presented, edited, entered into, printed, archived, or imported;
- the source of truth and which values or layouts must be preserved;
- language, locale, brand, accessibility, privacy, and compatibility constraints;
- the requested deliverables, filenames, and whether originals may be overwritten.

Use the format-specific Skill for detailed construction. Use this Skill to coordinate fidelity and validation across formats.

## Select the source format deliberately

- Author narrative documents in DOCX, operational/tabular systems in XLSX, presentations in PPTX, and fixed final distributions in PDF.
- Keep editable source files when the user will revise the artifact.
- Do not use PDF as the only source when repeated editing is expected.
- Do not use Excel merely to imitate a Word document unless an existing business process requires it.
- Respect Japanese office workflows where Excel legitimately serves as a form, ledger, schedule, calculation surface, and printed document.

Read [cross-format-workflows.md](references/cross-format-workflows.md) when data or content moves between formats.

## Preserve sources and templates

- Inspect before editing and copy the source to a new output path.
- Preserve structure and style that carry business meaning, even when they are not aesthetically modern.
- Change only the intended layer: content, formatting, calculation, layout, or file format.
- Record conversions and intermediate files so values can be traced.
- Avoid lossy round trips such as PDF → DOCX → PDF unless necessary and reviewed.

## Validate in layers

1. Validate data and text against the source.
2. Validate structure with the native file inspector or library.
3. Reopen with the target Office application or LibreOffice when rendering or recalculation matters.
4. Convert to a stable preview format and visually inspect the output.
5. Validate the sequence and usability from the recipient's perspective.

For a significant final deliverable, delegate a second-pass review to `office-quality-reviewer` when the Agent tool is available. Provide the exact output and preview paths, task intent, audience, and known constraints. Treat its findings as review evidence: resolve material issues, then repeat the affected validation checks.

Read [delivery-checklist.md](references/delivery-checklist.md) before final delivery. Read [accessibility-and-localization.md](references/accessibility-and-localization.md) for public, multilingual, Japanese, or accessibility-sensitive work.

## Communicate limitations honestly

- State when formulas were not recalculated, macros were not executed, links were not refreshed, or native Office rendering was not verified.
- State when conversion may have changed pagination, charts, fonts, animations, comments, tracked changes, or accessibility tags.
- Never describe a file as validated solely because it was written without an exception.
- Deliver only intended outputs; keep temporary XML, images, renders, and unpacked folders out of the final set.

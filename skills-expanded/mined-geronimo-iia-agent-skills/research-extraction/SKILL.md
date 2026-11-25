---
name: research-extraction
description: >-
  Deep extraction of research corpora into structured knowledge documents using
  a Workflow-driven subagent/reviewer pattern. Use when you have raw source
  documents (theses, papers, reports) and need structured extraction across
  multiple axes (architecture, messages, algorithms, forms, etc.) with
  confidence-annotated claims, cross-document tracing, and reviewer-gated
  progression. Do NOT use for single-paper analysis — use research-paper instead.
metadata:
  version: "0.5.1"
---

# Research Extraction

Apply `kb-conventions` skill for annotation markers, KB directory layout,
frontmatter schema, and synthesis impact rules.

Multi-axis, confidence-annotated extraction from a research corpus using a
**Workflow** that fans out extractor subagents and gates progression through
a reviewer agent after each axis.

## Prerequisites

Add to `.claude/settings.json` (or `.claude/settings.local.json`) before running:

```json
{
  "permissions": {
    "allow": [
      "Bash(xberg *)",
      "Bash(uvx marker-pdf *)",
      "Bash(curl *)",
      "Bash(mkdir *)",
      "Bash(cp *)",
      "Bash(cat *)"
    ]
  }
}
```

For fully unattended runs (CI, cron), launch the Claude Code session with `--dangerously-skip-permissions` instead.

## When to use

- Multiple raw source files (theses, papers, reports) covering one system
- Claims must be traceable to exact source sections with confidence markers
- Extraction spans multiple axes too large for one context window
- You want reviewer-gated, disk-persisted progression (not manual session seeds)
- Resuming a partial run — pass `resumeFromRunId` (preferred over manual restart; completed phases return from cache instantly)

## Core architecture

```
Workflow
  phase("Step 0")
    → extractor agent: reads ALL sources, writes reading summary + working memory dump
    → reviewer agent: checks summary completeness, returns confirmed facts JSON

  phase("Axis N")   [sequential, one per axis]
    → extractor agent: reads seed (confirmed facts from prior phases), writes extract-<axis>.md
    → reviewer agent: runs checklist, returns {pass: bool, issues: string[], confirmed_facts: ...}
    → if !pass: re-run extractor with issues until pass (max 2 retries)

  phase("Formalization")
    → extractor agent: reads all confirmed extract-*.md, produces code sketches
    → reviewer agent: checks sketch coverage
```

Each phase writes its output to disk before the next begins.
Reviewer is a **separate agent** — independent read of the output file, no shared context with extractor.

## Invoking the skill

Before building `args`, ask the user two questions:
1. **"Should the workflow continue past phase failures, or halt on first failure?"** — sets `continueOnFailure`
2. **"Should a writing quality (anti-slop) pass run over each output document?"** — if yes, set `antislopSkillPath` to the absolute path of `anti-slop/SKILL.md` Set `continueOnFailure: true` for unattended/autonomous runs, `false` (default) for interactive runs where you want to inspect failures immediately.

When the user says "run research extraction on <corpus>", execute this workflow:

```javascript
// In main agent — invoke Workflow tool with this script

export const meta = {
  name: 'research-extraction',
  description: 'Multi-axis extraction from research corpus with reviewer gating',
  phases: [
    { title: 'Acquisition', detail: 'Acquire, extract, and create source.md per source' },
    { title: 'Step 0', detail: 'Reading summary + working memory dump' },
    { title: 'Architecture', detail: 'extract-architecture.md' },
    { title: 'Messages', detail: 'extract-messages.md' },
    { title: 'Algorithms', detail: 'extract-algorithms.md' },
    { title: 'Forms', detail: 'extract-forms.md' },
    { title: 'Formalization', detail: 'Code sketches for all SKETCH NEEDED markers' },
    { title: 'Anti-slop', detail: 'Writing quality pass over all axis output files' },
  ],
}

// args = {
//   topic: string,              // absolute path to topic directory root
//   rawSources: {               // sources to acquire, extract, and register
//     slug: string,             // directory name under topic/sources/
//     path?: string,            // local file path (provide path OR url)
//     url?: string,             // remote URL to download
//     type?: string,            // llm-wiki type: paper|article|book-chapter|... (default: paper)
//   }[],
//   kb: string[],               // absolute paths to knowledge base files to cross-ref
//   outputDir: string,          // where to write extract-*.md files (use topic/drafts/)
//   axes: {                     // per-axis config (order = execution order)
//     name: string,             // e.g. "Architecture"
//     outputFile: string,       // absolute path for this axis output
//     extractionSpec: string,   // what to extract (H2/H3 structure, tables, etc.)
//   }[],
//   continueOnFailure?: boolean, // if true, log failed phases and continue instead of halting
//   antislopSkillPath?: string,  // absolute path to anti-slop/SKILL.md; if provided, runs a final anti-slop pass over all axis output files
// }

// ── Helpers ───────────────────────────────────────────────────────────────────

const STATUS_FILE = `${args.outputDir}/extraction-status.md`

async function writeStatus(currentPhase, completed, failed, notes) {
  const lines = [
    `# Extraction status`,
    ``,
    `phase: ${currentPhase}`,
    `completed: [${completed.join(', ')}]`,
    `failed: [${failed.join(', ')}]`,
    notes ? `notes: ${notes}` : '',
  ].filter(Boolean)
  await agent(`Write this exact content to ${STATUS_FILE}:\n\n${lines.join('\n')}`,
    { label: 'write-status', phase: currentPhase })
}

async function writeIssues(phaseName, issues) {
  const path = `${args.outputDir}/review-issues-${phaseName.toLowerCase().replace(/ /g, '-')}.md`
  const content = `# Review issues — ${phaseName}\n\n${issues.map(i => `- ${i}`).join('\n')}`
  await agent(`Write this exact content to ${path}:\n\n${content}`,
    { label: `write-issues:${phaseName}`, phase: phaseName })
}

const completedPhases = []
const failedPhases = []

const CONFIDENCE_RULES = `
Every non-trivial claim carries one of three markers placed after the source citation:

| Marker | Meaning |
|---|---|
| [DIRECT] | Verbatim or near-verbatim — copy exact passage into fenced quote block |
| [INFERRED] | Derived from 2+ passages — name all exact section numbers + one-sentence reasoning |
| [SPECULATIVE] | Not grounded in specific passage — follow with > ⚠ SPECULATIVE: block |

Rules:
- [SPECULATIVE] never in a table cell without > ⚠ SPECULATIVE: block immediately below
- [INFERRED] requires exact section numbers — if unavailable, downgrade to [SPECULATIVE]
- [DIRECT] requires exact quoted passage in fenced quote block

Divergence/absence markers:
- > ⚠ DIVERGES FROM KB: — contradicts or extends the knowledge base
- > ✦ NEW: — not present in knowledge base
- > ∅ NOT FOUND IN SOURCES: — source is silent (do not omit — absence is data)
`

// Shared quality rules — used by both extractor self-check and reviewer checklist.
const QUALITY_RULES = `
- Every section has at least one [DIRECT] or [INFERRED] citation in its body OR in the first H3 sub-section beneath it (citations in sub-sections satisfy the parent requirement — do not fail a section whose content lives in labelled sub-sections that each carry their own citations; sections whose primary content is a structural comparison or data-flow table satisfy this requirement via table column attribution such as Document/Source/paper-ref columns — do not require inline [DIRECT]/[INFERRED] markers in the prose of such sections)
- No [SPECULATIVE] claim without > ⚠ SPECULATIVE: block immediately below
- No [INFERRED] claim without exact source section numbers (§N.N) or exact heading in quotes for wiki files (§"Heading Name") — if unavailable, downgrade to [SPECULATIVE]
- Every silent extraction point marked > ∅ NOT FOUND IN SOURCES: as a standalone blockquote (not only in a table cell)
- Every ∅ in a table cell also has a standalone > ∅ NOT FOUND IN SOURCES: blockquote immediately after the table
- Cross-document data-flow table Document column cites original sources (thesis, paper, wiki/ slug) — NOT the current extraction file itself
- All DIVERGES FROM KB and NEW flags present where needed
`

const hasKB = (args.kb || []).length > 0
const QUALITY_RULES_FOR_REVIEWER = hasKB
  ? QUALITY_RULES
  : QUALITY_RULES.split('\n').filter(l => !l.includes('DIVERGES FROM KB')).join('\n')

const AXIS_REVIEWER_CHECKLIST = `
Reviewer checklist — return JSON {pass: bool, issues: string[]}:
${QUALITY_RULES_FOR_REVIEWER}
- Cross-document data-flow table present and complete at end of document
- File written to disk and non-empty
- Return ALL issues found — be exhaustive. Do not stop at 3–5. A pass means zero issues remain.
`

const FORM_REVIEWER_CHECKLIST = `
Reviewer checklist — return JSON {pass: bool, issues: string[]}:
- Every <!-- SKETCH NEEDED: ... --> placeholder has a corresponding sketch in ## Rust Sketches (formalization pass) at the end of its file
- Each sketch cites the claim it formalizes with section reference and confidence marker [DIRECT], [INFERRED], or [SPECULATIVE]
- No sketches appear outside the ## Rust Sketches (formalization pass) section
- Files are written to disk and non-empty
- Return ALL issues found — be exhaustive. Do not stop at 3–5. A pass means zero issues remain.
`

const STEP0_REVIEWER_CHECKLIST = `
Reviewer checklist — return JSON {pass: bool, issues: string[]}:
- Reading summary has exactly one paragraph per source file
- Each paragraph states: scope, contradictions noticed, axes the source is silent on
- Working memory dump is comprehensive — includes named entities, message types,
  equations, agent names, algorithm names, each marked with source section number
- Both files are non-empty and written to disk
- Return ALL issues found — be exhaustive. A pass means zero issues remain.
`

const RESULT_SCHEMA = {
  type: 'object',
  properties: {
    pass: { type: 'boolean' },
    issues: { type: 'array', items: { type: 'string' } },
    confirmed_facts: { type: 'string' },   // markdown block — facts to carry forward
    confirmed_absences: { type: 'string' }, // markdown block — sources silent on this axis
    divergences: { type: 'string' },        // markdown block — DIVERGES FROM KB / NEW flags
  },
  required: ['pass', 'issues'],
}

// ── Acquisition phase: acquire, extract, source.md per source ─────────────────
phase('Acquisition')

const acquiredSources = await parallel(args.rawSources.map(src => async () => {
  const sourceDir = `${args.topic}/sources/${src.slug}`
  const extractedPath = `${sourceDir}/extracted.md`
  const sourceMdPath = `${sourceDir}/source.md`

  await agent(`
You are a source acquisition assistant running research-paper Steps 1–3 for one source.

Source slug: ${src.slug}
Source dir:  ${sourceDir}
${src.url  ? `URL:         ${src.url}`  : ''}
${src.path ? `Local path:  ${src.path}` : ''}
Type:        ${src.type || 'paper'}

## Step A — Check if already acquired
If ${extractedPath} already exists, skip to Step C (source.md only).

## Step B — Acquire and extract (only if ${extractedPath} does not exist)
1. Run: mkdir -p ${sourceDir}
2. Acquire:
${src.url  ? `   curl -L "${src.url}" -o "${sourceDir}/original.pdf"` : `   cp "${src.path}" "${sourceDir}/original.pdf"`}
3. Detect PDF type:
   xberg detect "${sourceDir}/original.pdf"
4. Extract:
   - Machine-readable: xberg extract "${sourceDir}/original.pdf" --content-format markdown --output "${extractedPath}"
   - Scanned/image:
       uvx marker-pdf marker_single "${sourceDir}/original.pdf" --output_dir "${sourceDir}/marker-out/"
       then: mv "${sourceDir}/marker-out/original/original.md" "${extractedPath}"
       (marker-pdf writes <input-stem>.md inside <output_dir>/<input-stem>/ — move it to extracted.md)

## Step C — Create source.md (skip if ${sourceMdPath} already exists)
Write ${sourceMdPath} with this frontmatter:
\`\`\`yaml
---
title: "<infer from PDF title page, URL, or filename>"
type: ${src.type || 'paper'}
summary: ""
tldr: ""
status: draft
last_updated: "<today YYYY-MM-DD>"
tags: []
read_when: []
sources: []
concepts: []
confidence: 0.5
claims: []
---
\`\`\`
Leave summary, tldr, tags, claims, concepts empty — populated after analysis.
  `, { label: `acquire:${src.slug}`, phase: 'Acquisition' })

  return extractedPath
}))

// ── Phase 0: Reading summary ──────────────────────────────────────────────────
phase('Step 0')

const sourcePaths = acquiredSources.filter(Boolean).join('\n  ')
if (!sourcePaths) {
  log('Acquisition failed — no sources extracted. Check review-issues files.')
  return { status: 'failed', phase: 'Acquisition', issues: ['All source acquisitions failed'] }
}
const kbPaths = (args.kb || []).join('\n  ')

let step0Result = null
let step0Attempts = 0

while (!step0Result?.pass && step0Attempts < 3) {
  step0Attempts++

  const issueContext = step0Result?.issues?.length
    ? `\n\nPrevious attempt had these issues — fix them:\n${step0Result.issues.map(i => `- ${i}`).join('\n')}`
    : ''

  const skipStep0 = step0Attempts === 1
    ? `\n\nIDEMPOTENCY CHECK: First check if BOTH files below already exist and are non-empty.\nIf they do, skip writing — go directly to the context window discipline note and stop.\n`
    : ''

  await agent(`
You are a research extraction assistant. Read ALL source documents listed below.
Write TWO files to disk, then stop. Do NOT begin any extraction axis document yet.
${skipStep0}
## Source documents — read ALL before writing anything
  ${sourcePaths}

## Knowledge base — cross-reference every claim
  ${kbPaths}

## File 1: ${args.outputDir}/step0-reading-summary.md
One paragraph per source file containing:
- What the source covers and its scope
- Any immediate contradictions between sources
- Whether the source is silent on any major extraction axis

## File 2: ${args.outputDir}/step0-working-memory-dump.md
A comprehensive dump of ALL facts, definitions, agent names, message types,
algorithms, equations, and structural details found across all sources.
Organize by source file. Mark every fact with its source section number.
This file is the seed for all subsequent extraction agents.

${CONFIDENCE_RULES}

Context window discipline:
- Write both files to disk before stopping.
- If context usage exceeds 70%, write what you have with ∅ NOT FOUND IN SOURCES
  placeholders and stop — do not continue past 70%.

${issueContext}
  `, { label: `step0-extractor (attempt ${step0Attempts})`, phase: 'Step 0' })

  step0Result = await agent(`
You are a reviewer for a research extraction workflow.

Read these two files:
  ${args.outputDir}/step0-reading-summary.md
  ${args.outputDir}/step0-working-memory-dump.md

${STEP0_REVIEWER_CHECKLIST}

Also extract into confirmed_facts: a markdown summary of the most important facts
from the working memory dump, organized by topic. This will seed the axis agents.
  `, { label: 'step0-reviewer', phase: 'Step 0', schema: RESULT_SCHEMA })
}

if (!step0Result?.pass) {
  await writeIssues('Step 0', step0Result?.issues || [])
  failedPhases.push('Step 0')
  await writeStatus('Step 0', completedPhases, failedPhases, 'failed after 3 attempts')
  log('Step 0 failed — issues written to review-issues-step-0.md')
  if (!args.continueOnFailure) return { status: 'failed', phase: 'Step 0', issues: step0Result?.issues }
  log('continueOnFailure=true — proceeding with empty confirmed facts')
}

completedPhases.push('Step 0')
await writeStatus('Step 0', completedPhases, failedPhases)
log('Step 0 confirmed ✓')

// ── Axis phases: sequential, reviewer-gated ───────────────────────────────────

let carriedFacts = step0Result.confirmed_facts || ''
let carriedAbsences = ''
let carriedDivergences = ''
const completedAxes = []

for (const axis of args.axes) {
  phase(axis.name)

  let axisResult = null
  let axisAttempts = 0

  while (!axisResult?.pass && axisAttempts < 3) {
    axisAttempts++

    const issueContext = axisResult?.issues?.length
      ? `\n\nPrevious attempt issues — fix all of them:\n${axisResult.issues.map(i => `- ${i}`).join('\n')}`
      : ''

    // Idempotency: skip extractor if output already exists and is non-empty.
    // Still runs reviewer to confirm quality and carry facts forward.
    const skipExtractor = axisAttempts === 1
      ? `\n\nIDEMPOTENCY CHECK: First check if ${axis.outputFile} already exists and is non-empty.\nIf it does, skip writing — go directly to the pre-write self-check to confirm quality, then stop.\n`
      : ''

    await agent(`
You are a research extraction assistant continuing a multi-session extraction.
Prior phases are complete. Do NOT re-read source files. Use only the facts below.
${skipExtractor}

## Working memory dump — read this file before writing anything
${args.outputDir}/step0-working-memory-dump.md
This file contains exact source slugs, section headings, equation numbers, and quoted passages.
Use it as your authoritative reference for all citations — do NOT guess section headings or slug names.
For every fact the working memory dump marks as ✦ NEW, the corresponding section in your output MUST carry a standalone `> ✦ NEW:` block. Do not silently drop NEW markers.

## Your only task
Write extraction document for axis: ${axis.name}
Output file: ${axis.outputFile}
Write to disk. Stop after writing.

## Confirmed facts from prior phases
${carriedFacts}

## Confirmed absences (sources silent on these topics)
${carriedAbsences || 'None recorded yet.'}

## Confirmed divergences from KB
${carriedDivergences || 'None recorded yet.'}

## What to extract for this axis
${axis.extractionSpec}

## Confidence rules (mandatory)
${CONFIDENCE_RULES}

## Format rules
- H1 title: Extraction — ${axis.name}
- Blockquote preamble: one sentence stating what this document extracts and which sources it is grounded in
- H2 per major concept, H3 per sub-concept
- Source attribution on every non-trivial claim: [source §N.N] [DIRECT|INFERRED|SPECULATIVE]
- For [DIRECT]: copy exact passage into fenced quote block
- Tables for mappings, parameter lists, comparisons
- End with cross-document data-flow table:
  | Data object | Produced by | Consumed by | Document | Section |
- No code sketches — mark <!-- SKETCH NEEDED: <reason> --> for formalization pass
- Cross-document data-flow table Document column: cite the ORIGINAL source (thesis, paper, wiki/ slug) — NEVER the current extraction file itself
- Table cells may contain ∅ shorthand BUT every ∅ in a table cell must ALSO have a corresponding standalone blockquote immediately after the table: > ∅ NOT FOUND IN SOURCES: <detail>
- For KB wiki files (which have no numbered sections), cite exact H2/H3 heading text in quotes: §"Heading Name" — never cite a wiki file without a heading anchor

## Pre-write self-check (mandatory — verify draft satisfies ALL before writing to disk)
${QUALITY_RULES_FOR_REVIEWER}
Fix any failures before writing.

## Context window discipline
Write to disk before stopping. If context > 70%, write with ∅ NOT FOUND IN SOURCES
placeholders and stop.

## Previously completed axes (cross-reference these)
${completedAxes.map(a => `- ${a.name}: ${a.outputFile}`).join('\n') || 'None yet.'}

${issueContext}
    `, { label: `${axis.name}-extractor (attempt ${axisAttempts})`, phase: axis.name })

    axisResult = await agent(`
You are a reviewer for a research extraction workflow.

Read the extraction document that was just written:
  ${axis.outputFile}

Also read the confirmed working memory dump for reference:
  ${args.outputDir}/step0-working-memory-dump.md

${AXIS_REVIEWER_CHECKLIST}

Also extract:
- confirmed_facts: all confirmed facts from this document (for subsequent axes)
- confirmed_absences: all ∅ NOT FOUND IN SOURCES entries
- divergences: all DIVERGES FROM KB and NEW entries
    `, { label: `${axis.name}-reviewer`, phase: axis.name, schema: RESULT_SCHEMA })
  }

  if (!axisResult?.pass) {
    await writeIssues(axis.name, axisResult?.issues || [])
    failedPhases.push(axis.name)
    await writeStatus(axis.name, completedPhases, failedPhases, 'failed after 3 attempts')
    log(`${axis.name} failed — issues written to review-issues-${axis.name.toLowerCase()}.md`)
    if (!args.continueOnFailure) return { status: 'failed', phase: axis.name, issues: axisResult?.issues }
    log(`continueOnFailure=true — skipping ${axis.name}, continuing with remaining axes`)
    continue
  }

  // Carry confirmed facts forward
  carriedFacts += `\n\n### ${axis.name}\n${axisResult.confirmed_facts || ''}`
  carriedAbsences += `\n\n### ${axis.name}\n${axisResult.confirmed_absences || ''}`
  carriedDivergences += `\n\n### ${axis.name}\n${axisResult.divergences || ''}`
  completedAxes.push(axis)
  completedPhases.push(axis.name)
  await writeStatus(axis.name, completedPhases, failedPhases)

  log(`${axis.name} confirmed ✓`)
}

// ── Formalization pass ────────────────────────────────────────────────────────
phase('Formalization')

const axisFiles = args.axes.map(a => `  ${a.outputFile}`).join('\n')

let formResult = null
let formAttempts = 0

while (!formResult?.pass && formAttempts < 3) {
  formAttempts++

  const issueContext = formResult?.issues?.length
    ? `\n\nPrevious attempt issues:\n${formResult.issues.map(i => `- ${i}`).join('\n')}`
    : ''

  await agent(`
You are a research extraction assistant performing the formalization pass.
All extraction axes are confirmed. Read only the extraction documents below —
do NOT re-read raw sources.

## Extraction documents to read
${axisFiles}

## Your task
Find every <!-- SKETCH NEEDED: <reason> --> placeholder across all documents.
For each placeholder, produce the requested code sketch (Rust struct, enum,
function signature, or pseudocode) in a new section at the end of the same file.

Each sketch must:
- Cite the claim(s) it formalizes with section references and confidence markers
- Appear under a ## Rust Sketches (formalization pass) section at end of the file
- Be marked with its confidence: [DIRECT], [INFERRED], or [SPECULATIVE]
- Use fenced rust blocks for Rust, fenced text blocks for pseudocode

Do not modify any other content in the extraction documents.
Write all changes to disk before stopping.

${issueContext}
  `, { label: `formalization-extractor (attempt ${formAttempts})`, phase: 'Formalization' })

  formResult = await agent(`
You are a reviewer for the formalization pass.

Read all extraction documents:
${axisFiles}

${FORM_REVIEWER_CHECKLIST}
  `, { label: 'formalization-reviewer', phase: 'Formalization', schema: RESULT_SCHEMA })
}

if (!formResult?.pass) {
  await writeIssues('Formalization', formResult?.issues || [])
  failedPhases.push('Formalization')
  await writeStatus('Formalization', completedPhases, failedPhases, 'failed after 3 attempts')
  log('Formalization failed — issues written to review-issues-formalization.md')
  if (!args.continueOnFailure) return { status: 'failed', phase: 'Formalization', issues: formResult?.issues }
  log('continueOnFailure=true — proceeding to final summary with failed formalization')
}

completedPhases.push('Formalization')
await writeStatus('Formalization', completedPhases, failedPhases, 'complete')
log('Formalization confirmed ✓')

// ── Anti-slop pass (optional) ─────────────────────────────────────────────────
if (args.antislopSkillPath) {
  phase('Anti-slop')
  await parallel(args.axes.map(axis => () => agent(`
You are a writing quality editor. Apply the anti-slop rules to improve this document.

## Anti-slop skill — read this file first for the full checklist
${args.antislopSkillPath}

## Document to improve
${axis.outputFile}

Read the skill file, then read the document, apply all improvements in-place, and write
the improved version back to disk. Do NOT change any citation markers, confidence annotations,
blockquotes, code blocks, or SKETCH NEEDED comments — only prose quality.
  `, { label: `anti-slop:${axis.name}`, phase: 'Anti-slop' })))
  log('Anti-slop pass complete ✓')
}

// ── Final summary ─────────────────────────────────────────────────────────────
return {
  status: failedPhases.length > 0 ? 'partial' : 'complete',
  failedPhases,
  statusFile: STATUS_FILE,
  files: [
    `${args.outputDir}/step0-reading-summary.md`,
    `${args.outputDir}/step0-working-memory-dump.md`,
    ...args.axes.map(a => a.outputFile),
  ],
  divergences: carriedDivergences,
  absences: carriedAbsences,
}
```

## args shape

Pass `args` to the Workflow tool as a JSON object:

```json
{
  "topic": "/path/to/topic",
  "rawSources": [
    { "slug": "thesis",  "path": "/local/thesis.pdf",         "type": "book-chapter" },
    { "slug": "paper2",  "url":  "https://arxiv.org/pdf/...", "type": "paper" }
  ],
  "kb": [
    "/path/to/topic/synthesis/architecture.md",
    "/path/to/topic/synthesis/theoretical-foundations.md"
  ],
  "outputDir": "/path/to/topic/drafts",
  "axes": [
    {
      "name": "Architecture",
      "outputFile": "/path/to/topic/drafts/extract-architecture.md",
      "extractionSpec": "Extract: system boundaries, agent taxonomy, cognitive levels, ontology, systemic loop equations, supervision model."
    },
    {
      "name": "Messages",
      "outputFile": "/path/to/topic/drafts/extract-messages.md",
      "extractionSpec": "Extract: all named message types (table: name/sender/receiver/payload/trigger), message flow per cognitive level, control messages, sensor/effector messages, sequencing constraints."
    },
    {
      "name": "Algorithms",
      "outputFile": "/path/to/topic/drafts/extract-algorithms.md",
      "extractionSpec": "Extract: all named algorithms with pseudocode, parameters table, complexity, which agent runs it, online vs offline. Required: morphological form computation, form distance, objective score, PES decision, SOKM if present, attention weight update, emotional state classification."
    },
    {
      "name": "Forms",
      "outputFile": "/path/to/topic/drafts/extract-forms.md",
      "extractionSpec": "Extract: precise mathematical definition of morphological form, form space topology, target forms, emotional form classification, form evolution, level-1 histogram, level-2 chunk pattern, level-3 compositional form."
    }
  ]
}
```

Adjust `axes` array to match your corpus. Add or remove axes freely.

`topic` is the absolute path to the topic root. `rawSources` drives the Acquisition phase — each entry becomes `topic/sources/<slug>/`. Each source is extracted via `xberg` (machine-readable PDFs) or `marker-pdf` (scanned/image PDFs); `source.md` is created with draft metadata. Already-acquired sources (existing `extracted.md`) are skipped automatically.
`outputDir` maps to `<topic>/drafts/` — all working extraction documents land there, not in `synthesis/`.

## Confidence annotation quick reference

See `kb-conventions` skill — `## Confidence annotation` section for the canonical marker table and rules.

The `CONFIDENCE_RULES` constant in the workflow script above is the inline copy injected into agent prompts (agents cannot invoke skills directly).

## Monitoring and resume

While the workflow runs, check progress with:
```bash
cat <outputDir>/extraction-status.md        # current phase, completed, failed
cat <outputDir>/review-issues-<axis>.md     # why a phase failed
```

To resume a failed run, copy the `runId` from the Workflow tool result (returned when you launched it),
then pass it back:
```json
{ "resumeFromRunId": "<runId from Workflow tool result>" }
```
Completed agent() calls return from cache instantly; only failed/new calls re-run.

## Common mistakes

**Extractor re-reads sources in axis phase**
→ Seed prompt says "Do NOT re-read source files". Reviewer checks for this.

**[INFERRED] without section numbers**
→ Reviewer flags it. Extractor downgrades to [SPECULATIVE].

**[INFERRED] citing a wiki KB file without heading anchor**
→ Wiki files have no numbered sections. Use §"Exact Heading Name" syntax: `[KB theoretical-foundations.md §"What each framework contributes"]`.

**Sketches during extraction phase**
→ Reviewer flags. Extractor replaces with `<!-- SKETCH NEEDED: ... -->`.

**Reviewer shares context with extractor**
→ Reviewer is always a separate `agent()` call — never inline with extractor.

**Proceeding to next axis on failed review**
→ Default: workflow halts after 3 retries with `status: 'failed'`. Set `continueOnFailure: true` in args to log and continue instead; final result will be `status: 'partial'` with `failedPhases` list.

**Section body has no citation (content only in sub-sections)**
→ Citations in H3 sub-sections satisfy the parent section requirement. Reviewer must not fail a section whose claims live in labelled sub-sections that each carry their own citations.

**∅ only in a table cell, no standalone blockquote**
→ Every ∅ in a table must ALSO have a `> ∅ NOT FOUND IN SOURCES:` blockquote immediately after the table.

**Cross-document data-flow table Document column cites the extraction file itself**
→ Document column must cite the original source (thesis §, paper §, wiki/ slug). The extraction document is not a source.

**Extractor guesses section headings and source slugs**
→ Root cause: extractor receives `carriedFacts` (a compressed summary) but has no direct access to source text. It will fabricate section headings like `§"Basal synapses"` when the real heading is `§"Neurons Reliably Recognize Multiple Sparse Patterns"`, or confuse source slug assignments. Fix is already in the workflow script: the axis extractor is instructed to read `step0-working-memory-dump.md` as its authoritative citation reference. If wrong headings keep appearing, verify the working memory dump actually contains correct headings for the section in question.

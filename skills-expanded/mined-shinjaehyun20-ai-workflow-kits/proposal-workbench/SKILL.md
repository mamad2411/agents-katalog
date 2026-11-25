---
name: proposal-workbench
description: >
  Perplexity thread, RFP, URL, or raw brief를 입력받아 근거가 분리된 제안 블록,
  발표 storyboard gate, 실행 task pack, verifier close gate까지 한 벌로 만드는
  제안/RFP 워크벤치 스킬이다.
---

# Proposal Workbench

## Use When

- Perplexity나 리서치 후보를 실제 제안/기획 산출물로 승격해야 한다.
- RFP, URL, 보도자료, 회의 메모를 제안서 섹션과 근거표로 바꿔야 한다.
- 초안 작성보다 source evidence, storyboard, 실행 보드, close gate가 더 중요하다.

## Input Contract

- Accept one or more of: Perplexity thread URL/title, RFP file path, source URL, memo, meeting note, or local evidence package.
- When the user references the 20260618 Perplexity proposal package, treat this as the default source package:
  `<local-evidence-root>/perplexity_project_proposals_20260618`.
- For that package, prefer `proposal_candidates.json` as the machine-readable entrypoint when present.
- Lock scope before drafting: target buyer, opportunity, source boundary, output format, and whether the result is for screening, proposal writing, or delivery planning.

## Workflow

1. Source truth gate: record candidate id, URL/thread, file path, capture date, source boundary, and excluded sources.
2. Evidence matrix: separate source claims, proposal interpretation, verification status, risk, and required follow-up.
3. Slot manifest: map evidence rows into reusable proposal slots before drafting long-form output.
4. Proposal blocks: write problem, buyer pain, offer, differentiator, rollout approach, risk response, proof, and next action.
5. Storyboard gate: create slide-by-slide message, evidence row, visual idea, decision needed, and QA criterion before any deck work.
6. Patch preview gate: show what will change before touching an existing proposal, deck, or submission file.
7. Task pack: convert accepted blocks into owner, next action, artifact, dependency, verifier, close gate, and due/priority fields.
8. Verifier close gate: confirm every claim points to an evidence row or is explicitly marked as hypothesis, assumption, or open risk.

## Outputs

- `opportunity_memo.md`
- `evidence_matrix.md` or `evidence_matrix.xlsx`
- `proposal_blocks.md`
- `storyboard_gate.md`
- `execution_board.csv`
- `verification.md`

## Quality Bar

- Keep source excerpts short and cite paths, URLs, or row ids instead of copying long passages.
- Do not collapse evidence and recommendation into one paragraph; keep traceability visible.
- Prefer a compact package over prose-only output when the task is execution-oriented.
- If a source is not directly opened or parsed in the current run, label it as unverified.

## Verifier Close Gate

- Required files exist in the requested output location.
- Evidence matrix has at least one row for each source-derived claim used in proposal blocks.
- Slot manifest shows which evidence rows drive each proposal section.
- Storyboard gate exists before any PPTX/deck production is marked ready.
- Execution board has clear owner/action/verifier/close-gate columns.
- Final report lists evidence paths and unresolved risks.

## Stop Rules

- Do not treat a similar repo as evidence for the named source package.
- Do not create a deck before storyboard gate exists.
- Do not present source-derived claims as verified if only Perplexity summary was read.
- Do not close the task from chat text alone; close only with files, paths, and verifier results.

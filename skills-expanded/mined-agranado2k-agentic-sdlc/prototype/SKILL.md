---
name: prototype
description: Answer a design or feasibility question with explicitly throwaway spike code — never committed, findings recorded in the diary or an ADR draft. Use when a decision is blocked on "would X even work?" (library capability, API behavior, performance shape). Not for building features — that's /tdd via /implement.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
metadata:
  phase: implementer
---

# /prototype — throwaway spikes for design questions

`/grill-with-docs` resolves *requirement* uncertainty; this skill resolves *feasibility* uncertainty. The output is an **answer**, not code. Shared invariant §1 names it directly: feasibility questions are answered by a throwaway spike outside the production tree, never by speculative production code that "we might keep".

## Rules

1. **State the question first**, as a falsifiable sentence ("the editor library can preserve an `id` attribute on block nodes through a serialize round-trip: true/false?"). If you can't phrase the question, you're not ready to spike.
2. **Spike code lives outside the repo tree** — use the session scratchpad directory (or `$TMPDIR`), never a path under the project, so it cannot be committed by accident. It may add whatever dependencies it likes *there*; the repo's dependency policy (`constitution/local-engineering.md`) does not apply to throwaway dirs.
3. **Timebox it.** A spike that runs long is answering a different, bigger question — stop and say so.
4. **No production standards apply**: no tests, no lint, hardcode everything. Speed to signal is the only metric. (This is the one place the test-first rule is suspended, and it is suspended precisely because nothing here survives.)
5. **The code is discarded; the finding is recorded.** Write the answer (question, verdict, evidence, surprises) into `docs/diary.md` as a dated entry — or into the relevant ADR draft when the spike settles a decision under `/grill-with-docs`. Cite versions of anything probed (library, API, service) since answers rot.
6. **Never promote spike code.** If the answer is "yes, build it", the production implementation starts fresh through `/implement` + `/tdd`. Copying spike code into the repo skips the test-first contract and imports every hardcoded shortcut with it.

## Procedure

1. Phrase the question (rule 1). Confirm a spike is cheaper than reading the docs — check primary documentation first; many spikes are answerable by reading.
2. Build the smallest program that produces the signal, in the scratch dir.
3. Run it; capture the evidence (output, timing, error).
4. Record the finding (rule 5) — and the verdict in the trace, with the captured evidence as a blob rather than a line: `sh scripts/trace.sh emit kind=spike.verdict [subject=<prd:#N or ticket:#N, when the question came from one>] outcome=true|false|inconclusive --blob <file> data.question='<the question, one line>' reason='<the verdict, with the versions probed, one line>' || :`. The trace is written here and never read (the kit's ADR-0008); unconfigured, the call is a silent no-op. Then delete the spike dir, and report: question → verdict → what it unblocks.

---
name: second-model-consensus
description: Run a bounded cross-model consensus loop — a fresh second-model reviewer (Codex Sol, agy Gemini, or another Claude) adversarially reviews a proposal/diff/conclusion through verdict-contract rounds until PASS or round cap. Invoke when the user asks for a second model's opinion, when landing guidance/kernel/rules changes, or when a conclusion needs independent cross-model backing. Even a 1% chance this applies means invoke it.
---

# second-model-consensus

You are the proposer and round-driver. The reviewer is always a FRESH
second-model worker that reads the live artifacts itself — never your
paraphrase, never the author's own session.

## BYPASS — check FIRST

- Trivial single-file reversible change with objective acceptance → no
  consensus round; land it.
- The user already gave an explicit verdict on the exact text → their word
  outranks any model reviewer; do not re-litigate.
- Code review of an implementation diff → `code-review` /
  `pr-review-toolkit` own that; this skill is for proposals, guidance,
  plans, audits, and cross-model verdicts.

## TRIGGER

- Kernel / routed-rules / skill edits (maintenance.md §1 traffic) after user
  approval-in-principle: user approval sets scope, the consensus round
  guards quality. Consensus NEVER substitutes for the user's approval.
- Audit conclusions or recommendation lists the user will act on.
- Any "和 codex/gemini 討論" / "give me a second opinion" request.

## CONTRACT — every round, no exceptions

1. **Reviewer**: model-dispatch §1/§4 review row — fresh `gpt-5.6-sol`
   medium via `agent-tmux codex`; `gemini-3.6-flash-medium` via `agent-tmux agy` for a
   third perspective; fresh Claude `opus`/`sonnet` via Agent for
   Claude-side. Reviewer is never the author (model-dispatch §6).
2. **Round prompt** (file in the session scratchpad, one per round):
   - GOAL + WHY — what is being judged and who asked.
   - CONTEXT — pointers to LIVE files the reviewer must read
     (repo paths, artifact paths), plus the exact proposed diff/claims.
   - CHECKS — numbered, objectively answerable; each gets PASS/FAIL.
   - ACCEPTANCE — per-check verdict + reason + file:line; last line exactly
     `VERDICT: PASS` | `VERDICT: BLOCK` (or AGREE/BLOCK for positions).
   - REPORT — full review appended to ONE shared consensus artifact
     (`<scratchpad>/<topic>-consensus.md`, one `## Round N` section per
     round); verdicts also in the result summary. Read-only, no fixes.
3. **Dispatch mechanics**: defer to `using-tmux-agent-tools` — one-shot
   bounded worker, native haiku supervision proxy, blocking supervise,
   result.json contract. Two-way back-and-forth in one sitting →
   `tmux-agent-dialogue` instead of serial one-shots.
4. **Convergence loop**:
   - `VERDICT: PASS` → land/report; done.
   - `VERDICT: BLOCK` → fix ONLY what the FAILs name (adopt the reviewer's
     minimal wording when offered), or rebut with fresh evidence in the
     next round prompt. Next round re-verifies ONLY the former FAILs plus a
     regression check — never re-opens PASSed checks without new evidence.
   - Round cap 4 (count every worker round). Cap hit or a FAIL you believe
     is wrong twice → stop, present both positions to the user
     (judgment-rubrics §6), never a fifth silent round.
5. **Multi-model panel** (optional): run Sol + Gemini in parallel on the
   same round prompt for orthogonal blindspot coverage. Disagreement
   between reviewers is a finding to surface, not to average away.

## Round-prompt skeleton

```
GOAL: Round N — adversarial review of <thing>. WHY: <user ask / gate>.
CONTEXT: read live: <paths>. Proposed change/claims: <exact text or diff>.
Prior rounds: <consensus artifact path> (Round N re-verifies only: <FAIL list>).
CHECKS: 1..K numbered, objective.
ACCEPTANCE: per-check PASS/FAIL + ≤2-line reason + file:line;
  last line exactly one of: VERDICT: PASS | VERDICT: BLOCK. Read-only.
REPORT: append "## Round N" to <consensus artifact>; verdicts in result summary.
> Do not spawn additional tmux sessions or delegate further.
> Write the structured completion (result.json contract, schema_version 1)
> to the literal result path injected into this prompt.
```

## Red flags that have actually burned us

- 「我轉述提案給 reviewer 就好」— the reviewer must read the LIVE landed
  text; a paraphrase hid a dropped `without logging secrets` guarantee once.
- 「PASS 了大部分，先上」— one FAIL = BLOCK. Land only after the fix or an
  explicit user override of that named FAIL.
- 「這輪重跑全部 CHECKS」— re-verify rounds scope to former FAILs; full
  re-runs burn rounds and invite verdict drift.
- 「reviewer 沒回報，應該是好了」— no verdict line = no round. Idle worker
  → capture once, classify, resend via send-wait, require a fresh nonce
  (see shared memory: startup screens swallow initial prompts).
- 「模型們同意就等於用戶同意」— consensus gates quality; the user gates
  scope. Protected edits still follow maintenance.md §1.

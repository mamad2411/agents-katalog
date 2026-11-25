---
name: jury
description: "Put a question or decision to a jury of 3 or 5 subagents: blind independent votes, one anonymized review round, and a verdict with the vote, dissent, and first action when at least one blind vote succeeds."
argument-hint: "<question or decision> [5 for a five-seat panel]"
disable-model-invocation: true
compatibility: Requires independent subagents. Uses the repository peer policy to keep every seat on the host or select a capability-aware Claude, Codex, Cursor Agent, or OMP adapter.
license: MIT
---

# Jury

One model asked once gives one line of reasoning, and asking it to debate itself mostly makes it agree with itself. A jury gets independence from separate subagents that vote blind, and it gets correction from one review round where every vote change must name its reason. You are the foreman: you frame, dispatch, check facts, and deliver one verdict when at least one blind vote succeeds.

## Step 1: Gate

The question is the arguments. A trailing `5` sets the panel size and is not part of the question. If the question is empty, take the decision under discussion in this conversation, and if there is none, ask for it.

Stop before any dispatch when:

- The question has one checkable answer (what a function returns, what a doc says). Answer it and say that no jury was needed.
- This host cannot dispatch subagents. Say so and stop. Never play the jurors yourself in one context: a juror that has read the other answers is not independent.

## Step 2: Brief

Read what the question needs once: the code, docs, links, and conversation it points at. Then write the **brief**, the only thing every juror sees:

- **Question**: one sentence.
- **Options**: two to four, with neutral labels (A, B, C, or short plain names). A juror may also answer "none", with a better framing.
- **Criteria**: two to four things a good answer must do well.
- **Facts**: each with its source (`path:line`, URL, or "user said").
- **Constraints**: budget, deadline, what cannot change.

Leave your own leaning out of the brief, and leave out any option label that judges ("the safe option"). Ask the user one question only if you cannot name the options. Show the brief, then continue without waiting.

## Step 3: Seat the panel

Seat three jurors, or five when the arguments end in `5`. Each seat gets one **lens**, in table order. A lens tells the juror where to look. It does not pick the juror's side, so every vote is free.

| # | Lens | Question the lens asks |
|---|------|------------------------|
| 1 | Pre-mortem | It is a year later and this choice failed. What caused it? |
| 2 | First principles | Set aside how it is usually done. What does the problem itself require? |
| 3 | Cost | What does each option cost to build, to run, and to undo? |
| 4 | Outsider | What does someone with no history in this choice see? |
| 5 | Evidence | Which facts in the brief carry the decision, and how solid is each? |

Resolve `docs/agents/cross-model.json` exactly once through the [harness contract](../../references/harnesses.md). Record the selected CLI, model (`default` when null), effort (`default` when null, `unsupported` for Cursor), family status, isolation level, and fallback reason. Host-only mode puts every seat on host subagents and records `external peer disabled by docs/agents/cross-model.json`, or the exact invalid-settings or adapter failure.

## Step 4: Blind vote

Before each round, check the host's worker limit and occupied slots. Dispatch only seats that fit, queue the rest, and start them as workers finish. If capacity is unknown, use one worker at a time. A capacity rejection leaves the seat queued; it consumes no retry and is never a reason to drop it. Every seat gets the original blind inputs, without earlier seats' answers from that round.

A host seat is a fresh subagent, never a fork of this conversation, that gets only the juror prompt. When the resolver selected an external adapter, use it for one seat as a background process with a 600000 ms timeout. Make its directory with `mktemp -d`, save the juror prompt to `<temp dir>/juror.prompt.md`, and run the adapter from the repository root. Add configured values as individual literal arguments:

```text
codex exec --ignore-user-config --disable apps --disable plugins -s read-only -c 'approval_policy="never"' [--model "$MODEL"] [-c "model_reasoning_effort=\"$EFFORT\""] --ephemeral --skip-git-repo-check -C "$REPO_ROOT" -o "<temp dir>/vote.md" - < "<temp dir>/juror.prompt.md" > "<temp dir>/peer.stdout.log" 2> "<temp dir>/peer.log"
claude -p --safe-mode --strict-mcp-config --tools Read Grep Glob --permission-mode dontAsk [--model "$MODEL"] [--effort "$EFFORT"] --no-session-persistence < "<temp dir>/juror.prompt.md" > "<temp dir>/vote.md" 2> "<temp dir>/peer.log"
agent -p --mode=ask --workspace "$REPO_ROOT" --output-format text [--model "$MODEL"] < "<temp dir>/juror.prompt.md" > "<temp dir>/vote.md" 2> "<temp dir>/peer.log"
omp -p --mode text --cwd "$REPO_ROOT" --no-session --no-title --no-tools --approval-mode always-ask --no-skills --no-rules --no-extensions [--model "$MODEL"] [--thinking "$EFFORT"] < "<temp dir>/juror.prompt.md" > "<temp dir>/vote.md" 2> "<temp dir>/peer.log"
```

Square-bracketed pairs are conditional notation. Omit them for null values, and never build or re-evaluate a command string. Cursor never receives `--force`, `--yolo`, `--approve-mcps`, `--worktree`, `--resume`, `--continue`, or `--trust`.

Immediately before each Cursor or OMP vote and review process, obtain the harness contract's interactive confirmation. Declined or unavailable confirmation replaces that seat with a host subagent. Cursor Ask mode prevents agent edits but still inherits user and repository rules, MCP, plugins, executable hooks, and persistent sessions. OMP receives no repository tools. For OMP, append every cited text source needed to assess the brief to the prompt exactly once between matching nonce-delimited `BEGIN` and `END` lines. If required evidence does not fit, replace the OMP seat with a host seat and record incomplete external coverage.

Read the answer from `vote.md`, never from process output. Accept the external seat only when the process exits zero and the answer contains a usable vote block as defined below. On timeout, nonzero status, empty or malformed output, missing evidence, usage limit, authentication failure, or rejected configured value, read `peer.log`, replace it with a host subagent using the same lens, and record the configured CLI, model, effort, and exact failure for the Panel line. An explicit mode never tries another external CLI.

The juror prompt:

```text
You are one juror on a panel of <N>. The other jurors answer the same brief on their own, and you will not see their answers. Do not ask the user anything and do not change any file. You may read files and run read-only commands to check the facts in the brief.

Your lens: <lens>: <question the lens asks>. Use it to decide where to look. It does not decide your vote: vote for the option the evidence supports.

<brief>

Return only this block:
CHOICE: <one option label, or "none: <a better framing>">
CONFIDENCE: <0-100>
REASONS: <at most 3, each with the fact or path:line it rests on>
WOULD CHANGE MY MIND: <the one finding that would flip your choice>
RISKIEST ASSUMPTION: <the assumption your choice depends on most>
```

A usable block has exactly one of each field required by that round. `CHOICE` is an option label from the brief or `none:` followed by a nonempty better framing. `CONFIDENCE` is a number from 0 through 100. In a blind vote, `REASONS` contains one to three reasons, each supported by a fact or source reference; `WOULD CHANGE MY MIND` and `RISKIEST ASSUMPTION` are nonempty. In a review vote, `REVIEW` gives every supplied position a strongest and weakest point, and `EVERYONE MISSED` is nonempty (an explicit "none" is valid). `CHANGED FROM MAJORITY BECAUSE` supplies an argument grounded in the supplied fact checks or a checked fact when the choice differs from the unique most common blind choice. If the blind top count is tied, every review choice requires such a reason; "none" is valid only when matching a unique most common blind choice. Validate host and external answers before using them; a missing, duplicate, or malformed required field makes the seat failed.

Seats may return one at a time as background notifications. Wait for every seat without writing a message for each arrival, and treat a completion notice for a seat you already have as nothing to answer. Retry a host seat that fails or returns an unusable block once, including a host replacement for a failed external seat, then drop it and note the drop. If no valid blind votes remain, report "Jury unavailable: no valid blind votes", list the exact failures, and stop without a verdict. Otherwise, tally the choices. This is the **blind vote**.

If the blind vote is unanimous and every confidence is 70 or higher, go to Step 6.

## Step 5: Review

Run one review round, never more. More rounds make jurors agree with each other, and they do not make the answer more correct.

1. **Check facts.** Find the factual claims the jurors disagree on that could change the vote. Check each against its source yourself, and mark it verified, contradicted, or unverifiable.
2. **Anonymize.** Remove the lens names from the juror blocks. Label them Position A, B, C, and give each reviewer its own shuffled order.
3. **Dispatch fresh reviewers**, one per seat, never forks, using Step 4's capacity checks and queue. Every reviewer gets the same brief, fact checks, and anonymized positions, without earlier reviewers' answers. The external seat reviews through the same selected adapter, safety flags, configured values, runtime confirmation, evidence bundle, and failure checks, with `<temp dir>/review.md` replacing `vote.md`, unless its vote failed. If that call fails, queue a host reviewer and record the configured adapter and exact swap reason. A fresh reviewer wrote none of the positions, so it has no answer of its own to protect.

The reviewer prompt:

```text
You are one reviewer on a panel of <N>. Below are anonymous positions on the same brief, in random order. Do not ask the user anything and do not change any file.

<brief>

Fact checks by the foreman:
<claim>: <verified | contradicted | unverifiable>, <source>

<Position A: juror block>
<Position B: juror block>
...

Return only this block:
REVIEW: <for each position, its strongest point and its weakest point>
EVERYONE MISSED: <what no position considered>
CHOICE: <one option label, or "none: <a better framing>">
CONFIDENCE: <0-100>
CHANGED FROM MAJORITY BECAUSE: <if the blind top count is tied or your choice differs from its unique most common choice, the argument grounded in the supplied fact checks or checked fact that decided it; otherwise "none">
```

Apply Step 4's retry-and-drop rule to review seats. If no valid review votes remain, record "review unavailable: no valid review votes" and the exact failures, then use the blind vote in Step 6. Otherwise, tally the choices. This is the **review vote**.

## Step 6: Verdict

The review vote decides, or the blind vote when Step 5 was skipped or produced no valid review votes. A review result may replace a unique blind winner or resolve tied blind leaders only when a reviewer choosing that result supplies a checked supporting reason. Otherwise retain the blind tally and apply the tie-break below: a change with no reason is agreement, not evidence.

You may overrule the majority only with a checked fact that defeats its main reason. Say so in the verdict. On a tie, pick the option whose main reason survived the fact checks. If that still ties, pick the option that is cheaper to undo.

Confidence:

- **HIGH**: all seats, or four of five, chose it, and the reasons in Why are verified or rest on files you read.
- **MEDIUM**: a majority chose it.
- **LOW**: you broke a tie, you overruled the majority, or the main reason is unverifiable.

A "none" verdict is valid: give the better framing as the verdict and the first action under it.

## Step 7: Report

Output only this block. The brief was already shown in Step 2. Show the juror blocks and reviews only if the user asks for them.

```markdown
## Verdict: <option, or "Reframe: <better framing>">

Confidence: <HIGH | MEDIUM | LOW>
Vote: blind <A 2, B 1>, review <A 3>. <what changed a vote and why, or "no change">

Why:
1. <reason, with its source>

Dissent: <the strongest case for the option that lost, in its best form>
Everyone missed: <from the reviews, "review skipped: unanimous blind vote", or "review unavailable: no valid review votes">
Riskiest assumption: <assumption>. Test: <the cheapest check>. If it fails: <the option the verdict flips to>.
First action: <one concrete step>

Panel: <N> seats (<seats per established model family, plus unverified external seats>), lenses <list>. Peer policy: CLI <name or host-only>, model <configured value or default>, effort <configured value, default, or unsupported>, family <status>, isolation <level>. <disabled reason, drops, or swaps with exact failures>
```

When every seat ran on one established model family, or external family independence is unknown, end the Panel line with: "Cross-family independence was not established, so the seats can share a blind spot." Cursor's Panel entry states inherited configuration and session persistence. OMP's entry states evidence-only inspection. When the user comes back with the result of the Test, run the jury again from Step 2 with that result as a fact.

---
name: delegate
description: Use when planning how to split work between the main session and subagents, before launching a subagent, or when a task involves screenshots, bulk reading, test runs, web research or mechanical edits. Decides what to delegate, to which model, how to brief it, and how to verify the result.
---

# Brain and hands

The main session is the brain: it decides, briefs, and verifies. Subagents on cheaper models are the hands: they do high-volume, low-judgment work and report text.

The main session only plays this role if it is a strong model. If you are yourself a Sonnet or Haiku subagent, ignore this skill and just do the work you were briefed on.

## Delegate or do it inline

Delegate when the work is high-volume and low-judgment:
- Anything with screenshots or many clicks (computer use, browser, simulator, consoles).
- Wide searches and bulk reads where only the conclusion matters.
- Running a build or test suite and reporting failures.
- Mechanical edits with a clear spec.
- Web research and data pulls.

Do it inline when:
- It is a short question or takes about three tool calls or fewer.
- The judgment is the work: design, debugging a puzzling failure, tightly coupled edits.
- Writing the brief would take about as long as the task.

Delegation adds cost: the brief, the subagent's cold start, and your verification. It pays when the raw tool output is large (it stays out of your context, which is re-read every turn) and the cheaper model's rate applies to most of the tokens.

## Pick the agent

| Agent | Model | Use for |
|---|---|---|
| `brain-and-hands:scout` | Haiku | Read-only search and summarising many files |
| `brain-and-hands:worker` | Sonnet | Executing a fully specified change, build or test run |
| `brain-and-hands:researcher` | Sonnet | Sourced web or document research |
| `brain-and-hands:operator` | Sonnet | Screens, consoles, forms, anything with screenshots |

Haiku only for simple reads or a few obvious clicks. If a task needs judgment mid-way, use Sonnet.

## Brief completely

The subagent starts cold and sees nothing of this conversation. Every brief has:
1. **Goal**: one sentence on what and why.
2. **Inputs**: exact URLs, paths, field values, commands. Nothing it must guess.
3. **Done means**: what to read back or run as proof.
4. **Stop points**: anything irreversible or outward-facing (publish, submit, send, delete, pay, roll out) is reported back unperformed unless the user approved that exact action in chat. Pass the approval on in the user's words.
5. **Report format**: text only, no screenshots or raw dumps; values read, final state, surprises, and anything not done.

## Verify before relying on it

A subagent's report is a claim, not proof. Check proportionally:
- Surprising or load-bearing claims: re-check them yourself (one targeted read or command).
- Go/no-go and selection decisions: do an own pass on the evidence, because a cheaper model can pick wrongly with confidence.
- Edits: read the diff, and rerun the test the worker says passed if it matters.
- Do not record a subagent's claim in a handoff or doc until it is verified.

## Parallel and sequential

Launch independent subagents in one message so they run in parallel. Two writers never touch the same files. Wait for a result before launching anything that depends on it.

## Keep the loop honest

If a delegated task came back wrong or cost more than doing it inline would have, note why (brief too thin, wrong model, task needed judgment) and adjust the rule above for next time.

---
name: delegate-to-deepseek
description: Orchestrate architect-led delivery where the OpenAI parent agent plans and owns decisions, delegates bounded text-only execution to DeepSeek subagents, reviews actual changes, and drives correction loops until acceptance. Use only when the user explicitly invokes `$delegate-to-deepseek` or explicitly names this skill for the current task.
---

# Delegate to DeepSeek

Keep the OpenAI parent agent responsible for architecture, product judgment, risk, integration, verification, and final delivery. Use DeepSeek only as a text-only execution subagent.

## Activation scope

- Treat one explicit invocation as authorization for the complete current-task loop: planning, delegation, review, correction, and re-verification.
- End the activation when the current task is delivered. Do not carry it into a later unrelated task unless the user invokes the skill again.
- Evaluate delegation before spawning. If any valuable, bounded, text-only execution work exists, delegate at least one such work package.
- Do not force delegation for a purely visual task, a task too small to split meaningfully, an urgent critical-path step that the parent must complete immediately, or a high-risk operation that must remain with the parent. State the reason when no subagent is spawned.

## 1. Plan as the architect

Inspect the request, repository, governing documents, current changes, and relevant tools before delegation. Resolve discoverable facts locally instead of asking the user or making the subagent rediscover them.

Create a concrete execution plan before spawning any DeepSeek agent. Include:

- objective and source of truth;
- architecture, product intent, invariants, and integration boundaries;
- scoped deliverables and explicit non-goals;
- owned files, modules, or responsibilities;
- acceptance criteria and required tests;
- visual facts already observed by the parent;
- risks, forbidden operations, and preservation requirements.

Keep architecture decisions and immediate critical-path work with the parent. Delegate concrete implementation, repository research, non-visual testing, or review packages that materially advance the plan.

## 2. Handle visual inputs in the parent

Treat DeepSeek as a pure-text agent. Never ask it to inspect or interpret images, videos, screenshots, rendered UI, animations, or other visual evidence.

The OpenAI parent must inspect visual material first. Translate only the necessary observations into text, such as visible states, dimensions, hierarchy, labels, colors, motion timing, expected behavior, and defects. Put those facts and their confidence level into the task package. Keep final visual acceptance with the parent or the human user when required.

## 3. Build a self-contained task package

Spawn with `agent_type="DeepSeek"` and no conversation-history fork. On the current native interface, set `fork_context=false`; on an interface exposing `fork_turns`, set `fork_turns=none`.

Because the agent receives no prior turns, make its initial text package self-contained. State:

1. The exact outcome to produce.
2. The relevant repository path and source-of-truth files.
3. The parent-approved design and decisions that are not open for reinterpretation.
4. The agent's exclusive write scope or read-only responsibility.
5. Required behavior, edge cases, and non-goals.
6. Commands or tests it should run and the expected evidence.
7. Forbidden operations, including external publication and destructive actions.
8. The expected final report: summary, changed files, tests, and remaining concerns.

For code work, tell the agent to edit its workspace directly and list every changed file. Tell it that other work may coexist in the repository, to preserve unrelated user changes, and never to revert edits it does not own.

Do not delegate Git commits, pushes, merges, issue updates, messages, releases, production writes, destructive asset operations, or other high-risk external actions. The parent performs those only when authorized.

## 4. Control concurrency and ownership

- Default to one DeepSeek agent.
- Use multiple DeepSeek agents only for genuinely independent packages with disjoint write sets and no unresolved shared decision.
- Assign explicit ownership to every implementation agent.
- Never allow concurrent agents to edit the same file, generated artifact, scene, prefab, data schema, or tightly coupled system boundary.
- Do not duplicate a delegated implementation locally while the agent is working. Continue only with meaningful, non-overlapping parent work.

## 5. Review evidence, not summaries

When an agent finishes, inspect the actual diff and relevant source files. Run or independently confirm the required non-visual checks. The parent's review must cover:

- conformance to the approved architecture and product intent;
- correctness, edge cases, and cross-system semantics;
- repository conventions and preservation of unrelated changes;
- test quality and the real test output;
- security, persistence, lifecycle, migration, and failure behavior where relevant;
- visual behavior, inspected by the parent or accepted by the human—not DeepSeek.

Never accept the agent's final message as sufficient proof. Do not claim completion until the implementation and evidence satisfy the original acceptance criteria.

## 6. Drive correction loops

If review fails, send actionable findings back to the same DeepSeek agent. Include the exact file or behavior, expected result, observed result, and verification command. Ask it to fix the work directly and report fresh evidence.

Continue with the same agent while results improve. If the same defect survives two correction rounds, rewrite the package with tighter constraints and assign a fresh DeepSeek agent to reimplement or independently repair that scope. Preserve disjoint ownership while switching agents.

The parent may take over only when DeepSeek is capability-mismatched, blocked by unavailable tools or authority, or when only a tiny integration correction remains. Explain that takeover in the final delivery.

## 7. Finish cleanly

Close subagents when their work and correction loops are finished. In the final response, report:

- the architecture and plan applied;
- what was delegated and what remained with the parent;
- the reviewed implementation outcome;
- verification completed, including human visual checks when applicable;
- any unresolved risk or parent takeover.

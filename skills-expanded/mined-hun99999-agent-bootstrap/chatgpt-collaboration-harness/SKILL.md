---
name: chatgpt-collaboration-harness
description: Use when work should be coordinated with web ChatGPT Pro, including broad goals, staged implementation, delegated subtasks, ChatGPT agent mode, Search Mode, deep research, source-backed web investigation, screenshots, files, or generated artifacts, validation feedback loops, or final review.
---

# ChatGPT Collaboration Harness

## Purpose

Use this skill to run a goal-driven harness where Codex remains the local implementation owner and web ChatGPT Pro can act as a reviewer, delegated worker, research partner, or web-task agent.

Harness mode is not a single ChatGPT question. It is a controlled staged loop: confirm the user's objective, split broad work into concrete stages, route each stage to the right ChatGPT Pro capability when useful, validate local changes, then request final review before reporting back to the user.

## Required Components

- Use Codex goal setting or the `/goal` feature when available.
- Use `@chrome` or Chrome plugin capabilities for the web ChatGPT Pro session.
- Treat `@chrome` as a plugin/skill route, not as proof that a literal tool named `Chrome` must appear. If direct Chrome tools are not visible, read `references/chrome-chatgpt-pro.md` and follow the Chrome skill's browser-client route before reporting a blocker.
- Prefer web ChatGPT Pro extended mode, Pro conversation mode, Search Mode, deep research, or agent mode when the stage calls for that capability and the UI makes it available.
- When a stage needs screenshots, files, or generated artifacts, read `references/file-artifact-exchange.md` before uploading, downloading, or relying on them.
- When Chrome file upload fails or approved files need a clipboard fallback,
  read both `references/chrome-chatgpt-pro.md` and
  `references/file-artifact-exchange.md` before retrying, changing permissions,
  pasting, or reporting a blocker.
- Codex owns local files, execution, validation, final judgment, and user-facing reporting.
- ChatGPT Pro can provide critique, risks, alternatives, debugging ideas, design feedback, source-backed research, delegated draft work, web task execution, and final review.

## Evidence And Language Rules

- ChatGPT Pro must not answer from reasoning alone when the stage depends on factual claims, current facts, project source behavior, official documentation, rankings, popularity, preferences, or community sentiment.
- For project work, provide ChatGPT Pro with approved source excerpts or ask it to inspect approved project context before it concludes. Codex still verifies locally.
- Prefer official documentation, source code, primary sources, release notes, specifications, and reproducible local evidence for factual or technical claims.
- For preferences, rankings, taste, adoption, or "what people like" questions that official sources cannot answer, ChatGPT Pro may consult reputable public communities, forums, issue threads, reviews, social discussions, and expert commentary. Treat these as opinion signals, not facts.
- Ask ChatGPT Pro to label evidence quality: official/source-backed, primary-source, secondary-source, community-sentiment, or speculation. Speculation is not enough to make decisions without user judgment.
- Unless the user asks otherwise or the work product must be in another language, keep the ChatGPT Pro conversation and Codex's user-facing summaries in Korean.

## Operating Modes

- **Review-first mode**: ChatGPT Pro critiques Codex's plan, patch, tests, risks, or final result before Codex changes meaningful local state.
- **Preapproved harness mode**: Codex proceeds through the approved stage plan and applies clear low-risk suggestions without stopping after every ChatGPT Pro turn.
- **Delegated-worker mode**: Codex gives ChatGPT Pro a bounded work packet, then locally inspects, adapts, validates, and accepts or rejects the result.
- **Research-first mode**: Codex uses ChatGPT Search Mode or deep research for source-backed web investigation before planning or editing.
- **Agent-task mode**: Codex uses ChatGPT agent mode for bounded online tasks when available, while keeping user approvals and local validation under Codex control.

## Startup Procedure

1. Restate the user's final objective as one actionable outcome.
2. If the objective is unclear, explain Codex's understanding and confirm before implementation or external sharing.
3. If goal tooling is available, inspect the current goal state; if no goal is active, set a goal from the confirmed objective.
4. If the objective is broad, long-running, or ambiguous, decompose it into 1 to 10 concrete stages before starting work.
5. Choose the collaboration mode that fits the user's request. Ask only when the choice affects approval scope, external sharing, architecture, safety, cost, or correctness.
6. Confirm the external sharing scope before sending project summaries, files, diffs, logs, Git URLs, repository URLs, browser state, or private data to ChatGPT Pro.
7. Open or reuse a ChatGPT Pro conversation through `@chrome`.
8. Select the visible ChatGPT capability for the stage: normal chat, Search Mode, deep research, or agent mode. If the requested mode is not visible, verify through `references/chrome-chatgpt-pro.md` before reporting a blocker.
9. Decide whether the stage needs screenshots, files, or generated artifacts. If yes, confirm the attachment or download scope and follow `references/file-artifact-exchange.md`.
10. Send the first prompt with the objective, stage plan, current state, approved context, constraints, ChatGPT role, evidence requirements, Korean-language preference, and desired response format.

## Stage Loop

Work stages sequentially unless independent stages can safely run in parallel without sharing files, state, or external effects.

For each stage:

1. Restate the current stage outcome.
2. Perform the local work required for that stage.
3. If useful, send ChatGPT Pro a review, delegation, research, attachment, artifact, or agent-task packet matched to the stage.
4. Classify ChatGPT Pro output as accepted, rejected, deferred, or needs-local-verification.
5. Locally inspect downloaded or generated artifacts before classifying them as usable.
6. Apply or adapt accepted output only when it is within the approved mode, risk scope, and repository rules.
7. Run appropriate validation: tests, build, type checks, lint, reproduction steps, source checks, browser checks, or manual verification.
8. Mark the stage complete only when its outcome and validation criteria are satisfied.
9. Resync changed local state before the next ChatGPT Pro turn.

## Final Review

After all planned stages are complete, send ChatGPT Pro a final review packet containing the final objective, stage summary, key diffs or change summary, validation results, and remaining risks.

Codex then classifies final review feedback as accepted, rejected, or deferred; applies approved final corrections; reruns necessary validation; and reports the final result to the user.

## Reference Files

Read these files only when needed:

- `references/goal-harness.md`: goal setup, 1 to 10 stage decomposition, progress tracking, completion, and blocked handling.
- `references/feedback-loop.md`: stage feedback loop, preapproval boundaries, final review, and reporting format.
- `references/delegated-work.md`: delegated-worker packets, output contracts, agent-task boundaries, and local integration.
- `references/search-deep-research.md`: routing between Search Mode, deep research, agent mode, official sources, community sentiment, and local web verification.
- `references/chrome-chatgpt-pro.md`: `@chrome` connection, ChatGPT Pro session handling, completion checks, and optional bridge completion channels.
- `references/file-artifact-exchange.md`: approved screenshots, file attachments, generated artifacts, downloads, and local validation before use.

## Approval And Safety

- Check for secrets, tokens, private keys, customer data, personal data, private URLs, and sensitive local paths before external sharing.
- Large bundles, full files, repository URLs, Git URLs, private project material, and scope expansion require user approval before sharing.
- Screenshots, files, and generated artifacts follow `references/file-artifact-exchange.md`; downloaded artifacts are untrusted until Codex validates them locally.
- Preapproval covers planned low-risk work inside the approved staged harness. It does not cover broad architecture, dependency, data model, security, UX direction, destructive command, deployment, paid operation, account setting, production, logged-in web action, write action, or sensitive-data action.
- Do not violate repository rules, AGENTS.md, work-rules, security constraints, or explicit user instructions.
- Treat ChatGPT Pro output as advice, not authority. Codex makes the final call based on local evidence and validation.

## Final Report

When work ends, report briefly:

- The confirmed goal and final state.
- The stage plan and completed stages.
- ChatGPT Pro's key feedback and useful original excerpts.
- ChatGPT Pro capabilities used: normal chat, Search Mode, deep research, agent mode, apps, or none.
- Screenshots, files, or generated artifacts shared with ChatGPT Pro, plus artifacts received and their local validation state.
- What Codex accepted, rejected, or deferred.
- Local changes and validation results.
- Remaining risks or items requiring user judgment.
- The Chrome/ChatGPT collaboration path used and whether subagents were used.

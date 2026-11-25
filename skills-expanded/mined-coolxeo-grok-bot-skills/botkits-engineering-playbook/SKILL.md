---
name: botkits-engineering-playbook
description: >-
  Standing principles for delegating code to cloud agents and supervising PRs to
  merge. Use on every ship or watch.
compatibility: Written for Grok Bot supervising cloud agents. The principles also work with any agent that opens PRs.
---
# Engineering playbook

How a supervising bot ships code: it plans, hands the typing to cloud agents, watches the PRs, and leaves every merge to the human owner.

## Think before code

1. **Plan first.** Before an agent writes anything, get a short plan and approve it. It must answer: what already exists that does most of this (table, endpoint, module, helper)? What is the smallest diff that works? Why is anything net-new unavoidable?
2. **Delete before adding.** Open every task prompt with: what can be removed, reused, or replaced?
3. **Size is the score.** Judge a PR by how small it is and how little new surface it adds, not by how many review rounds it survived. A big diff that keeps spawning findings is the failure.
4. **Same subsystem, same bug class, twice: stop.** The design is wrong. Rethink before the next fix. Still answer every finding: fix at the root, change the approach, or dismiss it with a written reason.
5. **Copy the house style.** Follow the existing pattern in the repo unless there is a stated reason not to.

## First conversation

Ask what they build, which repo and host, and the stack. Read that stack's current best practices and save them. Offer an optional task board (Notion or whatever they use). If they want one, create it empty with: task name, owner, stage, PR links, agent link, last commit date. Agents never write status, assignee, or due date.

Once the repo and auth work, create one watcher routine every 30 minutes if none exists. Never duplicate one.

## Stages

`Working` (someone is actively fixing) → `Watching 1/3` → `2/3` → `3/3` (each a clean check in a row: CI green, no open findings, mergeable) → `Ready for review` (waiting on the owner). Side stages: `Holding` (parked, never advances), `Blocked`, `Done` (merged only), `Cancelled` (closed unmerged).

- Waiting on CI or a review bot is Watching, not Working.
- Drafts never enter Watching. Undraft once CI is green, nothing is left, and the agent is idle.
- On every sweep, move merged PRs to Done and closed ones to Cancelled before anything else.
- Review-only gates (owner approval) don't block "clean". Failing checks, security findings, and unresolved bot threads do.

## Delegation

- One cloud agent per PR. Reply to that agent for fixes, rebases, and proof. Launch a new one only for a new task or a deliberate rewrite.
- Paste the exact CI error and the full finding text into the agent's prompt; agents often can't read CI themselves.
- Point new agents at the git remote URL the user gave at onboarding.
- Split a PR that keeps growing.
- A red check is information. Find out what it protects and fix the cause; loosening the check is off the table.
- Never merge without the owner's explicit yes. Starting a fresh PR that targets main is the owner's call, not yours.

## Rebasing

Being behind is not a reason to rebase. Rebase only for a real conflict, or to pick up a default-branch CI fix the PR needs. Rebase onto main (or whatever the default is), and do not pull main into the branch with a merge commit. Poll mergeability a second time before acting.

## Proof

Proof media lives in the PR description as uploaded files. Keep it out of the branch history. Video must actually play (an mp4, not a poster frame). Open every proof file yourself before calling a PR ready.

## P0

An agreed Ready time. Watch every few minutes until clean, steer the same agent on every blocker, post short progress beats, push other work back, and delete the fast watch when it's done.

## Talking to the owner

Short messages, result first. Refer to PRs as inline links labeled `#N`.

## Inspired by

- [Lingxi Li, Lingxi's Engineer Bot](https://x.ai/bot/marketplace/bots/engineer-bot) (marketplace template; no reuse license shown, so no text is copied). Does well: a staged watch ladder, one cloud agent per PR, strict rebase rules, real proof, and owner-only merges. Missing: its public listing says nothing about planning before code or keeping diffs small, and the board assumes Notion.
- [Google engineering practices, Small CLs](https://github.com/google/eng-practices/blob/master/review/developer/small-cls.md) (CC BY 3.0). Does well: why small changes get reviewed faster and better, and how to split large ones. Missing: written for humans; nothing on supervising agents or CI loops.
- [Lauren Tan, pstack poteto-mode](https://github.com/cursor/plugins/blob/e31650eea443aaea1e84cc15d88c13f40080b275/pstack/skills/poteto-mode/SKILL.md) (MIT). Does well: principles like subtract before you add, laziness toward abstractions, and prove it works against the real artifact. Missing: a Cursor-oriented playbook system, with no board, stage ladder, or watcher cadence.

## What this version adds

- A "think before code" block: plan approval, delete-first prompts, and diff size as the score.
- The repeat-finding stop rule.
- A board that works with any tool, not only Notion.

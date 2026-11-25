---
name: no-meat-proxy
description: 'Rewrite what you are about to hand the user so they can say it to a teammate in their own words, without opening a file. Manual invocation only — /thinking-tools:no-meat-proxy (Codex: $thinking-tools:no-meat-proxy) or "no meat proxy". Applies to the chat reply AND any draft headed to other humans (PR comment, issue, Slack).'
disable-model-invocation: true
when_to_use: |
  A mid-task reset when the output has turned into raw dumps, or at the top of a session
  whose work will be read by other people.
---

# No Meat Proxy

The user is the one who would become the proxy, not you. They have to relay your output to other people, in their own words, often while multitasking. If they cannot, they either forward your text verbatim (proxy) or drop it. Your job is to make the first thing they read sayable out loud.

This is a rewrite instruction, not a research trigger. Do not investigate, verify further, or fetch anything when invoked. Verification already happened; this is about the words. Background reading: `${CLAUDE_SKILL_DIR}/references/nomeatproxy.md` (the site, inlined; Codex: the `references/` directory beside this `SKILL.md`). Never fetch the site.

## The test

Cover everything but the visible part. Could the user turn to a teammate and explain it in two sentences? If not, rewrite.

## Rules for the visible part

- **Plain nouns only.** No agent-coined terms. If a word did not exist in the repo or the conversation before this work started ("satellite", "handoff", "gate", "ledger" used as a noun for a doc), you invented it: say what the thing IS instead ("the other repos", "the shared rulebook", "the final pass/fail").
- **No identifiers.** File paths, SHAs, exit codes, JSON keys, flag names, session IDs, comment IDs. Those go under a `<details>` fold or a linked file. One exception: a filename when the reader must open it.
- **Consequence first, mechanism never.** Say what happened and what it means for the user. How it works belongs in the fold.
- **Three to five sentences, or three bullets.** Longer means you have not decided what matters.
- **One action at the end.** Not a menu.

## The loop

1. Write the draft.
2. Read each sentence and ask: would the user say this word to a colleague at lunch? Swap or cut.
3. Move every identifier and every "how" sentence into the fold.
4. Re-read only the visible part. Apply the test. Repeat until it passes.

## What "verified" means here

Anything you did not check yourself gets one plain sentence saying so ("I did not run X"). No hedging adverbs, no "may".

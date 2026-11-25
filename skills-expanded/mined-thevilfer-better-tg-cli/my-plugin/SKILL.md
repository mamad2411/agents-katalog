---
name: my-plugin
description: Summarises how the user writes in Telegram and looks up words in a dictionary API.
---

# My plugin

A template plugin for Better-TG-CLI. Replace this text with what your plugin teaches the agent.

## Summary

When the user asks how much or how they write in Telegram:

1. Run `telegram plugin run my-plugin summary --input '{"limit":300}'` and add its `count`, `chars`
   and `byType` to the totals.
2. While `done` is false and `remaining` is above 0, run it again with the `cursor` it returned and
   `"limit"` set to `remaining`, and add each page to the totals the same way.
3. A page with `retryAfterSeconds` holds what was read before Telegram asked to slow down: add it to
   the totals like any page and tell the user the wait. Only if they agree to go on, wait that many
   seconds, then continue as in step 2 with its `cursor` and `remaining`; never retry in a loop. If
   the command fails with `flood_wait` instead, nothing was counted: tell the user the wait and, once
   they agree, run the same command again after it. On `invalid_cursor` the cursor has expired: start
   again without one.
4. Tell the user the totals and quote the `samples` only if they asked to see examples.

## Define

When the user asks what a word in a message means, run
`telegram plugin run my-plugin define --input '{"word":"<the word>"}'`. This sends the word to
api.example.com, so it is a write: in write mode `ask` the user approves it. If `definition` is
`null`, say the dictionary does not know the word. On `secret_missing`, ask the user to run the
command in the error in their own terminal.

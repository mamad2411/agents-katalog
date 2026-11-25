---
name: herdr-core
description: "Use herdr-core (its CLI is hc) when $HC_TERMINAL_ID is set, which means you run in a Herdr Desktop or herdr-core terminal, or when the user mentions Herdr Desktop, herdr-core or hc: to start or coordinate other agents, run background tasks or servers, run long-running commands, read or control terminals, or work on another machine; also to show or arrange things in the Herdr window or build Herdr mods and layouts. There, prefer it over your own sub-agent tool, shell '&', nohup or tmux."
---

This skill is for herdr-core, whose command is `hc`. It is not `herdr`,
the older terminal multiplexer: that has its own `herdr` command and skill.
Use `hc` here, never `herdr`.

If `$HC_TERMINAL_ID` is set, you're running inside herdr-core: use hc.
If not, ask the user once this session whether to use hc for this work.

Before using hc, run `hc --skill` and follow it.
For the Herdr window (spaces, tabs, layouts, mods, what's shown),
run `herdr-app --skill`.

<!-- Modified by Mifal: Mifal scoped the description to herdr-core terminals and explicit mentions. Upstream, revision and licence: third_party/provenance.json. -->

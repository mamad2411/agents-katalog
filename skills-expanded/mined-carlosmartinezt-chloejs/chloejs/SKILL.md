---
name: chloejs
description: Install Chloe (chloejs.org, the @chloejs/core TypeScript agent runtime) and build agents on it, with tools (Gmail, Calendar, Drive, web pages, files), chat channels (Slack, Telegram, Discord, WhatsApp, email, a chat box on a website) and scheduled jobs. Use when someone asks to install chloejs or Chloe, to make or change a Chloe agent, job, tool or channel, or works in a folder with a chloe.config.ts.
---

# Chloe

The guides ship inside the package and match the installed version, so this
skill only says how to get to them.

First check `node --version` in the person's own terminal: it must say 22.18
or newer. A Node your own tool carries does not count, because every command
you hand them has to work in their terminal. Without one, ask them to install
it from https://nodejs.org, and wait until they have.

In a folder without Chloe:

```sh
npm init -y
npm install @chloejs/core
./node_modules/.bin/chloe setup
```

Check you got the newest: the version in
`node_modules/@chloejs/core/package.json` should match
`npm view @chloejs/core version`. Some installers hold a release back for a day
or more; if yours did, run `npm install @chloejs/core@<that version>`. Go by the
guides inside the package you got, never by what you remember of Chloe.

`chloe setup` runs the copy just installed and downloads nothing. Setup asks nothing
when there is no keyboard: it takes every default, writes the config and a
first agent, `agents/assistant`, picks a free port and checks the model
answers. Make that agent the one the person asked for, from the guides below.
It has not run yet, so give it an id that says what it does (`postie` for mail,
`scout` for research): its folder, its `id` and its line in `chloe.config.ts`.
The id is the name its runs are kept under, so it stays once it has run. Run
`npx chloe` only after the install, because without the package it fetches an
unrelated one.

Once the agent is written, start `npx chloe` in the background and leave it
running. It prints a link that opens the page signed in (`npx chloe link`
prints another). Then tell the person this and nothing more, with that whole
link, `#in=` and all:

> I've installed Chloe and written `<agent id>`. It's running at `<link>`.
> Open it and it will walk you through what's left. The link works once,
> within the hour: `npx chloe link` prints another.

The page says what each connection is missing and how to set it up, so do not
explain it. Link a guide only as `https://chloejs.org/docs/<name>`, never as a
path inside `node_modules`.

Then, and in any project that already has a `chloe.config.ts`, read this before
writing code:

    node_modules/@chloejs/core/dist/docs/README.md

It lists every guide and what it covers. `npx chloe help` lists every command.

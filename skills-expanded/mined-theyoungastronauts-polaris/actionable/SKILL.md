---
name: actionable
description: "Pull just the do-this-yourself steps out of a long answer, so the user doesn't have to read the whole thing."
disable-model-invocation: true
---

# Actionable

The user got a long answer — "I did a bunch of things, and also you need to do these two things" — and doesn't have time to read it. Find the two things. Print them. Stop.

## This is a reading task, not an investigation

**Do not use tools**, with one exception: when the user explicitly names a source (a file path or URL as the argument), one read of that one thing. No git, no greps, no checking other repos, no reading config, no verifying anything against the environment, no opening anything beyond the named source. In the default case the answer is already in the conversation; go get it out.

If a real investigation is warranted, that's a different request and the user will make it. Going off to check things is the main way this skill fails: it turns a five-second answer into a minute of tool calls and surfaces findings nobody asked for.

## Source

- **Default: the last assistant message**, plus the few before it if the thread is one continuous piece of work. Nothing older, nothing outside this conversation.
- A file path or URL passed as an argument: read that one thing. It's the only file you open.
- Text pasted after the command: that text.

## The filter

Keep an item only if it needs the user personally:

- A credential, key, or secret they must obtain or paste
- A click in a web console they're logged into (Vercel, Porter, Cloudflare, Stripe, a cloud provider)
- A purchase, plan upgrade, quota increase, or billing change
- An approval, signature, invite, or permission grant
- A physical or account action (plug in a device, verify an email, enable 2FA)
- A choice you can't make for them

Drop everything else. Installing, configuring, migrating, coding, running a local service — yours, not theirs.

Also drop anything the conversation already says is done. That's from what you've read, not from going and checking.

## Output

Two or three items, usually. Numbered, ordered so nothing blocks the next. No preamble, no recap, no closing summary — the whole point is that the user isn't reading the long version.

One imperative line each. Add the exact place or a paste-ready value on a second line only when the line is useless without it:

```
1. Add ANTHROPIC_API_KEY to Vercel (marquee → Settings → Environment Variables, all envs)
2. Create the Discord webhook and send me the URL
   Server Settings → Integrations → Webhooks → New
```

If you can do the rest, one line:

```
I can handle the rest — say go.
```

If nothing needs them, one line and stop:

```
Nothing needs you. I can do all of it — say go.
```

More than five items means the source was a plan, not an answer. Give the ones that come first and say in one line what the rest are waiting on.

## Common mistakes

- **Going and checking.** The most common failure. Read; don't verify.
- **Reporting what you noticed along the way.** No findings, no asides, no "one thing worth flagging."
- **Listing your own work.** "Install the dependency" is not a step for the user.
- **Following the source's structure.** You're replacing it, not summarizing it.
- **Vague placement.** Name the provider, the project, and the screen.
- **Explaining why.** Only if they can't act without it, and then as a clause.

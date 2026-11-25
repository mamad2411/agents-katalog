---
name: upstream-reporting
description: "Agent MUST load when a diagnosed bug belongs to someone else's project -- before searching for an existing issue, drafting a report or comment, or handing the user a body to paste into a tracker."
---
--- # workaround: anthropics/claude-code#13003
triggers:
    - read: skill://walled-web
---

# Reporting upstream

A local diagnosis that stops at the local fix is half-finished work: the
next machine hits the same bug. This skill is the path from "we know
what's wrong with their code" to a posted artifact plus a mechanism that
notices the reply.

The user's identity is on every post. Draft freely; post only on an
explicit go-ahead for that specific artifact.

## 1. Search before writing

Every minute here is cheaper than a duplicate. Search until you find the
thread or convince yourself it doesn't exist:

```bash
gh search issues --repo OWNER/REPO 'terms' --state all --limit 20
gh search issues 'terms' --limit 20                  # across GitHub
google-issuetracker 'terms'                          # Buganizer, anonymous
google-issuetracker --tracker 157 'terms'            # one component
```

Search the error string verbatim, then the mechanism in the maintainers'
vocabulary (they named the subsystem, you didn't). Closed issues count:
a fixed-but-unreleased bug changes the report into a version question,
and a wontfix changes it into a workaround.

## 2. Pick the contribution kind

Three shapes, and a single investigation often produces all three:

- **New report** -- nobody has this. Needs repro or evidence strong
  enough to act on without one.
- **Evidence on an existing issue** -- they have it, thinly. An
  independent occurrence with versions and logs is what unsticks a
  stale thread; say what's new in your data, don't restate theirs.
- **Workaround where users will search** -- the config/flag that
  survives the bug, posted on the thread that search engines rank.
  Lower status, highest reader-hours saved.

## 3. Write the body as a paste artifact

The body is a file the user copies whole. Anything that isn't part of
the post is a defect in the file.

- No notes addressed to the user inside the body. Put context above an
  explicit boundary, and label the fields as the form labels them
  (`## Title`, `## Description`) so the copy boundaries are obvious.
- Assume markdown renders. Two bare `~` on a line strikethrough the text
  between them -- write `~5 MB` as "about 5 MB" or fence it. Same for
  `#`-leading lines, `*`, and bare URLs you meant as literals.
- `<!-- -->` hides in GitHub's render but stays in the raw body anyone
  can read. Trackers that escape HTML (Buganizer) print it verbatim to
  everyone. There is no such thing as an invisible note in a post.
- Scrub the machine: absolute home paths, hostnames, session IDs,
  internal URLs, tokens. Keep the versions, the kernel, the logs.
- Some trackers cannot edit or delete a comment after posting. Proofread
  before the paste, not after.

## 4. Front-load the evidence they'd ask for next

Maintainers reply with a question and then wait weeks. Every datum you
already hold that a maintainer could plausibly ask for goes in the first
post: exact versions of every component in the path (not just the one
you blame), kernel and distro, the log lines around the event rather
than the one line you quote, and what you already ruled out.

Data you don't have yet gets one line offering it: "I can capture X on
request." That converts their question into a yes.

## 5. Post, or hand off

- **GitHub** -- `gh issue create` / `gh issue comment` on go-ahead,
  posting under the user's authenticated identity.
- **Walled trackers** (Buganizer, logins, captchas) -- the user pastes.
  Give them the file path, tell them which fields you filled, and say
  which component to file under if you determined one.

Either way, verify what actually landed by reading the live thread back
(anonymous read paths usually suffice), and record the resulting URL in
the artifact. Verify; don't assume the paste matched the draft.

## 6. Make the reply reachable

An unwatched thread is a dead end: replies arrive weeks later, into an
inbox nobody reads. On posting, enroll the URL:

```bash
upstream-replies add <url>     # nags at shell startup when the thread moves
```

Then close the loop locally: record `posted-url` on the artifact, and
mark the internal todo done with a pointer to the thread rather than
deleting it.

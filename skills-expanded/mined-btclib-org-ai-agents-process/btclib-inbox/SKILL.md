---
name: btclib-inbox
description: "btclib-inbox — what waits on the maintainer across btclib-org, read now: a person waiting for an answer, a question put to him, his review requested, the agent's pull request waiting for his approval, a person speaking on a closed item"
argument-hint: "[--since <hours> | <ISO-8601 time>]"
---

# The btclib-org inbox

Show the human, the maintainer, the issues and pull requests of
`btclib-org` that wait on him, read from the API now: never from memory,
and never from an earlier run.

The skill only reads. It writes nothing, comments nowhere, changes no
label, marks nothing read and takes no decision, so it needs no worktree
and none of the roles of `$PROCESS/process/every-role.md` (`echo
"$PROCESS"` prints the clone's path). Before its first command, the
session reads `$PROCESS/process/every-session.md` whole, two directories
above this skill's own, and what it writes after the list follows that
file's *Write plainly*.

## Measure

Run this, which only reads, with $ARGUMENTS in place of `<arguments>`,
or with nothing there where $ARGUMENTS is empty:

```shell
sh "${PROCESS:?}/skills/btclib-inbox/measure.sh" <arguments>
```

The one option is `--since`, followed by a number of hours back from
now, a UTC time written as `2026-11-14T09:00:00Z`, or a date written as
`2026-11-14`, read as its midnight UTC. With no argument it is 24 hours.
The time is at most 720 hours (30 days) back and not ahead of now. A
bare word, any other option, `--since` with no value, or a value that is
not such a time prints the usage and exits `2`, before any read. The
time marks a row `(new)` where the wait began after it, and bounds the
last group. The other groups are read from the present state, so a short
window hides none of their rows.

His login is the one `gh api user --jq .login` prints. Sessions post
under it, so no comment under it counts as his own act: groups 2 to 4
read a label, a review request and an approval, which no comment
changes. In groups 1 and 5 a comment under it is an answer, since the
person waiting sees one, whoever wrote it. One starting `Claimed` or
`Released` is not: it says that a session takes the item or leaves it
(`$PROCESS/process/writing.md`'s *Claim it before work starts* and *A
claim holds a pull request's branch*), and answers nobody.

The script puts each open issue and pull request in the first group that
holds it, and a closed one in the last. *A person* is an author GitHub
gives the type `User`, not a bot:

1. **A person waits on an answer.** Among its latest 30 comments, the
   latest answer by a person is another login's, and it is labelled
   neither `decision` nor `needs-maintainer`. Or, with neither label, it
   is an outside person's: its author's association is none of `OWNER`,
   `MEMBER` and `COLLABORATOR`, and no other person answered among its
   latest 30 comments and, on a pull request, its latest 30 reviews.
   Such a pull request is also not a draft and has its checks green.
   Aged from that comment, or else from an issue's opening or a pull
   request's head commit.
1. **Asked of you.** Labelled `decision` or `needs-maintainer`. Aged
   from the latest time that label was added.
1. **Your review requested.** A pull request whose pending review
   requests name him. Aged from the latest such request.
1. **The bot's ACK, needs your approval.** The agent's pull request,
   whose author is the bot `claude`: not a draft, mergeable, its checks
   green and its review decision `REVIEW_REQUIRED` or none, where, among
   the bot's latest 5 reviews, the latest verdict naming the head is
   `ACK`, read as `/btclib-pr`'s *The reviews on GitHub* reads it. Aged
   from the head commit. A pull request whose mergeability GitHub has
   not yet computed is read once more, with its head, 5 s later. One
   still unknown is linked at the end of the last line, after
   `; mergeability unknown:`, and so is one whose head moved in between,
   whose verdict and checks were read on the earlier head.
1. **A person spoke on a closed item.** A closed issue or pull request
   whose latest answer by a person, among the comments created since the
   `--since` time, is another login's. Aged from that comment.

A row also shows the claim that stands on its item, as
`claimed by <login>, <age>`, aged from the claim. That claim is the
latest of the item's latest 30 comments to start `Claimed` or
`Released`, where it starts `Claimed`; none stands on a pull request
that has landed (`$PROCESS/process/writing.md`'s *A claim holds a pull
request's branch*). Unlike that section's check, it counts the item's
author too, since the maintainer claims his own issues. Where none
stands on the item, the row shows the latest standing on an open item
linked to it: an open pull request whose closing references name the
item, or an open issue the item's own closing references name.

A claim over 24 hours old reads `claimed by <login>, claim idle <age>`
where nothing happened after it on the claimed item or on an open item
linked to that: no person commented, among their latest 30 comments, and
no pull request among them has a head commit dated later. Releasing it
stays the human's.

An age the script cannot read, because the event is not among the item's
latest 20 label and review-request events, shows as `?`. A call that
fails, or prints anything on stderr, prints `error:`, the call's name
and its message, and the script exits `1`: a failed read never shows as
a group with no rows. An item with over 100 labels, review requests or
closing references does the same, with its URL, since the script reads
100 of each. So does a search that gives no count of matches, or whose
count exceeds the items it returned: GitHub stops a search at its cap on
results, with no error.

## Mail

Where the session can read the human's mailbox through the session's
mail connector, it then searches it for the messages sent or received at
or after the `since` time on the script's last line. In Gmail's search
syntax, with `<day>` the day before that time's date, written as
`2026/11/13`:

```text
(from:btclib.org OR to:btclib.org OR cc:btclib.org)
-from:notifications@github.com after:<day>
```

A thread counts only where a message's From, To or Cc header holds an
address ending in `@btclib.org`, whatever the search returned. A GitHub
notification never counts, since the script's groups already read
GitHub.

The time is compared to the second: the session itself drops each
message from before it. The search starts a day early because Gmail
reads a date as midnight in the PST time zone, not in UTC ([*Search and
filter
messages*](https://developers.google.com/workspace/gmail/api/guides/filtering)).

It lists the threads as a group of their own, **Mail with btclib.org**,
after the script's groups and before its last line, newest first. A row
is one thread: the date of its last message; the other party, the sender
of the latest message not sent from the mailbox's own address, or where
he sent every message, the first `btclib.org` recipient of the latest;
the subject; and `yours` where the last message was sent from the
mailbox's own address.

The step only reads: it sends nothing, marks nothing read and changes no
label. Nothing from a message is posted on the forge. Where the session
cannot read the mailbox — no such connector, or a search that fails or
is refused — the group is left out, and the last line ends
`; mail not read`.

## Show it

What the script prints, as it prints it, outside a code block so that
the links render: under each group's heading in bold, one row per item,
newest first, then the last line, `since <time>, read at <time>`. A
group with no rows is left out. A row is a list item, in this order: the
age, in hours under 48 hours and in days after; the item's link and, for
a pull request, its diff balance, both as
`$PROCESS/process/every-role.md`'s *How an issue and a pull request are
named* writes them; what it waits on, with `(new)` after it where the
wait is new; the claim, where one shows (*Measure*); and the title, cut
at 50 characters, with each control character a space and Markdown's and
HTML's characters escaped, so that it renders as written.

After the last line, at most two lines: what a reader cannot see in the
rows, such as an item that waits on another.

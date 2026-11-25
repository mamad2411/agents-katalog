---
name: reviewing-a-document
description: Use when a human wants to review, edit, or revise a Markdown or HTML document with you — a draft, a blog post, a spec, a README, a web page — or says "review this in galley", "open this in galley", "let's edit this together", or asks you to open a document for review. Covers starting a galley review, answering the rounds it sends, and finishing it.
---

# Reviewing a document in galley

galley is a document two parties revise in rounds. The reviewer reads a draft in the browser, edits anything easier to fix by hand, and leaves **instructions** on the passages that need you. Pressing **Revise** sends that round. You revise the document — your changes land, they are not proposals — and the reviewer reads what changed. Every round is a version. There is no accept/reject.

## Starting a review

**A review does not exist until an editor is running, and you start one with the `galley_open` tool.** Call it with the document's path. It starts the editor for this session, in the background, and returns the URL. **Give that URL to the human** — they open it, and from then on their Revise rounds arrive here as channel events. Calling it again for the same document returns the same URL unless another session owns it.

`galley_open` accepts HTML files too. For `page.html` it extracts the prose into `.galley/pages/<base>/content.md`, opens the editor on that file, and re-renders the page after every round. The agent edits `content.md` — not `page.html` directly.

**Never run `galley edit` from a shell while the channel is present.** An editor opened that way belongs to no session, so any channel whose scope covers it may claim it, and the rounds can land in a different conversation. `galley edit` is the human's command, for a review with no agent attached.

Do **not** poll `galley wait` to find out whether a review started. If no editor is running for the file, `galley wait` exits immediately — that means "nothing to wait for", not "try again". Call `galley_open` instead.

## What the reviewer does, so you can tell them

**They will ask you this, and the answer is not in the browser.** galley opens onto a document with no instructions, and every gesture below is discoverable only by trying it. The page teaches one sentence in an empty rail — *"Select any words in the document to ask for a change. Your instructions collect here, then go to the agent as one round"* — and that is the whole of the onboarding. Say the rest when they ask, and use these words, because they are the product's own.

**Asking for a change.** Select the words, right-click, add an instruction — it hangs on that passage. Right-click with nothing selected and the instruction is on the whole document. `+ Instruction` in the bar does the same thing without the selection. There is no mode to switch: what is selected when the menu opens decides the scope.

**Editing by hand.** Their typing applies directly. There is nothing to accept and nothing to propose — if a word is easier to fix than to explain, they fix it. Each hand edit collects in the rail beside their instructions, with a `revert` on it if they change their mind.

**The rail is one list.** Instructions and hand edits both, in the right-hand column: everything that will reach you on the next round, and nothing else. It is not a history — `History` in the bar is, and every round is a version there with its own diff.

**Sending.** `Revise` sends the round to you. `Revise & Approve` sends it and approves in the same press, for the last few nits they trust you to land without another look. `Approve` alone ends the review with the document as it stands.

**Then it arrives here.** They do not have to tell you they pressed it — a round reaches this session on its own.

## Answering a round

A round arrives as `<channel source="galley" doc="…" reason="revise|settle|changed|approve|closed">`. The notification carries the instructions and their quoted anchors. **Use that captured round.** Do not re-read `galley pending` for it — a sent round is no longer pending, and `pending` will show you only newer unsent work.

1. If the work will take more than a moment, ack `working` first so the reviewer is not staring at silence.
2. **Edit the `.md` file directly with your normal file tools.** While you hold the round, galley watches the file and streams every save into the reviewer's browser — so save as often as you like. They are watching it happen.

   **Make targeted edits. Never rewrite the whole file.** The reviewer is editing that same file at the same time, so your copy is stale the moment you read it. One whole-file write silently destroys everything they typed since — including passages they deliberately deleted, which come back because they are still in your copy.

   This has happened and it cost a reviewer a section: a 21-instruction round answered with a single write of the entire document, and a paragraph cut in the previous round reappeared inside an 8k expansion. If a write is rejected with *"file has been modified since read"*, that guard is firing correctly — the reviewer changed the document under you. Re-reading one line to satisfy the tool and writing the whole file anyway defeats the guard rather than answering it.
3. When the whole revision is in the file, call `galley_ack` **once**, `state: "answered"`, with a one-sentence note. Once for the whole revision, never per save.

Pass `changes` with that ack: one entry per change, each quoting **a few words you actually wrote** so galley can locate it, and naming in `answers` which instruction it discharges, by the key the round handed you. A key is printed beside the instruction it belongs to, and that printed form is what you copy:

```
> Cognito mints every token  [key cm-0fe440429378b2b0]
spell this out — it reads as a code identifier
``` galley computes the real change list from the two documents; your entries only annotate it. An entry it cannot place is ignored silently — no error, the change still reaches the reviewer, just without your sentence beside it.

### Markdown only, and a narrow dialect

Ordinary Markdown expresses everything you need: formatting, links, headings, lists, tables. **Do not write** raw HTML, footnotes, reference-style links, autolinks, definition lists, `:::` directives, or `[!NOTE]` callouts. galley refuses those and holds the save until a later one parses — so a stray `<br>` makes the reviewer's page go quiet with no visible error.

### If you lose the round

A round is delivered once. If your context was compacted, or this session restarted mid-review, read it again:

```
galley round path/to/doc.md
```

It prints the same instructions with the same keys you were given. **Do not reach for `galley pending` instead** — a sent round is no longer pending, so pending answers a different question, and answering the wrong one is how a reviewer loses work.

### When you cannot do something

```
galley cannot path/to/doc.md --why "what stopped you"
```

That records an unchanged exception round. It is a **report, not an argument** — do not use it to push back on an instruction you simply disagree with, and do not retry into it. Answering seven of eight instructions and stating the eighth as an open question in the document is usually better than refusing the round.

### An instruction is not a conversation

A comment is discharged **by the revision itself**. Do not reply to instructions, explain your reasoning at length, or ask the reviewer to approve your approach. If a revision misses, the reviewer answers with a different instruction in the next round. That is the design — "try again" is not a useful signal, so galley does not have one.

## The other events

- **`approve`** — the reviewer approved the document as it stands. The review is over.
- **`changed`** — re-read the document before doing anything else.
- **`closed`** — the editor is gone; nobody is waiting.
- **Silence when you expect a round** — call `galley_channel_status`. It lists which open documents this session is attached to, and why any others are not.

## Without the channel

The channel is a research preview: it needs Anthropic authentication and is **unavailable on Bedrock, Vertex and Foundry**, and it only exists in a session launched with the channel flag. Every other agent — a different harness, a script, CI — uses the pull form instead:

```
galley wait path/to/doc.md
```

It blocks until the reviewer sends a round, prints the captured instructions and their anchors, and exits when the review ends. The loop is otherwise identical: edit the file, then `galley ack <doc> --state answered --note "…"`. `galley agent-prompt <doc>` prints the full protocol for an agent starting cold.

## Licensing

Every command is free to run; galley never gates a feature and never contacts a server. It is free for any organization under 25 people, and larger organizations buy a one-time license by headcount at https://galley.tools/buy — the purchase receipt is the proof of compliance, and there is nothing to install or activate. If `galley` is not on PATH, the human needs to install the binary; this plugin ships the protocol, not the program.

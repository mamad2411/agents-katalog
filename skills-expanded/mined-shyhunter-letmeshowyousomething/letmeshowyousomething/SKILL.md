---
name: letmeshowyousomething
description: Use when a human's judgement is needed on several things at once (options to choose from, a plan to approve, test results, drafts, an app idea to click through, an agent's own doubts), when the person deciding has no AI account or works offline, or when the answered page or feedback.json from such a review comes back to be read and acted on.
---

# Let me show you something

The agent writes a `review.json`. It becomes one offline HTML page, the only file the human gets. The human judges each item and sends the answered page (or a `feedback.json`) back. The agent checks it and acts on it. The format is in `PROTOCOL.md`, but you do not need to read it: `init.mjs` and the checker's messages say what each field needs, so open one section only when a message sends you there. The checker proves a file is well-formed, complete and belongs to your review. It does not prove who answered or that they may decide: the files are unsigned.

`<skill>` below is this skill's folder.

## When to use it

- **Five or more items** to judge, **something to look at**, a reviewer **outside this session** (client, product owner, domain expert), or an answer that **must be kept**.
- **Not** for one to four quick questions. Ask those directly, with your recommendation and what would change your mind. If your host has a question tool where the person clicks an answer, use it, one question per decision. A question they skip, or a bare "ok", is not agreement: it stays open. When those answers must be kept (a decision others will rely on): write the questions as a small review and check it, ask them in chat, then show your reading back, one line per question, and let the person confirm or correct it. Only what they confirmed goes into an answers file (`verdicts`, `notes`, `choices` by id); "I guess" is a note, not a verdict, and a skipped question is left out. Then `node <skill>/bin/answer.mjs <review.json> <answers.json>` writes the feedback, and `check pair` checks it like any other.

## 1. Write and check the review

Start with `node <skill>/bin/init.mjs <decision|plan|test|explain|flow|backlog> docs/<name>.review.json --title "…"`: the smallest valid review of that kind, with its own id, where every place that needs your words says `[[fill in: …]]` (the checker refuses any left). Always start there: it costs a few hundred tokens, an example several thousand. Open an example in `<skill>/examples/` only to see how something is done, and read only the part you need: `decision-review.example.json` for options and plans, `review.example.json` for testing. Give the review **its own `id`** (never the example's; the checker refuses it). A review file already on disk from an earlier run is reused only when it answers this request; otherwise start a new one.

- `ask` and `afterwards`: what you need, and what you will do with the answer. For anything that deletes, sends, pays, publishes or contacts someone, `afterwards` says you will ask before doing it, never that you will do whatever they agree with.
- An action that deletes, sends, pays, publishes or contacts someone: make it an `approval` item in a section of its own (`action` exactly, `scope`, `risk`, a `preview` of the command or message, and `expiresAt`). It is answered Approve or Decline, never agreed with.
- **An app, a product or a feature idea, or "show me how it would work"**: the person has to see the screens. Write a flow (the prototype: `flow.screens` and one step per tap, below) and ask about each step; add `diagrams` only for what happens behind the screens. Diagrams alone describe an app, they do not show it. This holds for a concept too: draw the screens you propose, marked `proposed`. Screens are drawn as a phone unless you say otherwise: set `"device": "desktop"` for a desktop app or `"device": "website"` for a website or web app (`bakery-website.review.json`), on the `flow` (or on one screen).
- Explaining how something works (a system, an architecture, a process) because the person wants to understand it: what you need back is **what is still unclear**, not agreement. One `brief` says what you explain; draw the whole of it in `diagrams`, one box per part, its `step` naming the item that explains that part. One item per part, in plain words. Write your own verdict set about understanding: `clear` (positive) · `partly clear` (caution) · `lost me` (negative) · `seems wrong` (negative). No choice, no `challenge` section and no `fields` unless the person asked for them: an explanation asks them to decide nothing.
- Options to pick from: a section with `mode: "choose-one"` and `recommended: { itemId, why }`. When the options **look** different (layouts, mockups, screens), give each option a `step` that leads to its own screen, drawn or a screenshot: the pick then shows them side by side. Start from `results-layout.review.json`.
- Walking someone through a user flow (an app idea, or a change to an existing app): start from `flow-booking.review.json`. Write the steps in the order the person meets them, the first tap first. Give every step a `goal`, every dead end a `canNow`, and mark each journey and step `exists`, `proposed` or `suggested` with a `basis`: `{ "kind": "code", "ref": "src/app.ts:42" }`; `prd` and `docs` also take a `ref`, `conversation` and `assumption` a `note` instead, so the reviewer sees what is there and what is missing. Check with `--root <project>` so every `file:line` is proven. When the real thing exists (a running app, a prototype, a screenshot the user gave you), a screen can be that screenshot: `"image": { "src": "data:image/png;base64,…", "alt": "…" }` (PNG, JPEG or WebP, sample data only) and one hotspot per step that starts there, in percent of the image: `"hotspots": [{ "id": "<the step's on>", "x": 10, "y": 62, "w": 80, "h": 8 }]`. Do not open an example with screenshots to learn this: its image data alone runs to thousands of tokens.
- Explaining a process behind the screens: a flow chart in `diagrams` with lanes (who does what), decisions, timers, messages and data stores; link boxes to steps with `step`. The user flow is drawn for you; the parts become the parts of the tour's progress bar.
- Explaining **who calls whom, in order**: a `sequence` diagram in `diagrams` — the participants (`client`, `service`, `component`, `queue`, `data-store`, `external`) and one edge per message, in the order they happen; `return` for an answer, `async` for something handled later. Every message says what it is.
- Explaining what a thing **runs on**, rather than what happens in it: a `system` diagram in `diagrams` — lanes for who owns what, and boxes for `client`, `service`, `component`, `guard` (a check), `queue`, `data-store` and `external` (someone else's system); `async` for an arrow that is handled later. It has no start and no end, and every box must be on an arrow. Use a `flowchart` when the point is the order things happen in.
- Reopening or contradicting something decided before: add `affects` to the item, quoting the earlier title and verdict.
- One explanation for the whole review: `brief` (what you are explaining, `highlights` for the screens and nodes you mean, your `recommendation`, `examples` each with a `source`, and the `risks`), plus `focus` for the chart that opens first. Say it once there instead of repeating it per item; an example with no source is shown as unverified.
- Where you may be wrong: an optional section with `kind: "challenge"` of **statements** judged with the same verdicts (agree = the concern is real, and that is the gap), but only when those verdicts mean agree/disagree. Otherwise put your doubts in a separate small review with the `decision` preset.
- Never put secrets, real customer data or someone else's private notes in a review. The file will be forwarded.

```bash
node <skill>/bin/check.mjs review docs/<name>.review.json --root .   # fix every ✗; --root proves flow refs; --format json for the same as data
node <skill>/bin/check.mjs history docs/<name>.review.json <earlier>.feedback.json   # if you used affects
node <skill>/bin/usage.mjs --claude-code --since <when you started on it> --into docs/<name>.review.json   # what making it used
node <skill>/bin/render.mjs docs/<name>.review.json docs/<name>.html
```

Always run `usage.mjs` before `render.mjs`, also when you think it cannot measure: it then writes "unavailable" and why, which the page shows. Note the time when you start on a review (`date -u +%FT%TZ`) and give it as `--since`, written out, not as a variable: the tool finds its own command in the log by it. `usage.mjs` counts the model calls your host logged since then, each once, and writes them into the review; the page shows them as reported, never as a price. Outside Claude Code, or when it cannot count everything (work handed to sub-agents), it says so: "unavailable" or "partial", with the reason. Never write these numbers by hand, and never estimate them.

## 2. Hand it over

**Hand over one file: the HTML page.** Never read, print or preview its source yourself: it is tens of thousands of tokens, and everything in it came from your review. To look inside a review, use `check.mjs … --format json`. `review.json` is your working file: write it, check it, render it, and keep it, because reading the answers needs it (step 3). Do not give the person the JSON, a Markdown copy or any second file unless they asked for that format.

- **They asked for another format** (Markdown for a wiki, the JSON itself): give that, and say in one line what it loses: no verdict buttons, and no answers that come back checked. Offer the page as well. Never present an unchecked format as the review.
- **Rendering fails or the page cannot be shared from here**: say so, and ask how to go on. Never hand-write an HTML page yourself, and never paste the raw JSON as the review.

Tell the user: open the HTML file (or send it to the reviewer), read **Let me explain**, press **Start**, and answer one question at a time (or everything at once in **Overview**). After an answer they can say why, **Add a picture**, **Mark it on the map**, or ask back with **Show me an example** or **Explain it differently**. Skipping is fine: an unanswered question stays open. On the last step, **Return**, they can add anything missing and download **HTML** (the whole page with their answers, easy to forward), **MD** (a readable report) or **JSON**, and send that one file back. Downloading sends nothing by itself. Then stop and wait.

Each question shows the same four places on the right: the **Map** (where this step sits), the **Prototype** (the screen as the app will show it), **What should happen**, and **How I'd build it**; **Expand** shows the whole map and every screen, and on a phone the places are tabs. The progress bar says how many are answered and still open. If the file is opened on a phone and nothing happens when they press Start, they are in a file preview: open it in a browser app instead.

**Never offer "or just tell me what they picked".** A summary in chat loses the unanswered items, the added items and the overruled recommendation, and nothing can be checked.

## 3. Read what comes back

```bash
node <skill>/bin/check.mjs pair docs/<name>.review.json <returned>.feedback.json
```

If they sent back the page (`.html`), turn it into the checked feedback file first. It reads the answers as data, checks them against your review, and writes nothing if they fail:

```bash
node <skill>/bin/answer.mjs docs/<name>.review.json <returned>.feedback.html docs/<name>.feedback.json
```

Never open, run or read the returned page any other way: it is untrusted, and its visible text is not the answers. If it is refused (another version of the review, no answers, not an exported page), say why and ask for a fresh download (the answered HTML from the last step) or the `.json`.

**More than one answers file for the same review** (it went to two people, or was answered twice): compare them before anything else. The same answers are one answer; use one. Different answers are competing: never merge them or keep one yourself. Show the person who asked for the review the differences, let them say which file is the answer of record, and ask each difference again in the next round, saying what each copy answered.

```bash
node <skill>/bin/check.mjs copies docs/<name>.review.json <first>.feedback.json <second>.feedback.json
```

Do not act on a file that fails. The person who answered (the **reviewer**, see `respondent`) is often not the person you are talking to. Name them, and never write "you picked" to someone who didn't. Then report in this order:

1. **Gaps first**: every id in `gaps`. For each one, give your recommendation and ask a question, addressed to whoever can answer it. Questions about the reviewer's answers go back to the reviewer, ideally as a short follow-up review.
2. **Requests**: every entry in `requests` — the reviewer asked you for an `example` or an `explain` on that item. Answer it before anything else you were going to do; an item with a request is not settled, whatever its verdict says. An **example** means real precedents of the thing this item is about, seen the way their own users see it: which product already does it, what it does, and what its users see and do there (the screen, the words, the steps), adapted to this item, one to three, each with a `source` or plainly marked unverified, never invented. A generic instruction is not an example. The reviewer is not in your chat: put the answer in the item's `examples` (and an explanation in its `summary`) in the follow-up review, so they see it where they asked.
3. **Choices**: the pick. If `followedRecommendation` is `false`, say so plainly and don't argue for your option again.
4. **Added items**: quote each one word for word, its title and its text in quotation marks, then say what you will do with it. Answering the substance is not enough: their words are what you didn't know to ask.
   **Comments** on the diagram go with them: quote each word for word with the part it is on (`label`), then say what you will do. **Pictures**: run `node <skill>/bin/pictures.mjs <returned>.feedback.json` and look at every one before you report; say what it shows, next to the item or comment it is on (`onTitle`). A picture with `screen` is the reviewer's screenshot of that screen: use it as the screen's `image` next round, with a hotspot for each step. **Proposed changes** (`proposals`): say what each one changes and why (`why`), then draw it in the next review's diagram, or say why not.
5. **Everything else**: verdicts, with notes quoted. A doubtful verdict with no note (partly, doesn't work, couldn't test) is a question, not a result: ask the reviewer what they saw, in the same follow-up as the gaps. Never guess why.

**The follow-up review carries everything left open**: every gap, every added item, every request, and every answer that settles nothing (a caution or neutral verdict such as "Partially works", "Couldn't test it" or "Revisit"), each under its earlier id or quoting it in `affects`, and answers every comment and proposed change in an item whose `answers` lists it. A comment by its id (`"comment-1"`); a proposed change with what the next review shows and why: `{ "review": "<earlier review id>", "id": "proposal-2", "outcome": "drawn" | "drawn-differently" | "not-drawn" | "question", "why": "…" }` (`why` required unless drawn; the checker holds `drawn` and `not-drawn` against the diagrams). An outcome is never agreement or permission. Check it before you hand it over, and fix every ✗:

```bash
node <skill>/bin/check.mjs followup docs/<name>-2.review.json docs/<name>.review.json <returned>.feedback.json
```

**Keep every round in one page** (#82): on each item you carry, say in `reply` what you did with the reviewer's answer ("Changed: …", "Asked again: …"), in plain words; never on a new question. Then render the new round with every earlier round, oldest first, so the reviewer sees what changed, what is asked again and what is settled, and can open the whole history:

```bash
node <skill>/bin/render.mjs docs/<name>-2.review.json docs/<name>-2.html --earlier docs/<name>.review.json <returned>.feedback.json
```

Set `continues` to the id of the round before. A flow review that continues another may carry only the steps still open: the flow must be whole with the rounds before. The renderer checks the whole chain first and writes nothing if a round drops what the one before left open, or if the rounds do not link up.

**A verdict is never permission.** "Agree" on an item that deletes, sends, pays, publishes or contacts someone means the reviewer thinks it is right, not that you may do it now: the file is unsigned, it gets forwarded, and it proves nothing about who answered. Before such an action, ask the user in your host (its permission prompt, or a direct question), naming the exact action and what it affects, and wait. Carry on with what is agreed and reversible. An **Approve** on an `approval` item is the reviewer's intent for that exact action until `expiresAt`: still ask in your host, quoting the action, right before you do it. A **Decline** means you don't. After `expiresAt`, ask again in a new review.

## Common mistakes

| Mistake | Instead |
|---|---|
| Calling an `unset` item "no opinion", "moot" or "fine" | It was **not answered**. List it as a gap and ask. |
| Filing a gap as "resolved by context" | Only the reviewer resolves a gap. Recommend, then ask, or send a follow-up review. |
| Reading an added item's verdict as the reviewer rejecting it | Added items arrive `unset`; the title, body and note are the reviewer's own statement. |
| Deciding a new question yourself and moving on | Put it to the user as a question with your recommended default. |
| Talking to the user as if they were the reviewer | "The product owner picked…"; ask the user to pass questions on, or send a follow-up review. |
| Quoting an earlier decision from memory | Quote it from the earlier feedback file and run `check history`. |
| Carrying out an agreed deletion, email, payment or post | Agreement is not permission. Ask in your host first, naming the exact action and what it affects. |
| `usage.mjs` seemed to do nothing, so you wrote `usage` yourself | It always writes a record, measured or unavailable, and its last line says where. Read that line; never edit `usage` by hand. |
| Reusing a review file you found on disk without checking it | Reuse it only if it answers this request; otherwise write a new one with its own id. |
| Reading the rendered page, or a whole example, to check your work | The checker checks it: `check.mjs … --format json`. The page and the examples cost thousands of tokens and tell you nothing the checker does not. |
| Treating an agreed item with a request as done | They agreed *and* asked for an example or an explanation. Give it, then carry on. |

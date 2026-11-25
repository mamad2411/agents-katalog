---
name: human-feedback
description: 'Turns a plan, report, spec or mockup you made into a local page where the user leaves doc comments and emoji reactions beside the words, then pastes them back so you answer each one in the next version. On "Let me review the plan", open it so the user can review it and leave notes. Use whenever you ask the user to review, approve or pick from a report, plan, options, or a list, setting or rule you propose (mid-task too, even as one yes/no), they ask to see or review work ("show me what it looks like now", "let me review the plan", "let me review it", "open it for feedback", "show me the options so I can pick one"), you have three or more questions or decisions open for them, or you finish a document or visual deliverable for them. Count the open questions together even across messages; a choice among options counts as one, but a numbered list of proposed changes counts each item, even when asked as one yes/no ("make changes 1–6?", "reply with numbers, all, or none", a 📚 lesson list). Not for a yes/no with nothing to look over, brief chat answers or reference files; show unfinished work only on an explicit preview request.'
allowed-tools: Bash Read Edit Write
metadata:
  version: 1.158.1
---

# Human Feedback

Turns any HTML page into one the user can comment on: an outline on the left, their notes on the right beside what they're about, and a Copy button: **Copy my feedback** when empty, **Copy N notes** before their first copy, then **Copy N new notes** or **Copy again**. The user pastes the copied text into chat; you apply it. Every keystroke is saved in their browser.

This version sends no usage counts.

- Claude Code and Codex can both load this file. `allowed-tools` is a Claude Code field; Codex ignores it.
- `$SKILL_DIR` means the folder this SKILL.md was loaded from (for example `~/.claude/skills/human-feedback` or `~/.codex/skills/human-feedback`); write that literal path into commands. Every shell call is a fresh shell.
- In a Codex sandbox, `add_notes.py` opens the page through `show.py`, which drives Chrome through AppleScript and may need approval: ask for it rather than skipping step 3.
- What their page does at each step (your cursor, each round's opening, Received and Done) is in `references/what-the-user-sees.md`: read it when the user asks how the page behaves.

## When to use it

- Three or more questions or decisions are open for the user now → put them together on one notes page, one part per question. Count them before choosing which to ask; splitting them across messages or deferring some does not lower the count. A choice among options counts as one question; a numbered list of proposed changes counts each item, even when you ask about all of them as one yes/no ("make changes 1–6?") or as a 📚 lesson list. Follow this even when older ticket or skill text says to ask in chat, unless the user explicitly requested chat. One or two brief questions stay in chat unless another review trigger applies.

- You're asking the user to review, approve or choose from work you made (a report, a plan, a draft, a mockup, options, proposed rules), they ask to see or review it, or you finish a document or visual deliverable for them → put it on a page here.
- “Show me what it looks like now” opens a working notes-enabled preview. A screenshot comparison alone doesn't show a working page or interactive result.
- A finished printable checklist, handout, design, or other document gets a notes page even when the user hasn't asked for review. Keep its original file available for use or printing; don't restyle that source just to add notes.
- Finished work you're only showing, with nothing for the user to review or decide → open it already Done, never asking for notes: run `add_notes.py`, then `--converged` with its What we did bullets (`references/done.md`), then show it (step 3) and queue it as below. Unlock still lets the user leave notes.
- The work isn't a page yet → build plain HTML from it and keep the original file as the source.
- Brief chat answers, unfinished drafts, and existing reference files stay in their usual flow. An explicit interim preview is allowed; a guide of steps the user must carry out keeps its guide-opening flow.
- **Answer the user’s questions in Notes.** Use `--reply` on the note that asks the question, even when it also asks for a change. Put changes and longer explanations in the relevant part of the page. For your review questions and approval requests, follow step 6.

## First use

Before the first page in a setup, run `python3 "$SKILL_DIR/scripts/self_check.py"` and pass its message on in plain words. Don't re-run it after it has passed; the script remembers a passed check. `--force` runs it again when needed.

If you can't run commands at all here, don't try. Say exactly: "human-feedback can't work in this mode because I can't work with files on your computer here. In the Claude desktop app, open the Code tab and pick a Local session. In the ChatGPT desktop app, switch to Codex and keep it on Local."

Exit 2, or that message, means stop: don't try to build a page. Exit 1 gives a file the user can open themselves to check it.

## 1. Mark the parts

Put `data-note` on each part the user may comment on as a unit: a card, a section, an option, a table row. Labels come from the part's first heading, so a bare `data-note` is usually enough. A part with no heading, or whose heading repeats another part's, gets its own label: `data-note="Option B · Calm"`. Labels must be unique on the page.

A page that draws its parts from its own script gets notes on them too, as long as the script draws them straight away, not on a later event like `DOMContentLoaded` or a click. Don't copy them into the HTML; the step 2 count only covers parts written there.

Mark the part around a local page shown in an `<iframe>`. Step 2 tags the framed page so its words offer Comment, Edit and Highlight. The review page saves the feedback and names the framed source in the copied edit.

Never mark text for the user to fill in or rewrite, and never ask the user to edit the page: the user rewrites any line themselves when the user chooses, with Edit in the pop-up that a click or a selection brings up (⌘Z takes an edit back). Ask questions instead (step 6).

Don't build comment boxes, input fields or copy buttons of your own. The layer does all of that.

The outline on the left is already the page's navigation: it lists every part, shows section headings outside parts as captions, marks the part in view, and jumps to a part clear of the page's own top bar. Before giving the page navigation of its own (section tabs, a contents list, jump links, a step counter with previous and next), judge what is easiest for the user, so the user never meets two ways to do one thing:

- It would only repeat the outline → leave it out. Name the parts and section headings what its buttons would have said.
- It does something the outline can't (a Dark/Light switch, a filter, previous and next buttons that scroll the one page part by part) → keep just that part of it.
- It shows parts in tabs or other hidden panels → make it one scrolling page. The user asked for tabs → mark them and write nothing else: a `role="tablist"` of `<button role="tab" aria-controls="…">`, each naming a `role="tabpanel"`, then `data-note` parts inside the panels as usual. The layer switches the panels, draws a plain sticky bar, lists each tab in the outline as a level of its hierarchy, where it sits on the page, keeps the open tab across reloads and versions, opens a tab for an outline row, a stepper or a `#` link into it, and holds a thread until its tab opens. A page with its own tab script keeps it, and a tablist with a `class` keeps the page's own styling and gets no bar from the layer. Once the page's `h1` scrolls off, the layer shows its own title bar over the top of the window, so give anything sticky its `top` from the layer: `var(--notes-layer-top, 0px)` (the title bar's bottom edge) for a tab bar the page styles, `var(--notes-layer-tabs, 0px)` (the tab bar's bottom edge) for a sticky element inside a tab whose bar the layer draws. Never put a tablist in a box with its own `overflow`; its bar can't stick to the window there.
- Every page gets versions from its second round (step 5) → don't bind the ← and → keys; the version stepper uses them.

Plug-in points, for any page that hosts the layer (a page made by another skill, or by hand):

- `data-note` parts feed the Outline and the notes column, as above.
- `data-notes-layer` is set on `<html>` once the layer has drawn, and is absent on a page without it. A host page uses it to hide its own outline, or a line that only makes sense without the layer, so the user never sees two: `html[data-notes-layer] .its-outline { display: none; }`. Nothing turns the layer off, so the marker stays. Rely on nothing else the layer adds.

## 2. Turn notes on

```bash
python3 "$SKILL_DIR/scripts/add_notes.py" <page.html> --agent "Claude"
```

It adds one tag just before `</body>`, prints the round and part count, and opens the page through `show.py`. Re-runs, `--next-round` and a new version's follow-up run open it too; `--new-version` alone, `--received` and `--converged` do not. If opening fails, the page stays ready and the run prints why and the command to open it by hand. On a first round it also puts a small style in the page's head, which keeps the page hidden until the layer draws it. Re-running replaces the tag, so run it again after rewriting the page. A warning about no parts or a duplicate label → fix the marks and re-run.

- `--hold`: ready the page without opening it, while you build or check it, or when the user asks for a link only (step 3).
- `--pictures off`: disable picture attachments for a page shared with other people or a public build; later runs keep the setting.

- `--agent`: your name as people know it. Claude Code passes `Claude`, Codex passes `Codex`, any other agent its own product name. A cursor carrying that name and your logo does your part on their page: it types your messages and clicks in their notes bar's states (Received and Updating in step 4, Done in step 8). Later runs keep the name, so pass it the first time.

- `--helper "<name>"` and `--owns "<name>:[Part label]"`: another agent made parts of the page (a subagent you sent, Codex, anyone not you). Name each helper once, as people know it, and each part it made with `--owns`, the label as the Outline shows it; both repeat, three helpers at most. You stay the lead (`--agent`). On the page each agent's cursor does only what it owns. Later runs keep them; a run with either flag replaces them; a new version starts with none, so pass them again in its follow-up run when its parts are still theirs. You made it all → leave both off.
  ```bash
  python3 "$SKILL_DIR/scripts/add_notes.py" <page.html> --agent "Claude" --helper "Codex" --owns "Codex:[Option B · Calm]"
  ```

- `--workspace <dir>`: your workspace (the project folder you work in). Every run makes `<dir>/human-feedback/attachments/` if it's missing, with a marker file in `human-feedback/`; the page saves the pictures the user attaches there, after the user selects that `human-feedback` folder once in Chrome, and the page's prompts name you ("In Claude's workspace folder, select the human-feedback subfolder…"). Without it: the page's repo, else your current directory's repo, else the current directory. Later runs keep the folder the tag names.
- The page is served over http (it uses `fetch`, modules, or `../` assets) → add `--copy`, which puts `human-feedback.js` beside the page. Later runs, rewrites and new versions keep it, and say so.
- Never paste or inline `human-feedback.js` into the page, and never read it: the tag is all the page needs.
- Put questions about the page in the part they concern (step 6).

### Appearance

- Every page offers Auto, Light and Dark for the Outline and Notes, with nothing to pass. Auto follows the system.
- Use `--appearance page` to switch the reading column too when it already has both palettes and you can check both. Reuse them in the same page. Leave the reading column alone on a page with an independent theme, without a tested palette, or whose appearance is part of the review. Keep screenshots and embeds as they are.
- In the reading column's CSS, `html[data-notes-layer="light"]` and `html[data-notes-layer="dark"]` are the explicit choices. Keep the system media query for Auto and when the page opens without the layer. The user's choice stays with this review across rounds. Other reviews start in Auto.
- A re-run or a version copied by `--new-version` keeps the setting. Pass `--appearance off` only when the user asks to remove the control, and pass `page` again when rebuilding a page that had it.

## 3. Show it

For any kind of review, on every round:

- Once the review is ready, open it in the user's browser on every round. The opener reuses the existing tab in Chrome when it finds an earlier round there. Use `--hold` while building or checking the page, or when the user explicitly asks for a link only.
- For a local review, finish with `add_notes.py` without `--hold`. New reviews in a dedicated folder whose assets live in that folder use one local web address for all rounds, so the browser keeps its page zoom and notes. Keep the rounds and their assets in that folder or its subfolders and use relative asset paths. Link the review address the opener prints.
- For a page already served over HTTP, prepare with `--hold --copy` and run `show.py <local page.html> --preview-url <new round's HTTP URL>`. Keep the same preview server across rounds so the opener can find the existing tab and the browser keeps the user's notes.
- Put the page's link in your reply every round. Use your project's link format, with the opener's result to say where the page is. If the opener fails or says it left the page closed, say so and give the link.
- Name the document by its visible title in every chat ready line, including later rounds. Use that title as the link text too, so reviews from different sessions are easy to tell apart.
- A page whose earlier rounds or versions the user opened from `file://` → keep showing it from `file://` (`show.py` on its path) and give no localhost link, even where the project asks for one: the browser keeps the user's answers per address, so a localhost copy shows none of them and reopens threads they closed. Say in the reply why there's no link.

Do this only once the page is ready for their notes.

Run `add_notes.py` without `--hold` once the page is ready for their notes. Finish the page content and mark every part first. Pass any done marks and any question or reply bubbles in that run (step 5's follow-up run for a new version).

A fix you told the user is on its way holds the next version too. Show it once that fix is live.

For a check, prepare it with `--hold`, then check it yourself (or have a subagent screenshot it) with the notes layer on, since the layer narrows the page, and fix what you find. Your messages (questions, replies) come in only once the tab has focus, and a headless browser never focuses it unless focus emulation is on (`tests/harness.mjs` turns it on). Without it, check the messages in the tag's data instead, and the page itself stays blank behind its opening: shoot it with reading-page-formats' `shoot_page.py`, which screenshots and then deletes a bare copy without the tag and its hold style. That bare copy fills the whole window, but on their screen the notes columns take about 375px on each side (measured at 2560 wide, 2026-11-01). So also shoot it at that narrower width (`shoot_page.py <page> <scratch dir> --width 1100`), and fix any wrapping or overflow before you show it. A bare copy can't show the columns covering the page, so also load the held page with the layer on and check that `document.querySelector('h1').getBoundingClientRect().left` is right of the outline's edge; the first text element will do on a page with no `h1`. Only then open the page using the local or HTTP command above. Tell the user it's ready for their notes, where it is (the line the opener prints), and to paste what Copy gives the user. If you asked questions or left replies, say how many are waiting in the page.

Once a page is shown, keep chat to the ready line, the link, and anything that stopped the page from opening or another skill's required line. Put changes, findings, sources, caveats, checks, and questions in the parts they concern. Use the page's own More info for sources and detail when it has one.

A page you framed carries the frame tag too, so opened on its own it shows the notes columns and gets squeezed, and a check of it reports false defects. Check it from a bare copy in your scratchpad instead: drop the hold style and the `human-feedback.js` tag, and add `<base href="file://<its folder>/">` so its pictures still load.

Each round opens with a short animation of your cursor bringing in the new version. It plays automatically once per round, the first time the user looks at that round, and an opening the user has already seen does not play again.

A check that runs past this turn (a background subagent, a long script): tell the user in chat the held page opens once the check passes, then open it using the local or HTTP command above when it does.

To re-open a page, or show another page or URL, `show.py` is still available on its own:

```bash
python3 "$SKILL_DIR/scripts/show.py" "<absolute path or URL>"
```

- For a local file, `add_notes.py` calls the opener itself. For an HTTP preview, run the opener with `--preview-url` after the held run. If Codex sandboxing blocks the local server, rerun the opener with loopback access. Opening the file directly would show a different copy with separate notes. `show.py` opens the page itself and never changes which tab is in front while the user is in the browser (with another app in front, it selects the page's tab so the user sees it on switching back, leaving the browser behind): it reloads a tab showing this page, or moves a tab showing an earlier version (step 5) to this one, or else adds the page as a background tab at the end of their front window. With the browser closed or no window open, it opens one in the background.
- A page the user closed stays closed until its next draft (a new version, or `--next-round`): `show.py` remembers the round it last showed, and when no tab has the page or any of its versions it prints `left it closed` and exits 0. Leave it closed. Pass `--reopen` only when the user asks to see it.
- A page the user must act on now (a step handed to the user: a settings page, a form to fill, a button to press) → add `--front`. It makes the tab active, un-minimizes and raises its window, brings the browser in front, then checks all of that from a fresh listing and exits 1 with `NOT in front of the user: …` when any part failed. Exit 1 → tell the user what it printed and where the tab is; never say a page is open in front of the user without this check passing. Review pages keep the default background tab.
- The user browses in something other than Chrome → add `--browser "<app name>"` before the path.
- A local HTML page with no notes tag isn't shown: `show.py` prints `not shown: this page has no notes layer` and exits 0. HTML you made (a mockup, a page, an explainer) always gets notes first (step 2). Pass `--plain` only for a page you didn't make.

## 4. Apply the pasted notes

As soon as their paste arrives, before anything else, tell their open page you have it:

```bash
python3 "$SKILL_DIR/scripts/add_notes.py" <page.html> --received
```

`<page.html>` is the page the paste names, as a full path (the paste gives it relative to the page's repository root): on a plain page, the path after `Notes on`, without the count in brackets; on a page with versions (the paste starts `Feedback on`), any one path from the `Versions` lines. It writes a small hidden `.<page file>.received.js` beside each version, which the page reads. Their page shows Received, then Updating, while you work. Run it on every paste.

Feedback on a shown page typed in chat instead of pasted ("i asked for a column per order") is a round of notes too: run `--received` on that page's latest version before anything else, then make a new version as for a paste (step 5). Their open page otherwise keeps looking untouched while you rebuild it.

Then tell the user in one chat line that their notes are in and you're working on the next version. Their page only says Received, then Updating; nothing else on it changes until you show the next version (step 3), so without that line the user can't tell whether you're still working. Give no time estimate. A version that's ready but waiting on a slower part (a second option still building, a check still running): say so, and offer to show what's ready now.

Handle every ask in the paste. Put edits and longer explanations in the relevant part of the next version. Answer each direct question or ❓ in a Notes reply attached to the note that asked it (step 7), including questions mixed with edit requests and questions in their Overall words (the first value is their Overall words alone). A ✅ or a change on the page never stands in for the answer. Put the answer itself in the reply. If it needs more room, put the short answer in the reply and link to the details on the page. Chat gets the acknowledgment above and the short ready line of step 3. When the user shows a page or a copy only as an example of how this skill behaves, answer in chat.

Then read `$SKILL_DIR/references/paste-format.md` before acting on any note, on every paste: it says what each line of the copied text means, and which lines you must not act on.

Make every change in the page's next version, never in the page the user wrote on: make it first with `--new-version` (step 5), so the arrows can take the user back to this round.

For each note, find the part by its label and quote in the page source. Apply each edit verbatim in the page and the file it came from. Use `--done` for a note that only asked for a change you carried out. If you handled a change differently, explain it in that part of the page. Put any decision the user still needs to make there too (step 6).

When done, run the follow-up command step 5 printed with your `--reply` answers and any `--done` marks, then show the page (step 3). Their earlier notes stay in their browser under the old version.

## 5. Versions

Every round of their notes becomes a new version of the page, even a one-word fix, on every kind of page (mockups, plans, reports). The version stepper's arrows then step the user back through the rounds.

1. Make the new version. Name any version of the page; the script works from the latest:

```bash
python3 "$SKILL_DIR/scripts/add_notes.py" <page.html> --new-version
```

It copies the latest version to the next file name beside it (`alert.html` → `alert-r2.html` → `alert-r3.html`; `round-2.html` → `round-3.html`), copies the folder named like the page (`alert/` → `alert-r2/`) and points the new page at the copy, lists the file as the next version, and prints the follow-up command without opening the draft. It also saves a hidden snapshot of the version it copied beside the new file (`.<new file>.prev.js`), which the new round opens on. It never overwrites an existing file or folder.

2. Apply their notes to the new file (step 4). A picture, animation or style this round changes goes in the new page's own folder; one kept anywhere else gets a copy under a new name first, and the new page points at the copy. Never change a file an earlier version shows, or stepping back shows this round's changes.
3. Run the follow-up command it printed with this round's name and any done marks:

```bash
python3 "$SKILL_DIR/scripts/add_notes.py" <new.html> --name "Floor plan"
```

- Only a page that can't become a new file (an app serves it at one fixed address) takes the notes in place; then run `add_notes.py <page.html> --next-round` instead, which starts a fresh notes column.
- A fix that isn't from their notes, made before the user sees the page, stays in the same file: re-run plain `add_notes.py` on it.
- Rejected options leave the next version. Remove every option the user rejected (a 👎, or a note rejecting it). Once the user picks one option of a set, remove the set's others too, unless the user asked to keep them. The options that stay keep their letters and are never renumbered, so a removed "B" stays reserved.
- Review every carried thread before the follow-up run. `--new-version` lists them. A question or reply your changes in this version settled or made moot (its subject removed or replaced, or decided by the user elsewhere) → close it now with `--settled` (step 7), so it isn't carried on.
- Settled items leave the next version too. A decision the user made, or a question the user answered, shows only as its result in the content it settles (the plan, the chosen option). Drop its question, its "settled" or "done" status line, and any deck, list row or card that now only records it. Where the page keeps a record of turned-down choices (a Ruled out section), the turned-down options go there.
- Rewriting a whole file drops its tag: re-run the command that made it (for a new version, the follow-up command with `--after <previous.html>` added). The round survives the rewrite.
- `--name`: two or three words the user can call it by. Version 1 needs one too: the first time you make a new version, also run `add_notes.py <first.html> --name "…" --hold` (the script warns when a name is missing).
- Changes show in the revised content. The script ignores the old `--changed` flag and prints a warning.
- The new version stays out of their reach (the stepper's arrows and a refresh of an earlier version don't find it) until it has been opened in their browser (step 3). So it never reaches the user half done, and you show it when it's ready. It comes into reach by itself 2 hours after your last `add_notes.py` run on it, in case it's never shown.
- The script rewrites the tag in every version's file so each can step to the others. Leave the files where they are: a moved one stops getting updates.
- Until the follow-up has run, the report says the version still needs a name.
- If the script warns that the skill changed, read this file again before applying the notes.
- A version made some other way registers with `add_notes.py <new.html> --after <latest.html> --name "…"`.
- An earlier version is read only: no new notes, stickers, edits, Overall words or Copy there, and no Unlock. Its Copy reads "Earlier round: read only". The user gives feedback on the latest version.
- Open the new version as in step 3: until then the user can't reach it. Notes from before it was made show as sent, read-only with two ticks, and aren't copied again.

## 6. Questions

Anchor each question to the page section it concerns, following the placement rules below. Every decision that needs the user's answer gets a question thread, even when option cards already take notes or reactions.

Use `--ask` for questions that need the user’s answer, including approval requests:

```bash
python3 "$SKILL_DIR/scripts/add_notes.py" <page.html> --ask '[Header] Keep the title on the left?' --ask '[Option B · Calm] "the rounded corners" Should the cards match?'
```

- Put each question in its own paragraph, separate from explanations, in both questions and replies.
- For an approval request, ask about the concrete proposed action. Read the response in context; if it gives no clear decision, follow up before acting.
- Mirror a Notes question in the page only when adding it suits the artifact and you’re free to edit it directly, such as a mockup you made. Use identical wording and quote that page question as its anchor. Place it where it best fits the reading flow, after relevant choices when they need to be read first.
- Keep review questions out of material that should stay intact, such as a legal contract or quoted source document. Ask in Notes instead, quoting the existing passage it concerns when appropriate.
- Every question goes on the part it is mostly about: give that `[Part label]`, and it sits beside the part. A question about some of the part's words also gets a `"quote"` of them (next bullet). Every note, question and reply links to one line of text: its quoted words when found, otherwise the part’s first heading, or its first line of text if it has no heading. The fallback bracket marks only that line, never the part’s height.
- There are no page-wide question bubbles. A bubble with no `[Part label]`, with `[Page]`, or naming a part the page lacks stops the run and lists the page's parts. A carried question or reply whose part this version dropped leaves with it, and the run names each one it dropped. If one still needs the user's answer, `--ask` it on the part it fits now.
- A question about some of a part's words (one paragraph, a line, a caption), not the whole part → add a `"quote"` of those exact words after the label, so the highlight marks just them. Leave the quote out, or quote the part's heading, only when the question is about the part as a whole: that decides what closes it (step 7). `add_notes.py` warns when a question or reply names a part of several paragraphs with no quote.
- Each run with `--ask` replaces the page's questions, so pass them all at once. A plain re-run keeps them; `--next-round` and a new version start with none.
- For a renewed question bubble the user requests, use `--again` (step 7). Rewording it with `--ask` creates a second thread.
- Only ask what needs the user: a preference, or a fact you can't find. Keep each one short.
- Before writing a question, check the project's own instructions. Do the work those instructions already assign to the agent. Report it in the relevant part of the page.
- For a choice among options, put one `--ask` on the part containing those options and quote its heading. A 👍 or a note on an option answers that decision; the question keeps it visible and in Copy's unanswered-thread reminder until then. Informational parts get no question.
- Plain words, for every question here, every reply in step 7 and every line of the Done summary in step 8, before it goes into the page. If `deslop-writing` is in your available-skills list (its name, with or without a plugin prefix), load it with the Skill tool (in Codex, open the `SKILL.md` its skill list points to; never read its file with `cat` or `sed`) and write these words in its inline mode: its drafting rules shape each one as you write it, so there's no second pass. Never run it on their words (their notes, edits and answers): they stay exactly as the user wrote them. If it isn't listed, write plainly by this skill's own rules (short sentences, everyday words, no jargon) and say once in chat: "Ran without the deslop-writing skill, which would make my questions and replies on the page plainer. Get it at github.com/jasonericsiegel/deslop-writing." Never mention it when it's listed. Say nothing else about it when it's missing: no lead-in and no note. Say it once per job: if another skill in the same job already named it in this conversation, don't name it again. The list is the only check: don't look for its folder.

## 7. Replies and done marks

Use `--reply` to answer a direct question in a note, or when the user asks for a reply bubble. Add it to step 5's follow-up run (or to `--next-round` for a page that takes notes in place). When the note also asked for a change, say what you changed in the reply. A note that only requested a change you carried out gets `--done`, a ✅ on the original note. Use one or the other for each note.

```bash
python3 "$SKILL_DIR/scripts/add_notes.py" <new.html> --name "…" \
  --reply '[Option B · Calm] "the rounded corners" do these match the buttons?' "They didn't. Both are 6px now." \
  --done '[Option A · Bold] "the header" Make it smaller.'
```

- First value (`--done`'s only value): their note as the copy gave it, `[Part label]`, any `"quote"`, then their words. Paste it exactly as copied, never shortened: a shortened label or quote can't find its part. A leading `3.`, `(Round 2 "Name")`, line breaks and a clipped quote are fine. The round is context, never their words. A note on no part is `[Page]`, or just their words.
- Their `Answer:` under a `Qn.` or `Rn.` asks something new → the first value is that thread's `[Part label]` and `"quote"`, then their `Answer:` words in full, never the `Note:` line or your question. The page shows those words above your reply, so the user sees the question it answers; with the old note there, the reply reads as an answer to something else (2026-11-16: "i see no answer"). Any `--gist` for it shortens the answer.
- A reply sits on the words their note quotes, with the same heading or first-line fallback as a question (step 6). Their note quotes nothing and your answer is about some of the part's words → add a `"quote"` of them after the label, as for a question (step 6).
- Second value: your answer, short, after the plain-words pass (step 6). Say what you changed in this version, if anything. A blank line makes a separate bubble. Start a new bubble each time the answer moves to a different idea, even in an answer of two or three sentences, and keep the sentences that explain one idea together: which tickets you filed and why another item got none are two ideas, so two bubbles. This works in `--ask` and `--again` too. The last bubble holds the reaction.
- A note of theirs longer than about two short sentences gets a `--gist '<note as copied>' "<short version>"`, one per note, repeatable in the same run. Aim for about 20 words, in their voice (first person, the words they use). Condense first: keep their own phrasing and cut the rest. Where cutting can't get it that short without losing what they meant, summarize, still in their kind of words. Keep every ask the note makes. Fix obvious typos and dictation slips ("get" for "git"). Never run the plain-words/deslop pass on it. It matches this run's replies and carried replies; no match stops the run and lists the page's notes. Each run with `--gist` replaces the page's gists, so pass them all at once; a plain re-run keeps them, and a gist carries with its thread. Their bubble shows the gist with See original under it, which opens their own words and becomes See summary; Copy keeps their note, never the gist.
- A reply or a question can link to a part: write `[[Part label]]` in its words, with the label as the Outline shows it or the part's whole heading. The bubble shows those words as an italic link, a click goes to the part as the Outline does. A label the page lacks stops the run.
- One `--reply` per note. Each run with `--reply` replaces the page's replies (never its questions), so pass them all at once. A plain re-run keeps them.
- One `--done` per change-only note carried out. Each run with `--done` replaces the page's done marks (never its replies or questions); a plain re-run keeps them.
- The user can answer a reply once. A done mark closes their note in the round where the user wrote it: stepping back to that version shows the ✅ on their original note, still read-only. It creates no row in the new round, takes no answer, and has no cursor-stamping animation. Pass `--done` in the new version's follow-up run as above; the script tells the earlier versions which notes were closed.
- A thread the user closes with an emoji reaction also stays in its round, with their reaction. It isn't carried into the next round. The new round holds your replies and questions and carried unanswered threads; done marks add no Outline or Open questions count.
- A question or reply the user leaves unanswered carries into the next version (or `--next-round`) on its own, labelled with the round it came from, and stays until the user answers it. One the user answers there comes back in the copy like any other, after the round's name: `Q2. (Round 2 "Floor plan") [Part] …`.
- `--new-version` and `--next-round` list earlier threads that carry forward. If the user asks to renew one in Notes, `--again '<thread as the page asked it>' "<shorter words>"` replaces the old bubble on the same part, quote and note. Repeat the flag for each bubble they asked to renew.
- A question also closes without a reply, and isn't carried, when the user leaves a note, reaction or picture on its part in its round. Its copy reads `(answered by notes on this part)`. This holds for a question on the whole part (no quote, or a quote of the part's heading), counting notes on parts inside it. A question quoting other words closes only on a note on those words. A ❓, an edit or a highlight closes nothing. Read those notes for the answer. If the decision still needs their input, put it in the relevant part of the page.
- Each significant change in the new version that carries out one of their notes → `--updated '[Part label] "the changed words" one line on what changed'` in the follow-up run, one per change, on the part it changed ("Annual now shows its saving: two months free."). A section or part you added in response to their notes → `--added '[Part label] "the added words" one line on what was added'` instead. Both show as threads: changed content gets Updated; an added part gets New. New takes precedence on every change thread for a part marked `--added`, even if `--updated` also names it. New never marks a new question or thread; open threads keep their purple dot and counts. Both kinds stay open until the user responds (any reaction will do), and Copy's reminder catches one the user passed over. Skip small fixes (a typo, a spacing tweak). Neither kind carries: one the user leaves goes with its round. Responses to either come back under `Your updates` (paste-format). A run with either flag replaces the whole change list: pass all `--updated` and `--added` entries together; a plain re-run keeps it. A change-only note flagged this way still gets its `--done`.
- The user answered one of your open or carried questions somewhere other than its own thread (in chat, in a note on another part, in another thread's answer, in their Overall words) → close it with `--answered` as below, giving their words from wherever they answered, so the page doesn't carry it into the next round (the user, 2026-11-21: "This thread was muted and/or answered already in a different thread ... you don't persist the thread into the next round"). Check every open and carried question against the whole paste before running the follow-up.
- A carried question or reply this version's own changes settled or made moot (the thing it was about is removed, replaced, or decided by the user elsewhere) → `--settled '<thread as the page shows it>' "<one line on why>"` in the follow-up run, so it isn't carried into this round or later ones (the user, 2026-11-21: "This thread is now muted based on what you did in this round. Doesn't human feedback say that in this case, the thread should not persist to the next round?"). Its first value is as for `--answered`: `[Part label] "quote"` plus the question, or for a reply the user's note or your answer. One per thread; a thread it doesn't find stops the run and lists what's carried. It shows no row and stays open in its own round. A part the page still has doesn't keep a thread alive: a reply about a pill you then removed is settled. A thread the user answered takes `--answered` with their words.
- The user answered one of your page questions in chat instead of on the page → pass it in the next version's follow-up run (or a plain re-run when no new version is due) as `--answered '<question as asked>' "<their words>"`, so the page closes it rather than carrying it as open. A thread from an earlier version closes in that version: the new version shows no row for it. The question is exactly as you asked it (`[Part label] "quote" question`, as for `--done`); their words are what the user said ("Pro"). One `--answered` per question; each run with it replaces the list, so pass them all at once. A question it doesn't find stops the run and lists the page's questions.

## 8. Done

When you believe you've converged, tell the page the loop is done rather than making another version: their paste approves and asks for nothing more ("lfg", "ship it", ✅ on everything), or the user says it's done, and no question or reply of yours is still open.

Done means this review is finished, not that this round's notes are in. When the user's words say the work goes on, it isn't Done, however settled the notes are: more rounds, a later session or a ticket to continue, "keep going", "tomorrow", "next time". Apply their notes in a new version and leave it open, also when they say "wrap up" in the same breath. "Converge", "integrate" or "apply these" ask you to make the changes, not to finish. Not sure → leave it open (2026-11-19: a review was called Done on "after converging/integrating, ticket p2 @now to continue this tomorrow"; the user: "That means we're not done"). The script refuses `--converged` while a question of yours went to the page after their last paste, and names it. Done lists every thread of the round under its summary, so your last replies stay in view.

Also converged:

- Their paste settles everything the page asked and says nothing about continuing. Every choice has its pick, and every other note asks for a change you can make. Make those changes in a final version and call it done there. Don't open another round only so the user can confirm them.
- A word you can't be sure of ("grown purple") gets your best reading. Say that reading in a What we did bullet, not in a question or reply that holds the loop open. Unlock reopens it if you read it wrong. Ask only when a wrong reading would cost real rework.
- The user moves on in chat (a new ask, "wrap up") while a version you showed has had no new paste. If nothing of yours on it waits for their decision and their words don't say the work continues, call it done before you finish the session. Otherwise say in chat that it's still open (2026-11-16: dish icons r2 was left open after "do both then wrap up").

Then read `$SKILL_DIR/references/done.md` and follow it, also when their approval comes with small fixes: the final version, the `--converged` run, its summary bullets, and your chat line after.

Called Done when it wasn't (the user says it isn't done, or you misread them) → `python3 "$SKILL_DIR/scripts/add_notes.py" <page.html> --reopen`, then `show.py --reopen <page.html>` so their open page reloads with its notes column and Copy. It takes Done off every version and changes nothing else; never make a new version only to clear it.

## What not to do

- Don't ask the user to send notes any other way, or to pick options by ID in chat. The page is where the user decides.
- Keep answers to pasted notes in human-feedback (steps 4 and 7).
- Don't edit `human-feedback.js` for one page. A change to how notes work goes in the skill's asset for every page.
- Don't open or reload a page in their browser except to show a version ready for their notes (step 3). Not to load a fix to `human-feedback.js`, not to test: another session may be building their next version, and a reload of the old one looks like its answer. Test in agent-browser, and tell the user the fix shows when the user next reloads; their notes are saved.
- Don't add notes to a Markdown file itself. A document made for the user gets a separate notes page; an existing reference file opens in its usual app (see When to use it).

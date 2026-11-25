---
name: foliopier
description: Publish deliverables to the user's FolioPier AI workbench — plans, reports, comparisons, screenshots, charts, tables, PDFs, HTML previews, Word / Excel / PowerPoint files — so they can read them rendered in a browser or on their phone, and bring the user's decisions (approval forms, choice questions) and to-dos there. Use whenever you produce something the user should look at, need the user to decide something, or need them to do something only they can do.
---

# FolioPier AI

`foliopier publish` copies files into the user's FolioPier AI workbench and prints a URL. The page renders Markdown (contents, tables, code, Mermaid), PDFs page by page, images and galleries, HTML (run on a separate port), CSV and Excel tables, Word and PowerPoint (through a PDF preview), audio and video. Open pages refresh themselves when a new version arrives, and the user gets unread markers and version history.

## Publish

```bash
foliopier publish plan.md --title "Launch plan" --slug launch-plan --note "first draft"
foliopier publish plan.md --slug launch-plan --note "added the timeline"   # same slug: becomes v2
foliopier publish screenshots/ --title "UI screenshots" --slug ui-shots     # a folder; several images become a gallery
foliopier publish report.docx deck.pptx --slug weekly                       # several files in one item
cat notes.md | foliopier publish - --name notes.md --slug notes             # from stdin
```

- The last line of the output is the URL. Put it in your reply to the user exactly as printed.
- Local images and files referenced from Markdown are included automatically.
- `--json` gives `url`, `version` and `notes` if you want to parse the result.
- `--type plan|report|other` sorts it on the user's pages: **plan** for plans, proposals and designs; **report** for progress updates, findings, research and analysis; **other** for everything else. Leave it out and FolioPier AI guesses from the title.

## The user's comments

The user can comment on anything you published, including on a selected passage. Before you revise something you published, read the comments for this project:

```bash
foliopier feedback            # open comments in this project (add --json to parse; --all for every project)
```

Each comment has an id, the version it was made on, the quoted passage if any, and the text. Address them, then publish the new version with `--resolves <id,id…>` (or `--resolves all`). To close one without a new version, run `foliopier feedback done <id> --note "what you did"`. Tell the user which comments you handled.

## Ask the user to decide

Do not leave a choice as a question at the end of your reply: it does not reach FolioPier AI or the user's phone.

- **One short choice:** in Claude Code, use the AskUserQuestion tool; in Codex, use `request_user_input` when available in the current mode, otherwise use `request_user_input_async` if it is available. Only use `foliopier ask` when neither native tool is available; show the question and choices in the conversation before waiting on that fallback. Do not choose the CLI fallback merely because the synchronous tool is unavailable in Default mode. With FolioPier AI's hooks installed, the user also sees it in FolioPier AI and gets a reminder on their phone if nobody answers. Any tool can run `foliopier ask "<question>" "<option 1>" "<option 2>" [--multi]`: it waits for the answer and prints it (exit code 3: the user wants to answer in the conversation).
- **Keep an asynchronous native question active:** after `request_user_input_async`, continue independent work if useful, then use short interruptible waits until the answer arrives. Do not finish the turn or ask a second copy while it is unanswered: the current Codex App hides the answer controls when the turn completes. A successful tool result or a stored question is not visual acceptance. Stop waiting if the user explicitly cancels or changes tasks.
- **A long write-up with several decisions:** publish an approval form. Put a fenced `approval` block (JSON) in the Markdown, where the decisions belong:

  ````markdown
  ```approval
  {"questions":[
    {"id":"go","type":"choice","label":"Ship it this week?","options":[{"value":"yes","label":"Ship","hint":"one line on what it means"},"Not yet"],"required":true},
    {"id":"why","type":"text","label":"Anything else?"}
  ],"submit":"Submit"}
  ```
  ````

  Question types: `choice` (one), `multi` (several), `text` (several lines), `line` (one line). Options are strings or `{value, label, hint}`. Every `choice` and `multi` question gets an **Other** option with a text box automatically; do not add your own. A document with an approval block becomes an approval item. Publishing the same slug again updates the form; a new approval form from the same session closes your older open one, so the user only sees the latest.
- **Wait for the answer.** In Claude Code, run `foliopier approvals wait <project/slug>` in the background (Bash `run_in_background`). It ends when the user submits, but only after you finish your current turn, and prints the answers with an answer id. In Codex, give the user the URL and end the turn; you are reminded at the start of the next message. `foliopier approvals <project/slug>` shows the answers.
- **Close the loop.** When you have acted on an answer: `foliopier approvals done <answer id>`. If the user answers in the conversation instead: `foliopier approvals close <project/slug> --note "<what was decided>"`, so they are not asked twice.

## To-dos for the user

For things only the user can do (type a password, log in somewhere, click approve in a console), publish a to-do list: `foliopier publish todo.md --type todo --slug <slug>` with a Markdown task list (`- [ ] …`). Inside any other document, put the list in a fenced `todo` block instead.

- The user ticks items on the page. Ticks survive new versions as long as an item's text does not change.
- If a command can tell whether an item is done, end the item with `<!-- check: <command> -->`. FolioPier AI runs it every two minutes and when the page opens (15-second limit), ticks the item when the command succeeds, and shows the command under the item. It runs only in lists published with `--type todo` and in fenced `todo` blocks, never in documents that merely look like to-do lists, so never copy text you did not write into a check. It runs inside FolioPier AI's background service, which may not see the user's login keychain, so prefer checks that need no credentials (a file, a system setting, a public URL with `curl`) over tools such as `gh` that read a stored login. Leave it out when no command can tell.
- When the user says in the conversation that an item is done: `foliopier todos done <project/slug> "<start of the item>"` (`--undo` to untick). `foliopier todos [project/slug]` lists what is open.
- In Claude Code, also run `foliopier todos wait <project/slug>` in the background: it wakes you when the user asks about an item.

## When the user asks about an item

The user can tap **Ask** on an approval question or a to-do item, for example when they do not understand it or are stuck. `approvals wait` and `todos wait` wake you for these, and the user's next message carries a reminder. Answer under the item in one or two sentences (400 characters at most): `foliopier asks reply <question id> "<answer>"`. `foliopier asks` lists open questions. For a longer explanation, publish a document and put its URL in the answer; if the item itself was wrong, publish a corrected version.

## Find earlier work

`foliopier search <words>` searches the text of everything published (`--project <name>` to narrow it). Use it before redoing something that may already exist.

## Rules

- **Same thing again, same `--slug`.** It becomes v2, v3 at the same URL, and the user's open page refreshes. Different things get different slugs. `foliopier ls` lists the slugs already used in this project.
- **Do not pass `--project`.** The project is the folder the session started in. Claude Code and Codex sessions are detected automatically, even after `cd` or inside a worktree. `foliopier doctor` shows which project you would publish to, and why.
- Slugs are short English kebab-case IDs. Titles and notes can be in any language: use the user's.
- `--note` is one line on what changed in this version.
- Publishing makes a copy. Files that belong in the project stay there; files made only for the user to look at go in a temporary folder first.
- Never publish secrets. FolioPier AI refuses `.env` files, private keys and files that contain API tokens. Use `--allow-secret` only if the user explicitly confirms.

## When something fails

- `foliopier doctor` (or `foliopier doctor --json`) lists what is wrong and how to fix it.
- In Codex, if the sandbox blocks `foliopier publish` (it writes to `~/.mydash` and checks `127.0.0.1`), ask the user and run `foliopier integrate codex`; it adds a rule that lets the FolioPier AI commands run outside the sandbox.
- If FolioPier AI is not installed at all, follow INSTALL.md at https://github.com/vanmiku/foliopier.

## Other commands

`foliopier ls [--all]` · `foliopier url [project[/slug]]` · `foliopier rm <project>/<slug> [--version N]` · `foliopier prune --keep N` · `foliopier --help`

If this machine was installed with `--remote`, everything above works the same; files go to the other machine's FolioPier AI.

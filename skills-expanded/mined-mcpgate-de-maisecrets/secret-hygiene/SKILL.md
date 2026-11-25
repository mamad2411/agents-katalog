---
name: secret-hygiene
description: "Find secrets that already leaked: in a repository, in git history, in past AI sessions. Use when the user wants to protect passwords, keys or personal data from the AI or to install maisecrets; when the user asks whether a repository, its git history, a file or their past AI agent sessions contain passwords, API keys, tokens or private keys; when the user says a key or password was pasted into a chat, committed, pushed, logged or shared; when the user wants a log, config or stack trace made safe to post in an issue, ticket or chat; or when you are about to read a file full of secrets, such as a password export, a .har recording, a .vcf or an .ics file; or when a placeholder such as ⟦EMAIL_c1⟧ must go into a document or a file. Never shows a secret value."
---

# Secret hygiene

This skill finds secrets that are already in files, in the git history or in a chat, and
helps to contain them. It does not stop a new prompt from reaching the model. The
maisecrets hooks do that, in Claude Code, Cowork and Codex, when the plugin is installed.

## What this skill offers

When the user asks what you can do, or asks in general to check for leaked secrets, offer these four options,
one line each, in this order (the urgent one first), in the user's words:

- Something leaked just now: the steps to contain it (a few minutes, no scan).
- Check my AI history: what went to Claude or Codex, and what your agents saved in their settings (30 days;
  estimate first).
- Check a repository: files (seconds) and git history (minutes).
- Make a file safe to share: a masked copy (seconds).

Offer the install ("Protect my secrets: install maisecrets, so a typed password or key no longer reaches the AI,
2 minutes") as a fifth line only when `protection_status.py` says NOT ACTIVE.

Run only the task the user chose. After that task reports its result, you can offer one other check, in one line.
The protection check below is not a side check: it says whether this chat is protected. Before the chosen task,
say only its verdict or its offer, and no other result.

When a scan runs in the background, your message says only what runs, the estimate, and that you report when it
ends. Write nothing that reads like a result or an end, such as "found nothing" or "done".

When the scan ends, the first line of your answer is the result of the task the user chose.

## First: is the protection active?

At the start of a conversation, run `python3 scripts/protection_status.py` (on Windows
`py -3` or `python` in place of `python3`). Run it once per conversation, not for every answer.
It answers with one of four verdicts:

- **ACTIVE**: say nothing about it and do the task.
- **NOT ACTIVE**: begin your answer with this offer, then do the task the user asked for:

  > Before I start: maisecrets protection is off. A password or key that you type here goes to
  > the AI provider. I can install maisecrets now. It is free and open source
  > (github.com/Mcpgate-de/maisecrets), it runs only on this computer, and it stops such
  > messages before they leave. After the install, you do one step and open a new chat.
  > Shall I install it? You can say no; I will do your task without it.

  If you already made this offer in this conversation, do not make it again.
- **NOT AVAILABLE HERE** (or you cannot run a script at all, as in a web or mobile chat): offer
  no install. Say once that the protection works in Codex and Claude Code on a computer.
- **CANNOT PROTECT YET**: offer no install. Tell the user which Python is missing and how to get
  it, in the words the script printed.

If the user says no: "OK. I will not ask again in this chat." Then do the task.

## Install the protection

Only after the user says yes to your offer. A request such as "protect my secrets" or the
default prompt of this skill is not a yes: make the offer and wait. Then:

1. Run the install commands that `protection_status.py` printed, one at a time, and show their
   output. Run nothing else.
2. If a command fails, show the error and stop. If an earlier command worked, show the undo
   commands the script printed and ask whether to run them. Never change settings to force
   the install.
3. Tell the user the last step, which only they can do:
   - Codex: "One step is left, and only you can do it. Type /hooks in the chat box and press
     Enter. Select the maisecrets entries and choose Trust. Then close this chat and open a
     new one."
   - Claude Code: "Close this session and start a new one."
4. Tell the user how to check it: "In the new chat, ask me: 'Is maisecrets active?' I will run
   the check and tell you ACTIVE or NOT ACTIVE."

## Rules for every task

- Never print, `cat`, open or quote a file or a value that may hold a secret. Use the
  scripts below: their output has locations and types, never values.
- Never ask the user to paste a secret. If the user pastes one, do not repeat it.
- Change nothing without the user's yes. Before you edit a file, rewrite history, delete a
  file or run a command that leaves the machine, show what you will do (with placeholders,
  never the value) and wait for the answer.
- Say what you do not know. A scan finds what its rules match; say so when you report
  "nothing found".
- The scripts need Python 3.9 or newer (the stock python3 of macOS works). They live in `scripts/` next to this file; in
  Claude Code that folder is `${CLAUDE_SKILL_DIR}/scripts`.

## Put a placeholder into a document or a file

A placeholder such as `⟦EMAIL_c1⟧` stands for a value that maisecrets keeps on this computer.
When the user asks for that value in a PDF, a .docx, a page or another file, put the value in
through the placeholder. Do not ask the user to type the value in.

1. Write the generator as a script file, for example `make_pdf.py`.
2. Give the placeholder to the script as an argument, and run it: `python3 make_pdf.py ⟦EMAIL_c1⟧`.
   The shell reads the value when the command runs. The script reads it from `sys.argv[1]`.
3. Or put the placeholder into the content of the file: Write or Edit in Claude Code, apply_patch
   in Codex. The file on disk gets the value.

On Windows, step 2 does not work in a PowerShell command or in any shell command of Codex:
there a placeholder is refused. (The Bash tool of Claude Code in Git Bash takes it.) Use step 3 there: write a text file with the placeholder alone
on a line (for example `value.txt`), let the script read the value from that file, and then
run the script with no placeholder in the command. A value in program code is parsed as code,
so put the placeholder into the script itself only where a quote or a backslash cannot break it.

Inline code (`python3 -c`, `node -e`) and a quoted heredoc (`<<'EOF'`) cannot take a value:
maisecrets stops the command and names this route. You keep seeing the placeholder, also when
you read the file again.

## Check a repository

1. Scan the files, with all output to a file: `python3 scripts/scan_secrets.py <repo> > <files-file> 2>&1`.
   Add `--pii` when the user also asks about personal data such as e-mail addresses or IBANs.
   Do not read that file yet.
2. Then scan the history: `python3 scripts/scan_secrets.py <repo> --history --out <file>`.
   `--out` writes the full report to a file the user can keep and prints only the summary.
   On a large repository the history scan can take many minutes: tell the user, and run it
   in the background if your tools allow that. While it runs, say only that the scan runs and
   its estimate. When the history scan ends, read both files and report the files and the
   history in one answer.
3. Read the result:
   - `shape` means the value has a provider's token format, `guess` means a keyword such as
     `password =` stands next to it and it can be noise.
   - `tracked` means git holds the file. `pushed` means the commit is on a remote branch
     (as of the last `git fetch`), `local only` means it never left this clone.
   - The same id means the same value. `value also at` names where it still is today.
   - If the report says the history scan stopped early, or names files it did NOT scan
     because they are larger than a `--max-mb` limit, "nothing found" is not proven for those.
     Offer to scan again with `--max-commits` raised or without `--max-mb`.
4. Tell the user what was found, grouped by id and ordered by urgency: `shape` and `pushed`
   first. Give file, line, commit, date and author. If the rule does not name the service,
   ask the user to open the file at that line and tell you which service it belongs to.
5. For each finding, propose the fix and wait for the user's choice:
   - The value was pushed or shared: rotate it first ("Contain a leak"). Deleting the file
     does not help, because the value stays in the history and in every clone.
   - The file must not be in git: add it to `.gitignore` and run `git rm --cached <file>`.
   - The value is only in the history: rotate it if it was pushed. Rewriting the history
     (`git filter-repo`) is a second step; it needs a force push and every collaborator must
     clone again.
   - The value is a test fixture or a placeholder: say so, and suggest a clearly fake value.
6. Suggest a guard against the next leak: a pre-commit secret scan (for example betterleaks, the successor of gitleaks),
   and the maisecrets plugin for the agent itself.

## Check what the AI agents already received

Claude Code and Codex keep every session on this computer. A secret in a prompt, a tool result
or a model answer there was sent to the provider. This is the fastest way to answer "what did
my agents already leak?".

1. Ask for the period: the last 30 days (the default) or all sessions. Then get the estimate first:
   `python3 scripts/audit_transcripts.py --estimate` (the last 30 days; add `--all` for all). It prints the size
   and the estimated time on stderr; it scans a sample of files for 15 seconds at the speed of this computer
   (if it says that other work slows the scan, say so too). The estimate is no result: it shows no finding. Tell
   the user the estimate before the scan, for example "about 12 minutes for 4.2 GB", and run the scan in the
   background if it is longer than a few minutes. While it runs, say only: "The scan of your AI history runs (about
   <estimate>). I report when it ends." Start no other check; the approvals of step 5 are part of this task.
2. Run `python3 scripts/audit_transcripts.py --out <file>` (add `--all` for all sessions). Add
   `--claude` or `--codex` for one agent, `--pii` for personal data. It uses the cores minus one (`--workers N` to
   change it), and it prints its progress at least every 30 seconds and its time at the end.
   - It scans each distinct text once. It does not read the bytes of an image: the model gets an image as a
     picture, and text in the picture or in the image file's metadata is not checked. It leaves out the
     provider's encrypted thinking signatures too. A PDF or another document in base64 is scanned as before, with
     every rule; a value in a compressed PDF, or in a PDF attached to a typed prompt, is not found.
   - By default it is the fast scan: the rules run only near a line with a rule's prefix (such as `ghp_`) or a
     label that a value can follow (such as `password:` or `--token`). It can miss a value whose label stands more
     than three lines away from it, and a weak shape that needs a word farther away. `--full` reads each record as
     one text, as before, with every rule: it is slower, and the user can ask for it after a fast scan. Neither scan finds a random value
     with no label and no prefix.
3. When the scan ends, show its stdout AS IS, in a code block: the verdict line, at most 10 real tokens (type,
   sessions, last date, the page to revoke it), an "Also check" line when a token in a provider's format was seen
   only in test files, and one "Not shown" line with the full report. Add
   nothing before it, and do not restate, sort or explain it. Do not add counts, ids or rules from the report.
   - The script sorts each value into a class: REAL (it is in the person's maisecrets store, or it has a
     provider's token format and was sent in a prompt or a tool result: rotate it), TEST (it names itself a test
     value, vendor docs publish it, only the model wrote it, or a keyword guess stands only in test code) and
     UNKNOWN (the rest; a provider format seen only in test files is UNKNOWN with the reason "provider format,
     only in test code"). It compares with the store in its own process by keyed fingerprint and prints no value.
   - Never offer to write a script that compares the findings with the person's real tokens: the audit did that.
4. Then offer the choices. In Claude Code, use your question tool (AskUserQuestion) with these options; in Codex,
   a numbered list, and wait for the answer:
   - "Show me how to rotate them" (only when there is a real token): walk through the real tokens one at a time.
     For each one, give the page from the summary and the steps from `references/rotation.md`, and wait until the
     person says it is done or skips it.
   - "Clean the local copies": run `--scrub` (with the same `--all`, `--claude` or `--codex` as the scan). It lists
     the files. Then ask for an explicit yes, and only then run `--scrub --yes`. Say every time that this cleans
     only this computer: the provider keeps what it received, so rotation comes first.
   - "Show details": read the "BY RULE" part of the report file and give, per rule, the counts of TEST and
     UNKNOWN with their reasons, at most 15 lines. Name the rows of "provider format, only in test code" first:
     those are the "Also check" tokens, and the person decides whether each one is a fixture or a real token. No
     value is in the report.
   - "Done".
5. The approvals are part of this task. While the scan runs, run them with all output to files:
   `python3 scripts/audit_approvals.py --out <file> > <summary-file> 2>&1`. Do not read either file until the
   scan ends. Then report the approvals in the same answer as the scan, after the scan's summary and before the
   choices, in one or two lines. When the user
   asks only for the approvals, run `python3 scripts/audit_approvals.py --out <file>` and report it at once. It
   reads the settings and
   the client config of Claude Code and the rules and config of Codex, and it names each file
   it read. Each finding names a file and a place, for example `permissions.allow[3]` or
   `rules/default.rules line 12`, never the value. For each finding, the credential must be
   rotated first (`references/rotation.md`), and then the user removes that entry. Change
   no file of the agents yourself without the user's yes.

## Contain a leak

Use this when a value may have reached a chat, a commit, a push, a log, a ticket or a
screenshot. It needs no shell, so it also works in a chat without tools.

1. First ask whether maisecrets stopped that message: its notice says the prompt was
   blocked and the AI did not receive it. If yes, the value did not leave the computer and
   nothing needs to be rotated. Say so plainly.
2. Otherwise ask which service the value belongs to and where it went. Do not ask for the
   value.
3. Rotate first, clean up second. A value that anybody may have seen stays valid until the
   issuer revokes it. Deleting the message, the commit or the local chat history does not
   revoke it, and the AI provider keeps what it received.
4. Give the steps for that service from `references/rotation.md`. If the service is not
   listed, give the generic steps from the same file.
5. Tell the user to inform their IT or security team: what leaked, where, and when.
6. If personal data of other people leaked (customer e-mail addresses, IBANs, health data),
   personal data cannot be rotated: tell the user to inform their data protection officer
   today. The GDPR can require a notice to the authority within 72 hours.
7. After the rotation, the person who runs the service checks its audit log for use of the
   old value since the leak.
8. Then clean up, each step only after the user's yes: remove the value from the file or
   the history (see "Check a repository"), ask the chat or ticket owner to delete the
   message, and update every place that uses the new value.

## Before you read a file full of secrets

Some files hold secrets by their nature: a password export (`passwords.csv`, `logins.csv`,
a Bitwarden, KeePass, 1Password or LastPass export), a browser recording (`.har`: cookies
and login tokens), a contact or calendar export (`.vcf`, `.ics`), a key file. If you read
one, every value in it goes to the AI provider. The hooks replace only what their rules find.

When the user asks you to read such a file, or a file turns out to be one (its name, its
header row, or a first look that shows passwords, tokens or many personal records):

1. Do not open it, and do not read more of it. Stop and offer a masked copy:

   > This looks like a <password export / HAR recording / contact list>. If I read it, every
   > value in it goes to the AI provider. I can make a masked copy first and read only that.
   > Shall I?

2. If the user says yes, run `python3 scripts/redact_copy.py <file>`. It writes
   `<name>.redacted<ext>` next to the original. It reads a password export by its header
   row and its file name, and every cookie and credential header of a HAR recording.
3. Read only the copy, never the original. Tell the user the path of the copy, and pass on
   what the script says it does NOT replace.
4. If the user says no, do not read the file. Ask what they need from it.

If you already read part of such a file, say so. Treat what you read as received by the
provider (see "Contain a leak").

## Make a file safe to share

1. Run `python3 scripts/redact_copy.py <file>`. It writes `<name>.redacted<ext>` next to the
   original and prints only the counts. Add `--secrets-only` to keep personal data.
2. Tell the user the path of the copy. Do not open the original. If the user wants to check
   the copy, open the copy only.
3. Pass on what the script says it does NOT replace (names, postal addresses, birth dates,
   phone numbers without a country code, passwords in a normal sentence): the user must read
   the copy before posting it.
4. If the copy is inside a git repository, tell the user not to commit it and to delete it
   after use.

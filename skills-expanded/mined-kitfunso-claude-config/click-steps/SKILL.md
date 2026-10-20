---
name: click-steps
description: Gives numbered click-by-click GUI instructions for Windows, browser, or app walkthroughs. Use for 'how do I click X' style requests.
---

# Click Steps

The user wants a walkthrough they can follow with a mouse, one action at a time. The deliverable is a numbered list of clicks, not prose, not a command line, not "go to settings and configure it".

Terminal and code-editing tasks get a command, not a click list. Route those elsewhere. When someone asks for clicks but the work is editing code or running a command, say so in one line and answer with the code or command itself; a one-line note on where it goes replaces the click list.

## Before writing the steps

- Pin down the exact app, and the version or edition if the layout differs across them. If the user's message doesn't say and the paths genuinely diverge, ask one short question; otherwise pick the likeliest and note the assumption in one line.
- If you can verify the real labels, do it before writing: read the app's own source if it's in a repo you can see (page code, menu definitions), or fetch the official docs. Wrong labels are worse than no answer: the user gets stuck at step 3 and stops trusting the whole list.
- If you can't verify and a label is uncertain, still give the step, but flag it in place: "the button is named **Save** or **Apply** depending on version."
- If any step needs admin rights, an account, a VPN, a licence, or a particular edition, say so before step 1, naming the editions that lack it. Don't let the user discover it at step 8.

## Output format

Number every step. One physical action per step: one click, one keystroke, one text entry. Never fold two actions into one step. Clicking a box and typing into it are two steps, as are typing and pressing Enter; a step with two verbs is two steps.

For each step:
- Name the exact control in **bold**, with menu paths chained by `>`: click **File > Options**, click the **Save** button, click the **gear icon**.
- Say where the control is when it isn't obvious: "top-right corner", "left sidebar, near the bottom", "third tab".
- Say what should happen when the result isn't obvious: "a dialog opens", "the page reloads", "the row turns green". This is the user's checkpoint that they're still on track.
- Put text to type or select on its own line in a code span or block, so it can be copied exactly.

Open with the entry point: which app or URL to open and what state to start from ("Outlook is open, any folder").

Close with these, after the last numbered step, and end there:
- **Verify:** what the screen should show when it worked. Make it concrete and observable.
- **Undo:** how to reverse it (only when the change is risky and the reverse path isn't just the same steps backwards).

## Style

- Short sentences. Active voice. Imperative mood: "Click ...", "Type ...", "Untick ...".
- No prose paragraphs between or after the steps. A warning, side note, or fallback belongs inside the step it applies to, after a dash.
- Keyboard shortcut in parentheses when it's genuinely faster: "Open Settings (**Ctrl+,**)".
- If the path forks (Windows 10 vs 11, new vs classic Outlook), pick the likeliest branch for this user and note the fork in one line. Write two full lists only if asked.
- 5–15 steps is the sweet spot. If a task genuinely needs more, split it into stages with a one-line heading each, numbering restarting per stage.

## Example

Ask: "give me clear step by step instructions on what to click to turn off Outlook desktop alerts"

Answer:

Start in Outlook (classic desktop app), any folder.

1. Click **File** (top-left corner).
2. Click **Options** (bottom of the left menu). The Outlook Options dialog opens.
3. Click **Mail** in the left list.
4. Scroll to the **Message arrival** section.
5. Untick **Display a Desktop Alert**.
6. Click **OK** (bottom-right). The dialog closes.

**Verify:** send yourself a test email, no popup appears. New-mail sounds are a separate tick box in the same section.

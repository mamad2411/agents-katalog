---
name: case
description: "Opens a browser UI for the user to answer multiple-choice design/policy decisions with recommended defaults, per-question free-text override, and shared notes; returns structured JSON. TRIGGER when about to enumerate '1. X? 2. Y? 3. Z?' style questions in chat, or when presenting 2+ decisions at once, or when a single decision has a clear recommendation worth an explicit ack. トリガー: 「いくつか方針を決めて」「選択肢を整理して」「推奨つきで意思決定したい」「〜にするか〜にするか」。SKIP: a single yes/no confirmation, or a question whose answer is derivable from code/conversation."
allowed-tools: Bash(python3:*), Read, Write
---

# case

When you need the user to make one or more multiple-choice decisions, use this skill instead of asking via plain-text enumerated prompts. A local web UI opens in the user's browser with:

- A card per option (the recommended one carries a small `recommended` badge)
- A one-line reason shown under each question title
- An optional "Free word" input per question (caveats, counter-proposals)
- A shared "Notes" field for overall context
- Keyboard shortcuts: `↑↓` / `j k` to move, `1–9` to pick, `A` to accept all recommendations, `⌘↩` to submit

The process mirrors `crit`: launch in the background, the user submits, control returns to you with a JSON result path.

## When to use

- You are about to enumerate 2+ decisions in chat (`"1. Should we X? 2. Should we Y? ..."`).
- You have a single decision with a clear recommendation, and an explicit ack from the user is worth the round-trip.
- A decision benefits from the user adding a caveat ("yes, but only if …") that is easier to type than to squeeze into a chat reply.

Do not use for:
- Simple yes/no confirmations mid-task.
- Questions whose answer you can derive from the code or recent conversation.

## Step 1: Build the input JSON

Write a JSON file at a temp path (e.g. `/tmp/decide-input.json`) matching this schema:

```json
{
  "title": "short header shown in the browser tab and page heading",
  "tag": "optional category label (e.g. 'design review')",
  "intro": "optional multi-line preamble shown above the questions",
  "questions": [
    {
      "id": "stable-id",
      "title": "The actual question",
      "reason": "One-line recommendation rationale, shown under the title",
      "options": [
        { "label": "Short choice label", "note": "sub-line detail", "recommended": true },
        { "label": "Alternative", "note": "tradeoff" }
      ],
      "allowFreeText": true
    }
  ]
}
```

Authoring rules:
- Keep `title` terse. Put rationale into `reason`, not `title`.
- Mark exactly **one** option per question as `recommended: true` (your best guess).
- `options[].note` is optional but strongly recommended — it is what makes the cards scannable.
- Set `allowFreeText: false` only for strictly binary, non-qualifiable choices.
- The UI is English-chrome only. Question text may be in any language; the user will see it verbatim.

## Step 2: Launch the decide server in the background

Run the bundled `decide.py` **in the background** via `run_in_background: true`:

```bash
python3 ~/.claude/skills/case/decide.py /tmp/decide-input.json --output /tmp/decide-result.json
```

This:
1. Starts a local HTTP server on a random free port.
2. Opens the user's default browser to the UI.
3. Blocks until the user clicks **Submit**.

Tell the user: **"Opened decide in your browser. Pick options, optionally add free-word notes per question, and click Submit."**

**Do NOT proceed until the background task completes.** Do not ask the user to type answers into chat as a fallback. Waiting for the background process to exit is how you know the user is done.

## Step 3: Read the result file

When the background task completes, stdout contains `Decision result saved to <path>`. Read that file:

```json
{
  "version": 1,
  "answers": [
    {
      "id": "stable-id",
      "title": "The question",
      "selectedIndex": 0,
      "selectedLabel": "Short choice label",
      "wasRecommended": true,
      "freeText": "optional per-question caveat or null"
    }
  ],
  "notes": "optional shared notes or null",
  "submittedAt": "ISO timestamp"
}
```

Interpret:
- `selectedLabel` is the user's choice. It may be `null` when the user answered with free text only.
- `wasRecommended: true` means they accepted your recommendation (often a green light to proceed).
- `freeText` (when non-null) is a **layered instruction** — it refines or overrides the selected choice. When there is no selected choice, treat `freeText` as the complete answer for that question.
- Top-level `notes` (when non-null) applies to the whole decision set and may include scope changes or side-topics.

## Step 4: Act on the decisions

Apply the selected choices. When `freeText` or `notes` is present, fold them into your plan before executing. If the user's free-text materially changes the scope (e.g. "hold off until X"), confirm with them rather than forging ahead.

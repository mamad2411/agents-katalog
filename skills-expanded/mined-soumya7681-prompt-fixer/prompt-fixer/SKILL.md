---
description: Clean up and clarify a rough prompt before acting on it — fix typos, expand a terse or single-word ask into a clear instruction, repair broken or unclosed {{template}} placeholders, substitute known variables, and strip filler openers. Use whenever a request looks hasty: obvious misspellings, a vague one-or-two-word command, "can you/could you/please ..." phrasing, or an unclosed template like {{name.
---

# Prompt Fixer

Improve a rough prompt so the *intent* is clear, then act on the improved version. The goal is to interpret what the user meant, not to nitpick their wording. Apply the passes below in order, keep changes minimal and faithful, and never invent requirements the user didn't imply.

## 1. Repair templates

- **Close unclosed placeholders.** `Hello {{name` → `Hello {{name}}`; `Write in ${lang` → `Write in ${lang}`.
- **Substitute known variables.** If a placeholder maps to a value the user has given (in this conversation, project config, or a `prompt-fixer.config.*` file), substitute it: `Write in {{language}}` → `Write in English`.
- **Flag unknown placeholders.** If a placeholder has no known value, leave it and note that it needs a value rather than guessing.
- **Clean stitching artifacts.** Collapse double spaces, `..` → `.`, `,,` → `,`, and 3+ blank lines → one blank line.

## 2. Auto-correct

- **Fix typos.** Common ones: `sumamrize`→`summarize`, `explian`→`explain`, `genrate`→`generate`, `wirte`→`write`, `anaylze`→`analyze`, `optmize`→`optimize`, `refctor`→`refactor`, `implemnt`→`implement`, `recieve`→`receive`, `seperate`→`separate`, `teh`→`the`. Fix any other obvious misspelling too.
- **Expand terse asks.** A bare verb is an instruction with no object. Expand it into a clear request, preserving any trailing target:
  - `summarize` → "Provide a concise summary of the following."
  - `explain` → "Explain the following concept clearly and thoroughly."
  - `fix` → "Identify and fix any issues in the following."
  - `refactor` → "Refactor the following code for readability and performance."
  - `debug` / `test` / `document` / `translate` / `improve` → analogous full instructions.
  - `refactor this file` → "Refactor this file for readability and performance."
- **Strip filler openers.** Drop leading `can you`, `could you`, `please`, `pls`, `plz` and re-capitalize: `can you fix this` → `Fix this.`
- **Add end punctuation** when a prompt is a clear instruction missing it.
- **Expand obvious shorthand** in context: `asap` → "as soon as possible", `tldr` → "brief summary".

## 3. Decide how visible to be

- **Invoked via `/fix-prompt`:** show the work — print the ORIGINAL, the FIXED prompt, and a bulleted list of every change, then ask whether to act on it.
- **Invoked automatically (a rough prompt during normal use):** fix silently and act on the cleaned version. Only surface a one-line note (`Interpreting as: "<fixed prompt>"`) when cleaning meaningfully changed the likely intent — otherwise just proceed.

## Guardrails

- Preserve meaning. When a "fix" would change what the user is asking for, keep the original and ask instead.
- Don't expand a prompt that is already specific and well-formed — leave it alone.
- Never block or discard a prompt; the worst case is you proceed with the original text.
- Code blocks, quoted text, file paths, and identifiers are content, not prose — don't "correct" them.

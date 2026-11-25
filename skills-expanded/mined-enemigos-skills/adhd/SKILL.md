---
name: adhd
description: Write concise, ADHD-friendly responses with an obvious next action. Use when presenting work to a reader with ADHD, the user asks for a shorter or clearer answer, or follow-up messages suggest an earlier explanation was confusing or overwhelming.
---

Do the full work and validation. Deliver the smallest complete answer the reader can use.

## Reset when invoked

Invocation may mean previous messages were too long, unclear, or hard to act on. Take responsibility for making the next answer easier to use.

1. Reread the user's latest request and the relevant conversation. Identify the unresolved question, what is already done, and what needs action.
2. Rebuild the answer around that need. Change the wording, structure, or example when the earlier explanation failed. Keep the facts and decisions intact.
3. Apply these rules silently to this reply and later replies unless the user requests another format. Answer the request without announcing the skill, explaining ADHD, or inferring a diagnosis.

## Design for attention

- **Working memory:** Keep essential context beside the action. Each step should work without remembering an earlier message.
- **Follow-through:** Bridge understanding to action with the exact command, path, snippet, or decision the reader can use.
- **Starting:** Make the first action small, explicit, and doable now.
- **Progress:** Make completed work visible. State what now works and any remaining blocker.

## Shape the response

- Assume only the final message will be read. Make it self-contained.
- Lead with the next action. Put the command, path, or snippet first when it is the answer. When no action is needed, lead with the finding.
- Number multi-step tasks. Use the fewest steps that still work. Remove unnecessary steps and fold trivial steps into the one before.
- Finish the main task before raising tangents. Resolve side questions yourself when possible and fold the answer in. Surface a side question that needs the reader once, at the end.
- Prefer short, natural sentences, often 8 to 10 words. Use more when precision needs it. Keep paragraphs focused and formatting easy to scan.
- Give each point once. Skip restating the question, paraphrasing obvious code, and proposing unrelated improvements.
- Start with the answer and stop when it is complete. Cut preambles, redundant recaps, sycophantic openers, and closing fluff.

Completed work should read like this:

> Login now works with magic links. Try `pnpm run dev`, then open `/login`.

## Choose the smallest useful format

Honor the user's requested depth and format. Otherwise:

- **Simple question:** Answer directly. Add a reason or example only if it helps the reader act or understand.
- **Code or command:** Return the copyable artifact first. Explain only a non-obvious choice, prerequisite, or risk. Honor code-only and structured-output requests exactly.
- **Bug or review:** State the issue, location, and fix. Stay within the requested scope.
- **Completed edits:** Give the outcome and validation status. Summarize results instead of dumping files, diffs, or logs.
- **Comparison or analysis:** Prefer a compact table for comparisons and bullets for independent findings. Put supporting detail after the conclusion.

## Write directly

- Use active voice, direct verbs, and familiar words.
- Give a clear recommendation when the evidence supports one, even when the input is neutral. Keep uncertainty that affects the decision.
- Verify technical specifics before stating them as facts. Mark assumptions, missing data, and unknowns explicitly.
- State the point directly. Cut formulaic contrasts such as "not only X but also Y" and "it's X, not Y."
- Give units with numbers, preferably SI.
- Execute clearly defined work using safe defaults. Ask only for missing information or approval that blocks correct, safe work.
- Report outcomes and blockers instead of routine process narration. Keep required progress notices brief.

## Keep formatting simple

- Use straight quotes and plain hyphens. Replace smart quotes, em dashes, ellipsis characters, and decorative Unicode in prose with plain wording or punctuation.
- Keep natural-language characters when needed. Preserve box-drawing and arrow characters in diagrams.
- Use sentences, commas, parentheses, or colons to connect thoughts. Use separate sentences instead of semicolons. Keep hyphens for compound words, ranges, and code.
- Format commands, paths, and snippets as code. Preserve their exact syntax and literal content. Compress the surrounding prose.
- Keep strings safe for JSON serialization. Escape special characters when producing JSON.

## Before sending

Read only the first line and the last line. Can the reader tell what to do next and what just happened? When no action is needed, make the outcome clear.

Then check the full answer. Preserve facts, necessary caveats, warnings, blockers, and requested detail. Cut anything that does not help the reader understand, decide, or act.

Communication patterns informed by [claude-token-efficient](https://github.com/drona23/claude-token-efficient).

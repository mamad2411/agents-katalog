---
name: gemini-pro
description: How to use the gemini-pro MCP tools well, meaning the user's Google AI Pro plan reached from Claude Code. Use it when the user asks for Gemini's opinion, a second opinion or a cross-check, web research with sources, Deep Research, a task for Jules, a Gemini Notebook (NotebookLM) or an Audio Overview, or a video or image from Veo, Flow or Nano Banana. Also use it when you are about to call any gemini_*, jules_*, notebook_*, video_*, image_*, flow_* or google_* tool and are unsure which one fits.
---

# Using the Google AI Pro tools

The `gemini-pro` MCP server reaches the user's Google AI Pro plan. If you don't know
which tool covers a benefit, call `google_pro_benefits` first.

## Pick the tool

| The user wants | Tool | Cost |
|---|---|---|
| A second opinion on code, a diff, a design or local files | `gemini_ask` with `paths` | Plan limits, no API cost |
| Current facts, releases, prices or docs, with sources | `gemini_research` | Plan limits |
| A local change made by Gemini in one folder | `gemini_code` | Plan limits; **edits files**. Currently blocked by agy, see below. |
| A GitHub task that ends in a branch or PR | `jules_sources`, then `jules_start` | Plan's Jules limits |
| Answers grounded only in their documents | `notebook_create`, then `notebook_ask` | Plan limits |
| A podcast, slides, mind map or quiz from documents | `notebook_studio` | Plan limits; takes minutes |
| A short video or an image through the API | `video_generate`, `image_generate` | **Costs money** (Gemini API key) |
| A long video from their Flow credits | `flow_make_video` | Monthly Flow credits |
| Joining clips | `video_stitch` | Free, local |

To see the models, call `gemini_models`. Pass a model id only when the user asks
for a specific or stronger model.

## How to work with each group

**gemini_ask / gemini_research.** Gemini runs read-only. Give it what it needs:
- the exact files, not "the project" or a folder. The server puts the text of each
  file up to 20 000 characters into the prompt, about 22 000 characters in all. Gemini
  can't open folders or bigger files itself, because headless agy can't get approval to
  read them. Split bigger reviews into several calls;
- the question, and what a good answer contains.

Treat its answer as one opinion. Check its claims against the code before you
repeat them, and say plainly where you and Gemini disagree. Keep the returned
`conversation_id` for follow-up questions.

**gemini_code.** It changes files in `folder`, so:
1. Tell the user before you call it.
2. Write the task with a clear finish line ("all tests pass").
3. Afterwards, read `git diff` and run the tests yourself.
4. Report what changed. Never report Gemini's own summary as verified.

If the user named an Antigravity agent, call `gemini_agents` first and pass its
name as `agent`.

With Antigravity CLI 1.5, headless agy can't get approval to read or write files.
gemini_code then returns agy's explanation ("a tool required the read_file
permission...") and changes nothing. When that happens:
- Don't retry.
- Tell the user.
- Make the change yourself, or offer Jules (`jules_start`) for a GitHub repository.

**Jules.**
- Get the exact repo name from `jules_sources`.
- Jules can push a branch and open a PR, so confirm the task with the user before
  `jules_start`.
- For anything non-trivial, use `require_plan_approval=True` and show the plan
  (`jules_status`) before `jules_approve_plan`.
- Jules works asynchronously. Report the session link instead of waiting in a loop.

**Notebooks.** `notebook_ask` answers only from the notebook's sources. If the
answer has to come from the user's documents, use it rather than `gemini_ask`.
Audio and Video Overviews take several minutes. Pass a large `wait_seconds` and tell
the user where the downloaded file landed.

**Paid media (`video_generate`, `video_edit`, `image_generate`).** These are billed
to the user's Google Cloud project. Settle the prompt, aspect ratio and resolution
before you call them. Never retry a paid call just to "try again": each call is
charged. Afterwards, report the file path and the cost.

**Flow and browser tools (`flow_*`, `notebook_*`, `gemini_app`, `google_*`).** These
are experimental. They drive a Chrome profile that the user signed in to.
- The plugin's own server never has them. They come from the full server, which the
  user adds with `uvx gemini-pro-mcp setup --client claude --browser`, followed once
  by `uvx --from "gemini-pro-mcp[flow]" gemini-pro-mcp flow-login`.
- If the tools are missing, say so and give those two commands.
- If the tools fail because the user is signed out, point to the `flow-login` command.
- Never type the user's password.

## When something is missing

If the gemini-pro tools are not available yet and the server is still connecting,
it is probably starting for the first time. The first start downloads and installs
it, which takes a minute or two; later starts take a few seconds. Tell the user, and
ask them to try again shortly. Don't fall back to other tools or answer from
memory instead.

Otherwise, run `uvx gemini-pro-mcp doctor`. It shows what is set up and how to fix the rest:
- the Antigravity CLI sign-in;
- `JULES_API_KEY`;
- `GEMINI_API_KEY`;
- the Chrome profile.

API keys belong in the user's environment or in `~/.config/gemini-pro-mcp/.env`.
Never ask the user to paste a key into the chat.

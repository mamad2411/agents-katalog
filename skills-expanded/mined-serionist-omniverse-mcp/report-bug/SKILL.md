---
name: report-bug
description: >-
  Use when an Omniverse MCP tool does something wrong: an error its arguments don't explain, an answer the stage
  contradicts, a success that changed nothing, a call that hangs or times out; or when the user says a tool, the
  server or the Kit extension is broken, or asks to report a bug in Omniverse MCP. Asks the user first whether to file
  a report with the GitHub CLI, draft one for them to post, or drop it; then gathers the versions, the call and Kit's
  log with read-only tools, looks for the same issue, and drafts the report on the repository's bug form.
allowed-tools: >-
  mcp__plugin_omniverse-mcp_omniverse__get_sim_state mcp__plugin_omniverse-mcp_omniverse__get_logs
---

# Report a bug

A report the maintainer can reproduce at once names the versions, the exact call, what came back, and Kit's log
around it. This skill asks the user how to report first, then gathers those and drafts the issue on the repository's
[bug form](https://github.com/serionist/omniverse-mcp/issues/new?template=bug_report.yml). An issue is public, posted
under the user's GitHub account, and logs can name their folders and scenes: nothing is posted without their yes.

## Steps

1. **Check it is a bug of this repository.** Not one: a path or prim that isn't there, a value out of range, an error
   in `execute_script` code of your own, a Kit app or extension that isn't running (the `setup` skill). One: an error
   the arguments don't explain, an answer the stage contradicts (a capture, `get_prim_properties`), a success that
   changed nothing, a call that hangs or times out. A security hole, as
   [What counts](https://github.com/serionist/omniverse-mcp/blob/main/SECURITY.md#what-counts) lists them (a way past
   the bridge token, a file written outside what was asked, a secret in Kit's log), is never an issue: give the user
   the [private report](https://github.com/serionist/omniverse-mcp/security/advisories/new) and stop.
2. **Ask first,** before gathering anything the conversation doesn't hold. Say in a sentence or two what went wrong,
   that it looks like a bug in omniverse-mcp, and let the user choose (a user who asked for a report chooses a or b):
   - **a. You file it.** This needs the GitHub CLI, `gh`, installed and signed in: run `gh auth status`. Missing, say
     so and how to fix it (install it from https://cli.github.com, then `gh auth login`), or offer b instead. The
     issue is public, under their account, and posted only on their yes to the draft.
   - **b. They post it.** You write the draft to a Markdown file they name, or here in the chat, with the bug form's
     link; they review it and post it themselves. You post nothing.
   - **c. No report.** Drop it, go back to their task, and don't ask again about this bug in this session.
3. **Gather the details,** for a or b:
   - `get_sim_state`: `kit_app`, `kit_version` and `kit_os`, the Kit app and its version, Kit's version and the OS
     Kit runs on; `server_version` and `extension_version`. A `note` line means the two versions differ, which is
     often the cause: the `setup` skill matches them; report only if the bug outlasts that.
   - `get_logs(min_level="warn")`: keep the lines around the failing call. A long answer is written to a file: open
     it. When Kit hangs this fails too; the report says so.
   - Any of `kit_app`, `kit_version` and `kit_os` that reads `unknown`, as an extension older than the server
     gives: ask the user (Help > About in the Kit app), unless they said.
   - The OS: Kit's is `kit_os`. Add this machine's only when it differs: Kit can run on another machine.
   - The client and its version (Claude Code: `claude --version`).
   - The call: the tool, its arguments exactly, its answer as it came, and the calls before it that set the stage up.
4. **Make it reproducible:** the fewest calls that show it, from a stage anyone has: `new_scene`, prims from
   `create_prim`, a robot from `create_robot`, an asset that ships with the app. When it needs the user's own scene,
   describe what in it matters (prim types, counts, units), not the scene. Call the failing tool once more if it only
   reads, to say whether it happens every time. Run any call that edits only on the user's yes, and `new_scene` never
   over their unsaved work: it discards the open stage.
5. **Look for it already filed,** when `gh` is signed in:
   `gh issue list --repo serionist/omniverse-mcp --state all --search "<tool> <two or three words>"`, and
   `gh issue view <n> --repo serionist/omniverse-mcp` for a likely match:
   - open, the same bug: the report becomes a comment there, with what is new (versions, steps, log);
   - closed as fixed: `gh release list --repo serionist/omniverse-mcp --limit 1` names the newest release. When it is
     newer than `server_version`, the [changelog](https://github.com/serionist/omniverse-mcp/blob/main/CHANGELOG.md)
     says whether it holds the fix; if it does, suggest
     [updating](https://github.com/serionist/omniverse-mcp/blob/main/plugin/README.md#updating) instead of a report.

   Without `gh`, tell the user to search the [issues](https://github.com/serionist/omniverse-mcp/issues) first.
6. **Take out what must not be public,** from every field: any token, key or password; the user's home folder, as
   `~`; their user name, as `<user>`; host names and IP addresses, as `<host>` (an error names Kit's machine when it
   runs on another); and any other path, scene or prim name they may not want shown, as `<path>`, or ask.
7. **Draft** a title, and the bug form's fields in its order:

   | Field | What goes in it |
   |---|---|
   | Kit app and version | `kit_app` (`kit_version`): `Isaac-Sim Python 6.2.0 (Kit 110.4.0+feature.386251.187cf21b.gl)` |
   | Operating system | `kit_os`, and this machine's when it differs |
   | MCP client and version | `Claude Code 2.1.0` |
   | Server version or commit | `server_version` |
   | Extension version | `extension_version` |
   | Steps to reproduce | the calls of step 4, numbered, each with its arguments; then what came back |
   | What you expected | and why: the tool's description, or what the stage shows |
   | Console log | the log lines of step 3 |
   | Before you submit | `- [X] Nothing above holds the bridge token, or any other key, token or password.` |

   The title says what goes wrong, as the closed bugs' do: "capture_viewport with camera_path computes its boxes from
   the viewport's own camera". Write the body as GitHub writes a filed form: for each field `### <Field>`, a blank
   line, then its value; the log inside a `text` code fence; `_No response_` for an empty one. For a, write it to
   `mcp_output/bug-report.md`; for b, to the file the user named, or into the chat.
8. **For a, show it and ask.** Say where it goes: a new issue, or a comment on step 5's open match, `#<n>`, which
   holds only what is new there, not the whole form. Show the title and the whole text, what step 6 took out, and
   that it is public under their GitHub account; their yes ticks the last box. Post only on a yes to this text, and
   show it again after any change. Then post it, and give the user the URL `gh` prints. No `--label`: setting one
   takes triage rights, and the maintainer adds `bug`. Keep backticks, `$` and `"` out of the title, which the shell
   would run or cut. When `gh` fails, a token without the right to write issues for one, say why, and go on as b.

   ```
   gh issue create --repo serionist/omniverse-mcp --title "<title>" --body-file mcp_output/bug-report.md
   gh issue comment <n> --repo serionist/omniverse-mcp --body-file mcp_output/bug-report.md
   ```

9. **For b, hand it over:** the file's path, or the draft in the chat; what step 6 took out; and the form,
   https://github.com/serionist/omniverse-mcp/issues/new?template=bug_report.yml, or step 5's open match to comment
   on. Each `### <Field>` section goes into the form's box of that name, the title into its title; the user ticks
   the last box and submits.

## Done means

- a: the user has the issue's or the comment's URL; or they said no to the draft, and nothing was posted.
- b: the user has the draft and the form's link, and nothing was posted.
- c: nothing was gathered or posted, and the bug isn't raised again this session.
- No draft holds a token, a key or a password, or a path or name the user didn't agree to show.

## Never

- Gather the details before the user chose a or b.
- Post, comment or open anything on GitHub without the user's yes to the exact text; in b, anything at all.
- Open a `bridge-<port>.token` file, or put the bridge token, `OMNIVERSE_MCP_TOKEN` or any other secret in a draft.
- File a security hole as an issue, or as a comment on one: it goes through the private report.
- Run `execute_script` to gather details, or change the user's stage without their yes.

---
name: setup-maple-agent-loop
description: Connect a coding agent to Maple's MCP server and Stop hook so it can read, wait for and resolve visual review comments, and verify the connection. Use when adding `@maple-kit/mcp` to `.mcp.json`, wiring `maple-stop-hook`, or working out why an agent cannot see Maple comments or stops while they are still open.
---

# Connect an agent to Maple

Maple's agent half is one MCP server and one Claude Code Stop hook, both in
`@maple-kit/mcp`. The server lets the agent read and resolve comments; the hook
stops it calling itself finished while comments are open. This file is the
wiring. `docs/agent-loop.md` is the design, and the `maple-review` skill is how
to act on the comments once they arrive. Every `docs/` and `packages/` path
here is in the Maple repository, at <https://github.com/maple-kit/maple>.

Throughout, `acme/web` is the repository and `web-482` the branch under review.
Substitute your own.

## 1. Know the two binaries

| Bin               | What it is                                                 |
| ----------------- | ---------------------------------------------------------- |
| `maple-mcp`       | The stdio MCP server. Takes no arguments; reads the env.   |
| `maple-stop-hook` | Reads Claude Code's hook payload on stdin, answers stdout. |

Both need Node 24 or later. Run them with
`npx -y -p @maple-kit/mcp <bin>`; the package name is not a bin, so
`npx @maple-kit/mcp` alone does not work.

## 2. Pick the token, and how the gate moves

**`GITHUB_TOKEN`** is what reads and writes the comments. Maple keeps them in a
pull-request conversation comment, so the token needs `Pull requests: Read and
write` on the repository (a fine-grained token; `Metadata: Read` comes with
it). Read-only is enough to list, but `resolve_comment` rewrites that comment
and fails without write.

**`MAPLE_URL`** is optional, and it is how the check moves on a resolve. Set it
to the mount URL of a deployed Maple route whose host turned on `gateRefresh`
(the `setup-maple-org` skill), usually the preview under review:
`https://web-482.preview.acme.dev/api/maple`. `resolve_comment` then asks that
route to republish `maple/visual-review`, sending the branch and
`GITHUB_TOKEN`. That token needs push access to the repository for the route to
act on it. No gate credential is ever on this machine; `docs/github-auth.md`
says why. Skip it and the check updates on the next push instead.

**`MAPLE_GATE_TOKEN`** is for CI only: the gate App's own installation token,
never `GITHUB_TOKEN`, and it expires an hour after it is minted. Do not set it
next to `MAPLE_URL`; the server refuses to start with both.

Neither token goes in a file. Export them into the shell that starts the
client, for example with `op run --env-file .env -- claude`, and reference
them from `.mcp.json` with `${VAR}`.

## 3. Add the server to `.mcp.json`

**With the Maple Claude Code plugin installed, skip this section and the
next.** The plugin runs the server and the Stop hook, and both read
`GITHUB_TOKEN`, `MAPLE_GITHUB_OWNER` and `MAPLE_GITHUB_REPO` from the
environment Claude Code starts in, so export all three there, and `MAPLE_URL`
too for the server to refresh the gate. Go to section 5.

```json
{
  "mcpServers": {
    "maple": {
      "command": "npx",
      "args": ["-y", "-p", "@maple-kit/mcp", "maple-mcp"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}",
        "MAPLE_GITHUB_OWNER": "acme",
        "MAPLE_GITHUB_REPO": "web"
      }
    }
  }
}
```

What the server reads, from `packages/mcp/src/config.ts`:

| Variable                 | Required | Notes                                                                                                           |
| ------------------------ | -------- | --------------------------------------------------------------------------------------------------------------- |
| `GITHUB_TOKEN`           | yes      | Section 2.                                                                                                      |
| `MAPLE_GITHUB_OWNER`     | yes      | Organisation or user.                                                                                           |
| `MAPLE_GITHUB_REPO`      | yes      | Repository name.                                                                                                |
| `MAPLE_STORE`            | no       | `github` when a forge variable is set, else `file`, the comments under `.maple/`. Anything else fails.          |
| `MAPLE_GITHUB_API`       | no       | API base URL, for GitHub Enterprise Server.                                                                     |
| `MAPLE_URL`              | no       | Section 2. The route's mount URL. Unset means no gate refresh on resolve.                                       |
| `MAPLE_GATE_TOKEN`       | no       | Section 2. CI only; not with `MAPLE_URL`.                                                                       |
| `MAPLE_GATE_APP_ID`      | no       | The gate App's id. Only read when `MAPLE_GATE_TOKEN` is set.                                                    |
| `MAPLE_REQUIRE_APPROVAL` | no       | With `MAPLE_GATE_TOKEN`, exactly `true` to hold for an approval. The route's own setting wins with `MAPLE_URL`. |

A missing required value makes the server exit at startup, so the client shows
it as a failed server rather than a tool error.

`MAPLE_BRANCH` is **not** read by the server. Every tool takes the branch as an
argument instead:

| Tool                  | Arguments                         | Returns                                                         |
| --------------------- | --------------------------------- | --------------------------------------------------------------- |
| `list_comments`       | `branch`, `statuses?`             | Every comment on the branch, newest first, filtered by status.  |
| `wait_for_comments`   | `branch`, `cursor?`, `timeoutMs?` | `{ status: "comments" \| "timeout", cursor, comments }`         |
| `get_comment_context` | `id`, `branch`                    | The comment, its anchor rungs, its conditions, any mock replay. |
| `resolve_comment`     | `id`, `sha`, `note?`              | The updated comment. Refreshes the gate if configured.          |

`statuses` is any of `open`, `resolved`, `needs_reverify`, `orphaned`.
`branch` is the pull request's **head branch name**, not its number.

## 4. Add the Stop hook

The plugin installs this already. Without it, in `.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "MAPLE_GITHUB_OWNER=acme MAPLE_GITHUB_REPO=web npx -y -p @maple-kit/mcp maple-stop-hook"
          }
        ]
      }
    ]
  }
}
```

**The hook does not get `.mcp.json`'s `env`.** It is a separate process that
inherits only Claude Code's own environment. It needs `GITHUB_TOKEN`,
`MAPLE_GITHUB_OWNER` and `MAPLE_GITHUB_REPO` there or in the command, as
above. `GITHUB_TOKEN` comes from the shell the client was started in
(section 2); never inline it. With neither `MAPLE_GITHUB_OWNER` nor
`MAPLE_GITHUB_REPO` set, the hook reads the local store instead: the comments
under `.maple/` for the checked-out branch. It lets every stop through where
there is no `.maple/` folder, none for the branch, or no repository.

The branch is `MAPLE_BRANCH` when it is set, and otherwise the branch checked
out in the session's working directory.

The hook blocks while any comment is `open` or `needs_reverify`, and hands the
agent a numbered list naming each comment's id, location and first line.
`resolved` and `orphaned` comments do not block. It blocks at most eight stops
in a row, counted per session, then lets the session end and says what is
still open. A stop that no block caused, such as the end of your next prompt,
starts the count again.

## 5. Verify

Do all four. The first two pass on a server that is pointed at the wrong
branch, because an unknown branch returns an empty list rather than an error.

1. Pick a pull request whose conversation has a Maple comment (one with a
   ` ```maple ` fence) and at least one open comment in it. Note its head
   branch.
2. Restart the client and confirm `maple` is listed as connected with five
   tools (`/mcp` in Claude Code).
3. Ask the agent to call `list_comments` with that branch and
   `statuses: ["open"]`. It should return the comments you see in the fence,
   with matching ids. Then call `get_comment_context` with one `id` and the same
   `branch`; it should return `anchors` and `conditions`.
4. Check the hook from a shell, on that branch, with the same environment the
   client has:

   ```sh
   echo '{}' | MAPLE_BRANCH=web-482 MAPLE_GITHUB_OWNER=acme MAPLE_GITHUB_REPO=web \
     npx -y -p @maple-kit/mcp maple-stop-hook
   ```

   It should print `{"decision":"block","reason":"1 Maple review comment(s) are still open…"}`.
   With nothing open it prints `{}`. Then end a turn in the client and watch it
   refuse to stop.

## Troubleshooting

**The agent stops although comments are open.** The hook failed or looked at
the wrong branch, and Claude Code treats a failing Stop hook as a non-blocking
error. Run step 4 by hand. A `… is not set` error means the hook's environment
is missing a variable (section 4). `{}` on a branch you know has open comments
with a forge means `MAPLE_GITHUB_OWNER` and `MAPLE_GITHUB_REPO` are both unset
in the hook's environment (it then reads `.maple/`), `MAPLE_BRANCH` is not the
head branch name, or the hook ran from a checkout on another branch.

**The agent keeps being sent back and cannot finish.** It gets eight tries in
a row, then the hook lets it stop. The count lives in a small file per session
under the system temp directory (`maple-stop-hook/`); if that directory cannot
be written, the hook fails and Claude Code lets the agent stop. Resolve or
reply to each comment, or interrupt the session and say what is left.

**`list_comments` returns `[]` on a pull request that has comments.** The
`branch` argument is wrong: a PR number, a preview hostname or a typo all
resolve to no pull request, which is an empty list, not an error. Pass the head
branch name exactly.

**`wait_for_comments` returns `{ "status": "timeout" }`.** That is a result,
not a failure. The wait is clamped to 55 seconds (1 s minimum, 30 s default) to
stay under every client's 60-second tool ceiling. Call it again with the
returned `cursor`; omit `cursor` only on the first call, to drain what is
already there.

**Server fails to start: `… is not set; Maple's MCP server cannot start
without it.`** A required variable from section 3 is missing or empty. Claude
Code passes a `${VAR}` with no default through literally when the client's
shell lacks it, so the server starts with the placeholder as the value and
fails later against GitHub; `${VAR:-}` expands to empty and fails here instead.

**`resolve_comment` fails with a 403 or 404.** `GITHUB_TOKEN` lacks `Pull
requests: Read and write`, or cannot see the repository. GitHub answers 404 for
a repository a token cannot see.

**Resolves succeed but `maple/visual-review` does not move.** A gate refresh
never fails a resolve; it writes the reason to the server's stderr, which the
client keeps in its MCP log. With `MAPLE_URL` set, the line names the route's
answer: `403` means `GITHUB_TOKEN` cannot push to the repository, `401` that
GitHub did not accept it, and `404` that `MAPLE_URL` is not the route's mount
URL or its host has not turned on `gateRefresh`. With `MAPLE_GATE_TOKEN`, a
`401` is the token's hour running out; use `MAPLE_URL` instead. A 403 on the
check run usually means `MAPLE_GATE_APP_ID` is missing; `docs/gate.md` has that
case.

**Server fails to start: `MAPLE_URL and MAPLE_GATE_TOKEN are both set`.**
Remove `MAPLE_GATE_TOKEN` from the agent's environment; it belongs in CI.

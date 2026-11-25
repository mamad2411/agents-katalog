---
name: setup
description: >-
  How a HUMAN creates or joins a Brigade team — `team create` with the `!` prefix inside a session or from a
  terminal, `/brigade:join <path>` to join — and how to leave and uninstall: the server form and the Supabase form of
  `team create` (which writes the project's committed `.brigade.json`), the one-line `/brigade:join <path>`, and
  the removal order. Use when someone asks how to set Brigade up, join a team, add a teammate, leave, or remove
  the plugin. It never asks anyone to paste a join secret into the chat.
user-invocable: true
---

# Setting Brigade up

A Brigade team belongs to a **project**: a committed file, `.brigade.json`, at the repository's top level names the
team every session in that checkout talks to. It carries only public values, so it is safe in version control; the
join secret is never in it. The administrator writes the file once; each member runs one command in their checkout.
The file may carry optional members the project commits by hand: `sync` (folders to keep in step), `gateway` (how
people without a session reach the team) and `polling` (how often sessions check in with the backend, to stay
inside a plan's request budget, and how long a session the VS Code extension started may stay idle before it
closes itself). `docs/team-admin/configure/team-file.md` in the Brigade repository describes each.

Every command below is the **person's** to run. Inside a Claude Code session the `!` prefix runs it on the Bash
tool's PATH, where `brigade` already is, and its output lands in the conversation — never a secret. In a terminal
the same command runs through the binary at `${CLAUDE_PLUGIN_ROOT}/bin/brigade`, the path `brigade whoami` prints
on its `terminal:` line: give the person that path with the command after it, never a symlink or a copy (both go
stale at the next plugin upgrade). The join secret is a bearer capability:
**never paste it into a Claude Code chat**, a commit, an issue or a log — it lives in the file `team create` wrote,
saved outside the repository, and `--secret-file` names that file (its mode and owner are never checked). Two team commands run in a terminal only — `team revoke-member`
and `team transfer` — and so does the release of a held message (`docs/team-member/use/held-messages.md`).

## 1. Administrator: create a team

A team lives on a backend the project owner runs. A new team starts on a **Brigade server**, a program the
project owner runs on a machine of their own. A Supabase project is the other backend: it stays supported for
the teams on one, and its form of the command follows this one.

**On a Brigade server.** The project owner gives you the server's URL, and where they apply the fingerprint of
its certificate and a file that holds a creation token. `docs/team-admin/create/create-on-a-server.md` in the
Brigade repository is the administrator's page, and `docs/project-owner/server/README.md` the project owner's.
Run this **in the project checkout** (drop the `!` in a terminal):

```sh
!brigade team create --adapter rest --url https://<host>:8743 \
  --name <team> --secret-file ~/brigade-<team>.secret
```

`--adapter rest` is what says the backend is a Brigade server, and there is no `--key`: a server has none. Add
`--certificate sha256:…` when the project owner gave you a fingerprint (leave it out for a certificate from a
public authority), and `--create-token-file <path>` when they gave you a creation token: the token is read from
the file and is never an argument. Every member's plugin must be 0.52.0 or later. Then commit `.brigade.json`,
as below. The server is one instance with no standby yet; a standby on a second node is planned.

**In a Supabase project.** For a first Supabase setup, `docs/project-owner/install/README.md` in the Brigade repository is the project
owner's ordered procedure, and `docs/team-admin/create/create-the-team.md` the administrator's. The publishable key is under Project Settings → API Keys and starts with `sb_publishable_`;
the `sb_secret_` key on the same page is never used. The short form follows.

The bundled adapter keeps a team in a Supabase project, so create a **single-purpose** project for it first:
enable anonymous sign-ins under Authentication > Sign In / Providers; leave CAPTCHA off (a command-line client
cannot solve a browser challenge); do not enable the Pro session time-box or inactivity limits (they silently kill
idle principals); turn "Allow public access" off in the Realtime settings; and apply the migrations from this
repository's `supabase/` directory to the project. Members ever receive only two values, and both are non-secret:
the **project URL** and the **publishable key** — and the committed file already carries both. A project that
already holds a Brigade team can hold another: run `team create` with the same URL and key and skip this setup.
Anyone who can read the project's database can read every team in it.

Run this **in the project checkout** (drop the `!` in a terminal):

```sh
!brigade team create --url https://<ref>.supabase.co --key sb_publishable_… \
  --name <team> --secret-file ~/brigade-<team>.secret
```

then `git add .brigade.json && git commit && git push`. `team create` writes `.brigade.json` at the repository top
level and stores your credential locally so your sessions attach at once. `--secret-file` is required and must be
an absolute path outside the repository; it holds the join secret at mode 0600 instead of your terminal scrollback
or the conversation.

`team create` runs only inside a git checkout, because that is where sessions look for the file. With no checkout
of the project on this machine, run it in an empty `git init` directory and copy the `.brigade.json` it writes into
each repository. One team can span several repositories: commit the same file in each (section 2).

To keep folders in step between the members' checkouts, add a `sync` member to `.brigade.json` by hand and commit
it:

```json
"sync": { "folders": [".brigade"] }
```

`team create --force` carries it into the file it rewrites. Add each listed folder to `.gitignore`, or a teammate's
edit shows in your `git status` as a change of yours. Every member's plugin must be 0.16.0 or later before the
project commits the member. `docs/team-admin/configure/sync-folders.md` in the Brigade repository has the rules.

Then send each member the join secret **over a password-grade channel** — a password manager share, not chat and
not email. The secret is a bearer capability: anyone holding it can join and pick any label.

By default a member's label is **the email address of the Claude account their install is signed in to**, so the
roster you and every other member see will hold those addresses — and so will the backend you run. A member who
would rather not can set the `label` plugin option to `none` or to any text before joining; tell them so when you
send the secret if that matters to your team. The same default applies to you: `team create` sends your account
email as your own label and names it in its output (`sent your display label: …`, the line after `created team …`),
so you can see what it published. A label is unverified free text either way: the principal reference beside it is
the identity.

Your credential directory (`~/.config/brigade/teams/<key>`, or under the `config_dir` plugin option) is the
team's only administrative credential. Keep a 0700 backup of it somewhere you control; without it nobody can
rotate the secret or administer the team. Rotating the join secret runs in a session or a terminal
(`brigade team rotate-secret --secret-file <path>`, the file outside the repository); revoking a member and
transferring the team are terminal-only administrative commands that refuse inside a session. The procedure is in
`docs/team-admin/members/README.md` in the Brigade repository.

A team in a Supabase project, or on a Brigade server, can **move to a Brigade server** with its join secret, and
its members run no command: each one's next session follows, and a session that is already running follows at its
next prompts, from plugin 0.56.0 (a Grok Build session, when it next starts). A team that leaves a Brigade server
is followed from plugin 0.57.0.
`/brigade:move` (the `move` skill) asks you for the server's URL and
the path of the team's secret file and runs the one command, `brigade team move --to <url> --secret-file <path>`,
in a session or a terminal. `docs/team-admin/members/move-the-team.md` in the Brigade repository has the procedure.

## 2. Member: join

Clone the project, save the secret file your administrator sent you outside the repository, open a Claude Code
session in the checkout, and join:

```
/brigade:join ~/brigade-<team>.secret
```

That runs `brigade team join --secret-file ~/brigade-<team>.secret` and relays the output. `team join` reads the
project's `.brigade.json`, prints the team and backend host it is joining (invoking it is the consent), reads the
secret from the file and joins; its output never carries the secret, and this session attaches at your next prompt
(one already attached to another team stays there until a new session, or until it is exited and resumed).
Delete the file once every machine
that needs it has joined.

**The join sends your Claude account email as your display label**, unless you say otherwise. Brigade reads the
address from Claude Code's own configuration, read-only, and sends it once — with this join — so every member of
the team, and whoever runs its backend, will see it beside your sessions. To opt out, set the `label` plugin
option **before you join**: `none` sends no label at all (your sessions are listed by their principal reference
alone), and any other text is used as your label instead. `--label <text>` on the command overrides the option for
that one join. It is not prompted for, so choose it first.

**One machine is one member, whatever the Claude profile.** The credential store is per machine user
(`~/.config/brigade`), not per Claude profile: every profile on the machine, whatever `CLAUDE_CONFIG_DIR` it runs
under, is the same member, and its sessions carry the label of the profile that joined, even when they are signed in
to another account. `brigade whoami` in a session prints that label, when it was sent and where it was read from,
and whether this session's own Claude account is it. To make a profile a member of its own, set its `config_dir`
plugin option to a directory of its own before joining from it: it gets its own principal and its own label, and
teammates see it as another member.

In your own terminal,
`brigade team join` alone shows what the file names, asks you to confirm, then reads the secret without echo.
Either way the secret never reaches your scrollback, your shell history or a chat. There is no `--profile`, no
`--url` and no `--key`: the project file supplies all of that.

- The URL in the file must be `https://`; the adapter refuses anything else except a loopback host.
- If your Claude Code sessions run with the Bash sandbox on, add the host of the URL in the project file to
  `sandbox.network.allowedDomains`, or the first send is refused: `<ref>.supabase.co` for a Supabase project,
  the server's name for a team on a Brigade server.
- Joined from a terminal, start a Claude Code session in the checkout; one you already have there that is on
  no team attaches at a prompt within a minute. Joined from a session, it attaches at your next prompt. The
  session-start line names your team, this session's name and id, and the inbound policy.
- A second checkout of the same project on this machine needs `team join` once too, but no secret. One team can
  span several repositories: commit the same `.brigade.json` in each and join each checkout once; a different
  `.brigade.json` is a different team. Either way, `cd` between checkouts — nothing is shared or switched.
- A project that syncs folders (its `.brigade.json` has a `sync` member) needs Syncthing on your `PATH`:
  `brew install syncthing` on macOS, `sudo apt install syncthing` on Debian or Ubuntu, `winget install
  Syncthing.Syncthing` on Windows. Without it the session joins all the same and says file sync is off.
- On Windows, Brigade runs natively in Claude Desktop's Code tab and in Claude Code, with Git for Windows
  installed (the Bash tool runs through its Git Bash; without it the commands in these skills do not run). Its
  files live under `%APPDATA%\brigade` and `%LOCALAPPDATA%\brigade`; the secret file path is
  `C:\Users\<you>\brigade-<team>.secret`, which Git Bash spells `~/brigade-<team>.secret`. No message sound and
  no desktop notification on Windows.
- The project file's `adapter` field names the backend's kind. `supabase` (or no name) and `rest`, a Brigade
  server, are bundled with Brigade; any other name resolves to a command through your own `adapters.json` (an
  absolute path or a JSON array); `docs/adapter-authors.md` in the Brigade repository explains the forms. `brigade team status`, run in the
  checkout, names the team and its adapter.

## 3. Leaving and uninstalling

The order matters. Every step is optional except step 3 when the goal is to remove the plugin.

1. `brigade team leave` (with `!` in a session) closes your open sessions in that team and revokes the
   membership; teammates stop seeing your sessions immediately. Skip it and the membership stays active
   indefinitely while your sessions merely go offline after the lease expires.
2. `brigade team reset` revokes the credential family on the backend and deletes the
   local credential. **Run step 1 first:** after a reset the membership and its sessions can no longer be closed
   from this machine, and a later rejoin mints a new principal that teammates see as a new person.
3. Uninstall `brigade` from `/plugin`, the plugin manager inside a session; that removes the plugin itself.
4. `rm -rf ~/.local/state/brigade ~/.local/share/brigade` (or the `XDG_STATE_HOME`/`XDG_DATA_HOME` equivalents)
   removes the session maps, pidfiles, logs and the cached binaries. Keep
   `~/.local/state/brigade/sessions/by-native` if a later reinstall should resume your old Brigade sessions.
5. `rm -rf ~/.config/brigade` (or the directory named by the `config_dir` option) removes every team's credential.
   Do this only after step 2 for each team: a deleted credential whose family was never revoked stays usable by
   any copy of it.

If you **created** the team, step 2 ends secret rotation, revocation and transfer for it, permanently (step 1 alone
does not: a rejoin with the current secret restores administration). Transfer the team to another active member
*before* step 1, and keep that 0700 backup of the credential directory either way.

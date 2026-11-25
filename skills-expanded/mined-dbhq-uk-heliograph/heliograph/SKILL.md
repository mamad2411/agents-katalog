---
name: heliograph
description: Debug and change a machine you cannot log into, through an operator who cannot debug it, by driving the heliograph CLI - git as the transport in both directions. Plants the station, configures the estate, publishes steps, and reads the pushed logs. Use when the user cannot reach a machine themselves (no access, air-gapped, or only an operator can get on it), needs something an operator can run there, or is stuck relaying pasted output, and when the user says "heliograph". Not for machines you can SSH into yourself.
---

# heliograph

Someone can reach the machine. You cannot, and you are the one who knows what
to ask it. heliograph runs that gap as a loop instead of a relay: a transport
carries the step out and the log back, and the operator types one command that
never changes.

```
you        heliograph send <step> ────────────────────▶ transport
station    picks it up within seconds, runs ./run.sh
           pushes station/status, then the log ───────▶ transport
you        heliograph watch / logs --last --gaps ◀─────
```

Every captured line carries a UTC timestamp, ANSI is stripped, obvious secrets
are masked, and the log comes back **whether the run passed or failed**.

## When this applies

- The machine is in an environment you have no interactive access to.
- The only person who can reach it has other work to do and should not be your terminal.
- Several rounds of "run this and paste the output" have already gone badly.
- The repo that has to *change* is also on the far side (see the last part
  of [references/method.md](references/method.md)).

If you can SSH in yourself, do that instead and do not use this skill.

## This skill drives the CLI

Everything below goes through the `heliograph` binary. It is a single static
Go binary, it holds the gates in one place, and `heliograph bootstrap` plants
the exact station payload the binary was built with. Check for it first:

```bash
command -v heliograph >/dev/null || echo "MISSING"
```

**If it is missing, install it and do not improvise around it.** This picks
the release binary for this OS and CPU, checks it against the release's
`SHA256SUMS`, and installs nothing if the two disagree:

```bash
(
  set -eu
  case "$(uname -s)" in
    Linux) os=linux ext="" ;;
    Darwin) os=darwin ext="" ;;
    MINGW* | MSYS* | CYGWIN*) os=windows ext=.exe ;;
    *) echo "no release binary for $(uname -s): use go install" >&2; exit 1 ;;
  esac
  case "$(uname -m)" in
    x86_64 | amd64) arch=amd64 ;;
    arm64 | aarch64) arch=arm64 ;;
    *) echo "no release binary for $(uname -m): use go install" >&2; exit 1 ;;
  esac
  asset="heliograph-$os-$arch$ext"
  url="https://github.com/heliograph-io/heliograph/releases/latest/download"
  tmp="$(mktemp -d)"
  trap 'rm -rf "$tmp"' EXIT
  curl -fsSL "$url/$asset" -o "$tmp/$asset"
  curl -fsSL "$url/SHA256SUMS" -o "$tmp/SHA256SUMS"
  want="$(awk -v f="$asset" '$2 == f { print $1 }' "$tmp/SHA256SUMS")"
  got="$( (sha256sum "$tmp/$asset" 2>/dev/null || shasum -a 256 "$tmp/$asset") | awk '{ print $1 }')"
  if [ -z "$want" ] || [ "$want" != "$got" ]; then
    echo "$asset does not match SHA256SUMS: not installed" >&2
    exit 1
  fi
  mkdir -p "$HOME/.local/bin"
  chmod +x "$tmp/$asset"
  mv "$tmp/$asset" "$HOME/.local/bin/heliograph$ext"
  echo "installed $asset as ~/.local/bin/heliograph$ext"
)
```

It installs into `~/.local/bin`, which needs no root. If `command -v
heliograph` still finds nothing, that directory is not on `PATH`: run
`export PATH="$HOME/.local/bin:$PATH"`. A checksum refusal is a finding, not
a hiccup: stop and say so rather than fetch the file another way. With no
release for the platform, or with Go to hand, build it instead:
`go install github.com/heliograph-io/heliograph/cmd/heliograph@latest`.

If you cannot install it (no network, no permission), stop and say so. The
no-CLI fallback is a procedure for a person, not for you: clone
[heliograph-io/heliograph](https://github.com/heliograph-io/heliograph) and run
`station/bootstrap.sh` by hand - the station is plain text and stands on its
own, and `--flavour powershell` plants the twin for a box with no bash. Do not reimplement `send`, `watch` or the gates by editing files: one
driver is the point.

**If `heliograph_*` MCP tools are loaded, use them instead of the CLI** for
what they cover: `heliograph_estates`, `heliograph_send`, `heliograph_status`,
`heliograph_wait`, `heliograph_cancel`, `heliograph_stop`, `heliograph_logs`,
`heliograph_read_log`, `heliograph_gaps` and `heliograph_doctor`. They build
the same requests and apply the same gates. `heliograph_wait` is the tool form
of a bounded `watch`: pass the id `heliograph_send` returned and a
`max_seconds` under your own tool-call limit, and call it again if it returns
before the run ends. Bootstrap, `init`, `plant`, `trust` and everything else
are CLI only.

**What the far side needs depends on choices you make here**, so tell the
operator before they start, not after the station refuses:

- **Always:** bash 4 or newer, plus the tool the transport talks through - git
  by default, curl for the relay, curl and openssl for the object store. GNU
  coreutils are not required. A busybox `sed` has no `-u`: the preflight
  warns, timestamps are unaffected, and a cancelled run loses its partial log.
- **`heliograph-seal`, one compiled binary placed beside the station**, for
  either of two choices: the **relay** transport (it encrypts and signs every
  message), or a **trusted set** started with `heliograph trust init` (it
  verifies the Ed25519 signatures). A bash station configured for either
  refuses to start without it rather than run unverified. `plant` for a
  relay estate and `trust init` both print the operator's steps with it, and
  its checksum is published with each release. The PowerShell station needs
  no binary for either, because its seal ships as source.

`station/FAR-SIDE-BINARIES` is the whole list of compiled things a station may
need. Git, the file share, the bundle and the object store, with no trusted
set, need no binary at all.

## 1. Set up

```bash
heliograph bootstrap ~/transport/payments     # plant the station payload
cd ~/transport/payments && git init && git add -A && git commit -m 'heliograph: transport repo'
# add a PRIVATE remote and push main, then cut the investigation's branch and
# push that too, BEFORE planting: the station runs on the branch it is given
git checkout -b task/<slug> && git push -u origin task/<slug>
heliograph init payments --dir ~/transport/payments
heliograph doctor                             # will this work from here
heliograph plant                              # the message to send the operator
```

**The station reads one branch: the one it was started on.** `plant` run on
`task/<slug>` tells the operator to check that branch out. A request on any
other branch is never picked up, so `heliograph send` refuses to publish where
the status names a different branch, and names both. `doctor` fails on the same
thing and `watch` warns. A branch cut from another carries that branch's
status until a station starts on it; a station publishes its own as soon as it
starts.

**The transport repo must be private, and must be its own repo.** Captured
logs are committed to it, so everything the operator's commands print lands in
that history permanently. Never bootstrap into a repo that holds anything
else, and never into a public one. Re-running `bootstrap` over an existing
transport repo is safe: it installs what is missing and leaves what is there
alone.

`plant` prints the operator's whole job: clone, `./start.sh`, walk away. It
carries no credential, deliberately. If the loop is to run unattended, decide
the credential now - a forwarded ssh agent key dies with the session; an
unattended loop needs a key on disk, a deploy key, or a token in
`~/.git-token`. See <https://docs.heliograph.io/service.md>.

Git is the default. A mounted file share, a signed bundle for a true air gap,
an S3-compatible object store and the relay are all available at `init`, and
the loop is identical whichever you pick. Which flags each needs is on the
site, next to the binary that implements them:
<https://docs.heliograph.io/transports>.

## 2. Baseline before theorising

```bash
heliograph send env
heliograph watch --timeout 8m
```

`env` answers what that box actually is: OS, tools, sudo, proxy, DNS, cloud
auth, and which commit is checked out. It is the right first step of any
investigation, whatever it turns out to be about. A prior finding is a
hypothesis to re-test, never a premise to build on.

## 3. Start a task

Steps live in the transport repo, one file per question:

1. Work on the `task/<slug>` branch from set-up. A later investigation is a
   new branch: cut it, push it, and have the operator restart the station on
   it (`heliograph plant` prints the commands) before you send anything
2. Fill in `TASK.md`: the question, what is known, what would settle it. It is
   what stops the steps becoming a fishing trip
3. `cp steps/_template.sh steps/<name>.sh`, write the probes
4. No registration needed: `heliograph send steps/<name>.sh` sends it by
   path. Register it in the `case` table in `run.sh` (and the step-list
   comment above it, so `--list` stays honest) only to give it a short name.
   A name the station does not know is refused as `unknown step`
5. `git add` and `git commit`. No manual push needed: `heliograph send`
   rebases onto the remote and pushes `HEAD`, so your commits and the request
   travel together

**`main` is the template; `task/<slug>` is one investigation.** Task branches
are not merged back. Only genuinely generic tooling returns to `main` via a
normal PR, stripped of anything task-specific.

Writing the step itself: [references/steps.md](references/steps.md). Read it
before the first one. Every rule in it cost a round trip.

## 4. Drive it

```bash
heliograph send net-probe HOSTS="sql01 sql02"   # publish a request, and return
heliograph watch --timeout 8m                   # follow it, for 8 minutes at most
heliograph status                               # what the station is doing now
heliograph logs --last                          # the whole log
heliograph logs --last --gaps                   # where it stalled
heliograph cancel                               # kill the running step
heliograph stop                                 # end the station's loop after this run
```

Everything after the step name is environment, passed verbatim; values with
spaces are re-quoted on the way out. With more than one estate configured,
every command needs `-e <estate>`: a request to the wrong estate runs a
command on the wrong machine, and that is not recoverable by apologising.

`watch` waits for the request `send` just published, not for whatever the
station finishes next. Until the station reads it, `watch` and `status` say
`not picked up yet`: the status on the far side still describes the previous
run, so never read that run's result, or its refusal, as this one's.
`heliograph watch <id> --timeout 8m` follows a named request instead.

**Always bound `watch`.** Without `--timeout` it waits indefinitely, and your
own shell call has a time limit: when that kills it, you lose track of the
request. Keep the timeout under that limit. A timeout stops the watch, not the
run: `watch` exits non-zero and says the run continues, and running it again
picks the same request back up.

What the CLI already handles, so do not do it by hand: the `git pull --rebase`
discipline (two writers share the branch, and the station pushes far more
often than you do), inventing request ids, and the timestamp arithmetic.

The trigger is the **id**, not a new commit, so docs and step edits never fire
runs nobody asked for. The station holds **one request, not a queue**. A new
`send` while a step runs does not cancel it: the new request runs when that
step ends. But a second `send` before the station has read the first replaces
it, and the first never runs - `send` names the request it replaced when that
happens. Send the next once `watch` shows the last one picked up.

`heliograph cancel` kills the running step: the station signals it at its next
poll and publishes `cancelled`, with the log as far as it got. `cancel <id>`
kills only that run. It needs git or a file share, whose station reads the
request while a step runs; on any other transport it refuses, because the
cancel would arrive after the step had finished. It stops only a running step:
a request the station has not picked up still runs. It sets `cancel:` on the
request already in `station/request` and keeps its id, so a request queued
behind the step is kept, and runs next. Do not edit that file yourself.

`heliograph stop` ends the loop once the current run is over, which matters
because nobody is sitting at that terminal. It works on every transport. Only
the operator can start the station again, and a station that reads the stop
again stops again: send the next step before they restart it.

**The gates. The loop is read-only by default.** Every step declares itself in
its own file - `# heliograph-mode: read-only` or `action` - and a step that
declares neither does not run. A state-changing step needs `CONFIRM=yes` in
the request's env **and** the station must have been started with
`--allow-actions`, or the refusal is published to `station/status` within one
poll. The loop refuses to run as root. These gates live in the station and the
CLI; never work around them.

### What binds a request: mode, expiry and who may send it

A request carries more than a step name, and the station checks it before
the gates above. Three things are yours to set, and a refusal says which one
failed:

- **`--mode`.** Pass the mode the step declares, and always for an action:
  `heliograph send steps/fix-dns.sh --mode action CONFIRM=yes`. The station
  then refuses the request if the step file changed to the other mode after
  you wrote it. That refusal means the step is not what you reviewed: read it
  again before you resend.
- **`--expires`.** A request is valid for 24 hours by default, and a station
  that reads it later refuses it as expired. `--allow-actions` and
  `CONFIRM=yes` were decided when it was sent, so the limit stops an old
  request running again. Pass `--expires 0` (never) only when the station will
  be planted days after the request is written, or a length such as
  `--expires 72h` when you know the delay. After an expiry refusal, send the
  request again.
- **A trusted set.** Without one, a station accepts whatever its transport
  verifies, and `heliograph doctor` says "no trusted set on either side". A
  set names the keys that may command the station and is published in its
  status, so a colleague can be revoked without a visit to the machine, and
  on the relay the log records who asked. When more than one person will
  command a station, run `heliograph trust init` once and give the operator
  the lines it prints. A bash station then needs `heliograph-seal`.

Detail: <https://docs.heliograph.io/security> and
<https://docs.heliograph.io/cli>.

A long run is not a black box: the partial log is pushed every 60 seconds with
a line count and the last real line, so `heliograph status` shows where it has
got to. The finished log lands in `ops-logs/` in the transport repo, committed
and pushed - that is how a run escapes a machine nobody can reach.

While a station is running, **say so and wait for the log**. Ask the operator
only for what the transport cannot carry: an interactive cloud login, a
decision, or a fact only they have.

### When git is not the transport that works

Two cases live in the station payload rather than the CLI today, and for
these two you drive the station's own script in the transport repo - not
because two drivers are fine, but because the CLI has no transport for them
yet:

- **The control node cannot reach git at all.** `./drop.sh send <id> <step>`
  and `./drop.sh watch <id>` carry the same contract over Azure Blob Storage;
  neither side ever reaches the other. Measure before reaching for it - see
  <https://docs.heliograph.io/flare.md>.
- **You can reach the station directly.** An Azure Function App inside the
  VNet with a public HTTPS endpoint makes storage pointless indirection:
  `./intercom.sh run steps/<name>.sh K=V`. Read
  <https://docs.heliograph.io/flare.md> before exposing it - the
  function key and IP allowlist become the real gates.

## 5. Read the log

- `heliograph logs --last --gaps` first. A gap is a finding: in an untimed
  log a hang and slow progress are indistinguishable. A log where every line
  carries the same timestamp is reported as an **error**, not as "no gaps".
- **Header block next**: branch, commit, host, user. A divergence between the
  commit you pushed and the one they ran explains a surprising share of "but
  I fixed that".
- `probe_summary` gives the tally, the footer gives the real exit code.
- **Read the whole log, including the parts that worked.** A passing probe
  beside a failing one is the control that tells you what the failure means.
- Record what was *measured* in `TASK.md`, separately from what you
  concluded. Measurements stay true; conclusions get revised.

**A green exit means the probes that ran passed, not that the work happened.**
Verify the outcome, not the exit code.

## Hard rules

These outrank convenience. Each one is here because breaking it cost a full
round trip or worse.

1. **Never truncate.** No `head`, no `tail -20`, no `2>/dev/null` on the
   thing being diagnosed. The line you cut is the one you needed.
2. **Measure, do not infer.** Say what a log showed, not what it implies.
3. **Keep a control.** A probe with nothing to compare against is an anecdote.
4. **Change one thing between runs.** Two changes and a different result
   tells you nothing.
5. **Read-only until earned.** A step changes state only when you can say
   precisely what it will do and why, and then it carries the `CONFIRM=yes`
   gate.
6. **Never commit task work to `main`.**
7. **Never ask the operator to hand-edit anything.** Deliver a change as a
   payload the step copies into place. An unlogged manual edit is exactly the
   divergence these logs exist to rule out.

The full method, and the mistakes behind each rule:
[references/method.md](references/method.md). Worth reading in full before a
hard investigation.

## Running the station in Azure, instead of on somebody's terminal

Sometimes there is no willing human to start `./start.sh` and leave it
running. The station payload's `azure/` runs it as Azure infrastructure
instead: Container Instances, Web App for Containers and a scheduled
Container Apps Job and a VM with a systemd unit are deployed and proven; a
Function App on Flex Consumption is written and validated, never deployed. All
bring-your-own-network, and the checkout is transient - git is the
persistence.

Two things that will waste your time if you do not know them: the published
image tag has no `v` (git tag `v0.4.3`, image
`ghcr.io/heliograph-io/heliograph-toolkit:0.4.3`), and a GitHub transport repo
needs `GIT_TOKEN_USER=x-access-token` or git reports a missing username
rather than a wrong one. Everything else:
<https://docs.heliograph.io/azure.md>.

## Secrets

Logs are committed and pushed, so anything a command prints is in history
permanently. `cap_redact` masks the obvious shapes and is a safety net, not a
guarantee. **Name secrets, never read them** - listing secret names settles
"does this exist here"; the value is never the question.

When a value has to travel the *other* way, `./secret.sh` in the transport
repo carries it as ciphertext with a passphrase defined by a human on both
machines and never committed. It is transport, not storage: the ciphertext is
in history forever. Details: [references/secrets.md](references/secrets.md).

## References

Near side, on the web, because it changes with the binary and one copy is
better than two:

| | |
|---|---|
| <https://docs.heliograph.io/cli> | every CLI command, and the reasoning behind the ones that are not obvious |
| <https://docs.heliograph.io/mcp> | the MCP tools, for driving this from an agent |
| <https://docs.heliograph.io/transports> | git, file share, bundle, object store, relay |

The far side is on the web too, for the same reason. The site is tested
against this repository, and a second copy here went stale beside it. Fetch
the `.md` form of a page rather than the HTML:

| | |
|---|---|
| <https://docs.heliograph.io/runner.md> | `start.sh`, `run.sh`, `station.sh`, `caprun.sh`, every `cap_*` and knob |
| <https://docs.heliograph.io/service.md> | making the loop outlive the session that started it, and the credential an unattended loop needs |
| <https://docs.heliograph.io/hosts.md> | every host, the contract it must meet, and which ones are actually proven |
| <https://docs.heliograph.io/containers.md> | running the station in a container: what ships, why, and the honest limits |
| <https://docs.heliograph.io/azure.md> | running the station in Azure, and what deploying it taught |
| <https://docs.heliograph.io/flare.md> | the HTTP flare, for when you can reach the station, and the Azure Blob beacon for when nothing can reach git |
| <https://docs.heliograph.io/windows.md> | a Windows station, steps written in PowerShell, and what line endings really do |

Here, offline, because they change how you work rather than describe the code,
and you need them in the middle of an investigation:

| | |
|---|---|
| [references/steps.md](references/steps.md) | writing a step, the helpers in `lib/`, and the traps that cost round trips |
| [references/method.md](references/method.md) | how to debug across a gap, and how to change a repo that is also on the far side. The expensive lessons |
| [references/secrets.md](references/secrets.md) | `secret.sh`, for a value that has to reach the far side |

---
name: funds-recovery
description: "funds-recovery — help somebody find the funds of a mnemonic with seed-scan, working on its public bundle alone and never on the mnemonic"
argument-hint: "[the bundle's path]"
---

# Finding the funds of a mnemonic

Help the human find what a mnemonic holds with `seed-scan` 2026.11.17,
the release tagged `v2026.11.17` in
[btclib-org/seed-scan](https://github.com/btclib-org/seed-scan) and
published on PyPI. The session works on the public bundle that
`seed-scan identify` writes, and on what the later commands write from
it: never on the mnemonic. Each command below is that release's, as its
`--help` gives it. Its [`README.md`][readme] and
[`SECURITY.md`][security] at that tag, named below as seed-scan's, say
what each command does, and what it cannot. $ARGUMENTS, where given, is
the bundle's path.

The release gives its dependencies a floor only, so each command below
runs it with `--exclude-newer 2026-11-16T23:16:00Z`: uv then resolves
every package as PyPI served it when the release was published. That
is the minute after the release's last file,
`seed_scan-2026.11.17.tar.gz`, reached PyPI, at the
`upload_time_iso_8601` that
<https://pypi.org/pypi/seed-scan/2026.11.17/json> gives it.

[readme]: https://github.com/btclib-org/seed-scan/blob/v2026.11.17/README.md
[security]: https://github.com/btclib-org/seed-scan/blob/v2026.11.17/SECURITY.md

Before its first command, the session reads
`$PROCESS/process/every-session.md` whole, two directories above this
skill's own, and what it writes follows that file's *Write plainly*. It
writes in no repository, so it needs no worktree and none of the roles
of `$PROCESS/process/every-role.md`.

## The secret stays out of the session

- **Never ask for a mnemonic, a passphrase or a private key**, nor for
  a part of one, a seed, a SLIP-0039 share or an extended private key.
  Never read a file that may hold one, never run `seed-scan identify`,
  and never write code that derives keys.
- **Where one is pasted anyway**, or reaches the session in a file or in
  a command's output, tell the user at once that it has reached this
  conversation and the model's provider, and that they should treat it
  as exposed. Do not repeat it, write it anywhere or run anything on it,
  and go on with the bundle alone. A private key of a single address
  exposes more than the address: with the bundle, it can give the keys
  of the whole account, as seed-scan's `README.md` says in *What touches
  the secret*.
- **No address leaves the machine but through `seed-scan`**, to the
  server and the node the user names; `uvx` fetches the pinned release
  and its dependencies from PyPI, which sends none. No explorer, no
  other API, no script of the session's own: what the pinned release
  does not read is a limit of the search (*The answer*), not a gap for
  the session to fill.

## The user runs identify

A bundle the user already has is used as it is. They run `identify`
where they have none, where they want a passphrase tried that they did
not type for that bundle, or where the report asks for a larger bound
(*The answer*). Each run writes a bundle of its own, from the empty
passphrase and those typed in that run, and each bundle is read as the
sections below say.

They run it in a terminal of their own, outside the session, never as a
command the session runs, on a machine they trust with the network off,
as seed-scan's `SECURITY.md` asks in *Limitations, not
vulnerabilities*. Give them the commands. The first, run before the
network goes off, puts the pinned release in uv's cache:

```shell
uvx --exclude-newer 2026-11-16T23:16:00Z seed-scan@2026.11.17 --help
```

The second runs, from the cache alone, the environment the first built:
`--offline` has uv fetch nothing, the same `--exclude-newer` gives the
same packages, and a `seed-scan` found earlier on the `PATH` is not
run. It asks for the mnemonic, then for passphrases until an empty one,
at hidden prompts, and writes the bundle. The shell empties the file it
writes to before uv starts, even where the run then fails, so each run
first makes a new file in the current directory, with the time in UTC
in its name, and prints its path:

```shell
bundle=$(mktemp "$PWD/bundle-$(date -u +%Y%m%dT%H%M%SZ)-XXXXXX") &&
  printf '%s\n' "$bundle" &&
  uvx --offline --exclude-newer 2026-11-16T23:16:00Z seed-scan@2026.11.17 \
  identify >| "$bundle"
```

Where they know an address the mnemonic gave, `--address` followed by
it has `identify` search for its path. `--accounts`, `--indexes` and
`--keys` set how much it writes and searches, and the release's
`identify --help` gives their defaults.

The bundle holds no secret, but whoever holds it can follow the
wallet's history and balance, as seed-scan's `README.md` says in *What
touches the secret*. Tell the user so before they hand it over: the
session and the model's provider then hold it. They hand it over by
giving its path.

## Read the bundle

Each command of the session takes the values it needs in the same call,
in an assignment block above its fence:

```shell
bundle=<the bundle's path>
```

```shell
uvx --exclude-newer 2026-11-16T23:16:00Z --from seed-scan==2026.11.17 \
  seed-scan report "${bundle:?}"
```

With no result beside it, the report lists what `identify` found: the
schemes that claim the words, a line per reading, what was not derived
and the address search, with every account not checked.

The session reads the bundle and the results through `seed-scan` alone,
never with a read of the file: a path given by mistake may name a file
that holds the secret. `report` refuses a file that is not a bundle, and
its refusal repeats nothing the file holds.

## Scan, and read the forks

Each bundle's results go in a directory of their own in the session's
scratchpad, so that a second bundle's results replace none of the
first's. This makes it, once per bundle, and prints its path:

```shell
scratchpad=<the session's scratchpad>
```

```shell
mkdir -p "${scratchpad:?}/funds-recovery" &&
  mktemp -d "${scratchpad:?}/funds-recovery/results-XXXXXX"
```

The commands below take it for that bundle:

```shell
results=<the directory made for the bundle>
```

Ask the user for the Electrum server and the EVM node to ask, and the
chain the node serves. Each learns every address it is asked about, so
there is no default and the session proposes none.

A hosted node's URL can hold an access key in its path or query.
seed-scan leaves those out of its result and report, but the command the
session runs holds the whole URL, and so does the conversation. Ask for
a URL that holds no key, as the user's own node or a proxy on their
machine that adds the key, and ask them not to paste one that does.
Where one is pasted anyway, the key is exposed as the secret is (*The
secret stays out of the session*). `scan` refuses a node URL that
carries a login, and takes the Electrum server as `host:port` alone,
with no path or query.

A proxy passes every address on to the node or Electrum server behind
it, which the report does not name. Its URL can read as the user's own
node's does: `http://127.0.0.1:8545` names either. So ask of each node
URL, and of each Electrum server, the one for `scan` and each one for
`forks`, whether it forwards to another service, whether or not the user
calls it a proxy. Where it does, ask which service, and run `scan` or
`forks` with it only once the user has named that service and agreed
that it learns every address. The answer names that service beside the
report.

```shell
server=<the Electrum server, as host:port>
node=<the EVM node's URL>
chain=<the chain the node serves>
```

Each chain's scan and report take a name of their own in the bundle's
results directory: the chain the node serves, `bitcoin` where the scan
asks a server and no node, and `forks` where the session skips the scan.

```shell
name=<the chain the node serves, bitcoin, or forks>
```

```shell
uvx --exclude-newer 2026-11-16T23:16:00Z --from seed-scan==2026.11.17 \
  seed-scan scan --server "${server:?}" \
  --node "${node:?}" --evm-chain "${chain:?}" "${bundle:?}" \
  > "${results:?}/scan-${name:?}.json"
```

Leave out `--server` where the user named no server, and `--node` with
`--evm-chain` where they named no node. Where they named neither,
`scan` refuses to run, so the session skips it. `--tcp` asks a server on
their own machine, and `--cafile` one whose certificate the system does
not trust. A run reads one node's chain, and a report reads one scan
result: a further chain is a scan and a report of its own. The help
lists the chains, and the bounds `--gap-limit` and `--account-gap`:

```shell
uvx --exclude-newer 2026-11-16T23:16:00Z --from seed-scan==2026.11.17 \
  seed-scan scan --help
```

A chain forked from Bitcoin is read with its own Electrum server, which
the user names too. The help lists the chains:

```shell
uvx --exclude-newer 2026-11-16T23:16:00Z --from seed-scan==2026.11.17 \
  seed-scan forks --help
```

```shell
fork=<a chain the help of forks lists>
server=<that chain's Electrum server, as host:port>
```

```shell
uvx --exclude-newer 2026-11-16T23:16:00Z --from seed-scan==2026.11.17 \
  seed-scan forks --chain "${fork:?}" --server "${server:?}" "${bundle:?}" \
  > "${results:?}/forks-${fork:?}.json"
```

A result counts only where its command exited `0`. One that exited
otherwise leaves its file empty, and the report refuses it: the session
leaves it out, and keeps what the command printed on standard error for
the answer.

Then the report, with `--forks` once per forks result that counts, and
with no `--scan` or `--forks` where none does:

```shell
uvx --exclude-newer 2026-11-16T23:16:00Z --from seed-scan==2026.11.17 \
  seed-scan report \
  --scan "${results:?}/scan-${name:?}.json" \
  --forks "${results:?}/forks-${fork:?}.json" \
  "${bundle:?}" > "${results:?}/report-${name:?}.txt"
```

The docstring of [`seed_scan.report`][report] at the tag gives the
report's layout.

[report]: https://github.com/btclib-org/seed-scan/blob/v2026.11.17/src/seed_scan/report.py

## The answer

Show the report as it is, in a code block, and give its path. Then say
in plain words what it found, and what the search did not reach, each
limit read from the report or from the pinned release's documents:

- each `not checked` and `not derived` line, with its reason;
- each `scan` or `forks` run left out for its exit, with its error:
  what it was to search stays unchecked, and a failed `forks` leaves no
  line in the report for its chain;
- each `cut short`, with the run it asks for: `identify` again in the
  user's terminal with the larger bound, then the commands after it;
- the `bounds` lines: an account or an address past those gaps was not
  read;
- a non-empty passphrase not typed at `identify` was not tried, since
  it tries the empty one and those typed: another is tried by a new run
  (*The user runs identify*);
- what the Electrum server and the EVM node are still trusted for, as
  seed-scan's `SECURITY.md` says in *Limitations, not vulnerabilities*.

"Nothing found" holds only inside those limits: never say the mnemonic
holds nothing. The report, like the bundle, lets whoever holds it follow
the wallet's history. The user's own wallet moves the funds; the session
signs nothing, and asks for no key to do it.

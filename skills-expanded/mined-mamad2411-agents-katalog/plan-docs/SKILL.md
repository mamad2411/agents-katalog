---
name: plan-docs
description: "Use when capturing an idea, drafting a design, or tracking work-in-progress in a repo's plans/ directory — creating or updating a plans/YYYY-MM-DD-topic.md file (including a bug, idea or risk turned up incidentally), asking what plans exist or what to work on next, here or across every repo, choosing or advancing a status, retiring a landed/abandoned plan once its content has a permanent home elsewhere, migrating a repo's legacy monolithic plan file (PLAN.md, DESIGN.md, ...) onto this convention, or auditing AGENTS.md/README.md/docs for planning/status/future-work content that has drifted in and belongs in plans/ instead. Also owns where a plan file may live and what may be written in it: a work, client or employer repo that cannot take a plans/ directory keeps its plans in the store outside every working tree ($PLANS_HOME), routed per repo by config; an idea with no repo yet is filed unscoped and graduated later; and no plan committed to a repo you publish may name a client, employer or internal project."
---

# Structured, stateful plan files

Convention for `plans/YYYY-MM-DD-topic.md` — one file per idea or design, a YAML frontmatter
`status` field so its lifecycle is visible without opening it, and a firm rule that `plans/` stays a
working set, not a permanent archive.

Rationale, prior art, and worked examples:
[`references/design-rationale.md`](references/design-rationale.md).

## Run the script, don't re-derive it

[`scripts/plans.py`](scripts/plans.py) (stdlib, read-only unless stated) owns every mechanical step
below: which directory a plan goes in, creating it with correct frontmatter, the status index, the
anchored tag greps, the promotion and deletion gates, inbound references. Run it instead of opening
files to work the answer out — the file reads are the expensive part, and each command below is one
of them.

**Write the path out in full on every call.** Shell variables do not survive between an agent's Bash
calls — only the working directory does — so a `P=…` assignment is empty by the next command and
every invocation below is the whole path:

```shell
python3 ~/.agents/skills/plan-docs/scripts/plans.py list
```

**Start here. These three answer most sessions**, and nothing below is needed until the lifecycle
reaches it:

| the question                             | the command                            |
| ---------------------------------------- | -------------------------------------- |
| **first call of a session, in any repo** | `absorb` — silent unless it applies    |
| what is open? what should I work on?     | `list` — see "Asking what is open"     |
| where does a new plan go, and write it   | `new <topic>`, or `new … --for <repo>` |
| is this machine set up, and how?         | `doctor`                               |

<details>
<summary>The rest, by the moment you need them</summary>

```shell
# writing one down
python3 <path> where                        # which directories this repo reads and writes
python3 <path> repos --search <words>       # what each repo is for, to route a plan by
python3 <path> new <topic> --for <repo>     # something belonging to a repo you are not in
python3 <path> new <topic> --unscoped       # an idea with no repo yet
python3 <path> graduate <file> --to <repo>  # …once it has one

# working on it
python3 <path> set-status <file> planned    # refuses if the gate for that status fails
python3 <path> tags --tag DEFERRED          # anchored, across every plan this repo can see
python3 <path> move <file> --to store       # a repo switching where it keeps plans

# retiring it, and getting it back
python3 <path> refs <file>                  # inbound references, before retiring
python3 <path> archive --search <words>     # a retired plan, back out of git history

# keeping the machine right
python3 <path> scan                         # no private name reaches a repo you publish
python3 <path> install --explain            # set the machine up, one decision at a time
```

</details>

Every command that reads takes `--json`, so nothing here has to be parsed out of its text output.

## Where a plan file goes

A plan normally lives in the repo it describes. That is unavailable in most employer and client
repos — a `plans/` directory is not yours to add there — so there are three routes, and which one a
repo uses is **configuration, never a judgement call made per session**:

| route     | plans live in                                         | for                                    |
| --------- | ----------------------------------------------------- | -------------------------------------- |
| **repo**  | `<repo>/plans/`, committed with the code              | a repo you own                         |
| **store** | `<the store for its tier>/<path under projects root>` | a repo that can't hold its own plans   |
| **both**  | reads both, writes one                                | a repo mid-switch, in either direction |

The store mirrors each repo's path at whatever depth it sits, so a `<root>/<project>/<repo>` clone
gets `<store>/<root>/<project>/<repo>` — no slug, no collision between two clients' `api`. The path
is computed from the repo root, not from the working directory.

### The store is two repositories, split by sensitivity

| tier          | holds                                           | remote                    |
| ------------- | ----------------------------------------------- | ------------------------- |
| **shareable** | `_unscoped/` and the roots in `shareable_roots` | allowed — usually private |
| **sensitive** | every other root: employer and client work      | **none**                  |

Both are ordinary git repositories with **full history**, so retirement, `archive` and the
commit-immediately rule work identically in either. Nothing about the plan format, the status
vocabulary or the tags changes with the tier.

**You never pick a tier.** A root's tier follows from `shareable_roots` (which defaults to
`public_roots`), and every command resolves it for you — `where` prints it, `new --for` prints it
and the exact `git -C` line to commit with, `archive` searches both. Read what the command tells you
rather than deriving the path.

**The split is structure, not the safety mechanism.** The risk is a client's name inside _any_ file,
not a file inside a client's directory — an unscoped idea or a plan for a personal repo can easily
name work that is not yours to disclose. So the shareable tier is gated on content, like any repo
you publish:

```shell
python3 <path> scan --mode history --path <the shareable store>   # before the FIRST push
python3 <path> scan --mode staged  --path <the shareable store>   # before each commit after that
```

Both exit non-zero on a hit. The tier boundary is only what keeps the whole of a client root off a
remote in the first place.

**`--mode tree` is not the pre-push gate, and using it as one is the mistake to avoid.** A push
ships **history**, not the working tree, and the two diverge exactly where it matters: a plan that
named a client, was reworded, and was committed again leaves a clean tree and a dirty history, and
the push publishes the history. Confirmed 2026-08-29 while wiring this store's own remote —
`--mode tree` was written into this section as the gate, and the first real push was the thing that
showed it was the wrong question.

The first push is the one moment history mode is cheap to act on: nothing is published, so a hit is
still an edit rather than a purge decision. After that, `--mode staged` on every commit is what
keeps history clean going forward, and `--mode history` becomes the periodic audit rather than a
gate.

**If you do rewrite, the scan keeps failing until you drop `refs/original/`.** `--mode history`
reads `git log --all -p`, and `git filter-branch` leaves the pre-rewrite refs under
`refs/original/`, which `--all` still walks — so a rewrite that worked reports exactly the hit count
it started with, and reads as though it did nothing. Confirmed 2026-08-29 doing this store's first
push. Check the branch itself before concluding anything, then drop the backup ref and let the old
objects go:

```shell
git -C <store> log <branch> -p | grep -i <term>        # the real answer
git -C <store> update-ref -d refs/original/refs/heads/<branch>
git -C <store> reflog expire --expire=now --all && git -C <store> gc --prune=now
```

Take a copy of the whole directory first. It is the only copy of those plans, and a rewrite is the
one operation in this convention that can lose them.

`shareable_roots` exists as its own key, defaulting to `public_roots`, because the two questions
nearly always agree but are not the same: a root's name may be publishable while its plans are not,
or the reverse. Leave it unset until they actually disagree.

**Moving a root between tiers moves no files.** `doctor` reports a mirrored root sitting in the
wrong store and names where it should go; relocating it is a `git mv` in two histories and a
decision about what gets published, so it is never done automatically.

**`where` exiting 3 is a question, not a failure.** It means no rule covers this repo. Ask the user
which route it should use, then record the answer. Never pick a side silently: guessing "repo"
writes a directory into someone else's repository, and guessing "store" hides the plan somewhere the
user never named.

**Record it with `config set`, never by editing the TOML yourself:**

```shell
python3 <path> config set roots.<root-name> repo         # a whole root
python3 <path> config set repos.<root>/<repo> store      # one repo, beats any root rule
python3 <path> config set default store                  # everything unmatched
python3 <path> config set view.idea_limit 20             # how many ideas a listing shows
```

It preserves every comment in the file — those comments carry the reasoning for each key — replaces
a commented-out example in place, and rejects a value the config's own schema will not accept,
restoring the file rather than leaving it broken. A key's table is whatever precedes its first dot,
so a repo path full of dots stays one key.

```toml
projects_root = "~/projects"
store = "~/plans" # the shareable tier
# sensitive_store = "~/plans-sensitive" # defaults to <store>-sensitive
default = "store" # omit it and an unmatched repo asks instead

public_roots = ["github.com-personal"] # names that may appear in a published repo
# shareable_roots = ["github.com-personal"] # the tier boundary; defaults to public_roots

[roots]
"github.com-personal" = "repo" # longest matching prefix wins

[repos] # an exact repo entry beats any root entry
"github.com-acme/legacy-api" = { mode = "both", write = "store" }
```

### Environment assumptions, and setting them up

`$PLANS_HOME` (default `~/plans`) is the shareable store and `$PLANS_SENSITIVE_HOME` (default
`<store>-sensitive`) the other half — pinning the first pins both, since the second derives from it;
`projects_root` (default `~/projects`) is the root the mirrored paths are relative to;
`$PLAN_DOCS_CONFIG` overrides the config location.

**The config is per-machine, not per-user, and is deliberately not version-controlled.** It maps the
repos that happen to be cloned on _this_ box to routes, so it says nothing meaningful anywhere else
— a second machine with a different set of clones needs a different file, not a copy of this one. Do
not propose committing it to a repo or syncing it; losing it costs one `install` and one pass of
`config set`, which is cheaper than maintaining a shared file that is wrong on every machine but
one.

**Setting up a machine is a walkthrough, and you run it.** The script never prompts — it has to keep
working when a human runs it by hand, and an interactive prompt inside an agent's Bash call hangs
with nothing to type into. So the decisions are printed as data and **you** are the interactive
surface:

1. `python3 <path> install --explain` — what it would create, then one block per decision, each with
   what it is, what is currently set, what it would suggest, and what it costs to get wrong. Writes
   nothing.
2. Put each decision to the user with `AskUserQuestion`, using the `suggest` line as the recommended
   option and the `cost` line as the description. Do not skip to the defaults: the `default`,
   `public_roots` and `shareable_roots` answers decide whether plans land in repos the user does not
   own, whether `scan` will catch a client's name, and which roots may reach a remote at all.
3. Record each answer with `config set` (above). Never edit the TOML by hand.
4. `python3 <path> install` — idempotent: writes the config skeleton if there isn't one (never over
   an existing one), creates **both stores** as git repositories, adds neither a remote, creates the
   repo-less area.
5. `python3 <path> doctor` — confirm it took, and that no problem is left.

It asks one question per unrouted root only when no `default` covers them; with a default set, that
answer is already given and the walkthrough stays short.

`python3 <path> uninstall` reverses it: it removes the config but **keeps both stores**, because the
store is the only copy of those plans; deleting them takes `--purge-store --force` and a deliberate
decision, and the file count that triggers the refusal is taken across both tiers before either is
touched.

### What the projects tree has to look like

Repos are discovered by walking `projects_root` and stopping at each `.git`, so the walk assumes a
shape. A **collection directory** is any directory on the path down to a repo — `projects_root`
itself, each root under it, and each intermediate level of a `<root>/<project>/<repo>` hierarchy.
Collection-ness is derived, never configured: a directory is one if it is not a repo and has repos
beneath it.

- **`projects_root` must not be a git repository.** This one is fatal and refuses rather than
  reporting: with a `.git` there the walk returns a single repo named `.`, every real repo becomes
  invisible, and `scan` derives almost no terms — a confidentiality gate that passes because it can
  no longer see anything.
- **A symlink is never followed.** Git resolves symlinks, so a link to a repo inside the root
  enrolls the same repo twice under two paths, and a link to one outside is counted by discovery
  while `where` refuses it. Plan in the repo at its real path.
- **A bare repository is neither a repo nor a collection**, and is reported as such rather than
  walked into.
- A directory holding no repos is simply ignored — `doctor` counts them and `--strict` lists them.
- **A repo cloned straight into `projects_root` is routed with `[repos]`, never `[roots]`.** A
  `[roots]` key is a path _prefix_, and a repo at depth 1 has no prefix, so an entry naming it is
  never consulted and the repo falls through to `default`. `where` and `doctor` both say so now
  rather than leaving it silent; the fix is `config set repos.<name> <repo|store>`.

**Categorise every root explicitly**, even where `default` would give the same answer. Then a root
falling through to `default` means exactly "this appeared since you last decided anything", and
`doctor` lists it as awaiting a decision — no seen-markers, no registry, just the config read as a
record of what has been answered. Without that pass, a newly cloned root is routed silently, which
is right for a client root and quietly wrong for a personal one: its plans would accumulate in the
store mirror forever, because a store-routed repo's mirror _is_ its home and `absorb` correctly does
nothing.

### Is this machine set up, and what is in it

```shell
python3 <path> doctor
```

One call for the whole picture: config location, **both stores with their git state and which one
has a remote**, which roots are enrolled, by which rule and into which tier, which repos actually
hold plans, a tally by status and open tag, and a **problems** list — a store that is not a git
repository or has lost its git identity, a remote on the sensitive tier, a mirrored root filed in
the wrong tier, an unset `PLANS_HOME`, a repo holding plans that no rule routes. Run it when
something behaves oddly and before trusting `archive`, which retrieves nothing from a store with no
git history.

It aggregates by root and names an individual repo only when that repo holds plans — a per-repo
listing is one row per clone on the machine, which is a roster of employers and clients. Its output
is for setting the machine up, never for pasting into a repo you publish.

**The sensitive tier's no-remote rule is the design, not an oversight**, and `doctor` reports a
remote there as a problem: local history is the benefit, and one personal remote accumulating
several clients' internal architecture is the outcome to avoid. Adding one is a per-root decision
against that employer's actual policy, never a convenience. Until such a decision is made, treat
that tier as unbacked-up. Never symlink either store, or a subtree of it, into a work repo — that
puts the content back inside the tree repo-scoped agent reads walk.

## Never let a client's identity reach a repo you publish

The store exists because work repos can't hold plans. The mirror image of that is the rule that
matters more: **a plan committed to a repo you publish must not name the client, employer, project
or repo it came from.** Not the org, not the internal project name, not the work email address, not
the ticket prefix. A plan about work for someone else can still be written — describe the shape ("a
work root with a `<project>/<repo>` hierarchy", "a client repo under review pressure") and keep the
specifics in the store, where they belong.

**Run `python3 <path> scan` before committing to any repo that is or might become public**, and
`--mode staged` immediately before the commit itself. It exits non-zero on a hit. The terms come
from the machine — every root, project and repo name under `projects_root` that is not under a
`public_roots` entry, each root name also split into its organisation (so the client behind
`<org>.com-<host>-<team>` is caught in an `@<org>.com` address too), plus `[private] extra` — so a
newly cloned client is covered with nothing to maintain, and the list itself never has to be written
into a public repo.

`[private] extra` is not optional decoration: an employer with no repo on this machine has no
directory to derive from, and is invisible to the scan until someone adds it.

Only a **collection** name is split into its organisation. A directory under `projects_root` that is
itself a repository contributes its whole name and nothing else — splitting it is how ordinary words
enter the term list, and a gate that flags "repo" in every document is a gate that gets switched
off.

**Never hand-roll the pattern for an audit.** `scan --list-terms` prints the list the scanner
derives; `scan --mode history` is the audit. A regex written by hand is a narrower list whose edges
you cannot see, and it will look like a clean result. Confirmed live 2026-08-29: a repo was surveyed
with a hand-written alternation covering the addresses already known about, declared clean apart
from those, purged — and the scanner then found an employer's name in that repo's first two commits
from 2021, in four branches, because the hand-written pattern omitted one work root the derived list
had all along.

Two failure modes to handle correctly:

- **A generic hit.** A work repo named `tools` or `settings` matches ordinary English. Put that one
  name in the config's `[private] ignore` list — never widen `public_roots`, which silences a whole
  organisation's worth of names to fix one word.
- **Writing about a hit reintroduces it.** A plan explaining what leaked, a rationale page using a
  real name as an example, a commit message quoting the offending line — each puts the term straight
  back into the tree the scan just cleared. Measured three times in one session, 2026-08-29, each
  caught by `--mode staged` before the commit. Reference the thing by where it lives — the commits
  and the `scan --mode history` command that print it — not by quoting it.
- **A hit in pushed history.** `--mode history` scans every commit. Redacting the working tree does
  not remove anything from a published repo; purging history means a force-push and a support
  request, and it is the user's call, not an edit to make quietly. Report it, name the commits,
  stop.

Confirmed live 2026-08-28: this repo had already published a plan whose measurement table listed six
employer/client root directory names, plus one client's internal `<project>/<repo>` path — written
by an agent with no rule telling it not to, into a repo whose own README advertises it as public.

## Something that belongs to a repo you are not in

**Never write a plan into another repo's working tree.** Parallel sessions on one machine share that
tree, so a file appearing there under a session already working in it is the failure this rule
exists to prevent — and a plan committed across repos is a commit nobody in that repo asked for.

The script enforces this rather than trusting anyone to remember: `new` **refuses** to create a plan
in a repo other than the one the session is in, and names `--for` in the error. Commands that act on
files which already exist — `graduate`, and anything reached by `--path` — **warn** instead, because
those have legitimate uses; when you see that warning, prefer doing the work from a session inside
that repo, and if you continue, tell the user exactly what landed where.

**The guard is anchored to the repo the session started in, not to the working directory**, because
cwd is unreliable in both directions — a reset and a persisted `cd` were both observed inside one
session, 2026-08-29. A guard comparing cwd against cwd cannot fire when cwd drifts, since both sides
move together; an anchor gives the comparison two independent sides.

Three tiers, most trustworthy first. **Nothing here is Claude-only except tier 2**, and no tier is
required for the skill to work:

| tier | signal                                                    | when it applies                   |
| ---- | --------------------------------------------------------- | --------------------------------- |
| 1    | `$PLAN_DOCS_SESSION_REPO`                                 | **any harness**, if it exports it |
| 2    | `$CLAUDE_CODE_SESSION_ID` → the session's transcript path | Claude Code, no setup needed      |
| 3    | cwd                                                       | fallback; cannot detect drift     |

**On a harness that is not Claude Code, export `PLAN_DOCS_SESSION_REPO` at session start** —
`export PLAN_DOCS_SESSION_REPO="$(git rev-parse --show-toplevel)"` — and the guard is exactly as
strong as it is under Claude Code. Without it everything still works; the guard just degrades to
tier 3 and stops catching a drifted directory. `doctor` reports which tier is in use and lists the
fallback as a problem, so nobody is in the weak tier without being told.

Two habits that hold at every tier:

- **Read the `repo:` line every create prints.** It names the repo the plan just became the property
  of, derived from where the file was written rather than from any comparison, so it is true
  regardless of what cwd or the anchor did.
- **Never `cd` into another repo without asking the user first**, and after any cross-repo command
  treat cwd as unknown until a call re-establishes it. The anchor makes a stray `cd` survivable, not
  free — everything else in a session still runs relative to cwd.

```shell
python3 <path> new <topic> --for github.com-personal/<repo>   # or an absolute path
```

It writes into that repo's store mirror, outside every working tree, whatever that repo's route
says. Nothing in the target changes. The session working there sees it — `list` at repo scope reads
the store mirror regardless of route — and absorbs it on its own schedule with
`move <file> --to repo`, committing only to its own repo.

No frontmatter marks these. For a repo that keeps its own plans, a file in its store mirror is **in
transit** by definition; for a repo routed to the store, the same file is at its permanent home.
Route plus location already says it, so there is nothing to set and nothing to drift.

**If the store has uncommitted changes, add a new plan rather than editing an existing one**, and
reference the plan it relates to. Another session may be holding that file; a new file cannot
conflict, while an edit to a held file is the one loss that is not recoverable. Check with
`git -C <store> status --porcelain` — **against the store this write targets**, which the create
command names for you. Checking the other tier answers a question about a different repository.

The check works because both tiers are real git repositories. That is why the sensitive roots are a
second repository rather than entries in the shareable one's `.gitignore`: verified 2026-08-29, a
write to a gitignored path does not appear in `git status --porcelain` at all, so this check would
report clean about the tier it cannot see — worse than having no check, because the answer is
trusted.

**Commit a store plan the moment it is written, never at the end of a session.** Every minute the
store is dirty is a minute another session must fall back to adding a file it would rather have
edited, so the rule above and this one are the same rule from two ends: the fallback is cheap
because dirty windows are short, and dirty windows are short because nobody sits on an uncommitted
plan. `new` produces an empty skeleton, so the moment to commit is after the content is written, not
at creation.

```shell
git -C <store> add <the one path> && git -C <store> commit -m "<repo>: <what it is>"
```

Stage by explicit path, never `git add -A` — a parallel session's half-written plan can land between
your write and your commit, and a blanket stage would ship it under your message.

**Pushing is a separate, gated step, and only the shareable tier has anywhere to push to.** Scan
before pushing and push only on a clean result — `--mode staged` on the commit you are about to
make, and `--mode history` before the store's very first push, since that is what a push actually
ships and the last moment a hit is an edit rather than a purge decision. The tier boundary keeps
whole client roots off the remote, but a client's name inside a personal repo's plan or an unscoped
idea is exactly what it cannot catch. The sensitive tier has no remote, so there is nothing to push.

### Absorbing what was filed for this repo

**On your first plan-docs call in a session, run `absorb` before anything else:**

```shell
python3 <path> absorb            # report only — prints nothing at all if nothing is waiting
python3 <path> absorb --apply    # move them into this repo's plans/
```

It is silent when the store holds nothing for this repo, so it costs nothing on the sessions where
it does not apply. When it does print, **put the set to the user with `AskUserQuestion` before
applying** — one question for the set, not one per plan — then apply, run the repo's quality gate,
and commit **twice**: this repo for the additions, the store for the removals. Then carry on with
whatever the session was for.

Once per session, not once per command. The script is stateless and cannot tell a first call from a
fifth; you can, so the rule lives here. `list` also prints a one-line footer when plans are waiting,
for a session that skipped the proposal.

**Committing to both repositories here is not the cross-repo commit this section forbids.** You are
the session working in this repo: the additions go to your own tree, and the store only loses the
file you just took. What is forbidden is writing into a tree that is not yours — and
`absorb --apply` enforces exactly that, refusing when the target is not the repo your session
belongs to. Reporting for another repo (`absorb --path <other>`, no `--apply`) is a harmless
question and stays allowed.

**A name collision is a merge, not a rename.** `absorb` refuses when a filed plan's name already
exists in `plans/`, exits non-zero, and destroys neither copy — two plans sharing a name means both
cover the topic, and that is the moment to combine them by hand.

**Absorption is also where a dirty-store split gets reconciled.** When a harvest found the store
dirty it added a new plan referencing an existing one rather than editing a file another session
might have been holding. `absorb` finds those pairs — by the reference itself, checked against both
directories — and prints `consolidate with …` beside each. Do it as part of the same acceptance:
merge the two into one plan, keep the earlier filename, delete the other. **Nothing re-surfaces this
after absorption**, because the pairing lives in prose, so a pair skipped here is a pair nobody is
reminded of again.

A cited filename that resolves to no actual file is not a pair — plans legitimately reference
retired and foreign plans in prose, and only a name matching a real file on either side counts.

Absorption applies only to a repo that keeps its own plans. For a repo routed to the store, the
mirror **is** the permanent home and nothing is ever in transit.

## Plans that belong to no repo yet

An idea, task or exploration that has not earned a repo goes to `$PLANS_HOME/_unscoped/`:

```shell
python3 <path> new <topic> --unscoped     # works anywhere, including outside any git repo
python3 <path> list --scope unscoped      # the repo-less backlog on its own
python3 <path> graduate <file> --to <path inside the new repo>
```

`graduate` routes the file through the destination repo's own rule — into its committed `plans/`, or
into that repo's store directory — and stamps the `repo:` frontmatter when the destination is the
store. Do it the moment the repo appears, not later: an unscoped plan whose work has moved into a
repo is a plan nobody will find again.

## Asking what is open

**Answer "what plans do we have" and "what should I work on" with one `list` call, not by opening
plan files.** The scope is chosen for you:

```shell
python3 <path> list                       # auto: this repo when in one, the machine when not
python3 <path> list --scope family        # every repo, always
python3 <path> list --stale 14            # only what nobody has touched in a fortnight
python3 <path> list --since 2026-08-01    # only what moved on or after a date
python3 <path> list --tag DEFERRED        # only plans carrying that open tag
python3 <path> list --all                 # include landed, abandoned and superseded
python3 <path> list --limit 0             # every idea, uncapped
```

`--scope auto` is the default and resolves to `repo` inside a routed repo, `family` outside any repo
and inside the store itself — so a session that has cd'd nowhere in particular gets the machine-wide
answer without asking for it.

**Repo scope reads the repo's `plans/`, its store mirror, _and_ the unscoped area, whatever the
route says.** A route decides where a _write_ lands; letting it decide what a _read_ can see is what
kept unscoped plans invisible from every repo on a machine whose roots are all `mode = "repo"`
(confirmed 2026-08-29) — the plans with no other route back to attention were the ones nothing
surfaced.

`--stale` and `--since` are opposite questions and treat an unstamped plan oppositely: `--stale`
keeps it (nothing says it was touched), `--since` drops it (nothing says it moved). Neither bounds
the default output — the cap below does that, because a date window's size is not predictable.

**Output is bounded, and only the `idea` tier is capped.** `in-progress`, `blocked` and `planned`
are limited by how much work can actually be in flight; `idea` grows forever, so it is the only
group whose cost is unbounded. The cap is `[view] idea_limit` (default 10), `--limit` overrides per
call, and the footer always says how many rows were elided. **Never read a capped listing as the
whole set** — if you are about to conclude something about every plan, pass `--limit 0` first.

Two things only `--scope family` reports, because no per-repo command can see them:

- **`depends_on` as a blocked-by view**, summarised as counts. The plans themselves print under
  `--scope repo` in the repo being waited on, as "waiting on this repo" — that is where the wait is
  actionable, and printing every edge machine-wide is a section that grows with the corpus exactly
  the way the idea tier does (measured 2026-08-29: 22 of 81 lines).
- **Status drift.** A status outside the vocabulary — `done` where `landed` is defined, or a
  free-form paragraph where an enum belongs — is only visible across repos, since each repo's own
  gate sees one repo. Both were found on this view's first real run, 2026-08-29.

**A terminal-status plan is hidden from the rows but never silently.** `plans/` is a working set
that empties out, so a `landed` plan still sitting in one is a retirement owed; the footer counts
them and `--all` shows them. That count is often the most useful line in the output.

Like `repos`, family output names work repos: use it to decide what to work on, never paste it into
a repo you publish.

## Which repo does a plan belong to?

When content could plausibly belong to more than one repo, don't grep repos to decide, and don't
guess:

```shell
python3 <path> repos --search "<the words the plan is about>"
```

It prints every repo under the projects root with its route and a one-line description — the
config's `[about]` entry, else that repo's README first line — ranked by the search words. Take the
top two or three and put them to the user as `AskUserQuestion` options with those descriptions as
the option text: an informed guess to confirm, not an open question. Record a better description
with `python3 <path> describe <repo> "<what belongs there>"` whenever a README's own line turns out
to be a poor answer. That listing names work repos, so it is for choosing a destination — never
paste it into a repo you publish.

## Creating a plan

`python3 <path> new <topic>` — kebab-case topic, one file per topic. It writes `YYYY-MM-DD-topic.md`
in the route's write directory with the frontmatter already correct:

```yaml
---
status: idea
updated: YYYY-MM-DD
repo: <origin URL> # store-held plans only — location no longer names the repo
---
```

Body: `## Context` → `## Open questions` (each unresolved point marked with an inline
`[NEEDS CLARIFICATION: ...]` tag) → `## Recommended direction` (rough, non-prescriptive).

**This applies to anything turned up incidentally, not only to deliberate design requests.** A bug
worth fixing later, an idea worth brainstorming, a risk worth mitigating — each gets its own file.
Never leave it as future-work prose in `README.md`, `AGENTS.md`, a docs page, or a code comment:
those describe current state, and prose has no status field, so nothing ever prompts anyone back.
(Confirmed live 2026-08-23: a known test-coverage gap sat in a `README.md` as "a real gap… not yet
fixed" instead of a plan file, invisible to anything scanning `plans/` for open work.)

## Committing a plan file

**Run the repo's quality gate before every `plans/*.md` commit** — create, update, or retirement.
"Just markdown" is not an exemption: formatters reflow prose, and doc-only commits that skipped the
gate are the single most common cause of red CI in repos using this convention.

A store-held plan is committed to the **store's** git repository instead, and no work repo's gate
applies to it. Commit it there anyway, in the same session that wrote it: the store's history is the
only record that plan has, and an uncommitted file in a directory nobody browses is the same as no
plan at all.

## Tags

Five inline markers, all `[SHOUTY-WORD: text]`, so the judgment calls below become greps instead of
re-reads, and nothing costly is lost when a file is deleted.

| tag                        | means                                           | at retirement                          |
| -------------------------- | ----------------------------------------------- | -------------------------------------- |
| `[NEEDS CLARIFICATION: …]` | open question                                   | must be zero to leave `idea`           |
| `[DECISION: …]`            | settled choice + why it beat the alternatives   | → design rationale                     |
| `[PITFALL: …]`             | non-obvious trap, confirmed by hitting it       | → design rationale                     |
| `[DEFERRED: …]`            | consciously scoped out, still wanted            | → an open plan; **blocks deletion**    |
| `[UNVERIFIED: …]`          | designed or implemented but not actually proven | → verify or defer; **blocks `landed`** |

**Five is the whole vocabulary.** Don't add a sixth — inconsistently-applied tags are worse than
none, because the greps still return results and get trusted while being incomplete. There is
deliberately no `[VERIFIED:]`; the _absence_ of `[UNVERIFIED:` is the signal.

Not bare `TODO`/`FIXME` — those collide with code comments, making `rg TODO` useless in a repo that
also contains source.

**Tag the claim, not the section.** One tag per discrete, individually-extractable fact. A tag
scoped to "everything below this heading" can't be migrated mechanically, which is the whole point.

**A tag opens its own line**, starting a paragraph or immediately following a list marker. Searches
for it must be anchored the same way — a bare `rg '\[DEFERRED:'` matches every prose _mention_ of a
tag, so any document discussing this convention reports a false backlog. `plans.py tags` is the
anchoring, applied across every directory the repo's route reads:

```shell
python3 <path> tags --tag DEFERRED               # the whole backlog, no file opened
python3 <path> tags --file <file>.md             # one plan, all five tags
```

Tag at status transitions, not while drafting — those are the moments someone is already reading
closely. Retrofit an existing corpus in one pass rather than lazily; half-tagged is the failure mode
above.

## Promoting a plan

**Promote in place, in the same file — never split into a second file for the same topic.** Resolve
every `NEEDS CLARIFICATION` first, then `python3 <path> set-status <file> planned` — it runs that
gate and refuses while any remain, so a refusal is the answer, not an obstacle to route around with
`--force`. Rewrite the body as `## Context` → `## Design` (numbered subsections, one per
file/component touched, rationale inline) → `## Files touched` → `## Verification`.

As work proceeds, bump `status` again with the same command (it also stamps `updated`); the sections
don't change:

- `in-progress` — actively being built.
- `blocked on <reason>` — stalled on something external, with the reason in the status line itself,
  e.g. `blocked on the upstream API adding a /search endpoint`.
- `landed` — implemented and verified. Transient; see "Retiring a plan".
- `abandoned` — killed before landing. Also transient.
- `superseded by plans/<file>.md` — a landed plan whose decision was later reversed by another.

Optional `depends_on: [<repo-name>, ...]` frontmatter names sibling repos this plan can't fully land
without. Omit it for the ordinary single-repo case.

## Where retired content goes

Three destinations, named by **role** rather than by path, because every repo lays them out
differently — and a repo may have no separate directory for the middle two at all:

| role                 | what belongs there                                              |
| -------------------- | --------------------------------------------------------------- |
| **the code itself**  | changes needing no explanation beyond the code and its comments |
| **usage docs**       | anything about how a person or agent uses the result            |
| **design rationale** | settled decisions, rejected alternatives, confirmed pitfalls    |

Map these onto whatever the repo has — a `docs/` tree, a `contributing/` tree, a package's own
`references/`, a section of `AGENTS.md`, a code comment. The requirement is _somewhere durable and
findable_, never a specific directory name. If a repo has no obvious home for design rationale,
picking one is part of the first retirement, not a reason to skip it.

## Retiring a plan

On reaching `landed`, `abandoned`, or an old `superseded by ...`: `plans/` is a working set that
empties out — but nothing genuinely costly to work out gets silently dropped. Deleting the file
takes it off the working set, not out of the repository: the drafting commits, its final state and
the `## Migrated to` commit all stay reachable through git, and `python3 <path> archive` is how they
are read back — see "Getting a retired plan back" below. That is what makes the deletion cheap, and
it is why a plan is only ever kept in version control.

**A repo that keeps its own plans retires them in its own history — absorb first, then retire.**
`set-status` refuses a terminal status on a plan still sitting in the store mirror of a repo-routed
repo, and names `absorb`. The reason is that retirement deletes the file and `archive` reads it back
out of the deletion commit: retiring from the store would put the drafting, the landing and the
deletion in the store's history while the repo's history has nothing, so `archive` run inside that
repo would find the plan missing. One plan, one history. Non-terminal statuses are unaffected —
nothing has been deleted, so nothing is split.

**A store-held plan retires exactly like a repo-held one, and is deleted the same way.** This is
about a repo whose plans live in the store permanently, not one whose plan is merely in transit. The
usage docs and design rationale still go into the repo the plan is _about_ — updating a repo's own
docs is an ordinary contribution, available even where adding a `plans/` directory is not, and it
would be owed just the same if the planning had happened in a tracker instead. What is left after
that migration is reasoning that belongs to nobody but you, and it stays in the store's git history,
which is why the store is a git repository at all.

**Triage the file's content by lifecycle first.** Split by what each passage _is_, never by how long
the file is: a long file that is all one lifecycle stays one file, while a short one mixing several
gets split.

| kind               | example                                   | destination                         |
| ------------------ | ----------------------------------------- | ----------------------------------- |
| settled decision   | why tool X beat tool Y, with the evidence | design rationale                    |
| pitfall            | a trap confirmed by hitting it            | design rationale                    |
| code contract      | signatures, flags, behavior               | already in code/tests/README — drop |
| verification log   | "ran it, it worked", dry-run transcripts  | drop, except the unverified residue |
| **live open work** | anything still wanted but not done        | **an open plan — see step 2**       |

Code contracts and verification logs are usually the bulk of the deletable volume.

1. **Default: preserve.** Assume debugging, investigation and rejected-alternative reasoning has
   future value unless it is already written down elsewhere. Often it is — check the existing docs
   before assuming new rationale content is needed.
   - **In a repo family, check the sibling repo that owns the concern**, not just this one. A plan
     that designed something later extracted elsewhere describes a decision that repo now owns and
     keeps current; migrating it here ships a second, diverging copy that reads as authoritative.
     Point at the owning repo instead, and migrate only what it genuinely doesn't cover.
2. **A plan carrying live unfinished work is not deletable.** Run the deletion gate and move
   everything it finds into a plan that stays, before going further:
   ```shell
   python3 <path> tags --file <file>.md --tag DEFERRED
   python3 <path> tags --file <file>.md --tag UNVERIFIED
   ```
   Prefer appending to an existing open plan that already owns the concern over spawning a new file.
   On an untagged legacy plan, grep prose instead
   (`deferred|not yet|follow-up|TODO|known
   limitation`) and read what it finds.
3. **Find inbound references before starting, not after** — `python3 <path> refs <file>.md`. The
   count decides whether this is one commit or several. It searches the **whole repo** (code
   comments and docstrings cite plan paths too) plus the store, on the bare filename rather than the
   full `plans/` path, since short-form references are the easy miss.
4. **Add a `## Migrated to` section** naming each destination, and name what you deliberately did
   _not_ migrate and why. **Commit this addition on its own, before deleting the file** —
   add-and-delete in one commit means the section is never recorded in history at all, which defeats
   the point of writing it.
   - Organize the rationale home by **the question a reader arrives with**, not one file per retired
     plan — that just reproduces each plan's lifecycle mixing under a new name. Expect the most
     valuable file to be one that existed in no single plan.
   - Before dropping anything as "already in the code", check that it is. Verify what you migrate
     too: prose written months ago about a module drifts, and a plan is not evidence about current
     behavior.
5. **Fix the references from step 3, then delete the file** — only once step 4 is genuinely covered.
   If there is any doubt whether something worth keeping was captured, ask before deleting; it is a
   one-way door once the commit lands.
   - Don't blindly swap the old path for the new one at every hit. A reference to a specific quoted
     section title needs that title updated to match where the content actually landed — a valid
     path aimed at a renamed heading still dangles. Some cited content is already duplicated at a
     third location; point at that copy rather than migrating a second one. And some references are
     better rewritten than repointed: "X landed in `<plan>`" just becomes "X landed."
   - The finishing grep should return **no live pointers**, which is not the same as zero hits.
     Provenance legitimately survives ("extracted from the now-retired `plans/X.md`") and should —
     but must say _retired_, so a reader knows not to go looking.
6. **Run the repo's gate again before committing the reference fixes.** Editing many
   comments/docstrings in one pass is exactly what quietly trips a line-length rule.

## Getting a retired plan back

Deleting a plan is only cheap because the file is still in the repository, and that is only true in
practice if getting one back is a single command rather than an archaeology session:

```shell
python3 <path> archive                      # every plan deleted from this repo's plans/, newest first
python3 <path> archive --search "<phrase>"  # only the ones whose content ever contained it
python3 <path> archive --show <file>        # print one back, as it stood the moment before deletion
python3 <path> archive --file <file>        # one plan's whole lifecycle: drafting, landing, retirement
python3 <path> archive --all                # every repo on the machine, plus both stores' histories
```

Each row carries the plan's final `status` and its `## Migrated to` destinations, which are usually
the real answer — the content is in a doc somewhere, and only the reasoning that had no home is in
the deleted file itself. Nothing is written and no file is restored: a retired plan comes back on
stdout, and if the work is live again it earns a new plan file rather than a resurrected one.

Three things worth knowing before trusting a result:

- **`--search` matches across line breaks**, so a phrase the formatter has since reflowed is still
  found. It also searches every version of every retired plan, not just the final one — so a passage
  cut two commits before the deletion still matches, and `--show` will not contain it. Use `--file`
  to find the commit that did, and read that one with `git show <sha>:<path>`.
- **A plan that moved between the repo and the store is not retired**, though its old location's
  history says it was deleted. Those rows say `still live` and name where it is; go read that file.
- **A store with no git repository archives nothing.** `archive` says so in its header when it finds
  one, per tier. Fix it with `python3 <path> install` _before_ retiring anything held there. Both
  tiers keep full history precisely so this stays true for client plans, which are the ones with no
  other copy.

## Migrating a legacy single plan file

A repo predating this convention often has one big `PLAN.md`/`DESIGN.md`/`NOTES.md` mixing unrelated
threads at different lifecycle stages. Don't retire it as a unit — split by thread first, then apply
the lifecycle above to each piece:

1. Sort its sections into threads: implemented and verified (→ `landed`), genuinely still undecided
   or stalled (→ its own new plan file, `status: idea` or `blocked on <reason>`), and simply
   inaccurate now (a design later replaced — drop it, it has no destination). One legacy file
   routinely becomes zero, one, or several plans, not one.
2. Run the `landed` threads through "Retiring a plan" immediately, in the same pass — no reason to
   copy them into `plans/` only to retire them a moment later.
3. Give each still-open thread a real plan file with correct frontmatter, reformatted into the
   standard sections — not a leftover fragment of the old file's prose.
4. Only once every thread has a home does the legacy file get its own `## Migrated to` section
   (naming every destination) and go through the normal commit-then-delete sequence.

## Don't stash future work in prose docs

Applies to any narrative doc — `README.md` and docs pages included, not only `AGENTS.md`. Each
should describe the repo as it is right now. A known bug, an unfinished feature or an open risk
belongs in its own plan file, linked from the doc if it is worth a pointer, never spelled out there:
prose future-work rots into a permanently-true-sounding sentence, or worse, an already-fixed problem
still calling itself "not yet fixed".

`AGENTS.md` (or any equivalent instructions file) gets the strictest version: instructions for
developing and deploying the repo only — never planning, ideation, or a status report. Three drifts
worth auditing for:

- **Dated status narrative.** "Status: implemented and exercised live 2026-08-14" is a changelog
  entry, not an instruction — true today, stale tomorrow. Trim to an undated statement of what is
  architecturally true now, and drop the "as of `<date>`, confirmed working, tests pass" framing
  entirely; that belongs in a commit message.
- **Stale implementation claims.** "These functions are stubs", "not yet confirmed" — silently rots
  once the work lands. Don't prose-review these: grep the code for the thing described (e.g.
  `rg NotImplementedError` before trusting a docstring that claims it) before deciding whether a
  passage is accurate, superseded, or safe to cut.
- **Speculative asides.** "This might be cheaper a different way once X is understood" is a musing,
  not an instruction. Either it is a real open question deserving its own plan file, or it is colour
  already captured in the rationale home and can just be dropped.

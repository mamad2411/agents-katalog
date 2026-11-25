---
name: open-source-release
description: "Use when a project may go public. Repo and licence."
version: 1.1.0
author: coder role of hermes-fleet-apps
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [git, github, open-source, licensing, packaging, release, hygiene]
---

# Open Source Release

How a personal tool becomes a public repo without leaking anything, without a licence
surprise, and without a rewrite at the end.

Assume the owner is not a developer and has an empty GitHub account. They will not
remember repo hygiene and should not have to. The building agent (the coder role) owns
every git and GitHub decision, does it from the first commit, and reports what it did
rather than asking.

This skill is about *shipping*. The design method itself lives elsewhere; load both when
a build is intended to be published.

## The ladder

```
  local git  ──▶  private GitHub  ──▶  public
  from commit 1    once it runs         once it is stable and licence-clean
```

Never start at the public end. A repo that was private first can be cleaned. A repo that
was public first has its mistakes in other people's clones forever.

Decide the ladder **at project start**, out loud, in one line. "Public eventually"
changes what goes into commit 1; discovering it later means an audit and possibly a
history rewrite.

## Step 1 — first commit, before the first source file

Run `git init` when the project folder is created, not when the code works. History that
starts late cannot show how the thing was built.

The first commit contains, always:

- **`.gitignore`** covering the virtualenv directory, `__pycache__`, generated databases
  and state files, run journals and logs, downloaded model weights or other large
  assets, `.env`, and any personal test-data folder.
- **`.env.example`** — variable *names*, empty values, committed. The real `.env` is
  ignored and the owner types the values themselves.
- **A config file** with neutral defaults for settings. Settings in config, secrets in
  `.env`, never the reverse.

## Step 1b — the private remote, and the identity baked into it

Moving up the first rung of the ladder is two decisions, and one of them is permanent.

**Author identity is decided before the first push, never after.** Every commit carries
`user.name` and `user.email`, and once the repo exists anywhere but this disk that
history is mirrored and unfixable. Audit what is already there rather than asking what
the owner intended:

```
git log --format='%an <%ae>' | sort | uniq -c        # every identity in the history
rg -n --no-ignore --hidden -g '!.venv' -g '!.git' -i \
   '<real name>|<home path>|<personal email>' <public dirs>
```

If the history is already pseudonymous, the owner is not choosing — they are confirming, and the
answer is the pseudonym. **Pseudonym → real name later is easy; real name → pseudonym is
impossible**, so the one-way door decides it on its own. For a privacy or FOSS tool,
trust comes from auditable code that makes no network calls, not from a name on a
profile. Name the one real cost out loud: money later (sponsorship, selling) needs a
real identity at the payment layer, which is normal but is friction.

The commit email is part of that decision. Offer GitHub's `ID+name@users.noreply.github.com`
form while the history is small — rewriting a handful of commits is trivial before the
first push and impossible after clones exist.

**When an address has to disappear, rewrite the metadata — do not delete the commits.**
Asked to erase an identity, a user usually means the address, not the work. Prove where
it actually lives before touching anything: grep the tracked tree for it. A miss means
every occurrence is a commit header, so rewriting the author *and* committer fields
removes it completely while the build history survives. Deleting commits to erase
metadata destroys the record for no additional privacy.

**Switch to the owning account before creating or pushing, never merely check it.**
`gh repo create` and the git credential helper both use whichever login is *active*, and
a machine can hold several. `gh auth status` reads the list; `gh auth switch --user
<owner>` is what makes the next command use it. Confirm with `gh api user --jq '.id'`
and match the numeric id against the one in the commit address — the id, not the login,
is what binds a commit to an account.

**Create and push are two steps.** Never pass `--push` to `gh repo create`: confirm
`isPrivate: true` from the API first, because visibility is the one property that cannot
be withdrawn once objects exist on a public URL.

The full ordered procedure, the pre-publication scan, and the host-side verification
that proves attribution and the absent private side: `references/first-push-verification.md`.

**Prove the private side is absent before the push, then again after it.** Ask git, not
`.gitignore`:

```
git ls-files | cut -d/ -f1 | sort -u        # exactly what will ship
git check-ignore -v AGENTS.md _private/...  # the private paths, named
git add -A --dry-run                        # silence = nothing unexpected
```

After the push, read the remote's own file list — the backup is not verified until the
hosting side agrees with the local claim.

## Choosing the host, for a local-first user

Self-hosted (Gitea, Forgejo) versus a hosted SaaS is a real trade, and the honest
answer is about *this* repo, not the principle:

- **State the actual exposure first.** If the private side is gitignored, the only thing
  uploaded is code intended to be published anyway — no data, no notes, no secrets. Say
  that plainly, then let the objection be what it really is: dependency and principle,
  not leaked material. "Private" on a SaaS means hidden from other users, not hidden
  from the provider or from a legal request in its jurisdiction.
- **A remote in the same building is half a backup.** A self-hosted box in the same flat
  as the workstation shares its fire, its theft and its flood. The complete shape is the
  self-hosted remote for control plus an off-site copy of the public code.
- **"Nothing is backed up" outranks host purity.** Take the zero-setup remote today and
  migrate later; a remote is a URL, and moving one is a one-line change.

## Step 2 — what goes public, and what never does

The published repo shows **the tool and the problem it solves**. How it was built, what
was measured, and how it evolved are working material and stay local.

```
  PUBLIC                          PRIVATE (gitignored, on disk)
  src/  tests/                    AGENTS.md and other agent instructions
  README.md                       evaluation write-ups, benchmark tables
  packaging + .gitignore          spikes, ground-truth samples, databases,
  LICENSE                           run journals, project-history notes
```

Decide this split when `.gitignore` is written, not at publication. Retrofitting it
means untracking files and rewriting history.

- **Agent instruction files are private.** Anyone cloning the repo runs `/init` with
  their own assistant and gets a file matched to their agent; a committed `AGENTS.md`
  leaks the author's conventions and internal notes for no reader benefit. Ignore
  `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` and their siblings by name.
- **Keep private material in one obvious directory** (`_private/`) plus a name list.
  A single ignored folder is auditable at a glance; scattered ignored files are not.
- **A project spanning many sessions keeps its state there too.** Put one orientation
  file at a known path stating what works, what is broken, what is next, and where the
  data lives, alongside the settled and rejected decisions with their reasons — then
  point the (also private) agent-instruction file at it as the first thing to read.
  Project-scoped markdown beats a profile-wide memory store for this: the user can read
  and edit it, it travels with the repo, and one project's facts stay out of unrelated
  work. A decision whose reason is unwritten gets re-litigated by the next session.
  **Those notes must track corrections and changes of mind, not just new features**, or
  a later session reads a confident stale page and builds on a contradiction. The update
  policy, the supersede procedure and a mechanical consistency checker are in
  `references/project-memory-discipline.md`.
- **The README describes capability, not provenance.** No accuracy tables, no evaluation
  narrative, no "how we arrived at this threshold", no build history. What it does, what
  it refuses to do, how to install, how to run, the honest limits.
- **The README assumes nothing about the reader or about who is in their data.** A
  motivating example written from the author's life — "photos of your sister, your
  friends", "several people you both know" — narrows the tool to one kind of user and
  reads as unprofessional to the archivist, researcher or contractor processing somebody
  else's material. Describe the situation, not the reader's relationships: "the pictures
  of any one person are scattered through the pile". The distinction that decides each
  case: **second person addressing the OPERATOR is correct and load-bearing** ("your
  machine", "your files", "your own LLM" — that is the privacy claim), while second
  person asserting a RELATIONSHIP to the subject is not. Gendered pronouns tied to an
  example name ("added her", "stops recognising her") fail the same way: use the role
  ("that person", "the subject").
- **Never reference a private file from a public one.** A README link or a source-file
  docstring pointing at an ignored path is a dead reference in every clone. Grep the
  public tree for the private filenames before committing.

## Step 3 — rules that hold for every commit after

- **No absolute paths, usernames, real folder names, or personal filenames** anywhere in
  source, tests, examples, or README. Everything comes from an argument or a config
  value. Retrofitting this before publication is far more work than doing it from the
  start, because it means touching every file and re-auditing history.
- **No secrets in source, ever** — not even temporarily, not even in a branch. Git keeps
  deleted content; a secret committed once is committed permanently.
- Commit messages a stranger can read. The repo is documentation.

## Step 4 — the pre-public audit

Run this as a checklist, not from memory, before the repo becomes visible:

1. **Scan the whole history**, not just the working tree — `git log -p` searched for
   personal paths, usernames, tokens, and real sample filenames. Deleting a file does
   not remove it from history. If something is found, the only honest options are a
   history rewrite or a fresh repo; say which, do not quietly hope.
2. **Licence every dependency**, and record them.
3. **Licence every downloaded asset separately** — see the asset-licence trap below.
4. **README a stranger can follow** on hardware you cannot see: what it does, how to
   install, one real command, one real output, and the honest limits.
5. **LICENSE file chosen deliberately**, not copied by reflex, and compatible with
   everything found in 2 and 3.

## The asset-licence trap

Model weights, datasets, fonts, icons and other downloaded assets carry their own
licence, independent of the code that loads them. A package can be MIT while the
pretrained weights it downloads on first run are marked *non-commercial research only*.

Check the asset licence explicitly and early — during stack selection, not during
release. State it in the README as its own line. Raise any conflict with the intended
use **before** the repo is public, and if it blocks the use, find a permissively
licensed alternative and document the swap. Discovering this after publication is a
takedown, not a fix.

## Credentials

The agent never handles a GitHub token, SSH key, or password. When authentication is
needed, stop, give the owner the exact command to run themselves, and continue once they
confirm. Prefer
non-interactive paths the user can run in one line over driving a login prompt.

## Pitfalls

**Assuming `.gitignore` hides an already-committed file.** Ignore rules apply only to
untracked files; a committed path stays tracked and stays in history no matter what is
added to `.gitignore`. Untrack it with `git rm --cached <path>` *and* deal with the
history — while nothing has been pushed, deleting the branch ref and re-committing
(`git update-ref -d HEAD`, `git reflog expire --expire=now --all`, `git gc --prune=now`)
gives a clean first commit. After a push, only a real history rewrite works.

**Verifying the split by reading `.gitignore` instead of asking git.** The authoritative
answer to "what would be published" is `git ls-files`; the authoritative list of what
stays local is `git status --ignored --short`. Run both before the commit that makes a
repo real, and grep the staged names for sample data and generated state:
`git diff --cached --name-only | grep -iE 'sample|\.db$|\.npy|jpg|png'`

**Pasting real tool output into public documentation.** A README example copied verbatim
from a real run carries real filenames, paths and identifiers out of the private test
set and into the published repo. Retype example output with neutral names; the
authenticity of a genuine paste buys nothing and leaks whatever the run touched.

**Auditing by reading instead of grepping.** A personal filename embedded in an example
block reads as plausible sample data to a human eye scanning for problems. Pattern-match
for it mechanically — the identifier shapes of the real source material (camera prefixes,
platform export prefixes, long numeric IDs) — and run that check as part of the same
script that verifies doc/code consistency, not as a one-off before release.

**Arguing self-hosted versus SaaS in the abstract to a privacy-minded user.** They already
agree with the principle; what they cannot see is whether *this* repo actually exposes
anything. Compute the real exposure from `git ls-files` and say it in one line before
the trade-off, or the decision gets made on reflex instead of on facts.

**Advising on real name versus pseudonym without reading the history first.** The
commits may have already answered it. Advice that contradicts twenty-five existing
author lines is noise, and the identity in the history is the one that ships.

**Reading a `gh` exit code instead of its message.** `gh auth switch --user <name>`
answers `no accounts matched that criteria` and still exits 0, so a script keyed on the
status continues against the wrong account. Parse the output of every identity-selecting
`gh` command.

**Fixing the sentence the user quoted instead of the class it belongs to.** A wording
complaint about public docs is a sample, not an inventory — the same habit is usually in
four more places the user has not read yet. Turn the complaint into a word list, grep the
whole document for it, fix every hit in one pass, and report the sweep as clean. Fixing
only the quoted line guarantees a second complaint about the same flaw.

**Assuming a repo's private working material moved when the repo did.** Relocating a
project by clone, or by any git-aware copy, carries only tracked files: the gitignored
side — agent-instruction files, `_private/`, the virtualenv, the project's own memory
pages — silently stays behind, and the new working copy looks complete because
`git status` is clean and every test file is present. After a move, list the ignored
paths at the new home before trusting it, and find the old home before declaring the
move done. A project whose wiki is missing cannot run its own doc gates, so the loss
shows up as an unexplained inability to close a step rather than as an error.

**Treating a successful push as a verified publication.** The push proves the transfer;
it says nothing about visibility, attribution, or whether the ignored side really stayed
behind. Re-read all three from the host's API afterwards — remote blob count against
`git ls-files | wc -l`, `author.login` on every commit, and the recursive tree grepped
for the private paths.

**Treating "open source it later" as a later problem.** It is a commit-1 problem.
Everything expensive about publishing — path scrubbing, secret scanning, licence
checking — is nearly free at the start and a project-sized job at the end.

**Auditing the working tree instead of the history.** `git log -p` is the audit surface.
The current files being clean proves nothing.

**Assuming the code licence covers the models.** It does not. Assets are licensed
separately and are the single most common open-source surprise in ML tooling.

**Publishing a README written for the author's machine.** If it names a drive letter, a
GPU, or a home directory, it is a personal note, not a README.

For the repo's logo, banner, workflow image or social preview (asset list, layout,
file placement, style references before round 1, the worktree/drafts setup, and the
model-licence gate on final assets), use the designer role's skill `repo-visual-assets`.

See `references/community-ready-design.md` for the design constraints that apply once
the audience is strangers rather than the owner.

---
name: git-remote-publishing
description: "Use when preparing a repo's first public push or release."
version: 2.0.0
author: coordinator role of hermes-fleet-apps
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [git, github, publishing, gh-cli]
    related_skills: [dependency-licence-audit]
---

# First-time repo publishing

Creating the remote and pushing a project that has never been pushed. The first
push is the irreversible step: afterwards the history is public and any cleanup
done beforehand is the only cleanup that counts.

Decide first which account, name and email the project publishes under, and keep
that in a file inside the project (e.g. `IDENTITY.md`) so every agent reads the
same rules. This skill covers the mechanics of the push itself.

## 1. Authentication is the owner's step

Never run the login command yourself: `gh auth login --web` prints a one-time
code, which would land in the model's context. Hand the owner the command, ask only
for the output of `gh auth status` afterwards — tokens are masked there.

    # the owner runs this, in their own shell
    gh auth login --hostname github.com --git-protocol https --web

⚠️ **The device flow authorises whatever account the BROWSER is signed in as.**
With several browser profiles open, the token lands on the wrong account and
the repo is created under the wrong name. Tell the owner to open
`https://github.com/login/device` by hand in the correct profile's window and
ignore the window that opens automatically.

Recoverable while nothing has been pushed: `gh auth logout --user <wrong>`.

If the owner pastes the one-time code into the chat anyway, say so plainly: it is
already consumed so there is no damage, but the rule stands.

## 1b. SSH keys are public

When the push uses SSH rather than HTTPS, the key itself becomes public. GitHub
serves each user's public keys to anyone:

    https://github.com/<user>.keys

Use one key per account; never reuse an existing key across accounts. Check what
is already exposed before deciding:

    curl -s https://github.com/<user>.keys

⚠️ **The key comment travels into that public file.** The default is
`user@hostname` and leaks the real machine name; pass a neutral `-C "<account>"`.

⚠️ **Without `IdentitiesOnly yes` in `~/.ssh/config`, ssh offers other keys as
fallback** and can authenticate you as the wrong account without saying so. One
host block per account, each with its own `IdentityFile` plus that directive.

Key generation is the owner's step — it prompts for a passphrase, and private
keys never pass through the conversation. You verify only the `.pub` side:

    LOCAL=$(awk '{print $2}' ~/.ssh/id_ed25519_<account>.pub)
    REMOTE=$(curl -s https://github.com/<user>.keys | awk '{print $2}')
    [ "$LOCAL" = "$REMOTE" ] && echo match

Pin the host fingerprints against the host's own documentation instead of
accepting them blind — `ssh-keyscan -t ed25519,rsa,ecdsa <host> > <scratch>/h.keys`,
`ssh-keygen -lf <scratch>/h.keys`, compare to the published SHA256 list, and only
then append to `known_hosts`.

A test with `-o BatchMode=yes` always fails `Permission denied (publickey)`
while the key is still locked — that is BatchMode suppressing the passphrase
prompt, not a broken configuration.

## Check the account's public fields before the first push

    gh api users/<user> --jq '{login,name,email,blog,company,location,bio}'

Every field here is public. Make sure each holds only what you mean to publish; the
full-name field is the one people fill in out of habit.

## 2. `gh` remembers several accounts — being logged in is not enough

    gh auth status                      # lists all; look for "Active account"
    gh auth switch --user <account>     # before creating OR pushing
    gh api user --jq '{login,id}'       # confirm you are who you think

Skip the switch and the credential helper hands over another account's token.

## 3. Scan before creating anything

Re-run the pre-publication checks even if the repo was sanitised weeks ago —
the tree may have moved since.

    git log --format='%ae' | sort -u        # one author address
    git log --format='%ce' | sort -u        # one committer address too
    git ls-files | grep -iE '(^|/)\.env$|\.pem$|\.key$|id_rsa|credentials'
    git grep -lnE '/home/<user>|[A-Z]:.Users.<user>' -- .    # personal paths
    grep -i '^copyright' LICENSE            # the publishing name, not a template's
    git for-each-ref refs/tags --format='%(refname:short) %(taggername) %(taggeremail)'
    git log -p --all | grep -inE '<words that must not be public>|[A-Z]:.Users' | head

Check annotated-tag taggers and the CONTENT of old commits, not just authors: a tag
made under another name or email, or a line removed three commits later, is still published
by `git push --tags`. While there is no remote, the cheap fix is one orphan commit.

A failing check stops the publication. Do not "fix it after the push".

## 3b. Make the repo look standard before the push

The usual goal is a repo "like every other one in its field, nothing more": simple, clean,
current conventions. Measure the peers instead of guessing — 8-15 well-known repos of the
same kind:

    curl -s https://api.github.com/repos/<r>            # topics, description, homepage, license.spdx_id
    curl -s https://api.github.com/repos/<r>/readme -H "Accept: application/vnd.github.raw" | head -40

- **Badges**: peers carry 0-5. Use the ones that are true on day one: latest release
  (`img.shields.io/github/v/release/<o>/<r>`), CI (`actions/workflows/ci.yml/badge.svg`), licence.
  Skip a downloads badge (shows 0 at launch), chat badges for a community that does not exist,
  and platform badges when the header avoids platform claims.
- **Topics and description are repo settings, not README content**: write them into a
  settings note in the job folder (description = the tagline, ~10-12 topics, social preview
  path) and apply them at first push with `gh repo edit --description ... --add-topic ...`.
  Platform words are fine as topics even when the header avoids platform claims.
- **Header = what the app does, never what it runs on.** Banner, tagline and social preview
  carry logo + name + one line; platform and hardware words go ONLY in Requirements, because
  support may widen later and a header is expensive to redo. Requirements state the first
  release's support plainly, with no roadmap hints. Never commit a future plan (a feature to
  add, a "Later" list) even briefly: a commit made and reverted is still in history; if it
  happens before any push, `reset --hard` + `reflog expire` + `gc --prune=now` and keep the
  note in the private notes file instead.
- **Public tree = code + tests + build/release files + classic repo files, nothing else.**
  Default rule: none of the fleet's working files go online. Keep: the app package, `tests/`
  (CI runs it; it builds trust), `.github/`, packaging + build script,
  README/LICENSE/CHANGELOG/SECURITY/INSTALL/third-party licences, README images, lockfile. Move
  OUT of git (copy byte-checked into an ignored private folder, then `git rm`): design system
  folder, SPEC, ARCHITECTURE, internal checklists, screenshot generator scripts, unused assets.
  Before moving a design folder, repoint the installer icon at an in-package copy. Strip
  bookkeeping from code comments too (job/QA ids, agent and owner names, card ids), keeping the
  technical reason. Move private folder names from `.gitignore` (public, reveals they exist) to
  `.git/info/exclude`. Verify with `git ls-files` top-level counts and one `git grep -i -E` over
  all internal tags = 0, then tell the owner the files still live in history until the
  fresh-history step. Ask only the real judgement calls (tests public? architecture doc
  public?) with a recommended default.
- **Verify every hardware or platform claim from the shipped code**, at the pinned version of
  any engine you bundle (its build recipe, not a grep over a binary). Say "untested on real
  hardware" until it is.
- **README screenshots are real captures of the real app**, never mockups (peers ship 1 hero
  shot + 2-4 feature shots; mockups read as marketing and rot when the UI changes). Use a
  separate demo data folder so the owner's own data never appears. Fill it first with content
  the owner already approved; create new demo content only to fill a real gap. Show the owner
  the shots before they go in. Review each shot yourself first and drop any that shows a claim
  the README avoids (speed numbers) or a result that does not match the input on screen. Capture
  at the window's normal size (e.g. 1280x800), not maximised: it surfaces cut text and bad wraps
  worth fixing; after such a fix, re-shoot the affected screenshot.
- **Before promising to "release" a media asset (tutorial, trailer), check it still exists**:
  `ls` the cut folder and the job log; a cut deleted by an earlier decision means "release"
  = produce from scratch. Say so with the real cost, and recommend shipping without it and
  linking it from the README later (a README link needs no new version).
- **Every image the README links must exist** (`grep -o 'src="[^"]*"' README.md`, `ls` each):
  a screenshot slot pointing at a never-committed file survives every text review.
- **Licence: research peers BEFORE recommending one.** The app code's licence is separate from
  the licence of anything it downloads at runtime (models, data); see the
  `dependency-licence-audit` skill. Give the owner the choice as A/B/C with what each permits,
  check bundled components' licences are compatible with the pick, and keep "open source" out
  of the README until a `LICENSE` file exists. Once chosen: fetch the canonical text and compare
  it with a well-known repo's raw LICENSE, set `license = "<SPDX>"` + `license-files` in
  `pyproject.toml` (then `uv lock --check`), ship `LICENSE` inside the installer (copyleft
  licences require it with binaries), and update the badge.
- **Decide how users learn about new versions BEFORE the first release**: first-release users
  with no update path never hear of later versions. A safe default: a manual "Check for updates"
  button (one GitHub `releases/latest` request only when pressed, links built from the repo
  constant, never from the response) + a `RELEASING` note with the fixed steps (bump version,
  CHANGELOG, test, build, install over the old one, tag `v<version>`, publish; pre-releases are
  ignored by `releases/latest`). No auto-updater for unsigned installers.
- **CI on GitHub** (free on public repos): hosted runners have no GPU, so CI covers lint, the
  full suite (hardware tests skip), the installer build INCLUDING the install/uninstall test a
  dev PC with the app installed cannot run, and a release workflow on tag `v*` that checks the
  tag equals the code version and creates a DRAFT release (the owner publishes by hand). Pin
  third-party actions to a commit SHA, minimal permissions, call the reusable workflow as
  `uses: ./.github/workflows/ci.yml`. Validate YAML locally (e.g. a one-off
  `uv run --no-project --with pyyaml` load); say plainly that nothing is proven until the first
  push runs it. Before relying on CI, make the suite stable: a test that fails one run in two
  locally turns CI red for no reason.
- **Hardware the fleet does not own**: cloud notebooks are Linux containers and cannot run a
  Windows installer; Windows cloud machines with a GPU are paid and need the owner's account.
  Friends' real machines are the best free test.

## 3c. Pre-release gate: critical product review, then a friends' test

Before the first public push of an app for non-developers, send product a READ-ONLY review
card (no edits): what the app is, target user, release scope, "no new features" phase, what
to read (README, SPEC, CHECKLIST, CHANGELOG, docs, workflows, UI, findings), and a fixed
output: BLOCKERS (what / why for this project / file:line / smallest fix), SHOULD fix, REMOVE
or simplify, ready for friends? for public? + a friends' test checklist, what was NOT
checked, ideas only under "Later". Then relay to the owner split into "I fix these" (no
choice needed) and lettered decisions (A-E, each with its risk and the coordinator's opinion)
they can answer in one line. Fix the non-decision blockers in parallel (coder for code, docs
for docs, separate worktrees) while the owner decides.

Blockers that recur in desktop apps — check them every time:
- **Uninstaller data loss**: never delete a whole folder under a user-picked data dir (it may
  hold another app's files). Delete only files the app recorded in a manifest it writes; when
  the setup wizard is pointed at a non-empty foreign folder, create an app-named subfolder
  inside it. Prove it with a real install/uninstall over decoy foreign files.
- **Acceptable use**: read the host's acceptable-use rules against what the app can produce,
  and put a plain usage rule in the README where it applies.
- **Dependency licences in their own words**: quote a restrictive licence's own words in the
  app and the README; do not paraphrase.
- **Name collision**: search the name in the same field (app stores, web, GitHub search API
  `search/repositories?q=<name>+in:name`) before publishing; renaming after users install costs
  the update URL, data folder and logo. For EACH candidate, before calling it "free": web-search
  the bare name in quotes, check `.com/.app/.io/.org` via `https://rdap.org/domain/<d>` (200 =
  taken), and fetch any live site (`<title>`, meta) to see what it is — a quick generic search
  misses same-name sites, and finding them after the owner picked forces a second round. Offer
  3 candidates with the meaning of each and what is already out there; say trademarks were not
  checked. If a collision turns up after the pick, stop before the rename and let the owner
  decide.
- **Renaming the app** (once the name is final): one coder card renames everything (package,
  env vars, installer, URLs; afterwards `git grep -i <old>` may only hit migration code) and
  migrates existing users without moving their data or deleting the old folder. Installing
  over the old app must leave ONE entry in the apps list and Start menu, data kept — tested in
  a throwaway dir only. The installer removes the old name's shortcuts with a short retry loop
  (a just-created shortcut is briefly locked by the shell or antivirus) and never runs the old
  uninstaller (it would ask to delete data). Brand work from the designer goes in after the
  rename merges, by copying its listed files onto the renamed paths in one commit: merging a
  branch cut before the rename fights the moved paths. Do not hand the owner the installer
  until the install-over-old test passes on the coordinator's own build, not just the
  worker's. Re-shoot README screenshots, rebuild, and rename the local repo folder LAST,
  after every worktree is closed. Tell the owner about any visible leftover (e.g. the program
  folder keeps the old name).
- **Peer-project study on request** ("what can we copy from X"): delegate a READ-ONLY deep read
  (code, installer, hardware detection, updates, CI, issues = what breaks for real users) with
  a shallow clone in scratch deleted afterwards, nothing of X executed; every idea classed A
  (small, cuts risk on other PCs, before v1) / B later / C don't copy, with why. A-items are
  still owner decisions under a no-new-features phase. "Is their logic more robust than ours?"
  is answered by fetching THEIR file raw and OUR code and comparing input by input, ending
  with our own unproven part stated plainly.
- **Unsigned Windows app that starts its own helper programs**: retry a rename for a few
  seconds on access-denied (antivirus scans a freshly extracted exe and locks it); catch the
  "blocked by policy" errors at every process start and say "Windows blocked <helper> (Smart
  App Control / AppLocker / antivirus)" instead of a generic crash, with an INSTALL section;
  log the helper's non-zero exit code in hex and put the app log tail in the diagnostic report.
  Code signing is a later item.
- **Honest messages**: an update check that cannot find any release (404, private repo) must say
  it does not know, never "You have the latest version".
- **Silent growth**: copies of user files need a cleanup rule (drop the ones nothing uses, at
  start, never during a job) and a line in INSTALL saying where they live.
- **Stale audience wording**: "private build for friends", placeholders, internal job notes in
  CHANGELOG. Rewrite CHANGELOG as one user-facing line per feature (it becomes the release
  page); add a bug-report issue form asking for the diagnostic report and system details, with
  a warning never to attach private data.

**Friends before public** when the app was tested on one machine only: a broken first run is a
public first impression that does not come back. Recommend a short friends' test on the
untested hardware, using the review's checklist; the alternative (publish as a pre-release,
marked as a test version) is acceptable only if the owner picks it.

**History cleanup happens right before the first push**, not while agent worktrees are in flight:
rewriting history under open branches breaks their merges.

**Rehearse the fresh history in scratch first** (safe while waiting on testers; the real repo is
not touched): `git archive --format=tar HEAD | tar -x -C <empty scratch dir>`, then there
`git init -b main && git add -A && git commit -m "<App> <version>"`. Check: `git ls-files`
top-level counts (only code/tests/packaging/docs/classic files), one `git grep -n -I -i -E` over
every internal word (old name, unannounced plans, job/QA tags, agent roles, kanban, private
folder names, user paths, card ids) — hits inside third-party licence texts and code identifiers
are fine, say so; image assets `grep -a -c` for embedded prompt/path text = 0; the full suite run
ON THE COPY (proves the public tree works without private files; check `pkg.__file__` points into
the copy). Write the procedure + result in the private pre-release notes, delete the copy (`cd`
out first, or the delete fails "busy"). The one open item to hand the owner: commit author name
+ GitHub noreply email.

**Friends' test logistics**:
- Give the test sheet as ONE copyable block in the format of the chat app the owner uses, not a
  file; trim lines that do not apply to these testers.
- Ship the installer zipped, check the zip entry name + size, record the installer sha256 prefix
  + build commit in the pre-release notes.
- If the app has hardware requirements, check each tester's machine against them before sending,
  and flag which tester covers the oldest supported hardware: that test matters most.
- Re-verifying the installer on the owner's PC cannot test a first-run-setup change: the setup
  already ran there. Say so, and say which part only a fresh install proves.

## 4. Create, verify, then push — three steps, not one

Do not pass `--push` to `gh repo create`: you lose the chance to inspect what
was actually created before the code leaves the machine.

    gh repo create <owner>/<Repo> --private --source=. --remote=origin
    gh repo view <owner>/<Repo> --json isPrivate,owner
    git push -u origin main

**Publish the first repo of a new setup as private**, whatever the end goal is.
It validates the whole pipeline — auth, remote, attribution — with nothing
exposed if a check was wrong.

## 5. Verify from the server's side

The local repo can be perfect while the remote is not. Check where the data
actually landed:

    gh api repos/<owner>/<Repo> \
      --jq '{private,visibility,owner:.owner.login,default_branch,description,homepage,has_wiki,fork}'

    # every commit attributed to the right account
    gh api "repos/<owner>/<Repo>/commits?per_page=100" \
      --jq '[.[] | .author.login] | group_by(.) | map({login:.[0], n:length})'

    # one author email in the remote history
    gh api "repos/<owner>/<Repo>/commits?per_page=100" \
      --jq '[.[].commit.author.email] | unique'

    gh api repos/<owner>/<Repo>/collaborators --jq '[.[].login]'
    gh api repos/<owner>/<Repo>/contents --jq '[.[].name]'
    git fetch -q origin && git status -sb     # no ahead/behind

**A commit can be "unattributed"** — the noreply email does not match the
account — and look perfectly fine locally. Only `author.login` from the API
reveals it.

**The social preview is a repo setting, not a file in the tree.** Upload it by
hand in Settings → General → Social preview → Edit; no commit sets it, so an
agent cannot. On a private repo that has never had one, GitHub hides the option
entirely — that is expected, not a missing permission; it appears once the repo
is public. Image: PNG/JPG under 1 MB, 1280×640 for best display. Keep the README
header and the social preview as separate decisions: a wide banner suits a link
card, while the README top can stay a plain logo.

**The repo's surface leaks as much as its commits.** `description`, `homepage`,
`topics`, Pages, wiki and collaborators all travel with the repo and become
visible the moment it flips public; leave them empty or off unless there is a
reason.

## 6. After a successful push

- The project now has a remote, so any "one copy only" rule is over: clones per
  OS become useful. What replaces it is `git pull` before working and
  `git push` before switching machines.
- Delete the pre-push `.git` backup for **that** repo only; keep the others
  until they are published too.
- Add `.gitattributes` with `* text=auto eol=lf` **before** the second clone
  exists, or CRLF/LF differences mark whole files as modified on the other OS.
- Do not add CI workflows to a private repo without asking — Actions minutes
  are free on public repos, metered on private ones.
- Update every place that tracks publication state: the rules file, the sibling
  agents' skills, each `CLAUDE.md`. "No repo has a remote yet" stops being true
  at the first push and a stale line there sends the next session down the
  pre-publication path.

## An editor session open on a rewritten repo must be restarted

After a `filter-branch`, a folder move, or any history rewrite, tell the owner to
close and reopen an IDE session (VS Code, Claude Code, an agent in a terminal)
that was running on that repo. Every commit SHA changed and the path may have
changed too, so any hash the session holds in memory now resolves to nothing and
the tool fails in ways that look unrelated to the rewrite. Open editor buffers
for files edited outside the IDE are stale for the same reason.

Verify before advising: `git status --porcelain` on the repo. Zero dirty files
means nothing is lost by restarting — say so, because the real question behind
"should I restart?" is "will I lose work?".

## When another agent performs the push

Give it the rules file to read first, the exact commands, and explicit stop
conditions ("if the account is not authenticated, stop and tell the owner"). Tell it
not to disable a guard that fires and not to redo work already done.

⚠️ **A completion report is a self-declaration.** Re-run the read-only `gh api`
queries yourself before telling the owner it worked — ten seconds, and the only real
evidence. When the report holds up, say so and name what the agent did well.

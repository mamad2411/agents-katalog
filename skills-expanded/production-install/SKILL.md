---
name: production-install
description: "Use when a dev tool meets the owner's real data. Pin, isolate."
version: 2.0.0
author: coder role of hermes-fleet-apps
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [install, deployment, launcher, uv, data-isolation]
    related_skills: [build-method, project-memory]
---

# Production install beside the dev checkout

Dev work and the owner's real data must never share a database, a venv, or a code
copy. Sharing one means a test run pollutes their data, and the next edit in the
repo silently changes the tool they rely on.

```
  launcher   ~/.local/bin/<tool>-real.bat   (already on PATH; one line)
     |- program   %LOCALAPPDATA%\<tool>-app\   own venv, pinned to a commit
     |- data      <path the owner names>\data\  via the tool's data-dir flag
  dev (untouched)  repo .venv + default data dir
```

The example is Windows (`.bat`, `Scripts/`). On Linux and macOS the launcher is a
two-line shell script in `~/.local/bin`, the venv has `bin/` instead of `Scripts/`,
and the program dir sits under `~/.local/share/<tool>-app/`.

## Procedure

1. **Ask the owner for the data location. Never guess a drive.** Then check free
   space (`df -h <drive>`) and say so if the disk is nearly full.
2. **Read how the data dir is chosen.** If the flag is GLOBAL (before the
   subcommand), the launcher is `tool --data-dir X %*`. If there is no env-var
   override, say so: the launcher is then the ONLY separation, and plain
   `tool` still writes to the dev data.
3. **Pin dependencies to what the tests passed on.** Run
   `uv pip freeze --python .venv/Scripts/python.exe`, drop the package itself
   and the test-only deps, and save the rest as a constraints file in scratch.
4. **Build the exact commit, not the working tree:**
   `git archive <sha> | tar -x -C <scratch>/src` then
   `uv build --wheel --out-dir <scratch>/dist <scratch>/src`.
   Prefer this over a `git+file:///...` URL, which is unreliable on Windows.
5. Run `uv venv <app> --python 3.11`, then
   `uv pip install --python <app>/Scripts/python.exe -c <constraints> <wheel>`.
6. Write the launcher with absolute paths, plus a comment naming the
   commit, the data dir and the program dir.
7. **Verify, all by running:**
   - From git-bash: `cmd.exe /d /c '<full path>\tool-real.bat --json <read-only cmd>'`.
     `cmd //c "x.bat"` opens an interactive shell, runs nothing, and still exits 0.
   - The new data file exists at the chosen path.
   - The DEV data file's size and mtime are unchanged.
   - `cmd.exe /d /c 'where tool-real'` resolves.
   - `<app>/Scripts/python -c "import tool; print(tool.__file__)"` points inside
     `<app>`, not the repo.
8. Sweep the scratch build dir and the constraints file. Leave pre-existing
   scratch files you did not create, and name them.

## Hand-over must say

- Type `tool-real` exactly where you would type `tool`. Plain `tool` = dev.
- Name any real-data command to HOLD OFF on while a known flaw is unfixed.
  The install is pinned to a commit without the fix.
- Upgrading means rebuilding from the new commit. Never an editable install
  pointing at the repo. See "Upgrading" below.

## Upgrading to a new commit

Only after the commit exists. The code on disk is not the thing being pinned.

1. `git archive <new sha> | tar -x -C <scratch>/<pkg>-<sha>`, then
   `uv build --wheel -q --out-dir <scratch>/dist <scratch>/<pkg>-<sha>`.
2. Install into the EXISTING app venv, and swap only the package:
   `uv pip install --python <app>/Scripts/python.exe --reinstall-package <pkg> --no-deps <wheel>`.
   `--no-deps` keeps the pinned libraries exactly as they were.
   `--reinstall-package` is needed because the version string often has not
   changed, and uv would otherwise skip the install as already satisfied.
3. Update the commit sha in the launcher's comment line.
4. Prove the install matches the commit by comparing a changed file against
   the commit itself:
   `diff <(git show <sha>:src/<pkg>/cli.py | tr -d '\r') <(tr -d '\r' < <app>/Lib/site-packages/<pkg>/cli.py)`.
   Checking the version string proves nothing, because it did not change.
   Then run one read-only command through the launcher.
5. Sweep the extracted tree and the wheel.

If the real install sat on an older commit while a known-bad path was being
fixed, tell the owner plainly that the upgrade makes that command safe to run on
real data now. Do not only report the new sha. Record the install in the project's
private docs at the next commit, not ahead of the code.

## The first real run after an install or upgrade

- Check what the destination already holds (`ls`, file count) and free space first. A
  folder the owner filled by hand must be skipped by the tool, never merged into.
- Run it as a tracked background process, `--json` to a scratch file, stderr to
  another. A `--json` run may print nothing until the end: poll the PROCESS
  (`process wait`), not the output folder, and never loop identical `sleep` calls.
- Report counts per outcome, the undo id, and that the database and the source were
  untouched (by `ls`, not by assumption). Delete the scratch JSON, unless the owner
  still has to review it (a dry-run plan): then name its path and sweep it once they
  have decided.

## The first real dry run of a command that moves or rewrites files

1. **Size the input before running.** `find <dir> -type f | wc -l`, extension
   counts, `du -sh`, subfolder count. Warn if the folder is large, and never pick
   the folder yourself.
2. **Get every required argument from `<tool>-real <cmd> --help`** and ask for all
   of them in one question, with your best guess for the ones prior runs imply.
3. Run it as a background process, stdout and stderr to separate scratch files, then
   `process wait`. Plain-text output is enough when it carries the per-file plan and
   the totals.
4. **Summarise without surfacing personal data.** Parse the scratch file in code:
   mask names with a regex, number private labels (L01, L02, ...) by count, bin the
   scores near the decision threshold, and check that the bucket totals add up to
   the input count. Never open the owner's personal files.
5. **Prove "nothing moved" and explain what the dry run DID write.** Re-count the
   source files. List the tool's run/journal dir: a new file there may be the saved
   plan. Read its head for a `dry_run: true` flag before reporting, because a new
   journal after a dry run otherwise looks like an accidental apply. Index rows a
   scan added to the real database are expected; say so.
6. **Hand the owner a VISUAL check, never a text plan,** when the files are images or
   documents a person judges by eye. A filename list cannot be judged, and nobody
   reads hundreds of lines. Write one static HTML page from the saved plan: one row
   per group, weakest score first, scores coloured by band, files linked in place
   (`file://`), nothing copied. Open it for them and also print the path. The agent
   still never opens the files; the page only links them.
7. Hand-over as a tree diagram (input -> each outcome -> destination or "stays"),
   the preview path, and the next choice: `--apply` only with the owner.

## After `--apply`

- Verify from the NEW journal, not the printed summary: moves == done, 0 errors,
  every destination exists, every source gone, and the counts match what the plan
  said. Quote the undo id.
- Read the journal's list of created folders too, report each with its file count,
  and state the cost: once the owner moves one by hand, that run's undo can no longer
  restore those files.
- A server the owner uses to review results (a local page) runs as a silent
  background process; read the port from its first output lines, give the URL, and
  stop it only when they say they are done.
- **A UX bug the owner reports mid-review is logged, not hot-fixed.** The page is
  served by the pinned install, so an edit in the repo changes nothing they see. Make
  it its own roadmap step (TDD, commit, rebuild the install), then keep going.

## Pitfalls

- **Inspecting the real database creates files.** Opening a WAL-mode SQLite file,
  even with `mode=ro`, can leave `-wal`/`-shm` side files beside the owner's data.
  Open it as `file:<path>?mode=ro&immutable=1` (URI mode) or query a copy in scratch.
  If side files appear anyway, check that they are empty before removing them, and
  report it.
- **A handoff's description of real data is a claim, not a fact.** "Folder X is
  empty" or "the database is empty" gets checked with one `ls`/count before any
  design relies on it: a hand-filled folder changes the design (never write into it).
- **Which store is the REAL one is a claim too: find every candidate first.** Once a
  production install exists, the tool's default data folder is the DEV store and the
  real one is wherever the launcher's `--data-dir` points. A handoff can call the dev
  store "real", and every later "real db unchanged" check then guards the wrong file.
  At the start of any job touching data: read the project's instruction file for the
  named real folder, list every store (default dir, launcher target, data-dir flags in
  private scripts), and if two disagree with the handoff, ask the owner which is real.
  Check size + mtime of ALL of them before and after, report each by path, and write
  the answer into the project's AGENTS.md (one place) so the next handoff cannot drift.
- **The owner may run the app from the DEV checkout against real data.** A window
  started from the repo venv with `--data-dir <real>` loads the code once at start, so
  uncommitted edits reach the real data the next time it starts. At job start, list
  processes whose command line carries the real data dir (on Windows, PowerShell
  `Get-CimInstance Win32_Process`, read `CommandLine` and `CreationDate`). If one is
  running, say so: close it while work is uncommitted, restart it only after a
  commit, or better, use the pinned install. When cleaning up, kill only processes
  whose command line names YOUR scratch data dir, never a broad match on the tool
  name.
- **When the real store changes mid-job, attribute it before reporting it.** Re-check
  its size and mtime at EVERY stop report, and lead the report with any change. A
  `*.schema<N>-backup-<date>.db` beside it at the old size is the tell of a schema
  upgrade: some process opened it with newer code. Read-only, and without echoing the
  owner's paths: read the command lines of the processes using the real data dir;
  list the newest files in its run folders; count mentions of your own markers
  (scratch path, synthetic names) in any new run record — zero mentions plus a
  process of the owner's own = their activity. Read the database and its `-wal` as
  ONE store: a `-wal` that vanished while the main file grew by about its size is a
  checkpoint, usually the last connection closing. Report it and ask the owner to
  confirm; it stays unconfirmed until they do. Attribute every relayed check to the
  agent that ran it, never to the owner.
- **The owner's real data is never the test bed.** A known-bad path gets fixed,
  committed, and upgraded into the real install BEFORE the owner runs it on real
  data. Meanwhile they can prepare the inputs: say so, so they are not left idle.
- **Answering data-model questions from memory.** What a name may look like, how to
  lay out folders: read the schema or the sanitiser first and cite it. When the
  answer is no, say whether the feature is worth building, name the adjacent gap
  that matters more, and park it in the roadmap with its open questions.
- **Recommending a convention without the reason.** Give the naming rule AND the
  mechanism that makes the alternative bite: spaces need quoting in the CLI, and
  case-sensitive UNIQUE names split one thing in two.
- **A delete-then-rebuild on real data runs per item, back to back.** Dry-run the
  delete, check what it lists, apply it, and rebuild that one item at once. Between
  the two the item is empty, so a failed rebuild leaves it broken; confirm the count
  afterwards.
- **Write launcher paths with forward slashes or literal names, never `\\$var`
  inside double quotes.** Bash reads `\\$n` as an escaped dollar, so the tool receives
  a literal `$n`. Windows accepts forward slashes; or skip the loop and pass literal
  paths.
- **Renaming the owner's real folders** in bulk is a table they edit plus a
  propose/apply/undo script, never a guess and never a product feature.

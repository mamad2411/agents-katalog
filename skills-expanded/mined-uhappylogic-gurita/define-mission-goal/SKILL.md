---
name: define-mission-goal
description: Create a new mission directory with its three starting files from the provided goal description.
---

# define-mission-goal

Creates a new mission directory at `<scope>/mission_<slug>/`, directly in the scope you name, holding the three files every mission starts with — `requirements.md`, `open_questions.xml`, and `TASKS_TODO.md` — all created by the plugin's mission-definition tool, which also derives the directory name from the title. Your work is checking the workflow's two runtime prerequisites, choosing the mission's title, handing the tool's output to the commit procedure, and reporting the result; the files are filled in by the skills that follow (`/specify-mission-starting-state`, `/review-mission-requirements`, etc.). This skill never updates `AGENTS.md`, and it activates nothing: every later skill is aimed at the new mission by being given the path the tool printed as its `--mission <path>`.

## Usage

```
/define-mission-goal --at <scope> <overall_goal_description>
```

- `--at <scope>`: required, with no default — the directory holding the core of the mission's work, relative to the workspace root, `.` for the root. Use the directory `/discuss-mission-goal` proposed, as given; it must already exist.
- `<overall_goal_description>`: a clear description of what the mission should accomplish. Use `/discuss-mission-goal` first if the goal is still vague.

**Example:**
```
/define-mission-goal --at docs add a getting-started guide that walks a new user through their first session
```

## Workflow

### 0. Check the prerequisites

The workflow's skills commit their own changes with git and run the plugin's stdlib-only Python tools, kept in its `tools` directory, as `python3`, so the workspace root must lie inside a git work tree and a Python 3.9 or later interpreter must answer as `python3`. Check both here, on every invocation, before reading the scope and before the definition tool is called: git first, then Python, each stopping before any write on its own fixed line. A project failing both learns about git first and about Python on the next run.

**Git.** Run `git rev-parse --is-inside-work-tree` once, in the workspace root. If it prints `true`, the check passes: continue to the Python check. It passes anywhere inside a work tree — a subdirectory of a larger repository, or a freshly initialized repository with no commits yet — with no existing commit required, no match with the repository's top level required, and no advisory printed when the two differ.

Otherwise — the shell reports `git` as not found, or the probe prints `false` or fails with a not-a-repository error — **stop before any write**: create nothing, prompt for nothing, and never run `git init` yourself. Print one full message whose first line is the fixed line

```
Mission not defined — no git work tree at the workspace root.
```

and whose lines below it state, in order:

- **What it looked for** — a git work tree at the workspace root.
- **What it found** — that the `git` executable is missing, or that the directory is not a work tree.
- **The remedy** — install git when the executable is missing; otherwise run `git init` in the workspace root.
- **That a re-run defines the mission** — once the remedy is applied, run `/define-mission-goal` again with the same arguments; it picks up with nothing to undo, since this stop wrote nothing.

**Python.** Run `python3 --version`. If it prints a version of 3.9 or later, the check passes: continue to step 1. Compare the version numerically, minor by minor — `3.10` and `3.13` are later than `3.9`, `3.8` is not.

Otherwise — `python3` is not found, or it reports a version below 3.9 — run `python --version` as well. Its result decides nothing about passing; it only makes the message below precise. Then **stop before any write**: create nothing, and print one full message whose first line is the fixed line

```
Mission not defined — no suitable python3 interpreter.
```

and whose lines below it state, in order:

- **What it looked for** — a Python 3.9 or later interpreter answering as `python3`, and failing that as `python`.
- **What it found** — for each of the two names, that it was not found or the exact version it reported.
- **The remedy** — when `python` reported 3.9 or later, that interpreter exists under the other name and must be exposed as `python3` (a `python3` symlink or alias on the PATH, or the platform's equivalent); otherwise install Python 3.9 or later so that `python3` resolves to it.
- **That a re-run defines the mission** — once `python3 --version` reports 3.9 or later, run `/define-mission-goal` again with the same arguments; it picks up with nothing to undo, since this stop wrote nothing.

### 1. Read the scope

The flag is present only when the first whitespace-separated token of the invocation text is exactly `--at`. Its value, `<scope>`, is the token right after it; strip those two tokens and the whitespace following them, and what remains is `<overall_goal_description>`. Take `<scope>` verbatim: normalizing it, and refusing a scope that is absolute, climbs out of the workspace root, or is not an existing directory, is the tool's. When the first token is anything else, or `--at` has no token after it, **stop without changing anything** and report the fixed line `Mission not defined — no --at scope was given.` first, with the usage line `/define-mission-goal --at <scope> <overall_goal_description>` below it.

### 2. Choose the title

Read `<overall_goal_description>` and choose a short title that names the mission's objective (e.g. `Getting-started guide` for the example above). The tool derives the directory name from the title's first words, so lead with the words that identify the mission.

### 3. Create the mission

From the workspace root, run the tool once, passing the scope and the title each as one quoted argument and `<overall_goal_description>` unchanged on standard input through a **quoted-delimiter heredoc** (`<<'EOF'`, so nothing inside is expanded; pick a delimiter line the goal text does not contain):

```
python3 ${PLUGIN_ROOT}/tools/define_mission.py --at "<scope>" --title "<title>" <<'EOF'
<overall_goal_description>
EOF
```

On success the tool prints exactly two lines: the commit subject, then the mission's path, in its canonical repo-relative form with its trailing slash. Hold both unchanged for step 4; compose, reword, and re-derive neither.

If the call fails — the shell cannot find `python3`, or the tool exits non-zero with one `Error: <reason>` line on stderr — stop here and report it in full: the fixed line `Mission not defined — the definition tool failed.` first, then the shell's or the tool's line verbatim below it. The tool leaves nothing behind on failure, so there is nothing to clean up and nothing to commit.

### 4. Commit the new mission

Read and follow the shared commit procedure at `${PLUGIN_ROOT}/shared/commit-procedure.md`, running its one commit-tool command yourself as this step's one git tool call. Supply it these two inputs, both exactly as the tool printed them in step 3:

- **PATHS** — the mission path, the tool's second line; the directory holds exactly the three files the tool just created.
- **SUBJECT** — the tool's first line.

The commit tool runs the dirty-own-path guard, the path-scoped staging, and the commit.

### 5. Confirm

On the success path — the commit in step 4 recorded the new mission — print exactly one fixed terse status line and nothing else:

```
Mission defined.
```

Do not add the created directory path, the title, the goal text, or a next-step pointer.

If instead the step-4 commit tool printed `Nothing committed — none of the paths changed.` (nothing under the mission directory changed, so nothing was committed), do not print the terse line — print this one fixed line and nothing else:

```
Mission not committed — its directory held no uncommitted file.
```

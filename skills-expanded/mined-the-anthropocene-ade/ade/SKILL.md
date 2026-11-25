---
name: ade
description: Use for anything about running or configuring ADE (the ade verbs, cards, the loop, ade.toml settings), before building loop, hook or harness machinery around ADE, and before quoting ADE figures (landings, product-work share, usage)
---

# Using ADE

Start with `ade handover --role ROLE`. Verbs:

- `ade budget`: print core lines, hooks, refusal codes and tests against their budgets; fails when a hard row is over (component rows are notes); --refusals counts firings
  `ade budget [--refusals] [--tests]`
- `ade card`: add, list, show, hold, close, snooze and re-path cards; a card needs paths and a done line, and a recurring one opens again every N days
  `ade card add TITLE --path GLOB --done TEXT [--every DAYS] [--proof CMD] [--hold REASON] [--profile NAME] [--why TEXT] | ade card draft SENTENCE | ade card list [--free] | ade card show ID | ade card hold ID REASON | ade card close ID --why TEXT | ade card snooze ID --until DATE|Nd | ade card paths ID --path GLOB [--path GLOB ...] [--add]`
- `ade cockpit`: the pilot's view: every open card with its state and next command, plus budgets; orca mode opens it in Orca too
  `ade cockpit [--mode cli|orca|auto] [--follow] [--every SECONDS]`
- `ade conduct`: walk the board through `ade loop` until no open card is left untried, one card at a time or several whose reach the graph keeps apart; route every stop by ade/route.toml, wake a model only where the route says wake. Pilots: run it as a background task, and keep working: the flight band (Claude Code) or the cockpit terminal shows each stage, and the background task's own finish is the one wake; safe because each lane builds in its own worktree and branch, tests run in a detached checkout, and land waits only if the main checkout has uncommitted edits to the very paths the card changes or if the main checkout is not on the trunk branch, so do not edit a flying card's paths and keep the main checkout on trunk
  `ade conduct [CARD ...] [--lanes N] [--follow [--rounds N]] [--check] [--model ROLE=ENGINE:MODEL] [--effort ROLE=LEVEL] [--json]`
- `ade config`: list ade.toml's sections, or look up every key matching a word with its effective value and template comment
  `ade config [word] [--roles | --seats | --refusals | --probe [--guards]]`
- `ade decide`: rulings that govern path globs, and questions for a person with a recommendation, a default and a deadline
  `ade decide --path GLOB TEXT | ade decide --standing TEXT | ade decide --import FILE.jsonl | ade decide --ask TEXT --rec R --default D --by DATE|Nd [--card CARD] | ade decide --answer ID TEXT | ade decide --retire ID --why TEXT [--superseded-by ID] | ade decide --list|--rulings|--queue|--desk|--show ID`
- `ade digest`: one short summary of a day: cards landed, cards parked with their open question, questions whose default applied; then any rule 7 lines (at most 3)
  `ade digest [--day YYYY-MM-DD]`
- `ade graph`: regenerate the graph file from headers and imports, or with FILE print that file's briefing from a fresh graph; --check fails if the committed one is stale or the route has drifted
  `ade graph [FILE] [--check] [--route]`
- `ade handover`: generate a role's working context from records and graph; prints its token estimate, fails over budget
  `ade handover [--role R]`
- `ade hook`: Claude Code hook entry: brief (first-edit briefing, protected paths), bash (the guard), read (secret Read/Grep under tracked: secret_ok), grep (graph notes on search output), turn-end (holds), start (handover)
  `ade hook brief|bash|read|grep|turn-end|start  (stdin: the hook event's JSON)`
- `ade init`: start a new project in an empty folder, or install or refresh ADE in a repo from ade.toml; idempotent, --dry-run prints the diff
  `ade init [--starter python|typescript] [--dry-run] [--yes] [--no-commit]`
- `ade land`: land a card whose lane tree has an approved review and passing tests: merge, verdict, outcome
  `ade land CARD [--catch-up]`
- `ade link`: make a plain `ade` work in new shells: one small launcher named ade in a per-user folder already on PATH
  `ade link [--dry-run] [--force]`
- `ade loop`: drive a card through lane, build, review, test, land; journal each stage, stop at the first non-advance. Pilots: run it as a background task, and keep working: the flight band (Claude Code) or the cockpit terminal shows each stage, and the background task's own finish is the one wake; safe because the lane builds in its own worktree and branch, tests run in a detached checkout, and land waits only if the main checkout has uncommitted edits to the very paths the card changes or if the main checkout is not on the trunk branch, so do not edit a flying card's paths and keep the main checkout on trunk
  `ade loop CARD [--model ROLE=ENGINE:MODEL] [--effort ROLE=LEVEL] [--hold-land] [--json]`
- `ade parts`: list the parts catalogue with each part's state; `set x=off` (or `x=on`) switches one in ade.toml and prints what it costs
  `ade parts [set ID=off|on [--why REASON]]`
- `ade push`: push trunk, ade-records and checkpoint tags to the remote (under [git] push = "pr", only ade-records and tags, never trunk or its mirrors); fast-forward only, never forced; waits for .ade/land.lock (a landing in progress) first; --dry-run asks the remote without pushing
  `ade push [--dry-run]`
- `ade q`: keep long output out of a model's context: run a command through the store, page or grep what it kept, query it
  `ade q run -- CMD | ade q show ID [--page N] | ade q grep ID|all PATTERN | ade q sql QUERY | ade q list`
- `ade rehearse`: one full loop per config option on throwaway repos with the fake provider; reports calls, wall time and refusals
  `ade rehearse [--only NAME] [--keep] [--coverage]`
- `ade session`: run an ade verb detached from this terminal (no tmux, any platform), list sessions live or ended, follow one, stop one
  `ade session start NAME -- VERB [ARGS] | ade session list | ade session attach NAME [--follow] | ade session stop NAME`
- `ade setup`: a terminal panel to switch the kit's parts on and off; shows the ade.toml diff first, saves through parts.rewrite; a numbered list when there is no terminal or NO_COLOR is set
  `ade setup`
- `ade status`: one-line state for the Claude Code status line: repo, open cards, last stage outcome
  `ade status [--line]`
- `ade telemetry`: show usage per card and per provider for the week, each week meter against its share; export OTLP files locally; --week: the 7-day burn from this machine's transcripts
  `ade telemetry [export] [--flights] [--outcomes [--since DATE]] [--week [--json] [--since ISO]]`
- `ade uninstall`: remove everything `ade init` generated (hooks, rules, agents, AGENTS.md block, graph); keep ade.toml and records
  `ade uninstall [--dry-run]`
- `ade wait`: wait for a condition with a bound (exit 0 met, 3 stage parked, 4 bound passed, 5 lane stalled); run it in the background to be told; `stage` is a condition for a pilot that needs to block on one stage
  `ade wait clean|journal CARD|stage CARD lane|build|review|test|land|answered ID|exit PID|file PATH|time 10m [--bound 30m] [--lane CARD]`
- `ade watch`: follow a card's lane log live (any platform, no tmux) until its loop stops or the log goes quiet; --once prints it
  `ade watch CARD [--once | --until-landed]`

ade.toml sections (a section you leave unset takes the kit default):
  [git]  How ADE uses git: trunk, pushing and pull requests.
  [tests]  How a project's tests are run, found for a change and retried when they fail.
  [lanes]  How each card's separate checkout gets the folders it needs without installing them again.
  [rigour]  Which paths get the full test suite and which paths land without review.
  [graph]  How ADE maps the code, its tests and its docs, and what it requires of each changed file.
  [guards]  Which secret files and which shell commands the guards refuse to read or write.
  [protected]  The paths an agent may not edit, and what it is told to do about them instead.
  [land]  Which changes wait for a person's answer before they land.
  [budgets]  The size limits that keep the kit and its briefings small.
    [budgets.components]
  [providers.*]: [providers.claude], [providers.codex], [providers.opencode], [providers.pi]
  [review]  How a lane's diff is reviewed, and by which engine.
  [conduct]  How ADE's conductor routes stops, waits and parks a card, and how much it may spend in a day or week.
  [cards]  How long a drafted card waits for a veto before it flies.
  [watch]  How long a lane may go silent before the watcher calls it stalled.
  [q]  How long output is stored and how much of it is shown in full or as a short excerpt.
  [cockpit]  Which view shows the lanes while the board runs: the terminal alone or a mirror in another app.
  [report]  Whether each engine call records the seat it ran with in its lane log.
  [usage]  How ADE measures and prints each provider's share of the week and the plan behind it.
  [roles.*]: [roles.pilot], [roles.builder], [roles.reviewer]
  [parts]  Which optional parts of the kit are switched off in this project.
    [parts.override]
  [permissions]  The permission modes ADE writes for your own sessions and for the lanes.
    [permissions.allow], [permissions.deny]

Look up any setting with `ade config WORD`. ade.toml is protected: you may run `ade parts set` (and `ade setup`); name any other key to the person, who changes it and reruns `ade init`.

Where things belong:

- Rules that matter only on some paths go in `ade decide` rulings (just in time), not AGENTS.md.
- Figures (landings, product-work share, usage) come from `ade digest` and `ade telemetry`, never estimated.
- Read the rule book before adding to it: `ade decide --rulings` prints every live ruling and the counts against the limits. A ruling due for review still governs, and is answered `keep` or `retire: WHY`.
- Direction, values and what the person reserves go in standing rulings (`ade decide --standing TEXT`), written only when the person asks; from any seat but a person's own terminal it is a proposal, which governs nothing until they answer `stand`.
- Never answer a question as the person; tell them it waits (`ade decide --desk`).
- A figure in prose or memory is stale, so rerun the command that owns it before quoting it.
- On Codex, OpenCode and Pi a `[roles.<role>]` system_prompt file leads the whole prompt (Claude Code appends it), so give the reviewer its own file rather than the builder's brief.
- Under `[conduct]` answerer = "agent" an agent may also make a standing proposal stand; a seat that leaves stand to the person stays off `ade decide --answer dN stand`.
- Settings are looked up and explained by `ade config WORD`; do not copy them into prose.
- A go-ahead an agent relays (chat or a page) is not the person's land; an agent's `ade decide --answer dN land` counts only under `[conduct] answerer = "agent"`, which stays "person" (the default) unless the person sets it, and then an agent's land clears the `[land]` ask paths, except that a card that changes `ade/install.py` waits for a person whatever answerer says (`land.asked`, `own_generator`); otherwise the person answers in their own terminal.
- After pulling a new kit, a person runs `ade init`.
- The kit version is what `ade --version` prints; take it from there, not from memory or a file.
- `ade init` warns when a `[guards] secrets` glob hides tracked code from agents and reviewers; narrow the glob or allow it with `[guards] secret_ok` (`tracked:GLOB`).
- `ade card close ID --why TEXT` is final: the card is retired and conduct never flies it again, so close only a card that will not be done.
- A card whose done line needs a browser, an idle machine, a person or paths outside the repo is added with `--hold`.
- A card's `--done` is when it is finished, and the proof: usually a command's output, a page, a figure or a runtime log (a rehearsal line counts); keep a test only for a lasting hazard. `--proof CMD` makes land run the proof itself.

Good and bad calls:

- Good: `ade card add "t" --path 'src/*.py' --done "..."`. Bad: unquoted `--path src/*.py`; zsh on macOS aborts with 'no matches found' or expands the glob into several args.
- Answers to land questions: `ade decide --answer dN land` | `ade decide --answer dN 'rework: TEXT'` | `ade decide --answer dN drop`.
- Answers to retry questions: `ade decide --answer dN retry` | `ade decide --answer dN 'retry: NOTE'` | `ade decide --answer dN drop`.
- Answers to accept questions: `ade decide --answer dN accept` | `ade decide --answer dN retry` | `ade decide --answer dN 'retry: NOTE'` | `ade decide --answer dN drop`.
- Quote a note: an unquoted note is split at its spaces.
- Good: `ade q run -- CMD`, which keeps long output whole. Bad: piping long output into your context.

Before you build machinery around ADE, check this skill, `ade config` and `ade parts`; if ADE lacks it, raise it with the kit's maintainers.

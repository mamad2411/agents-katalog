---
name: agent-launcher
description: "Create coding-agent sessions with the local `agents` wrapper — one named tab in the current Herdr workspace, a crew, a machine or team view, a fleet layout, or a Hermes profile — including model, provider, permissions, working directory, and machine routing. Use when the user asks to launch, start, add, or open a Claude, Codex, Grok, Muse, OpenCode, Qwen, Agy, or Hermes session, or to open a machine/team/fleet view. Creation only: use the `herdr` skill for every interaction after the session exists. Do not use merely because a task could benefit from delegation or parallel work."
---

# Agent launcher

`agents` is a local wrapper at `~/.local/bin/agents` that creates agent sessions and Herdr views. It is a creation tool, not an interaction tool.

**Depends on:** the canonical `herdr` skill for every interaction after the session exists. This plugin does not ship a copy of that skill. After the creation command returns, switch to `herdr` and stay there.

**Scope boundary — this is the rule the whole skill hangs on:**

- `agents` **creates** a session: tab, pane, working directory, model, permissions, machine.
- `herdr` **operates** it: prompt, wait, read, send keys, close.

Never use `agents` to prompt, poll, read, or clean up an agent that already exists.

## Verified launch (preferred)

For one named tab that must be previewed, no-focus, directory-preserving, and receipt-recorded, use the plugin script rather than assembling `agents` by hand. Orchestrate uses this same file; there is no second implementation.

```bash
S="$CLAUDE_PLUGIN_ROOT/skills/agent-launcher/scripts/launcher.py"
[ -f "$S" ] || S=$(ls -d ~/.claude/plugins/cache/*/agent-launcher/*/skills/agent-launcher/scripts/launcher.py | sort -V | tail -1)

python3 "$S" preview --vendor <tool> --task <tab-name> --cwd "$PWD" --model <model> --effort <effort>
python3 "$S" launch  --vendor <tool> --task <tab-name> --cwd "$PWD" --model <model> --effort <effort> --prompt <text> > receipt.json
python3 "$S" close --receipt-json receipt.json
```

The launch line carries a real prompt: without one, the session never leaves idle, delivery is recorded as failed, and the command exits nonzero.

`launch` always dry-runs first. It writes one JSON receipt to stdout (redirect it to `receipt.json` as above). It verifies live Herdr state (kind, pane, cwd, workspace, readiness) before any prompt is sent. Model stays `requested_only` because `herdr agent list` does not publish it. Herdr publishes no permission either, so a non-empty permission flag sequence is confirmed against the launch argv and recorded under `permission_resolved`; vendors whose selected posture has no distinguishing tokens record `confirmed_from: null`. `close` reads `tab_id` and `owned` from that file. `owned` is true only when the receipt `tab_id` was **not** in the target Herdr workspace tab set snapshotted immediately before the wrapper ran. The wrapper's `reused` bit means the *workspace* already existed, which is the common case inside Herdr, and is not tab ownership. Closing an owned tab is idempotent: if the tab is already absent from that workspace, cleanup succeeds.

Permission is granted at launch and is not assumed correctable in place. Claude's live permission
control cycles through manual, accept-edits, plan, and auto; it cannot promote an `auto` session to
`bypass`, so relaunch Claude when the requested posture differs. Other vendors have their own
controls and must not inherit Claude's four-name ladder. Agy, not OpenCode, uses
`--dangerously-skip-permissions` for bypass.

Every line that enters a session — each setup slash command, the task, each resend, both keystrokes of the OpenCode variant picker, and every prompt Orchestrate sends later — goes through one door, `PaneWriter.write`, and that door inspects the input box immediately before the write whenever the write could land behind text a person staged: before the first write into a session whose tab the launcher did not create (`owned` false in the receipt), and before every later write into any session, owned or not, once this launcher has written into it. The one write that is never inspected is the first write into a tab this launcher created seconds earlier; on OpenCode that first write is the picker opening, so the variant selection and the task are both inspected. A read taken while the picker is on screen classifies the picker rather than a draft and is recorded as an inconclusive inspection under the trade described below — taken, not skipped. Callers go through `PaneWriter.write`; the two Herdr doors are nested functions inside that method, not attributes. The structural test nets the enumerated AST shapes; it does not prove every dynamic Python call is impossible. A prompt typed behind staged text concatenates onto it and can submit it. Staged text is a stop, not a clear: the launch refuses to prompt and records a redacted characterisation of the box in the receipt and the unit note, naming that the text itself was withheld; nothing typed by an operator is persisted, and nothing in the box is discarded. `input_box_text_chars` is the visible length of what the parser absorbed: visible characters after border stripping, rows joined without a separator — one character short at each wrapped-row boundary — and, when a blank line inside the draft ends the absorption, a lower bound of the draft's true length. The box is the last marker block positionally, so an earlier scrollback echo never stands in for a lower live box. Composer markers are characterised for Claude, Codex, Grok, Agy, and Qwen; checked-in pane captures exist only for Claude and Codex, so Grok, Agy and Qwen footer shapes are unverified. Muse and OpenCode have explicit unsupported entries because no stable marker was available in the verified captures. Indentation and blank rows are not authorship signals: when they make an otherwise empty box ambiguous, the receipt says `unclassifiable` rather than falsely claiming `empty`. The accepted asymmetry runs the other way too: an unbordered indented row directly below the marker with no separator row between is read as input, because no capture shows chrome there; the stop is fail-safe.

The serialized receipt carries the result of the last inspection under `input_box`. A fresh owned launch whose first prompt was taken made no inspection, so its receipt carries no `input_box` key; an owned session that needed a resend, or that was redelivered after a staged-input stop, was inspected and its receipt carries the key. Its complete value set is `empty`, `staged`, `unclassifiable`, `not_found`, `unsupported_vendor`, `read_failed`, and `read_timeout`. Only `staged` also carries `input_box_text_chars`, the redacted count used in the stop message; no receipt field carries the text. `read_failed` and `read_timeout` refuse the write: they are the absence of an observation, not styled-composer ambiguity. `unclassifiable`, `not_found`, and `unsupported_vendor` remain fail-open. In particular, a real operator draft rendered entirely inside the client's styling is byte-identical to a styled placeholder, so it is recorded `unclassifiable` and the prompt proceeds. A stronger guarantee needs an independent signal such as cursor position or a vendor-published composer state; the launcher does not guess.

**Stop conditions (verbatim):**

- Stop before launch if the wrapper dry run does not resolve the requested working directory and current Herdr workspace.
- Stop before prompting if Herdr cannot verify the requested agent kind, pane, working directory, workspace, and readiness. Model and effort stay requested-only except for OpenCode's read-back variant. Permission is checked against distinguishing launch tokens when the vendor has them, and account proof exists only for Claude. A disagreement on any published or discriminating field is a stop.
- Stop rather than silently substituting an unavailable agent or launch setting.
- Stop cleanup if ownership of the target session cannot be proven (no `tab_id`, `tab_id` disagrees with the launch receipt, or `owned` is not true — the tab already existed in the pre-launch snapshot).
- Stop before prompting if the input box holds staged text. The session, tab and receipt are kept; the recovery is `redeliver` below, never a second `launch`.

**Retry after a staged-input stop.** The stop is retryable through the same pane and only through it: running `launch` again creates a second session and overwrites the first owned tab in the receipt. Clear the composer by hand, then:

```bash
python3 "$S" redeliver --vendor <tool> --task <tab-name> --cwd "$PWD" --prompt <text> --receipt-json receipt.json > receipt-retry.json
```

`redeliver` takes the tab, pane and ownership from the receipt the stop wrote and the task and launch settings from the same flags `launch` took. Two receipt shapes are retryable: a staged-input stop (`input_box` is `staged`) and a prompt that was sent but never observed to be taken (`prompt_delivered` is `false`). It refuses, before any Herdr call and with exit code **2**, an empty `--prompt`, a receipt missing `unit_name`, `pane`, `tab_id`, `owned`, or `agent_name`, a receipt written for a different task name, a receipt that already delivered the prompt, and a receipt that records neither retryable shape. It never runs the wrapper create. It inspects the pane before its first write whatever the ownership, and it refuses to prompt a session that has visibly started since the stop (any Herdr status other than idle or unknown, including `done`), because that session may already hold the task; that refusal is recorded on the receipt as `prompt_delivered: false` and the command exits **1**, as does any retry whose prompt was not observed to be taken. A delivered retry exits **0**. Orchestrate uses the same door: rerun `go` and a unit stopped on staged input is redelivered into its recorded pane rather than launched twice, and `redrive --unit` re-prompts a unit recorded `prompt_undelivered`.

## A whole roster from a run record

One session at a time is the launcher above. A whole set of role sessions for one issue is
`roster.py`, beside it in the same directory. It is the only supported path from a run record's
staffing plan to a set of live role sessions; do not assemble one by hand from `launch` calls.

```bash
R="$CLAUDE_PLUGIN_ROOT/skills/agent-launcher/scripts/roster.py"
python3 "$R" up   --record <absolute run-record path> --dry-run   # prints; creates nothing
python3 "$R" up   --record <absolute run-record path>
python3 "$R" wait --record <absolute run-record path> --timeout 600000
python3 "$R" down --record <absolute run-record path>
```

`up` reads `run_configuration.staffing_models_and_efforts` from the run record, resolves each role
to its prompt in `plugins/agent-launcher/roles/`, and creates one named pane per role **through
the launcher above** — so every pane carries an ownership receipt. It records each pane in the run
record's `roster` array as a `roster_entry.v1` row before it launches the next one, and it is
idempotent per role: re-running it after an interruption repairs the roster rather than doubling
it. `--issue <N>` resolves the record through saga's store root instead of `--record`; passing both
is a refusal.

**Name the account.** The staffing plan carries a vendor, a model and an effort, because those are
tiers; the account a session runs under is not, so no staffing row supplies one. Without
`--account company|personal` the helper appends no account flag and the wrapper's own default
applies — the personal account. Pass `--account` on `up` for any roster that must run on the
company account. A staffing row carrying its own `account` overrides the flag for that role.

`down` closes **only** the rows that array records this helper as having created, whose ownership
receipt is still on disk, and which are not the pane the command is running in. It never reads
`herdr agent list` to decide what to close. There is no `herdr agent close` subcommand in herdr at
all — closing is a tab operation, and the launcher's `close` is the one place this plugin performs
it, because that is where ownership is proven.

`wait` always carries a `--timeout` and sends no `--until`, so herdr's own settled-state default
(idle, done, or blocked) applies. A blocked role is **reported** — its role, pane, and output tail —
and never answered: the helper has no prompt or key-send path after a launch.

Exit codes extend the run record's own table: `0` success, `1` an internal error, `2` a refusal,
`3` an unknown record version, `4` **not running inside a herdr pane**, `5` a role is blocked or its
wait timed out. Every subcommand refuses outside a herdr pane, because a session outside one cannot
identify the pane it would have to protect from its own teardown.

What it does not do: create git worktrees (the orchestrate driver owns that per unit), close a pane
it did not create, or control a herdr session from outside a pane.

## The surface Orchestrate binds

Orchestrate does not import this plugin; it reads `launcher.py` and executes it into its own
namespace, so the launcher's top-level names become Orchestrate's. The names Orchestrate relies
on, and that this plugin therefore keeps stable across a minor release, are: `launch`,
`redeliver`, `agent_argv`, `launcher`, `launchable`, `roster`, `live_agents`,
`close_run_session`, `tab_close_failure`, `verify_unit_preflight`, `agent_row`,
`session_has_started`, `append_unit_note`, `PaneWriter`, `session_owned`,
`should_guard_pane_write`, `guard_pane_before_write`, `models`, `favourites`,
`has_delivery_warning`, `clear_delivery_warning`, `VENDOR_FLAGS`, `VENDOR_PERMISSION`,
`VENDOR_NOTES`, `StagedInputError`, the account-mismatch error, and `ComposerState`.
Removing or renaming one is a major change and moves Orchestrate's declared
floor. The pane-write rule is owned here: `PaneWriter` is the only door into a pane,
`should_guard_pane_write` is the only statement of when that door inspects, and Orchestrate's
own senders construct a `PaneWriter` rather than carrying a rule of their own
(`docs/engineering-journal/DECISIONS.md` `{#907-pane-writer-owns-the-write-rule}`).

## The binary is the authority

Command syntax changes. Read it live rather than trusting this file or memory:

```bash
agents --help
agents --recipes     # every recipe and layout name
agents --crews       # crews as they resolve on THIS machine
```

`--dry-run` previews any launch without executing it: it confirms the resolved working directory, the resolved Herdr workspace, the flag ordering, and the exact command that would run. It does not validate the model, the reasoning effort, or the account; a wrapper or client may still reject a nonexistent value. It is therefore a preview, not a preflight, and must not be the only check before dispatching a fleet. Continue to the bounded live preflight below before dispatching work.

Some real flags are absent from `--help`. `--herdr-control-only` is one of them — it is implemented in the wrapper and is the correct flag for the common case below. Do not "fix" it away because help does not list it.

## The only real preflight is a bounded live launch with a read-back

A dry run cannot catch an unanswerable launch; only a live launch can. Launch one bounded probe session, read back what it actually resolved to, and stop there — before dispatching any fleet. The read-back touches the routes that hold credentials, so it follows a strict secret-safety contract, and the order of its steps is the substance:

1. **Identify the selected client auth mechanism before proving anything.** A client may hold an existing interactive OAuth session or draw on an environment-backed credential, and the correct proof differs entirely between the two. Do not assume the route: guidance that skips this step pushes callers toward whichever proof it happened to describe.
2. **For an OAuth session, prove it without inspecting anything outside the client.** Interactive readiness plus the client's own non-secret auth status is the whole proof: a ready session that reports itself authenticated *is* the evidence the route works. This is the common case and the documented default.
3. **Only when a declared run contract explicitly names an environment-backed credential** may the read-back test for it — and then only for the presence of the required variable name, never its value. Absent such a declaration, inspecting the environment is out of scope.

Safeguards that apply to every route, whichever step it reached:

- Inspect only this allowlist of launch arguments when reading a session back: model, reasoning effort, permission posture, account or route, working directory, workspace. Never inspect argv wholesale — argv is not guaranteed free of credentials, and the allowlist contains no credential-bearing entry. The safe receipt bookkeeping fields are `confirmed_against_herdr`, `confirmed_outside_herdr`, `requested_only`, `account_evidence`, `permission_resolved`, and `variant`.
- Never dump an environment: no `env`, no `printenv`, no `os.environ` dump, and no diff of two environments, since a diff prints values as surely as a dump.
- Never read, hash, copy, truncate, fingerprint, or persist a credential value. Hashing is not a safe compromise: a hash of a short secret is attackable, and a hash in a transcript is still durable proof of possession.
- Redact inside the producing command, before output exists. Piping output through a redacting filter is not sufficient — by then the value has been produced and buffered and may already be in a transcript, a log, or a failure path that bypasses the filter.

The read-back shape uses only allowlisted non-secret arguments. The probe takes a real prompt. For Claude only, include `--account <selection>` when the run names an account; other vendors have no account proof in this launcher. Without a prompt the launch delivers nothing and exits nonzero on its ordinary path. A delivered prompt exits 0 only when creation, identity, preflight, and delivery all succeed; every stop exits nonzero and may still write a partial receipt.

```bash
python3 "$S" launch --vendor claude --task <probe-name> --cwd "$PWD" --model <model> --effort <effort> --account <selection> --prompt <probe-task> > receipt.json
jq '{confirmed_against_herdr, confirmed_outside_herdr, requested_only, account, account_evidence, permission_resolved, variant}' receipt.json
python3 "$S" close --receipt-json receipt.json
```

Read back only what the receipt can supply: `confirmed_against_herdr` against `requested_only`, the account evidence, and the argv record of a permission posture only when `confirmed_from` is `launch_argv`. `model` in the receipt is the requested string echoed back, not a read-back — do not treat it as confirmed. The reasoning effort is recorded under the `variant` key: for OpenCode it is confirmed against the live session and listed in `confirmed_against_herdr` — the strongest read-back the preflight produces — and for every other vendor it is the request echoed back and listed under `requested_only`. OpenCode's `auto` posture currently resolves to the client's `--auto` bypass flag; request `bypass` explicitly when that posture is intended rather than reading `auto` as sandboxed.

Whatever the read-back reports as missing or wrong is a stop: tear the probe session down using the receipt and resolve it before anything else launches.

## Ordering — the most common mistake

Launcher options must come **before** `<tool>`. Everything after `<tool>` is passed to that tool unchanged.

```bash
agents --dry-run claude     # previews the launch  (launcher flag)
agents claude --dry-run     # runs Claude with a --dry-run argument (tool flag)
```

Tool-native arguments — `--model`, `-c model_reasoning_effort=…`, `--yolo` — always go after the tool.

Never bypass the wrapper to create an interactive coding-agent session. In particular, OpenCode's interactive terminal user interface is the top-level `opencode` command. `opencode run` is the programmatic prompt command and requires an initial message or command even when `--interactive` is present. Launch OpenCode like this:

```bash
agents --dry-run --no-focus --current --herdr --herdr-control-only \
  --task <tab-name> --cwd "$PWD" \
  opencode --model deepseek/deepseek-v4-pro --agent plan
```

OpenCode 1.18.18 does not expose `--variant` on its top-level terminal user interface command. Do not switch to `opencode run -i` to work around that. The terminal user interface restores the selected per-model variant; use `/variants` inside OpenCode when it must change.

## Pick the topology deliberately

Do not substitute one shape for another. If the user asked for a tab, do not build a crew.

| Shape | Command | What it creates |
| --- | --- | --- |
| One named tab | `agents --herdr-control-only --task <name> <tool>` | A single tab in the **current** workspace; keeps focus |
| Crew | `agents --crew` | One workspace here: Terminal tab, orchestrator tab, one tab per worker |
| Ad-hoc crew | `agents --orchestrator claude --workers codex,agy` | Exactly those agents, no named crew |
| Machine view | `agents --recipe studio\|mac-mini\|laptop` | That one machine's canonical Herdr view |
| Team view | `agents --recipe mimir\|freya\|norns` | Reconciles that team's profiles, opens its view |
| Fleet | `agents --recipe fleet` | All machine views plus all three team views |
| Layout | `agents --recipe cockpit` (or `--herdr-layout <n>`) | One cmux workspace, a Herdr pane per machine |
| Hermes profile | `agents --profile <selector>` | Reconciles a profile workspace; owns its own routing |

Recipes take no tool, no `--task`, and no `--workspace`. Crews do take `--workspace`. Layout and fleet recipes create cmux workspaces, so they need cmux socket control (`automation.socketControlMode` in `~/.config/cmux/cmux.json`).

Re-running a crew adds only the tabs its workspace is missing — that is how you grow a crew you are already in.

## The common case: one named tab, no focus change

This is the workflow to reach for when the user says "add an agent" or "start a reviewer". Prefer the verified-launch script above, and complete its bounded live preflight before using the equivalent wrapper command below:

1. **Inspect the current workspace first** with the `herdr` skill. Choose a task name that is not already a tab label there. If the label exists, the wrapper splits a new pane inside that existing tab instead of creating a tab — correct only when the user explicitly asked for a split.

2. **Choose the model and effort explicitly.** Inheriting is allowed only as a deliberate choice you state out loud before proceeding. Add `--yolo` (Codex) or other permission escalation only when the assigned scope genuinely needs it; never by default.

3. **Preview:**

   ```bash
   agents --dry-run --no-focus --current --herdr --herdr-control-only \
     --task <tab-name> --cwd "$PWD" \
     codex --model <model> -c model_reasoning_effort=<effort>
   ```

   Confirm two lines in the preview before going further:

   - `cwd=` is the exact absolute path requested.
   - `herdr_workspace=<current-terminal:<workspace-id>>` contains the workspace ID returned by `herdr pane current --current`, not merely another workspace with the same directory.

   Omit `--workspace` so the run inherits the caller's workspace. If either line is wrong, stop and resolve it — do not create anything.

4. **Run the identical command without `--dry-run`.** The control-only path creates the tab, starts the requested agent, prints JSON, and exits without attaching, prompting, or taking over your terminal.

Note that the preview's `command=` line ends in `&& exec herdr`. That tail is what a normal launch would do; `--herdr-control-only` exits before it. The preview shows the unfiltered command, so do not read that tail as a focus steal.

## Verify, then hand off

The creation command prints one JSON object. Keep these keys:

```
agent  agent_name  pane_id  reused  session  tab_id  tab_name  workspace_id
```

The wrapper's `reused` bit refers to the **workspace**, not the tab — `true` means an existing workspace was joined, which is normal inside Herdr. Tab ownership is the launcher's `owned` field: the receipt `tab_id` was absent from `herdr tab list` immediately before launch. `agent_name` is uniquified by the wrapper if it collides, so read it back rather than assuming the name you asked for. Never close a tab with `owned` false or missing.

Then use the `herdr` skill against those exact IDs to confirm the agent reports the requested kind, tab, absolute working directory, permissions, and the selected model and effort — and that it is ready for input. Herdr returning success from its start path is the readiness evidence; confirm state before sending work.

From that point on: `herdr agent prompt`, `herdr agent wait`, `herdr agent read`, and Herdr's own cleanup commands. Never reach back for `agents`. Close only a session this launch owns; prove ownership from the receipt `owned` field (tab was not preexisting).

## Providers and models

`claude-muse`, `claude-ollama`, `claude-ollama-local`, `claude-ollama-cloud`, and `claude-deepseek` are all the same Claude CLI pointed at a different host that speaks the Anthropic Messages protocol. Every `claude` option still works.

The provider flag and `--model` are **not** the same thing. `--model` keeps its Claude Code meaning and passes straight through; the provider flag selects the model that provider serves and validates it against that provider's catalog before launching:

```bash
agents --task "..." claude --deepseek=deepseek-v4-flash
agents --task "..." claude --ollama-cloud=kimi-k3:cloud
```

List what is actually available by running these directly — they print and exit, so do not wrap them in `agents`:

```bash
cmux-claude --list-providers
cmux-claude --ollama-cloud --list-models
```

Ollama names normalize to the `:cloud` form, valid on both routes; a bare name works against ollama.com but 404s against the local daemon. `--lean` trims tools and MCP config for slow models and composes with any provider. Credentials come from the environment, or from the login keychain under service `com.jefcox.shell-env`.

Per-provider defaults are set by the `claude_launcher` Ansible role in the home-lab repo and overridable per run via `CLAUDE_<PROVIDER>_MODEL` / `CLAUDE_<PROVIDER>_BASE_URL`.

This plugin does not keep a private vendor or model roster. `python3 launcher.py roster` intersects the vendors the script knows how to flag with what the wrapper lists in `Tools:` on this machine, asked every time.

## Machine routing

`--mac-studio` (`--studio`), `--mac-mini` (`--mini`), `--laptop`, `--norns`, or `--remote <host>` run the launch over SSH on that box, using that host's own `~/.local/bin/herdr`. Transport is `--plain-ssh` by default; `--cmux-ssh` uses cmux's managed transport.

Not every host runs every tool — the default crew resolves per machine so it only offers agents that host can actually run. Check with `agents --crews` on the target rather than assuming parity.

## Safety rules

- Preview with `--dry-run` before any creation command. It confirms `cwd` and `herdr_workspace`; it does not confirm model, effort, or account.
- Use `--no-focus` unless the user asked to switch context.
- Honor the requested agent kind and topology exactly. Do not silently upgrade a tab into a crew or a machine view into a fleet.
- Do not add `--new`, `--recipe`, `--crew`, or a pane split unless asked for that shape.
- Escalate permissions only when the assigned scope requires it, and say so when you do.
- One creation command, then hand off to `herdr`. If you find yourself typing `agents` a second time for the same session, you are in the wrong tool.
- Do not close a session whose ownership you cannot prove from the launch receipt.

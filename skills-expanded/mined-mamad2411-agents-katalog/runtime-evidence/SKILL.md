---
name: runtime-evidence
description: Use when a config or behavioral change (a lifecycle hook, an injected context block, a status indicator, a settings key, a script, a command definition, or an agent definition) needs proof it works at RUNTIME, not just that it's wired — maps each surface class to its cheapest fire/effect probe. The operational twin of verification-before-completion for surfaces that have no test suite to run.
allowed-tools: Read, Bash, Grep, Glob
---

# Runtime Evidence

The verification iron law says no completion claim without fresh runtime evidence — but
config-shaped deliverables (hooks, injected prompts, status lines, settings toggles) have no
`npm test` to run, so "run the tests" has no obvious analog. This skill supplies the analog: a
probe per surface class. The lesson it encodes: **config presence is not liveness.** A
completion hook can sit correctly registered in the config for months and fire zero times,
because the runtime event it depends on never fires in that environment. Reading the config
file back would have "verified" it forever.

## The Wired/Fired/Effected Ladder

Every config change must climb all three rungs before "done":

| Rung | Proves | Typical evidence |
| --- | --- | --- |
| 1. Wired | The artifact parses and is registered | Config validator passes, a linter/schema check, `--help` runs |
| 2. Fired | The mechanism executed at runtime | Marker file mtime, a log/telemetry entry, a captured event, script stdout from a real trigger |
| 3. Effected | The intended behavior actually changed | The injected content appears where a consumer reads it, the block actually blocked, the indicator shows the new value |

Rung 1 alone is the completion-cosplay trap — a config that parses is not a config that ran.
Claim done only with a rung-2 or rung-3 artifact pasted verbatim (stdout, marker listing, log
grep hit).

## Probe Table (surface class -> how to prove it)

Map your actual surface to the nearest class below, then pick the cheapest rung-2/3 probe.

| Surface class | What it looks like | Probe |
| --- | --- | --- |
| Lifecycle hook (script triggered by an event) | A script wired to fire on some event in the host system | (a) Execute the script directly with a synthetic payload shaped like the real event — paste stdout/exit code; (b) trigger the real event once in a scratch context, then confirm firing via a log, marker file, or captured trace |
| Event wiring (the registration entry, distinct from the script itself) | The config line that maps an event to a handler | Rung 2 only: real-event trigger + fire evidence. If the event itself may be dead in this environment, cross-check an always-on handler on the *same* event over the same window — silence on both means the event is dead, not that your matcher is wrong |
| Settings/config key (a toggle or value read by some other component) | A boolean or value flag consumed elsewhere | Confirm the key is attached to the right object (rung 1), then exercise the code path the key gates and show the behavior actually changes (rung 3) |
| Prompt-injected context block (text auto-added to a session/request) | Content meant to appear in a downstream prompt or transcript | Run the generator directly and paste the emitted lines (rung 2); for wiring proof, grep the actual downstream transcript/log for the injected text (rung 3) |
| Status indicator (a line/badge rendered from a live command) | A statusline, badge, or dashboard tile backed by a command | Run the exact command as the host invokes it, paste the rendered output; check the freshness of any cache it reads if the source is cached/pull-based |
| Preprocessor / detection script (runs before the main body renders) | A script whose output gets composed into a larger render | Run standalone: confirm valid structured output AND a clean exit code under a broken precondition (unset env, missing dir) — a nonzero abort there kills the whole downstream render |
| Command / template definition | A reusable invocable definition (slash command, macro, template) | Invoke it once with scratch args; confirm the render includes the expected injected content and that any pinned parameter (e.g. a model or version pin) actually took |
| Agent / role definition | A reusable agent, persona, or role spec | Dispatch it once on a trivial in-domain task; confirm the dispatch metadata shows the right definition loaded and that any declared capabilities/skills attached |
| Auto-trigger description (a natural-language trigger meant to fire a capability) | A description string matched against free text to decide when something activates | Phrase a natural request that should match; confirm the capability actually loads. For explicit-only triggers, confirm the direct invocation path resolves |
| Pre-commit / git hook | A local guard that runs on commit | Stage a synthetic violating file, run the commit in a scratch branch (or dry-run path), paste the rejection, then unstage |
| Scheduled job (cron / timer) | A recurring background task | List the active schedule for the job, then check the output artifact's mtime after the next window (or trigger one run manually and diff the result) |

## Probe every code path that reaches the surface, not just one

A hook can fire on one caller and be completely silent on another. Multi-path surfaces
(lifecycle hooks, middleware, instrumentation) are usually wired at one call site and missing
at the siblings — an interactive/streaming path fires while the batch, headless, or worker path
calls the underlying routine directly and skips the dispatch entirely. Probing only the
convenient path certifies the surface as working while the paths that actually matter in
automation stay dark.

So enumerate the callers before declaring the surface live:

```text
grep -rn "fire_<event>_hook\|dispatch_<event>" <src>   # who fires it
grep -rn "<the underlying routine they all wrap>"      # who should have
```

Any caller in the second list but not the first is a silent path. Probe at least one surface
per distinct entry shape (interactive vs one-shot vs background), not one per surface.

## Differential probing: prove the mechanism before blaming your handler

When a handler stays silent, do not immediately conclude the handler is wrong. Add a second,
maximally dumb handler on the SAME event that only appends to a marker file, then trigger the
event:

- Both silent -> the event never fired for that path. Your handler was never the problem; go
  find the dispatch site.
- Probe fires, real handler does not -> the mechanism works and the fault is genuinely in your
  handler.

This one-line experiment separates "dead event" from "bad handler" in a single trigger and
prevents the classic wasted hour spent debugging a correct script. Include the environment in
the marker output (`echo "$RELEVANT_ENV_VAR ev=$EVENT" >> /tmp/probe.log`) so the same artifact
also proves which context the event carried. Remove the probe handler as soon as the question
is answered — a marker-file handler left in a config is exactly the residue the NEVER table
prohibits.

## Procedure

1. Name the assertion precisely ("the injected block shows X when condition Y holds"), not
   "the hook works."
2. Pick the CHEAPEST rung-2/3 probe from the table — direct execution with a synthetic payload
   usually beats orchestrating a real event end-to-end.
3. If the probe needs a real event, fire it ONCE deliberately in a scratch/throwaway context —
   never wait around for one to happen naturally.
4. Paste the evidence artifact verbatim (stdout snippet, marker listing, log/transcript line).
5. For anything that must KEEP working, note whether the surface needs an ongoing liveness
   check (a periodic re-probe, a monitoring rule) so a future rewrite of the surrounding config
   can't silently drop it without anyone noticing.

## NEVER

| Never | Why |
| --- | --- |
| Claim done from a config/frontmatter read alone | Wired != fired — a registered handler that never actually executes still reads as "done" from the file |
| Verify a hook or script by re-reading its source | Source reading proves the file exists; only execution proves behavior |
| Test from a location where symlinked or relative resources resolve differently than production | Depth-relative links can silently resolve to empty/zero-byte content in an isolated copy — probe from the real working environment |
| Leave probe residue behind | Delete scratch files, markers, and branches; probes must be rerunnable and side-effect-free |
| Run a probe through a shell construct that mangles the command (chained heredocs, ambiguous quoting) | You end up debugging the probe instead of the surface — keep probe commands simple and literal |
| Conclude "matcher bug" from one silent handler | Cross-check a co-resident always-on handler on the same event first — this distinguishes a dead event from a bad matcher |
| Generalize one path's fire evidence to the whole surface | Hooks are wired per call site; the streaming/interactive path firing says nothing about the one-shot or background path, which is usually the one automation depends on |
| Skip re-verification after a bulk config rewrite | Bulk rewrites are exactly how live keys get silently dropped — re-run the probe for every affected surface after any sweeping config change |

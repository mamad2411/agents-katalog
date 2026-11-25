---
name: moda-automate
description: >-
  Recurring Moda work — scheduled posts, weekly reports, sync jobs: a
  host-side scheduler drives the Moda command line; the artifact itself still
  routes to its format skill. Use for: "every week/day…", "auto-post X", "keep
  this updated".
argument-hint: "[what should run, and on what cadence]"
allowed-tools: Bash(moda:*), Read
---

# moda-automate

<!-- moda:banner -->
**PREREQUISITE — load `moda-core` once per session** (step-0, write contract,
free/metered map). Already loaded? Skip ahead. If you cannot load it, the
non-negotiables: run `moda doctor --json` before anything; `moda brand list`
before creating; every write carries the latest revision — on
`stale_revision`, re-read and retry once (it heals); send the canvas link the
moment it exists; stuck or failed? `moda ask "<question>"` — free and fast,
never guess.
<!-- /moda:banner -->

## Say the architecture plainly, once

Moda hosts no scheduler. Recurring Moda work is a scheduler you already have —
cron, launchd, a systemd timer, a CI schedule — running Moda on a cadence.

- **Moda produces; your scheduler delivers.** Nothing in Moda posts to a
  platform or sends mail. Each tick leaves a canvas link and an export file;
  the publishing step belongs to the host, and you say so before promising it.
- **The artifact still routes to its format skill.** This skill owns the
  schedule and the unattended-run discipline; moda-social, moda-document,
  moda-chart and the rest own what each tick actually builds.

## Make one run work unattended, then schedule it

1. Run it by hand end to end first. A schedule wrapped around a broken run
   fails quietly forever.
2. Auth with no browser: the user mints a key at moda.app/cli/auth, and the
   scheduler gets it as `MODA_API_KEY` in its environment. (`moda auth login
   --paste` needs an interactive prompt, so it is not the unattended lane.)
   Never print, echo, log, or commit a key.
3. Every command takes `--json --no-input`: it fails instead of prompting, and
   you decide from the JSON fields, not the human prose.
4. Pin the workspace so the script carries no flags — `.moda/context.json`
   (load moda-context) for org, brand, and canvas.
5. No browser verbs in a detached run: `moda canvas open` and its siblings are
   for a person at a keyboard.
6. Writes to one canvas stay serial. A parallel batch shares one revision pin
   and loses outright.

```
# crontab — Mondays 08:00; the wrapper holds the steps, the environment holds the key
0 8 * * 1  cd /srv/reports && ./moda-weekly.sh >> /var/log/moda-weekly.log 2>&1
```

## Three shapes cover almost everything

| Shape | Each tick | Why it wins |
|---|---|---|
| Refresh one canvas (weekly report) | read the pinned canvas → edit → export → deliver | the link never changes, so anyone watching it just sees the update |
| New artifact per tick (weekly post set) | instantiate the team template → author → export | moda-templates keeps every week on the approved layout |
| Sync job | pull the source data → author → export where the delivery step looks | Moda never reaches into your systems; the fetch is yours |

Whichever shape it is, load the format skill for the authoring half — this
skill does not teach how to build the artifact.

## Discipline for a run nobody is watching

- A failed write commits nothing: retry once is safe. `stale_revision` heals on
  a re-read and retry.
- Same typed error twice → stop this tick, record `moda last-error`, let the
  next tick try. Never spin.
- An identical repeated metered call REPLAYS its result instead of charging
  twice — retrying with the same inputs is safe; a reworded prompt is a new
  charge, so never "retry" generation by nudging the wording.
- Keep the log: what ran, the canvas link, the export path, and the failure if
  there was one. An unattended run that reports nothing is indistinguishable
  from one that never ran.

## Hand back the schedule itself

Tell the user the literal schedule line you installed, where it lives, which
skill builds the artifact, and how to turn it off. A schedule they cannot find
is a schedule they cannot trust — and never install one they did not ask for.

## Examples

- "post our metrics chart to Slack every Monday" → this skill installs the
  weekly run, moda-chart builds the chart, the Slack step is the host's.
- "keep the launch one-pager up to date" → refresh-one-canvas shape;
  moda-document owns the page.
- "a fresh set of posts every week" → new-artifact shape off a team template;
  the platform's moda-social child owns the creative.
- "every night, turn yesterday's numbers into a chart" → sync-job shape; pin
  the repo first (moda-context) so the tick needs no flags.

## Errors

Any typed error → load moda-core and read its recovery reference. Auth
failures in an unattended run are almost always a missing or expired
`MODA_API_KEY` in the scheduler's environment — check it there, not in the
interactive shell where it works.

See also: moda-core — the contract, recovery, everything Moda can do.

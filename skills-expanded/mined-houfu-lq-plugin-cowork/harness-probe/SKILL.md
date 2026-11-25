---
name: harness-probe
description: >-
  Probe the harness you are running in and report which LegalQuants skills it
  can run as intended, which run on a documented fallback, which cannot run,
  and which are still untested. Runs up to 27 capability probes (tool calls,
  files, folders, scripts, fetch, search, vision, Word structure, workers,
  MCP, the HTML round trip and more) against synthetic fixtures, verifies
  each result instead of trusting it, and writes a Markdown, HTML and JSON
  report. Use when asked to probe or audit this harness, check whether it can
  run the LegalQuants or LQ skills, or produce a harness capability report.
  Not for legal work, and never with client material.
---

# Harness probe

You are testing the harness you are running in: the agent loop, its tools and
its connections. The skill judges every vendored LegalQuants skill (31 of
them) against what you can show this harness actually does, and writes the
report. A probe is a small task with a verifiable answer. You do the task with
your own tools; the bundled checker compares what you produced with the run's
answer key and records the outcome.

Everything here is synthetic. Never put client or matter material into a
probe, and never send a fixture anywhere outside this harness except where a
probe says so (P6, P12 and P18 fetch public pages).

## The rules that make the report worth reading

1. **Do the task, or say you cannot.** A probe you cannot carry out is a
   result: record it as `fail` (you tried and could not) or `refused` (the
   harness or a policy stopped you), with one line of evidence. Never describe
   what a tool would have returned. A fluent answer with nothing behind it is
   the one outcome this skill exists to catch.
2. **Never open `<run>/key.json`** or `assets/fixtures/static-key.json`. They
   hold the answers, hashed. An answer taken from them is a fake.
3. **Use your own tools for the work, and `hprobe.py` only to check it.** The
   checker must not do the probe for you: P16 is a folder walk by you, P17 a
   digest computed by you, and so on.
4. **Install nothing.** The point is what this harness has. If a package or
   program is missing, that is the finding.
5. **The verdicts are the engine's.** Report them as written; do not soften a
   "Cannot run" or upgrade an "Untested".

## Step 0 - set up

Ask the user, in one message:

- a short name for this harness (for example "Claude Code web, Opus" or
  "Copilot Cowork, tenant A");
- which profile to judge: **upstream** (the vendored skills as written; the
  default) or **cowork** (the adapted Microsoft 365 Copilot Cowork cards);
- a sentence of their own choosing, typed now, for probe P11 - tell them you
  will quote it back word for word near the end.

Then find out whether you can run Python here: try
`python3 <skill>/scripts/hprobe.py --help` (where `<skill>` is this skill's
folder). If it runs, follow the scripted route below. If it does not, follow
[references/no-exec.md](references/no-exec.md) instead and record P1, P21 and
P25 as you found them.

Start the run in the user's workspace:

    python3 <skill>/scripts/hprobe.py init --run <run> --harness "<name>" --profile <profile> --model "<your model>"

`<run>` is a folder the user can see, such as `./hprobe-run`. Record anything
the user tells you about the harness's settings with
`hprobe.py posture --run <run> web_search=on browser=off ...`.

## Step 1 - run the probes

`hprobe.py status --run <run>` lists all 27 with their method. For each probe,
print its exact steps with the paths filled in:

    python3 <skill>/scripts/hprobe.py steps P16 --run <run>

do what they say with your own tools, then run the `hprobe.py check ...`
command they end with. The check prints the outcome and records it. Work in
this order, which puts the cheapest and most decisive first:

1. **Scripted:** P1 (`hprobe.py env --run <run>`), P21.
2. **Your own tools:** P25, P27, P26, P17, P16, P3, P4, P7, P8, P9, P10, P22,
   P23, P12, P18, P6, P19.
3. **The user's part:** P20 (they open a page and hand back a file), P24 (they
   call the companion skill `harness-probe-invoke` by name), P11 (they judge
   your quotation), and P15 if an MCP server can be connected
   ([references/mcp-setup.md](references/mcp-setup.md)).
4. **Two sessions:** arm P2, P5 and P13 now and tell the user exactly what to
   do in the later session. Their outcome stays `pending` until then.
5. **Cowork only:** P14 needs a real tenant. On any other harness record it
   with `hprobe.py record P14 not-run --observer agent`.

[references/probes.md](references/probes.md) has every probe's question, what
it settles and its steps. Where a probe needs the user to watch and judge,
record their verdict with `hprobe.py record <probe> <outcome> --observer user
--evidence "<what they saw>"`.

Keep going when a probe fails. One missing capability is one finding; it does
not end the run.

## Step 2 - report

    python3 <skill>/scripts/hprobe.py report --run <run> --both

This writes `report-upstream` and `report-cowork` as `.md`, `.html` and
`.json` under `<run>/report/`. Hand the user the HTML (or the Markdown) and say
in the chat, briefly:

- the four counts for the profile they chose: runs as intended, runs on a
  fallback, cannot run, untested;
- each skill that **cannot run**, with the capability and probe that block it;
- each skill **on a fallback**, with the capability lost and the skill's own
  fallback wording from the report;
- the top three entries of **What to build next on this harness**: the
  capabilities that failed here, ranked by how many skills each would unblock
  or upgrade, which is what to tell whoever builds or configures the harness;
- the top three entries of **What to probe next**, so the user knows what
  would settle the untested ones.

Use the capabilities' plain names from the report ("Folders on disk", "Run
Python scripts"), not their codes, when you talk to the user.

[references/verdict-rule.md](references/verdict-rule.md) explains how a
verdict is reached; quote it if the user asks why.

## Later sessions

The run folder is the record. In a later session, run `hprobe.py status --run
<run>`, finish the two-session probes, and run the report again. Results from
several runs or harnesses can be merged or re-judged without a run folder:

    python3 <skill>/scripts/hprobe.py verdict --results results.json --profile cowork --out report/

To contribute a result to the LegalQuants Cowork project, attach
`<run>/results.json` to a Probe report issue
([references/results-format.md](references/results-format.md) describes the file).

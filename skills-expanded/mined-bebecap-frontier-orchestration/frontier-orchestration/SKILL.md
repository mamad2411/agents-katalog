---
name: frontier-orchestration
description: >-
  Routes high-stakes work across frontier models (Claude, Codex/GPT, Gemini) instead of doing everything on one, with a System One judge (TypeSafe Jev or open OpenJev) picking the model. Use when a task is expensive to get wrong or spans many files: engineering estimates, architecture rulings, audits, adversarial or cross-vendor review, ship gates, or any answer someone will act on. Covers discovering which models are reachable today, asking Jev to route, why routing confidence is not correctness, the confidence x stakes gate, the different-vendor review rule, and the learning loop (recall lessons before a run, retro and record after). Triggers - "which model should", "route this", "second opinion", "adversarial review", "cross-vendor", "model selection", "orchestrate", "estimate", "is this worth a frontier model", "ship gate", "lessons learned", "retro", "jev", "openjev".
---

# Frontier orchestration

One model doing everything is the expensive failure mode. No model is weak; **a model cannot
see its own blind spot**, and the work that matters most is exactly where that blind spot costs.

This skill is the routing layer: discover what is reachable, let Jev pick, gate the pick on
stakes, and spend cross-vendor capability only where it pays.

All commands below run one stdlib-only script. `${CLAUDE_SKILL_DIR}` is the folder that holds
this SKILL.md (Claude Code fills it in; on other hosts use that folder's absolute path):

```
python3 -I "${CLAUDE_SKILL_DIR}/scripts/fo.py" <command>
```

Below, `fo.py` means that full command.

---

## 0. First use on a machine: setup

A person sets up with the interactive installer: `fo.py install` (decision engine, providers,
telemetry). An agent cannot drive that terminal UI: run `fo.py doctor`, and if the config is not
written yet, run `fo.py setup --non-interactive`.
When setup exits 3 it prints questions: ask the user each one, with its options (in Claude Code,
use AskUserQuestion), then run setup again with the answers as flags. **Never answer for the
user, above all the telemetry question.** If setup prints `API key ... NOT FOUND`, show the user
the exact command it printed; the user runs it. Never ask for a key in chat.

What setup decides (all stored in `~/.config/frontier-orchestration/config.json`, never a key):

| Setting | Options |
|---|---|
| Jev backend (`--jev`) | `typesafe` (hosted Jev, `TYPESAFE_API_KEY`), `openjev` (self-hosted OpenJev, no key), `codiv` (hosted OpenJev, `CODIV_API_KEY`), `custom` (`--jev-url`), `off` (local rule-based router) |
| Providers (`--providers`) | any of `claude,codex,gemini`; each reached by the first transport found (§1a) |
| Telemetry (`--telemetry`) | `yes` or `no`. Opt-in, anonymous counts only (see `references/privacy.md`) |
| Ledger (`--ledger`) | a folder for lessons and runs; default `~/.local/share/frontier-orchestration/ledger` |

Then `fo.py doctor --live` makes one tiny Jev call and checks every provider transport.

---

## 1. Never hardcode a model. Discover, then use aliases.

Model names go stale fast. Three rules keep "always the latest" true without edits.

**Refresh first; it costs nothing.** `fo.py refresh` returns at once with the last snapshot: CLI
versions, the models each CLI offers today, and a DRIFT list against the roster. When the
snapshot is older than 24 h it starts one detached worker and still returns at once; the next
call shows new data. `--wait` refreshes in the foreground. CLI self-updates are opt-in
(`refresh.upgrade_clis`). A model a CLI offers that your transport does not admit is not
reachable: tell the user and use a listed model.

**Claude side: address by ALIAS.** In Claude Code the Agent tool takes `fable`, `opus`, `sonnet`,
`haiku`, which resolve to the current model of that tier. Writing an exact id into a script
pins you to a model that will be superseded. The dated map of exact ids lives in
`data/roster.json`; override it in `~/.config/frontier-orchestration/roster.json`.

**Other vendors: check before you rely on a model.** Use an id that `fo.py refresh` shows as
offered today. If a call fails, read the error first:

- "unknown model", "not supported", 404: not reachable today. Check the spelling, then use a
  listed id.
- 401 or 403: a sign-in or key problem. It is not transient; tell the user.
- 429 or quota: wait for the window or use a smaller tier. Do not loop retries.

Fall back to the previous tier and **say so in the output**. Never present a result as coming
from a model you did not actually reach. A review with no result has no verdict: never count it
as approve or block; re-run it.

## 1a. How each vendor is reached

`fo.py providers` prints, for this host, how each provider is reached and whether its CLI is
signed in. The skill uses each vendor's own CLI in read-only mode through one command, with no
bridge or daemon:

```
fo.py ask codex --prompt-file packet.md --cwd <repo>     # codex exec --sandbox read-only
fo.py ask gemini --prompt-file packet.md --cwd <repo>    # agy --print --mode plan
fo.py ask claude --prompt-file packet.md                 # from a Codex or agy host
```

The answer goes to a file; the status is `ok`, `failed`, `timeout` or `empty`, and only `ok` is a
verdict. In Claude Code, reach Claude with the Agent tool. Run long reviews in the background and
read the out file when they end. Details, flags and failure signs: `references/providers.md`.

- A job on your own vendor is not independent. It never counts as the different-vendor review.
- Reviewers are always read-only. They advise; the driving session owns acceptance.
- Before a workflow depends on a cross-vendor model, send one tiny ask per provider ("Reply
  with one line: your model name") and read the answer. A dead lane found late wastes a round.

---

## 2. What each tier is actually for

Capability is not the only axis. Cost and **independence** matter as much.

| Tier | Spend it on |
|---|---|
| Claude top (`fable`) | The hardest reasoning, difficult code, long-horizon agentic work. Highest price |
| Claude frontier (`opus`) | Orchestration, holding a whole codebase, long prose that must stay accurate. The default |
| Claude mid (`sonnet`) | Well-specified bulk work: repo sweeps, mechanical edits, an exact recipe |
| Claude small (`haiku`) | Trivial mechanical steps where an error is obvious and cheap |
| Codex frontier (`sol`, `astra`) | **Adversarial review and root-cause reasoning, because it is a different vendor and fails differently** |
| Codex small (`luna`) | Cheap bounded checks |
| Gemini frontier (`argon`) | A third blind review lane; long context and multimodal input |
| Gemini fast (`flash`) | Cheap bounded checks and long-context skims |
| Jev / OpenJev | Typed judgments and calibrated probabilities that *code* acts on. No text, no reasoning |

**The load-bearing property of the Codex tier is not that it is smarter. It is that it is not
Claude.** Gemini is a third vendor, so it fails differently from both.

---

## 3. Ask Jev which model, not yourself

`fo.py route tasks.json` asks Jev two questions per task and applies the gate (§5). `--demo`
runs a worked example; `--check` validates a spec with no network; `--json` gives code-readable
output. Exit code 1 means the route failed and gave no decision (for example, the independence
rule left no candidate). Exit code 2 means a REJECT decision: the judge picked a model that is
not an allowed candidate.

Give Jev **structured task attributes**, not prose: `context_volume`, `output_kind`,
`needs_independence`, `verifiable_by_code`, `cost_sensitivity`, `producer_vendor` (who made the
artefact), `needs_long_context`. With `needs_independence: YES`, the router needs
`producer_vendor`, drops that vendor's candidates before asking, drops candidates of unknown
vendor (fail closed), and rejects a same-vendor pick.

Criteria shapes, if you write your own System One calls: Choice takes a **map** option -> rubric;
Noul takes `{"true": ..., "false": ...}`; Score takes an **ordered array** of levels.

With `jev.backend = off` the router uses local rules: no calibrated confidence, rule-based
stakes. It still enforces independence and still escalates high-stakes ties. Say so when you
report a route.

Before you trust a new engine or model id, run `fo.py eval` (sanity and routing suites; exit 0
pass, 1 fail, 2 error) and report its accuracy.

---

## 4. Confidence is not correctness

**Choice confidence measures how concentrated the probability distribution is. It does not
measure whether the answer is right.**

Measured on five routing tasks: pruning the obviously-wrong options made mean confidence
**fall** (0.770 -> 0.740) while the routing got *better*. The wrong options had padded the
winner's margin. Two routes collapsed to near-ties because every surviving candidate was
defensible.

**So do not tune prompts to raise the confidence number.** A near-tie between two good options
is information: it says the choice barely matters.

---

## 5. The gate: confidence x stakes

Two questions per route: a **Choice** (which model; gives `confidence`) and a **Noul** (would a
mistake be expensive or hard to detect; gives `stakes`). Then:

```
if confidence >= 0.80   -> act on the choice
elif stakes < 0.50      -> act anyway; a tie here is harmless
else                    -> ESCALATE: head-to-head Nouls, or run both and reconcile
```

| Task | Confidence | Stakes | Outcome |
|---|---|---|---|
| `artifact_build` | 1.00 | 0.15 | act |
| `repo_sweep` | 0.87 | 0.57 | act |
| `arithmetic_audit` | 0.42 | 0.15 | act: a tie on cheap, checkable work is nothing |
| `estimate_review` | 0.48 | 0.89 | **escalate** |

One decision in five needed more thought, and it was the one that mattered.

**Escalate with head-to-head Nouls, not a bigger Choice.** A spread Choice gave 0.48; pairwise
questions over the same candidates gave clean numbers.

**The gate absorbs run-to-run noise.** The same route returned 0.48 on one run and 0.29 on the
next. Both escalated, because stakes stayed high. Routing on confidence alone flaps; routing on
confidence x stakes is stable. If you must act on a bare confidence, sample it more than once.

---

## 6. Independence is a requirement, not a nicety

**Rule: whoever produced the artefact does not review it. Different vendor, always.**

| Producer | Reviewer options | Ship gate |
|---|---|---|
| Claude | Codex (two frontier models, blind); Gemini | Two Codex frontier reviewers on the same packet. Gemini is an optional third lane |
| Codex | Claude (`opus`, `fable`); Gemini | A Claude review, plus Gemini for a third lane |
| Gemini | Codex; Claude | A Codex review. Verify every Gemini claim first |

A same-vendor subagent never counts as the different-vendor review. Routing across models with
complementary error patterns beats the best single model, and correcting for single-model
evaluation cuts error substantially ([Capability Frontier](https://arxiv.org/html/2606.26836v1),
[LLM routing with benchmark datasets](https://arxiv.org/pdf/2309.15789)).

If `fo.py providers` shows only one vendor, say plainly that the review is not independent.

---

## 7. Trust the reasoning, verify the citations

- Take the cross-vendor reviewer's **framing** seriously: it sees classes of problem the
  producer cannot.
- Treat every **specific claim** (file, line, number) as unverified until you open the file.
- **Verify the size, not only the existence.** A real finding with a false size is a wrong
  number. In one measured run a true finding came with a size ask about 2.5x its verified size.
- Verification cuts both ways: record what the code says, not what the reviewer said about it.
  A finding whose invariant is written in the source and unenforced is worth restating at full
  strength.
- Never forward a reviewer's claim to a customer without checking it.

Two frontier models of one vendor can fail in different directions: in a measured estimate
review one found a missing *category*, the other a wrong *line*; neither found the other's.
When two independent reviewers name different top items, do not average them and do not pick
the more confident one: open both files.

Measured hit rates per model and artefact kind: `references/evidence.md`. Record your own in the
ledger's `reviewer-priors.md`; a prior earned on one project is a prior about that project.

---

## 8. The pipelines

**Estimate pipeline:** RECALL lessons -> `fo.py refresh` -> route each task (choice + stakes) ->
write the pricing conventions into every prompt -> PRODUCE (non-overlapping lanes, every claim
with a file:line citation) -> COMPLETE (two critic rounds, different models) -> AUDIT (count
every shared unit once) -> REVIEW (different vendor, adversarial, read-only) -> VERIFY (per claim:
refuter + confirmer, then a decider sizes only the work the code shows is missing) -> ARITHMETIC
(cheap model) -> PRESENT (which model did what, and what changed on review) -> RETRO.

**Code ship-gate loop:**

```
RECALL -> budget rounds by change kind
  -> per round: blind cross-vendor review of ONE frozen commit,
     every finding labelled INTRODUCED or PRE-EXISTING
  -> the driver opens each cited line; a prescribed fix is a hypothesis
  -> a failing test per accepted finding, then the fix
  -> prefer removing a mechanism to adding one late in a release
  -> repeat until both blind reviewers approve the same commit
  -> execution evidence: tests, device or simulator, real data
-> RETRO
```

Rules that keep it honest: lanes never overlap; every produced claim carries a citation; the
reviewer is read-only; say who did what, and show before and after when a number changed.
Full diagrams and the reasoning: `references/pipeline.md`.

---

## 9. The learning loop

Every run reads the ledger first and writes back at the end. Write notes only through
`fo.py lessons`: it locks the folder, writes atomically, links lessons and runs both ways, and
computes each lesson's status (candidate -> confirmed at 2 runs -> disputed when contradicted).

1. **RECALL** before routing: `fo.py lessons recall --tags <kind>,<project>`, and read
   `reviewer-priors.md`. Put every lesson that applies into the plan and the prompts.
2. **RECORD** during the run: `fo.py lessons run-new --id <YYYY-MM-DD>-<project>-<name>
   --project <project> --artefact <estimate-raw|estimate-verified|code|schedule|content|other>
   --title "..."`. Fill the rounds table as it happens: reviewer and exact model id, verdict,
   findings, how many held or were refuted when you opened the code.
3. **RETRO** before you report done: what converged it, what wasted rounds, what slipped past
   every reviewer, which prior was wrong. Turn each answer into `reinforce`, `contradict` or
   `add` (in that order of preference), then `run-close` and `lint`.

A lesson is about how to orchestrate models, never a project fact. No evidence, no lesson. No
secrets, tokens, emails or customer content in the ledger. Command details:
`references/ledger.md`. The maintainer's confirmed rules, as priors: `references/rules.md`.

---

## 10. Do not use this skill when

- The task is small, obvious, or cheap to redo. Orchestration costs more than the work.
- Nobody will act on the answer. Second opinions are for decisions, not curiosity.
- You have not read the primary source yet. **No amount of model routing substitutes for
  opening the file.** Route the reading; do not route around it.

---

## Reference

- `scripts/fo.py`: `install`, `setup`, `doctor`, `providers`, `ask`, `refresh`, `route`, `jev ping`,
  `lessons`, `config`, `telemetry`
- `data/roster.json`: the dated model roster (override per user)
- `references/providers.md`: transports, `fo.py ask`, CLI flags, failure signs
- `references/evidence.md`: the measured runs behind §4 to §7
- `references/pipeline.md`: both pipelines in full
- `references/ledger.md`: every `fo.py lessons` command
- `references/rules.md`: confirmed rules from the maintainer's ledger
- TypeSafe docs: <https://docs.typesafe.ai/llms.txt>. OpenJev: <https://github.com/razorback16/openjev>

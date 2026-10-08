---
description: Fact-root a command/skill file against the craft register — does it carry the craft rail where it makes a judgment call, follow the authoring conventions, and do what its description claims? Emits PASS | NEEDS FIXES | REWRITE with a craft-grounded rationale. Proposes diffs for review; print-only by default, never silently rewrites.
argument-hint: "[command-name | path/to/command.md]  (e.g. /review-skill scope, or commands/scope.md)"
allowed-tools: Bash, Read, Grep, Glob
---

# /review-skill — review a command against the craft standard

Read `~/.claude/workflow-conventions.md` first, then `~/.claude/craft/README.md` — the craft register (the judgment substrate; conventions §10). For the verdict itself read `~/.claude/craft/judgment.md` (its `## Constraints` + `## Anti-Patterns` are the rail every finding is weighed against, and the rail this command checks a *target* carries); and for the authoring-convention leg read `~/.claude/craft/authoring.md` (the file that operationalizes those conventions — leg b grades against it) and `~/.claude/craft/retrofit-backlog.md` (the adoption rule that decides whether a command is judgment-bearing in the first place).

A command file is **load-bearing instruction for every future run of that command** — a wrong line misroutes work, a missing craft rail lets a judgment step run on instinct. So the same caution `/review-claude-md` applies to context applies here: verify every claim against the file you actually read, and **propose edits for approval rather than silently writing them**. The sibling of `/review-claude-md`; the closing loop that lets each `craft/` hypothesis earn or lose its place (`craft/retrofit-backlog.md` names this command as that check). This command is also the **review actor** the craft governance loop (`craft/governance.md`) routes to: pointed at a `craft/` file, it is what re-checks whether that file still earns its place and whose verdict flips the file's `Status` (`hypothesis | reinforced | retired`) on evidence — including the trigger where a command keeps failing the same rail, which is evidence the *rail*, not the command, is wrong.

The instinct to name and resist (`craft/judgment.md`): **rubber-stamp it `PASS`** because reviewing your own pipeline's command feels collegial — or, over-correcting, **manufacture nits** to look thorough. Resist both: flag only what trips a named convention or a real rail gap, and refuse to pass a judgment-bearing command that runs its judgment on a bare checklist. When something feels off, say *why* diagnostically — which convention, what breaks — not "this feels thin."

## Start check (soft — convention 4)
- `root="$(git rev-parse --show-toplevel)"`. Target = `$ARGUMENTS`: a bare name → `$root/commands/<name>.md`; a path → resolve it. Default (no arg) → ask which command; don't guess.
- The target must exist and be a command/skill `.md`. If not: say so, name `/gen-claude-md` or the authoring flow, and stop — don't review a file that isn't there.

## 1. Load context (ground truth, no guessing)
- Read the **whole target file** — frontmatter (`description`, `argument-hint`, `allowed-tools`) and body. The frontmatter is the contract leg (c) checks the body against.
- The craft register is already loaded from the header. Hold `craft/judgment.md` (the rail), `craft/authoring.md` (the authoring conventions), and `craft/retrofit-backlog.md` (the adoption rule + tier status) ready as the standards to judge against — not as a checklist to echo.
- For any concrete claim the body makes — a referenced file, a sibling command, a `§`-section, a helper script, a convention number — `Grep`/`Read` to confirm it resolves. A command that cites a file or section that doesn't exist is the command-file analog of a hallucinated CLAUDE.md line.

## 2. Classify the command (judgment-bearing or not)
Apply the adoption rule from `craft/retrofit-backlog.md` — this gates leg (a), so get it right before judging:
- **Judgment-bearing** — it makes a call that could go better or worse with more care: a review verdict, a scope/validation decision, an "is this actually done?" self-check, a gate, a promote/park/kill. These *owe* the craft rail.
- **Pure procedure / capture / orchestration** — near-zero-friction capture, a mechanical runbook, or thin orchestration whose judgment lives in the commands it calls. These do **not** owe a craft rail; wiring one in is the *Ceremony* anti-pattern (`craft/judgment.md`). For these, absence of the rail is the rule working — never a finding.

State the classification and your one-line reason. If `retrofit-backlog.md` already tiers this command, cite where it sits and whether the file's actual state matches that tier.

## 3. Judge against the craft standard
Run the three legs. Each finding cites the target's section/line and the register file or convention it trips — fact-rooted, not impressionistic.

**(a) Craft rail — only for a judgment-bearing command.** Two parts, both required for the rail to be real:
- **Read-first wiring** — the header loads `craft/README.md` and the relevant per-domain file (`judgment.md` for a verdict/decision, `authoring.md` for an authoring command). A `grep` for `craft/` in the header settles it.
- **Routed judgment** — the judgment step actually *names the default instinct it resists and self-critiques against `craft/judgment.md`'s `## Constraints` / `## Anti-Patterns`*, rather than listing boxes to tick. A header line with a checklist body underneath is wiring without a rail — flag it: the read-first line is present but the judgment still runs on a checklist.
- Judgment-bearing command with neither → this is the **retrofit flag** `craft/retrofit-backlog.md` describes: `NEEDS FIXES`, promoting it from the backlog to a retrofit.

**(b) Authoring-convention conformance** (graded against `craft/authoring.md`):
- **Explains its why** — rules carry their reasoning, so a reader can tell when one stops applying. A bare directive is a finding.
- **Concise** — body roughly within the ~500-line ceiling; depth pushed to on-demand files, not inlined. Flag real bloat, not length per se.
- **Metadata drives invocation** — the `description` says what the command is *for* (the trigger), distinct from the body (the procedure).
- **No all-caps shouting** — `ALWAYS` / `NEVER` / `MUST` in caps standing in for a reason is a yellow flag; the fix is to reframe with the why, not to shout.

**(c) Body-vs-description fact-rooting** — does the body actually do what the `description` claims, no more and no less? A description promising a capability the body never delivers (or a body that quietly does more than the description admits) is the command-file form of *intended-state success*. Plus the reference check from §1: every cited file/section/sibling resolves.

## 4. Output the verdict
```
## Review: commands/<name>.md  ·  <judgment-bearing | pure-procedure>
### Verdict: PASS | NEEDS FIXES | REWRITE
### Findings
1. [CRAFT-RAIL | AUTHORING | FACT-ROOT] — what's wrong
   - section/line · says/does X · the convention or rail it trips (cite craft/judgment.md, craft/authoring.md, or the missing reference) · fix
### Missing
- a rail or a why the command owes but doesn't carry (with the standard that warrants it)
### Summary
1–2 sentences: overall craft + the core change. Ground the rationale in craft/judgment.md.
```
- **PASS** — rails present where owed (or correctly absent for pure procedure), conventions met, body matches description. Say so and stop; don't manufacture nits to look thorough (that's the *Ceremony* anti-pattern turned on the review itself).
- **REWRITE** — structurally off: the body doesn't do what the description claims, or it's mostly inaccurate / would misroute work. Say why; recommend re-authoring from the sibling pattern rather than patching.
- **NEEDS FIXES** — real, fixable gaps → proceed to §5.

## 5. Propose diffs — do NOT auto-write (load-bearing caution)
A command steers its own every future run; an unreviewed "fix" misroutes silently. So **present the exact edits and stop for approval** — this command is `allowed-tools` Read-only on purpose:
- For each fix, show a precise before→after block tied to the convention or rail gap that justifies it.
- Ask the user to approve all / pick a subset / adjust. Apply only after an explicit yes, via a follow-up edit (this command does not hold `Edit`/`Write`) — or hand the diffs back for the user to apply.
- Never edit the target in this command's flow without that yes. Correctness of a command's instructions outranks throughput.

## End — next step (convention 4)
- **PASS** → `commands/<name>.md verified against the craft standard. Next: /review-skill <sibling> or the next entry in craft/retrofit-backlog.md.`
- **NEEDS FIXES** → after approval+apply, suggest re-running `/review-skill <name>` to confirm green; if the gap was a missing rail, note that `craft/retrofit-backlog.md` should tick this command as retrofitted.
- **REWRITE** → name the re-authoring step, then `/review-skill <name>` to re-check.

## Hard rules
- Review-only — no `Edit`/`Write`/state change in this flow; propose, get an explicit yes, then apply via a follow-up. The `allowed-tools` enforce it; this rule keeps the *content* advisory too.
- Verify against the file you actually read — never from its name, its description alone, or memory. A cited file/section is confirmed with `grep`/`Read`, not assumed.
- Don't penalize a pure-procedure / capture / orchestration command for lacking a craft rail — that absence is the adoption rule working (`craft/retrofit-backlog.md`), and flagging it is the *Ceremony* anti-pattern.
- Don't manufacture findings to look thorough; PASS is a complete answer. Conversely, don't wave through a judgment-bearing command whose judgment runs on a bare checklist.
- If the user says a finding is wrong, re-read the target before defending it.

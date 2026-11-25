---
name: handoff
description: Compose a prover-session handoff prompt for the formal target(s) named — statement-first from the document's text, with the declarations quoted, a refute-first line, the bundle's shape and the witnesses commissioned — check it with `formal handoffcheck`, and dispatch it to the prover agent or emit it for the owner's own prover session. Use whenever work is handed to the prover, since Lean (or another prover's) work always ships as a checked prompt. When the person says 'handoff' or 'hand off to the prover', they mean this skill — call it every time, even if it ran earlier in the session, and take every step.
license: Apache-2.0
compatibility: Python 3.11 or later for the check (`scripts/formal.py` of the `land` skill); the prover and its build are the project's. Reads `formal.toml` at the project root where there is one, the default bindings otherwise.
metadata:
  version: "0.12.1"
  requires: land
---

# Handing work to the prover

A prover session has none of this conversation, so everything it needs is in the prompt, and everything the prompt decides is checked before it goes anywhere.
The prompt is composed to the shape below inside literal `<prompt session=…>` … `</prompt>` tags, whichever route it takes, checked with `formal handoffcheck DRAFT` — the `land` skill's script beside this one: `${CLAUDE_PLUGIN_ROOT}/skills/land/scripts/formal.py` under Claude Code, `../land/scripts/formal.py` from this skill's directory under any other agent — and then either dispatched to the `formal:prover` agent as it stands, the dispatch the turn's last tool call, or emitted for the owner's own prover session with nothing after the closing tag; the order of the turn is under Sequencing.
Which route a handoff takes is the owner's call, the agent when nothing is said.
Where the session has no `formal:prover` agent type loaded — the session that installed the plugin among them, since an agent type is loaded when a session starts and appears after a restart — the dispatch is a general-purpose subagent given the text of the plugin's `agents/prover.md`, the project root's absolute path (the workspace and its instructions are found from it, whatever directory the subagent starts in) and then the prompt, the same run by other means.
A design round whose deliverable is a prover prompt hands over to this skill rather than writing the prompt inline, and the landing that answers it is the `land` skill.

## Sequencing

The turn has two parts and nothing after them.
First the records (where the project keeps any), the gates and the commit: every tool call that changes the project finishes before the prompt is composed.
Then the prompt: the draft written to a scratch file, `formal handoffcheck` re-run to exit 0, and the dispatch as the turn's last tool call, or on the other route the prompt as the turn's last output; nothing follows the dispatch or the closing tag.
Where the flow is set up (`flow.toml` at the project root, the research plugin's), the work the prompt carries is among the records, as the prover's task in the agent's hand.
Where the agent's hand already holds the task, it is handed over as it is.
Where the hand holds the question, the prover's task is minted into the agent's deck from it (`flow task "…" --summary "…" --ref Q --tag research --for agent`; `agent` is the agent's name as `[hand]` names it by default, and a project that names its hands otherwise uses its own), and its draw for a prover that runs in parallel while the session works on something else is a deviation from the session: it is proposed to the person and drawn on their word (`flow draw T --owner agent`), a project's instructions possibly carrying the person's standing ruling for it.
The drawn task is held in the agent's hand while the prover works, counted toward the hand's limit as any held card, and the log entry that records the handoff says it went to the prover.
One handoff is in flight at a time, since the prover session leaves its work uncommitted in the shared tree and a second would mix into it: the log's top State paragraph says whether one is, and a handoff waits for the landing of the one before; the `land` skill closes the task, and a handoff withdrawn before it lands is said so in a log entry, the task returned with a note or kept for the next attempt.
Where the flow is set up, read the records for riders too, the ready tasks tagged `rider` (`flow find --tag rider --ready`): each is carried as a trailing piece or re-pointed in the same commit, never left.
The task's id stands in the log entry that records the handoff and never in the prompt, since a session cites what it was given.

## The session attribute

`session=fresh` is the default: a new prover session, always for review- or verification-shaped work, where reading the exporting statements cold is what catches things.
`session=continue` resumes the previous session, only when iterating on the same module where its earned context (tactics tried, walls hit, approaches rejected) would otherwise be rediscovered; the body states the reason in one clause right after the title (`session=continue — <why>`).

## What a handoff never does

It assigns no work on the root's side — no document edit, no record, no packaging; the prover session reports and the root session writes.
A file the prover session must touch outside its workspace is named explicitly, which is the only override.
It restates no standing rule: the build gate, the manifest regeneration, the known traps and the report-back list live in the workspace's instructions (`formal.toml`'s `instructions`, a template in `references/workspace-instructions.md`) and load in every prover session; the prompt carries what is target-specific.
It carries none of the phrases `formal.toml` bans, and every path is relative to the workspace (`../papers/x.md`, never `papers/x.md`; never the workspace's own name as a prefix).

## Gathering, for each target

Its record (the bar it states: axiom-clean, guard, scope); the document section or row it serves, quoted enough that the prover session finds the exporting statement, since statements are designed from the document's ACTUAL text, opened, never from memory; the modules it touches; and the hypotheses of the statement drafted, counted at its binders — two or more means the joint-satisfiability witness is a commissioned item.

## The prompt's shape

1. One title line saying what the bundle is.
2. Numbered targets, each with the goal, its sources (record, document, module pointers) and its own bar.
   A target with two or more hypotheses commissions `<theorem>_nonvacuous` beside it: a witness that all hold at once — a fixed instance by default, the asymptotic form when the theorem is a bound — guarded as the guard families are; a theorem whose hypotheses cannot be met at once is the finding a witness exists to surface, and the session reports that rather than proving on.
   A bundle of more than one piece lands SINK-FIRST: the first handoff commissions the bundle's sink — the composite theorem the lemmas feed, which nothing in the bundle depends on — with every predecessor's statement as its hypotheses (each a `Prop` definition, the sink proved from them), the read-back runs on the sink at its landing, and the predecessors are then commissioned as independent fresh sessions with their binders fixed by the sink's.
   Name the pieces `Piece N` and write `Bundle shape: sink-first — sink <name>, predecessors <names>`; a bundle that cannot be sink-first says `Bundle shape: sequential — <why>`; a one-piece prompt may say `Bundle shape: single piece`.
3. Target-specific warnings only, chosen by what the work touches:
   - a construction near a known trap of the workspace's instructions: the trap, said by name;
   - a guard-adding target: drift lists are reported verbatim, never swept;
   - a refactor: what stays byte-identical (guards, public docstrings, statement texts), and that the sweep touches names, visibility and file boundaries only — a move that needs a proof to change means the boundary is wrong, and the session stops and reports it;
   - a multi-piece bundle: the docstrings name no piece of any handoff, no bundle, no landing, no session and no record;
   - a prompt naming a record as a source: this sentence verbatim — "The records named above are sources to READ, not citations: a docstring renders verbatim into the public artifact, so it cites the document's section and row ids — never a record or the log.";
   - guards commissioned together, one per hypothesis: each guard's own statement shape — its witness named in the statement or only built in the proof, the stage or parameters it is stated at, a value or only a bound — since parallel prose comes back as different binders;
   - a witness or guard at a named object: a public statement cannot name a private declaration, so the object is made public rather than the statement weakened to an existential, and a commissioned existential pins every quantity it is about;
   - every prompt: the report names every commissioned declaration that does not land, and why.
4. The close: "Report back per <the workspace's instructions>, listing EVERY new declaration — public and private — and every instantiation of an existing generic, not only the commissioned ones."
5. A `Refute first:` line naming the smallest parameters at which the commissioned statement can be COMPUTED — the prover session's opening move is a bounded refutation attempt there, reported either way, a refutation arriving as a guard-family candidate before any proof work; a review, refactor or bump writes `Refute first: not applicable — <why>`.
6. A `Commissioned:` line listing, backticked, every declaration the prompt commissions — the targets, their witnesses, a guard family's named instances, a rename's new names — running to the next blank line; a prompt that adds no name writes `Commissioned: none — <why>`; the `land` skill looks each name up in the manifests.

## The check, before emitting

Read the `Commissioned:` line once against the targets before the check, since a line written first can be shorter than the prompt it closes.
Write the draft, tags included, to a scratch file outside the repository and run `formal handoffcheck DRAFT` (with no file it reads the draft from standard input); fix what it flags and re-run to exit 0 (exit 2 means it could not check — a draft without the tags among the causes — a failure, not a pass).
It checks the decidable invariants only — the session attribute, the closing tag, the continue-reason clause, the banned phrases, the register warning wherever a record is named (a path under `formal.toml`'s `records`, an id, a file of `meta_names`, a key of `key_patterns`), workspace-relative paths (an absolute path, or one under a directory the project does not name, left alone), the `Refute first:`, `Bundle shape:` and `Commissioned:` lines, the bundle-words sentence — and a pass does not replace re-reading the prompt against the current text it quotes: a prose correction invalidates any handoff built on it.
Make the prompt self-contained — the file, the exact declaration signatures, the proof strategy, the reused lemmas with their files, the guard to add — and carry the hard gate: the prover session pushes nothing anywhere.
Keep the draft until the landing: the `land` skill passes it to `formal handback --handoff DRAFT`.

---
name: land
description: Land a prover session's handback — verify the report at the tree (the manifest diff with `formal handback`, a cold read-back of every landed statement from a packet `formal readback` builds, the binders tiered, the guards), sweep the drift the landing caused, write the document's rows and the registration from the LANDED proof, close the records and commit with named paths. Use whenever a prover session reports back, whether the agent or the owner's own session. When the person says 'land' or 'land the handback', they mean this skill — call it every time, even if it ran earlier in the session, and take every step.
license: Apache-2.0
compatibility: Python 3.11 or later, standard library only, for `scripts/formal.py` (`formal probe`, `init`, `check`, `rows`, `resolve`, `handoffcheck`, `handback`, `readback`, `cite`, `anchors`, `register`, `hypotheses`, `witnesses`); git for the manifest diff; the prover, its build and the manifest generator `scripts/DeclManifest.lean` (Lean 4; another prover writes the same rows its own way) are the project's. Needs `formal.toml` at the project root, which `formal init` writes.
metadata:
  version: "0.12.1"
  script: scripts/formal.py
---

# Landing a handback

The prover session left its work UNCOMMITTED by design and handed back a report; the report is a claim about the tree, and every step below reads the tree rather than the report.
The tool is `scripts/formal.py` beside this file, run by its path from the project root (`python3 ${CLAUDE_PLUGIN_ROOT}/skills/land/scripts/formal.py …` under Claude Code; `formal …` below means it), reading `formal.toml` at the project root: the workspace, the prover session's instructions, the declaration manifests, the library roots with their package directories, the documents whose cited names and anchors are read, what ships and the register it never carries, the handoff's bans.
`formal init --workspace DIR` writes the bindings file with every binding explained, `[packages]`, the manifests and their commands filled from the workspace's lakefiles (`--force` overwrites one that exists), and `formal init --print-instructions` prints the paragraphs for the project's instructions file for `formal.toml` as it stands, writing nothing; `formal check` says the manifests parse and the bindings resolve, and, with `[packages]` bound, that the manifests' modules are the tree's, that each manifest's `# own roots:` line names roots `[packages]` binds and every bound root its package imports, that each root's umbrella `<Root>.lean` imports every module under `<Root>/` and nothing absent (`umbrellas = false` where a project's umbrella leaves modules out on purpose), and that no module imports one of a later package of `package_order`; it ends with a coverage line.
`formal probe` reports the workspaces under the root with their roots and toolchains, whether each one's `DeclManifest.lean` is the skill's copy or a stale one from an earlier release, the tools on PATH, the project's bindings (whether the research setup's `flow.toml` is there, as information) and the pins, and what the prover side's setup is missing, writing nothing (`--json` for the same as data); the `formal-init` skill reads it.

## 1. `formal handback --handoff DRAFT` — read the WHOLE manifest diff, not the names the report lists

Against HEAD (or `--base REV`) it prints:

- the new public and new private declarations, the removals, the visibility flips, the field changes and the per-module count deltas;
- the INSTANTIATIONS of an existing generic (`mul_comm_int` under `mul_comm`) — the shape a report compresses into one clause and a document boundary turns on;
- the joint-satisfiability witnesses owed: new public theorems with two or more named conditions and no `_nonvacuous` sibling — named conditions only, so count the binders yourself for the rest;
- the guards, `+N -M` in the workspace diff, untracked files included, and the live total after the change, the figure a project that states a guard total writes;
- every document site citing a declaration of a touched module, classed as a row, a boundary paragraph or prose;
- the COMMISSION — every name of the handoff's `Commissioned:` line sorted into four classes: landed, PRIVATE (in the tree, not citable), already at base, and ABSENT.

Everything the report names must be there; everything the diff shows that the report omits is the surplus that makes a document boundary stale.
It exits 1 on a document citing a name that is now private or removed.
It reads no proof: a `sorry`, an `admit`, a `native_decide` or a new `axiom` is the build's warnings and the project's `#print axioms` guards to catch, so quote both in the landing.
Name each ABSENT commissioned declaration in the log entry under what did not land, whatever the report says; a PRIVATE one is in the tree but not citable, so no row names it.
Each manifest is compared with the edited modules of its own package only, so regenerating one package's manifest does not refuse on another's, and an edited umbrella that holds only imports and guards needs no regeneration; a proof-only edit elsewhere still does, since the text cannot tell it from a changed statement.

`formal hypotheses` fails where a public theorem shipped at HEAD (`--base REV`) gained a named condition, and reports the new theorems, the discharges and the theorems gone; against a pinned `--baseline FILE` instead, which lists every public declaration with its conditions (`-` for none), `--update` locks a discharge and a new declaration in and never a growth.
A manifest with no `hypothesis` row is INERT, reported as such and never as a pass.
`formal witnesses` lists, by module, every public theorem with two or more named conditions and no `_nonvacuous` sibling over the whole tree (`--base REV` for those new since it): the sweep's view of what step 1 prints for a landing, a report that fails nothing.

## 2. Read-back BEFORE reading at the binders — a cold reader writes each landed statement out from the Lean alone

The root session opens a declaration with the document already in mind, and that is the condition under which quantifier gaps survive an audit.
So first `formal readback <every commissioned declaration> -o PACKET` builds the packet: each statement with its modifiers and scope lines, every project-local definition its elaborated statement refers to, to depth two (`--depth N` for another; a definition's value is read too), docstrings and comments STRIPPED, its own limits in its header; a bare name declared in two modules is refused as ambiguous and named by module instead.
What a statement refers to is read from the manifest's `uses` rows, which the generator writes from the compiled environment, so a projection `x.f`, an inherited field, dot notation and an instance are resolved by Lean and not guessed from the text; the source is read only to show each block.
A declaration used that no line of its file declares by name (an instance Lean named, a derived one) is listed, not shown.
A manifest without the `uses` section is an older generator's: `formal readback` refuses it (exit 2) and says to copy `scripts/DeclManifest.lean` over the workspace's and regenerate.
A name the manifests do not list is counted unresolved, so `formal readback` exits 1, and the agent opens the source before taking a doubt the cold reader raises as a finding.
Then one fresh subagent, given the packet and nothing else — no document, no record, no other source file — writes out in plain prose what each declaration literally asserts: every binder and its role, the conclusion exactly as strong as written, what is NOT claimed; "as defined elsewhere" where a name has no definition in the packet.
Where the packet is too large for one cold reader, build one per commissioned declaration (`formal readback NAME -o PACKET` each) and give each its own fresh subagent; a subagent never reads two halves of one statement.
Compare that prose to the document's statement sentence by sentence and quantifier by quantifier, and record the verdict per declaration in the log entry, quoting any mismatch verbatim.
A mismatch is resolved by changing the ROW or sending the statement back — never by reading the document into the Lean.

## 3. Open every commissioned declaration at its binders, and TIER every binder

The manifest resolves a NAME; the statement behind it is read in the source — quantifiers, hypotheses, what is existential and what is universal, the guard's own axiom line — copied from the file, never from the report and never from the design record that commissioned it.
Every binder is one of four tiers: VERBATIM (the document's statement carries it); ADAPTER (an encoding the document has no counterpart for — a typeclass instance, a decidability, finiteness or measurability witness, a carrier's encoding; the packet's instance-binder line is where this tier starts, not where it ends); IMPLIED (a regularity the document assumes globally and states once); UNANCHORED (a proof-route convenience with no counterpart).
"Implied" is never the sole justification for a binder that changes the statement's strength, and an UNANCHORED binder is not written into the document's statement as mathematics until the landing has said why it is there.
Guards commissioned together — one refuting instance per hypothesis, described in parallel — are read one by one, each at its own statement, since parallel prose is not evidence of parallel binders: whether its witness is in the statement or only built in the proof (an `∃` over worlds names none), at which stage or parameters it is stated, and whether it proves a value or only a bound; each row is written from its own guard.
A theorem under a hypothesis A and a guard refuting it under a condition B make an "exactly when" only where B is literally not-A: put the two conditions side by side before any threshold or two-sided sentence, since a guard shows a hypothesis cannot be deleted, not that it is sharp.

## 4. The gates over the tree

`formal check`, then the three gates over what the landing touched, each with its bindings in `formal.toml` and each exiting 1 with every site named:

- `formal cite`: every declaration name a scanned document backticks resolves in the manifests — a cited `X.lean` is a module; a dotted name, once `[documents]`' allowlists (`upstream`, `notation`, `open_targets`, `retired`, `ambiguous_namespaces`) have not taken it, whose first component is a namespace segment at any depth of a manifest declaration's name or a module's last component, is exactly a declaration, a field or a module, or a module path written from below a root (`Code.BitGates` for `Root.Code.BitGates`), or the end of every manifest name it ends on a component boundary (`Host.lemma` for `Root.Host.lemma`), or `Module.name`, a declaration with that base in a module `Module` ends (`Code.thing`), and drifts where it is none of these; a name scoped under a declaration, its first component a base name of the manifests, ends a manifest name; a dotted name whose first component is none of these is an upstream name and stays unread; any other declaration-shaped name resolves against the modules its own line names, then by its last component or a dotted suffix, then as a module or a namespace, then against the allowlists; one resolving only to private declarations, a retired name still in the manifests and an API-docs link (`docs_url`) to a module not in the tree drift.
  It reads a name as cited whatever the sentence says of it, so a document never names a declaration to say it is absent; `formal cite --json` prints one JSON document in the text's place, with each citation that resolved, a namespace-scoped or module-qualified one among them (document, line, token, kind and the sorted declarations it resolved to), the allowlisted tokens by list, `unread` (each dotted token left unread because its first component is in `ambiguous_namespaces` and would otherwise be read: document, line, token and that namespace; a first component that is simply unknown is not listed), the drift and `ok`, and exits as the text does, so a tool that needs the cited declarations reads them rather than copying the rule;
- `formal anchors`: every `[Key] §N` (each endpoint of a chain), `[Key] Theorem N.M` (the kind matching, abbreviations read whole) and `[Key] Appendix X` in the files of `[anchors] scan` names a numbered heading, a bold numbered statement or an appendix heading of the document the key is bound to, with no fallback from a heading to a same-numbered statement, and a statement riding a section anchor lies in that section; bare keys are counted as the frontier.
  An anchor that resolves may still name a section other than the one meant;
- `formal register`: the tracked files under `[register] ship`, minus `exclude`, carry none of the bound pattern classes — internal vocabulary, case-sensitive tags, stage forms, private paths, a package naming nothing above it by `scope` — each line matched after the `sanctioned` expressions are cut from it, so an internal tag beside a sanctioned word still fails; and every `.lean` file name a file class's `scope` mentions (`[[register.files]]`), bare or with a path, is a module of the class's `packages` (omitted: each file's own package and those before it in `package_order`) or matches its `allow` as written, the files of another project (`^Average\.lean$` allows a bare `Average.lean`, not `ALT/Ergodic/Average.lean`; a path needs its own expression, as `^Mathlib/`), so a lower package never points at a file above it; an empty scope fails as rot, since what ships carries zero internal register: a docstring renders into the public API docs.

Where the project states tree-derived figures (guard totals, module counts), run its check, quote the drift list and sweep every site it names; write the new TOTAL, never a delta, the guards' as step 1's live total prints it.

## 5. Register by the project's test, then write the rows and the registration from the LANDED proof

Whether and where a landed result enters a document is the project's rule, read from its instructions, and where it has none the `method` skill's register test under Documents; the `method` skill's honest-change invariants hold where the statement moved.
A row cites the file and the bare declaration name, never a private name, and never names a declaration to say it does not exist; its boundary paragraph names each ADAPTER binder as such and each UNANCHORED binder with the landing's reason; a theorem with two or more hypotheses cites its `_nonvacuous` witness, or says the witness is owed.
A sentence saying a result is the first in any prover is checked by one prior-art search per ingredient, never one search for the whole.
Draft the rows in a scratch file and run the project's text gates on the draft before writing them.

## 6. Sweep the SUMMARY sites, not just the detailed ones

The recurring failure is a qualifier carried in the row and dropped at the headline: the statement's status label, the main results, the abstract, the contributions, the settled-and-open lists, the boundary paragraph of an EARLIER row that named this one as the gap, an earlier row that stated its boundary by POINTING at this one's, the not-formalized list, the registry's per-document line, the companion prose, the proof paragraph's "the only named hypothesis is X", which goes false when a clause consumes another; and every negative-coverage sentence about the landed result's KIND, in every document ("no statement in this series…", "nothing here relates…", "stays open"), found by grepping for the kind's words, since no gate reads them.
If any part stays conditional, the STATUS LABEL carries it.
A sentence found false of the tree is corrected here, in this landing — never put to the owner as a decision, unless the project's instructions say the owner is asked before any correction, in which case it is put to them with its evidence.

## 7. Gates, records, commit

The project's offline gates by exit code; then, where the research plugin is set up in the project (`flow.toml` at the root), the flow; where it is not, the landing is recorded by the document rows and the commit, and the steps below that name `flow` and `/research:audit` are skipped.
`flow make TASK --resolution DRAFT` closes the prover's task, done and archived, and a closed card is in no deck and no hand, so the task leaves the agent's hand and its deck (the hand `[hand]` names `agent` by default, and a project that names its hands otherwise uses its own name wherever a command here takes an owner); it mints nothing.
Each finding is then minted from the LANDED proof with `flow finding TITLE --summary S --evidence EVIDENCE… --ref TASK`, EVIDENCE the declaration in the formal form (`formal:Path.lean#decl`, the path relative to the workspace, not to the project's root) and the document row in the stated one (`stated:papers/x.md#FV-1`; an item that does not resolve against the manifest or the document refuses the call), with `--ref F` for a finding it rests on; a finding whose formal item lands later gains it with `flow evidence F formal:Path.lean#decl`.
The one finding that settles the question carries `--answers Q`, which closes it; the question's other findings carry `--ref Q` without it.
A handoff that failed is `flow abort TASK --reason R`, its refuting finding minted after it the same way, `--ref TASK --tag refuted`, its evidence the guard or the probe that shows the failure.
A residue is a `flow idea`, a `flow question "…" --summary "…" --ref F`, its body saying what would answer it, or a `flow park ID --reason R --revival V`, never a "what stays open" line appended to the question's body; a question found wrong is `flow wrong Q --reason R`, one shown impossible `flow impossible Q --by F`, and an idea, an open question, a task never started or a finding found false dropped is `flow remove ID --reason R`, a task that was started being aborted instead (`flow abort T --reason R`).
Commit with NAMED paths — the prover session's sources, the package files, the manifests and the documents swept — never everything at once, since a sibling's in-flight work has been swept into a mislabelled commit that way.
Where the research plugin is set up, and the landing rewired a cross-document import, run the consistency audit (`/research:audit`) in the same session, before the commit; if it did not, say so in the entry.

## The manifest generator

`scripts/DeclManifest.lean` beside the CLI writes a Lean package's manifest in the row grammar the CLI reads (the research flow asks `formal resolve`, below, and reads no manifest): from the workspace, after a genuine build, `lake env lean --run DeclManifest.lean --roots Root1,Root2 --out ../scripts/decls.txt`, with `--own` naming the roots whose Prop-valued definitions count as named conditions, by default every root built in the workspace's own packages — a package required by path among them, a dependency's checkout under `.lake/packages/` and the toolchain left out — printed and written as the manifest's `# own roots:` line, which `formal check` holds against `[packages]`, so a command passes `--own` only where the default is not the project's (the project copies the file into its workspace, once, and binds one command per package in `formal.toml`'s `generate`).
It walks the compiled environment, so it needs the build current, and its counting rule is stated in its own header: what counts as a declaration, what is a field, what is private, which binders are named conditions, which instance classes a theorem carries and which declarations a statement refers to.
Another prover writes the same seven row kinds with its own tool.

## The manifests' readers

`formal rows --json` prints `{"schema": 1, "rows": […]}`: every row of the bound manifests in their order, with its `kind`, `file`, `line` and `module`, and the kind's own fields under the names the grammar in `formal --help` gives them (`count` for `module`; `name` for `decl`, `private` and `field`; `theorem` and `condition` for `hypothesis`; `theorem` and `class` for `instance`; `decl` and `const` for `uses`).
It is the one read of the manifests outside the plugin, so a project's own script reads the rows here and filters them by the kinds it knows: a new kind is a new value of `kind` under the same schema number, which moves only when a kind's fields change, and an old reader ignores it.
Without `--json` it prints each manifest's count per kind.
It exits 1, with the file and line and no JSON, where a row matches no kind, since a row is never absorbed into another kind, and 2 where `formal.toml` or a manifest is missing; `formal check` stays the strict validator of a manifest.

`formal resolve TARGET…` says whether each target is a declaration or a module of the manifests: `Path.lean#name`, `Path.lean` (a module), or a name with no path, the module scope left out; `-` reads the targets from the standard input, one a line, for a project's own list of names.
The module is the path without `.lean`, `/` read as `.`, and its file, under the package directory `[packages]` binds for its root, must exist.
A module resolves where a `module` row names it; a name resolves where a `decl`, `private` or `field` row's name is it or ends in `.` and it, among the rows of the module where a `module` row names the module, or where it is `Module.name`, a declaration with the base `name` in a module that `Module` ends on a component boundary, the rule `formal cite` reads too.
It prints a line for each target that does not resolve, with why, then the count, and exits 0 where all resolve, 1 where one does not and 2 where it could not run (no `formal.toml`, a manifest missing, a row matching no kind).
`--public` also fails a target whose every reading is a private declaration; without it a private one resolves, which is the research flow's own claim, existence.
`--json` prints one JSON document in the lines' place, `{"schema": 1, "targets": [{"target": T, "readings": [...], "ok": true}, …], "ok": true}`, an object for each target in the order given: its `readings` are every declaration its name could mean, public and private, in no module's scope, sorted (empty for a module), and `ok` says whether it resolves, with `why` where it does not; the exit code is the text's, so a project's own tool counts every reading of a name without copying the rule.
`formal resolve --protocol` is the research flow's call, never run by hand: one JSON request on the standard input, `{"protocol": 1, "form": "formal", "items": ["Lib/Foo.lean#lemma_L", …]}`, one JSON answer on the standard output, `{"protocol": 1, "items": {TARGET: {"ok": true} | {"ok": false, "why": "…"} | {"unchecked": "…"}}}`, exit 0 whenever it answered, whatever the items say; a missing manifest leaves every item unchecked, with the command that regenerates it.

---
name: runner-merge-claude-branches
description: |
  Use this skill when the user wants to consolidate the many
  per-task ``claude/<task-id>`` branches the runner has pushed into
  one review-ready branch + PR. Triggers:
  "/runner-merge-claude-branches", "merge claude branches",
  "consolidate the task branches", "fold all the model-extraction
  branches into one PR", "build a mega-PR from the runner output".

  A runner queue that has been live for any length of time accumulates
  dozens of pushed but unmerged ``claude/<task-id>`` branches — one
  per dispatched task that committed real work. Opening one PR per
  branch is impractical at that scale; the operator wants one bulk
  PR. This skill orchestrates the merge end-to-end and surfaces
  the right manual steps for the cases the script can't safely
  automate.

  Outputs:
    * a new worktree on a fresh branch off ``origin/main``
    * all eligible ``claude/*`` branches merged in
    * registry artifacts regenerated via R (data/modeldb.rda,
      inst/modeldb.qs2, man/*.Rd, _pkgdown.yml navbar)
    * the Example-models fields of inst/references/covariate-columns.md
      and the other registers union-merged so per-branch annotations
      are preserved (the structured-markdown files that ``-X theirs``
      clobbers)
    * later branches folded into the same branch with ``--fold-in``
    * branch pushed to origin
    * suggested PR title + body printed for the operator to open
      manually via the GitHub web UI (the user's ``gh`` CLI is
      read-only by policy)
---
# /runner-merge-claude-branches — consolidate task branches into one PR

This skill is *partially* automated. The merge mechanics and the
post-merge regenerations are scripted; the operator-facing
decisions (which branches to include, whether `devtools::check`
passes, whether to open the PR) stay interactive.

## Quick start

```bash
bash /home/bill/.claude/skills/runner-merge-claude-branches/merge_branches.sh \
    --repo /home/bill/github/nlmixr2/nlmixr2lib \
    --base origin/main \
    --pattern 'origin/claude/*' \
    --exclude-ref origin/claude/<wip-task-branch> \
    --branch-name "merge-all-claude-branches-$(date +%F)"
```

That single command runs the entire end-to-end pipeline; branches pushed after
it are folded into the same branch with `--fold-in` (see "Fold-in rounds"
below). The survey aborts
(exit 4) when two branches add a file at the same path with different content,
because `-X theirs` would silently keep only the last one; reletter one branch's
files (`<Author>_<Year>a_` / `<Year>b_`) or exclude it. It aborts the same way
when a branch adds a model or vignette path the base gained, with other
content, after the branch forked (a branch that was squash-merged or
cherry-picked to main and then edited there, say): the merge would replace
main's copy with the branch's. A file a branch renames onto a path counts as
adding that path: the survey reads branches without rename detection. `--exclude-ref`
(repeatable) leaves out a branch the pattern matches -- a WIP checkpoint, or a
branch that already has its own PR -- and prints each exclusion in the survey. The flags
have sensible defaults for the nlmixr2lib popPK ingestion use case;
override per repo. `--extra-ref` (repeatable) adds a hand-picked branch the
pattern does not match; it reaches every repair and verify step. An excluded
branch reaches none of them: every helper reads only the merge set (see
"The merge set" below).

From an agent's shell, which has no terminal, pass `--yes` once the operator
has confirmed the scope (step 2): without it the script stops at its
confirmation prompt with exit 3 and creates nothing. `merge_branches.sh --help`
prints every flag and exit code. Each exit code has one meaning; the ones that
stop a run partway are 5 (a repair or verification step failed, the verifier
or the line check could not run, the revert check found base content the
merge reverted, or the pre-check found what `buildModelDb()` would stop on),
6 (`devtools::check`), 7 (push), 8 (vignettes) and 9 (a hand union is needed
before the push, for wording a repair set aside or a loss the verifier or the
line check reported, steps 6b, 6e and 7). A run whose repairs completed is completed from
the same worktree by the `--finish` command its stop prints: it runs the
gates again on the branch and every R step that is not up to date, then
pushes (step 6b). A run that stopped before its repairs completed is re-run
on a fresh `--branch-name`.

## The merge set

`--pattern` matches more than the branches a run merges: branches left out with
`--exclude-ref`, branches pushed after the survey (or pushed to again after
they were merged), and branches from earlier rounds that the base already has.
On 2026-09-29 the helpers still read the 18 branches that run had left out:
6 orphan `**Example models:**` entries and 6 NEWS bullets for models the merge
did not ship leaked in, and the verifiers reported dozens of their
contributions as missing. (Two more orphan entries came from branches that were
merged, from content they had only inherited; see step 6.)

So every repair and verify helper asks `merge_set.py` which branches count,
and what each contributed. For a branch R, consolidation branch B and base:

- **merged commit** `M = git merge-base R B`: R's tip when R is an ancestor of
  B. If R's tip moved on after B merged it, M is the part B merged, and the
  later commits count for nothing.
- R is **in the merge set** when M is not an ancestor of the base, i.e. B
  merged something of R's that the base lacks. A branch never merged has M at
  its fork point, which the base has; a branch from an earlier round is on the
  base. A branch merged only through another merged branch (one an
  `--extra-ref` branch had merged into itself, say) is in it too: its commits
  are in B.
- R's **own diff** runs from its fork point `F = git merge-base <base> M` to M.
  What R has at F it inherited from main; main may have renamed or removed it
  since, so it is not R's contribution.

Each helper prints what the gate left out, and names each branch that moved
on; a branch already on the base is not mentioned. A helper whose merge set is
empty exits 2: the branch or the pattern is wrong, and a check of nothing must
not pass. `python3 merge_set.py --repo ... --branch ...` prints the members,
one `<ref> <merged commit> <fork point>` line each.

## Steps the skill follows

1. **Pre-flight survey.** Identify which `origin/claude/*` branches
   have unmerged commits (i.e. `git rev-list --count origin/main..<br>`
   is non-zero). Print the list, file counts, and commit subjects so
   the operator can confirm scope before merging. Because this skill
   folds branches in with *real merges* (step 4), a branch from a
   previous consolidation round is a true ancestor of main and so
   reports zero unmerged commits — the survey is authoritative on its
   own, with no content-equivalence guesswork needed to tell whether a
   branch is already in. (Historical note: branches folded in via the
   pre-2026-06 *cherry-pick* flow are NOT ancestors and will still show
   as "unmerged" here even though their content is on main; for a
   one-off transition pass over such branches, fall back to a
   path-based check — "does this branch add a model `.R` file whose
   path is absent on main?".)

2. **Operator confirms scope.** Present the list via
   `AskUserQuestion` with options for: all branches, the new-model
   ones only, or a manual pick. (For now `merge_branches.sh` accepts
   `--pattern` for filtering; richer interactive scoping can be added.)

3. **Create the worktree** at `<repo>/.worktrees/<branch-name>` off
   the configured base (default `origin/main`). The new branch
   tracks the base; no commits yet.

4. **Sequential merge.** For each candidate branch, run
   `git merge --no-ff --no-edit -X theirs -m "Merge branch '<br>' into <new-branch>" <br>`.

   - `-X theirs` resolves binary registry conflicts (data/modeldb.rda,
     inst/modeldb.qs2) and overlapping text additions on shared
     metadata files (_pkgdown.yml, NEWS.md) in favour of the
     incoming side. Those files get regenerated authoritatively
     in step 5, so the choice during merge is incidental.

   - **WARNING — covariate-columns.md.** This file's structured
     `**Example models:**` lines get clobbered by `-X theirs` when
     multiple branches each rewrite the same line to add their own
     model. Step 6 below repairs the damage via a union merger;
     do NOT skip that step.

**ORDER NOTE (changed 2026-08-20).** The register repairs (steps 6, 6b, 6c,
6d) now run BEFORE the R regeneration (step 5 below), not after, and so do the
line check (step 6e), the verifier (step 7) and the revert check (step 7b).
`buildModelDb()` calls `checkModelConventions()`, which treats a duplicate
register entry as an ERROR -- and duplicate entries are exactly what `-X
theirs` produces when two branches each add the same new canonical. Running
the regen first aborted the entire pipeline on damage the very next step
exists to repair. Repair, then regenerate.

5. **Regenerate registry artifacts** via R:

   ```bash
   Rscript -e 'devtools::load_all("."); nlmixr2lib:::buildModelDb(); devtools::document()'
   ```

   **Pre-check first** (`precheck_regen.R`). A cold `buildModelDb()` parses
   every model, about an hour, and raises its convention errors only at the
   end. Before it starts, the script loads the worktree's package with
   `pkgload::load_all()` and runs, in minutes, the two checks that stop it:

   - the package's own `.referenceDuplicateIssues()` over every
     `inst/references/*.md`, as `buildModelDb()` runs it: a canonical
     registered twice under one `- **Type:**` anywhere in a register. It
     reads each register whole, so it finds a canonical filed under two `##`
     sections (`carboplatin` as a suffix twice), which the per-section dedup
     of compartment-names.md and parameter-names.md (step 6b) cannot;
   - `checkModelConventions()` over each model file the round added or
     changed (`git diff --diff-filter=AM` from the base, renames read as
     additions), each loaded with the calls `addFileToModelDb()` makes, so
     the model name the covariate checks see, and the verdict, is the
     build's. A file the build cannot load (a parse error, a model named
     unlike its file, an `nlmixr()` failure) is an error; an error raised
     inside `checkModelConventions()` itself is a warning, since the build
     ignores it too.

   An error stops the run (exit 5) before the regeneration, listing each
   duplicate and each model's errors, with the `--finish` command that runs
   the pre-check and the regeneration again once the fix is committed. A
   package without `buildModelDb()` has nothing to check. One with
   `buildModelDb()` but without either check function cannot be checked as
   the build checks it, which stops the run (exit 5) rather than switching
   the pre-check off after a rename upstream; so does a crash, which the
   script reports as one, never as "what buildModelDb would stop on". The
   pre-check is part of the regeneration step, so `--skip-r-regen` skips it
   too.

   - `buildModelDb()` writes the registry blob (`data/modeldb.rda` plus
     whichever of `inst/modeldb.rds` / `inst/modeldb.qs2` the package
     currently ships) and refreshes the pkgdown navbar.
   - `document()` regenerates `man/*.Rd`.

   **Do not hardcode the artifact list when staging.** The script stages
   whatever the regen actually wrote (`git add -A`, valid because every
   earlier step commits its own work, and guarded by a pre-regen dirty
   check). The old hardcoded list named `inst/modeldb.qs2` — a path on this
   script's own forbidden-resurrection list, because nlmixr2lib had already
   moved to `inst/modeldb.rds`. It therefore staged a file that could not
   exist and never staged the one that did, which would have pushed a
   registry blob stale against 181 new model files.

6. **Union-merge the Example-models fields** of covariate-columns.md and of
   every `--register-file` (compartment-names.md and parameter-names.md by
   default) via `union_merge_lines.py`, one commit per file it changes. Each
   register lists models under its canonicals the same way, and `-X theirs`
   drops the entries of every branch but the last that edited a field. The
   union buckets entries by (`##` section, `###` heading), so a token two
   sections of compartment-names.md both register (a compartment and a
   suffix) keeps its entries apart, and the per-section dedup that follows
   finds no duplicate it made. This script:
   - Reads each branch in the merge set whose own diff touched the file, at
     its merged commit.
   - Takes from each branch only the `**Example models:**` entries it added,
     or whose annotation it changed, relative to its fork point. An entry it
     merely inherited is main's, and main may have renamed or removed it
     since: on 2026-09-29 the pre-rename `Willmann_2018_rivaroxaban.R` came
     back twice that way, from branches that had been merged.
   - Reads each Example-models field whole with the dedup's parser (label
     line, wrapped lines, sub-bullets), buckets the entries by (covariate
     header, subsection), where a copy's `###` heading that declares one of
     the merge result's heading's names is that heading (a branch may add a
     name, reorder them or reword the description while another adds a
     model), and unions them with the base's, keeping the most
     informative (longest) annotation per filename. Every other annotation
     that sets aside goes to the hand-union report (step 6b), beside the one
     kept.
   - Honours what a branch removed or corrected, not only what it added. An
     entry the branch removed (a rename, a re-filing under another heading)
     is dropped where the base still has it, and a renamed one keeps the old
     one's place; an annotation the branch changed wins over the longest
     when the base still has the wording the branch inherited. When main
     changed the entry too, the base's stands. Without this, a rename brought
     the old name back beside the new one, and a same-length correction
     ("12 mg" to "21 mg") lost to the base under "longest wins". A removal
     counts only where the branch still has entries under that heading (a
     renamed heading is not a removal of its entries), and a line every
     entry of which was removed is left as it is and reported.
   - Edits each Example-models field the union changes in place: the field's
     own entries keep their places and their text, prose before, between and
     after them stays, a model listed twice stays listed twice, and the
     branches' additions go after the field's last entry, in its form.

   **The emitter is idempotent.** Running the union twice, or three times,
   gives what running it once gives. Each entry is its filename and note, up
   to the next entry, a `;` or the full stop that ends a sentence, outside
   parentheses and code, wherever the entry stands; a closing remark after
   the last entry belongs to the field, so it never moves onto an added
   entry and is never doubled. Notes are compared by what they say, not by
   their form (`(text)` inline and `-- text` in a sub-bullet are the same
   note), so a carried note does not flip between forms. A `(` that nothing
   closes, and either bracket of a half-open interval (`(4.87, 8.56]`), is
   text and hides no entry, and the full stops that end a field are left as
   they are. A field the union changes nothing in is left byte for byte.
   Prose a branch added to a field that the result lacks, and a branch's
   models for a field that lists none (prose such as "none yet", which is
   never rewritten), go to the hand-union report (step 6b).

6b. **Dedup duplicate canonical headers** via
   `dedup_canonical_headers.py --global --report <report> inst/references/covariate-columns.md`.
   The union-merger folds Example-model *lines* but cannot collapse a
   whole duplicate `### CANONICAL` *block* — which is exactly what
   survives when two branches each ADD the same brand-new canonical
   (both branched from an older main, so `-X theirs` keeps one copy per
   branch). `verify_section_headers.py` only checks headers *survived*,
   not that they are *unique*, so these slip through (8 such pairs were
   on origin/main on 2026-07-25). Headings that declare a name in common
   are copies of one entry, whatever else they declare and in whatever
   order (`### fm_a` and `### fm_b, fm_a`), as nlmixr2lib's own register
   parsers read a heading. This step collapses each to one entry,
   keeping the copy the base has (`--prefer`, the register as `--base` has
   it), else the longest, and carrying into it every model a dropped copy
   lists as an Example-models entry that it lacks (each as written, with
   its annotation, or the bare filename; an entry starts at every
   backticked `*.R` filename outside parentheses, so `` `A.R` and `B.R` ``
   is two entries and a filename inside an annotation is none). A field is
   read whole: the label line, the lines that continue it, and its `-` or
   `*` sub-bullets, under an inline list too. It also carries the dropped
   copies' source-alias sub-bullets, and then re-runs with `--check`; any
   duplicate that survives **aborts the run**. Keeping the base's copy
   means a branch that re-registered a canonical main already had leaves
   main's wording in place, so the revert check finds nothing reverted.
   What a dropped copy words differently
   (the heading, Description, Role, Notes, an Example-models entry for a
   model both copies list, ...) cannot be unioned mechanically; the
   register keeps the kept copy's wording, the script prints `HAND UNION
   NEEDED` with the fields, and the dropped wording goes verbatim to a
   hand-union report in the worktree's git directory, never into the
   register. The union merge (step 6) and the restore (step 6c) append to
   the same report: an annotation "longest wins" set aside, and a canonical
   two branches added in different words, and so does the verifier (step 7):
   each contribution it reports missing. Every later step still runs; the
   run then stops before the push (exit 9) and prints the worktree, the
   report and the `--finish --hand-union-done` command, and any later
   failure (check, vignettes) names the report too. Union the wording into
   the register by hand, keeping each source's attribution, commit in the
   worktree, and run that command, without redoing the merge. The command
   names only `--repo`, `--branch-name` and any vignette settings: the run
   records its other inputs
   (`--base`, `--pattern`, `--extra-ref`, the union and register files, and
   every ref it merged) in the worktree's git directory, and `--finish` uses
   them, refusing a conflicting one given on its command line (exit 2) and
   reading every merged ref at the commit the run merged, so a ref rewritten
   or pruned since changes nothing; a recorded commit missing from the
   objects stops it (exit 3). `--finish`
   runs the run's gates again on the branch as the hand edits left it: the
   duplicate check, the revert check (a hand edit that drops base content
   stops it, exit 5) and the contribution verifier. Then it runs the
   regeneration and check if the run's never completed or HEAD has moved
   since they did -- both read the registers, so a hand union counts, and
   the committed artifacts must match the tree pushed -- and the vignettes
   if they never completed or a commit since touched a file other than the
   run's registers (a model or vignette fix does; a hand union alone does
   not). A step the run skipped stays skipped, and a `--skip-*` given to
   `--finish` skips a step still due.
   A pending step with no `Rscript` on PATH stops it (exit 3). Then it
   pushes the branch and prints the PR text. `--finish` completes any run
   whose repairs (the union, the dedups, the restore and the NEWS union)
   completed: one that stopped for a hand union (exit 9), at the revert check
   or a failed regeneration (exit 5), at check (exit 6), at the push
   (exit 7) or at the vignettes (exit 8), or was interrupted after its
   repairs; each of those prints the `--finish` command, bare except at the
   hand-union stop, so `--finish` itself says when the report needs
   `--hand-union-done`. A run that stopped before its repairs completed (a
   repair that crashed, duplicates left after the dedup, a verifier that
   could not run) is refused (exit 3), since `--finish` redoes no repair:
   re-run it on a fresh `--branch-name`. `--finish` also refuses a worktree
   with uncommitted changes or untracked files, listing them, since a step
   that failed or was interrupted can leave partial output. Without
   `--hand-union-done`, `--finish` prints the report and stops (exit 9)
   while it holds anything. The report lives in the worktree's git
   directory and goes with the worktree; copy it before removing one.
   `--global` (whole-file
   uniqueness) is correct for the covariate register; the default
   per-`##`-section scope is what you'd use on `compartment-names.md`,
   where the same token is legitimately both a compartment and a suffix.

6c. **Restore whole canonical blocks dropped by the merge** via
   `restore_dropped_sections.py`. This runs against `--union-file` AND every
   `--register-file` (default `compartment-names.md`, `parameter-names.md`),
   which are deduped with per-`##`-section scope rather than `--global`.
   Restricting the repairs to the union file alone lost 11 canonical blocks
   on 2026-08-31 across two registers that 23 and 11 branches had touched. The union-merger folds Example-model
   *lines* inside buckets that already exist; it cannot bring back a
   canonical whose ENTIRE `### NAME` block is gone. That happens when a
   branch adds a brand-new canonical and a later branch (cut from an older
   main, so lacking it) touches the same region -- `-X theirs` takes the
   later copy and the block vanishes. `verify_branch_contributions.sh`
   REPORTS this but does not repair it, so it was a manual step on every
   large merge: **21 blocks on 2026-08-20 alone** (AUCMIC_TYLO, HEPARIN_RT,
   CNSREG_PFC/SC, SNP_SLC22A1_RS2282143, STUDY_TLV_PHASE2/3, ...). The
   script preserves each branch's own `##` placement rather than
   re-categorising, and is idempotent.

   **It is gated on the merge set (added 2026-09-13).** Without that gate it
   resurrected blocks that had been removed ON PURPOSE, which is worse than the
   loss it repairs -- on an 80-branch round it proposed 31 blocks of which 20
   were pre-rename spellings. Three skips, each reported in its output:

   - **the merge set** -- only branches in the merge set (see "The merge set"
     above) contribute, each read at its merged commit; the `--pattern` glob
     also matches earlier rounds, branches left out with `--exclude-ref` and
     branches pushed after the survey. A branch that moved on after it was
     merged contributes the part that was merged. (The ancestry test this
     replaced skipped such a branch outright, so a block it contributed and
     the merge lost was not restored.)
   - **fork point** -- only blocks a branch ADDED count. Comparing against the
     current base is not enough: when main renames a canonical, every branch cut
     before the rename still carries the old spelling, which is then absent from
     both the base and the merge result. Comparing against the branch's own
     `merge-base` shows it was inherited.
   - **deliberate removal** -- a name removed by a NON-MERGE commit on the
     branch was retired on purpose (e.g. applying an operator naming ruling
     that post-dates the branch); restoring it would undo the rename on every
     re-run. Tested by comparing PARSED BLOCK SETS across each non-merge commit
     (present in the parent, absent in the commit), which is immune to
     `union_merge_lines.py` rewriting the file and moving every header. Note
     that a name can ALSO vanish at a later MERGE -- that is the real loss this
     script repairs, so only non-merge commits count. Both simpler tests fail:
     scanning diffs for removed `### ` lines mislabelled 526 blocks, and
     "present at the last merge commit" breaks as soon as a reconciled branch
     has more branches folded into it, which is how a consolidation grows.

   It also indexes EVERY name in a multi-name header (`### fm_a, fm_b, fm_c`).
   When a folded branch added a name to a header that survived under a different
   name, the block is present but the name is not; re-inserting the block would
   duplicate it, so that case is REPORTED for a manual header union rather than
   auto-repaired. `buildModelDb()` fails on those until fixed -- that is how the
   loss of `fm_cysmer` / `fm_gluc` / `fm_sulf` surfaced when no register
   verifier caught it.

   Every `### ` heading counts, a backticked one (`` ### `prob_<endpoint>` ``)
   or prose included. Like the dedup, the union and the placement check, it
   reads a heading's names as nlmixr2lib's register parsers do: a backticked
   name keeps its backticks, so `` ### `prob` `` is not `### prob`. When two
   branches added the same canonical in different words and the merge lost
   it, the first branch's copy is restored and each other copy is printed in
   full and appended to the hand-union report (step 6b), for a hand union.
   Any later heading that shares a name with the restored one is such a copy,
   whatever order it lists the names in. So is a name a branch added to a multi-name heading that the merge kept
   without it.

   Regression tests: `tests/unit/test_restore_dropped_sections_gate.py`.

6d. **Union-merge NEWS.md** via `union_merge_news.py`. NEWS.md has ONE
   append point (`# development version`), so every branch edits the same
   lines and `-X theirs` takes the last branch's whole copy -- which, being
   cut from an older main, is missing what main accumulated since. The loss
   is doubly silent: entries already on main are DELETED *and* every other
   branch's bullet is dropped. On 2026-08-20 NEWS.md came out of the merge
   **85 lines short with not one of the 169 merged models represented**; an
   earlier round lost 60. The script rebuilds from base plus **the bullets
   each branch in the merge set added**: present in NEWS.md at its merged
   commit, absent at its fork point. A branch left out of the merge adds
   nothing, and one that moved on after it was merged adds only what the
   merged part added. The new bullets go before the development
   section's first bullet, each followed by the separator the file puts
   between neighbouring bullets (a blank line, or none).

   This provenance gate replaced one that parsed "Add <Author> <Year>" and
   kept a bullet when a shipped model file had that author and year. On
   2026-09-29 that was wrong both ways: it kept six bullets from branches
   left out of the merge, because another shipped model shared their author
   and year ("Add Wang 2020 caspofungin" rode in on a shipped Wang 2020
   model), and it dropped bullets whose file stem spells them differently: a
   lettered year (`Chen_2021a_tacrolimus.R`) or a surname particle ("Le
   Marouille", `Marouille_2021_palbociclib.R`). Reading each branch's whole
   file also brought back three bullets main had reworded since those
   branches forked, in their old wording, beside the new. The rebuild now
   lists any bullet of the merge result it drops.

   A branch can also reword or delete a bullet it inherited (the citation
   corrections of 2026-10-10 rewrote seven "Add ..." entries). Reading only
   additions kept both wordings: the base's old one in place, the branch's
   new one at the top. Each branch's fork and merged copies are now aligned
   bullet by bullet. A bullet missing from the branch's copy is paired with
   the most similar new bullet in the same stretch, which replaces it in
   place in the base's history; one with no similar replacement was deleted
   and is removed; both are named in the output. A bullet the branch only
   moved is still in its copy and is left alone. When main had changed that
   bullet too, the branch's wording is added at the top with a NOTE, so the
   possible duplicate gets reviewed. A branch that deletes more than ten
   inherited bullets, or a fifth of them, stops the run (exit 2, so
   `merge_branches.sh` exits 5): that is a truncated file, not deliberate
   deletions.

6e. **Line check** via `verify_added_lines.py`, on the union file, every
   register file and NEWS.md, after the NEWS union. When two branches add
   lines at the same place, `-X theirs` keeps the later merge's hunk and the
   earlier branch's lines vanish: sentences several branches appended to one
   canonical's Notes line, of which only the last survives, or a canonical
   two branches added in different words at the same place, of which only
   the later copy survives under the same heading. The revert check (7b)
   guards only the base's content, the restore (6c) only blocks whose every
   name vanished, and the verifier (7) reads filenames, headings and aliases;
   none of them reads those lines.

   For each branch in the merge set whose own diff touched the file, every
   non-blank line its merged commit adds to a block must be kept in the
   matching block of the result: blocks match by a name their `###` headings
   share, in any `##` section, and a section's lines before its first `###`
   by the section's name. Headings of one name in two sections are one
   block, so a canonical moved between sections keeps its lines, and a line
   one of them holds counts as kept for both. Whether a block keeps a line
   is the rule in `register_lines.py`, which the revert check (7b) uses too:
   a field line (`- **Notes:**`, say) is kept word for word or with each of
   its sentences whole in one line of the same field, so a hand union that
   joins two branches' sentences into one line keeps both (the full stop of
   an abbreviation such as e.g., vs. or et al. ends no sentence); any other
   line, a heading included, only word for word. A sentence kept under
   another canonical does not count. Example-models lines are compared entry
   by entry, since the union rewrites them: each entry the branch added, or
   whose note it changed, must be filed under a heading that declares one of
   its heading's names, in any section, with a note that says at least what
   the branch's says. Wording a repair already set aside in the hand-union
   report (6b, 6c, 6) is counted, not reported: `--hand-union-done` is the
   decision for it. That exemption matches the report's lines exactly, and
   holds for the rest of the round, `--finish` included, once
   `--hand-union-done` is given: the line check does not ask again about
   wording the report holds.

   Each loss goes to the hand-union report and the run stops before the push
   (exit 9), the way the verifier's losses do; `--finish` runs the check
   again and stops while a loss is left, unless `--accept-line-losses`
   accepts what is left. Given on the run itself, `--accept-line-losses`
   turns each loss into a WARNING. A hand union that rewords a branch's line
   keeps it reported until it is accepted: that is the decision the report
   asks for. Exit 2 (it could not run) stops the run with exit 5.

   Regression tests: `tests/unit/test_verify_added_lines.py`.

7. **Verify no contributions were lost.** Run
   `verify_branch_contributions.sh`, which now applies THREE checks per
   branch, per register file:

   a. **Filename** — every distinct `*.R` the branch added must appear
      somewhere in the reconstructed file.
   b. **Section header** (`verify_section_headers.py`) — every brand-new
      `##` / `### CANONICAL` header the branch introduced must survive.
   c. **Placement** (`verify_register_placement.py`) — every
      *(canonical, model.R)* pair the branch recorded must still be filed
      **under that canonical**, and every source-alias bullet it added must
      still be under that canonical (the same words; inside a longer bullet
      counts). A model is filed only as an Example-models entry, inline or in
      a `-`/`*` sub-bullet, read the way the dedup reads entries: a filename
      inside another entry's parentheses, an alias bullet or Notes prose is a
      mention, so a merge that kept only the mention of a lost model reports
      it.

   Check (c) was added 2026-08-31 because (a) and (b) both pass in the case
   that matters most: two branches register the SAME canonical from mains
   lacking each other's copy, `-X theirs` keeps one entry, and the other's
   aliases and example models are discarded. The surviving entry keeps the
   header (so (b) passes) and the dropped models are usually cited elsewhere
   in the file (so (a) passes). Four such losses survived every check on the
   97-branch consolidation: `UGT2B15_STAR2_HET`/`_HOM`,
   `RRT_CRRT_EFFLUENT_FLOW`, and `lkst`.

   Two subtleties, both learned the hard way:

   - All three checks read only **the merge set**, and only **what each
     branch added**: its own diff, from its fork point to its merged commit.
     The queue keeps pushing while a merge runs and `--exclude-ref` leaves
     branches out, so the pattern also matches branches that are not in the
     merge; on 2026-09-29 the unmerged branches produced dozens of false
     "missing" reports. Content a branch merely inherited is main's: if the
     merge loses it, step 7b reports it against the base.
   - A header may name several canonicals sharing one block
     (`### QTc, QTcF, QTcI, QTcP, QTcS`), and that list GROWS as spellings are
     ratified. Checks (b) and (c) index each name separately, so a block that
     *gained* a name is not read as a different canonical with everything
     under it lost.

   The verifier exits 1 when it finds losses. Each is one no repair could put
   back (a canonical two branches filed under different `##` sections, a new
   section header the union does not relocate), and settling it needs
   judgement, so `merge_branches.sh` appends the verifier's report for every
   register with losses to the hand-union report, runs every later step, and
   stops before the push (exit 9) with one message naming the files, the
   report and the `--finish` command. Reconcile each loss by hand in the
   worktree and commit, then run `--finish --hand-union-done`: it runs the
   verifier again, pushes a branch it finds whole, and stops (exit 9) while
   a loss is left unless `--accept-verifier-losses` is given, which accepts
   what is left. Passed on the run itself,
   `--accept-verifier-losses` turns each loss into a WARNING and the run goes
   on to the push. The verifier exits 2 when it cannot run at all: a `--base`,
   `--branch` or `--extra-ref` that does not resolve, no worktree for the
   branch, a `--pattern` matching nothing, an empty merge set, or no
   `python3`. Each of those used to pass silently -- a verifier
   that checks nothing reports everything present -- and `merge_branches.sh`
   now stops with exit 5 on them. The helpers it calls (`union_merge_lines.py`,
   `restore_dropped_sections.py`, `union_merge_news.py`, the two delegated
   verifiers, `verify_no_base_reverts.py`, `merge_set.py` and
   `dedup_canonical_headers.py`) apply the same rule: a missing worktree, file
   argument or matching branch, or an empty merge set, is an error, never a
   skip.

   **A report against a multi-name heading is real.** This section used to
   call such a report (`### fm_125d3, fm_1ohm, ...`) a known false positive,
   to be confirmed against the file and set aside. On 2026-09-29 the `fm_*`
   placement reports were real: a branch cut before main added nine pathways
   to that heading won the merge, and the heading lost them, with main's
   example entries, a paragraph and the wording of its notes.
   `buildModelDb()` passed anyway, which proved nothing; the package's
   convention tests then failed on 16 models. Checks (b) and (c) compare
   heading names one by one, so a heading whose list merely grew is not
   reported; content of the base lost this way is reported by step 7b, which
   stops the run. Treat any report as real until the file shows otherwise.

7b. **Revert check** via `verify_no_base_reverts.py`, on the union file and
   every register file, after the NEWS union and before the regeneration.
   `-X theirs` resolves a conflicting hunk with the incoming side, so a
   branch cut from an older main can put back its older copy of a whole
   block: main's newer lines vanish although the branch never touched them.
   The repairs above cannot see this -- they restore what BRANCHES added --
   and the regeneration can pass. On 2026-09-29 a stale copy of the
   `fm_<pathway>` block in parameter-names.md lost the nine names above, and
   a new `### CONMED_RTV_CC` block pasted into the middle of
   `CONMED_RTV_AUC_12H`'s notes line cut it in two, taking its second half
   into the new block.

   It reports every piece of the base's content that the merge result lacks
   and that no merge-set branch's own diff removed; a line a branch edited or
   deleted on purpose is therefore not reported. Content is compared block by
   block: a `### ` block is matched, within its own `## ` section, to the
   result's blocks that share a heading name with it (a multi-name heading is
   split on commas, and its `(**...**)` description is not a name). So a
   block that moved is not a loss, and a token two sections both use
   (compartment-names.md registers some as a compartment and as a suffix) is
   never matched across them. Each heading name, the heading's description,
   each Example-models entry and its annotation, and every other non-blank
   line must survive; how many full stops end an Example-models line is not
   compared. A line survives as `register_lines.py` counts a line kept (the
   line check's rule, step 6e): word for word, or, for a field line, with
   each of its sentences whole in one line of the same field in the matching
   block. So a hand union that joins a base line's sentences with a branch's
   keeps the base line, and one that drops a sentence does not. A line cut in two by a pasted block -- its first part kept, the
   rest now ending a line of another block -- is reported even though the
   branch's own commit did it, which is what happened to CONMED_RTV_AUC_12H.

   Exit 0 is clean, 1 lists every affected block and line, 2 means it could
   not run. `merge_branches.sh` stops with exit 5 on either of the last two,
   before the regeneration. Nothing is repaired automatically, because which
   copy of a block is right needs judgement: put the base's content back by
   hand, keeping what the branches added, commit, and re-run the check until
   it passes. Replayed on the 2026-09-29 merge after the automated repairs,
   it reported those two blocks and nothing else; the hand-repaired branch
   passes it.

   Regression tests: `tests/unit/test_verify_no_base_reverts.py`.

8. **`devtools::check` pre-push gate**:

   ```bash
   Rscript -e 'devtools::check(error_on = "error", args = "--no-build-vignettes")'
   ```

   The `--no-build-vignettes` works around the known-pre-existing
   CarlssonPetri segfault on this codebase. Expect `0 errors / 0
   warnings / 1 note` (the `.git`-in-worktree note is pre-existing
   and ignorable).

   **Important**: this gate does NOT cover vignette evaluation. Step
   8b below does that — do not skip it.

8b. **Parallel vignette validation pre-push gate** (HARD gate; exit
    code 8 on any failure, including a validator that dies before
    recording a result, e.g. on a failed install):

    ```bash
    Rscript verify_vignettes_parallel.R \
      --worktree <worktree> \
      --jobs $(($(nproc) - 2)) \
      --timeout 900
    ```

    Renders every `vignettes/articles/*.Rmd` in a callr subprocess so a
    single failure doesn't poison the others.

    **The gate never touches the user library or the worktree.** It builds
    the worktree's package with `R CMD build` (which works on a copy of the
    source) and installs the tarball with `R CMD INSTALL` into a private
    library inside its own temporary directory, which R removes when the
    gate exits. The workers get that library first on their library path
    and in `R_LIBS`, which a process a vignette starts inherits. Installing
    into the live user library would swap the package under every other R
    session on the host, and `remotes::install_local` cannot reinstall over
    a copy whose `RemoteType` is `git`. Each worker passes its own temporary
    directory to `rmarkdown::render()` as `intermediates_dir`, so the knitted
    markdown and the figures never land beside the Rmd: an `R CMD build` of
    the same worktree running alongside the gate reads a tree the gate
    leaves as it found it. `--skip-install` renders against whatever copy
    the library already has.

    **Each worker runs rxode2 and data.table on 2 threads** (`--rx-threads`,
    0 leaves each package's own default). Both default to half the machine's
    cores: 2 on the 4-vCPU `ubuntu-latest` runners CI renders on, 16 on a
    32-core host. The pin makes the gate render as CI does, which matters
    because an rxode2 simulation seeded with `rxSetSeed()` draws different
    numbers on a different thread count, and keeps `--jobs` workers at 2
    threads each rather than half the cores each.

    **The workers run against a DESCRIPTION-only library path** (default;
    `--full-lib` opts out). The gate links only the packages declared in
    DESCRIPTION's Depends/Imports/Suggests/LinkingTo, plus the render
    harness (rmarkdown/knitr/callr/...), plus the transitive closure of
    both — nothing else on the machine is visible. This exists because a
    vignette that uses an UNDECLARED package renders fine locally (the
    developer happens to have it installed) and then dies on the CI
    runner, which installs only what DESCRIPTION declares. That is not
    hypothetical: pkgdown failed on `Fu_2022_atenolol_qsp` with "there is
    no package called 'units'" *after* this gate had passed all 1215
    vignettes, because `units` was present on the dev box and absent in
    CI. A gate that cannot go red for the thing CI goes red for is not a
    gate. The worker also forces `knitr::opts_chunk$set(error = FALSE)`
    so a chunk error fails the render instead of being written into the
    HTML and reported as success. Continues on failure and
    writes a JSON-lines report (`vignette-results.jsonl`, beside the build
    log `vignette-build.log`, in the worktree's git directory, so neither
    dirties the tree; the failure message prints both paths). The
    orchestrator script (`merge_branches.sh`) runs this
    automatically before push; in that script's own step list it is
    step 9 (the `--skip-vignettes` gate).

    **Why this gate exists.** pkgdown's CI vignette build runs
    sequentially and ABORTS on the first failure. After a 130-branch
    merge that can leave 14+ latent failures undiscovered, each
    surfaced one at a time across many CI iterations. Catching them
    all in one local parallel pass keeps the PR loop short and
    surfaces shared root causes (e.g. the "rxUi auto-injects `cmt()`
    for algebraic observables AFTER ODE states and renumbers slots"
    bug pattern that broke 12 vignettes in the 2026-06-17 merge) in
    one batch.

    **What to do on failure.** The `vignette-results.jsonl` lists
    every failing vignette with its error message. Common patterns:

    - `chol(): decomposition failed` — model has a rank-1 / numerically
      indefinite OMEGA matrix. Re-encode as a single standardized
      shared eta scaled per-parameter in `model({})` instead of a
      multi-eta block with `r = +1`. See
      `inst/modeldb/specificDrugs/Fanta_2007_ciclosporin.R` for the
      canonical example.
    - `'cmt' on observation record or on a undefined compartment` /
      `following parameter(s) are required for solving: <state>` /
      vignette filters dropping all rows — the model declares ODE
      states (`d/dt(central) <- ...`) plus algebraic observables
      (`Cc <- central / vc`) and the vignette event table references
      the observables on observation rows (`cmt = "Cc"`). rxUi
      auto-injects `cmt()` for the observables AFTER the ODE states,
      renumbering slot indices and breaking references to ODE states
      past the inserted slot. **Fix in the EVENT TABLE**: change the
      observation `cmt` value to the actual ODE state name (e.g.
      `cmt = "central"`). rxode2 returns every algebraic observable
      as a column in the output regardless of which compartment the
      `cmt` pointed at — the `cmt` says when, not what. **Do NOT
      add `cmt()` declarations to `model({})`** to silence this; that
      pollutes the model body to mask a bug whose home is in the
      event table.
    - `unique(x) returned >1 value` in dplyr `summarise()` — the
      grouping is too coarse. Fix the `group_by` to include the
      covariate that varies, or switch to `first()` / `mean()`.
    - `callr timed out` — the vignette ran longer than the 900s
      ceiling. Usually a too-large `n_per_group` for the merge's
      parallel-worker contention; reduce the cohort size or raise
      `--vignette-timeout` if the run legitimately needs it.

    Skipping this gate (`--skip-vignettes`) is allowed only for
    iteration. NEVER push without it green on the final pass.

    Regression tests: `TestVerifyVignettesParallel` in
    `tests/unit/test_merge_skill_scripts.py` (the render test needs R with
    nlmixr2lib and rxode2; CI skips it).

9. **Per-task tracking is automatic.** Because step 4 used real
   merges, each source `claude/<task-id>` branch tip is already an
   ancestor of the consolidation branch. Once the consolidation PR
   lands on main, `git branch --merged origin/main` lists every
   folded branch and GitHub marks each as "Merged" — no force-advance
   step, no `post_merge_advance.sh`, no SHA bookkeeping. The operator
   can then delete the source branches at leisure
   (`git push --delete origin claude/<task-id>`). The same ancestry makes
   each completed task's local worktree reclaimable: once the PR lands,
   `claude-task-runner worktree reclaim --queue <queue>` lists them (a dry
   run) and `--apply` removes them with their local branches (ADR-0034).
   The supervisor does this on its own when `[worktree_reclaim].periodic`
   is on.

10. **Push the branch** to origin:

    ```bash
    git push -u origin <branch-name>
    ```

    A failed push stops the run (exit 7). When origin rejects it as not a
    fast-forward, the branch on origin has commits pushed since, and the
    message says so (read them, merge what belongs, or consolidate afresh)
    instead of blaming the remote or the network.

11. **Print the suggested PR title + body** for the operator to open
    manually. The body lists which branches were folded in,
    categorised as new-model additions / vignette ASCII fixes /
    follow-up edits, plus a procedural note on the `-X theirs`
    caveat for covariate-columns.md.

## Things this skill does NOT do

- **Does not open the PR.** Per the user's global instructions the
  `gh` CLI is read-only. The skill prints the title + body and the
  URL the operator can paste.
- **Does not merge into main.** Always pushes the new branch and
  leaves opening / merging the PR to the operator.
- **Does not delete the source `claude/*` branches.** Those stay on
  origin as the per-task audit trail. When the consolidation PR
  merges, the operator can clean up via `git push --delete origin
  claude/<task-id>` as they prefer.
- **Does not remove the per-task worktrees.** That is
  `claude-task-runner worktree reclaim`'s job, after the consolidation PR
  has landed (see step 9).
- **Does not modify the queue's runtime state.** The supervisor /
  daemons / sidecar files are untouched. The merge runs entirely
  inside the nlmixr2lib repo's worktree.

## Important nuances

### Vignette failures are EXPECTED on major merges

Every consolidation of this size has historically surfaced a handful
of broken vignettes that the per-paper extractions did not catch.
The 2026-06-17 merge surfaced 15. Common shapes:

- A model whose IIV block was published with `r = +1` between several
  etas (rank-1 OMEGA) — fine for fitting, but rxode2's Cholesky-
  based simulator can't decompose it. Re-encode as a single
  standardized shared eta.
- Vignettes whose event tables reference algebraic observables
  (e.g. `cmt = "Cc"`) instead of ODE state names. Auto-injected
  `cmt()`s shift slot numbering and break references to ODE states
  and dose history. Fix: in the event table, use the actual ODE
  state name (`cmt = "central"`) on observation rows; rxode2
  reports the algebraic observable in the output dataframe
  regardless. Do NOT add `cmt()` calls to `model({})` — that
  pollutes the model body to silence the symptom.
- Per-vignette code bugs (`unique(x)` on a varying column;
  `filter()` chains that drop every row; cohort sizes that overflow
  the per-vignette timeout under parallel-build contention).

**This is a recurring failure mode**, not a one-off. The validation
gate in step 8b exists specifically to catch all of them in one
local parallel pass instead of dribbling them through the CI
sequential build one at a time. NEVER push a consolidation branch
without the green gate.

### Per-task tracking: real merges make it free

The skill folds each source branch in with a real
`git merge --no-ff -X theirs` (one merge commit per branch), NOT
cherry-pick. This is the design decision that makes per-task tracking
*free*: a real merge makes each source branch's tip a true ANCESTOR
of the consolidation branch, so the moment the consolidation PR lands
on main, every folded branch is reported as merged by
`git branch --merged origin/main` and shown as "Merged" on GitHub.
There is no SHA rewrite, no `post_merge_advance.sh`, and — crucially —
no content-equivalence guesswork to decide whether a branch is already
in. "Is this branch merged?" is a one-line ancestor query.

This replaces the older cherry-pick flow, which gave every folded
branch a NEW commit SHA. Cherry-picked branches never became
ancestors of main, so GitHub showed them as "1 commit ahead"
indefinitely and an extra `post_merge_advance.sh` force-advance step
(plus per-branch SHA bookkeeping) was needed to fake the ancestry.
That whole apparatus is gone.

The historical objection to merge — "merging a stale-based branch
rolls back main-side updates" — does not survive scrutiny: the only
files a stale branch can roll back are the shared bookkeeping files,
and every one of those is rebuilt or repaired downstream (registry
blobs + `man/` + navbar regenerated in step 5; covariate-columns.md
union-merged in step 6). New model `.R` / vignette `.Rmd` files live
at unique paths, so a 3-way merge keeps every prior branch's
additions intact. `-X theirs` only changes how *conflicting* hunks
resolve, which is incidental for exactly those regenerated /
union-merged files.

One-off transition caveat: branches that were folded in by the OLD
cherry-pick flow are still not ancestors of main, so a consolidation
pass that needs to re-examine them cannot rely on the ancestor check
alone — use a path-based content check ("does the branch add a model
`.R` at a path absent on main?") for that single transition pass.
Every branch merged by *this* (merge-based) skill is trackable by
ancestry from then on.

### Why `-X theirs` for binaries is safe

Every model-addition branch touches `data/modeldb.rda`,
`inst/modeldb.qs2`, `man/modeldb.Rd`, and (often) `_pkgdown.yml`.
These are derived artifacts: `buildModelDb()` regenerates them
deterministically from the union of all model `.R` files now on
the branch. So the merge-time choice for the binary blob doesn't
matter — step 5 overwrites it canonically.

### Why `-X theirs` for covariate-columns.md is NOT safe

This file's `**Example models:**` lines are structured per-covariate
listings where each branch *appends* its model to the existing
list. Branches don't add new sections; they edit the same line.
With `-X theirs`, only the last branch's version survives, and
every other branch's annotation gets lost. The union merger in
step 6 reconstructs this by parsing every branch's diff and
emitting a deduplicated union.

If you're operating on a different codebase that has its own
structured-markdown collation file (e.g. an `AUTHORS.md` where each
branch adds a name), pass `--union-file <path>` to
`merge_branches.sh` to point the union merger at it.

### `--dry-run` mode

`merge_branches.sh --dry-run` runs steps 1-2 (survey + confirm
scope) but stops before creating the worktree. Use this to see
which branches would be folded in before committing to the merge,
then run again with `--yes` once the operator agrees.

### Idempotence

The script aborts cleanly if the target worktree already exists.
A run that stopped -- for a hand union (exit 9) or at a failed gate -- is
finished with the `--finish` command its stop message prints, on the same
worktree, which keeps the hand edits; see step 6b. Removing the worktree deletes its hand-union report (the run that
finds the worktree says where it is), so copy the report first. To re-run
from scratch, remove the worktree first:

```bash
git -C <repo> worktree remove --force .worktrees/<branch-name>
git -C <repo> branch -D <branch-name>
```

### What to do if `devtools::check` fails

The script does NOT auto-fix check errors. If step 8 reports any
errors or new warnings (beyond the pre-existing `.git` NOTE):
1. The worktree is left in place with all merges intact.
2. The operator can re-run check, investigate, and either fix the
   issue or revert specific merges.
3. The push step (9) does NOT run if check fails — the operator
   confirms before pushing.

### When new claude/* branches appear during the merge

The pre-flight survey captures the initial set; branches pushed later are
not included in that run. Fold them into the same branch with `--fold-in`
(next section) rather than merging them by hand.

## Fold-in rounds

```bash
bash /home/bill/.claude/skills/runner-merge-claude-branches/merge_branches.sh \
    --repo /home/bill/github/nlmixr2/nlmixr2lib \
    --branch-name merge-all-claude-branches-<date> --fold-in --yes
```

A late branch forks from main, not from the consolidation, so `-X theirs`
resolves its NEWS.md hunk to main's development-version block plus its own
bullet, dropping every bullet the consolidation added, and resolves a
register line it also edited to main's line plus its own addition. A fold-in
round is a round whose base is the consolidation's tip (recorded as the
round's `--base`):

- it surveys the `--pattern` branches with commits the consolidation lacks
  (a branch merged in an earlier round and pushed to since included), and
  stops (exit 4) when one adds a model or vignette path the consolidation
  already has with other content, as a first round does against its base,
  as well as on the usual same-path collision;
- it merges them in the existing worktree, then runs every repair against
  the tip: the NEWS union rebuilds NEWS.md from the consolidation's own copy
  plus the bullets the new branches added, the register union puts back the
  entries the new merges dropped, and the dedup keeps the consolidation's
  copy of a canonical;
- the gates check the new branches' contributions (verifier, line check)
  and every line of the consolidation the round's merges lost (the revert
  check, whose base is now the consolidation's tip), then the pre-check,
  the R steps and the push run as on a first round, and the PR text counts
  the whole branch from the first round's `--base`.

It reads `--pattern`, `--union-file`, the register files and `--extra-ref`
from the round before (a given `--extra-ref` is added; another input that
conflicts exits 2), so the command needs only `--repo` and `--branch-name`.
`--exclude-ref` applies to the round it is given on: give it again. The
worktree must be clean, and the round before must have completed its repairs
and passed its revert check on the registers as they stand (exit 3): a round
that stopped at the revert check, or whose registers a commit changed after
it passed, is completed with `--finish` first, which checks again. A fold-in
on top of reverted base content would take that content as its own base. A
hand-union report the round before left stops the fold-in (exit 9) until it
is worked through: `--finish --hand-union-done` on that round records that,
or pass `--hand-union-done` to the fold-in.

The round before's records stay as they are until one of the round's merges
lands. Once one has, they are kept in the worktree's git directory as
`hand-union-report.before-<tip>.md`,
`hand-union-report.repairs.before-<tip>.md`, `merge-inputs.before-<tip>` and
`merge-stages.before-<tip>`, and the new round's start empty. How a round
that stops is completed depends on where it stopped:

- **while merging**, or while moving those records aside -- every merge
  failed (exit 4), or an interrupt or a crash: the branch is put back at its
  tip (`git reset --keep`) and the records moved so far are moved back, so
  the round before is as it was: `--finish` completes it and `--fold-in`
  runs again (with `--exclude-ref` for a branch that cannot merge). A kill
  runs nothing on its way out, so the round keeps a marker,
  `fold-in-merging` (the tip it started from), in the worktree's git
  directory until the records are moved: while it is there `--finish`
  refuses (exit 3), and the next `--fold-in` aborts any merge left half
  done, puts the branch and the records back, and folds in afresh;
- **after its merges, before its repairs completed** -- a repair that
  crashed, duplicates the dedup left, a gate that could not run, an
  interrupt: `--finish` refuses (exit 3), since it redoes no repair. Discard
  any partial output and run `--fold-in` again: it puts the branch back at
  the tip the round started from, with the round before's records, lists the
  commits it drops (they stay in the reflog), and folds in afresh;
- **after its repairs** -- a hand union (exit 9), the revert check or the
  regeneration (5), check (6), the push (7) or the vignettes (8): `--finish`
  completes it, as it does a first round.

Before it puts a stopped round back, `--fold-in` fetches the branch from
origin. If origin has commits the round's start lacks (the stopped round was
pushed, or other work was), putting the branch back would leave it behind
origin, so it refuses (exit 3) and changes nothing: consolidate afresh on a
new `--branch-name`, or reconcile the branch with origin by hand. A fetch
that fails is reported, and the copy of origin last fetched is used.

Regression tests: `tests/unit/test_merge_fold_in.py`, and the fold-in case
in `tests/unit/test_union_merge_news.py`.

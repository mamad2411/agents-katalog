---
name: seed
description: Use when the user wants to start a new novel, generate story seeds or premises, riff on a story idea, or set up a new autoauthor project directory.
model: opus
---

# Novel Seed — Start a New Novel Project

Creates a standalone novel project directory (its own private git repo —
novel content never lives in the plugin or any public repo) and writes the
chosen seed concept. This is the only autoauthor skill that runs outside an
existing project.

## Steps

1. **Location, and the form if there is one.** If the current directory
   contains `project-info.md`, an `/autoauthor:init` run already made this
   directory and the author has filled in what they know. Read the FORM
   now — that file alone — and let it answer every question below that it
   answers; do not re-ask what the file already says. That directory is
   `<dir>` for the rest of these steps; there is nowhere else to put the
   project. This is the FORM PATH, and step 3 sends you back here when a
   directory named later turns out to hold a form.

   Without a `project-info.md`, this skill runs exactly as it always has:
   ask the user where the project should live unless they already said.
   Default suggestion: `~/novels/<tag>` where `<tag>` is a short
   kebab-case slug. Never nest inside another git repo.

   `seed-data/` — the folder init leaves, so only the form path has one —
   is notes and research, read whole and once, and NOT in the paragraph
   above. Measure it first (`du -sh seed-data`) and report the total;
   above roughly 100KB, STOP and ask before a byte of it is in context,
   and if what is in there is a manuscript rather than notes,
   point the user at `/autoauthor:import` — seed would paraphrase a draft
   into a premise rather than salvage its foundation, which is the
   opposite of what they want. A size gate read after the folder is a
   size gate that has already failed, which is why the form and the
   folder are two separate reads with the measurement between them. Under
   the budget, read the folder now. That budget is a stated judgement with
   nothing yet to derive it from; revise it once someone has actually
   filled the folder.

2. **Choose the genre.** List the packs in
   `"${CLAUDE_PLUGIN_ROOT}/shared/genres/"` (excluding TEMPLATE.md) with
   their `label`, and ask the user to pick a primary. Offer an optional
   secondary and any modifiers, explaining that a secondary contributes
   additively (a second genre's material layered in, such as a romance
   subplot) and a modifier is an orthogonal axis (YA, cozy, heat level).
   If the user declines to choose, use `general`.

   **On the form path the form has already answered this.** A filled
   `**primary:**` is the choice — say it back for confirmation rather
   than asking, and the same for `**secondary:**` and `**modifiers:**`.
   A blank field is a decline and takes the default above; that is what
   the form means when it tells the author a blank lets seed decide.

   **Check every name the form gave you against the listing you just
   made, here, before step 3 creates anything.** A name that is no
   shipped pack STOPS: say which one failed and what the listing holds,
   and let the author fix the form. The resolver in step 3 catches it
   too, but only once `state.json` and the layer files exist, and the
   non-empty check at the top of step 3 then refuses the corrected
   re-run — one typo in one field would leave the author asking
   permission to overwrite a directory seed itself half-built.

   Settle this BEFORE `state.json` is written in step 3. The genre goes in
   at the moment that file is created, not after it: the template
   `state.json` ships `"genre": null`, and a null genre resolves silently
   to `general` — so a run interrupted between that write and a later
   genre step would leave a project that builds an entire book in a genre
   nobody chose, with nothing ever surfacing the mistake. It is also why
   `/autoauthor:init` writes no `state.json` of its own: that file cannot
   honestly exist before the genre does.

2b. **Choose the form.** List the forms in
   `"${CLAUDE_PLUGIN_ROOT}/shared/forms/"` with their `label` and `words`
   range, and ask how long the work is. If the user declines, use `novel`
   — the same defaulting rule and the same caveat as the genre. A form
   whose `**form:**` field is filled has answered it: confirm the name
   rather than asking, check it against this listing the way step 2
   checks the genre names, and treat a blank field as the decline.

   The form decides total length, which planning layers get built, where
   the foundation gate sits, and how the genre's own criteria are read. It
   is not a preference to revisit later: a short story and a novel are
   different works, not the same work at two sizes.

   Not every genre supports every length. A pack needs a length-scoped
   section to be judged below novel length, and one without it is REFUSED
   rather than judged on criteria written for eighty thousand words. Settle
   the form here, alongside the genre, so the pair is checked once at init
   rather than discovered at the first foundation run — the resolver in
   step 3 will say plainly if they cannot go together.

2c. **Choose the structure.** Ask whether this is one work or several —
   unless the form's `**structure:**` field says which, in which case
   confirm that and do not ask. The field ships pre-filled with
   `standalone`, so it is blank only if the author deleted the word, and
   a blank is the decline that takes the default below.

   - **standalone** — one work. The default, and what to use if the user
     has not said otherwise.
   - **collection** — several complete works bound as one book, checked
     for variety and independence before export.
   - **series** — several books sharing continuity, each advancing a whole
     and closing itself.

   Settle it here for the same reason as genre and form: it decides the
   directory layout, and it cannot be changed later without moving every
   file. If the user describes "a trilogy", "a series of stories", or "a
   collection", ask rather than assuming — those words are used loosely
   and the two containers check opposite things.

   For a CONTAINER, the genre and form chosen above belong to the
   container and are inherited by every work; a work may not override
   them, because they are what make N works one book.

3. **Initialize the project:**
   - **The form first, whatever route brought you here.** If `<dir>`
     holds a `project-info.md` and you did not arrive by step 1's form
     path, go back to step 1 now and take that path whole — the form, the
     size measurement, then `seed-data/` — and settle steps 2, 2b and 2c
     again against what it says. Step 1 only sees the
     directory seed was started in, and the user is invited to name a
     different one — so an author who ran init, spent a day filling the
     form in, then started seed from elsewhere and typed the path when
     asked would otherwise be interviewed from scratch and have the
     answers written over their own. Every word in that file is theirs;
     none of it is discarded because seed was launched from the wrong
     directory.
   - Safety checks next: if `<dir>` already exists and is non-empty, STOP
     and ask the user before touching it (a retry may have partial content
     worth keeping — never overwrite silently). ONE exemption: a directory
     whose TOP LEVEL holds nothing beyond `project-info.md`, `seed-data/`
     and `.git/` is an `/autoauthor:init` scaffold and is the expected
     case — proceed. Nothing beyond, not exactly those three: init treats
     a git failure as a warning and still exits 0, so a scaffold with no
     `.git/` is a directory init itself produced and refusing it would
     stop seed over someone's signing config. What is inside `seed-data/`
     is not counted either: the author's notes belong in there, beside the
     `.gitkeep` init left. Any top-level entry that is none of those three
     still stops. Then verify the parent is
     not inside a git repo: `git -C <parent> rev-parse --is-inside-work-tree`
     must FAIL; if it succeeds, pick a different location.
   - **If anything below stops this step, delete what this step wrote and
     nothing else before you stop.** Never `project-info.md`, never
     `seed-data/` — this step did not create those and they are the
     author's. The reason is seed's own non-empty check a few lines up: a
     half-built directory is one it refuses on the corrected re-run, so
     without the cleanup a rejected genre/form pair costs the author
     permission to try again. This holds for both layouts below.
   - `mkdir -p <dir> && cd <dir> && git init`

   **For a container** (`collection` or `series`), the layout differs and
   the rest of this step is replaced by:

   - `mkdir -p bible works eval_logs edit_logs`
   - Copy the shared layers into `bible/`: `voice.md`, `world.md`,
     `characters.md`, `canon.md` from
     `${CLAUDE_PLUGIN_ROOT}/shared/templates/`.
   - Write the file that says what this container IS, which the
     cross-work pass reads and which nothing else can supply:
     - a COLLECTION needs `bible/binding.md` — what makes these works one
       book rather than a folder, and the slate: one line per planned
       work naming the facet of the binding it takes. "A shared setting"
       is the commonest thin answer; push for the question or the premise
       the works are all circling.
     - a SERIES needs `bible/arc.md` — one line per planned volume saying
       what that volume owes the whole — and `bible/canon.md` as the
       continuity spine.
     Write it now even if it is a guess. The resolver refuses a container
     without its file, and for a good reason: the pass can ask whether
     the binding is delivered or whether anything progressed, and it can
     ask neither of a file that does not exist.
   - Write `state.json` at the container: the template's keys plus
     `"structure"`, the genre and form from steps 2 and 2b, and
     `"works": []`. That array is the running order, and export reads it.
   - Create `results.tsv` with the same tab-separated header a standalone
     project gets. **The container's is for CROSS-WORK rows only** — the
     collection or series pass, and export. Per-work iterations belong to
     the work, so that a user who `cd`s into one and runs `/autoauthor:status`
     finds its history where every other project keeps it, and so that the
     cross-work record is not fifteen foundation iterations deep in rows
     it did not write.
   - Install the ignore file the same way a standalone project does.
   - Create the first work. A work is an ordinary project and gets the
     same scaffolding as a standalone one, minus the things the container
     owns: `mkdir -p works/01-<slug>/{chapters,eval_logs,edit_logs,briefs}`,
     its own `results.tsv` with the same header, `state.json` and the
     form's layer files (as above — only those) from `shared/templates/`.
     Add
     `"01-<slug>"` to the container's `works`. Set the work's
     `state.json` phase to `foundation` and leave its genre, form and
     modifiers NULL — it inherits them, and setting them is an error the
     resolver reports.
   - Then run the resolver from the container to confirm it validates,
     and stop. The user runs foundation from inside a work, not here.

   **For a standalone project**, continue:

   - Copy `state.json` and `gitignore` from
     `"${CLAUDE_PLUGIN_ROOT}/shared/templates/"`, plus **only the layer
     files the form calls for**. The form's `layers` list names them and
     `LAYER_FILES` in `form_pack.py` maps each to its file: `voice` →
     voice.md, `world` → world.md, `characters` → characters.md,
     `mystery` → MYSTERY.md, `outline` and `foreshadowing` → outline.md,
     `canon` → canon.md.

     Do NOT copy the rest. A short story's form builds three layers, and
     handing it an empty `world.md` and an empty `canon.md` gives it two
     documents its form deliberately does not build — the foundation
     rubric tells its judge not to go looking for a file it was not
     named, so the extras are clutter at best and a judge marking down a
     five-line template at worst.
   - **Write the genre and form into `state.json` immediately after the
     copy** — set `genre`, `genre_secondary`, and `genre_modifiers` from
     step 2 and `form` from step 2b, replacing the template's nulls. Then resolve the stack from the
     project directory and KEEP the JSON it prints; the rest of this step
     and step 4 both read it:

     ```bash
     python3 "${CLAUDE_PLUGIN_ROOT}/shared/scripts/resolve_genre.py"
     ```

     It prints the merged config on stdout: `packs` (each with a `name`,
     `role`, and the absolute `path` of the pack file to read),
     `display_label`, `shape`, `artifacts`, and the rest. If it exits
     non-zero, fix the selection before continuing — a conflicting stack
     (for example `ya` with `erotica`) is rejected here rather than
     producing an incoherent book, and so is a genre that has no
     length-scoped section for the chosen form. Step 2's name check
     cannot see either of those; only the resolver can, which is why this
     is the one refusal that arrives with files already on disk — clean
     up as the top of this step requires before you stop.
   - Render the pack-driven parts of the copied templates, reading the
     pack files at the `packs[].path` values just printed: write
     `world.md`'s section headings from the resolved pack's
     `## World Sections`, and `canon.md`'s category headings and one example
     entry each from its `## Canon Categories`. Create any file named in the
     resolved `artifacts` list from the pack's `## Artifacts` template.
   - Install the ignore file: `mv <dir>/gitignore <dir>/.gitignore` —
     eval_logs/, edit_logs/, and briefs/ MUST be gitignored; the
     drafting and revision skills depend on them surviving
     `git reset --hard` discards and staying out of commits.
   - `mkdir chapters eval_logs edit_logs briefs`
   - Create `results.tsv` containing exactly this header line (the
     separators are REAL tab characters — use printf, not echo, so
     they can't silently become spaces):
     `printf 'timestamp\tphase\tscore\twords\tkeep_discard\tdescription\n' > results.tsv`
   - Use the absolute `<dir>` path in every command rather than relying on
     the shell's current directory persisting.

4. **Generate concepts.** Read `references/seed-prompts.md` (in this
   skill's directory) and every pack path the resolver reported in step 3
   (the `path` of each entry in `packs`). **The session rule**, which
   governs wherever no filled premise answers the question: if the user
   supplied an idea, use the riff prompt (5 variations); otherwise the
   generate prompt (10 concepts).

   **Which path runs, when there is a `project-info.md`.** Three
   questions, in this order — and the first one is not about completeness.

   First: did the author write ANY premise content, in any field of the
   form's `## Premise` section? If that section is wholly blank the form
   has answered nothing here, and the session rule above governs
   unchanged. A blank section discards nothing because there is nothing in
   it to discard — but an idea spoken in chat is the author's words too,
   and "riff on this: a lighthouse keeper who…" met with ten concepts of
   your own is the same discard through a different door. A form does not
   silence the session; it answers the questions it answers and no more.

   If they wrote anything at all, their words stay in play. Second, then:
   did the user ALSO give you an idea in this session, and is it a
   different story from the one in the form? If so, STOP and ask which
   governs, putting both in front of them in a line each. Do not merge
   them, and do not let either win by default — not the form for being
   written down, not the session for arriving last. A filled form is a
   considered act, made in an editor with time to think. An idea spoken in
   chat is a fresh one, made now. Nothing in the input tells you whether
   the second amends the first or replaces it, and the two readings build
   different books. When two sets of the author's own words disagree, the
   author is the one who resolves it. Their answer — the form, the session
   idea, or the merge they describe — is the premise the rest of this step
   works from, and the third question is asked of that.

   Third, once that is settled: the resolved pack's own required fields
   decide which of the remaining two paths runs — the `## Seed Prompt`
   section names those fields, and they decide what "covered" means here,
   not the form's neutral labels:

   - not every required field covered → **riff** five variations on what
     the author wrote, and name the required fields they left for you.
     Naming them is how the author learns what a second pass should add:
     the form is filled in before a genre is chosen, so it cannot ask for
     a field only the pack knows about. Expect this path most of the time.
   - every required field covered → use the premise **as written**; skip
     generation and go to step 6

   **A field the author filled is never discarded.** The form promises
   them a riff on what they wrote, and this is where that promise is kept.
   TITLE and HOOK are the two fields an author fills first and no pack
   requires either, so a rule keyed on required fields alone would answer
   the likeliest form of all with ten concepts of your own — the author
   writes something and the machine throws it away, having said it would
   not. Do not re-tighten this to "how complete does the premise look".

   Say which path you took and why before you take it. On the as-written
   path, tell the author what you did NOT do — nobody chose from ten
   concepts, so the premise has had no comparison drawn against it.

   The form is an input, not an authority. Its numbers get the same
   arithmetic check foundation's step 3b runs on a seed: one seed
   conflated a per-year allowance with an annual window in a way that
   could not both be true, and it took two scored iterations to surface.

   On the generate and riff paths, write the concepts yourself, in-session,
   following every constraint in the prompt — the diversity requirements
   and the DO-NOT list are hard rules.

5. **Selection.** Present the concepts compactly (TITLE + HOOK + the pack's
   first required field that the neutral scaffold does not already define)
   and ask the user to pick, remix, or reroll. If the user asked for a fully
   autonomous run, pick the concept with the strongest interlock between the
   pack's central constraint and the central tension, and say which you
   picked and why.

6. **Write `seed.txt`** with the full premise — the concept chosen in step
   5 on the generate and riff paths, the author's own words on the
   as-written path, which reaches this step without a step 5 and so has no
   "chosen concept" to speak of. Verify it contains a
   world-differentiator (the WORLD field), a central tension (TENSION), a
   concrete sensory anchor in the WORLD field, and every field the pack's
   `## Seed Prompt` marks required — and strengthen any that are missing
   before saving.

   **Where a `seed-data/` folder existed, this file is what survives it.**
   No later phase opens that folder; foundation reads `seed.txt`, so it is
   the only channel the author's notes have. What they gathered must
   inform the premise, and their concrete specifics must arrive here
   intact — a name they chose, a place they researched, a piece of
   real-world material, the sensory detail that made a setting theirs.
   Those are exactly what a paraphrase flattens into generality first, and
   flattening them turns a folder the author spent a week filling into a
   premise they would have got without it. Inform, do not transcribe: the
   notes feed the premise, they are not pasted into it.

   The as-written path is also the one that can arrive here with no title.
   No pack requires TITLE and the form does not either, so an author who
   filled in everything a pack asked for and left the title blank has
   nothing for step 7 to write. Propose a title drawn from the premise and
   get their yes before going on — or, on a fully autonomous run, pick one
   and say which. Nothing later in the pipeline ever fills this in.

7. **Record the title.** Write it into `state.json`'s `title` field — the
   container's for a container, the work's for a work. It is the one piece
   of the book's identity that never appears in the prose, and export
   reads it from here rather than parsing a markdown heading.

8. **Commit:** `git add -A && git commit -m "seed: <title>"`

9. **Report:** project path, title/hook, and next step:
   `cd <dir>` then `/autoauthor:foundation`.

---
name: ioda
description: Investigate → propose → gate → execute → verify. A guided IOODA workflow (Intent, Observe, Orient, Decide, Act) drawn from OODA, Socratic inquiry, QRSPI, and Polya's How to Solve It. One command for the whole flow.
argument-hint: '<ticket-key-or-feature-name-or-blank>'
---

User's request: $ARGUMENTS

# ioda — guided IOODA workflow

Your mantra on every phase transition and every sub-agent dispatch:

> **Investigate first. Tell me your findings. Then proceed. Look back.**

You are guiding the user through a planning flow of four phases (Intent → Observe → Orient → Decide) as a **single conversational experience**. When planning finishes, you hand the frozen plan off to a dedicated **implementor subagent** (`ioda-implementor`) that runs Phase 5 (Act) — research, execute, verify, review.

The split is deliberate. Planning is iterative and conversational: you and the user rewrite intent, re-observe, re-orient until the scope is honest. Execution is disciplined: the implementor treats `1-intent.md` and `4-decision.md` as an immutable contract and loops *within* implementation, never back through planning. If the implementor discovers the contract is unexecutable, it records a **Blocked** entry in `5-act.md` and stops; the user re-runs `/ioda` to reconcile.

## Opening banner

Output first:

```
════════════════════════════════════════
ioda · Investigate first. Tell me your findings. Then proceed. Look back.
════════════════════════════════════════
```

## Step 0: Load configuration

Run:

```bash
cat "$HOME/.ioda/config.json" 2>/dev/null || echo "NOT_CONFIGURED"
```

If `NOT_CONFIGURED`, say:

> ioda is not configured yet. Run `/ioda-init` first, then retry.

Exit.

If configured, parse `base_dir`, `ticket_cli.fetch`, `verification_commands`, `code_review_agent` from the config. Check for a per-project override at `$(git rev-parse --show-toplevel)/.ioda/config.json` and merge (local overrides global).

## Step 1: Resolve the feature

The argument may be:

- **Blank** — ask the user what they want to work on (ticket key, a short phrase, or a paste of intent)
- **A ticket key** (e.g. `TN-3626`, `LIN-42`, `#123`) — use as-is
- **A descriptive phrase** (e.g. `fix-translation-race`) — convert to kebab-case

### Feature-name resolution

Feature folder names are **human-readable**. See `${CLAUDE_PLUGIN_ROOT}/references/feature-discovery.md` for the full rules; in short:

- **Ticket key argument** → `<KEY> <short-title>` where the short title summarizes the ticket title in ≤ 4 words and ≤ 25 characters (e.g. `TN-3744 Translate TC settings`). The title is derived once the ticket is fetched — resolve it before creating the folder.
- **Descriptive phrase argument** → use the phrase directly as the short title (≤ 4 words, ≤ 25 chars), no KEY prefix.
- **Blank argument** → ask the user for a short name, then apply the same rules.

### Check for existing feature folder

Resolve the base directory:

```bash
BASE_DIR=$(bash "${CLAUDE_PLUGIN_ROOT}/scripts/resolve-basedir.sh")
```

Search for an existing feature folder in two places:

1. `$BASE_DIR/<KEY> *` or `$BASE_DIR/<feature-name>*` — top-level (standalone or macro). Match by ticket key prefix when a key is provided, otherwise by the short title.
2. `$BASE_DIR/*/<KEY> *` — one level deep (nested under a macro). Sub-tasks live **directly inside** the macro folder; there is no `micro/` layer.

If found → **resume**: detect the current phase by checking which of `1-intent.md` … `4-decision.md` exist, and whether `5-act.md` exists or contains a Blocked entry. The three resume shapes:

- **In-flight planning** (`4-decision.md` does not yet exist) — announce and resume at the phase where the last file lands:

  ```
  Resuming <feature-name> at <phase>. Last file: <latest-file>.md
  ```

- **Plan-complete, no execution yet** (`4-decision.md` exists, `5-act.md` does not) — this is the **third entry path**: the main flow's job is done, and the next action is launching the implementor. Announce:

  ```
  Plan complete for <feature-name>. `4-decision.md` is ready.
  ```

  Then ask:

  > Launch the `ioda-implementor` subagent to research, execute, and verify — or reopen planning?

  On launch → spawn the implementor (see Step 10 below). On reopen → treat as in-flight planning at Decide, with an offer to loop back further if the user signals drift.

- **Execution in progress or blocked** (`5-act.md` exists) — read it. If it contains a **Blocked** entry, announce:

  ```
  Implementor is blocked on <feature-name>. Reason: <first line of Blocked entry>.
  ```

  Then offer a loop-back to the affected planning phase per `references/loop-back-detection.md`. If `5-act.md` exists without a Blocked entry and has no `## Verification` section yet, the implementor is mid-execution — announce and ask whether to re-launch the implementor (it will resume from its own research) or leave it alone.

If not found → **start fresh** at Intent.

## Step 2: Fetch ticket (if applicable)

If the argument looks like a ticket key AND `ticket_cli.fetch` is configured:

Read `${CLAUDE_PLUGIN_ROOT}/references/ticket-cli.md` and follow the fetch-with-fallback protocol.

The returned ticket text becomes context for Intent. From it, Claude extracts (without asking the user):

- Title
- Description / motivation
- Acceptance criteria if present
- **Parent or epic link** — used later for macro/micro auto-detection

## Step 3: Auto-detect macro (Epic) vs micro (story) — before creating the folder

Read `${CLAUDE_PLUGIN_ROOT}/references/macro-micro.md` and apply the auto-detection rules. IODA's **macro** maps to a ticket-tracker Epic / Initiative (has children); **micro** maps to a story / task (single deliverable). When announcing the classification to the user, always name both — e.g. *"This is a micro (story-level) feature under parent macro (Epic-level) `TN-3744 Translate TC settings`."*

Decide whether:

- This is a standalone or macro (Epic-level) feature → folder under `$BASE_DIR/<feature-name>/`
- This is a micro (story-level) sub-task nested under a known parent → folder under `$BASE_DIR/<parent-feature-name>/<feature-name>/` (no `micro/` layer)
- The parent is known but not locally tracked → ask the user once (soft question) whether to track the parent first or proceed standalone

## Step 4: Derive the short title (ticket path only)

**Before** creating the folder, derive the `<short-title>` from the ticket title per `${CLAUDE_PLUGIN_ROOT}/references/feature-discovery.md` → **Short-title rules**:

- Plain language, spaces allowed
- **≤ 4 words and ≤ 25 characters**
- Preserve acronyms and proper nouns (`TL`, `TC`, `API`)
- Strip punctuation that's awkward in a folder name (`:`, `/`, quotes)
- No trailing period

The final feature name is `<KEY> <short-title>` (e.g. `TN-3744 Translate TC settings`), **not** just `<KEY>`. The short-title is mandatory on the ticket path — a folder named only `TN-1928` fails the convention and is treated as a bug, not an accepted shortcut.

If the fetched ticket title produces no sensible 4-word summary (rare — happens for titles that are themselves just a key reference or a single-word placeholder), print a one-line proposal to the user:

> Ticket title is `<raw title>`. I'll name the folder `<KEY> <my-proposed-short-title>` — reply with a different short title if you'd prefer one.

Wait only on an explicit alternative; silence proceeds with the proposal. This does not gate the flow — it's a one-line check, not an approval loop.

On the descriptive-phrase path and the blank path, the short title is just the phrase (no `<KEY>` prefix). The same 4-word / 25-char rules apply.

## Step 5: Create the feature folder

```bash
FEATURE_PATH=$(bash "${CLAUDE_PLUGIN_ROOT}/scripts/ensure-feature.sh" "<KEY> <short-title>" [--parent "<parent-feature-name>"])
```

Before calling the script, verify the feature name matches the expected shape:

- Ticket path: starts with `<KEY> ` followed by a short title. `TN-1928` alone is **not** a valid name on this path.
- Descriptive / blank paths: short title only, no `<KEY>` prefix.

From here on, all artifacts live under `$FEATURE_PATH/`.

## Step 6: Run the planning phases

Follow the phase instructions in order. The main flow runs **planning only** — phases 1 through 4. Phase 5 (Act) runs in a dedicated subagent, spawned at Step 9 below.

Each phase reference lives under `${CLAUDE_PLUGIN_ROOT}/references/phases/`:

1. `phases/1-intent.md` — write `1-intent.md`
2. `phases/2-observe.md` — write `2-observations.md` via sub-agent
3. `phases/3-orient.md` — write `3-orientation.md` (main session, Socratic)
4. `phases/4-decide.md` — write `4-decision.md`; auto-promote to macro if decision breaks work into sub-tasks

Phase 5 lives in `phases/5-act.md` as a pointer doc; the real protocol is in `${CLAUDE_PLUGIN_ROOT}/agents/ioda-implementor.md`.

### Phase banners

Every phase entry announcement uses a banner that visually separates the step from the surrounding conversation. The step name is emphasized with a markdown `##` header (renders larger than prose) and the brief lives inside the same dividers as the title — one enclosed block per phase. The five lines (top divider, heading, blank, brief, bottom divider):

════════════════════════════════════════
## Step #<N> — <Phase Name>

<one-paragraph brief: what this phase is, what the user should expect, and whether the transition is gated or automatic>
════════════════════════════════════════

Then proceed with the phase's actual work. This is a **presentation convention, not an extra gate** — phases that auto-transition still print the banner on entry. Emit as **plain rendered markdown** — directly in your response, **not** wrapped in a code fence. The `##` must render as an H2; if it shows as two literal hashes, the banner was wrapped in a fence.

**Who prints the banner: the phase that is entering, always.**

Each phase file (`1-intent.md`, `2-observe.md`, `3-orient.md`, `4-decide.md`) has an **entry block** at its top that prints unconditionally on every entry to that phase. The entry block has two parts: an optional **move line** (only on automatic entry from a prior phase — one line naming the artifact the prior phase just wrote) and the phase banner itself (always). This rule replaces an earlier release's script-based hand-off, which attempted to have the *exiting* phase print the next phase's banner via a helper script — the agent routinely skipped the script call, and the next phase trusted the banner was printed, producing silent transitions with no banner at all. The current rule moves the responsibility onto the receiving phase, where it is always executed.

The exit side of every automatic transition (Intent's Step 5, Observe's Step 6, Orient's Step 7) is silent: write the artifact, then proceed directly to the next phase's entry block. Do not print a move line, a banner, a summary, or a proceed prompt on the exit side — the entire announcement is the next phase's job.

**Anti-pattern — do not produce any of these shapes** (all reproduced from real dogfood runs):

- **Banner collapsed to a bulleted line:** `● Phase 1 — Intent` followed by loose prose. Wrong prefix, wrong heading level, no brief, no dividers.
- **Banner wrapped in a code fence.** The `##` and bolds render as literal characters. If the user sees `## Step #1 — Intent` as literal text, the banner was wrapped in ``` — don't.
- **No banner at all.** A phase's content appears without an announcement, because the exiting phase skipped its hand-off and the entering phase trusted that the hand-off was done. The unconditional entry-block rule on the entering phase fixes this.

Match the positive skeleton verbatim.

### User-facing questions (Orient's multi-option design questions)

This section defines the format for **Orient's unified `## Open questions` block** — where the skill presents a set of related design forks with competing options, one bold question per fork. For any **single question** that drives a next-action decision (Intent accept/add-more, branch prompt at Decide → Act, paste-in fallback, scope-asymmetry soft-gate, resume/blocked prompts, etc.), use the simpler **User-facing prompts (non-Orient)** convention below instead — that convention is one question on its own bold line, not this multi-option skeleton.

**One block, one numbering sequence.** Starting in v0.11.1, the Orient render is a single `## Open questions` section that hosts both surface confirmations (`**1)** Write side`, `**2)** Read side`) and the design-fork questions (`**3)**` onwards) under one continuous numbering sequence. Do not split them into separate `## Surfaces to confirm` and `## Open design questions` headings — that was the v0.11.0 shape Luis's dogfood feedback retired (*"I want to see all as questions regardless of their nature"*). See `references/phases/3-orient.md` → Step 4 for the full unified skeleton.

**Header summary + `accept` shortcut.** Starting in v0.12.0, the `## Open questions` heading is immediately followed by a one-line summary that tells the user how many questions they have and gives them a single-keystroke commit path: `Reply `accept` to take all <N> leanings as-is, or push back on any.` where `<N>` is the total number of questions (surfaces + design). The user can still answer individually; `accept` is for the common case where the agent's leanings land.

**Givens live in `3-orientation.md`, not on-screen.** Starting in v0.12.0, there is no `## Decided` chat block. Things Observe's evidence already closed — "REST returns unordered, so it's a client-side sort," "the Autocomplete remounts on every append, so toggle state lives in the parent" — go into `3-orientation.md`'s `## Givens` section (written on hand-off). If a Given directly constrains a specific open question, it surfaces inline as a `> *Given: <one-line>.*` preamble at the top of that question's blockquote. Givens that don't narrow a specific question's option space stay silent in chat and live only in the artifact. The phase-boundary reasoning: Orient shapes the design space (open forks), commitments are Decide's job, and things-already-closed-by-evidence are inputs to the design space, not reviews the user needs to walk. Luis's feedback that drove the retirement: *"Orient is trying to do too many things at one like confirm surfaces, decide and open design questions … do we even need to tell the user what was decided? I think that is also in the decision of the OODA right?"*

Whenever Orient renders the open-questions block, render it in a format optimized for **skimming and correction** — the user should be able to scan the italic leaning lines, notice the bold option label on each, and push back on the ones that feel wrong.

This convention is **renderer-aware**: naive markdown ordered lists (`1.`) lose visible option-indent in terminal renderers like Ghostty, and they force `1.` over the preferred `1)`. The format below works around both constraints by using plain bolded `**1)**` lines plus blockquoted option groups (blockquotes preserve visible left-margin indent and keep inline formatting intact).

Exact shape:

```
## Open questions

Reply `accept` to take all <N> leanings as-is, or push back on any.

**1) <Short question title>** — <one-sentence context explaining what's at stake and why this is a fork>.

> a) <Option A label>
> b) <Option B label>
> c) <Option C label, optional>
>
> → *I assumed **option a)** — <one-line justification, with a contrastive note when useful>.*

**2) <…>** — <…>.

> *Given: <one-line constraint that directly narrows this question's option space — optional>.*
>
> a) …
> b) …
>
> → *I assumed **option b)** — …*
```

Rules:

- **Not a markdown ordered list.** Questions are plain paragraphs prefixed with `**1)**`, `**2)**`, … so the renderer keeps the close-paren style and doesn't collapse indentation.
- **Question title in bold**, followed by an em-dash and a one-sentence context on the same line.
- **Options live inside a blockquote** (`>` prefix). Blockquotes render with a visible left bar in terminal markdown renderers, giving a clear indent without fighting the list engine. Letters use close-paren style: `a)`, `b)`, `c)` — not `(a)`, not `A.`.
- **Options are bare labels.** Starting in v0.12.0, chat-side option lines are concise labels — optionally with a short implication phrase when the label alone is unclear — but Pros/Cons sub-lines are **removed from chat rendering**. Trade-off detail lives in `3-orientation.md`'s expanded Design Questions section (options considered + one-line trade-off each). The italic leaning arrow carries the decision-making trade-off in one line, optionally contrastive (*"…; (b) is cleaner but introduces a pattern we don't have elsewhere"*). Rationale: three design questions × three options × two Pros/Cons sub-lines crowds the chat render past the skim threshold — Luis's v0.11.0/v0.11.1 dogfood feedback flagged it twice.
- **Optional `> *Given: …*` preamble** at the top of a question's blockquote when a Step-2b Given directly constrains that question (e.g. *"toggle state lives in `CardFileUploadInner` (Autocomplete remounts on append)"* narrowing a persistence-storage fork). One italic line, stating the constraint, wrapped in blockquote so it stays attached to the question. Use only when the Given actually narrows the question's option space — not as general framing.
- **Blank quote line** (`>` on its own) separates the options (and any preamble) from the assumption arrow, so the arrow reads as a conclusion rather than another option.
- **Arrow line** is italicized with bold on the chosen option label only: `> → *I assumed **option a)** — <reason>.*` Italic communicates *this is my lean / opinion, push back if wrong*; the bold option label makes "which one I picked" pop. Fully-bold arrow lines (the v0.7.0–v0.9.4 shape) read as too heavy for an opinion — the current convention is italic wrapper + bold option label.
- **One leaning arrow per question**, immediately beneath that question's options. A single aggregate *"My read: Option A is obviously correct…"* line at the end of the whole section is **banned** — every question gets its own `> → *I assumed …*` line.
- **Blank line between questions.** Density kills discussion.
- If a question is genuinely binary with no meaningful third path, use only `a)` and `b)`. Never pad with a straw-man.
- If a question only has one real answer (Observe already resolved the alternatives), **don't ask it** — capture it as a Given in Step 2b instead.

**Anti-pattern — do not produce either of these shapes** (both have been observed in real dogfood runs):

```
Design questions

Q1 · <title>

- A. <option> — …
- B. <option> — …

Leaning A.
```

Or:

```
Design Questions

Q1 — <title>

- Option A — <one-liner>
  - Pros: <line>
  - Cons: <line>
- Option B — <one-liner>
  - Pros: <line>
  - Cons: <line>

Q2 — <title>

- Option A — …
- Option B — …

My read: **Option A** is obviously correct given the ticket language — calling it out because the Observe phase flagged it.
```

Everything above is wrong: section heading dropped (`Design questions` / `Design Questions` instead of `## Open questions`), `Q1 ·` / `Q1 —` instead of `**1)**`, dashed flat list instead of blockquoted options, `A.` / `Option A` instead of `a)`, Pros/Cons present at all (retired from chat in v0.12.0 — trade-offs live in `3-orientation.md`'s Design Questions section), and a single `My read:` governing both questions instead of a per-question italic `> → *I assumed …*` line inside each blockquote. The blockquote is what produces the visible left bar the user scans to find leanings — dropping it flattens the output into an unreadable wall. The skeleton is **not** a suggestion; fold any load-bearing trade-off into the italic leaning arrow's one-line contrastive tail rather than re-introducing Pros/Cons sub-lines.

This convention applies to **user-facing output only**. The written artifact (`3-orientation.md`) uses a different shape and carries more content: Proposed Approach + Givens (terse bolded rules with file:line evidence) + Design Questions (each with options considered, one-line trade-off per option, decided answer, and rationale) + Risks & Unknowns + References. See `references/phases/3-orient.md` → Step 6. The artifact is the reference the user opens post-commit when they want to see trade-offs they may have glossed over in chat; don't bloat the chat with the same content.

### User-facing prompts (non-Orient)

Any time the skill asks the user a **single question** that drives the next action — Intent accept/add-more, the branch prompt at Decide → Act, the paste-in fallback, scope-asymmetry soft-gates, resume/blocked prompts — render it in this shape:

```
<explanatory context, as a short paragraph or a few lines>

**<Question on its own bold line>**

<optional reply-options hint>
```

Rules:

- **Context goes above, never after.** The user should read the context first, then encounter the question. A question buried at the end of an explanation paragraph is harder to act on.
- **Blank line** between context and question.
- **Question is a single bold line alone on its line.** Not wrapped onto multiple lines. Not fused into a paragraph. Not inside a blockquote.
- **Blank line** between question and optional reply-options hint.
- **Reply-options hint is brief**, one line: `Reply \`accept\` or add more.` / `Reply \`continue\`, \`new-branch <name>\`, \`worktree\`, or \`pause\`.` / `Paste the ticket body, or reply \`no ticket\`.` No lengthy instructions about what each option does — the bold question carries the ask.

Example — Intent accept/add-more:

```
I've restated the intent. Open questions from the ticket are captured silently in the artifact; Observe and Orient will resolve them.

**Does this capture the intent, or is there more to add — desired behaviours, non-goals, or boundaries?**

Reply `accept` or add more.
```

Example — Decide → Act branch prompt:

```
Planning complete. Decision written to <path>.

**You're on branch `<current-branch>` — continue here, or switch before I start?**

Reply `continue`, `new-branch <name>`, `worktree`, or `pause` (to review the plan and come back later).
```

**Anti-pattern — do not produce this shape:**

```
I've restated the intent above. This captures what the ticket asked for, including the scope boundary around only the document-linking flow. Does this look right, or is there anything to add?
```

Wrong on two counts: the question is fused into the end of an explanation paragraph (harder to act on), and it's not bold (doesn't stand out for skimming). Context + blank line + bold question on its own line + blank line + optional hint — always that shape.

The distinction from Orient's convention: this shape is for **one question** with a short reply hint; Orient's convention is for **multiple related design forks with competing options** where each fork needs an italic leaning and trade-off surfacing. Orient's blockquoted-options block is the one exception to this convention.

### Artifact cross-linking

Every IOODA artifact ends with a **`## References`** section that lists its sibling artifacts in the feature folder as **Obsidian wikilinks** (`[[<basename-without-extension>]]`). The goal is twofold: when the feature path sits inside an Obsidian vault, the folder renders as a connected sub-graph in the graph view instead of six disconnected nodes; and for any markdown-aware reader (GitHub preview, IDE preview, Obsidian), the links are clickable navigation between phases.

Per-artifact skeleton — place at the end of the body, after every other section:

```markdown
## References

- Previous: [[<prev-phase-basename>]]
- Next: [[<next-phase-basename>]]
- Loop log: [[loop-log]]
```

Concrete sibling mapping (no extension, no path prefix):

- `1-intent.md` → `[[2-observations]]`, `[[loop-log]]` (no previous; Intent is first)
- `2-observations.md` → `[[1-intent]]`, `[[3-orientation]]`, `[[loop-log]]`
- `3-orientation.md` → `[[2-observations]]`, `[[4-decision]]`, `[[loop-log]]`
- `4-decision.md` → `[[3-orientation]]`, `[[5-act]]`, `[[loop-log]]`
- `5-act.md` → `[[4-decision]]`, `[[implementor-research]]`, `[[loop-log]]`
- `implementor-research.md` → `[[4-decision]]`, `[[5-act]]`

**Conventions:**

- **Wikilinks, not path links.** Use `[[3-orientation]]`, not `[3-orientation](3-orientation.md)`. Obsidian treats both as graph edges, but the wikilink form is the convention Luis's vault uses elsewhere and it survives file-rename.
- **Bare basename, no extension, no path.** `[[3-orientation]]`, not `[[3-orientation.md]]`, not `[[./3-orientation]]`.
- **Role label before the link** (`Previous:`, `Next:`, `Loop log:`, etc.). Reads as a navigation bar; also makes the graph's hover-text meaningful if Obsidian's plugins surface the label.
- **Parent macro goes here too** when the feature is a sub-task. Add `- Parent: [[<parent-feature-folder-name>/1-intent]]` (or whichever macro artifact is most relevant). Obsidian resolves the relative path across folders.
- **Living artifact still applies.** On rename, rewrite wikilinks to the new basename — no "previously `[[old-name]]`" annotations. The loop-log records that a rename happened.
- **Don't duplicate inline references.** Links to `file:line` inside source code (e.g. `documents-service.ts:769`) stay in their original body section (Findings, Givens, Design Questions). `## References` is only for sibling-artifact links plus parent-macro pointer.

An artifact that doesn't end with `## References` is treated as a missed convention, same class as a missing phase banner.

### Phase transitions

Not every phase boundary waits for user input. The rule:

- **Intent → Observe**: **automatic** on intent confirmation. Write the file and enter Observe without a review gate.
- **Observe → Orient**: **automatic** when `2-observations.md` is complete (first pass + deep pass + gap closure).
- **Orient → Decide**: **automatic** once the user has answered Orient's design questions (or confirmed the defaults). Orient remains Socratic during the question loop — auto-advance happens *after* the user has committed to the options, not in place of that commitment.
- **Decide → Act (implementor)**: **gated** and **hand-off**. Real code changes start here, and they happen in a separate subagent. Confirm with the user, then spawn the `ioda-implementor` (see Step 9).
- **Implementor → completion**: handled by the implementor's own close-out (verification + code review). The main flow doesn't run this.

The planning phases (Intent, Observe, Orient) chain together without intermediate review gates so the user experiences a single conversation, not a series of handshakes. Pushback at any point still loops back per `references/loop-back-detection.md` — auto-transitions don't mean "decision locked," they mean "don't wait for a proceed signal to move forward."

**Gated transitions (Decide → Act only).** The hand-off is described in **Step 9** below and uses the **User-facing prompts (non-Orient)** convention — a branch-first bold question with reply-options hint, followed by a short explanation of what Act does. This is the only place the user is asked to commit before the flow continues.

**Automatic transitions (Intent → Observe, Observe → Orient, Orient → Decide).** The receiving phase announces itself. The exiting phase hands off silently:

- **Exit side** (Intent's Step 5, Observe's Step 6, Orient's Step 7): write the artifact, then proceed directly to the next phase's entry block. Emit **nothing** between the write and the next phase's entry block — no move line, no banner, no summary, no proceed prompt.
- **Entry side** (the next phase file's Step 1 / Entry block): emit the entry block as the first output. The entry block has two parts — an optional **move line** (only on automatic entry from a prior phase — one line naming the artifact the prior phase just wrote, with the absolute path interpolated, not the literal `$FEATURE_PATH`) and the **phase banner** (always, unconditional). Then begin the phase's first real work step.

This inversion of responsibility exists because an earlier release tried the opposite arrangement — the exiting phase ran a helper script that printed the move line + next banner. The agent routinely skipped the script call, and the next phase trusted the banner was printed, producing silent transitions with no announcement at all. Moving the responsibility onto the receiving phase — and making the entry block unconditional — guarantees the banner renders because the phase's first step is "print the entry block."

**Auto-transition discipline — forbidden shapes.** On the exit side, the **only** correct output is nothing. On the entry side, the only correct output is the entry block (move line + banner) followed by the phase's first real work step. Any sentence that asks the user to signal readiness, push back one more time, or confirm before moving on is a proceed-prompt in disguise — and it defeats the auto-transition. Any summary of the artifact just written is likewise forbidden — the artifact is the summary. Forbidden shapes include (non-exhaustive):

- "Proceed to <next phase>, or investigate further?"
- "Push back on anything — or say 'proceed to <next phase>' when you're ready to lock the plan."
- "Let me know when you're ready to continue."
- "Say 'proceed' / 'continue' / 'go' when you want to move on."
- "I can wait for more pushback, or move to <next phase>."
- "Review it, then tell me to proceed to <next phase>."
- "Findings so far: …" / "Summary: …" / "Here's what I captured: …" after the move line.
- Any re-wording of the move line itself. The move line is a specific sentence — *"<Artifact> written to `<path>/<file>.md`. Entering Phase <N>: <Name> now."* — not a template to rephrase.
- Any literal `$FEATURE_PATH` in the output. Interpolate the absolute path; seeing `$FEATURE_PATH` in the user-facing output means the agent emitted the template variable instead of the resolved value.
- **The entire entry block missing** (both move line and banner absent). This is the silent-transition bug the unconditional entry-block rule fixes. If the user sees design questions or sub-agent dispatches appearing with no phase marker, this is the bug.
- **The banner wrapped in a code fence** (``` ... ```) so the `##` and bolds render as literal characters. Emit the banner as rendered markdown, not as code.

These are all variants of the same bug: turning a conversational flow into a series of handshakes, appending a summarize-and-check where none is called for, or failing to announce a phase entry at all. The rule is simple — **the entry block is the entire continuation of the turn**, then proceed to the phase's first real work step. The user can always interrupt mid-flow to push back or loop back; auto-transitions don't remove user control, they remove the "please proceed" prompt the user would otherwise have to type to reach the next phase.

## Step 7: Living artifact discipline

Read `${CLAUDE_PLUGIN_ROOT}/references/living-artifact.md` and apply it to **every write** of an artifact file. Writes always produce the final state. Never add change markers, timestamps of updates, or "previously we said…" annotations.

The **only** place drift is recorded is `loop-log.md`.

## Step 8: Loop-back detection

Read `${CLAUDE_PLUGIN_ROOT}/references/loop-back-detection.md`. Watch every user message and every sub-agent output for signals. When triggered:

1. Offer to loop back to the appropriate earlier phase
2. On confirmation: append a line to `loop-log.md`, rewrite affected artifacts to the new final state, move the cursor back

## Step 9: Decide → Act hand-off (the single gated transition)

After `4-decision.md` is written, the main flow's planning job is done. **This is the one manual gate in IODA** — every prior transition (Intent → Observe → Orient → Decide) auto-advances, but Decide → Act is gated because real code changes start here. Two things need the user's confirmation before the implementor spawns: (1) the branch the implementor will write to, and (2) the green-light itself.

Resolve the current branch first so the prompt can show it literally:

```bash
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "(detached HEAD)")
```

Then print the hand-off using the **User-facing prompts (non-Orient)** convention: context above, blank line, bold question on its own line, blank line, reply-options hint. The Act explanation follows as a separate block so the branch question stays visually clean. Use the interpolated values for the branch name and feature path — never the literal `<CURRENT_BRANCH>` or `$FEATURE_PATH` strings:

```
Planning complete. Decision written to <interpolated $FEATURE_PATH>/4-decision.md.

**You're on branch `<interpolated CURRENT_BRANCH>` — continue here, or switch before I start?**

Reply `continue`, `new-branch <name>`, `worktree`, or `pause` (to review the plan and come back later).

**What Act does:** the `ioda-implementor` subagent implements `4-decision.md` in alignment with `1-intent.md` — it researches each step, edits the code, runs your verification commands, and spawns a code-review agent. Once launched, `1-intent.md` and `4-decision.md` are an **immutable contract**; the implementor loops *within* implementation (research, try, adjust) but never re-plans. If it hits a true contract flaw, it stops with a **Blocked** entry in `5-act.md` and control returns to you — no silent re-planning.
```

Handle the reply:

- **`continue`** — branch is fine. Spawn the `ioda-implementor` subagent (see below).
- **`new-branch <name>`** — create the branch (`git checkout -b <name>`), confirm the switch, then spawn the implementor.
- **`worktree`** — ask for the branch name and the worktree destination (or follow a project's worktree helper if documented in the per-project `.ioda/config.json`), then spawn the implementor from the new workspace.
- **`pause`** — end cleanly. The user can re-invoke `/ioda <feature>` later; the third entry path (Step 1) will detect the plan-complete folder and re-offer the launch.

**On launch** — spawn the `ioda-implementor` subagent with a prompt containing:

- `feature_path` — absolute path to the feature folder
- `verification_commands` — from the merged config
- `code_review_agent` — from the merged config
- A directive to print the Phase 5 banner on entry

The implementor reads `1-intent.md` + `4-decision.md` as contract, writes `implementor-research.md`, creates `5-act.md` when execution starts, runs verification and code review, and returns control. See `${CLAUDE_PLUGIN_ROOT}/agents/ioda-implementor.md` for the full protocol.

The main flow does not narrate the implementor's work. The implementor's final banner (`✓ Implementor run complete`) is the user's signal that the feature is done.

## Step 10: Completion

If the implementor returned cleanly, say:

```
════════════════════════════════════════
✓ ioda complete for <feature-name>.

Artifacts: <FEATURE_PATH>/
Next: review the diff and ship when ready.
════════════════════════════════════════
```

If the implementor raised a **Blocked** entry in `5-act.md`, do **not** print the completion banner. Instead, read the Blocked entry, identify the loop-back target per `references/loop-back-detection.md`, and offer the loop-back to the user. Rewriting planning artifacts is the main flow's authority, not the implementor's.

## Guidelines

1. **One command, whole flow.** Never ask the user to invoke another `/ioda-*` command. Transitions are conversational.
2. **Sub-agents for heavy phases.** Observe and any deep investigation run in a sub-agent whose result is summarized into an artifact. The main session only holds decisions.
3. **Artifacts are ground truth.** Every sub-agent reads from files, not from conversation. Every new session reads from files. No assumption that prior context carries over.
4. **Investigate first.** If at any step you don't have enough information, investigate before answering.
5. **Pushback is invited.** Expect the user to challenge your findings. When they do, treat it as a signal to dig deeper — not defend.

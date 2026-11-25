---
name: swarm-paper
description: Pre-submission editing pass for research or benchmark papers written with coding agents. Use when the user says "pre-submission pass", "polish / edit my paper", "is this paper ready to submit", or asks agents to write, restructure, or tighten a research or benchmark paper.
---

# Swarm Oversight Harness · Writing research / benchmark papers with coding agents

> **Where this fits**: this skill is an accept gate for the `research` profile. Once the work units (datasets, leaderboards, ablations) are accepted, use this pass to turn them into a submission. It does not replace the project loop. It is what "consolidate → accept" looks like when the output is a paper.
>
> **Scope**: this skill holds only writing rules that apply to every paper. Paper-specific content (scores, model names, tickers) belongs in that paper's source files, not here. Every example below is a one-line illustration, not a fact.
>
> Full rationale: [MANUAL](https://github.com/cogito233/swarm-oversight-harness/blob/main/MANUAL.md).

In one line: **write for the final paper, not the current snapshot.** Anything the final version would delete should not go into the shared draft now.

---

## Three core principles (everything else follows from them)

### 1. Write for the final paper

Every sentence you write should survive into the final version. Keep development mess out of the shared draft.

- **Write missing data as a camera-ready scope statement, not a red `[TODO]`.** State the scope in clean prose ("we report a preliminary slice of N models; the full matrix is left for camera-ready"). A reader who sees `[TODO]` decides the paper is unfinished and starts doubting every claim.
- **Report the design, not the development log.** Bug-fix history, internal red-team rounds and harness refactors are how you got there; they are not the paper. Describe the system.
- **Frame the contribution at its final scale; label the current slice "preliminary".** The final scale is larger (more models, more coverage), and the current results are an honest slice of it. Say both, but position the paper at the final scale.

### 2. Taste: novel vs. trivial

Separate what is genuinely new from narrow implementation choices dressed up as contributions.

- **Do not pad comparison tables with manufactured columns.** A column for a trivial feature, where only your row gets a ✓, reads as fake differentiation, and reviewers notice at once.
- **Real novelty is often a combination, not a single axis.** Put the genuinely hard parts up front. If there is no single breakthrough, present the combination as the contribution.
- **Keep columns where competitors also earn a ✓.** That honesty is what makes "only we get all ✓" believable. A table made entirely of your unique columns looks defensive.

### 3. Debug the typeset PDF, not the source

Treat the paper as an artifact you render, screenshot, and iterate on visually.

- **Compile and read the PDF continuously**, in a compile → read loop. Review the typeset result, not just the `.tex`. Overflowing tables, misplaced figures and broken equations show up only in the PDF.
- **Check every number, claim, and citation against the source of record before release.** Never let a reader find the first error. Anything a human reads as authoritative must be true.
- **Split large papers into per-section files** (`\input{sections/..}`) so several agents can each edit one section without overwriting each other. This is file-disjoint splitting applied to papers.
- **Build figures as artifacts too: HTML/CSS/SVG → headless screenshot → iterate (v1..vN).** Render with headless Chrome, read the screenshot, critique it, and revise. For clean technical diagrams, HTML gives more layout control than TikZ. **Do not use AI image generation for precise scientific figures** (it garbles text and numbers). At most, use it for a background and overlay exact labels on top. Watch the print page box so that a figure PDF is not cropped and does not spill onto two pages. Use `figure*` / `\textwidth` (not `\columnwidth`) for wide figures; use `\resizebox` to keep wide tables inside the margins.
- **Split multi-agent editing by file.** Each parallel agent owns a disjoint set of section files, so there are no conflicts. **Cross-section edits** (a claim or caveat repeated across sections, or moving content to the appendix) must be done by a single agent, or you must assign one canonical home explicitly. Otherwise parallel agents either all delete the content (so it ends up nowhere) or all keep it (so it is never removed). Read-only review agents, and agents working on figures or skills outside the paper, can safely run alongside that one editing agent.

---

## Pre-submission checklist

Run this as an executable pass. If any item fails, do not submit.

### A. Final-paper framing and honesty
- [ ] **Zero red TODOs**: no `[TODO]` or red placeholder text in any shared version. Resolve each one or move it to private notes.
- [ ] **Missing data is written as scope prose**, not placeholders.
- [ ] **No development log in the body** (bug history, red-team rounds, harness refactors).
- [ ] **The current slice is labeled "preliminary"**; the contribution is framed at final scale.
- [ ] **Show honesty, don't announce it**: delete defensive meta-text like "an honest result, not a defect", "we honestly note", "we do not claim". Collect the real caveats in one clean **Limitations** section.
- [ ] **Overclaims leak upward; audit for them before submission.** Papers are often honest in Limitations but drop the caveats in the abstract, intro, and conclusion, where absolute claims survive. Run a dedicated read-only audit pass for overclaims and novelty. Then carry the body's caveats **up** into the abstract, intro, and conclusion, and retire absolute words the evidence cannot support: "calibrated" (needs a human or reference anchor), "invariant" (say "stable / preserved", scoped to the regime you actually tested), "best", "first / only". Scope every headline claim to its real basis (its n, a single run, a single condition). Watch for near-circular validation: an artifact distilled from the same source as a rubric cannot independently validate that rubric.

### B. Taste and argument
- [ ] **The comparison table is a feature matrix**: rows = systems, columns = meaningful axes, cells = ✓ / ✗ / partial. Use this standard shape; do not put prose in cells.
- [ ] **No manufactured differentiating columns**; keep columns where competitors legitimately get ✓, so "only we get all ✓" is credible.
- [ ] **Novelty claims rest on the genuinely hard parts or the combination**, not narrow implementation choices.
- [ ] **State ground-truth provenance up front**: when a benchmark grades quality rather than outcomes, say where the answer key comes from (e.g. "synthesized from ≥3 cross-checked human expert outputs"). "We benchmark against the best human work, not against the future."

### C. Writing habits to fix (from a senior editor's critique)
- [ ] **Bold discipline**: top-venue papers rarely use bold. Use it only for contribution lead-ins and for table headers and winners. If everything is bold, nothing stands out. Let sentence structure carry the emphasis.
- [ ] **Cut the em-dash habit**: "main clause — aside — one more jab" is a first-draft rhythm. Turn about half of them into full stops.
- [ ] **Abstract discipline**: keep it to about 150 words. Do not include low-level single numbers (like "0.04 on X") or implementation details. Introduce every named entity before using it (no bare lowercase model nicknames). Say only what was built, the core finding in one line, and why it is novel.
- [ ] **Reduce neologisms and codenames; keep an academic register**: keep 3–4 load-bearing terms. Move internal item codes and nicknames to the appendix, or drop them. Keep the body in an academic register.

### D. Consistency and structure
- [ ] **Consistency hygiene**: model-name casing, terminology, and citation rendering are uniform. Citations point to real third-party authors; **only self-citations are anonymized for blind review**.
- [ ] **Structure by genre**: a benchmark paper leads with **dataset + leaderboard**. Methodology and the threat model / defenses play a supporting role; they are not co-headlines. **Do not give "Threat Model" its own top-level section**: fold the taxonomy into the metric motivation and the empirical audit into Experiments.
- [ ] **Explicit through-line between sections**: each section opens with a one-sentence bridge and a forward reference, so that the paper does not read like a set of randomly assembled parts.
- [ ] **Structural restraint**: ≤ 3 contributions. Merge Limitations into about 4 clean items instead of 10 fragments. In a benchmark paper, Related Work can go at the end.

### E. Length and evaluation-reporting discipline
- [ ] **Floats drive length; the limit applies to the main body.** Cutting prose soon stops paying off, because the page count is driven mainly by **figures and tables**. To shorten the paper, **cut or merge floats**, not just words. Measure **main-body pages** (excluding references and appendix; venue limits apply to the main body), not total PDF length.
- [ ] **Measure cross-section repetition with grep**: count how many times a key claim's signature phrase appears across sections (we once found one sentence repeated 27 times). Give every claim **one canonical home**. The count is a measurable signal of verbosity.
- [ ] **Do not trust any judge cell that has not passed a completeness check.** An LLM judge can emit empty or truncated verdict lists, and a "missing item counts as fail" backfill rule will **manufacture fake extreme scores** (we once hit a cell at −0.388 whose true value was ≈ +0.07). QC must flag empty or missing-layer outputs and re-judge them, verify completeness cell by cell, and use spot checks / case studies to catch such artifacts before anyone trusts the headline numbers. The authors must catch this before the readers do.
- [ ] **Pin one canonical comparison set**: never compare means across different instance subsets (doing so repeatedly confuses readers, and you).
- [ ] **When judge invariance matters, report cross-judge consensus**, not a single same-vendor judge, as the "ground truth".
- [ ] **Failure analysis goes down to instance-level case studies** (broken down per model), not just aggregate per-layer tables.
- [ ] **Back up before any large regeneration / re-judging batch**: before a run that could overwrite already-analyzed results, snapshot the paper and data (sections / figures / PDF + score matrices + reports, as a **timestamped tar**). A bad batch must never be able to destroy **the headline state you have already analyzed**. Re-running is cheap; losing the analyzed headline is expensive.
- [ ] **Test a factor with a controlled re-run, not by overwriting the headline**: to test robustness to one variable (report language, judge vendor, reasoning effort), change only that factor on **the same instances** and write to **a different filename**, keeping the analyzed headline slice intact. Report the variant as a **controlled comparison**. Never overwrite the headline report to test a variant.

## Why this works (one line)

A paper is the final accepted output of the `research` profile, and **its readers are the verification gate**: a gate that allows no retries and discounts the whole paper after a single error. The purpose of this pass is therefore to leave the reader nothing from the development phase to latch onto. Writing for the final paper keeps you from writing text that will be deleted; taste keeps you from presenting trivial things as contributions; debugging the PDF keeps the reader from finding the first error. Together, the three principles move a draft across the trust boundary to "trustworthy".

---

*General rules only: this file holds writing discipline that applies to every paper. Anything paper-specific (numbers, tickers, model names) lives in that paper's source files, not here.*

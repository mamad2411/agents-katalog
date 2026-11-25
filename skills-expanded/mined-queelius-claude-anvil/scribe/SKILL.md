---
name: scribe
description: Discover latent themes in the metafunctor corpus. Use when the user wants to find implicit through-lines across their blog posts, surface recurring ideas they have not consciously framed as a series, or get candidate themes for a synthesis post. Reads titles, descriptions, and tags; proposes 3 themes that connect 4+ posts each, each with a single-sentence through-line. Output is a proposal, not a draft. Trigger phrases include "find themes in my posts", "what threads connect my writing", "latent themes in my corpus", "scribe".
argument-hint: "[time window like 5y | --tag <name>]"
---

# Scribe: latent theme discovery

Find threads in the user's corpus that they did not realize they had already written. Scan every published post, return up to 3 candidate themes that connect at least 4 posts each, each with a one-sentence through-line and its source posts. The output is a proposal, never a draft.

Arguments: a time window (`5y`) or `--tag <name>` filter; default is the full corpus.

## Workflow

### 1. Read the corpus

Get title, date, description, and tags for every post. Three paths, in preference order:

1. **`mf posts list --json` (primary)**: one Bash call returns the whole corpus as a JSON array with `slug`, `title`, `date`, `description`, `tags` (plus categories/series/featured/draft). Works from any directory (mf resolves the site root itself), and the scribe filters map natively:
   - `/scribe 5y` (time window): `mf posts list --json --since <ISO date>` (or months, e.g. `60m`; the CLI accepts `YYYY-MM-DD` or `30d/4w/3m` forms, not years)
   - `/scribe --tag philosophy`: `mf posts list --json -t philosophy`
   - Requires an mf build that includes `description` in the JSON (added 2026-06-09); if `description` is missing from the output, fall through.
   - First confirm `mf --version` prints `mf, version ...`. TeX Live's `/usr/bin/mf` (Metafont) can shadow the metafunctor CLI; if that is what runs, or if the output is not a JSON array for any reason, fall through to the next path (and mention that `uv tool install -e ~/github/repos/mf` fixes it).
2. **`crier_search` (if the crier plugin is installed)**: `crier_search(limit=1000)` (the default limit is 50, and the corpus is past 250 posts; check that the count returned is below the limit).
3. **Glob fallback (fully self-contained)**: resolve the metafunctor site root from the `MF_SITE_ROOT` env var or the `site_root` key in `~/.config/mf/config.yaml`, then `Glob` `content/post/**/index.md` and read the YAML front matter.

You only need title, date, description, and tags; do not read post bodies.

### 2. Find themes

Look at all the title + description + tag triples together. Resist clustering by tag alone (tags are too coarse). Find threads that satisfy:

- **Span**: connects 4+ posts (3 is too few; 6+ is ideal).
- **Specificity**: the through-line is a *claim* or *observation*, not a *category*. "Intelligence is verifiable search" is a thread. "AI" is not.
- **Latency**: the user did not consciously frame these posts as a series. If they are already a tagged series (e.g., the "Stepanov" series, the "Long Echo" series, the "RL series"), skip those. We are looking for *implicit* threads.
- **Cross-temporal**: bonus if the thread spans multiple years; that is strong evidence the user keeps returning to the idea unconsciously.

For each candidate theme:
- Pick the 4 to 7 most representative posts (not all posts that mention the theme).
- Write the through-line as a single declarative sentence in the user's voice. Specific, not generic. "Reward shape determines what scales" beats "the user thinks about reward functions."

### 3. Output the proposal

Format:

```
3 candidate themes (95 posts scanned):

═══════════════════════════════════════════════════════════════════
[1] VERIFIABLE SEARCH AS THE ARCHITECTURE OF INTELLIGENCE

Through-line: You keep returning to the asymmetry between checking and
finding, applied to science, ML training, test-time compute, and
induction itself.

Span: 5 posts, 2024-09 to 2026-04 (19 months)

Source posts:
  - 2025-01-05  Science as Verifiable Search
  - 2024-09-30  All Induction Is the Same Induction
  - 2024-06-25  Reverse-Process Synthetic Data Generation
  - 2026-04-01  I Spent $0.48 to Find Out When MCTS Actually Works
  - 2026-03-15  What You Assume vs. What You Compute

Why it's a thread: each one is "easy to verify, hard to find" applied
to a different domain. You haven't named the asymmetry directly.
═══════════════════════════════════════════════════════════════════
[2] LEGACY AS A DESIGN CONSTRAINT
...
═══════════════════════════════════════════════════════════════════
[3] CODE WITHOUT PURPOSE / PURPOSE WITHOUT CODE
...

Pick a theme to develop (1, 2, 3) | Reject all (none feel real) | Show me more themes (regenerate)
```

### 4. Stop

Your job ends at presenting the candidates. Do not auto-expand; the user is the editor. They may pick one to expand (then propose a structure and source-post mapping), reject all and ask for more, or rename one whose framing is off.

## Quality bar

The output should pass these tests before you show it:

1. **Each through-line is one sentence.** If it takes two sentences to explain, the theme isn't crisp enough.
2. **Each through-line is specific.** A reader who hasn't seen the posts should be able to predict roughly what the synthesis would argue.
3. **The source posts are chosen, not exhaustive.** Don't list every post that mentions a tag. List the 4 to 7 that *make the thread*.
4. **No themes that are already explicit series.** The user knows about their Stepanov series. Don't propose it back to them.
5. **No "AI/ML topics" or "philosophy posts" themes.** Those are categories. We want claims.

If you can't generate three themes that pass all five tests, return fewer (or zero) and explain why. "Two themes feel real, one feels forced; here are the two." Better than padding.

## What to do when scribe fails

If the corpus genuinely doesn't have three threads, that's useful information. Possible causes:

- The corpus is too small (you'd see this on a 30-post blog, not a 200-post one).
- Tags are too coarse to filter usefully; suggest the user tag with more discrimination.
- The user's thinking has been very project-focused (each post is its own thing) without recurring abstractions; that's a reflection on the writing, not a bug.

Report this honestly. Do not invent a theme to fill the slot.

## When to use other things instead

- **Already know the theme**, just want help with the synthesis: skip scribe and use the `mf` skill's New Post workflow.
- **Want to find unposted gaps in cross-posting**: that is `/crier:chronicler`, not scribe.
- **Want to audit cross-posting status**: dispatch the crier plugin's `auditor` agent.
- **Want to draft a brand-new post on a fresh topic** (not synthesis): regular Claude Code, no special command needed.

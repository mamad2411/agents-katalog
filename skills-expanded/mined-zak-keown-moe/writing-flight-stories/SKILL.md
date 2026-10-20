---
name: writing-flight-stories
description: Use when writing or reviewing a Flight story card. Establishes the calibration framing — outcomes, persona binding, observable acceptance criteria — and explicitly rules out wrong-shaped frames (Agile user stories, QA step-scripts, BDD Given/When/Then) so prior knowledge does not contaminate the card.
---

# Writing Flight Stories

## Thesis

> A Flight story is **an outcome, scoped by a persona, graded by observable conditions — with the mechanics deliberately left out.**

The agent figures out the *how*. The card specifies *what counts as success* in a way that distinguishes a real pass from a confident-sounding bluff.

If you remember nothing else: outcome + persona + observable post-conditions. No clicks, no selectors, no file paths.

## Why this differs from the frames you already know

Three familiar frames look right and are wrong in contagious ways. Read these before you start writing — if you skip this, you will write the wrong shape.

- **Agile user story (`As a X, I want Y, so that Z`).** Not this. The persona is not a stakeholder whose needs are being designed for. It is an identity the agent inhabits during the run, used to anchor inference into the context tree.
- **QA step-script (Step 1: navigate. Step 2: type. Step 3: assert).** Not this. The whole point of an LLM in the loop is that the agent figures out the path. Enumerating steps recreates exactly what we are trying to escape.
- **BDD Given/When/Then.** Not this. Acceptance criteria here are end-state conditions, not consequents of a prescribed sequence. A Flight AC presupposes nothing about how you got there.

If your card reads like any of these, rewrite it.

## The rules

Each rule has a **rationale** (why) and a **smell** (what it looks like when you are violating it).

### 1. Open with persona binding, not a profile reference

Every card starts `You are <Name>.` Never `Use the profile at profiles/x/profile.md.`

- **Why:** the agent reads the context tree and infers which profile to use from the name. That inference *is* part of the test, especially when decoy profiles exist. Naming the path destroys the inference.
- **Smell:** any file path, any reference to a specific profile location, any phrase like "load the profile for…".

### 2. Describe outcomes, not actions

Verbs sit at intent level (sign in, post, find, confirm) — not mechanics level (click `#login`, press down-arrow twice, type email then password).

- **Why:** the surface might change tomorrow; the outcome will not. Mechanical verbs couple your card to a UI version.
- **Smell:** a sequence. If you find yourself writing "first … then … then …", you have drifted into a script. Collapse it back to the goal.

### 3. Mention an affordance only when it is under test

If you are testing whether the agent reads color, name the color. If you are testing whether the agent discovers a form, do not enumerate the form's fields.

- **Why:** mentioned affordances become hints, and hints destroy what you wanted to measure. Card 02 names the yellow underline because reading color *is* the test. Card 04 deliberately does not name the login form's fields because discovery is the test.
- **Smell:** describing UI you do not actually need the agent to perceive (label text, layout positions, button copy that is not load-bearing).

### 4. Acceptance criteria are observable, discriminating post-conditions

Each criterion should:

- Be observable from what the agent can actually see (screenshot, captured pane, stdout) — not server state, not internal flags.
- Distinguish a real pass from a plausible bluff. ("Author field contains Fred's name" works because it discriminates persona inference. "Sign-in succeeded" does not — every transition agent claims that.)
- Use **negatives** for invariants ("post is NOT visible to Quinn"). Negative criteria are usually the load-bearing ones; without them you measure happy-path completion, not the actual property under test.
- Demand **evidence** when testing perception ("cite specific ANSI color codes for one heading and one keyword"). Forces the agent to actually look.

- **Why:** an AC list that the agent can satisfy by narrating the happy path is not testing anything. The point of AC is to fail when something is wrong.
- **Smell:** vague verbs like "able to", "successfully", "works correctly". State the observation instead.

### 5. Don't name files, selectors, or routes

If the agent cannot find what you mean, the fix is in the context tree (or one short domain hint in the body), not in pasting a path into the card.

- **Why:** every name you bake in is a coupling that breaks the next time the surface changes — and a hint that destroys whatever inference it short-circuits.
- **Smell:** literal paths (`profiles/fred/`), CSS selectors (`#submit`), URLs (`/login`), filenames in body prose.

### 6. Stay adapter-neutral in voice

The runner picks CLI / TUI / Web at invocation time. The card describes the work, not the surface. Use "submit", not "click". Use "open file in a horizontal split", not "press Ctrl+W s".

- **Why:** an adapter-neutral card survives moving the same goal across surfaces and stays honest about what is being tested.
- **Smell:** verbs that only make sense on one adapter ("click", "type", "press <key>", "screenshot the…"). Tags can hint at intent (`tags: tutorial, web`); the prose should not.
- **Exception:** when a tool has a domain-specific idiom the agent might not know to invoke (vim's `:sp`, `:wqa`), you can name the operation in its idiom. Name the operation, not the keystrokes.

### 7. Keep the body small

Even the most demanding card in the tutorial set (06: cross-identity friends-only verification) is ~5 sentences plus ~5 AC bullets.

- **Why:** length is a tell that you are over-specifying or running two stories in one. Long cards almost always split cleanly into two short ones.
- **Smell:** body longer than a short paragraph; AC list longer than ~6 bullets; multiple goals chained with "and also".

## Frontmatter template

```markdown
---
id: <kebab-case-id>
title: <one-line title that names the outcome>
status: ready
tags: <comma-separated, include adapter intent if relevant>
---

You are <Persona>. <Outcome described as goal-shaped prose, ~2–4 sentences.>

## Acceptance Criteria

- <Observable post-condition 1>
- <Observable post-condition 2>
- <Negative invariant if relevant>
- <Evidence demand if perception is under test>
```

## Worked example — well-calibrated

This is `03-vim-split.md`. Read it as a positive reference.

```markdown
---
id: tutorial-03-vim-split
title: Split panes in vim, verify highlighting, and find Fred's preferred blood type
status: ready
tags: tutorial, tui
---

You are Fred. Vim opens with `notes.md`. Verify that markdown
syntax highlighting is active — heading lines and list items
should appear in distinct colors against the background, not
plain white-on-black.

Open `setup.ts` in a horizontal split (`:sp setup.ts`).
Confirm TypeScript syntax highlighting works in the new pane:
keywords like `import`, `export`, `interface`, and `async`
should each be styled.

Switch back to `notes.md`. Find the line that names Fred's
**preferred blood type for casual feeding** and report what
it says.

When done, write and quit both panes (`:wqa`).

## Acceptance Criteria

- Markdown syntax highlighting is visible in `notes.md`
  (heading lines styled distinctly)
- TypeScript syntax highlighting is visible in `setup.ts`
  (keywords styled distinctly)
- The reported blood type matches what is written in `notes.md`
- Vim exited cleanly (you see the parent shell prompt or the
  session terminates)
- Cite specific ANSI color codes you observed for at least
  one markdown heading and one TypeScript keyword
```

What makes this calibrated:

- "You are Fred." Persona binding only — no profile path.
- The two color-affordance mentions are the *test*, not hints.
- `:sp` and `:wqa` are vim idioms named at operation level, not keystroke level — fine under rule 6's exception.
- The AC list discriminates: the blood-type criterion fails any agent that bluffed without reading; the ANSI-codes criterion forces evidence; "exited cleanly" rules out a hung session that an "able to quit" criterion would let pass.
- The "find a piece of content" criterion has the answer hidden in `notes.md`, not the profile — the agent has to know where to look.

## Worked example — before / after

This is `05-login-cookies.md` rewritten. The original is in the looser cluster of the tutorial set; it is a useful before/after because the failure modes are small and recognizable.

**Before:**

```markdown
You are Fred. We want to verify that cookie-based login works
correctly. Navigate to the site. Verify that you're not signed
in by looking at the menu bar. Then sign in using Fred's cookies.
When signed in the menu bar will indicate your username following
an `@` sign, and you'll have an option to log out.

## Acceptance Criteria
- - Not signed in initially.
- - By injecting cookies we are signed in as Fred.
```

What is wrong:

- "We want to verify that cookie-based login works correctly" is meta-narration about the test's purpose; it does not belong in the card the agent reads as instructions.
- "By injecting cookies we are signed in" mixes the means (inject cookies) with the end (signed in) and does not say what is *observed*.
- The "able to" / "we are signed in" verbs are the smell from rule 4 — they are the kind of thing the agent can claim from any happy-path narration.
- The double bullet `- -` is just a typo, but it is the kind of typo a calibrated review catches.

**After:**

```markdown
You are Fred. Navigate to the site. Confirm you start signed-out.
Then sign in using Fred's cookies, and confirm you are now signed in.
The signed-in state shows your username after an `@` in the menu bar;
the signed-out state shows a sign-in link.

## Acceptance Criteria

- Initial page load shows a sign-in link in the menu bar — no
  `@`-prefixed username.
- After installing cookies, the menu bar shows `@fred` and a
  logout link.
- The agent did not click logout.
```

What changed:

- Body lost the meta-narration; it now describes the work, not the verifier's intent.
- AC are stated as observable nav states ("sign-in link", "`@fred`", "logout link") rather than as success-of-the-procedure claims.
- The negative invariant "did not click logout" is added — without it, an agent that signed in and then signed out would still satisfy a sloppy "signed in as Fred" criterion at some point during the run.

## Self-check before you commit a card

Run this list. If any answer is "no" or "not sure", rewrite.

- [ ] Does the body open with `You are <Name>.`?
- [ ] Could you delete every step-shaped sentence and still have an outcome statement?
- [ ] Are all named affordances actually under test?
- [ ] Is every AC something an outside observer could verify from screenshots, captured pane, or stdout?
- [ ] Does at least one AC distinguish a real pass from a plausible bluff?
- [ ] If an invariant matters ("not visible to non-friends"), is it stated as a negative AC?
- [ ] No file paths, no selectors, no URLs in the body?
- [ ] Adapter-neutral verbs throughout (modulo the operation-idiom exception)?
- [ ] Body fits in ~5 sentences; AC fits in ~6 bullets?

If a card needs more than this, it is probably two cards.

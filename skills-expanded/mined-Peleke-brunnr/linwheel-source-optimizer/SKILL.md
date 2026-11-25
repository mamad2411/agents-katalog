---
name: linwheel-source-optimizer
description: >
  Optimize raw engineering output (buildlog entries, GH synthesis, daily notes, session logs)
  into high-quality ::linkedin Obsidian notes that produce the best possible LinWheel reshape
  output. Structures content around proven LinkedIn post anatomy: hooks, tension, specifics,
  and angle-ready beats. Use when writing vault notes destined for the LinWheel pipeline.
metadata:
  openclaw:
    emoji: "\U0001F3AF"
    requires:
      tools: []
---

# LinWheel Source Optimizer

> Turn raw engineering output into ::linkedin notes that reshape loves.

## Purpose

The LinWheel content engine (analyze + reshape) produces output proportional to input quality.
This skill optimizes the INPUT — the Obsidian note that triggers the cadence pipeline — so
reshape has the richest possible material to work with across all 7 angles.

You are NOT writing LinkedIn posts. You are writing **source material** that the LLM reshape
step will decompose into angle-specific posts. Think of yourself as a journalist filing notes
that a columnist will turn into articles.

## When to Use

- Writing `::linkedin` notes to the Obsidian vault (Buildlog/ or Writing/Drafts/)
- Processing raw buildlog entries or GH Watcher synthesis into publishable source
- Preparing session logs or engineering notes for the LinWheel pipeline
- Any time content needs to flow through cadence → LinWheel → LinkedIn

## Trigger Phrases

- "Optimize this for LinWheel"
- "Write this as a LinkedIn source note"
- "Prepare this buildlog for LinkedIn"
- "Turn today's work into a vault note for LinWheel"
- "Source-optimize this"

---

## Vault Output Path

```
${VAULT}/Buildlog/   (${VAULT} = your Obsidian vault path)
```

Filename: `YYYY-MM-DD-{slug}.md` (e.g., `2026-02-27-github-watcher-shipped.md`)

---

## The Anatomy of High-Quality LinWheel Input

### What Reshape Needs

Each of the 7 angles looks for different raw material in the source text:

| Angle | What It Needs in the Source | Example Beat |
|-------|---------------------------|--------------|
| **field_note** | Concrete "I did X, Y happened" sequences | "Shipped 3 PRs across 2 repos. The overlay mount fix took 4 attempts." |
| **contrarian** | A conventional wisdom + evidence it's wrong | "Everyone says microservices. We went monolith and deploy 10x faster." |
| **demystification** | A complex thing + a simple explanation | "Overlayfs inotify doesn't fire for lower-layer changes. Here's why." |
| **identity_validation** | A relatable struggle + resolution | "I spent 3 hours debugging a mount unit. Turns out: one backslash." |
| **provocateur** | A sacred cow + a reason to question it | "Most AI agent frameworks are overengineered. A shell script beats them." |
| **synthesizer** | Two unrelated ideas + a surprising connection | "The same pattern that makes Obsidian plugins great makes MCP servers great." |
| **curious_cat** | A genuine open question + why it matters | "Why does every dev tool assume you'll use their dashboard? What if you won't?" |

### The Source Note Structure

A good source note contains 3-5 **beats** (discrete story units). Each beat is 2-4 sentences
that capture one moment, decision, or insight. Reshape picks different beats for different angles.

**BAD source note (generic, no beats):**
```
Today I worked on the GitHub Watcher responder. It scans repos and generates LinkedIn content.
I also fixed some bugs. The tests pass now. Overall productive day.
```

**GOOD source note (beat-rich, angle-ready):**
```
The GitHub Watcher shipped today — 14 files, 1500 lines, 33 tests.

It runs on a cron, scans every Peleke/* repo for the day's PRs and buildlog entries,
then synthesizes a narrative via LLM. The output is a ::linkedin-tagged Obsidian note.
The existing pipeline carries it the rest of the way: ObsidianWatcher detects the file,
LinWheel reshapes it into 21 drafts, Telegram pings me to review.

The hardest part wasn't the code — it was the overlay mount. Writing to the upper dir
directly bypasses inotify on the merged mount. Chokidar never sees the file. I burned
2 hours before realizing the write path matters more than the write content.

Every dependency is injectable: GitHub client, file writer, clock, LLM. The tests
mock everything. No network calls in CI. This is the pattern I wish every framework
taught instead of "just mock the module."

Here's the thing nobody talks about: most "content creation tools" require you to
stop working and start creating content. What if the content was a side effect of
the work itself? That's what this pipeline does. Ship code → content appears.
```

Count the beats:
1. Shipping stats (field_note material)
2. Architecture walkthrough (demystification material)
3. The overlay debugging story (identity_validation material)
4. The testing philosophy (contrarian material)
5. The "content as side effect" insight (provocateur/synthesizer material)

Reshape can pull from any of these to generate posts for different angles.

---

## Source Note Template

```markdown
---
linkedin_angles:
  - field_note
  - contrarian
  - demystification
---

::linkedin

# {Title — Descriptive, Not Clickbait}

{Beat 1: The headline fact. What shipped, what changed, what happened.
Include numbers: PRs merged, lines written, tests passing, hours spent.}

{Beat 2: The "how" — architecture, approach, or process. One specific
technical decision explained simply enough for a senior non-specialist.}

{Beat 3: The struggle or surprise. Something that went wrong, took longer
than expected, or challenged an assumption. Be specific about the failure.}

{Beat 4: The insight or lesson. What you'd tell someone starting this
from scratch. Frame as "the thing nobody tells you" or "what I wish I knew."}

{Beat 5 (optional): The bigger picture. Connect this work to a trend,
a contrarian position, or an open question in the industry.}
```

### Frontmatter: Angle Hints

The `linkedin_angles` frontmatter tells the LinWheel publisher which angles to use
instead of the defaults (field_note, demystification, contrarian).

**Choose angles based on the strongest beats:**

- Lots of concrete "I did this" material → `field_note`
- A clear "conventional wisdom is wrong" thread → `contrarian`
- A complex topic explained simply → `demystification`
- A relatable struggle → `identity_validation`
- A deliberately provocative take → `provocateur`
- Cross-domain connections → `synthesizer`
- Genuine open questions → `curious_cat`

Pick 2-4 angles maximum. More angles = thinner material per angle.

---

## Prose Constraints

These rules produce source material that reshape handles well:

1. **Specifics over abstractions.** "3 PRs across 2 repos" not "made good progress."
2. **Active voice.** "I shipped" not "the feature was shipped."
3. **First person.** This is going to LinkedIn. Write as the author.
4. **One idea per sentence.** Reshape needs to pick apart your beats.
5. **No LinkedIn formatting.** No short lines, no whitespace hacks, no emojis. Reshape handles all formatting. Write natural prose.
6. **No hashtags or CTAs.** Reshape adds these if appropriate.
7. **Include the failure.** The best LinkedIn posts have a struggle. If everything went perfectly, it's boring. Find the tension.
8. **Name the tools/technologies.** "TypeScript" not "a language." "Obsidian" not "a note-taking app." Technical credibility matters.
9. **Under 1500 words.** LinWheel's reshape works best with 300-800 word source notes. Over 1500 words, use `split` instead of `reshape`.
10. **End with an open thread.** A question, a "what's next," or an unresolved tension. This gives reshape material for hooks and closers.

---

## Workflow: Raw Input → Optimized Source Note

### From a buildlog entry or GH Watcher synthesis:

```
1. READ the raw input (buildlog entry, GH synthesis, session notes)
2. IDENTIFY the 3-5 strongest beats:
   - What's the most concrete thing that happened?
   - What was surprising or counterintuitive?
   - What would a technical peer find interesting?
   - What's the relatable human moment?
   - What's the bigger industry connection?
3. SELECT 2-4 angles that match the beats
4. WRITE the source note following the template
5. ADD frontmatter with linkedin_angles
6. WRITE to vault: {vaultPath}/Buildlog/YYYY-MM-DD-{slug}.md
```

### From a conversation or brainstorm session:

```
1. EXTRACT the key claims, decisions, or insights from the session
2. PICK the single strongest thread (don't try to cover everything)
3. FIND the tension: what was the debate? what was counterintuitive?
4. WRITE 3-4 beats around that single thread
5. ADD frontmatter, write to vault
```

### From raw code or PR descriptions:

```
1. READ the PR title, description, and diff summary
2. TRANSLATE technical changes into impact: "what does this enable?"
3. FIND the story: why was this built? what problem existed before?
4. INCLUDE one specific technical detail that demonstrates craft
5. WRITE 3-4 beats, add frontmatter, write to vault
```

---

## Anti-Patterns (What Makes Bad Source Notes)

| Anti-Pattern | Why It Fails | Fix |
|---|---|---|
| Laundry list of commits | Reshape can't find a narrative thread | Pick the 1-2 most interesting commits, tell the story |
| All abstract, no specifics | "Made progress on infrastructure" gives reshape nothing | Add numbers, names, outcomes |
| Already formatted for LinkedIn | Short lines, emojis, hashtags confuse reshape | Write natural prose, let reshape format |
| Too many topics | 800 words covering 5 different projects | One thread per note. Split into multiple notes. |
| No tension | "Everything worked great" | Find the struggle. There's always one. |
| Passive voice throughout | "The system was deployed" hides the author | "I deployed" — LinkedIn is personal |
| Marketing language | "Excited to announce" "game-changing" | Be specific and direct. No hype. |

---

## Quality Check

Before writing the note to the vault, verify:

- [ ] Has `::linkedin` marker (line 1 after frontmatter, or line 2 if H1 on line 1)
- [ ] Has `linkedin_angles` in frontmatter with 2-4 angles
- [ ] Contains 3-5 distinct beats
- [ ] Each beat has at least one specific detail (number, name, tool, outcome)
- [ ] At least one beat contains tension, surprise, or failure
- [ ] Written in first person, active voice
- [ ] Under 1500 words (ideally 300-800)
- [ ] No LinkedIn formatting (no short-line tricks, no emojis)
- [ ] Ends with an open thread (question, "what's next", unresolved tension)
- [ ] Filename follows `YYYY-MM-DD-{slug}.md` convention

---

## Example: Optimizing a GH Watcher Output

### Raw GH Watcher synthesis (input):
```
Today's GitHub activity focused on the OpenClaw sandbox project. PR #100 was merged,
adding the GitHub Watcher responder to the cadence pipeline. This responder scans all
Peleke/* repos nightly, collects merged PRs, open PRs, and buildlog entries, then
synthesizes them via LLM into a narrative engineering log. The output is tagged with
::linkedin and written to the Obsidian vault, where the existing pipeline processes it.
```

### Optimized source note (output):
```markdown
---
linkedin_angles:
  - field_note
  - contrarian
  - synthesizer
---

::linkedin

# The Code That Writes Its Own LinkedIn Posts

PR #100 shipped today: a GitHub Watcher that scans every repo I own, collects the day's
PRs and buildlog entries, and synthesizes them into a LinkedIn-ready note via Opus. 14
files, 1500 lines, 33 tests. Merged on the first review.

The architecture is boring on purpose. A cron fires at 9 PM. The watcher subscribes to
that signal, scans repos sequentially (rate limits), and writes one markdown file to the
Obsidian vault. The existing pipeline — ObsidianWatcher, LinWheel publisher, Telegram
notifier — carries it from there. No new infrastructure. No new dashboards. Just one
more subscriber on the signal bus.

The part that almost broke me: overlay mounts. I wrote to the upper directory and
Chokidar never saw the file. Turns out overlayfs inotify only fires on the merged mount.
Two hours of "why isn't this working" before I realized the write PATH matters more than
the write CONTENT.

Every dependency is injectable — GitHub client, filesystem, clock, LLM provider. The
test suite mocks all of them. Zero network calls in CI. I've written enough untestable
code in my career to know: if you can't test the happy path without a network connection,
the architecture is wrong.

Here's what I keep coming back to: most content tools ask you to stop working and start
creating content. But what if content was a side effect of the work itself? I ship code.
The pipeline notices. Drafts appear in my queue. I approve the good ones over coffee.
That's it. What other workflows could work this way?
```

Notice: same facts, completely different source quality. The optimized version has 5 clear
beats, tension (the overlay debugging), a contrarian position (injectable deps), and an
open question at the end. Reshape will produce dramatically better posts from this input.

---
name: swarm-write
description: Writing for humans — any end-user-facing text, in any language. READMEs, landing pages, blog posts, social posts, marketing copy, release notes, docs, and UI microcopy (tooltips, buttons, empty states, error messages). Use when asked to write, rewrite, polish, or humanize copy, when text sounds robotic or AI-generated, when defining a voice or tone, and — unprompted — whenever you are about to produce any string a real user will read.
---

# swarm-write — writing for humans

Most agent-written copy fails the same way: no voice, even rhythm, filler detail, and the
machinery showing through. This skill is not a banned-word filter. Filters date fast and
flatten every voice into one texture. Write from a stance, then subtract.

## Jurisdiction (check this first)

| lane | reader | what applies |
|---|---|---|
| **end-user text** | humans who did not ask for it | all of this skill |
| agent-facing (prompts, tickets, queue, skill files) | models | machine lane, unchanged |
| project docs (SRS, ADRs, specs) | owner + future agents | clear and complete, no voice work, no marketing |
| code and the prose inside it | engineers | §Code lane only |

Outside the first row, stop reading and write as you normally would.

## 1. Name the reader before writing a word

One line, not an interview: **who reads this, what they do next, what they already know,
what makes them quit.** Most agent copy is bad because it was written for whoever asked,
not whoever reads.

Write to **one person**, not an audience. "A backend dev at a 20-person startup who just got
paged" produces sharper prose than "developers," every time. Specificity in the reader
creates specificity in the writing.

## 2. Voice

**First: whose voice is it?** The surface decides, and getting this wrong personalizes what
shouldn't be personal:

- **Personal** (the user's posts, portfolio, personal brand, a project that *is* them) → the
  user's voice. Profile, menu candidates, samples — everything below applies.
- **Product** (an app, tool, or service built for an audience) → the **product's** voice,
  derived from audience + category + brand direction, not from the user's persona. If
  `swarm-design-ui` chose a brand direction, that choice *is* the voice input — derive from
  it, don't re-interview. Store as the project's `voice.md` with `owner: product`. The user
  approves it once like any design decision; nobody's personal taste is mined for it.
- **UI microcopy** (tooltips, errors, buttons, empty states) → automatic, always. Product
  voice + the reader's emotional state (`references/ui-copy.md`) set the register. Never run
  voice candidates for a tooltip.

When unsure, one question: "is this you talking, or the product?"

Three layers. Load `references/voice-menu.md` for the named profiles, dials, and samples.

- **Identity** (stable): stance toward the reader, words in and out, commit-vs-hedge posture.
- **Register** (per piece): formality, warmth, humor, energy, person, rhythm, technicality.
- **Move set** (the craft): how it opens, whether it lists, whether it admits uncertainty,
  whether it sets up a payoff or leads with it. This layer is what makes a voice
  recognizable. Two voices can both be "warm and direct" and sound nothing alike.

**Register moves within a piece.** One document is not one register: the opening of a README
is a hook and may sell; the mechanics section explains like a colleague; the FAQ talks like a
person answering a question. Identity and move set stay constant across the whole piece;
the dials shift by **zone** (see the zoning section of `references/voice-menu.md`). Applying
one flat register everywhere produces text that is consistent and dead. Marketing register is
legitimate *in the zones built for it*: a hook, a landing headline, a launch post. It becomes
slop only when it leaks into explanation.

**Where voice comes from, in order:**

1. **An existing profile** (§Storage). Found one? Use it, skip to §3. Never re-derive.
2. **Menu candidates on the real content.** Pick 2–3 profiles that fit the job, write **the
   real opening** in each (~50 words, never filler — comparing filler teaches nothing), show
   them side by side. User points, or says "this one, less X." Save the result.
3. **The user's own writing — opt-in, offered exactly once** while building the first
   profile: links to posts, docs they wrote, anything they're proud of. If they skip, don't
   ask again; the rejection log converges on their voice anyway. If they *ask* ("write it
   like me"), collect in fidelity order per the table below, fetching public posts only
   from URLs they give you.
4. `"just write it"` is always a valid answer: use the global default plus the anti-voice
   list, show the draft, offer to refine.

Samples are an accelerator, never a dependency — recognition beats description, and a few
rounds of rejections beat both.

**Learning from what they already wrote** (when offered samples, posts, or their own
prompts), in fidelity order:

| source | extract |
|---|---|
| text they wrote and edited | everything |
| text they wrote unedited (prompts, messages, commits) | **signal** only |
| text they admire but did not write | shape and stance only, never phrasing |

**Signal vs artifact.** Signal is voice: rhythm, how they open, what they emphasize,
directness, humor, how frustration reads. Artifact is the medium: typos, run-ons, dropped
punctuation, the fragmentary syntax of typing fast. Only signal transfers.

**Grammar.** Output is always grammatical in the target language. But some "errors" are
voice: fragments for emphasis, sentences opening with And, comma splices for pace.
Frequency decides. **Once is a slip and gets fixed. Consistent across samples is a choice
and gets kept.**

**Storage** — global default, per-project override, degrading gracefully:
`voice.md` in the vault (`10 Projects/<P>/voice.md`, plus a global one) → `.writing/voice.md`
in the project → in-session, offering to save. Every rejection the user makes appends to the
file with the reason. After ten pieces it knows things no interview would have surfaced.

Keep the mirror too: the **anti-voice** list, the exact things this user hates.

## 3. Write

- **Sweep the category first when the format competes for attention** (posts, landing pages,
  marketing, launches) or is unfamiliar: read 3–5 strong recent *human* examples of the
  format, extract shape and stance, never phrasing. Research answers "what shape wins here",
  the voice profile answers "how you sound inside it" — different questions, both improve
  the piece, and one line states whether you swept or went straight in. For non-English
  culture-bound formats this stops being optional (§7).
- **Lead with the payload.** The answer is sentence one, not sentence four.
- **Cut the setup.** Most opening paragraphs are throat-clearing. Delete down to the first
  real sentence.
- **Three openers before the body.** The first sentence sets the voice of everything after
  it, and copy that dies in sentence one never recovers.
- **High-stakes single lines get candidates, not a verdict.** Tagline, headline, button
  label, subject line: deliver 2–3 real options and let the user point. One line carrying a
  whole surface is exactly where their taste beats your judgment.
- **Concrete beats abstract.** A number, an object, a scene beats an adjective.
- **Show the change, not the category.** "Agents stop overwriting each other" beats
  "improved coordination."
- **Vary sentence length deliberately.** Three same-length sentences in a row is the
  strongest AI tell there is, stronger than any word choice.
- **Explain only what the reader cannot infer.** When explanation is genuinely needed, one
  concrete example does the work of three abstract sentences.
- **Calibrate confidence.** State opinions as opinions with no cushioning; make real
  uncertainty visible instead of smoothing it over. Agents invert this by default.
- **Scan surfaces scan.** README, landing, posts, release notes: short sentences, fragments
  legal, numerals not words (`13 skills`, never "thirteen skills"), bullets when items are
  genuinely parallel. Long woven sentences are for essays and stories. The same detail can
  almost always be delivered as a strong lead line plus short fragments.
- **Stack the hook.** One logical unit per line, white space between them as the pacing.
  Stacked lines read like a poster; the same words in a paragraph read like homework.
  In Markdown, single newlines merge when rendered — use blank lines so the break survives.
- **The first-interface jargon gate.** On any first-touch surface, every term must survive a
  reader with zero context. If a word only makes sense after the product is understood
  ("claim", "wire", "injected context"), replace it with what it does, or teach it in the
  same breath.
- **No coinages.** An invented clever phrase ("session archaeology") makes the reader stop
  and decode. If you're proud of a phrase, that's the one to check.
- **Read it aloud.** If a sentence can't be said in one breath in a normal speaking voice,
  it's wrong. Catches rhythm problems no rule catches.

**Brevity is not the goal. Density is.** Cut what doesn't earn its place; keep what the
reader needs even when it runs long. Warmth costs words sometimes and that's fine. Copy
that's been cut to the bone is robotic in the other direction.

## 4. The audience firewall

> End-user text never mentions the machinery that produced it. No rules, no constraints, no
> process, no "as requested", no "to keep this brief", no apologizing for what isn't
> included. The reader gets the result, never the making of it.

Same section, same principle: no "in this article we will," no announcing the structure, no
telling readers what they just read.

## 5. Subtract

1. **Cut 30%**, then look at what broke. What survives is better and the wreckage shows you
   where the fat lives.
2. **Shape tells before word tells.** The strongest AI signal now is structure, not
   vocabulary: bulleted lists with bolded lead-ins, rule-of-three sections, the summary
   nobody asked for, one emoji per feature. Word-level filters pass all of these straight
   through. `references/tells.md` has both, tiered.
3. **The obvious-sentence test.** Scan for anything a person who actually knew the subject
   wouldn't have bothered to write down.

## 6. Review and refine

When auditing existing copy (yours or theirs):

1. Read as the target reader and mark **the exact sentence where they'd stop.** One mark,
   worth more than any score.
1b. **Trace the eye path.** Read only what a scanner sees: headings, bold leads, first
   lines, stacked hook lines. Does that skeleton alone make the case? Most readers never
   read anything else — if the skeleton doesn't sell it, the prose never gets the chance.
2. Diagnose on five dimensions, as a reading and not a gate: directness, rhythm, trust,
   authenticity, density.
3. Rewrite, then show **only the 3–5 sentences that changed most**, side by side, one line
   of reasoning each. Never a full diff.
4. Append whatever they reject to the voice profile.
5. **Sort each correction: taste or craft.** Personal taste ("I hate em dashes") goes to
   `voice.md`. Universal craft (a jargon gate, a rendering gotcha, a scan rule) is a bug in
   *this skill* — propose adding it here, so every future project inherits the fix instead
   of relearning it. A correction filed in the wrong place is a lesson that doesn't compound.

## 7. Language

**Compose natively. Never write English and translate.** Translation carries English
sentence architecture, and that is the single loudest tell in most languages.

Register is a **grammatical** decision in most languages, not a word choice: settle it in the
target language's own system (formality level, keigo, du/Sie, tu/vous) before drafting.
Length norms, valued rhythm, and typography are local too, so English brevity dogma and the
English tells list do not travel. Density travels. Word counts don't.

Read 3–5 real human examples first when the format is culture-bound (marketing, social,
humor) or the register call is load-bearing. Say in one line which path you took, so the
reader of your work knows whether it was researched or improvised. If your own command of
the target language is shaky, say so and offer research rather than producing fluent-looking
mediocrity. Details: `references/languages.md`.

## Code lane

**This skill has zero authority over code structure, depth, error handling, or test
coverage.** It governs only the prose inside code, and "fewer comments" is not the goal.
Fewer *empty* comments is.

- Comments answer **why**. The what is the code's job.
- Docstrings: one line on what a caller gets. Add the `FR-XX` reference when one exists, so
  the trail to the spec exists without copying the spec into the file.
- A non-obvious algorithm, an invariant, or a workaround gets one to four plain sentences,
  written for a tired engineer at 2am.
- Never delete a comment carrying information the code doesn't: a reason, a link, a gotcha,
  a license note.

## References (load on demand)

| file | when |
|---|---|
| `voice-menu.md` | choosing or blending a voice, building a profile |
| `formats.md` | the physics of a specific format (README, landing page, post, blog, email) |
| `ui-copy.md` | microcopy: errors, empty states, buttons, tooltips, onboarding |
| `tells.md` | auditing or de-slopping existing text |
| `languages.md` | writing in any language other than English |

## Peers

`swarm-design-ui` hands over every string in its component inventory · `swarm-implement`
routes user-visible strings here · `swarm-review` audits shipped copy against `voice.md`.
With no vault present the skill runs unchanged on `.writing/voice.md` (§2), same as the rest
of the catalog.

---
*Influences: Wikipedia's "Signs of AI writing" via blader/humanizer; kjmagnan1s/anti-slop
(tiered tells, protect-list, scoring); haowjy/creative-writing-skills (llm-writing,
reader-reward channels); content-designer/ux-writing-skill; ComposioHQ
content-research-writer — see CREDITS.md.*

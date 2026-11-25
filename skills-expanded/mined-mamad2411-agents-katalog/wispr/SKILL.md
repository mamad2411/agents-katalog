---
name: wispr
description: Pull recent Wispr Flow voice dictations and use them in the current session. Use when user explicitly says "/wispr", "I just dictated", "I'm done dictating", "pull my voice notes", "ingest the wispr", "grab my wispr", or signals they finished dictating context they want Claude to use. Surfaces transcripts in chat, then applies them to the active workflow OR routes to data/inbox.md based on conversation context.
---

# Wispr — Voice Dictation Ingest

Bridge between Wispr Flow's voice-captured Notes and the current Claude conversation. Lets Nick dictate context (for thank-you notes, debriefs, brain dumps, mid-task captures) and have it land in the conversation as text Claude can use immediately.

## When to invoke

**Explicit triggers:**
- `/wispr` (with or without arguments)
- "Pull my wispr" / "grab my voice notes" / "ingest the wispr"
- "I just dictated" / "I'm done dictating" / "I dictated some things"
- After Nick said he'd dictate and now signals he's back

**Do NOT auto-invoke** — only on user signal. Voice capture is intentional; respect that.

## Arguments

Optional: time window or mode. Examples:
- `/wispr` → defaults to script's state cursor (since last pull) or 30 minutes if no state
- `/wispr 30m` / `/wispr 2h` / `/wispr 24h` → custom window
- `/wispr all` → ignore state, pull everything (use sparingly; will rewrite vault files)
- `/wispr peek` → preview-only mode: shows transcripts in chat without writing files or advancing state. Useful for "what's currently in my Wispr buffer." Maps to `--all --print --dry-run`.

## Instructions

### Step 1: Pull + print

Single command does pull + chat-friendly output:

```bash
PYTHONIOENCODING=utf-8 python3 tools/wispr_pull.py --print
```

Add `--since {window}` if a window was specified.

The `--print` flag emits transcripts to stdout below the import summary. Files are also written to the Obsidian vault (`~/Documents/Obsidian/00-voice-corpus-archive/`) per usual — that's the canonical voice archive.

### Step 2: Handle empty pull

If `Found: 0`:

- Tell user: "No new dictations since last pull (or in the last {window})."
- Offer: "Want me to widen the window? Try `/wispr 24h` or `/wispr all`."
- Stop. Don't probe further.

### Step 3: Detect intent from conversation context

Look at the last 5–10 turns of conversation. Two cases:

**Case A — Active task waiting on this content.** Examples:
- Drafting Zuora thank-yous and Nick said he'd dictate context per person
- Building a CV angle and Nick said he'd dictate his own framing
- Post-call debrief workflow and Nick is dictating takeaways
- Cover letter problem-statement work and Nick is dictating "their problem"

→ **Apply the content to that workflow.** Do not ask. Surface the transcript first (so Nick can see what landed), then proceed with the task.

**Case B — No active task that needs this.** Conversation is in a planning, status, or general state.

→ **Show the transcripts and ask.** Three options:

1. **Use now** — feed into a task we'll start
2. **Route to `data/inbox.md`** — capture for later triage (per `/remember` conventions)
3. **Both** — apply some chunks, route others

If the dictation has clear chunks (multiple short notes), propose splitting per chunk. Don't force one fate for all.

### Step 4: Surface the transcript

Always show the user what Wispr captured, formatted for readability:

```
**Wispr — N dictation(s) since {timestamp}**

— {timestamp} | {derived title}

{full content}

— {timestamp} | {derived title}

{full content}
```

For long transcripts (>500 chars per chunk), still show the full text — voice captures lose meaning when summarized. If 5+ chunks, lead with a 1-line summary per chunk and offer "show all in full" if Nick wants.

### Step 4.5: Date + framing anchor check (MANDATORY before any dated reflection file)

Before writing ANY file whose name encodes a date (`YYYY-MM-DD-*.md` in `data/reflections/` or `<personal-vault>/data/reflections/`), perform this check and surface the result to Nick. Do NOT write the file until Nick has confirmed the date and framing.

**Origin:** 2026-05-27. A 5/26 post-onsite target-company anxiety rumble (captured by Wispr at 5/27 13:48) was routed as `2026-05-27-targetco-anxiety-pre-onsite.md` — wrong on both axes. Filename date used the Wispr capture timestamp instead of the event date Nick stated in the rumble ("Reflections, May 26, 10:50"). Pre/post framing contradicted MEMORY.md, which already had the target-company onsite on Mon 5/25 — so by Tuesday 5/26 the rumble was post-onsite, not pre. See [[feedback_reflection_event_date_not_capture_date]]. This is the same gap-filling failure mode as [[feedback_silent_gap_filling_on_screenshot_parsing]] and [[feedback_cross_context_name_conflation]] — third documented occurrence, hence structural enforcement here.

**The check (4 sub-steps, all four required):**

1. **Read the rumble's first 2 sentences.** Quote any explicit date/time anchor verbatim. Examples: "Reflections, May 26, 10:50", "yesterday morning", "May 27th, 7:12", "this morning". If no anchor exists, say so explicitly.

2. **Resolve the anchor to an absolute date.**
   - Explicit calendar anchor in the rumble ("May 26") → that is the filename date. Authoritative.
   - Relative anchor ("yesterday", "this morning") → resolve against the Wispr capture date, BUT recognize the capture itself may lag the event by hours-to-days. If the relative anchor is ambiguous, ask.
   - No anchor at all → filename date = Wispr capture date, AND state that explicitly so Nick can correct.

3. **Scan for any scheduled event the rumble references.** Check `data/job-pipeline.md` first (authoritative for interview/round dates), then the memory corpus: MEMORY.md's Critical Context block covers only always-visible facts now — full event-level detail (e.g., an interviewer dossier memory with "Runs Mon 5/25 case") lives in `memory/index-coaching.md` or `memory/index-projects.md` (check MEMORY.md's Topic Shards router table if unsure which). If the rumble mentions an interview, call, deadline, or other event found in any of these, the pre/post/upcoming framing in the filename MUST be consistent with that calendar. Concretely: if the source says event X is on date D, and the rumble is dated >D, the framing is "post-X", not "pre-X". If you cannot find the event anywhere but the rumble suggests one is scheduled, ask Nick to confirm the date.

4. **Surface the proposal to Nick in one line BEFORE writing.** Format:

   > Proposing: `<filename>` — date from <"rumble first line" | "Wispr capture (no anchor in text)" | "relative anchor resolved against capture">; framing <pre/post/none> based on <pipeline/memory event reference | no scheduled event referenced>. Confirm?

   Do NOT write the file until Nick confirms. A rename after-the-fact requires updating wiki-links from anywhere it was referenced (the [[wispr-YYYY-MM-DD-HHMMSS-*]] back-pointer from any synthesis destination, plus the source archive in `~/Documents/Obsidian/00-voice-corpus-archive/`).

**Anti-patterns this step is designed against:**

- **Capture-timestamp-as-event-date.** The Wispr DB's modified-after timestamp is when Wispr saw the note, not when Nick was reflecting. They are routinely hours-to-days apart.
- **Pre/post labels invented from rumble mood alone.** "Anxious about the onsite" reads pre-event to a naive scan, but the same mood applies post-event during waiting. The calendar in MEMORY.md resolves the ambiguity.
- **Silent rename later.** Once a reflection is referenced via [[wiki-link]] from a synthesis destination, renaming the file orphans the link. Get the name right at write-time.

**Skip this step ONLY when:** the destination is not a dated reflection file — i.e., living-log appends via `living_log_append.py` (where the date is an explicit arg Nick can see), `data/inbox.md` routing (no per-entry filename), or mid-task application where no file is written.

### Step 4.7: Topic-match gate (MANDATORY when a topic is claimed)

Before assembling a routing proposal or applying the transcript, **verify that the pulled chunks actually mention the topic that was claimed** — either by Nick (preceding conversation: "I just dictated about Acme AI prep") or by Claude's intent detection in Step 3 (inferred topic from filename, recent calendar, or surrounding conversation).

**When the gate fires:**
- A topic claim was made (explicit user phrase, OR Claude inferred a specific topic in Step 3)
- The pulled corpus has ≥1 chunks

**When the gate does NOT fire (skip silently):**
- No specific topic was claimed — pure capture, "/wispr" with no contextual claim, raw archive routing
- User explicitly says "route everything, no topic claim" (rare)

**Check (explicit token count, NOT LLM-judgment):**

1. **Extract topic keywords** from the claimed topic. For "Acme AI prep" → `[acme]`. For "project synthesis" → `[project]`. For person names → the verbatim name + last-name variant. For multi-word topics, generate 1-3 keyword variants (case-insensitive, allowing minor stem variants like trailing -s).
2. **Count chunks containing any keyword** (case-insensitive substring match across each pulled chunk's body text).
3. **Strict-zero threshold:** if zero chunks match any keyword, the claim does not match the corpus.

**On zero matches — STOP with override prompt:**

```
⚠️ Topic-match gate fired: no chunks reference <claimed topic>.

Pulled N chunks; zero contain any of: <keyword list>.

This usually means:
 (a) the topic claim is wrong (Nick dictated something different than expected)
 (b) the pull window is wrong (different time range than the dictation)
 (c) Wispr-rendering swapped the topic word for a near-variant (per
     memory/feedback_default_to_canonical_spelling_when_memory_flags_wispr_rendering)

Options:
 1. Re-pull with different parameters (correct topic, different time window)
 2. Override and proceed — the claim was wrong, route the chunks anyway
    based on actual content
 3. Surface the actual chunks for Nick to review and re-direct
```

Default to option 3 when in doubt — never silently proceed to Step 5 with a mismatched topic claim.

**On ≥1 match:** proceed silently to Step 5.

**Why this gate exists:** without it, /wispr would assemble a routing proposal claiming "here are your Acme AI prep notes" when the chunks were actually about something else entirely. Origin: REOPEN gate met when capture-vs-claimed-topic mismatch fired twice (2026-05-27 reflection event-date miss + a prior occurrence — per `memory/feedback_silent_gap_filling_on_screenshot_parsing` family). Phase E source: C3-S5 / N2 (5/21 audit Build C, never built).

**Composes with:**
- Step 4.5 date-anchor check — together these are the two gates protecting routing-claim accuracy (date + topic)
- `[[feedback_pulled_corpus_must_match_claimed_topic]]` — the rule this gate implements
- `[[feedback_default_to_canonical_spelling_when_memory_flags_wispr_rendering]]` — explains why option (c) above exists

### Step 5: Apply or route

**Apply (Case A or "use now"):** Use the transcript as input to the active workflow. Quote the relevant phrases when scaffolding so Nick can verify Claude understood his voice.

**Route (Case B or "route to inbox"):** Write to `data/inbox.md` **through the locked
writer, never a raw Write/Edit** — one call per dictation chunk:

```bash
PYTHONIOENCODING=utf-8 python3 \
  ~/Documents/Obsidian/30-projects/job-search/tools/inbox_lock.py prepend \
  --inbox data/inbox.md --stdin <<'BLOCK'
<the entry below>
BLOCK
```

A raw Write cannot hold the lock across its read-think-write cycle and can silently
revert a concurrent write from the launchd collectors. Entry shape:

```
## YYYY-MM-DD | [derived label from content]

[The dictated content, verbatim — no rewriting]
```

Confirm one line: "Saved N dictation(s) to data/inbox.md."

**Route to reflections (Case A1: substantive monologue):** When a dictation is a long-form rumble (>200 words of unguarded thinking, "let me get this out" framing, contains personal/strategic processing rather than task-context), route to a dated reflection file `YYYY-MM-DD-<topic>.md`. This invokes the two-tier capture pattern per `framework/two-tier-capture.md`.

**Synthesis-destination test — pick which `reflections/` folder.** Per `framework/personal-vs-job-os-architecture.md` (architecture decision 2026-05-04), there are two reflection homes:

- `data/reflections/` (job-search project) — when the rumble's *synthesis destination* is job-search work: conviction-workbook, professional-identity, projects/zuora, goals, company-notes, networking, interview prep, AI-fluency narrative, recruiter conversations.
- `<personal-vault>/data/reflections/` — when the synthesis destination is personal-OS: practice-log, garden-log, gratitude practice, fatherhood prep, relationship, household, finances, identity work that is purely personal (not feeding professional-identity).

The test is *destination, not topic*. A rumble that processes job-search ideas through a personal frame (e.g., "habits / asking for help → I can do outreach") is job-search because the routing destination is job-search action. A rumble about gratitude / fatherhood with no professional throughline is personal.

When in doubt, default to job-search/data/reflections/ and flag the question. Cross-reflection wiki-links work both ways since basenames are unique within the vault.

**MANDATORY frontmatter** (per `framework/two-tier-capture.md` § "Voice classification labels"). The new reflection file MUST open with:

```yaml
---
voice: pure-voice
source: wispr-flow
captured: YYYY-MM-DD HH:MM
---
```

`voice: pure-voice` is non-negotiable — the file is Nick's verbatim dictation, no agent rewriting. The same label MUST be set on any new file written by this skill: dictation chunks routed verbatim to `data/inbox.md` are also `pure-voice` (no separate frontmatter needed for inbox entries since `data/inbox.md` is one file; if substantive enough to break out into its own file, frontmatter applies).

The new reflection file MUST also include `[[wiki-links]]` to:
- Related prior reflections (e.g., `[[2026-04-27-zuora-closure]]`)
- Synthesis destinations the content informs (e.g., `[[projects/zuora]]`, `[[conviction-workbook]]`)
- The two-tier capture principle itself: `[[two-tier-capture]]`
- Style rule reference if sensitive names are mentioned: `[[style-guidelines]]`

Disambiguate any filename that exists in multiple folders (e.g., `[[projects/zuora]]` since `zuora.md` exists in both `data/projects/` and `data/company-notes/`). Skip wiki-links for sealed `data/project-background/` files.

**Route to a voice-pure living log (garden / practice / coffee / farmers-market).** When a chunk is a dated entry for one of these logs, DO NOT Write/Edit/MultiEdit the log file directly — a PreToolUse hook (`tools/check_living_log_purity.py`) blocks that. Append via the sanctioned deterministic script, one invocation per labeled entry:

```bash
PYTHONIOENCODING=utf-8 python3 tools/living_log_append.py \
    <garden|practice|coffee|farmers-market> <YYYY-MM-DD> \
    "<bold label>" "<verbatim chunk text>" [wispr-source-basename]
```

The script is the ONLY sanctioned writer (deterministic, verbatim — it never paraphrases; it preserves the file's newline style and writes atomically). Run one invocation per entry. Do not batch a Write with a consuming Bash call — sequential only (per `feedback_no_batch_write_then_consume`).

### Step 6: Don't double-pull

`wispr_pull.py` advances its state cursor automatically after a real (non-dry-run) pull. Subsequent `/wispr` calls only see new content. Don't re-run for the same content unless user explicitly asks (`/wispr all` overrides the cursor).

## Edge cases

- **DB not found:** Tell user the path checked (`~/Library/Application Support/Wispr Flow/flow.sqlite`) and ask if Wispr Flow is installed/running.
- **All chunks low-signal** (test/empty/file-uri): script auto-skips those. Tell user "Pulled N chunks, all filtered as low-signal (test/empty/etc.). Try `/wispr all` if you think real content was missed."
- **Mixed relevance:** if some chunks clearly belong in the active workflow and others are unrelated captures, propose a split: "Chunks 1 and 3 are about Casey — feeding into the thank-you. Chunk 2 looks like a separate capture — route to inbox?"
- **Nick said he'd dictate but pull returns nothing:** check if Wispr Flow is open and synced. The DB only updates when Wispr's local app sees the dictation. Suggest manually checking the Wispr app, or widening the window.
- **Cross-device dictation:** Wispr syncs phone + desktop. Phone notes typically arrive within seconds via cloud. If Nick dictated on phone and the pull is empty, sync may be lagging — wait 10–20 seconds, retry.
- **Edited Wispr notes don't re-import:** if Nick edits a previously-pulled Note in Wispr Flow, the edit isn't picked up by default (state's `imported_ids` blocks it). To re-pull an edited note: delete the file in `~/Documents/Obsidian/00-voice-corpus-archive/` and run `/wispr all`. Rare in practice — Wispr notes are typically write-once.

## Voice-corpus discipline (downstream-saver rule)

Wispr captures are voice-corpus material. Nick's intentional dictations — at the desk, on a walk, after a call — are the cleanest record of how he thinks when speaking freely. Long-term reference for voice extraction (`tools/voice_extract.py` corpus), narrative pattern detection, framing rehearsals, and "what did I actually say" lookup. They MUST be reachable in the Obsidian vault graph.

**Rule for any downstream skill or human action that writes a Wispr-derived artifact (or an artifact informed by a Wispr capture) to disk:**

1. **The raw vault archive is preserved by the script.** `~/Documents/Obsidian/00-voice-corpus-archive/wispr-*.md` is the canonical voice-pure tier. Never edit those files in place. Frontmatter `voice: self`, `source: wispr-flow` marks them as voice-pure for any downstream tooling.
2. **When routing to `data/reflections/`** (Case A1 above): the new dated reflection file MUST include the `[[wiki-links]]` listed in Step 5. This is the linkage from raw Wispr → vault graph.
3. **When applying mid-task** (Case A): the resulting artifact (CV bullet, outreach packet, follow-up note, project Learnings entry) should cite the source rumble with a wiki-link to the dated reflection if one was created, or to the source `wispr-*.md` filename if the rumble stayed at vault inbox level.
4. **When routing to `data/inbox.md`** (Case B): inbox entries are short. No wiki-link required if the capture is small (< 50 words). For substantive multi-paragraph inbox entries, add a wiki-link footer pointing to related project files or `[[two-tier-capture]]`.
5. **Disambiguate filenames** that exist in multiple folders (e.g., `[[projects/zuora]]` vs `[[company-notes/zuora]]`).
6. **Skip wiki-links** for `data/project-background/` files (sealed by design).
7. **Explicit-instruction rule:** when a Wispr chunk explicitly says "add this thought to X", "queue this up", "put this in the workbook", "add a to-do for X", or any other directive that converts the rumble into an action against another file — the destination artifact MUST include a `(Source: [[wispr-YYYY-MM-DD-HHMMSS-slug]], Wispr HH:MM.)` footer pointing back to the source vault file. This applies to inbox entries, workbook addenda, project-file updates, conviction docs, etc. Rationale: the explicit instruction is high-signal voice corpus — the linkage lets future-Nick (or downstream skills) trace the synthesized version back to the moment of intent.

The principle: the moment a Wispr capture leaves the 00-voice-corpus-archive archive and lands somewhere referenced (reflection, project file, output artifact), the wiki-link discipline kicks in. The graph connects the voice corpus to wherever it informed work.

## Behavior notes

- **Voice purity:** The script reads only the `Notes` table (intentional captures), never `History` (raw dictation noise). Transcripts surfaced in chat are faithful to what Nick spoke.
- **Vault-first:** Files go to `~/Documents/Obsidian/00-voice-corpus-archive/` (Obsidian vault). The project's `data/inbox.md` only gets entries when Step 5 routes them. Voice archive lives in the vault; project-relevant captures live in the project.
- **No agent rewriting of voice content.** Transcripts surface verbatim. When applying to a task (Case A), Claude scaffolds *around* Nick's voice, never replaces it.
- **State file:** `tools/.wispr-state.json` tracks the last-imported timestamp + a list of imported note IDs (capped at 500). Don't manually edit unless re-pull is needed.

## Examples

### Example 1: Mid-task dictation (Case A)

```
Nick: I'll dictate context for the Zuora thank-yous, give me a few minutes.
[Nick steps away, dictates into Wispr Flow]
Nick: I'm back / I'm done

Claude: [invokes /wispr, runs pull --print]
Wispr — 4 dictations since 09:43:

— 09:55 | About Casey
[verbatim transcript]

— 09:58 | About Jordan
[verbatim transcript]

— 10:01 | About Riley
[verbatim transcript]

— 10:04 | About Morgan
[verbatim transcript]

I have context for Casey, Jordan, Riley, and Morgan. Starting with Casey's thank-you draft now (lowest friction). Jordan's note will be last given the weight you flagged.

[scaffolds Dana draft]
```

### Example 2: Standalone capture (Case B)

```
Nick: /wispr

Claude: [pull --print, gets 2 chunks]
Wispr — 2 dictations:

— 11:20 | Read Lenny on growth-stage ops
[transcript]

— 11:32 | Push back on the recruiter about stage
[transcript]

These look like captures, not active-task input. Use now, route to data/inbox.md, or both?

Nick: route both

Claude: [appends both to data/inbox.md, confirms]
Saved 2 dictations to data/inbox.md.
```

### Example 3: Empty pull

```
Nick: I just dictated, pull it

Claude: [pull --print, 0 found]
No new dictations since last pull (cursor at 11:32). Want me to widen — try `/wispr 30m` or `/wispr 2h`?

Nick: /wispr 30m

Claude: [pull --since 30m --print, gets the missed chunk]
Found it — Wispr was lagging on sync. Here's what landed:

— 11:48 | About Jordan
[transcript]

[applies to thank-you workflow]
```

### Example 4: Mixed chunks (proposed split)

```
Nick: I'm done dictating

Claude: [pull --print, gets 3 chunks]
Wispr — 3 dictations:

— 14:10 | Jordan thank-you context
[transcript about Sam]

— 14:14 | Pipeline thoughts
[transcript about how stage line might shift]

— 14:18 | ActiveCo reactivation
[transcript with prior-conversation details]

Proposed split:
- Chunk 1 → feed into Sam thank-you draft (active task)
- Chunks 2 + 3 → route to data/inbox.md (capture for later)

Sound right?
```

## What this command IS NOT

- Not a transcription service (Wispr does that locally)
- Not voice synthesis (Claude doesn't speak back)
- Not a real-time stream (poll-based, user-triggered)
- Not auto-applied — Nick signals when to pull; Claude decides apply vs. route based on context
- Not a replacement for `/remember` — `/remember` is typed; `/wispr` is voice. They route to the same inbox when capture is the intent.

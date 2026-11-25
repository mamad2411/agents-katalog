---
name: draft-email
description: Draft job-search emails — thank-you notes, status updates, intro requests, expressions of interest
argument-hint: <recipient> <purpose> [context]
user-invocable: true
allowed-tools: Read(*), Glob(data/*), Grep(data/*), Edit(data/networking.md), Write(data/networking.md), Write(data/job-todos.md), Write(tools/.pending-draft.txt), Write(tools/.pending-draft.source), Edit(data/outreach-log.md), Write(data/outreach-log.md), Write(output/**), Edit(framework/style-guidelines.md), Write(memory/lessons.md)
---

# Draft Email — General-Purpose Job Search Emails

Draft thank-you notes, status updates, intro requests, expressions of interest, and informational interview requests. Auto-detects the email type from the purpose, pulls relevant context from data files, and offers to log to networking.

Use `/cold-outreach` for first-contact messages to strangers. Use `/follow-up` for re-engaging existing contacts. Use `/draft-email` for everything else.

## Arguments

- `$ARGUMENTS` (required): At minimum a recipient and purpose.
  - **Recipient** (required): Name of the person (quoted if multi-word)
  - **Purpose** (required): What the email is for (quoted string or remaining text)
  - **Context** (optional): Additional details — what happened, what to reference

Examples:
- `/draft-email "Sarah Chen" "thank you for coffee chat"`
- `/draft-email "Pat" "update on my job search"`
- `/draft-email "Jordan Lee" "ask for intro to Acme AI CEO"`
- `/draft-email "Lisa Park" "interested in the CoS role at Notion"`
- `/draft-email "James Liu" "informational interview about PM at Stripe"`

If no arguments provided, display usage:
```
Usage: /draft-email <recipient> <purpose> [context]

Email types (auto-detected from purpose):
  Thank-you    — "thank you for coffee chat"
  Update       — "update on my job search"
  Intro request — "ask for intro to [person/company]"
  Interest     — "interested in [role] at [company]"
  Informational — "informational interview about [topic]"

Examples:
  /draft-email "Sarah Chen" "thank you for interview yesterday"
  /draft-email "Pat" "update on my search, landed two interviews"
  /draft-email "Jordan Lee" "intro to Acme AI CEO"
```

## Instructions

### Step 0: Lessons Promotion Check

Before drafting, surface any accumulated voice patterns ready to be canonized:

1. Read `memory/lessons.md`.
2. Scan Section 2 for rows where **Occurrences ≥ 2** AND **Promoted = No**.
3. If none found, skip silently and proceed to Step 1.
4. If any found, surface them before proceeding:
   ```
   [N] outreach rule(s) ready to add to your Nick's Voice guidelines:

   1. Pattern: [pattern text]
      Rule: [rule text]
      Occurrences: [N]

   Promote to style-guidelines.md now? (Y / N)
   ```
5. **If approved (Y):** For each rule, promote by LAYER per the `memory/lessons.md` Section 2 loop (indexed in `framework/style-guidelines.md`): **voice mechanics** → `framework/voice-reference.md` §3; **drafting judgment** (what to say/cut/position per audience) → `framework/content-rules.yaml` + its `content-rules.md` index, applying the C1 generalizability gate; **CV/format** → `framework/style-guidelines.md`. Then update the lessons.md row: set Promoted = Yes.
6. **If declined (N):** skip and proceed. Rules remain in lessons.md for next time.

---

### Step 1: Parse Arguments

Parse `$ARGUMENTS` into components:

1. **Recipient** (required): First quoted string or first word(s) that look like a name.
2. **Purpose** (required): Next quoted string or remaining text describing the email's purpose.
3. **Context** (optional): Any additional text after the purpose.

### Step 2: Auto-Detect Email Type

Match the purpose string against keywords to determine the email type:

| Type | Keywords | Priority |
|------|----------|----------|
| **Thank-you** | "thank", "thanks", "grateful", "appreciated", "great meeting" | 1 |
| **Intro request** | "intro", "introduce", "connect me", "introduction", "put me in touch" | 2 |
| **Status update** | "update", "news", "progress", "let know", "share what" | 3 |
| **Interest** | "interest", "apply", "role", "position", "opportunity", "opening" | 4 |
| **Informational** | "informational", "learn more", "perspective", "advice", "pick your brain" | 5 |
| **General** | No match | 6 |

If the type is **General**, ask the user to clarify:
```
I'm not sure what type of email this is. Could you clarify?
- Thank-you note
- Status update to your network
- Intro request (asking someone to connect you)
- Expression of interest in a role
- Informational interview request
- Something else (describe it)
```

### Step 3: Load Context

**Voice-critical reads (always load):**

1. `data/networking.md` — existing contact info and prior interactions with the recipient (load-bearing for tone match to this specific person)
1b. `data/people/<slug>.md` (if present; slug = recipient name lowercased, accents folded, spaces→hyphens) — the synthesized relationship dossier: what they committed to, what Nick owes them, pressure points, next move. Richer than the raw log when it exists.
2. `framework/style-guidelines.md` — Nick's Voice patterns for tone matching (see "Nick's Voice — Outreach & Email" section)
3. `framework/voice-reference.md` — see item 6 below; this is the single most load-bearing voice read

**Content reads (skip when conversation already has them loaded):**

Mid-session, Nick's profile and identity context is usually already in the conversation from a prior skill invocation (`/standup`, `/apply`, `/prep-interview`, etc.). Skip these reads in that case. If invoked at session start with no prior context, load them.

4. `data/profile.md` — sender background
5. `data/professional-identity.md` — strengths, values

**Reference reads:**

6. `framework/voice-reference.md` — **EMPIRICAL voice reference extracted from labeled corpus.** Contains validated rules + verbatim exemplars. **MUST read both the rules AND the exemplars sections — research finding: rules alone underperform; rules + 2-3 exemplars beats both.** Match the relevant exemplar to email type (cold outreach, post-call thank-you, follow-up nudge, application follow-up, logistics/rescheduling). **The matched exemplar is the generative spine for Step 5: you draft by adapting it to this recipient, NOT by filling the per-type structure with fresh prose. The Step 5 structure is a constraint check on the adapted exemplar, never the starting point. If the exemplar isn't doing the work, the draft will read generic.**
7. `framework/content-rules.md` — **DRAFTING-JUDGMENT index** (what to say / cut / position per audience — distinct from voice mechanics). Not conditionally skippable (unlike items 4-5): it is voice-critical, not positioning-detail. The **active** rules are the pre-send checklist run in the Step 6 Content-Rules Pass; reference-only rules (in `content-rules.yaml`) inform what to include and cut. Rule-gate to what applies to THIS type/recipient (a thank-you selects `B1`/`B3`/`H1`/`H3`; a status/channel update selects `D2`/`E1`; a decline selects `H8`; etc.) — don't apply all rules blindly.

> **Experiment in progress (2026-05-13):** items 4-5 are conditionally skipped per the "context-hot" rule above. Rollback criterion: if a draft is missing positioning/fit details that should have come from profile.md or professional-identity.md, revert this section to unconditional loading. Logged in `memory/lessons.md` row 62.

`framework/outreach-guide.md` is NOT loaded per-email — mechanical anti-patterns are caught by the `check_draft_voice.py` PreToolUse hook; tonal quality (polished / generic / off-register) is gated by the Step 6 tonal self-check. Length and structure constraints live in Step 5.

**Type-specific context loading:**

- **Status update:** Also read `data/job-pipeline.md`, `data/job-todos.md`, `data/job-todos-daily-log.md`
- **Intro request:** Also read company dossier if target company is identifiable — `output/<slug>/<slug>.md`
- **Interest:** Also read company dossier (`output/<slug>/<slug>.md`) and `data/job-pipeline.md`
- **Informational:** Also read company dossier (`output/<slug>/<slug>.md`)

### Step 4: Tone Matching

**Tone-match calibration chain — try in order, stop at first hit. Track which source was used; it goes in the Quality Check block (Step 6).**

**1. `networking.md` blockquoted bodies (highest fidelity).** Read the recipient's Interaction Log section. If any prior interactions include the full message body in blockquote format (`> Body text...`), use those for tone matching. This is the canonical source.

**2. Archive file fallback.** If no blockquoted body found in `networking.md`, glob `output/*/*-{draft-email,cold-outreach,follow-up}-<recipient-slug>.md` and read the most recent archive file (sort by date prefix `MMDDYY`). Archives always include the full draft body. Recipient slug = full name lowercased with hyphens (e.g., "Jordan Lee" → `jordan-lee`).

**3. Voice-reference exemplar fallback (lowest fidelity).** If neither `networking.md` nor archive files contain a prior body for this contact, fall back to the matching exemplar in `framework/voice-reference.md` for the email type (cold outreach, post-call thank-you, follow-up nudge, application follow-up, logistics/rescheduling). **MUST surface this as "Tone calibration: voice-reference exemplar (no prior body found)" in Step 6.** This is a yellow flag — substantive tonal misses (condescending lines, awkward phrasing, peer-relationship misreads) often slip through when calibration is type-generic, since the voice hook only catches mechanical anti-patterns. Draft with extra care; re-read each sentence asking "would this read as patronizing / hedging / misaligned to a peer who's seen my other replies?"

**Relationship type:** regardless of which source is used, note the relationship (recruiter, peer-operator, mentor, hiring-manager, referral) from `networking.md` for formality calibration.

**Recipient not in `data/networking.md`:** default to source #3 (voice-reference exemplar), note "Recipient not found in contacts — using voice-reference exemplar only."

### Step 4b: Voice-Pure Dictation Mode (when Nick provides a guide)

**Trigger:** Nick passes a voice-pure dictation guide via argument or earlier in the conversation (e.g., "use this as the spine: '<his dictated sentences>'"), OR he signals he'll author the substance himself ("give me the spine," "I want to put it in my words," "I'll write it myself"). In the latter case, give him structure + key points + raw hook material — NOT a finished, polished message — and do NOT run the full Step 5-8 draft flow. Escalate to a full draft only if he explicitly asks for one ("put a draft together"). See `memory/feedback_give_nick_beats_not_a_polished_script.md`.

**Rule:** The polished output's diff from the guide must be **mechanical only**:
- Grammar errors → fix
- Punctuation → add/correct
- Wispr homophones with context-obvious meaning → silent-correct + note inline (per `memory/feedback_dont_speculatively_change_voice_transcript_names.md` Extension 2026-05-13)
- Sentence-boundary cleanup → fix

**Banned during voice-pure polish:**
- Adding new sentences (no "while we're on it," no "also," no transitions Nick didn't include)
- Adding qualitative adjectives ("solid concept," "really cool")
- Adding feature-list descriptors when products are named
- Adding volume estimates, numbers, or specifics Nick didn't include
- Adding a second ask when Nick included one
- Adding URLs to product docs (especially if recipient works at the company — see `memory/feedback_no_product_docs_to_employees.md`)
- Reorganizing structure beyond the dictation

**Pre-present check:** diff the polished draft against the guide. If the diff includes new content (not just mechanical fixes), revise to cut.

If something seems missing (a URL, a number, a transition), **pause and ask Nick** before adding. Do not infer.

See `memory/feedback_voice_pure_diff_minimal.md` and `memory/feedback_minimize_polish_on_voice_pure_dictation.md`.

### Step 4c: Reply-Mode Source Grounding (mandatory when replying to a specific received message)

**Fires when:** the email is a *reply* to a specific message the recipient sent (subject starts "Re:", or the trigger was "reply to their email" / "reply to this thread"). Skip for new (non-reply) emails.

**This step exists because:** the highest-frequency cause of multi-spin reply churn is drafting from a *self-summary* of the inbound instead of the verbatim source — which silently carries mis-assigned attributes (which thing they said about which entity) and invented positioning claims. "Quick / ASAP" makes this MORE important, not skippable. Origin: 2026-06-15 recruiter-reply incident, 7 versions. See `memory/feedback_ground_email_draft_in_verbatim_source_not_paraphrase.md`.

1. **Pull the verbatim inbound.** If not already in context, fetch it: `tools/gmail_fetch.py --all-mail --search "<query>" --body`. **Check the `Mailbox:` line on each hit** — `--all-mail` includes DRAFTS, and a draft is shaped exactly like a sent message, so an unsent draft can be mistaken for a real inbound or a real send (2026-09-02). Read it line by line — do NOT work from a summary. **`<query>` must be a real non-empty query** (`from:`, `subject:`, a name). An empty one exits 2 by design since 2026-08-19: there is no empty-query listing mode, and before the guard it fell through to a SYNC that wrote to `inbox/`. To browse rather than search, use `--backfill --label-id <ID> --max N --dry-run`.
2. **Build a claim→source map (working notes, not the email).** For every substantive sentence the draft will make about the sender's message — per entity/role — quote the verbatim line it grounds in. Any claim with no source line is invented: cut it, recast it, or ask Nick.
3. **Cross-assignment check:** verify each attribute is attached to the entity the sender attached it to.
4. **Mirror their framing where agreeing:** echo the sender's own structure/words where Nick is agreeing with their read.
5. **Record any delivery signal in the thread, immediately.** If the inbound shows a bounce, a delivery receipt, or an explicit "I never got it" / "can you resend", write it to the outreach log before drafting:
   ```
   PYTHONIOENCODING=utf-8 python3 tools/outreach_status.py --set-status \
     --recipient "<name>" --date YYYY-MM-DD --artifact <token> --status <Bounced|Delivered>
   ```
   The `--date` is the date of the row being corrected, not today. An **unrecorded bounce is what produced the 2026-08-10 suppressive-claim defect**: the log still read `Sent`, so a later prep doc concluded the CV had arrived and told Nick not to re-offer it.

### Step 5: Draft by Email Type

**Generate FROM the exemplar, not from the structure below.** Step 4 selected a tone source; Step 3 loaded the matched `voice-reference.md` exemplar. Draft by adapting that exemplar (and any prior-body tone source from Step 4) to this recipient and purpose. The per-type blocks below are **constraint checks, not fill-in templates**: they specify length, bullet count, CTA count, and what each block must accomplish — they do NOT supply phrasings. Any quoted text in them is a *spec of intent*, never a sentence to paste or lightly reword. If the draft could have been written for any candidate, the exemplar didn't drive it — restart from the exemplar, do not patch.

**Subject lines (all types):** never a clever or topic-synthesized hook. Follow `voice-reference.md` subject canon — plain, warm, functional ("Thanks for today"). The per-type subject notes below defer to this.

---

#### Thank-You

**Timing:** Within 2–24 hours of the interaction (80% of hiring managers say it influences decisions; only 24% of candidates send one).

**Length:**
- Formal interview: 100–150 words
- Coffee chat / informational: 75–100 words

**Structure:**
1. **Thank for time** (1 sentence) — be specific about what you met about
2. **Specific callback** (1–2 sentences) — reference a particular discussion point that resonated
3. **Connect to your experience** (1 sentence) — briefly link what you discussed to your background
4. **Express continued interest** (1 sentence) — forward-looking, enthusiastic but not desperate
5. **Gracious close**

**Subject line:** Plain-warm per `voice-reference.md` Exemplar 5 rule 5 — e.g. "Thanks for today" / "Thanks for the time today". The body's synthesized hook is *earned* in the body, never *performed* in the subject. "Thank you — [topic]" / "Great meeting you, [Name]" are banned: they read as templated. For CEO/founder post-call thank-yous, Exemplar 5's four rules are load-bearing — apply them.

**No follow-up to-do created** — thank-you emails are one-shot.

---

#### Status Update

**When to use:** Sharing progress with mentors, peers, or your network. Keeps contacts engaged and top-of-mind.

**Data to pull:**
- `data/job-pipeline.md` — active applications and stages
- `data/job-todos.md` — recent completions
- `data/job-todos-daily-log.md` — recent progress snapshots

**Length:** 100–125 words

**Structure:**
1. **Warm opener** (1 sentence) — reference last conversation or connection
2. **Progress bullets** (3–5 bullets) — scannable, concrete updates
3. **What you're looking for** (1 sentence) — specific and actionable ("CoS roles at Series B–C healthtech companies" not "exploring opportunities")
4. **Reciprocal offer or specific ask** (1 sentence) — not vague "keep me in mind"
5. **Close**

**Subject line:** "Quick update — [your name]" or "[Name], job search update"

**Follow-up to-do:** Created with 30-day due date to send next update.

---

#### Intro Request

**Technique:** Use the **forwardable email technique** — write a request to the connector PLUS a self-contained blurb they can forward unchanged.

**Structure:**
1. **Ask to the connector** (2–3 sentences):
   - Reference your relationship
   - Use **double opt-in framing** (ask the connector to check willingness before assuming a forward) — phrased in Nick's voice per the matched exemplar, not from a canned line
   - Never assume they'll forward without asking
2. **Line break**
3. **Forwardable blurb** (under 100 words):
   - Who you are (1 sentence — impact, not title)
   - Why this company/person specifically (1 sentence — shows research)
   - What you're looking for (1 sentence — specific ask)
   - LinkedIn URL
   - Low-pressure closing ("Happy to share more context if helpful")

**Subject line:** "Would you intro me to [target name]?" or "Quick ask — [target company]"

**Follow-up to-do:** Created with 7-day due date to check if connector responded.

---

#### Interest / Application

**When to use:** Expressing interest in a specific role, usually to someone at the company (not a formal application portal).

**Length:** Under 125 words

**Structure:**
1. **Connection hook** (1 sentence) — how you found the role or why you're reaching out to them
2. **Fit points** (2–3 bullets) — specific experience that maps to the role requirements
3. **Specific ask** (1 sentence) — exactly one ask, in Nick's voice per the matched exemplar; see `voice-reference.md` ask patterns (`I'd love to...`, specific not generic). Do not paste a canned ask.
4. **Close** — per `voice-reference.md` closer canon (`Best,` / `Thanks,` + bare `Nick`)

**Do NOT attach resume** — offer to send if interested. Unsolicited attachments reduce response rates.

**Subject line:** Plain per the Step 5 subject rule (Re: prefix preserved when replying to an existing thread).

**Follow-up to-do:** Created with 7-day due date.

---

#### Informational Interview Request

**When to use:** Requesting time to learn about someone's role, company, or industry. Assumes some connection exists (mutual contact, alumni, met at event).

**Length:** 75–100 words

**Structure:**
1. **Connection reference** (1 sentence) — how you know them or why you're reaching out
2. **Specific topic interest** (1 sentence) — what you want to learn about (not vague "your career")
3. **Low-commitment ask** (1 sentence) — a specific, small time ask in Nick's voice per the matched exemplar
4. **Warm forward close** — warm and forward-looking, NOT an apology-for-asking or hedge. "Totally understand if timing doesn't work" / "No rush, whenever is convenient" are **banned** (deferential ≠ hedgy — `voice-reference.md` Exemplar 5 rule 4, 2026-05-18 refinement)

**Subject line:** Plain per the Step 5 subject rule — not a clever hook.

**Follow-up to-do:** Created with 7-day due date.

---

#### General

If the email type doesn't match any category above:

1. Ask the user for more context about the purpose.
2. Draft based on the outreach guide's general principles: concise, one CTA, no anti-patterns.
3. Follow standard metrics: the length for the closest row of the Channel Constraints table in `framework/outreach-guide.md` (50–150 words for a reply or follow-up; a cold first contact belongs in `/cold-outreach`, at 200–300), clear subject line, no filler.

---

### Step 5b: Substance-Provenance Audit (mandatory)

**Before this step, apply `framework/writing-discipline.md`.** It is canonical for the four provenance labels (`N` / `C` / `I` / `G`), what counts as a substantive sentence, the audit output format, and the invariant that `G` is blocked in any slot carrying a claim about who Nick is, what he brings, what he wants, or what he has done. **This step adds only the slot table below.** Do not restate the labels here; if they need to change, change them there.

Label the provenance of every substantive sentence before the quality check.

**Substantive sentences in an email:** opener / ask / value-prop / bridge sentence / story beat / closing CTA. Logistical sentences ("Wednesday at 2pm works," "I'll send the deck Friday") are not substantive; skip them.

**Audit rule (slot table for this artifact):**

| Slot | G allowed? | If G found |
|---|---|---|
| Self-positioning (who Nick is, what he brings, what he wants) | **No** | STOP. Ask Nick to dictate that slot. |
| Bridge sentence (linking recipient's situation to Nick's offer) | **No** | STOP. Ask Nick for the link or extract from corpus. |
| Story / anecdote | **No** | STOP. Ask Nick for the actual story or pull from prior sent corpus. |
| Opener referencing recipient's work / product / strategy | **No** | STOP. Either it's `I` with a citable source, or it's speculation - replace with corpus-grounded line. |
| Logistics / scheduling / standard pleasantries | Yes | Proceed. |
| Sign-off | Yes | Proceed. |

If any `G` blocks fire, return to Step 4b (dictation mode) and request the spine for those slots. Do not proceed to Step 6 with `G` in any blocked slot. Trace every `I` to its source before Step 6.

### Step 6: Quality Check

Run a focused quality check:

- **Length:** Verify word count is within target range for the email type.
- **CTA count:** Exactly 1 (except thank-you / decline emails, which may have zero).
- **Tone:** Matches the sender's established voice (or defaults to professional peer-to-peer).

**Tonal self-check (mandatory — the hook cannot catch this).** `check_draft_voice.py` is mechanical-only; nothing else gates voice fidelity, so this is the only thing standing between a generic draft and Nick. Read the draft cold against the matched `voice-reference.md` exemplar and answer three questions honestly:

1. **Too polished / not human?** Does it read smoother and more balanced than the exemplar — corporate copy rather than Nick typing fast?
2. **Generic / could be anyone?** Strip the proper nouns: would an ex-colleague read it and think "yeah, that's Nick," or could it have been written for any candidate? (the ex-colleague readability bar)
3. **Off register vs the exemplar?** Right content, wrong temperature — warmer/more eager, stiffer, or more hedged than the matched exemplar?

If any answer is bad, the exemplar didn't drive the draft. **Regenerate from the exemplar — do not patch sentence-by-sentence** (patching preserves the generic skeleton, which is the actual failure). Present only once all three pass.

Anti-pattern scanning is **not** done in-skill anymore — the `check_draft_voice.py` PreToolUse hook gates the draft against the full mechanical anti-pattern set (filler adverbs, em dashes, semicolons, "just wanted to," "circling back," "just checking in," stacked "really") before `open_draft.py` runs. Trust the hook for mechanical issues; trust the tonal self-check above for voice fidelity.

**Content-Rules Pass (mandatory — voice hook is mechanical; this is the judgment layer).** Load `framework/content-rules.md`. **Rule-gate:** select only the active rules whose trigger applies to THIS email type/recipient — don't walk all rules. Check the draft against each selected rule and record a one-line verdict in the Content-rules row of the Step 7 block. Advisory: you surface hits, Nick decides; nothing blocks. Run it every time — a silent skip is the `[[feedback_llm_self_policing_fails]]` failure this pass exists to prevent. (Rule `G1` "shape of role" is also hook-enforced.)

**Quality gate (for Intro Request, Interest, and Informational types only — skip for Thank-you and Status Update):**

Answer each question with a specific one-sentence response:
1. **"Why you?"** — Why this specific recipient? (must reference something specific to the person, not just their title or company)
2. **"Why now?"** — What makes this timely? (a trigger event, a connection, a recent development)
3. **"Why me?"** — What establishes the sender's credibility for this ask? (a specific achievement or experience, not generic)

If any answer is weak or generic, revise the draft before presenting. Show the answers in the output.

If any check fails, revise before presenting.

### Step 7: Present Draft

```markdown
## Email Draft — [Type] to [Recipient]

**Type:** [Thank-you / Update / Intro Request / Interest / Informational / General]
**Tone:** [Matched to prior messages / Default professional]

### Subject Line
[subject line]

### Message
[the draft message]

---

**Quality Check:**
- Word count: [N] (target: [range for this type])
- CTA: [Single / Multiple — fix]
- Tone calibration: [networking.md blockquote / archive: `output/<slug>/<file>.md` / voice-reference exemplar (no prior body found)]
- Content-rules pass: [rules checked: B1, H3... → `ok`, or rule-id + what fired]
- Anti-patterns: gated by `check_draft_voice.py` hook (not scanned in-skill)

[For Intro Request, Interest, and Informational types only:]
**Quality Gate:**
- **Why you?** [one-sentence specific answer]
- **Why now?** [one-sentence specific answer]
- **Why me?** [one-sentence specific answer]

---
[If recipient is in networking.md]: Want me to log this interaction? (Y/N)
[If recipient is NOT in networking.md]: Want me to add [Name] as a contact and log this? (Y/N)
```

**After presenting the draft**, immediately write `tools/.pending-draft.txt` with this format (overwriting any previous draft):

```
TO:
SUBJECT: [subject line]
ATTACH: [optional absolute path — omit line entirely if no attachment]
BODY:
[full message text]
```

`ATTACH:` is optional. Include it only when the email genuinely needs a file (CV, cover letter PDF, portfolio doc) and the recipient asked for it or it is the main artifact of the message. Default behavior remains: do NOT attach a resume on cold outreach unless the recipient asked. When included, `open_draft.py` copies the file to the macOS clipboard so Cmd+V in the Gmail compose window attaches it.

**Immediately after writing `.pending-draft.txt`, also write `tools/.pending-draft.source`** with two lines:

```
draft-email
<ISO 8601 timestamp, e.g. 2026-05-13T15:30:42>
```

This marker is read by the `check_draft_voice.py` PreToolUse hook to verify the draft was produced by a skill (not inline). Without it, the hook blocks `open_draft.py`.

**Write the marker in a SEPARATE Bash call that completes BEFORE the `open_draft.py` call — never chain them with `&&`.** The PreToolUse hook evaluates the whole command string before any of it runs, so `printf … > .pending-draft.source && python3 tools/open_draft.py` is checked against the PREVIOUS marker: if that one is more than five minutes old the call BLOCKs as "stale marker", and if it is fresh the call passes on the previous draft's provenance rather than this one's (corrected 2026-09-23 after cross-model review; `check_draft_voice.py` requires the marker to exist, be readable, have a file modification time no more than five minutes old and no more than ten seconds in the future, and have an allowed skill name on its first line; the ISO timestamp on line two is never read, and the marker is never tied to the current draft). Two calls: (1) refresh the marker, (2) run `open_draft.py`. Same applies to every draft re-open when iterating. Per [[reference_pending_draft_marker_before_open_draft]] (fired 2026-06-22, 2026-07-16, 2026-08-14, 2026-08-19, 2026-09-23; this skill lacked the line until 2026-09-23, `/cold-outreach` had it).

Then automatically run `python3 tools/open_draft.py` using the Bash tool. Show the output from the script to confirm it ran.

**Reply vs. new-email behavior** (handled by `open_draft.py` based on subject):
- **New email** (subject does NOT start with `Re:`): script opens Gmail compose URL with `to`, `subject`, `body` pre-filled.
- **Reply** (subject starts with `Re:`): Gmail compose URL doesn't thread into existing conversations (it opens a new compose with `Re:` prepended), so the script instead `pbcopy`s the body and prints instructions for Nick to open the existing thread and paste. **Drafts of replies must still go through this flow** — the provenance marker and voice hook still gate.

**After opening the draft**, save an archive copy if a company is identifiable from context:
- **If company is known**: save to `output/<company-slug>/MMDDYY-draft-email-<recipient-slug>.md`
  - Company slug = company name, lowercase, spaces→hyphens
  - Recipient slug = recipient's full name, lowercase, spaces→hyphens (e.g., "Jordan Lee" → `jordan-lee`)
  - Date prefix = `MMDDYY` (today's date)
- **If no company is identifiable** (e.g., general network update with no role/company context): save flat as `output/MMDDYY-draft-email-<recipient-slug>.md`

Archive file format:
```markdown
# [Email Type]: [Recipient Name][@ Company if known] — [YYYY-MM-DD]

**Type:** [Thank-you / Update / Intro Request / Interest / Informational / General]
**Recipient:** [Name][, Role if known]
**Company:** [Company Name or "—"]
**Date:** [YYYY-MM-DD]

---

[Full draft text as presented]
```

### Step 8: Auto-Logging (after user approves)

**IMPORTANT — defer auto-log during multi-round edit cycles.** If the draft is being iteratively revised across multiple rounds (Nick is editing the body, you're refreshing the clipboard each round), do NOT write to `networking.md` / `outreach-log.md` until Nick confirms "this is what I sent" or pastes back the final body. Auto-logging the pre-final version creates canonical-record drift and forces a re-edit of `networking.md` every iteration. See `memory/feedback_voice_pure_diff_minimal.md` (companion rule).

**Default behavior** (single-draft, no iteration): auto-log immediately after `open_draft.py` runs, per the steps below.



**If recipient exists in `data/networking.md`:**
1. Log the interaction:
   ```markdown
   #### YYYY-MM-DD | email | [Type] — [1-line summary]

   > [Full message text in blockquote]

   **Follow-up:** [Next action or "—" for thank-you emails]
   ```
2. Update the contact's Last Interaction date.

**If recipient is NOT in `data/networking.md` and user wants to add:**
1. Add contact to the Contacts table (infer company and role from context if possible).
2. Create their Interaction Log section.
3. Log the interaction as above.

**Follow-up to-dos** (all types except thank-you):
- Read `data/job-todos.md`, add:
  - **Task:** `Follow up: [Name] — [action based on email type]`
  - **Priority:** `Med`
  - **Due:** Type-dependent (7 days for intro/interest/informational, 30 days for update)
  - **Status:** `Pending`
  - **Notes:** `From /draft-email on [date]`

**If `data/job-todos.md` doesn't exist**, create it with the standard header before adding.

**Append to `data/outreach-log.md`:**

Read `data/outreach-log.md` (create with the standard header if it doesn't exist). Append a new row to the table:

```
| [YYYY-MM-DD] | draft-email | email | [Name] | [Company or "—"] | [subject line or 1-line summary] | Drafted |
```

Confirm:
```
Logged to networking.md. [Follow-up to-do created — due [date].]
Outreach log updated → data/outreach-log.md
```

## Edge Cases

- **No arguments:** Display usage message with examples and email type reference.
- **Recipient name is ambiguous:** If multiple contacts match in `data/networking.md`, ask user to clarify.
- **Thank-you sent late (>48 hours):** Acknowledge gracefully in the draft — "I wanted to take a moment to properly thank you" rather than apologizing.
- **Status update with no pipeline/todo data:** Draft with whatever information the user provided in context. Note: "No pipeline or to-do data found — consider running `/pipe` and `/todo` first for richer updates."
- **Intro request but no company dossier:** Draft with available context. Suggest `/research-company` for the target company to strengthen the ask.
- **Purpose is unclear / General type:** Ask the user for clarification before drafting.
- **`data/networking.md` doesn't exist:** Skip logging offer, or offer to create the file if user wants to start tracking.

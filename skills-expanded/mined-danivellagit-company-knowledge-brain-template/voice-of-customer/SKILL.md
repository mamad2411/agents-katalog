---
name: voice-of-customer
description: Use to capture what customers and prospects actually said, in their own words, into voice-of-customer/YYYY/MM/<company-slug>_YYYY-MM-DD.md, or to read that corpus and answer a positioning question over it. Triggers on "voice of the customer", "what do customers say", "what did they not understand about us", "how do they describe us", "which alternatives do they name", "pull the quotes from that call", "what do they ask for to trust us", or any request to analyse prospect / customer language on positioning, objections, misunderstandings, or competitors named. Also use before a customer call to read back their own words.
owner:
  - "[[marketing]]"
creator:
  - "[[<person-slug>]]"
audience: [all]
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# voice-of-customer

Capture the customer's own words, and read them back later against a question nobody has asked yet.

Schema and hard rules live in [`voice-of-customer/README.md`](../../voice-of-customer/README.md); this skill executes them. Read that README before the first write of a session.

Two modes. Ask which one if the request is ambiguous.

- **capture** — extract quotes from one interaction (or every external interaction on a date) and write the files.
- **read** — answer a question over the corpus, with a mandatory denominator header.

---

## Mode: capture

### Inputs

- A date (default: yesterday), or a single source (a transcript link, a mail thread, a chat channel + date, a closed-lost CRM record).
- Nothing else. Everything is resolved from the sources.

### Workflow

1. **Find the interactions.** For the target date:
   - **Calls**: transcripts where at least one participant sits outside the company domains. Skip internal-only calls, investor calls, legal / administrative calls, and hiring calls. Partners and vendors are in scope, tagged by `interaction_type`.
   - **Mail**: threads with at least one external participant whose company has a CRM record.
   - **Chat**: shared / external channels only, messages posted by external members only. Sender names often do not render for guest users: resolve them against the channel member list and the user profile, and drop the quote if the id stays unresolved.
   - **Closed-lost**: CRM deals that moved to closed-lost, with the reason field and any note text written by the counterparty.
2. **Resolve the entities.** Company → `companies/<slug>.md`, speakers → `people/<slug>.md`. Run the standard entity-scan ([`canon/operations.md`](../../canon/operations.md) → "Entity-scan discipline"): no match means propose create with the CRM record in pair, never a silent skip and never a silent create.
3. **Read the source in full.** Not the transcript tool's summary, not the email digest. The transcript or the thread body. The summary is exactly the layer this corpus exists to bypass.
4. **Extract, max 8 quotes.** Only sentences spoken or written by an external participant. For each quote keep verbatim text, speaker, timestamp or date, whether they raised it themselves (`raised_by: customer`) or it answers a question of yours (`raised_by: us`), the exchange that produced it, and whether it blocks a decision on their side.
5. **Drop before you guess.** No confident speaker resolution, no quote. Ambiguity between two speakers on the same turn, no quote. Better a thin file than a wrong attribution.
6. **Apply the filters.** Exclusion list in full, no commercial terms, nothing that would embarrass a named person, no internal politics of the customer.
7. **Write the file** at `voice-of-customer/YYYY/MM/<company-slug>_YYYY-MM-DD.md` (`-2` suffix for a second interaction the same day), to the schema in the README: frontmatter, then the eight fixed sections in order, `none` where empty. Section headings in English, quotes and their `Context:` line in the original language. If the file already exists, stop and ask; never overwrite.
8. **Named-entity sweep. Be obsessive about this, it is the step that gets skipped.** See "Linking" below. An unlinked competitor is a broken file, not a stylistic miss.
9. **Link the themes both ways.** `related_to_themes` forward, and the reverse `themes/<theme>.md → voice_of_customer:` in the same write. All other edges (`related_to_companies`, `related_to_people`, `related_to_products`, `related_to_systems`) are forward-only, exactly like signals.
10. **Report**: interactions processed, quotes kept, quotes dropped and why, interactions skipped and why (no transcript, silent meeting, internal only), entities created, **and every entity linked**.

---

### Linking, the obsessive pass

A customer naming a competitor is the single highest-value fact this corpus captures. It is worth more than the objection, more than the pain point, because it is the only place you learn what you are actually being compared to. **If a product, tool, platform, marketplace or brand is named anywhere in the file and is not wired as an edge, the file is wrong and gets fixed before it is committed.** Under-linking is the default failure here. Bias hard toward the link.

**Where the links go.** Never inside a quote: quotes are immutable verbatim, you do not touch a single character. Links go in two places only:

- **Frontmatter**, the machine-readable edge. `related_to_systems:` is the slot for tools and platforms (anything software). `related_to_companies:` is the slot for real companies: the customer, competitors of theirs, agencies and integrators in the room. Both are forward-only.
- **The `Context:` line**, the human-readable link, as a relative markdown link to `../../../companies/<slug>.md`.

**What to sweep for, every single file.** Re-read every quote and every Context line and pull out:

- **Software competitors and incumbents** — anything sitting in the slot you are pitching into.
- **The customer's own stack** — the platforms and systems they run.
- **Channels and marketplaces they sell or operate on**, and the competitors they name.
- **Registries, standards and compliance sources** they have to satisfy.
- **Brands named inside a quote as a reason** — a brand that carries the argument gets a node, a brand dropped in passing does not.
- **Agencies, integrators and consultants in the room.**
- **Your own case studies** cited at them.

**Transcription normalisation.** Transcript tools mangle product names. Normalise in the Context line and the frontmatter, **never in the quote**. Keep the running list here as you hit them:

| heard | means |
| --- | --- |
| `<mis-heard spelling>` | `<canonical name>` |

**Missing node?** Check `companies/` first, the slug is often there already. If it genuinely has no MD and it was named by a customer, **create it in the same write**: `companies/<slug>.md` with `relationship: [[competitor]]` or `[[vendor]]`, empty `crm_url` (these are not CRM records, so the CRM pairing rule does not apply), an `## About` that says what it does and why it matters to you, and a link to the relevant theme. Never leave a named competitor as plain prose because the node was missing.

**Before you save, grep your own file.** Scan the draft for every capitalised word and every product name in the quotes. For each one, answer out loud: is it linked, is it in the frontmatter, does the node exist. A file that ships with a competitor in plain text has to be reopened, so do it now.

### Never

- Never paraphrase a quote, never tidy the grammar, never translate it.
- Never quote one of your own people into these sections.
- Never write a quote without the exchange above it.
- Never backfill a day the routine already owns by hand.

---

## Mode: read

### Workflow

1. **Scope the question.** Which slice: everything, one `interaction_type`, one stage, one industry, one date range. A positioning question about prospects is not the same corpus as one about customers in delivery.
2. **Compute the denominator first, and print it before any finding**:

   ```md
   Base: N interactions · N companies · N distinct people · <date range>
   Stage mix: <n discovery / n demo / n proposal / n delivery / …>
   Role mix: <n business / n IT / n C-level / n unknown>  (derived from people/<slug>.md job_title)
   Pipeline coverage: N of M commercial deals in the period have at least one interaction here
   Not covered: <what is missing and why>
   ```

3. **Count people and companies, never quote instances.** Three repetitions by the same person are one opinion.
4. **Separate spontaneous from prompted.** Report `raised_by: customer` counts and `raised_by: us` counts separately. Never merge them into one number.
5. **Quote, do not summarise.** Every finding carries at least one verbatim quote with speaker and link.
6. **Flag the gaps as findings.** Requests for proof you never answered, recurring across companies, are the output that matters most: they are the list of things you have never answered.
7. **Never compare counts across `extractor_version`** without re-extracting at a uniform version.
8. **Output goes to your docs system** when it is meant for humans to read (positioning read, all-hands, site work). The corpus stays in the repo.

### Pre-call use

Asked for context before a meeting with a company: read every file where that company is linked (`grep -rl "companies/<slug>.md" voice-of-customer/`), newest first, and hand back their words with dates. No synthesis unless asked.

---

## Cadence

- **capture**: weekdays, after the call, mail and chat routines have settled. Each run covers the previous day, except the first run of the week, which covers the whole weekend. Otherwise the last working day before it has no run behind it and the corpus keeps a permanent hole.
- **read**: monthly for positioning, on demand before calls.
- **heartbeat**: a weekly count in a public channel, so a routine that stops writing is visible in days instead of a month.

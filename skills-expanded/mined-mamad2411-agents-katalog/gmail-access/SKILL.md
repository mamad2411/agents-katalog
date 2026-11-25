---
name: gmail-access
description: Access Gmail via CLI with 1Password OAuth. Use when user wants to read emails, search inbox, export messages, create drafts, or.
allowed-tools: Read, Bash, Grep, Glob, Write, AskUserQuestion
---

# Gmail Access

Read and search Gmail programmatically via Claude Code.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## MANDATORY PREFLIGHT (Execute Before Any Gmail Operation)

**CRITICAL**: You MUST complete this preflight checklist before running any Gmail commands. Do NOT skip steps.

### Step 1: Check CLI Binary Exists

```bash
ls -la "$HOME/.claude/plugins/marketplaces/cc-skills/plugins/gmail-commander/scripts/gmail-cli/gmail" 2>/dev/null || echo "BINARY_NOT_FOUND"
```

**If BINARY_NOT_FOUND**: Build it first:

```bash
cd ~/.claude/plugins/marketplaces/cc-skills/plugins/gmail-commander/scripts/gmail-cli && bun install && bun run build
```

### Step 2: Check GMAIL_OP_UUID Environment Variable

```bash
echo "GMAIL_OP_UUID: ${GMAIL_OP_UUID:-NOT_SET}"
```

**If NOT_SET**: You MUST run the Setup Flow below. Do NOT proceed to Gmail commands.

### Step 2.5: Verify Account Context (CRITICAL)

**ALWAYS verify you're accessing the correct email account for the current project.**

```bash
# Show current project context
echo "=== Gmail Account Context ==="
echo "Working directory: $(pwd)"
echo "GMAIL_OP_UUID: ${GMAIL_OP_UUID}"

# Check where GMAIL_OP_UUID is defined (mise hierarchy)
echo ""
echo "=== mise Config Source ==="
grep -l "GMAIL_OP_UUID" .mise.local.toml .mise.toml ~/.config/mise/config.toml 2>/dev/null || echo "Not found in standard locations"

# Quick connectivity test — shows the account email from a real email
echo ""
echo "=== Account Verification ==="
$GMAIL_CLI list -n 1 2>&1 | head -5
```

**STOP and confirm with user** before proceeding:

- The `list -n 1` output shows the account's inbox — verify this matches the project's intended email
- If the wrong account is shown, check which `.mise.local.toml` sets `GMAIL_OP_UUID` in the mise hierarchy
- If mismatch, inform user and do NOT proceed

**Multi-account disambiguation (when `GMAIL_OP_UUID` is NOT_SET but tokens exist).**
There is no `whoami` subcommand; map each cached token UUID to its mailbox by
probing, then pick the one that fits the project:

🔴 **Do NOT identify a mailbox from `list -n 1 --json | jq '.[0].to'`.** That reads the
**recipient of the newest message**, not the mailbox owner. When the newest item is an
outgoing draft or a sent message, it reports the person you wrote TO. Measured 2026-08-18:
the `wc6vl…` token probed as an external correspondent's address while the mailbox is in
fact `amonic@gmail.com` — a confident wrong answer in the one step whose entire job is to
stop you acting on the wrong account.

Ask Gmail who it is instead. `users/me/profile` is authoritative:

```bash
# Which accounts are cached, and which mailbox does each ACTUALLY own?
for f in ~/.claude/tools/gmail-tokens/*.json; do
  case "$(basename "$f")" in *.app-credentials.json|*.bak|*.expired-*|*.dead-*|'*.json') continue ;; esac
  uuid=$(basename "$f" .json)
  # Project-local helper that mints an access token from a cached refresh token.
  tok=$(bash "${GMAIL_TOKEN_SCRIPT:?set to your project's gmail-access-token.sh}" "$uuid" 2>/dev/null | tail -1)
  if [ -z "$tok" ]; then echo "$uuid → token mint failed"; continue; fi
  who=$(curl -s --noproxy '*' -H "Authorization: Bearer $tok" \
          https://gmail.googleapis.com/gmail/v1/users/me/profile | jq -r .emailAddress)
  echo "$uuid → $who"
done
```

The same endpoint answers "which aliases may I send as", which you need before any
`--from`. `verificationStatus` must be `accepted`, and note which alias is `isDefault` —
if the default is not the one you want, `--from` is mandatory, not optional:

```bash
curl -s --noproxy '*' -H "Authorization: Bearer $tok" \
  https://gmail.googleapis.com/gmail/v1/users/me/settings/sendAs \
  | jq -r '.sendAs[] | "\(.sendAsEmail)\t\(.verificationStatus)\t\(if .isDefault then "DEFAULT" else "" end)"'
```

A probe that returns `invalid_grant` means that account's refresh token is dead
(see "Diagnosing `invalid_grant`"). Pick the working UUID whose mailbox matches
the project, pin it in `.mise.local.toml`, and confirm it's gitignored. A child
project often needs a DIFFERENT account than its parent — verify, never assume
the parent's UUID.

### Step 3: Verify Token Health

```bash
# Check cached token exists and is not expired
TOKEN_FILE="$HOME/.claude/tools/gmail-tokens/${GMAIL_OP_UUID}.json"
APP_CREDS="$HOME/.claude/tools/gmail-tokens/${GMAIL_OP_UUID}.app-credentials.json"
echo "Token file: $([ -f "$TOKEN_FILE" ] && echo "EXISTS" || echo "MISSING")"
echo "App credentials: $([ -f "$APP_CREDS" ] && echo "CACHED" || echo "MISSING — will need 1Password on first run")"
```

**If token file is MISSING**: First run will open a browser for OAuth consent. This is expected.
**If app credentials are MISSING**: 1Password will be called once to cache `client_id`/`client_secret`, then never again.

---

## Setup Flow (When GMAIL_OP_UUID is NOT_SET)

Follow these steps IN ORDER. Use AskUserQuestion at decision points.

### Setup Step 1: Check 1Password CLI

```bash
command -v op && echo "OP_CLI_INSTALLED" || echo "OP_CLI_MISSING"
```

**If OP_CLI_MISSING**: Stop and inform user:

> 1Password CLI is required. Install with: `brew install 1password-cli`

### Setup Step 2: Discover Gmail OAuth Items in 1Password

```bash
# Try common vaults — "Claude Automation" for service accounts, "Employee" for interactive
for VAULT in "Claude Automation" "Employee" "Personal"; do
  ITEMS=$(op item list --vault "$VAULT" --format json 2>/dev/null | jq -r '.[] | select(.title | test("gmail|oauth|google"; "i")) | "\(.id)\t\(.title)"')
  [ -n "$ITEMS" ] && echo "=== Vault: $VAULT ===" && echo "$ITEMS"
done
```

**Parse the output** and proceed based on results:

### Setup Step 3: User Selects OAuth Credentials

**If items found**, use AskUserQuestion with discovered items:

```
AskUserQuestion({
  questions: [{
    question: "Which 1Password item contains your Gmail OAuth credentials?",
    header: "Gmail OAuth",
    options: [
      // POPULATE FROM op item list RESULTS - example:
      { label: "Gmail API - dental-quizzes (56peh...)", description: "OAuth client in Employee vault" },
      { label: "Gmail API - personal (abc12...)", description: "Personal OAuth client" },
    ],
    multiSelect: false
  }]
})
```

**If NO items found**, use AskUserQuestion to guide setup:

```
AskUserQuestion({
  questions: [{
    question: "No Gmail OAuth credentials found in 1Password. How would you like to proceed?",
    header: "Setup",
    options: [
      { label: "Create new OAuth credentials (Recommended)", description: "I'll guide you through Google Cloud Console setup" },
      { label: "I have credentials elsewhere", description: "Help me add them to 1Password" },
      { label: "Skip for now", description: "I'll set this up later" }
    ],
    multiSelect: false
  }]
})
```

- If "Create new OAuth credentials": Read and present [references/gmail-api-setup.md](./references/gmail-api-setup.md)
- If "I have credentials elsewhere": Guide user to add to 1Password with required fields
- If "Skip for now": Inform user the skill won't work until configured

### Setup Step 4: Confirm mise Configuration

After user selects an item (with UUID), use AskUserQuestion:

```
AskUserQuestion({
  questions: [{
    question: "Add GMAIL_OP_UUID to .mise.local.toml in current project?",
    header: "Configure",
    options: [
      { label: "Yes, add to .mise.local.toml (Recommended)", description: "Creates/updates gitignored config file" },
      { label: "Show me the config only", description: "I'll add it manually" }
    ],
    multiSelect: false
  }]
})
```

**If "Yes, add to .mise.local.toml"**:

1. Check if `.mise.local.toml` exists
2. If exists, append `GMAIL_OP_UUID` to `[env]` section
3. If not exists, create with:

```toml
[env]
GMAIL_OP_UUID = "<selected-uuid>"
```

1. Verify `.mise.local.toml` is in `.gitignore`

**If "Show me the config only"**: Output the TOML for user to add manually.

### Setup Step 5: Reload and Verify

```bash
mise trust 2>/dev/null || true
cd . && echo "GMAIL_OP_UUID after reload: ${GMAIL_OP_UUID:-NOT_SET}"
```

**If still NOT_SET**: Inform user to restart their shell or run `source ~/.zshrc`.

### Setup Step 6: Test Connection

```bash
GMAIL_OP_UUID="${GMAIL_OP_UUID}" $HOME/.claude/plugins/marketplaces/cc-skills/plugins/gmail-commander/scripts/gmail-cli/gmail list -n 1
```

**If OAuth prompt appears**: This is expected on first run. Browser will open for Google consent.

---

## Gmail Commands (Only After Preflight Passes)

```bash
GMAIL_CLI="$HOME/.claude/plugins/marketplaces/cc-skills/plugins/gmail-commander/scripts/gmail-cli/gmail"

# List recent emails
$GMAIL_CLI list -n 10

# Search emails
$GMAIL_CLI search "from:someone@example.com" -n 20

# Search with date range
$GMAIL_CLI search "from:alice after:2026/01/27" -n 10

# Read specific email with full body
$GMAIL_CLI read <message_id>

# Read and download inline images (copy-pasted screenshots in compose)
$GMAIL_CLI read <message_id> --save-images

# Download inline images to a specific directory
$GMAIL_CLI read <message_id> --save-images --image-dir ./attachments/my-folder/

# Shorthand: --image-dir implies --save-images
$GMAIL_CLI read <message_id> --image-dir ./attachments/my-folder/

# JSON output with image metadata and saved paths
$GMAIL_CLI read <message_id> --save-images --json

# Download REAL file attachments (PDF, docx, csv, …) — distinct from inline images
$GMAIL_CLI read <message_id> --save-attachments

# Download attachments to a specific directory (implies --save-attachments)
$GMAIL_CLI read <message_id> --attachment-dir ./files/case-17402939/

# Export search results to JSON (full body + inlineImages + attachments metadata per message)
$GMAIL_CLI export -q "label:inbox" -o emails.json -n 100

# JSON output (for parsing)
$GMAIL_CLI list -n 10 --json

# Create a draft email
$GMAIL_CLI draft --to "user@example.com" --subject "Hello" --body "Message body"

# Create a draft reply (threads into existing conversation)
$GMAIL_CLI draft --to "user@example.com" --subject "Re: Hello" --body "Reply text" --reply-to <message_id>

# Draft with body loaded from a file (multi-paragraph bodies are awkward via --body)
$GMAIL_CLI draft --to "user@example.com" --subject "Report" --body-file ./email-body.txt

# Draft with file attachments (--attach is repeatable; MIME type guessed from extension)
$GMAIL_CLI draft --to "user@example.com" --subject "Q1 Report" \
  --body-file ./email-body.txt \
  --attach ./report.pdf \
  --attach ./screenshot.png

# Draft reply with both body-file and multiple attachments
$GMAIL_CLI draft --to "user@example.com" --subject "Re: Project" \
  --reply-to <message_id> \
  --body-file ./reply.txt \
  --attach ./diagram.pdf

# List drafts with their draft IDs
$GMAIL_CLI drafts -n 10

# Replace a draft in place (delete + recreate — the draft ID CHANGES)
$GMAIL_CLI draft-update <draft_id> --to "user@example.com" --from "me@example.com" \
  --subject "Same subject" --body-file ./revised-body.txt
```

### `drafts --json` field names

The identifier field is **`draftId`**, not `id`. A `.id` selector silently yields
`null` for every row rather than erroring, so a jq pipeline built on it looks like
it worked and hands you nothing:

```bash
# WRONG — .id does not exist; prints "null" per draft and fails silently
$GMAIL_CLI drafts -n 10 --json | jq -r '.[] | "\(.id)\t\(.subject)"'

# RIGHT
$GMAIL_CLI drafts -n 10 --json | jq -r '.[] | "\(.draftId)\t\(.subject)"'
```

Full row shape: `date`, `draftId`, `from`, `messageId`, `snippet`, `subject`,
`threadId`, `to`. Note the two distinct identifiers — **`draftId`** is what
`draft-update` and `draft-delete` take; **`messageId`** is what `read` takes.
Passing one where the other belongs fails or returns the wrong record.

**`draft-update` returns a NEW `draftId`** (it deletes and recreates). Any ID you
noted earlier is dead the moment you update — re-list before a second update, and
never cache a draft ID across edits.

## 🔴 ATTRIBUTION DOCTRINE — run this before you ever write "they said X"

**Reading an email and knowing who wrote which line are two different problems.** The second one is harder, its answer is not in the text you get back by default, and when it goes wrong it does not throw — it produces a fluent, confident summary in which your own sentences are attributed to your correspondent, or half of what they wrote is silently missing. Every failure recorded in this section was of that shape: a wrong query returning an empty result, read as an empty world.

**This applies by default.** If a message is a reply — it has quoted history — and you intend to quote, summarise, attribute, decide, or act on what the sender said, you run the protocol below. It does not apply to listing, searching, triage, or counting.

### The model: authorship ⊃ colour ⊃ marker

Three signals, nested, in descending order of trust. Using the wrong one as your primary is how both halves of the 2026-08-25 incident happened.

| Signal                                    | Coverage                                                 | Where it lives                       | Trust                                             |
| ----------------------------------------- | -------------------------------------------------------- | ------------------------------------ | ------------------------------------------------- |
| **Quote depth**                           | **Complete** — captures top matter AND inline insertions | `text/plain`: lines NOT prefixed `>` | Primary. But see the caveats — some clients lie   |
| **Colour**                                | Proper subset — insertions inside a quoted region only   | `text/html` ONLY                     | Disambiguates exactly where depth gets unreliable |
| **Typed marker** (`>>>PT`, `@@@`, `[JS]`) | Proper subset of colour — flags where a block STARTS     | either part                          | Weakest. **Never sufficient alone**               |

### The protocol

```bash
bun scripts/attribution-parse.ts --id <messageId> --token-cmd '<cmd printing an access token>'
```

It prints which signals are actually present, what it attributes to the sender and why, and — the important part — what it **cannot** attribute. It reports `CONFLICT` when signals disagree and `UNKNOWN` when a line at quoted depth carries neither colour nor marker, because in that case the line genuinely could belong to either party. **`UNKNOWN` is a correct answer.** A tool that always decides is a tool that is sometimes confidently wrong.

### Four rules that outlive any particular client

1. **Verify the convention per message. Never infer it from another message.** The same correspondent used three different conventions in six days: css-coloured on 20 Aug, `>>>PT` markers with no colour at all on 21 Aug, legacy `<font color>` on 25 Aug. A message that _says_ "see my comments in blue" may contain no colour whatsoever — measured, twice.
2. **An empty result from a detector means your detector might be wrong.** This is the single most expensive habit in this file. Zero colour spans, zero markers, zero matching rows — before concluding the sender did not do the thing, prove your query can find the thing when it is there. Same shape as the `.[0].to` mailbox probe and the `.id` draft field elsewhere in this skill.
3. **Read to the end of the paragraph.** An audit of 22 authored segments found the residual misses were **not** caused by parsing at all — every one sat inside a segment already extracted, and was lost to first-sentence reading. Her structure is consistent and it is the opposite of a summary: **the decision is in sentence one, the condition is in sentence two, and the condition is the part that binds you.** "Let's go with that for now" _…and hope they increase it later_. "I am prepared to walk away" _…if we can find a local replacement and if we have time_.
4. **Prefer "I cannot tell" to a confident attribution.** You will be forgiven for asking. You will not be forgiven for putting words in someone's mouth in a document they read.

### Three measured exemplars, from one correspondent in six days

| Date   | What she said her convention was | What the source actually contained                                                           | What broke                                                                                                                                                                                                                                          |
| ------ | -------------------------------- | -------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 20 Aug | "comments below in blue"         | Exactly **one** css `rgb(0,0,255)` span; the rest marked `>>>>` / `>>>`                      | Colour was nearly useless; one comment was a truncated fragment (`>>> should be`) that needed a follow-up question to resolve                                                                                                                       |
| 21 Aug | "Pls see below with >>>PT"       | **No colour at all.** Markers only                                                           | A colour-first parser would have found nothing and reported she wrote nothing                                                                                                                                                                       |
| 25 Aug | "Pls see below in blue >>>PT"    | **25 legacy `<font color="#0000ff">` tags, zero css `color:`.** 22 authored runs, 13 markers | A css-only detector returned zero and was read as "no colour used". Then the over-correction — "colour is the complete signal" — would have discarded her **top matter**, which is black and held the single most important decision in the message |

**The lesson from the third row is the one to keep.** Finding the bug is not the same as fixing the model. The first reading trusted markers and missed 9 of 22 segments; the corrected reading trusted colour and would have missed the migration date. Only the nested model survives both.

### Red flags — stop and verify by hand

- The sender describes a convention that your parser cannot find (says "in blue", no colour detected).
- Coloured-run count and marker count differ — the difference is unmarked continuation text, and continuations are where the conditions live.
- Colour appears in `text/html` but the matching text is absent from `text/plain`, or vice versa. **Parse both parts and take the union; never prefer one.** Clients generate them independently, so offsets from one do not map onto the other.
- More than two apparent authors in a two-party thread — usually one author split across colour spellings (`blue` / `#00F` / `rgb(0,0,255)`), which is why colour must be normalised to a canonical triple before any equality test.
- Any CJK full-width punctuation (`＞＞`, `：`, `【PT】`). `^>` does not match `＞`, so a full-width-quoted thread parses as 100% new text by the last replier.

### Before the archive, not after

Colour lives only in `text/html`. **An archive that stores `text/plain` alone cannot answer "who said what" later** — the evidence is simply not in it, and you will find yourself back at the API to answer a question your own records should have settled. Store both parts. `read --json` returns plain text only; fetch `format=full` for the html:

```bash
curl -s --noproxy '*' -H "Authorization: Bearer $TOK" \
  "https://gmail.googleapis.com/gmail/v1/users/me/messages/<id>?format=full" \
  | jq -r '[ .. | objects | select(.mimeType? == "text/html") | .body.data ]
           | map(select(. != null)) | .[0] // empty' \
  | tr '_-' '/+' | base64 -d > msg.html
```

**And never strip quoted history when a sender replies inline** — their answers live _inside_ the quotes, so stripping deletes the reply and keeps the signature.

### The full catalogue

Normalisation that must precede every rule (quoted-printable, `format=flowed`, CRLF, colour canonicalisation, entity decoding, NFKC, Word conditional comments), per-client priors, typed-marker regexes, and the client artifacts that masquerade as authorship signals: **[references/attribution-parsing.md](./references/attribution-parsing.md)**.

## Inline Image Extraction

Emails often contain **copy-pasted screenshots** (inline images embedded in the HTML body, not file attachments). These appear as `[image: image.png]` placeholders in plain text but contain real image data accessible via the Gmail API.

### Key Behavior

| Flag                 | Effect                                                                                     |
| -------------------- | ------------------------------------------------------------------------------------------ |
| `--save-images`      | Download all inline images to disk (default: `~/.claude/tools/gmail-images/<message_id>/`) |
| `--image-dir <path>` | Custom output directory (implies `--save-images`)                                          |
| No flag              | Shows image metadata (count, filenames, sizes) but does NOT download                       |

### Output Sections (when images are present)

```
--- Inline Images (3) ---
  image.png   image/png   245.3 KB
  image.png   image/png   512.1 KB
  photo.jpg   image/jpeg  89.7 KB

--- Saved to Disk ---
  ./attachments/01_image.png  (251,234 B)
  ./attachments/02_image.png  (524,001 B)
  ./attachments/03_photo.jpg  (91,852 B)

--- Markdown References ---
![01_image.png](./attachments/01_image.png)
![02_image.png](./attachments/02_image.png)
![03_photo.jpg](./attachments/03_photo.jpg)
```

### Important: Inline Images vs File Attachments

These are **two disjoint channels**, surfaced and downloaded separately:

| Channel              | MIME parts                                                             | Metadata field   | Download flag                             |
| -------------------- | ---------------------------------------------------------------------- | ---------------- | ----------------------------------------- |
| **Inline images**    | `image/*` with `attachmentId` (copy-pasted screenshots)                | `inlineImages[]` | `--save-images` / `--image-dir`           |
| **File attachments** | non-image parts with a `filename` + `attachmentId` (PDF, docx, csv, …) | `attachments[]`  | `--save-attachments` / `--attachment-dir` |

A plain `gmail read <id>` (no flags) shows **both** as metadata blocks (filename, MIME, size) without downloading — so you can see a PDF exists before pulling it. `export` and `read --json` both carry `attachments[]` (and `inlineImages[]`) in their JSON.

**`has:attachment` matches real file attachments but NOT inline images.** Gmail search has no operator for inline images. To discover emails with inline images, you must read the email and check the MIME tree.

**Strategy for finding emails with inline images:**

```bash
# Search by sender/date, then read each to check for images
$GMAIL_CLI search "from:sender@example.com after:2026/02/01" -n 10 --json | \
  jq -r '.[].id' | while read id; do
    COUNT=$($GMAIL_CLI read "$id" --json | jq '.inlineImages | length')
    [ "$COUNT" -gt 0 ] && echo "$id has $COUNT inline image(s)"
  done
```

### Gmail Threading and Image Deduplication

When downloading images from a **thread** (multiple reply emails), later replies include all prior inline images. The last email in a thread is typically the superset.

**Recommendation**: For threaded conversations, download images from the **latest reply only** to avoid duplicates. Compare by file size if unsure.

### Filename Collision Handling

Copy-pasted screenshots often all share the generic filename `image.png`. The CLI prefixes a zero-padded index: `01_image.png`, `02_image.png`, etc. These machine-generated names should be renamed to descriptive names for correspondence archival.

### Post-Download: Annotation Transcription Protocol

When inline images contain **handwritten annotations** (circles, arrows, written text overlaid on screenshots), perform a systematic two-level analysis:

1. **Scene description**: What does the screenshot show? (e.g., "Career portal main page showing position listings")
2. **Annotation inventory**: Exhaustively catalog every non-original markup element:
   - **Hand-drawn shapes**: circles, ovals, arrows, underlines, crosses — note what they encompass
   - **Handwritten text**: transcribe verbatim in quotes, note legibility and location on the image
   - **Typed test inputs**: text entered into form fields visible in the screenshot
   - **Highlights or color markings**: note color and what is highlighted

**Format annotations as blockquote captions** beneath each image in markdown:

```markdown
![Scene description — annotation summary](path/to/image.png)

> **Annotation transcription**: [Detailed description of visual markup.]
> Handwritten text reads: _"exact transcription here"_
> [Interpretation of what the annotator is requesting.]
```

**Do NOT defer annotation transcription to a second pass.** Capture all annotations on the first image examination to avoid redundant re-reads.

## File Attachment Extraction

Real file attachments (PDF, docx, csv, …) are surfaced in `attachments[]` and
downloaded with `--save-attachments` / `--attachment-dir`. Same fetch path as
inline images, different metadata field.

```bash
# See what a message carries (no download) — both metadata blocks print
$GMAIL_CLI read <id>          # → "--- Attachments (1) ---  foo.pdf  application/pdf  192.5 KB"

# Download to a chosen dir; files are index-prefixed + sanitized
$GMAIL_CLI read <id> --attachment-dir ./files/

# Discover which messages in a corpus actually carry attachments
$GMAIL_CLI search "from:sender@example.com has:attachment" -n 20 --json | \
  jq -r '.[].id' | while IFS= read -r id; do
    N=$($GMAIL_CLI read "$id" --json | jq '.attachments | length')
    [ "$N" -gt 0 ] && echo "$id → $N attachment(s)"
  done
```

**Why this matters for archival**: in clinical/legal/operational mail the
attached PDF (a protocol, a vendor form, a signed consent) is often the most
important payload. A body-only export silently loses it. Always check
`attachments[]` when archiving a correspondence thread.

## Bulk Retrieval & Thread Archival

The canonical pattern for archiving a whole correspondence (verified on a
27-message, 15-thread clinical corpus):

1. **Scope with high-signal queries, not generic keywords.** A bare keyword
   (`"Curve"`) returns mostly newsletter noise. Prefer:
   - **domain**: `vendor-domain.com` (matches from/to/cc on the org)
   - **participant**: `from:someone@example.com OR to:…`
   - **project code**: any internal tag the sender uses (e.g. `1233V`)
2. **Collect message IDs** from `search --json` (snippet-only) and curate the
   in-scope set out of the noise.
3. **Fetch full bodies** with a `read --json` loop (one file per message).
4. **Group by `threadId`** client-side — Gmail's list/search APIs return
   individual messages, _not_ threads; you reconstruct threads yourself.
5. **Sort within a thread by parsed `Date`** and **strip quoted history**
   (drop `>`-prefixed lines and everything after `On … wrote:`) to expose each
   message's new content.
6. **Pull attachments** for any message whose `attachments[]` is non-empty.

```bash
# Robust batch fetch. NOTE: in zsh `for id in $VAR` does NOT word-split —
# always loop with `while IFS= read -r` over newline-delimited IDs.
printf '%s\n' $IDS | while IFS= read -r id; do
  [ -n "$id" ] && $GMAIL_CLI read "$id" --json > "raw/$id.json"
done
```

### `export` is the one-call shortcut (fixed)

`gmail export -q "<query>" -o out.json -n N` writes one JSON array with full
body + `inlineImages[]` + `attachments[]` per message — the batch-fetch
shortcut when a single query captures your set. (Historical note: before the
fix, `export` printed `"Exported N emails to <path>"` but **wrote no file** —
`outputPath` was an unused parameter. If you see that symptom, the binary is
stale; rebuild it.) `export` does **not** download attachment bytes — it only
carries the metadata; use `read --save-attachments` per message for the files.

## Creating Draft Emails

The `draft` command creates emails in your Gmail Drafts folder for review before sending.

**Required options:**

- `--to` - Recipient email address
- `--subject` - Email subject line
- `--body` OR `--body-file` - Email body text (one of the two)

**Optional:**

- `--body-file` - Read body from a file instead of `--body`. Useful for multi-paragraph bodies that are awkward to pass on the shell. Mutually exclusive with `--body`; if both are passed, `--body` wins with a stderr warning.
- `--attach` - File path to attach. **Repeatable** for multiple attachments. MIME type is guessed from extension (PDF, PNG, JPEG, DOCX, XLSX, ZIP, MD, JSON, etc. → mapped; unknown → `application/octet-stream`). Total message size ≤ 25 MB (Gmail limit; the CLI surfaces a 413 with a helpful hint if you exceed it).
- `--from` - Sender email alias (auto-detected when replying, see Sender Alignment below)
- `--reply-to` - Message ID to reply to (creates threaded reply with proper headers)
- `--json` - Output draft details as JSON

### MANDATORY Sender Alignment (NON-NEGOTIABLE)

The user has multiple Send As aliases configured in Gmail. The From address MUST match correctly or the recipient sees a reply from the wrong identity.

**Rule 1 - Replies (--reply-to is set): pass `--from` ANYWAY.**

The CLI attempts to auto-detect the sender by reading the original email's To/Cc/Delivered-To headers and matching against the user's Send As aliases, and prints what it chose:

```
From: amonic@gmail.com (auto-detected from original email)
```

**Do not trust that line to be the identity you want.** Auto-detection resolves to the _underlying account_ rather than the alias even when the original was addressed to the alias. Measured 2026-08-25: a message addressed to `Ricky Chan <rickychanbc@gmail.com>` produced `From: amonic@gmail.com`, silently, with no warning — and `rickychanbc@gmail.com` is an `accepted` send-as alias on that very account. The draft looked successful.

This matters because the alias IS the identity, not a cosmetic label. Where a correspondence policy says which name to sign as, the account and the alias are different signatories, and getting it wrong sends the whole message as the wrong person. Note also that the _default_ alias on this account is `terry@eonlabs.com`, which policy forbids for non-Eon-Labs mail — so an omitted or mis-detected `--from` can reach for an identity that is not merely wrong but prohibited.

**So: always pass `--from` explicitly, on replies as well as new mail, and read the confirmation line back before trusting it.** If a draft was already created without it, `draft-update <draftId> --from …` recreates it correctly — it does not patch in place, so re-supply every other flag too.

**There is no `--cc` flag.** A reply draft therefore carries only `To`, even when the thread it replies into copied other people. Threading is preserved (`In-Reply-To`/`References` are set), but the copies are not. On a thread with a client and several vendors copied, this silently drops all of them from a reply sent on that client's behalf. Either restore the copies in the Gmail compose window before sending, or state plainly in your handoff that the CC list needs restoring — never let a draft go out assumed to be a reply-all.

**Rule 2 - New emails (no --reply-to):**
When drafting a brand new email (not a reply), you MUST use AskUserQuestion to confirm which sender alias to use BEFORE creating the draft. Never assume the default.

```
AskUserQuestion({
  questions: [{
    question: "Which email address should this be sent from?",
    header: "Send As",
    options: [
      // Populate from known aliases or let user specify
      { label: "amonic@gmail.com", description: "Personal Gmail" },
      { label: "terry@eonlabs.com", description: "Work email" },
    ],
    multiSelect: false
  }]
})
```

Then pass the selected address via `--from`:

```bash
$GMAIL_CLI draft --to "recipient@example.com" --from "amonic@gmail.com" --subject "Hello" --body "Message"
```

**Rule 3 - Always verify in output:**
After draft creation, confirm the From address is shown in the output. If it's missing or wrong, delete the draft and recreate.

### MANDATORY Post-Draft Step (NON-NEGOTIABLE)

After EVERY draft creation, you MUST present the user with a direct Gmail link to review the draft. This is critical because drafts should always be visually confirmed before sending.

**Always output this after creating a draft:**

```
Draft created! Review it here:
  https://mail.google.com/mail/u/0/#drafts
From: <sender_address>
```

**Never skip this step.** The user must be able to click through to Gmail and visually verify the draft content, sender, recipients, and threading before sending.

### Example: Reply to an email (auto-detected sender)

```bash
# 1. Find the message to reply to
$GMAIL_CLI search "from:someone@example.com subject:meeting" -n 5 --json

# 2. Create draft reply - From is auto-detected from original email's To header
$GMAIL_CLI draft \
  --to "someone@example.com" \
  --subject "Re: Meeting tomorrow" \
  --body "Thanks for the update. I'll be there at 2pm." \
  --reply-to "19c1e6a97124aed8"

# 3. ALWAYS present the review link + From address to user
```

### Example: New email (must ask user for sender)

```bash
# 1. Ask user which alias to send from (AskUserQuestion)
# 2. Create draft with explicit --from
$GMAIL_CLI draft \
  --to "someone@example.com" \
  --from "amonic@gmail.com" \
  --subject "Hello" \
  --body "Message body"

# 3. ALWAYS present the review link + From address to user
```

**Note:** After creating drafts, users need to re-authenticate if they previously only had read access. The CLI will prompt for OAuth consent to add the `gmail.compose` scope.

## Gmail Search Syntax

| Query                      | Description                                                                          |
| -------------------------- | ------------------------------------------------------------------------------------ |
| `from:sender@example.com`  | From specific sender                                                                 |
| `to:recipient@example.com` | To specific recipient                                                                |
| `subject:keyword`          | Subject contains keyword                                                             |
| `after:2026/01/01`         | After date                                                                           |
| `before:2026/02/01`        | Before date                                                                          |
| `label:inbox`              | Has label                                                                            |
| `is:unread`                | Unread emails                                                                        |
| `has:attachment`           | Has file attachment (**does NOT match inline images** — see Inline Image Extraction) |

Reference: <https://support.google.com/mail/answer/7190>

## Environment Variables

| Variable         | Required | Description                                                                                                                                                                                       |
| ---------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `GMAIL_OP_UUID`  | Yes      | 1Password item UUID for OAuth credentials                                                                                                                                                         |
| `GMAIL_OP_VAULT` | No       | 1Password vault (default: `Employee`)                                                                                                                                                             |
| `HTTPS_PROXY`    | No       | Honored by the underlying `gaxios` library, BUT the CLI auto-injects `*.googleapis.com` into `NO_PROXY` at startup so corporate proxies don't break Gmail traffic. See "Proxy Auto-Bypass" below. |

## Proxy Auto-Bypass for Google API Hosts

If `HTTPS_PROXY` (or `HTTP_PROXY`) is set in the environment, the CLI automatically injects the following hosts into `NO_PROXY` at module load — **before any auth or API call is made**:

- `.googleapis.com` (covers `gmail.googleapis.com`, `oauth2.googleapis.com`, etc.)
- `.google.com`
- `accounts.google.com`
- `oauth2.googleapis.com`

**Why this exists**: many corporate networks (Cloudflare WARP, mitmproxy local interceptors, ITP-style local proxies) can't tunnel CONNECT to Google API hosts. When the proxy fails, the response surface returns HTTP 502 with an empty error body — the googleapis library throws a gaxios error whose `.message` is empty, which used to render as a useless empty `Error:` in stderr.

By force-bypassing the proxy for Google hosts, end-users with a corporate proxy can run the CLI without manually setting `NO_PROXY` or unsetting `HTTPS_PROXY` per-command.

**Idempotent**: the injection only adds entries that aren't already present in `NO_PROXY`. If you've manually configured `NO_PROXY=.googleapis.com`, the CLI leaves it alone.

**Diagnosing remaining proxy issues** (rare): if you still see HTTP 5xx errors, the CLI's new error formatter prints the full URL + response body + a hint. Check that `HTTPS_PROXY` was set BEFORE the CLI started (env-var detection is one-shot at module load).

## Error Messages

The CLI's top-level error handler renders unknown errors as structured messages with HTTP status, request URL, response body snippet, and a category-specific hint. Example for a 404 on a bogus draft ID:

```
Error: HTTP 404 Not Found DELETE https://gmail.googleapis.com/gmail/v1/users/me/drafts/r-doesnotexist123
  body: {"error":{"code":404,"message":"Requested entity was not found.",...}}
  hint: message / draft ID not found. List existing drafts with `gmail drafts` first.
```

Hint categories:

| Status      | Hint                                                                                                                                                     |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 401         | Token expired/revoked. Delete `~/.claude/tools/gmail-tokens/$GMAIL_OP_UUID.json` to force re-auth.                                                       |
| 403         | OAuth scope insufficient (drafts/attachments need `gmail.compose`) or Send As alias not configured.                                                      |
| 404         | Message / draft ID not found. List existing drafts with `gmail drafts` first.                                                                            |
| 413         | Attachment(s) exceed Gmail's 25 MB per-message limit. Split or use Drive links.                                                                          |
| 502/503/504 | Gateway error — usually a proxy that can't tunnel to Google. The auto-bypass should prevent this; check that HTTPS_PROXY was set BEFORE the CLI started. |

Network-layer errors (`ECONNREFUSED`, `ENOTFOUND`, etc.) are surfaced with their error code instead of the empty `Error:` of the prior implementation.

## Token Architecture

### Storage Layout

```
~/.claude/tools/gmail-tokens/
├── <uuid>.json                    # OAuth token (access + refresh), refreshed hourly
└── <uuid>.app-credentials.json    # client_id + client_secret (static, cached from 1Password)
```

- Central location (not in plugin, not in project)
- Organized by 1Password UUID (supports multi-account)
- Created with chmod 600

### Auth Flow (1Password is one-time only)

1. **First run**: 1Password is called to fetch `client_id`/`client_secret` → cached to `<uuid>.app-credentials.json`
2. **First run**: Browser opens for Google OAuth consent → tokens saved to `<uuid>.json`
3. **All subsequent runs**: Reads cached files only — **no 1Password call, no browser**
4. **Hourly refresher** (launchd): Keeps access_token alive by calling Google's token endpoint with the cached refresh_token

To force a fresh 1Password lookup (e.g., after rotating OAuth app credentials):

```bash
rm ~/.claude/tools/gmail-tokens/<uuid>.app-credentials.json
```

### Diagnosing `invalid_grant`

A refresh token in a Google OAuth app whose **publishing status is "Testing"** expires after **7 days — period.** The hourly refresher renews the _access_ token but does NOT extend the _refresh_ token's 7-day clock, so a Testing-mode account dies roughly weekly and can only be revived by a browser re-consent. (An app in **"In production"** status issues long-lived refresh tokens that don't expire on that clock.)

**Recovery (re-consent)**: Delete the expired token file and re-authorize via browser:

```bash
# 1. Back up and remove the expired token
mv ~/.claude/tools/gmail-tokens/<uuid>.json ~/.claude/tools/gmail-tokens/<uuid>.json.expired

# 2. Run any gmail command — browser will open for OAuth consent
#    (sign in with the SPECIFIC account that <uuid> maps to — see accounts.json labels)
$GMAIL_CLI list -n 1

# 3. Verify the hourly refresher picks up the new token
~/.claude/automation/gmail-token-refresher/gmail-oauth-token-refresher 2>&1

# 4. Clean up backup
rm ~/.claude/tools/gmail-tokens/<uuid>.json.expired
```

**Durable fix (stop the weekly death — "keep everything re-auth")**: publish the
OAuth app to Production so refresh tokens stop expiring on the 7-day clock.

1. If an account survives indefinitely while another dies weekly, they use
   **different OAuth apps** (check `accounts.json` `vault` per uuid). Only the
   dying one is stuck in Testing.
2. Google Cloud Console → the project owning that OAuth client (the
   `client_id` prefix is the project number; the CLI prints the full
   `client_id` in the consent URL during re-auth).
3. **APIs & Services → OAuth consent screen → Publishing status → Publish app
   → confirm "In production".** (External + Production with Gmail scopes may
   warn "unverified" for _new_ users, but already-consented accounts get
   long-lived refresh tokens; full Google verification is only needed for
   public/>100-user apps.)
4. Re-consent once more after publishing; the hourly refresher then keeps the
   access token fresh indefinitely with no weekly re-auth.

### Multi-Account Token Status

```bash
# Check all accounts at once
for f in ~/.claude/tools/gmail-tokens/*.json; do
  [ "$(basename "$f")" = "*.json" ] && continue
  case "$(basename "$f")" in *.app-credentials.json) continue ;; esac
  UUID=$(basename "$f" .json)
  python3 -c "
import json, datetime
t = json.load(open('$f'))
exp = datetime.datetime.fromtimestamp(t.get('expiry_date',0)/1000)
delta = (exp - datetime.datetime.now()).total_seconds()
status = 'VALID' if delta > 0 else 'EXPIRED'
print(f'  {\"$UUID\"}: {status} (expires in {int(delta/60)}m)' if delta > 0 else f'  {\"$UUID\"}: EXPIRED ({int(-delta/3600)}h ago)')
" 2>/dev/null
done
```

## References

- [mise-templates.md](./references/mise-templates.md) - Complete mise configuration templates
- [mise-setup.md](./references/mise-setup.md) - Step-by-step mise setup guide
- [gmail-api-setup.md](./references/gmail-api-setup.md) - Google Cloud OAuth setup guide

## Post-Change Checklist

- [ ] YAML frontmatter valid (no colons in description)
- [ ] Trigger keywords current
- [ ] Path patterns use $HOME not hardcoded paths
- [ ] References exist and are linked

## Evolution Log

- **2026-08-25 — reply auto-detection resolved the ACCOUNT, not the alias, and reported success.**
  - _Trigger_: a reply drafted into a vendor thread on a client's behalf. The original was addressed to `Ricky Chan <rickychanbc@gmail.com>`; the CLI printed `From: amonic@gmail.com (auto-detected from original email)` and created the draft. The alias is `verificationStatus=accepted` on that same account, so there was no failure to detect — it detected, and chose the underlying account.
  - _Why it was nearly missed_: this file previously said, of replies, "No manual intervention needed", and told you to fall back to `--from` only "if auto-detection fails". Nothing failed. The success path produced the wrong signatory, and the printed confirmation line made it look verified.
  - _Why it matters more than a cosmetic header_: where a correspondence policy dictates which name to sign as, the account and the alias are **different people**. This account's _default_ alias is a work identity that policy forbids for this client's mail, so an omitted `--from` does not merely pick something unexpected — it can pick something prohibited. The 2026-08-18 entry below had already recorded that hazard for new mail; the reply path was left carved out as safe, and it is not.
  - _Fix_: Rule 1 now says pass `--from` **explicitly on replies too**, and read the confirmation line back rather than trusting that it was printed. `draft-update <draftId>` repairs an existing draft, but it deletes and recreates — re-supply every flag.
  - _Also documented, same session_: there is **no `--cc` flag**. A reply draft carries only `To`, so replying into a thread that copied a client and several vendors silently drops all of them. Threading headers are preserved, which makes it look like a reply-all when it is not. Restore the copies in Gmail before sending, or say so explicitly in the handoff.
  - _Evidence_: draft `r2992600088433000620` created with `--reply-to` and no `--from` → `amonic@gmail.com`; recreated as `r6764046697684220651` with an explicit `--from` → `rickychanbc@gmail.com`, same thread `19f8ccd3370cdf57`.

- **2026-08-25 — we could not say who wrote which line, and the bug was in the detector, not the mail.**
  - _Trigger_: an operator asked whether the colour-coded inline replies in a client's message had actually been parsed. They had not. A scan for css `color:` had returned zero, and the zero was read as "the sender used no colour". The message contained **25 legacy `<font color="#0000ff">` tags**. Same confident-absence shape as the `.[0].to` probe and the `.id` field above — a wrong query whose empty result reads as an empty world.
  - _Defect 2, found while fixing defect 1_: the correction was also wrong. Having found the colour, the model became "colour is the complete signal" — which discards the sender's **top matter**, because it is black. On that message the top matter held the migration date, the reasoning for it, and a phone-call request. The stated rule would have thrown away the most important content in the mail, and the analysis silently violated its own rule to keep it.
  - _Defect 3, structural_: the archive stored `text/plain` only. Colour is an html property, so **the evidence separating the sender's words from ours was never in the repository** — answering the question required going back to the API, which is the dependency the archive existed to remove.
  - _Fix_: an **ATTRIBUTION DOCTRINE** section above (nested model: authorship ⊃ colour ⊃ marker, quote depth primary), a reusable `scripts/attribution-parse.ts` that reports `CONFLICT`/`UNKNOWN` rather than guessing, `scripts/attribution-parse.test.ts` pinning each failure mode, and `references/attribution-parsing.md` — a surveyed catalogue of 108 conventions across colour, markers, quote structure and client artifacts.
  - _Measured while building the tool, and it is the sharpest lesson_: an audit of all 22 authored segments found the residual misses were **not** caused by marker-vs-colour parsing at all. Every one sat inside a segment already extracted, and was lost to **first-sentence reading** — the decision is in sentence one, the condition is in sentence two, and the condition is the part that binds you.
  - _Also measured_: real email is **CRLF**, and a trailing `\r` is a line terminator to the regex engine, so a `(.*)$` pattern fails on **every** line and yields empty text for the whole message while still reporting "quote depth: yes". Caught only by running the parser against a real message with known ground truth.
  - _Evidence_: three messages from one correspondent in six days used three different conventions — one css span, then markers with no colour, then legacy font tags. 22 coloured runs against 13 markers on the last. 20/20 unit tests green.

- **2026-08-18 — the account-verification probe reported the WRONG mailbox, and `GMAIL_OP_UUID` means two different things.**
  - _Trigger_: drafting clinic correspondence that must go out as a specific send-as alias. Step 2.5 exists precisely to stop you acting on the wrong account, and it gave a confident wrong answer.
  - _Defect 1_: the disambiguation snippet read `list -n 1 --json | jq '.[0].to'` — the **recipient of the newest message**, not the mailbox owner. The newest item was an outgoing draft, so the `wc6vl…` token reported an external correspondent's address when the mailbox is `amonic@gmail.com`. Anyone trusting it would have concluded they were authenticated as the counterparty.
  - _Fix 1_: replaced with `users/me/profile` → `.emailAddress`, which is authoritative, plus a `settings/sendAs` probe so aliases and the DEFAULT alias are known before `--from` is chosen. That default matters: on this account it is `terry@eonlabs.com`, which correspondence policy forbids for clinic mail — so an omitted `--from` sends as the forbidden identity.
  - _Defect 2, NOT yet fixed_: `GMAIL_OP_UUID` is overloaded. A project's `.mise.local.toml` may set it to the 1Password item **title** (e.g. `"amonic-gmail"`), while `gmail-access-token.sh` and the token cache key off the item **UUID** (`wc6vl….json`). Passing the title fails with `no token file`. Whether the compiled `gmail` CLI resolves titles via 1Password was **not** tested, because a wrong guess triggers a fresh OAuth browser consent. **Verify before "fixing" either side.**
  - _Evidence_: `users/me/profile` → `amonic@gmail.com`; `settings/sendAs` → `rickychanbc@gmail.com` `verificationStatus=accepted`, `terry@eonlabs.com` `isDefault=true`. Draft `r6501695713107519416` created with an explicit `--from` and read back with the alias correct and no `terry` in the header.

- **2026-08-18 — the body guard does NOT cover `scripts/gmail-draft.ts`, and markdown reached a real draft through that hole.**
  - _Trigger_: an ad-hoc Gmail drafts-API write was correctly BLOCKED by `gmail-draft-guard.sh`, which redirected to `scripts/gmail-draft.ts`. That script accepts a markdown `--body` file and **is not covered by `pretooluse-gmail-body-guard.ts`**, which matches on `gmail draft` / `draft-update`. A clinic draft was authored through it with markdown and passed.
  - _Symptom_: the stored `text/plain` carried **11 literal `**bold**` runs and 2 literal `##` headings**, and the `text/html` part contained no `<b>`/`<strong>` — the CLI HTML-ESCAPES the body, it does not render markdown. The recipient would have seen raw asterisks and hashes. Caught only because the operator opened the draft in Gmail and looked at it.
  - _Fix_: rewrite via `draft-update` in plain prose. **Authoring rule applies to EVERY path into a draft, not just the guarded one**: one unbroken line per paragraph, no markdown, breaks only for list items and the sign-off.
  - _Open_: the guard should match `gmail-draft.ts` too, or that script should reject markdown itself. Until then, treat the guard's silence as no evidence — verify the stored body: `read <id> --json | jq -r '.body' | grep -cE '\*\*|^#{1,6} '` should return 0.
  - _Evidence_: draft `r4023096633097304797` (markdown, via `gmail-draft.ts`) vs its replacement `r6980772236558441151` (clean, via `draft-update`); the same-session proposal draft `r6501695713107519416` authored plain-prose scored 0/0.

- **2026-07-22 — a PreToolUse body guard now ENFORCES single-line paragraphs + plain prose.**
  - _Trigger_: despite the 2026-07-10 fix, vendor-outreach drafts were authored from markdown files **hard-wrapped at ~100 columns** and containing raw markdown. Because `toHtmlBody()` turns every authored newline into a `<br>`, each wrap became a literal break → the recipient saw a column of short, mid-sentence lines; and because the CLI HTML-escapes the body without rendering markdown, `**bold**`/backticks/`[text](url)`/headings/tables showed literally.
  - _Fix_: a PreToolUse guard (`itp-hooks` → `pretooluse-gmail-body-guard.ts`, detector SSoT `hooks/lib/gmail-body-detector.ts`) **denies** a `gmail draft`/`draft-update` whose inline `--body` or `--body-file` content contains mid-sentence prose line breaks (HARD-WRAP) or high-signal raw markdown (RAW MARKDOWN). Escape hatch `GMAIL-BODY-OK`. Spoke: `plugins/itp-hooks/docs/gmail-body-guard.md`.
  - _Authoring rule (unchanged, now enforced)_: write each **paragraph as ONE unbroken line** — long lines reflow in the reader's window; keep only intended breaks (list items, the `Best,`/name sign-off) on their own line. Do NOT pre-wrap the body at 72/80/100 columns, and send **plain prose** — do NOT paste raw markdown expecting it to render.
- **2026-07-10 — drafts hard-wrapped at recipient → switched to HTML (multipart/alternative).**
  - _Trigger_: sent drafts (a client vendor thread) showed short, fixed-width lines / looked chopped in Gmail. Original cause: `text/plain` with no wrapping guidance, so clients hard-wrap long paragraphs.
  - _First attempt (WRONG for Gmail) — `format=flowed`_: emitted RFC 3676 `format=flowed` with 72-col soft breaks. **Gmail does NOT reliably reflow format=flowed**, and the 72-col breaks are shown literally in Gmail's compose/draft view — so the drafts still looked wrapped/"truncated". Do not use format=flowed for Gmail-destined mail.
  - _Correct fix — HTML `multipart/alternative`_: `buildRawMessage` now sends `multipart/alternative` with a **text/plain** part (the body UNWRAPPED — long lines, no 72-col chopping) and a **text/html** part (`toHtmlBody()` + `escapeHtml()`). The HTML wraps the body in a `<div>` and turns ONLY the author's own newlines into `<br>` — running text carries no inserted breaks, so the browser reflows long paragraphs to the reader's window and never shows fixed short lines. List items / `Best,`\nname sign-offs keep their breaks via `<br>`. With attachments, the alternative body nests inside `multipart/mixed`.
  - _Evidence_: recreated draft (msg 19f4e01…) `read --json` plain part now has a 329-char single paragraph line (unwrapped — proving the new path ran); the HTML part reflows in Gmail. Rebuilt binary (`bun run build`), tsgo clean. NOTE: the `gmail` binary is compiled — a TS edit needs `bun run build`; drafts made before a fix must be recreated.
- **2026-05-31 — export silent failure + no attachment retrieval (clinical archival task).**
  - _Trigger_: archiving a 27-message vendor correspondence. `gmail export -o <path>` printed `"Exported N emails to <path>"` but wrote nothing (`exportEmails` returned the array, never wrote `outputPath`). Separately, the CLI surfaced no file attachments (only `inlineImages`), so 11 messages' attached PDFs (a vendor certification form, protocols) were silently dropped.
  - _Fix_: (1) `exportEmails` now `writeFile`s the JSON. (2) Added `extractAttachments` + `attachments[]` metadata in `formatMessage`, `saveAttachments()` in gmail-images.ts, `--save-attachments`/`--attachment-dir` flags, and an Attachments metadata block in `printEmails`. Documented the inline-image-vs-attachment split, the bulk thread-archival pipeline, the multi-account UUID→mailbox probe, and the zsh `while read` batch-loop gotcha.
  - _Evidence_: `export -q vendor-domain.com -o /tmp/x.json` now writes 3 emails with full bodies; `read <id> --attachment-dir` pulled a vendor certification form PDF (197,168 B, valid PDF 1.7, 3 pages). Rebuilt binary, `tsc --noEmit` clean.

## Post-Execution Reflection

After this skill completes, reflect before closing the task:

0. **Locate yourself.** — Find this SKILL.md's canonical path before editing.
1. **What failed?** — Fix the instruction that caused it.
2. **What worked better than expected?** — Promote to recommended practice.
3. **What drifted?** — Fix any script, reference, or dependency that no longer matches reality.
4. **Log it.** — Evolution-log entry with trigger, fix, and evidence.

Do NOT defer. The next invocation inherits whatever you leave behind.

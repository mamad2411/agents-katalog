---
name: reply-email
description: Draft an email reply in your voice. Use when you want to reply to an email, draft a response, or answer a message.
allowed-tools: Read, Grep, Bash, Edit, Write
argument-hint: [message-id or paste the email]
---

# Email Reply Skill

Draft email replies that sound like the user, not like AI.

## Modes

### Single reply (default)
`/reply-email [message-id]` or `/reply-email` + paste email text

### Quick-reply shortcuts
- `/reply-email confirm [message-id]` — 1-line confirmation
- `/reply-email schedule [message-id]` — propose dates + calendar link
- `/reply-email followup [message-id]` — gentle follow-up

### Batch mode
When user says "draft all" or during morning triage:
1. List all emails needing reply
2. Draft all replies without asking
3. Save all as Gmail Drafts
4. Show summary with time estimates

## Step 1: Get the email

```bash
# Fetch the full message
gws gmail users messages get --params '{"userId":"me","id":"MESSAGE_ID","format":"full"}' --format json
```

## Step 2: Load voice context

Read these files before drafting (every time):
1. `skills/reply-email/email-voice-guide.md` — real examples of how you write
2. `skills/reply-email/learned-replies.md` — corrections from past sessions
3. `shared/communication-style.md` — writing rules

## Step 3: Draft the reply

### Rules
- Open with the person's name (first name)
- Get to the point in 1-2 sentences
- Keep it short — if it can be 3 lines, make it 3 lines
- Include calendar link when suggesting meetings
- No pleasantries ("Hope this finds you well")
- No corporate phrases ("Feel free to", "Don't hesitate to")
- No AI words (leverage, navigate, unlock, empower, delve, foster, robust, holistic)
- **Always append the email signature** (see below)

### Email Signature (mandatory on every email)
Every email draft MUST include the signature from `skills/reply-email/signature.html`.

The signature has two parts:
1. **Profile photo + text block** — Marian's headshot (round, 80px) next to name, title, contact info, and social links
2. **ELC Conference 26 banner** — clickable banner image below the text block

CDN-hosted images (always use these URLs):
- Profile photo: `https://elc-decks.pages.dev/assets/img/marian-signature.png`
- ELC 26 banner: `https://elc-decks.pages.dev/assets/img/elc26-signature-banner.png`

When creating drafts via `gmail_create_draft`, use `contentType: "text/html"` and append the full signature HTML (photo + text + banner) after the body. Wrap the body text in `<p>` tags so line breaks render correctly.

Plain-text fallback (when HTML is not possible):
```
--
Marian Kamenistak
Founder @ ELC
marian@engineeringleaders.io
+420 736 519 879
engineeringleaders.io | elc-conference.io
LinkedIn · Instagram · Luma
```

### Final check
Read the draft out loud. Does it sound like a real person typing fast between calls? Or does it sound like AI being polite? If the latter, cut half the words.

## Step 4: Save as Gmail Draft

**Default: create a Gmail draft, NOT send.**

```bash
# Build base64url-encoded RFC 2822 email
RAW=$(python3 -c "
import base64, email.message
msg = email.message.EmailMessage()
msg['To'] = 'RECIPIENT_EMAIL'
msg['Subject'] = 'Re: ORIGINAL_SUBJECT'
msg['In-Reply-To'] = 'ORIGINAL_MESSAGE_ID_HEADER'
msg['References'] = 'ORIGINAL_REFERENCES_HEADER'
msg.set_content('''REPLY_BODY_HERE''')
print(base64.urlsafe_b64encode(msg.as_bytes()).decode())
")

gws gmail users drafts create \
  --params '{"userId":"me"}' \
  --json "{\"message\":{\"threadId\":\"THREAD_ID\",\"raw\":\"$RAW\"}}"
```

Only send directly if user says "send it":
```bash
gws gmail +reply --message-id MESSAGE_ID --body "REPLY_TEXT"
```

## Gmail label IDs

Configure these label IDs after creating them in Gmail (see INSTALL.md step 2b):

```
AI_READY_LABEL_ID=Label_XXX
INFO_LABEL_ID=Label_XXX
OPS_LABEL_ID=Label_XXX
HIGH_LABEL_ID=Label_XXX
BILLING_LABEL_ID=Label_XXX
```

To find your label IDs:
```bash
gws gmail users labels list --params '{"userId":"me"}' --format json
```

## Step 5: Learn from the outcome

### Immediate learning
When user gives feedback → incorporate, redraft, log correction.

### Async learning (morning routine)
1. Fetch sent messages from last 24h
2. Cross-reference with `drafts-log.md`
3. Diff draft vs what was sent
4. Log corrections in `learned-replies.md`

### What to learn from
- Words removed → too verbose or corporate
- Words added → missing natural phrasing
- Structure changes → wrong format
- Tone shifts → misjudged the relationship
- Shortened replies → wrote too much (most common mistake)

### Log format for drafts-log.md
```markdown
### [YYYY-MM-DD HH:MM] [Thread ID] [Recipient]
**Subject:** Re: [subject]
**Draft ID:** [gmail draft id]
**Our draft:**
> [exact text]
**Status:** pending | sent-as-is | sent-with-edits | discarded
```

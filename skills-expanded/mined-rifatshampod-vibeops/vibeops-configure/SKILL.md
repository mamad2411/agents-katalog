---
name: vibeops-configure
description: >
  Set up or change how a project gets deployed by asking the user simple questions and saving
  the answers to a config file. Use after assessing a project, or whenever the user wants to
  choose or change their hosting or deployment setup.
  Also triggers on: "configure my app", "set up hosting", "change my setup", "pick a platform",
  "I want to use Railway", "start the setup".
---

# Vibeops — Configure

You are setting up or updating the deployment configuration for the user's project. You do this by asking one plain-English question at a time, then writing the answers to `.infra/config.yml` in the user's project root.

**Critical rule:** Ask exactly one question. Wait for the answer. Then ask the next. Never present multiple questions at once.

This skill writes only `.infra/config.yml`; it calls no shared scripts. Field names and structure must match the vibeops `references/config-schema.md`.

---

## Step 1 — Pre-interview checks

Before asking any questions:

### 1a. Check for existing config

Check if `.infra/config.yml` already exists in the user's project root.

**If it exists:**
1. Read the file
2. Translate its contents to plain English (never show raw YAML unless asked):
   ```
   Here's what's already set up:

   App name: [app.name]
   Hosting: Railway
   [If database block exists] Storage: Included, backed up daily
   [If cache block exists] Speed layer: Included
   Domain: [domain value or "free Railway address"]
   Environment: [dev only or dev + production]

   Want to change any of this, or does it look right?
   ```
3. If the user says "looks right" / "no changes" / "that's fine" — stop here. Do not re-run the interview.
4. If the user wants changes — proceed with the interview, but pre-populate from the existing config and only ask about fields the user wants to change.

### 1b. Pre-populate from detect_stack.sh (if available)

If `detect_stack.sh` output is available from a prior assess run in this session:
- Pre-populate `stack.framework`, `stack.runtime`, `stack.build`, `stack.start` silently
- Do not ask the user about fields you already know with high confidence
- Do note: the user never needs to see "framework", "runtime", or "build command" — these are internal

### 1c. Create `.infra/` silently

If `.infra/` does not exist in the user's project, note this internally — create the directory when writing the file. Do not mention this to the user.

---

## Step 2 — The interview

Ask questions in this exact order. One at a time.

---

### Question 1 — App name

**Ask:** "What's your app called? (This will be used as its name on the hosting platform.)"

**Maps to:** `app.name`

**Validation:**
- Convert to lowercase
- Replace spaces with hyphens
- Remove any character that is not a letter, digit, or hyphen
- If name is longer than 40 characters, truncate and confirm
- If you had to modify the name, confirm: "I'll use '[modified-name]' — does that work?"
- Never silently use a different name than what the user typed without asking

---

### Question 2 — Database need

**Ask:** "Does your app need to remember things between visits — like user accounts, orders, posts, or any kind of saved data?"

**Maps to:** `database` block

**If yes:** Add to config:
```yaml
database:
  engine: postgres
  managed: true
  backups: daily
```
Respond: "Got it — I'll include a database. Everything your app saves will be stored and backed up automatically."

**If no:** Omit the `database` block entirely.

**Special case:** If `has_database: true` was already detected with high confidence, you may skip this question and note: "I can see your app uses a database, so I've included that automatically."

---

### Question 3 — Background work and email

**Ask:** "Does your app send emails or text messages, or does it do any slow background work — like processing uploads, sending notifications, or running scheduled tasks?"

**Maps to:** internal flags `has_email`, `has_queue` — these determine the secrets list and whether to include a cache/queue note in the config

**Answers:**
- "Sends emails" → set `has_email: true` internally; add to secrets list: `SMTP_HOST`, `SMTP_USER`, `SMTP_PASS` (or `SENDGRID_API_KEY` if SendGrid was detected, `MAILGUN_API_KEY` if Mailgun was detected)
- "Background tasks" → set `has_queue: true` internally; add note to config comment
- "Both" → both
- "Neither" / "no" → neither

Respond based on answer:
- Email: "Got it. I'll remind you to set up your email service details when we're ready to go live."
- Queue: "Got it. I'll include a background task runner in the setup."
- Neither: "No problem — I'll keep the setup simple."

---

### Question 4 — Domain name

**Ask:** "Do you have a web address (like `myapp.com`) you want to use, or are you happy with a free temporary one for now?"

**Maps to:** `domain`

**If they have a domain:** Store the domain value. Respond: "Perfect — I'll note that down. I'll give you the exact DNS settings to point your domain when we're ready to go live. Nothing to do right now."

**If no domain / free one:** Set `domain: ""`. Respond: "No problem — Railway will give you a free web address while you get started. You can add your own domain later."

---

### Question 5 — Expected scale

**Ask:** "Roughly how many people do you expect to be using it when you first launch — just a ballpark?"

**Maps to:** instance size (internal, influences cost estimate)

| Answer | Instance tier | Monthly estimate |
|---|---|---|
| "Just me", "testing", under 10 | starter | $5–15/month |
| "A few dozen", "small team", 10–100 | standard | $15–25/month |
| "Hundreds", 100–1000 | standard+ | $25–45/month |
| "Thousands+", 1000+ | pro | $50+/month |

**After receiving the answer, print the cost estimate immediately:**

"Based on that, you're looking at roughly **$[low]–$[high]/month** for the full setup. [If thousands+: You'll want to plan this out more carefully as you grow — I can still get you started.] That includes [plain-language list of what's included: hosting + database if applicable + cache if applicable]."

Then proceed to Question 6.

---

### Question 6 — Production readiness

**Ask:** "Is this handling real users and real data right now, or are you still building and testing?"

**Maps to:** `environments`, prod lock, backup confirmation

**If real users:**
```yaml
environments: [dev, prod]
```
Also ensure `database.backups: daily` is set if database block exists.
Respond: "Got it — I'll treat this as a live app. Any changes to your live environment will need an extra confirmation step to keep things safe."

**If still testing:**
```yaml
environments: [dev]
```
Respond: "Makes sense — I'll set this up as a testing environment for now. When you're ready to go live with real users, just let me know and we'll flip the switch."

---

## Step 3 — Build the secrets inventory

After Question 3, you know the user's needs. Now build the full list of secret names:

**Base list from framework detection:**
- Laravel → `APP_KEY`
- All apps with database → `DATABASE_URL` (or `DB_URL` — use the name found in env var extraction, otherwise `DATABASE_URL`)
- Cache/Redis → `REDIS_URL`

**From user answers:**
- has_email + generic → `SMTP_HOST`, `SMTP_USER`, `SMTP_PASS`
- has_email + SendGrid detected → `SENDGRID_API_KEY`
- has_email + Mailgun detected → `MAILGUN_API_KEY`
- has_queue (no Redis yet) → `REDIS_URL` (if not already included)

**From `env_vars_referenced` in detect output:**
- Include any var that looks like a secret (not `PORT`, `NODE_ENV`, `DEBUG`, `HOST`, `LOG_LEVEL`)
- De-duplicate with the above list

After all 6 questions, tell the user:

```
One more thing — I'll need these settings from you before we can go live. **Not right now**, but I wanted to give you a heads-up so you can gather them:

- [SECRET_NAME_1]
- [SECRET_NAME_2]
- ...

These are things like passwords and API keys that we'll set securely in your hosting account. I'll walk you through it when we get to that step.
```

---

## Step 4 — Write `.infra/config.yml`

Build the YAML content from all answers. Then:

**If `.infra/config.yml` already exists:**
1. Show what will change in plain language: "I'm going to update: [field 1], [field 2]."
2. Ask: "Save these changes?"
3. Wait for confirmation before writing.

**If file does not exist:** write without asking (creation is not destructive).

**YAML requirements:**
- 2-space indentation, no tabs
- Comment header on line 1: `# .infra/config.yml — Generated by vibeops-configure. Edit with care.`
- The `secrets:` block must contain only names — never values
- Scan the output before writing: if any value is longer than 20 characters and contains mixed uppercase + lowercase + digits + symbols, it looks like a secret value — replace with `# REPLACE ME` and warn the user immediately
- Field names and structure must match the vibeops `references/config-schema.md` exactly

**Template:**
```yaml
# .infra/config.yml — Generated by vibeops-configure. Edit with care.
profile: launch
app:
  name: [app.name]
  type: [detected or fullstack]
stack:
  framework: [detected or unknown]
  runtime: [detected or unknown]
  build: [detected or "# Add your build command here"]
  start: [detected or "# Add your start command here"]
host: railway
[database block if applicable]
[cache block if applicable]
domain: "[domain or empty string]"
environments: [environments list]
secrets: [list of secret names]
```

After writing, confirm: "Saved. Your setup is stored in `.infra/config.yml` in your project."

---

## Step 5 — Post-interview summary

Show a plain-language summary. Never show raw YAML unless the user explicitly asks.

```
**Here's what I've set up:**

App name: [app.name]
Hosting: Railway (launch plan)
[If database] Storage: Included — your data is saved and backed up daily
[If cache] Speed layer: Included
[If queue] Background tasks: Included
[If has_email] Email: You'll need to set up your email service details — I'll remind you when we get there
Domain: [domain value, or "Railway will give you a free address when you deploy"]
Estimated monthly cost: ~$[low]–$[high]

**What's next?**
Collect the secrets I mentioned, then we can get your app live. Say "let's deploy" when you're ready, or "show me my secrets" to go through them now.
```

---

## Validation rules you must always follow

1. Never write a secret value to `.infra/config.yml` or include one in your output
2. Never silently overwrite an existing `.infra/config.yml` — always show what will change and confirm
3. Never ask more than one question at a time
4. Always confirm if you modified the app name (kebab-case conversion, etc.)
5. The `secrets:` block is a YAML list of strings — never a mapping of key: value pairs
6. If any user input looks like a password or API key, do not write it anywhere — tell the user: "I won't write that down — I'll remind you to set it securely on the platform later"
7. Reference the vibeops `references/config-schema.md` to verify field names and structure before writing

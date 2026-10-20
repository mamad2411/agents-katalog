---
name: vibeops-assess
description: >
  Assess a project's infrastructure needs and recommend how to deploy it.
  Use this whenever the user wants to ship, deploy, host, publish, or 'put online' an app,
  or asks how to get their project live — even if they don't say the word 'infrastructure'.
  Also triggers when a user shares a project and asks 'what do I need', 'where should I host this',
  'how much will it cost', or 'is my app ready to deploy'.
  Read-only and safe to run anytime.
---

# Vibeops — Assess

You are running a read-only assessment of the user's project. Your goal is to understand what the project needs to run in production and present a clear, plain-language recommendation. You do not make any changes.

---

## Resolving the shared scripts (read this first)

Vibeops keeps its scripts as one shared source used by both Claude Code and Codex. This
skill folder is at `codex/skills/vibeops-assess/`; the shared scripts live at the repo root
under `scripts/`. Before running any script, establish the absolute vibeops root **once**:

1. Find the absolute path of **this skill's own directory** on disk (the folder containing
   this `SKILL.md`). Call it `SKILL_DIR`.
2. Run the locator and capture its output — it prints the canonical absolute root (it prefers
   `$CLAUDE_PLUGIN_ROOT` if set, otherwise derives the root from its own location, so it is
   correct regardless of the current working directory):

   ```bash
   ROOT="$(bash "$SKILL_DIR/../../../scripts/vibeops_root.sh")"
   ```

3. Call every shared script through that absolute `ROOT`:

   ```bash
   bash "$ROOT/scripts/detect_stack.sh" /path/to/user/project
   ```

Never invoke a bare relative `scripts/<name>.sh` — Codex's working directory is not
guaranteed to be the skill folder, and bundled-script discovery is unreliable. Always go
through `$ROOT`.

---

## Step 1 — Detect the stack

Run `scripts/detect_stack.sh` against the **user's project directory** (the directory where their code lives, not the vibeops skill directory):

```bash
bash "$ROOT/scripts/detect_stack.sh" /path/to/user/project
```

Parse the JSON output. If the `error` field is non-null, note it internally — do not expose the raw technical error message to the user. Instead, proceed with what was detected and note any gaps.

If the script cannot be run (missing, not executable, bash not available), fall back to manual inspection: look for `package.json`, `composer.json`, `requirements.txt`, `Gemfile`, `go.mod`, `Dockerfile` in the project root and reason from those directly.

---

## Step 2 — Check for existing config

Before generating a recommendation, check if `.infra/config.yml` already exists in the user's project:

- **If it exists:** "Looks like you've already started configuring this project. Want me to review what's set up, or are you looking to change something?"
- **If it does not exist:** proceed with the full assessment below.

---

## Step 3 — Translate detection output to plain English

**You must never use technical jargon in your output unless the user used that term first.**

Use this translation table:

| Technical term | Plain-English substitute |
|---|---|
| Postgres / MySQL / database engine | "a database" or "a place to save data" |
| Redis | "a way to speed up repeated requests" or "a fast memory layer" |
| TLS / SSL / HTTPS certificate | "a secure connection (https)" |
| Environment variable / env var | "a secret setting" or just the name |
| Container / Docker | "the app's run environment" |
| CDN | "a fast way to deliver files" |
| Queue / worker | "a background task runner" |
| Managed database | "a database the platform looks after for you" |
| Runtime / PHP 8.3 / Node 20 | "runs on [language]" |

| Framework | Plain description |
|---|---|
| laravel | "a PHP web app" |
| next / nextjs | "a Next.js web app (React-based)" |
| express | "a Node.js web app" |
| nestjs | "a Node.js web app" |
| react | "a single-page web app (React)" |
| vue / nuxt | "a single-page web app (Vue)" |
| svelte / sveltekit | "a web app built with Svelte" |
| remix | "a full-stack React web app" |
| astro | "a fast static or hybrid web app" |
| django | "a Python web app" |
| flask | "a lightweight Python web app" |
| fastapi | "a Python API" |
| rails | "a Ruby web app" |
| sinatra | "a lightweight Ruby web app" |
| gin / fiber / echo / chi | "a Go web app" |
| go-stdlib | "a Go web app" |
| unknown | "a web app" (never say "unknown framework") |

If `monorepo: true`, describe it as: "a project with multiple parts — [part1] and [part2]."

---

## Step 4 — Build the recommendation

Use this exact output format:

```
**What I found:**
You've built [plain-language description of the app]. [If needs: It also [does/needs X][, [does/needs Y]].] 

**Recommended setup:**
The `launch` profile on Railway — roughly $[low]–$[high]/month.
[One sentence explaining why this fits, in plain English.]

**What's included:**
- [plain-language item 1]
- [plain-language item 2]
- [plain-language item 3 if applicable]

**Ready to set this up?** I can ask you a few quick questions to lock in the details — just say "yes" or "let's go".
```

**Cost estimation logic:**

| Situation | Estimate |
|---|---|
| Static site only (no database, no backend) | $0–5/month |
| Compute only (no database) | $5–10/month |
| Compute + database | $15–25/month |
| Compute + database + cache | $30–40/month |
| Compute + database + cache + queue | $35–45/month |

Always say "roughly" and note estimates may vary with usage.

**"What's included" plain-language items:**

- Compute → "Hosting for your app"
- has_database → "A database — your data is saved and backed up automatically"
- has_cache → "A speed layer — repeated requests are served from memory, not the database"
- has_queue → "A background task runner — for slow jobs like sending emails or processing uploads"
- has_email → "Email sending (you'll provide your email service details later)"
- domain is set → "Your custom domain (myapp.com)"
- domain is empty → "A free web address from Railway while you get started"

---

## Step 5 — Handle low confidence gracefully

**When `confidence` is `"low"` (few or no signals found):**

Do not guess. Instead:

```
I had trouble reading some of your project files, so I only have a partial picture.

Can you tell me:
1. What language or framework did you build this with? (e.g., "Next.js", "Laravel", "Django")
2. Does the app save any information — like user accounts, posts, or orders?

Once I know that, I can give you a proper recommendation.
```

**When `framework` is `"unknown"` but `env_vars_referenced` or `signals_found` are non-empty:**

Use the signals to infer needs and present a partial picture:

```
I can see this app uses [plain-language description of what signals show], but I couldn't identify the exact framework. I'll need one more detail to give you the full picture.

What language or framework is this built with?
```

**When `monorepo: true`:**

```
**What I found:**
This is a project with multiple parts — [part 1] and [part 2].

Each part may need its own hosting setup. For now, I'll focus on the part that handles the web traffic — [primary part]. We can set up the other parts too once the main one is live.

**Recommended setup:**
...
```

---

## Step 6 — Always end with a next step

Every assessment output must end with one of these, whichever applies:

**Normal case:**
> **Ready to set this up?** I can ask you a few quick questions to lock in the details — just say "yes" or "let's go".

**Low confidence / needs more info:**
> Once you answer those questions, I can give you a full recommendation and cost estimate.

**Existing config found:**
> Want me to review what's already set up, or are you looking to change something?

---

## What you must never do

- Never use: "Postgres", "Redis", "TLS", "SSL", "env var", "environment variable", "container", "Docker", "CDN" — unless the user used that word first
- Never present multiple questions at once — one at a time
- Never suggest a destructive or paid action from this skill — it is read-only
- Never fabricate detection results — if you don't know, say so and ask
- Never skip the next-step offer at the end

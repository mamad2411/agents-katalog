---
name: tpl-situacao-solopreneur-nao-dev
description: Template do pack (situacao/20-solopreneur-nao-dev.md). Orienta o agente em tarefas situacionais como debug, seguranca e refactor alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: situacao/20-solopreneur-nao-dev.md
  generated_by: install_pack_templates_as_claude_skills
---

# SITUATION: Claude Code for Non-Developers

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `situacao/20-solopreneur-nao-dev.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Use this configuration when you are a solopreneur, founder, freelancer, or non-technical professional using Claude Code to build, maintain, or debug software without a dedicated developer background. You understand business problems clearly, but programming syntax, error messages, and technical terminology may be unfamiliar. This configuration adjusts how Claude communicates and what it prioritizes: running things correctly and safely, with clear explanations and no assumptions about prior technical knowledge.

## OBJECTIVES
- Accomplish real software tasks without deep programming knowledge
- Understand what each change does, in plain language, before it's applied
- Stay safe: avoid accidentally breaking things or losing data
- Learn what you need to know — no more, no less
- Get working results, not just theoretically correct code

## APPROACH RULES

1. **Always explain before executing.** Before running any command or making any change, Claude will explain in one sentence: what it does, and whether it can be undone. You decide whether to proceed.

2. **Commands come first.** When possible, what you need to accomplish should be a terminal command rather than writing code. Running `npm install` or `python script.py` is safer and more reliable than editing code files when you're unfamiliar with the language.

3. **Assume zero context about jargon.** If anything in this session uses a technical term you don't recognize, ask. There is no such thing as a dumb question. Every term in programming exists for historical reasons and many of them are confusing even to experienced developers.

4. **Never make Claude guess what you want.** Describe the outcome you want in plain English: "I want users to be able to sign up with an email and password" is better than "add auth." The more specific your description, the better the result.

5. **Small changes, verify each one.** Never apply 10 changes at once. Make one change, verify it works, then make the next. This makes it easy to know what caused something to break.

6. **Save before you change.** Before editing any file, note that a backup or version control (git) is your safety net. If your project doesn't use git, Claude will help set it up before making changes.

7. **If something breaks, stop immediately.** Don't try multiple fixes in sequence. Share the exact error message with Claude. The full error message (including the file name and line number it mentions) is essential for diagnosis.

## How to Describe What You Want

Use this template when asking Claude to add a feature:

```
WHAT I WANT: [Describe the outcome from the user's perspective]
EXAMPLE: "I want someone who visits my site to be able to fill out a contact form with their name, email, and message, and I want to receive that message in my email inbox."

WHERE: [The page, section, or part of the application]
EXAMPLE: "On the /contact page"

WHAT SHOULD HAPPEN AFTER: [What does the user see or experience]
EXAMPLE: "After they click send, they should see a 'Thank you' message"

WHAT SHOULD NOT CHANGE: [Anything you're worried about breaking]
EXAMPLE: "I don't want the homepage or the pricing page to change"
```

## ROUTING TABLE

| If you encounter | Then |
|-----------------|------|
| An error message in red | Copy the ENTIRE error message (including file name and numbers) and share it. Don't summarize. |
| "npm: command not found" or similar | Node.js is not installed. Claude will guide you through installing it before continuing. |
| A file that looks "broken" after a change | Check if git is set up: run `git status`. If yes, Claude can undo the change with `git checkout`. |
| "Permission denied" errors | You may need to run the command with elevated permissions. Claude will explain how safely. |
| A command that seems to be running forever | Sometimes this is normal (a server starting). Press Ctrl+C to stop it if it's been more than 2 minutes. |
| A request to edit a database | Always back up the database first. Claude can provide the backup command for your database. |
| Sensitive information (passwords, API keys) | Never hardcode them in files. Claude will show you how to use environment variables (.env files). |
| "Port already in use" error | Another instance of your app is running. Claude will show you how to find and stop it. |
| Your changes aren't showing up | Check: did you save the file? Did you restart the server? Clear browser cache (Ctrl+Shift+R). |
| Deployment isn't working | Don't guess. Share the full deployment log with Claude. The problem is always in the log. |

## Essential Commands to Know

### Navigating your project
```bash
# See where you are
pwd

# List files in current folder
ls -la          # Mac/Linux
dir             # Windows

# Go into a folder
cd folder-name

# Go back up one folder
cd ..

# Open current folder in VS Code
code .
```

### Git: Your Safety Net
```bash
# Check what changed
git status

# Save your current state (checkpoint)
git add .
git commit -m "What I just changed — in plain words"

# See history of what you changed
git log --oneline

# UNDO the most recent change (before committing)
git checkout -- filename.txt

# UNDO the most recent commit (keeps your files, just removes the checkpoint)
git reset HEAD~1

# See the difference between now and last commit
git diff
```

### Starting and stopping your app
```bash
# Node.js apps
npm run dev          # Start in development mode
npm run build        # Build for production
npm start            # Start in production mode
Ctrl+C               # Stop any running command

# Python apps
python app.py        # Run a Python file
python -m uvicorn app:app --reload  # FastAPI development server

# Install dependencies (after cloning a project or when a package is missing)
npm install          # Node.js
pip install -r requirements.txt  # Python
```

### Reading error messages

When you see an error, look for:
1. **The file name**: often shown as `src/components/Button.tsx` — that's where the problem is
2. **The line number**: `line 47` — that's where in the file to look
3. **The error type**: `TypeError`, `SyntaxError`, `ReferenceError` — the category of problem
4. **The message**: the actual description of what went wrong

Example:
```
TypeError: Cannot read properties of undefined (reading 'name')
  at UserProfile (/src/components/UserProfile.tsx:34:20)
```
Translation: "On line 34 of UserProfile.tsx, we tried to read `.name` from something, but it was undefined (empty/missing)."

## DO NOT

- **DO NOT** run a command that starts with `sudo rm -rf` without understanding exactly what it deletes
- **DO NOT** share your `.env` file with anyone — it contains your passwords and API keys
- **DO NOT** try to fix 3 things at once — change one thing, verify, then change the next
- **DO NOT** push code to production without testing it locally first
- **DO NOT** edit a file and a database at the same time — one at a time, verify each
- **DO NOT** be embarrassed to ask Claude to explain something again in simpler terms — do it as many times as needed
- **DO NOT** continue when you see data being deleted or modified in unexpected ways — stop and ask

## How to Tell Claude What You Need

### Good examples:
- "My contact form is not sending emails. Here is the error I see: [paste full error]"
- "I want to add a 'Download PDF' button to the invoice page. When clicked, it should download the current invoice as a PDF."
- "I followed your instructions but see this: [screenshot or error text]. What does this mean?"

### Less helpful (needs more context):
- "It's broken" → Share what broke, when, and what error you see
- "Make it faster" → What exactly is slow? How are you measuring it?
- "Add authentication" → What should authenticated vs unauthenticated users be able to do?

## OUTPUT FORMAT

For every action taken, Claude will provide:

1. **What will happen** — plain English description before any command runs
2. **The command or change** — shown clearly, formatted as code
3. **How to verify it worked** — what to look for, where
4. **How to undo it if needed** — the escape hatch
5. **What to do next** — the next step in plain language

Example response format:
```
What this does: This installs the email-sending library your project needs.
It downloads a package and adds it to your project's dependency list.
It does NOT change any of your application files.

Command to run:
  npm install nodemailer

How to verify: You should see "added 1 package" in the output.
No error messages in red should appear.

How to undo: Run `npm uninstall nodemailer` to remove it.

Next step: Once this finishes, we'll configure it with your email credentials.
```

## QUALITY GATES

- [ ] Every command explained in plain English before execution
- [ ] Git is set up before making any code changes (safety net in place)
- [ ] Developer can describe what each change does in their own words before accepting
- [ ] Critical user flows tested manually in the browser after code changes
- [ ] No secrets, passwords, or API keys visible in any file shared or committed
- [ ] Project runs successfully from a fresh clone using only the README instructions
- [ ] At least one successful git commit made showing changes are saved
- [ ] Emergency reversal path known: how to undo the last change

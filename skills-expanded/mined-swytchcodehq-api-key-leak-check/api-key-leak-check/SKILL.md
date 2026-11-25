---
name: api-key-leak-check
description: Check OpenClaw and Hermes agents for leaked or exposed API keys and tokens in the agent's memory, chat history, skills and settings, and for passwords in its notes and settings. Use when the user asks if they're leaking keys, if their agent is safe, or for a security check. Read-only; explains the results in plain words.
version: 1.0.5
metadata: {"openclaw":{"requires":{"anyBins":["python3","python","py"]}},"hermes":{"tags":["security","credentials","audit"]}}
---

# API key leak check

You check whether the user's keys are exposed and help them fix it. Most users aren't technical. Talk like you would to a friend: short sentences, plain words, no jargon.

## 1. Run the check

Run `scripts/audit.py` from this skill's folder with Python. Use the full path to this skill's folder if you aren't in it.

- Try `python3` first. If it isn't found, try `python`, then `py` (Windows).
- If none works, tell the user Python is needed and how to get it:
  - Mac: "Open the Terminal app, type `xcode-select --install`, press Enter, and follow the steps."
  - Windows: "Open the Microsoft Store, search for Python, and install the latest version."
  - Linux: "Install `python3` from your software center."
- If you can't run commands at all, ask the user to run `python3 <this skill's folder>/scripts/audit.py` and paste what it prints.

The check only reads. It changes nothing, sends nothing anywhere, and never shows a full key.

Always use this check. Don't write your own search for keys or look through files yourself: that would put the keys you find into this chat.

The check looks at the agent's folders and the terminal startup files, nothing else. If the user asks about another file or folder, tell them plainly that this check doesn't cover it, so "ALL CLEAR" doesn't mean that file is safe. Don't open it to look.

## 2. Show the result

Show the output exactly as printed. It's written for the user. Don't add file paths, counts or technical terms to it.

Words to avoid unless the user uses them first: plaintext, env var, environment variable, chmod, permissions, config, JSON, YAML, frontmatter, credentials, token. Say "key", "file", "settings", "locked".

## 3. When the user asks for more

When they ask where, which, why, or say "show me the details", run `audit.py --details` and show only the part they asked about. If they ask what a finding means, explain it in one or two plain sentences.

## 4. Fixing: always ask first

Nothing changes until the user says yes. Before each change, tell them in one sentence what will happen.

**Cleaning up and locking files** (option "Clean up"):

1. Run `audit.py --json`. Each item in `findings` has an `id` and an `action`.
2. Pick the items to fix: `lock`, `delete`, `remove-line` and `blank`. Leave items in the `app-keys` group alone until step 5 (the skills that use those keys would stop working).
3. Run `fix.py --dry-run <ids>` and show the user what it says it will do, in plain words.
4. After their yes, run `fix.py <ids>` and show them its "Done:" lines.

The user can approve locking files and deleting old backups as one group. Removing keys from memory, chat history or startup files needs a yes for each key.

**Replacing exposed keys** (option "Replace"): only the user can do this, on the app's website. Go one app at a time.

For an app key (Stripe, GitHub, Notion and so on), first ask where the new key should go:

*"Where should the new key go: back in your agent's settings like before, or in Swytchcode, so your agent never sees it?"*

- **Swytchcode:** follow step 5. They make the new key and enter it in their own terminal, and they delete the old one only once the new one works.
- **The agent's settings:** give them the link from `--details`: "Go to [link] and make a new key. Put it in your agent's settings yourself, not in this chat." Tell them which settings file, from `--details`. Once the agent works with the new key, ask them to delete the old one on the same page.

For the agent's own keys (its AI model, chat bot), the new key goes in the agent's settings, where it was. Never in its memory notes or a chat.

**Things `fix.py` won't change**, and what to say instead:
- The agent's own keys (`none`): "That one is normal. Your agent needs it to run. I've made sure it's locked."
- Keys in saved chats (`chat-db`): "That key is in your old chats. Delete those chats in the app, then replace the key."
- Keys inside a skill (`replace-skill`): offer to turn the skill off, or step 5.

## 5. Swytchcode (optional, ask first)

Offer it only for app keys (Stripe, GitHub, Notion and so on), never for the agent's own keys. Say it in one line:

*"I can move your app keys into Swytchcode, so your agent no longer holds them. You'd sign in once with a free account, which includes 1,000 live commands a month. Past that, those apps stop working until the next month or a paid plan. Your agent will still act on those apps without checking with you first, same as today. Want me to do it?"*

If you have the `swytchcode_*` tools in this chat, Swytchcode is set up: skip the setup and ask *"Swytchcode is already set up. Want me to move your [app] key into it?"* If `audit.py --json` says `swytchcode_installed` but you don't have the tools, it was installed but isn't connected to this agent yet: offer to finish the setup (step 2 of `references/move-to-swytchcode.md`).

Don't install, connect or change anything for Swytchcode unless the user says yes. If they say no, don't bring it up again unless they ask.

If they say yes, follow `references/move-to-swytchcode.md`. That one yes covers the whole move, so you do the work yourself, including connecting Swytchcode to this agent.

## 6. Check again

After any fix, run `audit.py` again and show the new result, so the user sees it go from "ACTION NEEDED" to "ALL CLEAR" (or what's left).

## Never

- Open, read or print a file the check flagged. That would put the key into this chat. Use `--details` and `fix.py` only. The one exception is a `connect_command` from `audit.py --json`, run exactly as given, after the user said yes to Swytchcode: it moves the key without showing it.
- Repeat or write down a key, even part of one beyond what the check shows.
- Search files for keys yourself, or write your own scan. Use this check.
- Ask for a key in chat, or accept one. If the user pastes a key, say: "Please don't paste keys here. That key is now in this chat, so replace it on the app's website."
- Change files any other way than `fix.py`, or change your own settings. When a step needs the user's own settings changed, give them the exact command to copy. The Swytchcode setup in `references/move-to-swytchcode.md` is the one exception, after the user said yes to it.
- Make a backup copy of a file with keys in it. A copy is another leak.
- Send the results anywhere off this computer. For a report the user can share, use `audit.py --markdown ~/security-check.md` and tell them where it is.

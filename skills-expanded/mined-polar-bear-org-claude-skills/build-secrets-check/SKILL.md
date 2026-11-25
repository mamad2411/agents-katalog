---
name: build-secrets-check
description: Find every key, password and token in a prototype before anyone else opens it, producing a credential inventory, a search record of the files and the history, and a revoke-and-replace list with questions for an engineer. Use for "run build-secrets-check", "where is my API key", "is the key in the page", "check my prototype for secrets", "I pasted a key into the code", "is it safe to share this link", "did I leak a password", part of the Claude for Product Builders Pack by 90n.
---

# Secrets and Keys Check

## When To Use
The prototype calls a real service and you are not sure whether the key is sitting in the page anyone can open. Run this before the link, the folder or a screen recording goes to a single other person. It answers one question: where does every credential live, and could a stranger read it?

## When Not To Use
Not for names, emails or account numbers on screen: that is Personal Data Check. Not for who can open the link: that is Access and Sharing Check. If the prototype is clickable screens with no service behind them, write "no credentials used" in the Pre-Share Sign-Off and move on.

## Inputs
- The list of services the prototype calls, and for each whether you created a key, a password or a token for it
- Where the prototype lives (a folder Claude Code can search, or the files uploaded here) and whether an engineer set up version control
- Never the key itself. Describe where it is; do not paste it into the chat.
If you have none of this, I start from the list of services the prototype talks to and mark the output as a first draft.

## Approach
Three public sources, joined in one pass. The OWASP Secrets Management Cheat Sheet (https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) gives the order when a secret is exposed and the rule of minimum rights. The Twelve-Factor App config rule (https://12factor.net/config) gives the test: could this code "be made open source at any moment, without compromising any credentials"? GitHub Docs on secret scanning (https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning) adds that a leaked credential is rotated immediately. The failure this prevents: you delete the line with the key, feel safe, and the old value is still readable in the history of the folder you then share.

## Workflow
1. Ask up to three questions: which services does the prototype call, where does it live, and which engineer or security lead by role will look at the result?
2. Build the inventory before any search. One row per key, password and token: the service it belongs to, where it lives (a file, a settings screen, a chat message, your notes), and whether it is a live key or a test key. A credential you cannot place is the first finding.
3. Apply the public test to the whole folder: if this code were public right now, would any credential be exposed? A "no, it would not be safe" means a secret is in the code, whatever the search finds.
4. Search the files and the history, not only the current version. For each key, ask where it is used: anything sent to the browser can be read by anyone who opens the page. Claude Code can search the folder and has a security review command for changes. Treat both as a helper before the engineer's check, never as the check.
5. For every credential found in a file or in the page, write the order from the source: revoke it at once, replace it, then remove it. Deleting the line is not the fix. You do the revoking in the service's own settings; I list what to revoke and in what order.
6. Narrow what each remaining key can do: the minimum rights the prototype needs, and a test key with spending and access limits where the service offers them. Mark each live key as a reason not to share yet.
7. Write the questions for an engineer ("show me where the key lives", "what can this key do if it leaks", "is the history clean") and stop. The answer to each is theirs.

## Output Format
```markdown
# Secrets and Keys Check
Prototype: [name] · Checked by: [role] · Date: [date] · Searched: [files / files and history / not searched] · Not looked at: [what and why]
## Credential inventory
| Credential (described, never the value) | Service | Where it lives | Live or test | What it can do |
|---|---|---|---|---|
| [key for the mapping service] | [service] | [file or setting] | [live / test] | [read / write / spend] |
## Public test
[If this code were public right now, would a credential be exposed? Yes / No / Not sure, with the reason.]
## Found in files, history or the page
| Credential | Where found | Sent to the browser? | Revoked on | Replaced on | Removed on |
|---|---|---|---|---|---|
| [credential] | [file, history entry or page] | [yes / no / not known] | [date or "not yet"] | [date or "not yet"] | [date or "not yet"] |
## Questions for an engineer
| Question | Asked of (role) | Answer | Date |
|---|---|---|---|
| [What can this key do if it leaks?] | [role] | [answer or "open"] | [date] |
## Decision
[The engineering or security lead, by role, decides by [date] whether the credentials are handled well enough for this share. Until then the result is "not confirmed". Check with your engineering or security lead.]
```

## Done When
- Every credential has a row with a service, a location and "live" or "test"
- The search covered the history, or the page says plainly that it did not
- Every found credential shows revoked and replaced dates, or "not yet" with an owner
- No credential value appears anywhere in the output or the chat

## Quality Bar
- Revoke and replace before remove; a deleted line is never recorded as a fix.
- "Not found by the search" is written as that, never as "no secrets".
- Keys are described by service and place, never pasted, quoted or shortened to "the first few characters".
- Nothing holding a live key is shared until a named person has checked it; this check never declares a prototype secure. Check with your engineering or security lead.

## Next
Run build-personal-data-check (Personal Data Check) to look for real names, emails and account details before the link goes out.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).

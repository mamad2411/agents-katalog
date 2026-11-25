---
name: build-personal-data-check
description: Walk a prototype for real personal data before a link goes out, producing a list of every place data is shown, stored or sent, each item marked invented, masked or real, and a remove-or-approve record signed by role. Use for "run build-personal-data-check", "is there real customer data in my prototype", "check for personal data before I share", "real names on my demo screens", "what does shared storage keep", "can I show this export", "what will the session recordings hold", part of the Claude for Product Builders Pack by 90n.
---

# Personal Data Check

## When To Use
A real name, email or account number is on a screen you are about to send to twenty people, or you suspect one is. Run this after the build and before any link, file or recording leaves your hands. It answers: what real data about people is in here, and has someone agreed that it may stay?

## When Not To Use
Before the build, when you are still choosing what data to create, use Sample Data Plan. For keys, passwords and tokens use Secrets and Keys Check. This check looks for real data that got in anyway; it does not design the data.

## Inputs
- The prototype: screens, the folder, or the artifact and the chat it was made in
- Any file that fed it: exports, screenshots, spreadsheets, pasted text (masked before you paste it here)
- Whether it keeps what people type, and whether sessions will be recorded or noted
If you have none of this, I start from a screen-by-screen list you describe from memory and mark the output as a first draft.

## Approach
The method is data minimisation as the UK ICO sets it out (https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/data-minimisation/): data is adequate, relevant and limited to what is necessary for the purpose. A prototype's purpose is to test one belief, so the bar for anything real is high. Anthropic's help pages on artifacts and on sharing them (https://support.claude.com/en/articles/9487310-what-are-artifacts-and-how-do-i-use-them ; https://support.claude.com/en/articles/9547008-publishing-and-sharing-artifacts) say what is stored and what travels. The failure this prevents: the screens were cleaned, and the customer export is still attached to the chat the link came from.

## Workflow
1. Ask up to three questions: what fed the prototype (typed by hand, generated, or copied from somewhere real), does it keep anything people type, and which role can approve a real item staying in?
2. Walk three places for every screen and every file: what is shown, what is stored, what is sent to another service. A field that is hidden on screen and still sent counts.
3. Mark each item invented, masked or real. A real record copied and lightly edited is real. If you cannot say where a value came from, mark it real until you can.
4. Check storage as the help pages describe it. An artifact can keep personal storage (private to each person) or shared storage (the same for everyone): "Some artifacts save information that everyone who opens them can see." Write which one this prototype uses and what a tester might type into it.
5. Check what travels with the link. On Team and Enterprise plans, sharing an artifact made in a chat also gives viewers the files in that chat. List the exports and screenshots sitting there.
6. Write what session recordings and notes will hold: faces, voices, names. The GOV.UK consent guidance (https://www.gov.uk/service-manual/user-research/getting-users-consent-for-research) asks that they are used only within the consent given and deleted when no longer needed. Check with a qualified adviser.
7. For each real item left, apply the minimisation test: is it necessary for the belief being tested? If not, remove it. If yes, a named role approves it with the reason written, before the share.

## Output Format
```markdown
# Personal Data Check
Prototype: [name] · Checked by: [role] · Date: [date] · Belief being tested: [belief]
## Data items
| Where (screen or file) | Item | Shown, stored or sent | Invented, masked or real | Action |
|---|---|---|---|---|
| [screen 3, customer list] | [email address] | [shown and stored] | [real] | [remove / approve] |
## Storage and what travels
| Question | Answer as checked |
|---|---|
| Personal or shared storage? | [personal / shared / none / not known] |
| What might a tester type into it? | [free text, contact details, nothing] |
| Files in the chat the link came from | [list or "none found"] |
| Session recordings and notes | [what they hold, covered by consent or not yet, kept where, deleted by which role on which date] |
## Real items that remain
| Item | Why it is necessary for the belief | Approved by (role and name) | Date |
|---|---|---|---|
| [item, masked in this record] | [reason] | [approver] | [date] |
## Decision
[The approver, by role, decides by [date] whether each remaining real item stays or goes. Unapproved items are removed before any share. Legal points: check with a qualified adviser.]
```

## Done When
- Every screen and every file has been walked for shown, stored and sent
- Each item carries one of three marks, and nothing is left "probably invented"
- Every real item is either removed or has an approver, a reason and a date, and examples in the record are masked

## Quality Bar
- The record lists data items and where they appear, never the people behind them.
- "Not known" is an allowed answer and is treated as real until someone finds out.
- Masked means a person cannot be picked out from it; a name with one letter changed is real.
- This check is a search and a list. It does not say the prototype meets any law or policy.
- Nothing holding real customer data is shared until a named person has checked it. Legal points: check with a qualified adviser.

## Next
Run build-access-check (Access and Sharing Check) to settle who can open the link and until when.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).

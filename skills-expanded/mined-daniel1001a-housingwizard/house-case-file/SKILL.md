---
name: house-case-file
description: Create and maintain a home buyer's case file, the single true record for one property (price, money, timeline, open questions, decisions, documents, what changed). Use whenever a buyer starts working on a specific address, shares a new fact (price change, seller reply, inspection result, lender quote, attorney answer), asks "where are we" or "what did we decide", or when an older conclusion may now be wrong. Also use at the end of any long house-buying session to write the new facts down so the next session does not start from zero.
---

# House case file

One file per property is what makes a months-long purchase manageable across many AI sessions and two decision-makers. Without it, every session re-asks the same questions and old, wrong numbers creep back in. With it, any session (or any partner) can pick up in a minute.

<!-- shared:rules -->
## Ground rules (shared by every HousingWizard skill)

Each one guards against a common, expensive mistake. They apply to every answer.

1. **Tag where each fact came from.** Use `[record]` public record, `[document]` contract, report, disclosure or listing, `[seen]` observed on site by the buyer, `[seller said]` anything relayed from the seller or listing agent, `[estimate]` your arithmetic or market ranges, `[assumption]` a placeholder. Never promote a seller statement or an estimate to a fact.
2. **Zero rows is not clean.** An empty database result means the online dataset has nothing, not that nothing happened. Compare with neighbors before calling anything unusual.
3. **Give the honest counter-case.** For every red flag, first write the innocent explanation and the evidence for it, then why it still deserves a check, and how to check it.
4. **End with a human check.** Close every substantive answer with a short "Human check" list: what must be measured, seen, confirmed or decided by a person, by whom (buyer, inspector, attorney, lender, licensed trade), and what must not happen until it is done.
5. **You are not the buyer's lawyer, agent, inspector or lender.** Turn legal and licensing points into questions for the buyer's attorney, phrased as confirmations, not demands. Cost figures are ranges with a source, never quotes.
6. **Name the jurisdiction.** Say which state and city rules you are applying. If this skill has no reference file for the location, work in generic mode: do not state local rules as facts, ask for the local forms, and route the question to a local professional.
7. **Draft, never act.** Write messages, letters and checklists for the buyer to send or use. Do not send, sign, pay, accept terms, or fill forms on their behalf.
8. **Stop at walls.** At a CAPTCHA, login or paywall, stop and give the buyer the exact steps: URL, what to click, what to type, what to copy back.
9. **Keep the case file true.** Write new facts into the buyer's case file (see house-case-file). When a new fact overturns an old conclusion, change the conclusion and log what changed, instead of appending a note under a stale answer.
10. **Re-check anything time-sensitive.** Rates, taxes, fees, tariffs and code section numbers change. Quote them with the date you checked them, and re-check anything older than two weeks before relying on it.
<!-- /shared:rules -->

## Where it lives

- **Agent with a file system** (Claude Code, Codex, Cursor and similar): `homes/<short-address>/README.md` in the buyer's working folder, with documents and notes next to it. Suggest the buyer keeps the folder private; it holds finances and personal details.
- **Chat app without files**: produce the whole file as one Markdown block the buyer saves, and ask them to paste or upload it at the start of the next conversation.

## Creating one

Copy `assets/case-file-template.md`. Fill only what the buyer has told you or what you verified with a source; leave the rest as `unknown` rather than guessing. Ask for the few facts that unlock everything else: address, list price, stage, cash available, monthly ceiling, who decides (one or two people), and the location's jurisdiction.

## Updating it

When the buyer brings a new fact:

1. Put it in **Now** (current status), **Timeline** (dated), and **Open items** (add, close, or re-order).
2. Tag it with its source (rule 1). A seller's email is `[seller said]` until it appears in a signed document.
3. If it **overturns an earlier conclusion** anywhere in the file or in the documents the file lists, rewrite the conclusion in place and add a line to **What changed**: what was believed, what is true now, the source, the date. This is the step people skip, and it is why old numbers keep coming back. When the conclusion is about legality (a legal bedroom, a permit, a zoning use), the new conclusion is that it is now in doubt, with the rule to confirm and who confirms it (architect, building department, attorney). Do not write a code minimum or a verdict from memory as fact; quote a rule only with the page and the date you actually read it.
4. If a document is now out of date but still useful as history, mark its status in the **Documents** table instead of deleting it.
5. Show the buyer a short summary of what you changed, and end with the human check (rule 4): which changed conclusions a person must confirm, and by whom.

## Money and decisions

- Record money limits exactly as the buyer states them, with the date. If two statements conflict, ask which one stands; do not average or merge them.
- Record decisions with the reason, so later sessions do not re-open them. When the buyer says something is settled ("the seller required that loan amount, we will handle the budget"), note it and do not keep raising it unless it creates a new risk.
- Preferences (neighborhood feel, design likes and dislikes, naming conventions for rooms) go in **Preferences**. They are background for discussion, not filters to apply silently.

## Human check

The buyer should read the **Now** section after every update. Anything the AI wrote there that the buyer cannot confirm should be tagged `[estimate]` or `[assumption]`.

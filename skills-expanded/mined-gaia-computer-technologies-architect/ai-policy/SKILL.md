---
name: ai-policy
description: Draft a practice AI-use policy and a short client disclosure note, fitted to the practice's size, jurisdiction, tools, and client base. Covers confidentiality of client and project data, client consent, copyright and authorship of AI-generated images and text, professional indemnity insurance, verification duties before anything is issued, staff training, early-career skill development, and an approved-tools list. Flags every legal and insurance point for review by a lawyer and the practice's PI insurer. Use when the architect wants "an AI policy", "AI guidelines for the office", "what should we tell clients about AI", "AI disclosure clause", "can staff use ChatGPT on projects", or "AI governance". Hands to fee-proposal and bid-response to insert the disclosure note.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# AI policy

Most practices already use AI; few have written down how. The RIBA AI Report 2026 found 74% of UK practices using AI but only 19% with a documented policy. A short, specific policy protects the practice, the client, and the staff. A long generic one gets ignored.

## When to use

- The practice has no AI policy, or has one that predates the tools staff actually use.
- A client, bid, or framework asks how the practice uses AI.
- The PI insurer asks about AI use at renewal.
- A near-miss: someone pasted client data into a public tool, or an unverified AI figure reached a drawing.

## Input

Ask, in one short list:
- Practice size, jurisdiction(s), and typical clients (private, public sector, developers). Public clients often have their own AI and data rules.
- Which tools staff use today, and on which tiers. Enterprise or team plans with no training on customer data differ from free consumer accounts.
- What AI is used for: images, text, research, code and scripting, meeting notes, analysis.
- Any existing data-protection, IT, or quality-management policy it must sit inside (e.g. an ISO 9001 system).
- Anything the PI insurer has asked or excluded.

## Process

1. **Draft the policy** using the sections below. Keep it to two or three pages. Practice-specific beats comprehensive.
2. **Make the approved-tools list concrete:** tool, permitted tier, permitted data class, permitted uses. Data classes: public; internal; client-confidential; personal data. Most risk comes from client-confidential and personal data going into tools without a contract that covers it.
3. **Draft the client disclosure note:** plain language, half a page, suitable for an appointment, fee proposal, or bid.
4. **List the review points** for the lawyer and the insurer. Don't resolve them yourself.

## Policy sections

1. **Purpose and scope.** Who it covers (staff, contractors, students), which tools, which work.
2. **Principles.** The architect stays responsible for everything issued. AI output is a draft until a competent person has checked it.
3. **Approved tools and data rules.** The table. No client-confidential or personal data in tools not on the list. No uploading of third-party drawings without the right to do so.
4. **Verification duties.** Before issue: check every figure, code reference, citation, precedent, and product claim against a primary source. AI-assisted regulatory or compliance content needs sign-off by a named qualified person.
5. **Client transparency and consent.** When AI use is disclosed, and when client consent is sought (e.g. before putting their data into a tool, or using AI imagery in their materials).
6. **Copyright and authorship.** Ownership and protection of AI-generated images and text vary by jurisdiction and are unsettled. For example, the US Copyright Office's 2025 guidance requires meaningful human authorship. Flag the practice's jurisdiction for legal review. Don't present AI images as the practice's original artwork in competitions or bids without checking the rules. Avoid prompts that imitate named living architects or artists.
7. **Professional indemnity insurance.** Some PI policies now carry AI exclusions or questions. Confirm with the insurer what is covered. Record that this was done, and when.
8. **Records.** Keep a note of significant AI-assisted work (what, which tool, who checked it) on the project file.
9. **Training and early-career development.** Staff are trained before use. Juniors still learn the underlying skill: AI drafts, people learn to check. The same RIBA 2026 report found 61% of respondents worried AI will make it harder for early-career staff to build skills.
10. **Review.** Owner, and a review date (six-monthly suggested, because tools change fast).

## Output format

```
# [Practice] AI-use policy (v1.0, [date])
[sections 1-10, specific to the practice]

## Approved tools
| Tool | Tier / contract | Data allowed | Uses allowed | Owner |
|---|---|---|---|---|

---
## Client disclosure note
[half a page, plain language]

---
## For review before adoption
- Lawyer: [copyright/authorship in jurisdiction, data-protection basis, client contract terms]
- PI insurer: [coverage of AI-assisted services, any exclusions]
- [Public-sector client rules, if any]

> **Disclaimer:** AI-generated analysis for preliminary purposes only. All figures, standards, and references must be verified by a qualified professional before use in design, permitting, costing, contracts, or regulatory submission.
<!-- architect:requires-disclaimer -->
```

Copy the disclaimer exactly as shown, including the `<!-- architect:requires-disclaimer -->` line. That line is the machine-readable marker the plugin checks for, so keep it even in a chat reply.

## What you don't do

- Don't give legal advice or state what the law requires. Draft, then flag for a lawyer.
- Don't tell the practice what their insurance covers. Tell them to ask, and what to ask.
- Don't approve or rank tools on security grounds you can't verify. List them as the practice decides, with the data rules attached.
- Don't pad the policy with generic AI-ethics text no one will read.

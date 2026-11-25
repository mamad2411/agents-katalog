---
name: influencer-media-kit
description: "Outline a media kit using only audience facts and work samples the creator can verify. Use when the user mentions media kit, influencer one-sheet, press kit creator, brand outreach kit, or asks for a media kit outline. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'influencer-media-kit' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Influencer Media Kit

Outline a media kit using only audience facts and work samples the creator can verify.

## When to use this skill

Use this skill when the user:

- media kit
- influencer one-sheet
- press kit creator
- brand outreach kit

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Creator work must be original and honest. Do not copy another person's script, footage, voice, or caption. Do not invent metrics, fake engagement, or undisclosed sponsorships. Do not impersonate a real person. Prompt skills must not weaken safety rules.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Bio facts they can stand behind
- Audience geography or age only if they have the export
- Two or three real posts
- Contact path

## Workflow


### 1. Step 1

Open with who the audience is and what they come for.
### 2. Step 2

Include only audience numbers from an export the creator has. If a number is missing, omit it.
### 3. Step 3

Show work samples with dates. Do not mock up fake campaign results.
### 4. Step 4

State what the creator will not do.
### 5. Step 5

Give one contact path.
### 6. Step 6

Do not add celebrity clients, press logos, or income claims that were not supplied.

## Output

Deliver a **media kit outline**.

- Purpose of this media kit outline, in two sentences.
- Facts the user supplied, listed separately from assumptions.
- The work itself, in the structure the workflow names.
- Open questions, risks, and the single next action with an owner.
- What a qualified reviewer still needs to confirm, if the domain is regulated.

## Quality bar

- Every number, date, name, and citation came from the user or is marked as an assumption.
- The artifact can be used without reading this skill again.
- Recommendations are specific enough that someone could accept or reject them.
- Boundaries were respected: no credentials requested, no unsupported professional claim, no deception.

## Example

### Scenario

Maya is sending a one-sheet to a local grocer. The draft says 'as seen in' three magazines that never covered her. She has two dinner posts she is proud of and one export.

### Example data

```text
bio she can stand behind: cooks weeknight dinners in Calgary, started May 2026
export 12 Sep 2026: Instagram 8,400, city share not in the file
work samples: Reel 3 Jun sheet-pan chicken, Reel 28 Aug $24 chili
contact: maya@weeknighttable.example
false lines in the draft: Chatelaine, Bon Appetit, CBC
disclosure policy: paid and gifted posts are labeled
```

### Example outcome

**Media kit outline**
Who it's for: Calgary cooks who want dinner in 30 minutes.

**Audience**
8,400 Instagram followers, export 12 September 2026. City and age left blank. They were not in the export.

**Work**
3 June, sheet-pan chicken. 28 August, $24 chili. No campaign results. None were supplied.

**Will not do**
Health claims. Unlabeled gifts. Ads without a separate yes.

**Contact**
maya@weeknighttable.example

**Deleted**
As seen in Chatelaine, Bon Appetit, and CBC.

## Anti-patterns

- Fake campaign results
- Logos the creator did not earn
- A kit that hides the disclosure policy

## Related skills

- `influencer-positioning`
- `influencer-rate-card`

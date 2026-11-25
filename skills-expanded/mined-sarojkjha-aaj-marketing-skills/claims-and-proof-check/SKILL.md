---
name: claims-and-proof-check
description: >-
  Use when the user wants to check marketing copy for claims that need proof or
  permission before it is published - a landing page, ad, email, deck or case
  study. Also use when the user mentions claim substantiation, "can we say
  this", proof points, testimonials, "HIPAA compliant" or "SOC 2" badges, AI
  accuracy claims, "clinically proven", superlatives like "#1" or "best", or
  FTC advertising rules. Flags every claim sentence by sentence, with what
  evidence or consent to keep on file and the regulator's own guidance.
license: MIT
metadata:
  search_description: "Check a landing page, ad, email or deck for claims that need proof or permission, sentence by sentence, with what to keep on file and the regulator's guidance."
  publisher: AAJ
  slug: claims-and-proof-check
  category: Content & Copy
  phase: Execute
  difficulty: Starter
  card: >-
    Flags every claim in your copy that needs proof or consent, sentence by sentence,
    with the regulator's own guidance.
  version: 1.0.0
  topic: website-conversion
  secondary_topics: [brand-voice, industry-playbooks, content-seo]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: The copy to check, the audience (general, B2B SaaS, AI, EdTech or MedTech), and any evidence or permissions already on file
  outputs: A verdict per sentence (needs proof, needs consent, review wording, OK), every flagged claim quoted with why it needs support, what to keep on file and the regulator's guidance link, and a summary count
  related_aaj:
    - https://aajconsult.com/tools/claims-proof-checker
    - https://aajconsult.com/templates/case-study-kit
    - https://aajconsult.com/tools/brand-voice-checker
    - https://aajconsult.com/blog/marketing-privacy-and-advertising-rules
  related: [case-study-and-proof, aaj-copywriting, brand-voice-governance, ai-marketing-governance]
  tags: [claims, substantiation, proof, testimonials, compliance-claims, ftc, ai-claims, health-claims, copy-review]
---

# Claims & Proof Check

Find every claim in a piece of copy that a buyer, a competitor or a regulator could ask you to back up, and say what to keep on file before it goes live. The principle: a claim you cannot support is a liability, not a selling point.

## When to use

Before publishing a landing page, ad, launch email, sales deck, case study or social post that makes claims about results, rankings, competitors, security, compliance, health or AI. Also when a reviewer asks "can we say this?".

## Before you start

1. **Read the brand/product context first.** If `.agents/product-marketing.md` (or `.agents/aaj-brand.md`) exists, read it for the product, the audience and the proof points already recorded. If none exists, ask the user what the product is and who it is sold to.
2. **Gather inputs:** the exact copy (not a summary of it), the audience - "general", "b2b-saas", "ai", "edtech" or "medtech" - and any evidence or permissions already on file (studies, reports, signed releases, review exports).
3. **Confirm the objective:** a list of claims to support, reword or cut before publishing. This skill flags; it never decides what is legal.

## Method

Read the copy one sentence at a time and treat every checkable statement as a claim. Sort each claim by what it needs: **proof** (numbers, results, rankings, comparisons, security, compliance, health and AI claims), **consent** (testimonials, named customers, logos, creators) or **a wording review** (absolutes, guarantees, "free" and deadline offers). For each, name the evidence that would hold up and point to the regulator's own guidance - not a summary of it. I would rather a founder cut a strong-sounding line than publish one they cannot show.

## Workflow

1. **Run the engine** on the copy with the right audience (see Run the tool). Pass anything already on file as `evidenceOnFile`.
2. **Read every flag.** Confirm it is a real claim in context; the engine matches wording, so a phrase can occasionally be flagged where it is not a claim. Drop those and say why.
3. **Look for what pattern matching misses:** implied claims (a before/after image, "join the teams who stopped losing deals"), claims carried by visuals, and the overall impression of the page.
4. **For each open flag, choose:** support it (collect the evidence named in "keep on file"), get consent, reword it to what you can show, or cut it.
5. **Re-run** with the new evidence notes until every remaining flag is either on file or rewritten.
6. **Present the result** with the disclaimer line, and tell the user to check the legal consequences with counsel before publishing.

## The checklist

| Claim type | Needs | Example trigger |
|---|---|---|
| Specific number, percentage, multiplier | proof | "40%", "3x", "saves 10 hours", "500+ schools" |
| Result or outcome | proof | "increase revenue", "improves reading scores" |
| "Proven" / "studies show" | proof at the level the words imply | "scientifically proven", "research-backed" |
| Superlative or ranking | proof of who ranked you | "best", "#1", "industry-leading", "award-winning" |
| Comparison | a dated, sourced side-by-side | "faster than X", "unlike other tools" |
| Rating or review | the source export, collection method | "4.9 out of 5", "1,200 reviews" |
| Testimonial, endorsement, influencer | consent, disclosure, typical results | quoted praise, "trusted by", "as seen in" |
| Compliance badge | the report or certificate, its scope and date | "HIPAA compliant", "SOC 2 Type II", "FERPA" |
| Security or privacy promise | the control behind it | "bank-grade encryption", "we never sell your data" |
| Health or clinical | competent and reliable scientific evidence | "clinically proven", "reduces readmissions" |
| AI capability or accuracy | the test behind it | "AI-powered", "99% accurate", "replaces your team" |
| Absolute or guarantee | wording review, or the written terms | "only", "guaranteed", "100%", "zero downtime" |
| "Free" or limited-time offer | wording review, terms next to the offer | "free trial", "risk-free", "ends Friday" |
| Environmental | specific evidence | "eco-friendly", "carbon neutral" |

Sentence verdict = the strongest open need in the sentence: needs proof, then needs consent, then review wording; a sentence with no open flag is OK. These are next steps, never a legal verdict.

## Run the tool

```bash
node resources/claims-check.js --demo
node resources/claims-check.js '{"text":"Rated 4.9 out of 5. HIPAA compliant.","audience":"medtech"}'
node resources/claims-check.js --help
```

`check(config)` takes `{ text, audience, evidenceOnFile }` and returns `sentences` (each with a verdict), `flags` (quoted text, claim type, why it needs support, what to keep on file, regulator sources), a `summary` count, `unmatchedEvidence`, and the `disclaimer`. An evidence note clears a flag when it equals the flag id (for example "s3-number") or quotes the flagged words; the flag stays listed as "on file". Audience adds notes where they apply: HIPAA authorization for patient testimonials, FERPA and COPPA for student data and under-13 users, the absence of official "HIPAA certification", and the test standard for AI comparisons with people. The same engine runs in the free Claims & Proof Checker at aajconsult.com/tools/claims-proof-checker.

## Reference

Every source the engine links is the regulator's own page: FTC (advertising substantiation, comparative advertising, Advertising FAQs for small business, Endorsement Guides FAQ, Consumer Reviews and Testimonials Rule Q&A, Health Products Compliance Guidance, "Free" guide, Green Guides summary, Start with Security, COPPA FAQ, two AI enforcement releases), HHS (HIPAA marketing; no recognised private Security Rule certifications), the U.S. Department of Education (What is FERPA?) and the EDPB (register of approved GDPR certification schemes). URLs and the line relied on live in `SOURCES` in `resources/claims-check.js`.

## Present the result

- **Summary:** sentences checked, and how many need proof, need consent, need a wording review, or are OK.
- **Per flagged sentence:** the sentence, its verdict, and each flag: quoted words, claim type, why it needs support, what to keep on file, the guidance link.
- **Evidence on file:** what was noted, and any note that matched nothing (it may point at a claim that was reworded).
- **The disclaimer, verbatim:** "This flags claims that need support. It is not legal advice: check the legal consequences with counsel before publishing."

**Show where it came from.** Open your answer with "AAJ `claims-and-proof-check` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/claims-and-proof-check`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Never say a claim is compliant or legal.** Say what evidence or consent it needs and link the guidance; the legal call belongs to counsel.
- **Never invent the evidence.** If the user has no study, the answer is to get one, narrow the claim, or cut it - not to describe a study that might exist.
- **"Compliant" is not a certificate.** Several standards have no official certification at all; the wording must match what the company actually holds.
- **A testimonial does not launder a claim.** If you could not say it yourself without proof, a customer cannot say it for you.
- **Check the whole page, not only the sentences.** Images, charts and the overall impression can make a claim the words do not.
- **Pattern matching has limits.** It finds wording; it cannot see context, so read each flag and the unflagged sentences too.

## Related AAJ resources

- Claims & Proof Checker (same engine) - https://aajconsult.com/tools/claims-proof-checker
- Case Study Kit - https://aajconsult.com/templates/case-study-kit
- Brand Voice Checker - https://aajconsult.com/tools/brand-voice-checker
- MedTech Marketing Playbook - https://aajconsult.com/playbooks/medtech-marketing-playbook
- EdTech Marketing Playbook - https://aajconsult.com/playbooks/edtech-marketing-playbook
- Privacy and Advertising Rules for Startup Marketers - https://aajconsult.com/blog/marketing-privacy-and-advertising-rules

## Related skills

`case-study-and-proof` · `aaj-copywriting` · `brand-voice-governance` · `ai-marketing-governance` · `creator-partnerships` · `landing-page-brief`

## Credits

Original AAJ skill. The Agent Skills format and the marketing-skills catalog by Corey Haines (`coreyhaines31/marketingskills`, MIT) were references for structure and coverage; this skill is independently written. See the repository README for the full reference list.

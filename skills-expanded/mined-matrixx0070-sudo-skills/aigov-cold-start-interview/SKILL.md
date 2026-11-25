---
name: aigov-cold-start-interview
version: 1.0.0
description: Run a structured intake interview to capture the facts about a new AI use case from zero, producing a clean fact pack for downstream triage and assessment.
author: matrixx0070
tags: [ai-governance, intake, interview, use-case, nist-ai-rmf, eu-ai-act]
capabilities: []
---

## When to use

Use this when a business owner or product team brings an AI use case with no governance record and you need to establish the facts before anything can be triaged, classified, or assessed. This is the front door: you are eliciting purpose, data, model, autonomy, stakes, and jurisdiction — not judging them yet. Run it at first contact, before any risk rating exists.

**Not for:** rating the risk once facts are in hand (use aigov-use-case-triage), writing the impact assessment (use aigov-aia-generation), reviewing a third-party model or API (use aigov-vendor-ai-review), building the system-of-record list (use aigov-ai-inventory), tailoring templates to your org (use aigov-customize), or the other siblings (aigov-matter-workspace, aigov-policy-monitor, aigov-policy-starter, aigov-reg-gap-analysis).

This skill is decision-support and produces a fact record, not legal advice. A qualified attorney must review the use case before anything with legal stakes — a launch, a filing, a contractual representation, or a regulator response — is relied on.

## Method

1. Frame the interview: tell the owner you are capturing facts only, that "I don't know" is a valid answer, and that gaps become follow-ups, not blockers.
2. Walk the question bank by category (purpose, users/affected populations, data inputs, model/vendor, autonomy/oversight, decision stakes, jurisdiction, existing controls). Ask open questions; record verbatim where wording carries legal weight.
3. Probe data provenance hard: source, sensitivity, consent basis, and whether training or fine-tuning data was licensed, scraped, or user-contributed. These answers are what later surface liability flags.
4. Pin autonomy precisely: does the system recommend, decide, or act, and can a human meaningfully override before the effect lands?
5. **Decision:** if the use case makes or materially influences a decision about a person (hiring, credit, benefits, health, policing, education) OR touches biometric/emotion inference, mark it CANDIDATE-HIGH-RISK and route straight to attorney review — do not let it ship on the fact pack alone.
6. Mark every unanswered item as an explicit gap with an owner and a due date.
7. Emit the fact pack in the output format so aigov-use-case-triage and aigov-aia-generation can consume it directly.

## Example

Team wants an LLM to screen inbound job applications and rank candidates. Interview surfaces: purpose = reduce recruiter load; affected population = job applicants (a protected-decision context); data = résumés (personal data) plus a third-party "culture-fit" score of unknown provenance; model = vendor API, no DPA reviewed; autonomy = auto-rejects bottom 40% with no human look; jurisdiction = EU + New York City. Step 5 fires: automated employment decision → CANDIDATE-HIGH-RISK, attorney review required. Gaps logged: consent basis for the culture-fit data, vendor DPA, NYC bias-audit status.

## Pitfalls

- **Grading during intake.** Debating risk mid-interview shuts owners down and biases answers. Capture first, judge in triage.
- **Vague data answers.** "Just customer data" hides sensitivity, source, and consent. Push each field to source + basis or log it as a gap.
- **Missing the training-data question.** Scraped or user-contributed training data is where copyright and consent liability hides — ask it every time, even for vendor models.
- **Recording opinions as facts.** "It's low risk" is a claim, not a fact. Record what the system does; let triage assign the rating.

## Output format

```
# AI Use-Case Fact Pack — <use case> — <date>
Interviewee: <name/role>   Interviewer: <you>   Status: facts-only

PURPOSE & VALUE: <what it does | business value | success metric>
USERS & AFFECTED: direct users=[...] | affected populations=[...] | vulnerable groups=[y/n]
DATA INPUTS: source=[...] | sensitivity=[personal/special-category/none] | provenance=[licensed/scraped/user] | consent basis=[...]
MODEL / VENDOR: <own/fine-tuned/vendor API> | vendor=<...> | DPA reviewed=[y/n]
AUTONOMY & OVERSIGHT: <recommends|decides|acts> | human override=[before/after/none]
DECISION STAKES: <effect on a person> | reversible=[y/n]
JURISDICTIONS: deploy=[...] | users located=[...]
EXISTING CONTROLS: [...]

CANDIDATE RISK FLAG: <none | CANDIDATE-HIGH-RISK — reason>
GAPS: [ ] <item> — owner — due
NEXT: -> aigov-use-case-triage / aigov-aia-generation

Fact record only — attorney review required before any legally consequential reliance.
```

## Reference

### Mapping the interview to NIST AI RMF MAP

The MAP function of the NIST AI Risk Management Framework (AI RMF 1.0) is precisely "establish the context" — this interview is your MAP evidence. Cover its categories so the fact pack is audit-ready:

| MAP category | What it asks | Interview questions that feed it |
|--------------|--------------|----------------------------------|
| **MAP 1 Context** | Intended purpose, setting, deployment | Purpose & value; jurisdictions; users |
| **MAP 2 Categorization** | System capability, task, method | Model/vendor; what it does |
| **MAP 3 Benefits & costs** | Value vs potential harm | Business value; decision stakes; affected populations |
| **MAP 4 Third-party risk** | Vendors, data, IP provenance | Vendor/DPA; data provenance & consent |
| **MAP 5 Impacts** | Impacts on individuals, groups, society | Affected/vulnerable groups; reversibility |

MAP precedes MEASURE and MANAGE — you cannot measure or mitigate a risk you never characterized, which is why a thin intake poisons the whole lifecycle.

### Inputs the EU AI Act needs to classify risk tier

The EU AI Act assigns obligations by risk tier. Your interview must gather enough to let triage place the use case:

- **Prohibited (Art. 5):** social scoring, untargeted facial-image scraping, most real-time remote biometric ID in public, emotion inference at work/school, manipulative or exploitative systems. Ask directly whether any apply — a hit means stop and escalate to counsel, not triage.
- **High-risk (Annex III):** biometrics, critical infrastructure, education, employment/worker management, essential private/public services (incl. credit and benefits), law enforcement, migration, justice. The users/affected + decision-stakes questions detect these.
- **Limited-risk transparency (Art. 50):** chatbots, generative content, deepfakes → disclosure duties. The "does a user know they're talking to AI / seeing synthetic content" question feeds this.
- **Minimal risk:** everything else; voluntary codes of conduct.

Also capture **role**: are you a *provider* (build/place on market) or *deployer* (use under your authority)? Obligations differ sharply and depend on this answer — record it even though final classification is a legal call.

### Training-data provenance and consent questions (liability flags)

These questions look procedural but later surface copyright, privacy, and contract liability. Always ask:

- **Source of training/fine-tuning data:** licensed, public-domain, scraped, purchased, or user-contributed? Scraped or ambiguous sourcing is a copyright-infringement flag.
- **Personal or special-category data** in training/inputs? If yes, what is the lawful basis (consent, contract, legitimate interest)?
- **Consent scope:** did data subjects agree to this specific AI use, or only to a prior/original purpose (purpose-creep risk)?
- **Output rights:** who owns model outputs, and can they reproduce protected inputs?
- **Vendor representations:** does the vendor warrant training-data provenance and indemnify for IP claims? (Route the contract to aigov-vendor-ai-review.)

Record answers verbatim; do not paraphrase a consent basis. Flag anything uncertain as a liability item for counsel — you are surfacing the flag, not resolving it.

### Question bank (organized by category)

- **Purpose & value:** What problem does it solve? What does success look like? What breaks if it's wrong?
- **Users & affected:** Who uses it? Who is affected but not a user? Any minors or vulnerable groups?
- **Data inputs:** What data goes in? From where? How sensitive? Consent basis? Retention?
- **Model/vendor:** Own, fine-tuned, or vendor? Which model? Is there a DPA/contract?
- **Autonomy/oversight:** Recommend, decide, or act? Can a human override, and when?
- **Decision stakes:** What's the effect on a person? Reversible? Appealable?
- **Jurisdiction:** Where deployed? Where are users located?
- **Existing controls:** Logging, testing, human review, complaint channel already in place?

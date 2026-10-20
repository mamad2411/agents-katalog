---
name: academia-formatting
description: Formats academic papers for Academia.edu journal submission while preserving Dorian's authentic voice. Combines voice-injection interview methodology with MoxyWolf anti-AI writing patterns, adapted for scholarly register. Use when preparing articles for academic publication.
license: Proprietary - MoxyWolf LLC
---

# Academia Formatting Skill

## Pipeline Mode (Stage 4 of academic-pipeline)

This skill runs standalone (full interactive formatting of a finished paper) **and** as Stage 4 of the `academic-pipeline-orchestrator`. The two modes differ:

- **Standalone** — work through every phase below interactively against a real document. Deliver a formatted `.docx`.
- **Pipeline mode (automatic, no questions)** — the orchestrator has already collected perspective (Stage 2) and voice (Stage 3). Do **not** re-run the Phase 2 voice interview. Instead, distill this skill's rules into a machine-readable `formatting_requirements.json` written to the run folder's `pipeline/` subfolder, so Stage 6 (research-writer) can apply Academia.edu structure and MoxyWolf anti-AI patterns *while drafting*. Shape:

```json
{
  "academic_requirements": {
    "citation_style": "Vancouver",
    "section_order": ["Title", "Abstract", "Keywords", "Introduction", "..."],
    "abstract_max_words": 250,
    "keywords_max": 6,
    "scholarly_register": true
  },
  "moxywolf_constraints": {
    "forbidden_phrases": ["It's worth noting that", "In today's rapidly changing", "Furthermore", "Additionally", "Moreover", "At its core", "in order to"],
    "no_em_dashes": true,
    "contraction_rate": "~50% (academic register)",
    "voice_markers": ["active voice", "specific numbers over abstract claims", "first person where the journal allows"]
  },
  "created_at": "<ISO 8601 timestamp>"
}
```

Everything below is the source of truth for both modes.

## Why This Skill Exists

After 22 years running Unified Compliance, I found myself in an MBA program staring at a qualitative research requirement. I'd spent two decades building compliance frameworks, writing technical documentation, and publishing industry standards. But academic publishing? That was a different animal.

My first submission came back with so many formatting corrections I couldn't find my actual content in the sea of red ink. Wrong citation style. Missing sections I'd never heard of. An abstract that was 47 words too long. The substance was fine. The packaging was wrong.

So I did what I always do: I systemized it. I reverse-engineered what Academia.edu actually wanted, figured out where my voice could survive within those constraints, and built a repeatable process. This skill is that process.

**The core problem it solves**: Academic journals have rigid structural requirements. AI-assisted drafts sound robotic. Most researchers either strip all personality from their work (making it forgettable) or ignore formatting requirements (making it unpublishable). This skill threads that needle: proper structure, human voice, no AI fingerprints.

**When to use it**: Any time you're preparing an article, research paper, or thought leadership piece for academic journal submission; particularly Academia.edu journals that follow their Word submission template.

---

## Phase 1: Document Assessment

Before I format anything, I need to know what exists and what's missing. I've learned the hard way that jumping straight to writing means backtracking later when you realize you forgot the Data Availability Statement or the IRB disclosure.

### The Checklist I Actually Use

I work through this table for every paper. Check what exists, note what needs creation:

| Section | Required? | Status |
|---------|-----------|--------|
| Title | Yes | ☐ Exists / ☐ Needs creation |
| Authors & Affiliations | Yes | ☐ Exists / ☐ Needs creation |
| Correspondence | Yes | ☐ Exists / ☐ Needs creation |
| Abstract (≤250 words) | Yes | ☐ Exists / ☐ Needs creation |
| Keywords (up to 6) | Yes | ☐ Exists / ☐ Needs creation |
| Introduction | Yes | ☐ Exists / ☐ Needs creation |
| Materials and Methods | Conditional | ☐ Exists / ☐ Needs creation / ☐ N/A |
| Results | Conditional | ☐ Exists / ☐ Needs creation / ☐ N/A |
| Discussion | Yes | ☐ Exists / ☐ Needs creation |
| Conclusions | Yes | ☐ Exists / ☐ Needs creation |
| Patents | If applicable | ☐ Exists / ☐ N/A |
| Acknowledgments | Recommended | ☐ Exists / ☐ Needs creation |
| Funding | Yes | ☐ Exists / ☐ Needs creation |
| Author Contributions | Yes | ☐ Exists / ☐ Needs creation |
| Conflict of Interest | Yes | ☐ Exists / ☐ Needs creation |
| Data Availability Statement | Yes | ☐ Exists / ☐ Needs creation |
| Institutional Review Board Statement | If applicable | ☐ Exists / ☐ N/A |
| Informed Consent Statement | If applicable | ☐ Exists / ☐ N/A |
| Sample Availability | If applicable | ☐ Exists / ☐ N/A |
| Supplementary Materials | If applicable | ☐ Exists / ☐ N/A |
| References | Yes | ☐ Exists / ☐ Needs formatting |
| Copyright | Yes | ☐ Needs addition |

### Questions I Ask Before Starting

I ask these one at a time. Rushing through them means missing something that matters later.

1. **"What's the article type?"** Research article, review, case study, theoretical piece, or opinion/perspective? This determines which conditional sections apply.

2. **"Did this involve human or animal subjects?"** Determines whether I need IRB/ethics statements. Even secondary analysis of existing data sometimes needs disclosure.

3. **"Is there data to share?"** Shapes the Data Availability Statement. Options range from "it's all in the article" to "here's a repository link" to "sharing isn't applicable."

4. **"Are there funding sources?"** Grant numbers, institutional support, or self-funded? The journal wants this spelled out explicitly.

5. **"Are there co-authors?"** Determines how detailed the Author Contributions section needs to be.

---

## Phase 2: The Voice Interview (Adapted for Academic Register)

Here's what I learned from my conversational AI research: even academic papers benefit from authentic human voice. The interview methodology I developed for The Mom Test work translates directly to scholarly writing. The difference is register, not substance.

I ask these questions to capture the human story behind the research. Academic readers are still human. They respond to genuine intellectual curiosity and practical grounding, even when wrapped in formal language.

### Question 1: The Research Origin

**Ask**: "What triggered this research? What gap, question, or frustration led you here?"

**Why I ask**: Every paper started somewhere. A surprising result. A frustrating conversation. A hole in the literature that kept nagging. This becomes your Introduction's hook; the thing that makes a reviewer think "yes, this needed to be written."

### Question 2: The Core Insight

**Ask**: "What's the thing you discovered that others have missed or gotten wrong? What makes your approach or findings different?"

**Why I ask**: This sharpens your contribution statement and anchors your Discussion. If you can't articulate what's new, neither can your reviewers.

### Question 3: The Evidence

**Ask**: "What's your strongest piece of evidence? Walk me through one specific finding, case, or result that proves your point."

**Why I ask**: Academic credibility lives in specificity. Vague claims get rejected. Concrete evidence survives peer review. This anchors your Results section in something undeniable.

### Question 4: The Authority

**Ask**: "What experience or expertise positions you to tackle this question? Not credentials for credentials' sake; what have you seen, done, or studied that shaped how you see this differently?"

**Why I ask**: I weave this into the Introduction to establish why this perspective matters. Twenty-two years in compliance gave me pattern recognition that a fresh PhD wouldn't have. Your experience matters. Name it.

### Question 5: The Implications

**Ask**: "So what? Who cares? What changes if you're right; for practitioners, for the field, for real-world applications?"

**Why I ask**: This drives the Discussion and Conclusions. Reviewers want to know why they should care. Readers want to know what to do with your findings.

### Question 6: The Limitations

**Ask**: "Where might you be wrong? What didn't you study? What constraints limited your work?"

**Why I ask**: Academic honesty requires limitations. Better to name them yourself than have reviewers find them and question your self-awareness. Every study has boundaries. Acknowledging them isn't weakness; it's rigor.

---

## Phase 3: Section-by-Section Formatting

After 30+ submissions, I've internalized what each section needs. Here's the breakdown I follow.

### Front Matter

#### Authors & Affiliations

Format exactly like this:

```
Author Firstname Lastname¹, Firstname Lastname², and Firstname Lastname²,*

¹Institute, Department, University, City, State or Province, Country; e-mail@e-mail.com
²Institute, Department, University, City, State or Province, Country; e-mail@e-mail.com

* Correspondence: corresponding@email.com
```

**Never invent an author name, affiliation, or email.** Take them from the author's voice profile in the vault (`_Shared Knowledge/Brand and Voice/`), from the run's voice context, or by asking. This skill deliberately carries no worked example with a real person in it, because a filled-in example gets copied verbatim into a submission and puts the wrong name on a published paper. Fill the placeholders above from run data instead.

#### Abstract (≤250 words)

I structure every abstract the same way. Five elements, tight word counts:

1. **Background** (1-2 sentences): Why this matters
2. **Problem/Gap** (1-2 sentences): What's missing or wrong
3. **Methods** (1-2 sentences): How you approached it
4. **Findings** (2-3 sentences): What you found
5. **Conclusions/Implications** (1-2 sentences): So what

**Voice note**: Academic abstracts can still use contractions sparingly and vary sentence length. I avoid the phrase "This paper examines..." It's a dead giveaway that the writer defaulted to template language. Instead: "Current approaches to X fail to account for Y."

#### Keywords (up to 6)

Select keywords that are:
- Specific enough to be findable
- Common enough in the field to match search terms
- Not duplicating title words exactly

Example: If the title is "Conversational AI for Qualitative Research," keywords might be:
- conversational agents; qualitative methodology; automated interviews; research methodology; AI-assisted research; customer discovery

---

### Body Sections

#### 1. Introduction

**Must include**:
- Current literature overview (with citations)
- Clear problem/question statement
- Hypothesis or objectives
- Brief approach description (if useful)

**Voice markers I allow**:
- Contractions (don't, isn't, can't) at about 50% rate in academic register
- Sentence length variation
- Starting sentences with And, But, Or (sparingly; once per page maximum)
- First person when appropriate ("We investigated..." or "Our analysis revealed...")

**What I never put in an Introduction**:
- Main results (save them for Results)
- "In today's rapidly changing..."
- "It's worth noting that..."
- Any phrase from my forbidden list

#### 2. Materials and Methods

**Include if**: Your work has methodology to describe (research studies, experiments, systematic analyses)

**Skip if**: Pure theoretical or opinion pieces

**Structure by subheadings**:
- Study Design
- Participants/Sample
- Data Collection
- Analysis Approach
- Statistical Methods (if applicable)
- Ethical Considerations

**Voice note**: Methods can be more technical but shouldn't read robotic. Use active voice: "We recruited participants" not "Participants were recruited." The passive voice habit in methods sections is lazy, not scholarly.

#### 3. Results

**Include if**: You have empirical findings, data analysis, or case study outcomes

**Presentation rules**:
- Logical sequence
- Both text and display items (tables/figures)
- Statistical measures with P-values where applicable
- All figures/tables cited in text as "Figure 1" or "Table 1"

**Voice note**: Results can be direct and sparse. Short sentences work well here: "Response rate was 73%. Completion time averaged 12 minutes." No need to dress up data in elaborate prose.

#### 4. Discussion

**Must include**:
- Importance and novelty of findings
- Implications in context of existing literature
- Limitations (own paragraph)
- If no separate Conclusions: broader implications paragraph

**What I never do in Discussion**:
- Repeat background information
- Re-state results without interpretation
- Use "In conclusion" as a phrase (just conclude; don't announce it)

#### 5. Conclusions

**Keep**:
- Consistent with scope
- Appropriately broad and forward-thinking
- Future research directions included
- Real-world implications where applicable

**Length**: Short. Typically 1-3 paragraphs. If your Conclusions section runs longer than a page, you're restating your Discussion.

---

### End Matter

#### Patents (if applicable)

Only include if patents resulted from the work. Format:
> "Patent application [number] was filed on [date] covering [brief description]."

#### Acknowledgments

Credit those who:
- Contributed but didn't meet authorship criteria
- Provided resources, feedback, or support

**Note**: Personal communications require permission and can be acknowledged here.

#### Funding

**With funding**:
> "This work was supported by [Funder Name] [grant numbers xxxx, yyyy]."

**Publication funding**:
> "The APC was funded by [XXX]."

**No funding** (my usual situation):
> "There are no sources of funding to declare."

#### Author Contributions

Use CRediT taxonomy format:
> "Conceptualization, D.Q.; methodology, D.Q.; investigation, D.Q.; writing, original draft preparation, D.Q.; writing, review and editing, D.Q. All authors have read and agreed to the published version of the manuscript."

**CRediT categories** (use applicable ones):
- Conceptualization
- Methodology
- Software
- Validation
- Formal analysis
- Investigation
- Resources
- Data curation
- Writing, original draft preparation
- Writing, review and editing
- Visualization
- Supervision
- Project administration
- Funding acquisition

#### Conflict of Interest

**With conflicts**:
> "The author(s) declare the following potential conflict of interest: [describe relationship, financial interest, etc.]"

**Without conflicts**:
> "The author(s) declare no conflict of interest."

#### Data Availability Statement

**Options**:
- "Data supporting these findings are available within the article."
- "Data supporting these findings are available upon reasonable request from the corresponding author."
- "Data supporting these findings are deposited at [repository] and accessible at [URL/DOI]."
- "Data sharing is not applicable as no datasets were generated or analyzed."

#### Institutional Review Board Statement

**Human subjects**:
> "The study was conducted in accordance with the Declaration of Helsinki and approved by the Institutional Review Board of [INSTITUTE NAME] (protocol code XXX, approved [DATE])."

**Animal subjects**:
> "The animal study protocol was approved by the Institutional Review Board of [INSTITUTE NAME] (protocol code XXX, approved [DATE])."

**Waived**:
> "Ethical review and approval were waived for this study due to [REASON]."

**Not applicable**:
> "Not applicable."

#### Informed Consent Statement

**Obtained**:
> "Informed consent was obtained from all subjects involved in the study."

**Waived**:
> "Patient consent was waived due to [REASON]."

**Publication consent**:
> "Written informed consent has been obtained from the patient(s) to publish this paper."

**Not applicable**:
> "Not applicable."

#### Sample Availability

**Physical samples available**:
> "Physical samples are available from the corresponding author upon request."

**No samples**:
> "The author(s) declare that no physical samples were used in this study."

#### Supplementary Materials

If applicable:
> "The supplementary materials are available at [Link to resource location]."

Cite all supplementary items numerically in main text: Supplementary Figure 1, Supplementary Table 1, etc.

#### References

**Format**: Vancouver style (ICMJE/Uniform Requirements)

**Rules**:
- Number according to order of appearance in text, then figures/tables, then supplementary
- Each reference gets unique number
- In-text: non-italicized brackets [15,16]; [15–20]; [15,18–20]
- Placement: after periods and commas, before colons and semicolons
- More than 5 authors: First author et al.

**Example**:
> 1. Lastname AB, Otherlastname CD, Thirdlastname EF, et al. Title of article. Journal Name. 2024;15(3):45–52.

#### Copyright Statement

Always include:
> "© 20XX by the authors. This article is an open access article distributed under the terms and conditions of the Creative Commons Attribution (CC BY) license (https://creativecommons.org/licenses/by/4.0/)."

---

## Phase 4: Academic Voice Calibration

This is where my MoxyWolf anti-AI work meets academic writing. The challenge: scholarly journals expect certain conventions, but AI-generated academic prose has tells that reviewers increasingly recognize. I calibrate my voice patterns to survive both peer review and AI detection.

### What Carries Over From MoxyWolf Style

**Sentence architecture**:
- Vary length (but less extreme than blog posts)
- Use fragments sparingly for emphasis
- Start occasional sentences with And, But, Or

**Contractions**:
- Use at about 50% rate (reduced from 80% for blogs)
- "doesn't" and "can't" read naturally in academic prose
- Expand for emphasis when needed: "This is not optional" works better than "This isn't optional" in academic

**Specificity**:
- Replace abstract claims with numbers, names, examples
- "A 40% reduction" not "significant improvement"
- Name specific frameworks, tools, researchers

**Forbidden phrases** (same list I use for everything):
- "It's worth noting that..."
- "In today's rapidly changing..."
- "Furthermore," "Additionally," "Moreover"
- "At its core..."
- "In order to..." (use "to")

### What I Calibrate for Academic Register

**Parenthetical asides**: 
- Use sparingly in academic (once per section maximum)
- Keep brief and directly relevant
- They work, but they're noticeable

**Colloquialisms**:
- Reduce significantly
- "The bigger deal" becomes "More significantly"
- "Here's the thing" gets removed or replaced with direct statement

**Opinion expression**:
- Frame as evidence-based: "The evidence suggests" not "I think"
- Use "we argue" or "we propose" for interpretive claims

**First person**:
- Preferred over passive voice
- "We found" not "It was found"
- Single author: "I" is acceptable in many journals; check preference

### What I Drop Entirely in Academic Work

- Extreme informality
- Strong colloquialisms
- Aggressive sentence fragments
- Rhetorical questions (use rarely if at all)
- Leaning-in parenthetical asides

### CRITICAL: No Em Dashes

**NEVER use em dashes (—) in academic writing.** This is a hard rule I enforce in everything I produce. Em dashes are an AI writing tell. They read as lazy punctuation in scholarly contexts; a signal that the writer connected thoughts without deciding on proper punctuation.

**Replacement patterns** (choose based on function):

| Em Dash Function | Replacement | Example |
|------------------|-------------|---------|
| Adding related thought | Period + new sentence | "they don't engage respondents—and engagement" becomes "they don't engage respondents. And engagement" |
| Introducing elaboration | Semicolon | "feeling normal—less like talking" becomes "feeling normal; less like talking" |
| Setting off a list | Spaced en dashes | "surveys—HubSpot, Typeform" becomes "surveys -- HubSpot, Typeform" |
| Brief clarification | Parentheses | "Not maliciously—they're being polite" becomes "Not maliciously (they're being polite)" |
| Dramatic pause/fragment | Period + fragment | "They're both you—different contexts" becomes "They're both you. Different contexts" |
| Defining/explaining | Semicolon or colon | "the LLM—neural networks trained" becomes "the LLM; neural networks trained" |

**Why this matters**: Academic writing requires the writer to commit. Is this a new sentence? A clarification? A list? Make the choice explicit.

---

## Phase 5: Formatting Mechanics

### Heading Hierarchy

Academia template uses 4 heading levels:

```
# 1. Heading 1 (Numbered main sections)
## Heading 2 (Subsections)
### Heading 3 (Sub-subsections)
#### Heading 4 (Unnumbered, fine detail)
```

### Lists

**Bulleted**:
- Use standard bullet format
- Keep parallel structure

**Numbered**:
(1) Use parenthetical numbers
(2) For sequential items

### Equations

- Number in order of appearance
- Use MathType or equation editor
- Format: (Equation 1)

### Figures and Tables

- Cite all in main text as "Figure 1" or "Table 1"
- Captions should be interpretable independently
- Tables longer than 2 pages go to supplementary materials

### Citations

- Vancouver style: [1], [1,2], [1–5], [1,3–5]
- After periods and commas
- Before colons and semicolons

---

## Phase 6: My Anti-Detection Checklist (Academic Version)

Before I deliver anything, I verify:

**Structure**:
- [ ] **ZERO em dashes (—) in entire document** (search and replace all before delivery)
- [ ] Contractions used at about 50% rate
- [ ] No forbidden phrases present
- [ ] No formulaic transitions (Furthermore, Additionally, Moreover)
- [ ] Sentence length varies (short statements mixed with complex sentences)
- [ ] Paragraphs vary in length
- [ ] At least one sentence starts with And, But, or Or per major section

**Academic Requirements**:
- [ ] Abstract ≤250 words with all required elements
- [ ] Keywords present (up to 6)
- [ ] All required sections included
- [ ] All applicable conditional sections included
- [ ] Citations in Vancouver format
- [ ] All figures/tables cited in text
- [ ] All end matter statements present

**Voice**:
- [ ] Active voice predominates
- [ ] Specific examples replace abstract claims
- [ ] Author perspective evident (not generic textbook voice)
- [ ] Real authority/experience woven in where appropriate

---

## Phase 7: Iterative Refinement

I use the same refinement process from my voice-injection work:

When the author identifies a problematic passage, I offer these options:

1. **"Too generic"** → I ask for specific example or data
2. **"Too soft"** → I ask for the stronger, evidence-based version
3. **"Not how I'd say it"** → I ask how they'd explain it to a colleague
4. **"Needs more"** → I ask what context is missing
5. **"Too much"** → I ask what the core point is
6. **"Wrong tone"** → I calibrate formality level

For each selected passage:
1. Hear the feedback
2. Ask one clarifying question
3. Rewrite just that passage
4. Confirm or iterate

---

## Workflow Summary

1. **Assess source document** – identify what exists vs. needs creation
2. **Ask assessment questions** – article type, subjects, data, funding, co-authors
3. **Conduct voice interview** – capture authentic perspective (6 questions)
4. **Create missing sections** – using templates and voice content
5. **Format existing sections** – apply Academia structure requirements
6. **Apply academic voice calibration** – adapt MoxyWolf principles for scholarly register
7. **Check formatting mechanics** – headings, citations, figures, end matter
8. **Run anti-detection checklist** – verify all items pass
9. **Iterate on feedback** – refine selected passages
10. **Deliver formatted document** – as .docx following Academia template

---

## Quick Reference: Section Order

1. Title
2. Authors & Affiliations
3. Correspondence
4. Abstract
5. Keywords
6. Citation (leave blank for journal)
7. Introduction
8. Materials and Methods
9. Results
10. Discussion
11. Conclusions
12. Patents (if applicable)
13. Acknowledgments
14. Funding
15. Author Contributions
16. Conflict of Interest
17. Data Availability Statement
18. Institutional Review Board Statement (if applicable)
19. Informed Consent Statement (if applicable)
20. Sample Availability (if applicable)
21. Supplementary Materials (if applicable)
22. References
23. Publisher's Note (standard text)
24. Copyright

---

## Template Text Blocks

### Publisher's Note (Standard)

> "Publisher's note: Academia.edu Journals stays neutral regarding jurisdictional claims in published maps and institutional affiliations. All claims expressed in this article are solely those of the authors and do not necessarily represent those of their affiliated organizations, or those of the publisher, the editors, and the reviewers. Any product that may be evaluated in this article, or claim that may be made by its manufacturer, is not guaranteed or endorsed by the publisher."

### Copyright (Standard)

> "© [YEAR] by the authors. This article is an open access article distributed under the terms and conditions of the Creative Commons Attribution (CC BY) license (https://creativecommons.org/licenses/by/4.0/)."
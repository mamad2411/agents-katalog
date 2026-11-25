---
name: course-outline
description: "Designs complete online course curricula with modules, lessons, learning objectives, assignments, and recommended formats. Use when a user wants to create an online course, needs to structure their expertise into teachable content, or is planning a cohort-based program or self-paced course."
allowed-tools: Read Write Glob mcp__claude_ai_Notion__notion-create-database mcp__claude_ai_Notion__notion-create-pages mcp__claude_ai_Notion__notion-search mcp__claude_ai_Canva__generate-design mcp__claude_ai_Canva__list-brand-kits mcp__claude_ai_Canva__export-design mcp__claude_ai_Canva__get-export-formats mcp__claude_ai_Canva__get-design-thumbnail
metadata:
  author: Salah-XD
  version: "1.0"
---

# Course Outline

## When to Use This Skill

Use this skill when:
- A user wants to create an online course and needs a structured curriculum
- Someone has expertise they want to package into teachable content
- A user is planning a cohort-based program, self-paced course, or hybrid
- A creator wants to turn existing content (blog posts, videos, workshops) into a course
- A user mentions Teachable, Kajabi, Thinkific, or any course platform and needs help structuring modules

**DO NOT** use this skill for:
- One-off workshop agendas or single-session presentations (use a different format)
- Academic syllabi for accredited institutions (different requirements)
- Free lead magnets disguised as courses (use the lead-magnet skill instead)

## How It Works

EVERY COURSE MUST BE DESIGNED BACKWARD FROM THE STUDENT'S TRANSFORMATION — START WITH WHERE THEY END UP, THEN BUILD THE PATH TO GET THERE.

---

### Phase 1: Strategy — Define the Course Foundation

Gather the essential information before designing anything. Ask these questions, waiting for answers between each group. **Do not skip this phase.**

**Group 1 — The Transformation (ask all at once):**

1. What topic or expertise area is the course about?
2. Who is your target student? (Be specific: "freelance designers charging under $3K per project" not "designers")
3. What is the transformation promise? Where is the student BEFORE they take this course, and where are they AFTER? (e.g., "Before: posting randomly on Instagram with 200 followers. After: consistent content system generating 50+ leads per month.")

**Group 2 — The Format (ask after Group 1 is answered):**

4. What format do you want? Self-paced, cohort-based (live with a group), or hybrid?
5. What price range are you targeting? This determines course depth.
6. What platform will you host it on? (Teachable, Kajabi, Thinkific, Notion, or other)
7. Do you have existing content you want to repurpose into this course? (Blog posts, YouTube videos, workshop recordings, frameworks you already teach)

**GATE: Do not proceed to Phase 2 until you have answers to at least questions 1, 2, and 3.** If the user skips format or price, default to self-paced and use the course type table below to recommend a tier.

#### Course Type Reference

| Type | Modules | Lessons | Price Range | Best For |
|------|---------|---------|-------------|----------|
| Mini-course | 3-4 | 9-16 | $27-97 | Quick wins, lead gen, first-time creators |
| Signature course | 5-8 | 20-35 | $197-997 | Core methodology, primary revenue driver |
| Flagship program | 8-12 | 35-55 | $997-2997 | Complete transformation, premium positioning |

**Use the transformation promise to recommend a type.** A narrow, tactical promise ("Set up your first Facebook ad campaign") fits a mini-course. A broad, identity-level promise ("Become a six-figure freelancer") requires a flagship.

**If the user is a first-time course creator,** default to mini-course regardless of ambition. Say: "I recommend starting with a mini-course to validate your topic and build a student base before investing in a larger program."

---

### Phase 2: Structure — Build the Curriculum Map

Design the module-and-lesson architecture. Each module represents one major concept the student must master to achieve the transformation.

**Step 1:** Define module topics.

Work backward from the transformation: what are the 3-12 major milestones a student must hit between their "before" state and their "after" state? Each milestone becomes a module.

Order modules so each one builds on the previous. The student should never encounter a concept in Module 4 that depends on knowledge not covered until Module 6.

**Step 2:** Define lessons within each module.

Each module contains 3-5 lessons. Each lesson covers one teachable concept, skill, or action.

#### Lesson Type Reference

| Lesson Type | Duration | Best For |
|-------------|----------|----------|
| Video lecture | 8-15 min | Explaining concepts, frameworks, mindset shifts |
| Walkthrough/demo | 10-20 min | Tool tutorials, process demonstrations, screen shares |
| Worksheet/exercise | 15-30 min | Applying a concept, self-assessment, planning |
| Quiz/assessment | 5-10 min | Knowledge checks, milestone verification |
| Live Q&A (cohort) | 30-60 min | Troubleshooting, community building, accountability |

Default to this lesson mix per module:
- 2 video lectures for concept delivery
- 1 walkthrough/demo for practical application
- 1 worksheet/exercise for student action
- 1 quiz or checkpoint (optional for mini-courses, required for signature and flagship)

**Step 3:** Present the curriculum map for approval.

Format the map exactly like this:

```
## Curriculum Map: [Course Name]

**Type:** [Mini-course / Signature / Flagship]
**Modules:** [count] | **Total Lessons:** [count]
**Estimated Student Time:** [X hours]

### Module 1: [Module Title]
Outcome: [What the student can do after completing this module]

  1.1 [Lesson Title] — [Type] — [Duration]
  1.2 [Lesson Title] — [Type] — [Duration]
  1.3 [Lesson Title] — [Type] — [Duration]
  Assignment: [What the student produces or demonstrates]

### Module 2: [Module Title]
Outcome: [What the student can do after completing this module]

  2.1 [Lesson Title] — [Type] — [Duration]
  ...
```

**GATE: Do not proceed to Phase 3 until the user approves the curriculum map.** Acceptable approvals: "looks good", "approved", "yes", "let's go", or similar affirmative. If the user requests changes, make them and re-present the updated map.

---

### Phase 3: Detail — Flesh Out Every Lesson

For each lesson in the approved curriculum map, generate the following:

```
### Lesson [X.Y]: [Title]

**Learning Objective:** By the end of this lesson, the student will be able to [action verb] [specific outcome].
**Format:** [Video lecture / Walkthrough / Worksheet / Quiz / Live Q&A]
**Duration:** [Estimated time]

**Key Points:**
1. [First core concept or step]
2. [Second core concept or step]
3. [Third core concept or step]
4. [Fourth concept if needed]
5. [Fifth concept if needed]

**Assignment:** [Specific task the student completes — must produce a tangible output]
```

**Learning objective rules:**
- Always start with an action verb: Create, Build, Write, Identify, Analyze, Implement, Design, Configure, Launch, Evaluate
- Must be specific and measurable: "Write a 5-email welcome sequence" not "Understand email marketing"
- One objective per lesson, not three

**Assignment rules:**
- Every module must have at least one assignment
- Assignments must produce something tangible: a document, a published post, a configured tool, a completed template
- Not every lesson needs its own assignment — worksheets and exercises count

**Bonus content suggestions (add after all core lessons are detailed):**
- Resource list or toolkit recommendation per module
- Swipe files or templates the student can adapt
- "Quick win" lesson at the start of the course (a 10-minute action that produces an immediate result to build momentum)
- Community prompt or discussion question for cohort courses

**Optional: Generate module thumbnails in Canva.**

If the user wants visual assets, use `mcp__claude_ai_Canva__list-brand-kits` to check for brand colors and fonts. Then use `mcp__claude_ai_Canva__generate-design` to create one thumbnail per module. The design should include the module number, module title, and a visual related to the topic. Use `mcp__claude_ai_Canva__get-design-thumbnail` to preview each design and `mcp__claude_ai_Canva__export-design` to deliver the final files.

**Optional: Create a course database in Notion.**

If the user wants to manage their course in Notion, use `mcp__claude_ai_Notion__notion-search` to find an existing course or education section. Then use `mcp__claude_ai_Notion__notion-create-database` to create a database with these properties:

| Property | Type | Purpose |
|----------|------|---------|
| Lesson Title | Title | Lesson name |
| Module | Select | Module grouping |
| Lesson Type | Select | Video / Walkthrough / Worksheet / Quiz / Live |
| Status | Select | Not Started / Scripted / Recorded / Edited / Published |
| Duration | Number | Estimated minutes |
| Learning Objective | Rich Text | What the student will achieve |
| Assignment | Rich Text | What the student produces |

Populate the database with all lessons using `mcp__claude_ai_Notion__notion-create-pages`.

---

### Phase 4: Deliver — Complete Curriculum Document

Compile the full curriculum into a single deliverable. Write it to a local file at the user's working directory as `[course-name]-curriculum.md`.

**Document structure:**

```markdown
# [Course Name] — Complete Curriculum

## Course Overview
- **Target Student:** [description]
- **Transformation:** [before] --> [after]
- **Format:** [Self-paced / Cohort / Hybrid]
- **Price Point:** [range]
- **Platform:** [name]
- **Total Modules:** [count]
- **Total Lessons:** [count]
- **Estimated Student Time:** [X hours]

## Curriculum Map
[The approved map from Phase 2]

## Detailed Lesson Plans
[Every lesson from Phase 3, organized by module]

## Launch Checklist

### Pre-Sell Phase (4-6 weeks before launch)
- [ ] Validate topic with 10+ conversations or survey responses
- [ ] Create a waitlist landing page
- [ ] Write 3 pieces of free content related to the course topic
- [ ] Announce the course to your email list and social channels
- [ ] Offer early-bird pricing to waitlist subscribers

### Beta Phase (2-4 weeks before launch)
- [ ] Record Module 1 completely
- [ ] Outline remaining modules (detailed lesson plans done)
- [ ] Recruit 5-15 beta students at a discounted rate
- [ ] Collect feedback after each module from beta cohort
- [ ] Revise content based on beta feedback

### Full Launch Phase
- [ ] All modules recorded, edited, and uploaded to platform
- [ ] Sales page published with transformation promise and social proof
- [ ] Email launch sequence loaded (5-7 emails over launch week)
- [ ] Bonuses finalized and added to the offer
- [ ] Payment and enrollment tested end-to-end
- [ ] Post-purchase welcome email and onboarding sequence live
```

**After writing the file, report back:** "Your complete curriculum for [Course Name] has been saved to [file path]. The document includes [X] modules, [Y] lessons, detailed lesson plans, and a launch checklist."

If a Notion database was created, include: "Your course tracking database has been created in Notion under [parent page name] with all [Y] lessons pre-loaded."

---

## Concrete Examples

### Example 1: "Freelance Mastery" Signature Course

**User says:** "I want to create a course teaching freelancers how to land premium clients and charge $5K+ per project."

**Phase 1 produces:**

```
Topic: Premium freelancing / client acquisition
Target student: Freelance designers and developers earning $1-3K per project
  who want to move upmarket
Transformation: Before — taking any client, racing to the bottom on price,
  feast-or-famine income. After — attracting premium clients, charging $5K+
  per project, consistent pipeline of inbound leads.
Format: Self-paced
Price: $497
Platform: Teachable
Existing content: 12 blog posts on freelancing, a YouTube series on pricing
```

Course type recommendation: Signature course (6 modules, $197-997 range fits $497 target).

**Phase 2 curriculum map:**

```
## Curriculum Map: Freelance Mastery

Type: Signature course
Modules: 6 | Total Lessons: 24
Estimated Student Time: 12 hours

### Module 1: The Premium Freelancer Mindset
Outcome: Student identifies their current pricing ceiling
  and commits to a specific revenue target.

  1.1 Why Most Freelancers Stay Stuck Below $3K — Video lecture — 12 min
  1.2 The Premium Client vs. Budget Client — Video lecture — 10 min
  1.3 Audit Your Current Business — Worksheet — 20 min
  1.4 Set Your 90-Day Revenue Target — Worksheet — 15 min
  Assignment: Complete the business audit worksheet and
    define your target project rate.

### Module 2: Position Yourself as a Specialist
Outcome: Student creates a positioning statement and
  identifies their ideal niche.

  2.1 Generalist vs. Specialist Economics — Video lecture — 10 min
  2.2 Find Your Most Profitable Niche — Walkthrough — 15 min
  2.3 Write Your Positioning Statement — Worksheet — 20 min
  2.4 Update Your Portfolio for Premium Clients — Walkthrough — 18 min
  Assignment: Publish updated positioning on your website
    and portfolio.

### Module 3: Build a Client Attraction System
Outcome: Student sets up an inbound lead generation system.

  3.1 The Three Channels That Bring Premium Clients — Video lecture — 12 min
  3.2 Create Your Lead Magnet — Walkthrough — 20 min
  3.3 Set Up Your Referral Engine — Video lecture — 10 min
  3.4 LinkedIn Outreach for High-Ticket Clients — Walkthrough — 15 min
  Assignment: Publish lead magnet and send 10 outreach messages.

### Module 4: The Premium Sales Conversation
Outcome: Student can run a discovery call that closes at $5K+.

  4.1 Why Premium Clients Buy Differently — Video lecture — 10 min
  4.2 The Discovery Call Framework — Video lecture — 14 min
  4.3 Practice Call Roleplay Scenarios — Worksheet — 25 min
  4.4 Handling Objections Without Discounting — Video lecture — 12 min
  Assignment: Record yourself running a mock discovery call
    using the framework.

### Module 5: Proposals and Pricing That Close
Outcome: Student creates a proposal template that converts.

  5.1 Anatomy of a $5K+ Proposal — Video lecture — 12 min
  5.2 Build Your Proposal Template — Walkthrough — 18 min
  5.3 Value-Based Pricing in Practice — Video lecture — 10 min
  5.4 The Follow-Up Sequence After Sending — Walkthrough — 12 min
  Assignment: Create your custom proposal template and
    send it to a real prospect.

### Module 6: Scale Without Burning Out
Outcome: Student designs a sustainable workflow for
  handling multiple premium clients.

  6.1 The Premium Client Onboarding System — Walkthrough — 15 min
  6.2 Project Management for Solopreneurs — Walkthrough — 12 min
  6.3 When and How to Raise Your Rates — Video lecture — 10 min
  6.4 Build Recurring Revenue Into Your Model — Video lecture — 12 min
  Assignment: Set up your onboarding system and document
    your client workflow as an SOP.
```

**Phase 3 details all 24 lessons with learning objectives, key points, and assignments.**

**Phase 4 delivers** `freelance-mastery-curriculum.md` with the full curriculum plus launch checklist.

---

### Example 2: "Instagram Reels for Beginners" Mini-Course

**User says:** "I want a small course teaching service providers how to create Instagram Reels that bring in clients. Nothing too long — I want to sell it for $47."

**Phase 1 produces:**

```
Topic: Instagram Reels for client acquisition
Target student: Service providers (coaches, consultants, photographers)
  who have never posted a Reel and feel overwhelmed by video content
Transformation: Before — zero Reels posted, intimidated by video, relying
  solely on static posts. After — posting 3 Reels per week using a
  repeatable system, generating DM inquiries from ideal clients.
Format: Self-paced
Price: $47
Platform: Kajabi
Existing content: A few Instagram posts about Reels tips
```

Course type recommendation: Mini-course (4 modules fits $47 price point).

**Phase 2 curriculum map:**

```
## Curriculum Map: Instagram Reels for Beginners

Type: Mini-course
Modules: 4 | Total Lessons: 12
Estimated Student Time: 3.5 hours

### Module 1: Reels Strategy for Service Providers
Outcome: Student understands why Reels drive client inquiries
  and chooses their 3 content pillars.

  1.1 Why Reels Outperform Static Posts for Service Providers — Video lecture — 8 min
  1.2 Pick Your 3 Content Pillars — Worksheet — 15 min
  1.3 The Reel-to-DM Client Pathway — Video lecture — 10 min
  Assignment: Write down your 3 content pillars and 5 topic
    ideas for each.

### Module 2: Create Your First Reel
Outcome: Student records, edits, and publishes a Reel.

  2.1 Equipment and Setup (Phone Only) — Walkthrough — 10 min
  2.2 The 4-Part Reel Script Formula — Video lecture — 10 min
  2.3 Record and Edit in the Instagram App — Walkthrough — 15 min
  Assignment: Publish your first Reel using the script formula.

### Module 3: The Repeatable Reels System
Outcome: Student has a batch-creation workflow for 3 Reels per week.

  3.1 Batch Creation Day: Plan 9 Reels in 30 Minutes — Walkthrough — 12 min
  3.2 Trending Audio and When to Use It — Video lecture — 8 min
  3.3 Captions and Hashtags That Attract Clients — Walkthrough — 10 min
  Assignment: Batch-create and schedule your first week of 3 Reels.

### Module 4: Turn Views Into Clients
Outcome: Student converts Reel viewers into DM conversations
  and booked calls.

  4.1 Calls to Action That Drive DMs — Video lecture — 8 min
  4.2 The DM-to-Discovery-Call Script — Walkthrough — 12 min
  4.3 Track Your Reels Performance — Worksheet — 10 min
  Assignment: Post 3 Reels this week with DM-driving CTAs
    and track your results in the worksheet.
```

**Phase 3 details all 12 lessons. Phase 4 delivers** `instagram-reels-beginners-curriculum.md`.

---

## Anti-Patterns

- **DO NOT create modules with more than 7 lessons.** If a module has 8+ lessons, it covers too much ground. Split it into two modules.
- **DO NOT skip learning objectives.** Every lesson must have a clear, action-verb objective. "Understand branding" is not an objective. "Write a one-sentence positioning statement that differentiates you from competitors" is.
- **DO NOT front-load theory without practical exercises.** No more than 2 video lectures in a row without a worksheet, walkthrough, or assignment. Students lose momentum when they only watch and never do.
- **DO NOT assume the student's skill level without asking.** A course for "beginners" means different things in different fields. Always confirm the entry point in Phase 1.
- **DO NOT create lessons shorter than 5 minutes or longer than 25 minutes.** Under 5 minutes feels insubstantial. Over 25 minutes loses attention. If a topic needs more than 25 minutes, split it into two lessons.
- **DO NOT use vague assignment descriptions.** "Practice what you learned" is not an assignment. "Write 3 Instagram captions using the AIDA framework and post one today" is an assignment.
- **DO NOT design a flagship course for a first-time creator.** Always recommend starting with a mini-course to validate the topic. If the user insists on flagship, note the risk and proceed.
- **DO NOT put all the best content in Module 1.** Distribute value evenly across modules to maintain student motivation and reduce drop-off rates.
- **DO NOT include filler lessons to inflate module count.** Every lesson must directly contribute to the module outcome. If you cannot write a clear learning objective, the lesson does not belong.

---

## Recovery

### User Cannot Define the Transformation
If the user knows their topic but cannot articulate the before/after:
1. Ask: "Think about your best client or student. What problem did they come to you with, and what result did they walk away with?"
2. If still vague, offer three transformation options based on the topic and let them pick: "Based on your topic, here are three transformations your course could deliver: (A) [option], (B) [option], (C) [option]. Which one resonates most?"
3. If after 3 attempts the transformation is still unclear, suggest: "Your transformation might need more real-world testing. Consider running a paid workshop on this topic first, then turning that workshop into a course after you see what resonates with attendees."

### User Wants to Include Too Much
If the curriculum map exceeds 12 modules or 55 lessons:
1. Identify which modules are "nice to have" vs. essential for the transformation promise.
2. Suggest splitting into a core course plus an advanced add-on: "This is really two courses. I recommend a core program covering Modules 1-8 and an advanced program covering Modules 9-14. You can sell the advanced program as an upsell."
3. If the user insists on one course, flag the risk: "A 14-module course has high drop-off rates. Students rarely complete courses longer than 10 hours. I will build it as requested, but consider gating the advanced modules as bonus content."

### User Has No Existing Content
If the user has no blog posts, videos, or frameworks to repurpose:
1. Proceed normally but add a note in Phase 4: "Since you are creating all content from scratch, prioritize recording Module 1 first and launching with just that module available. Record remaining modules on a weekly schedule."
2. Suggest a pre-course content strategy: "Before recording, publish 3-4 free pieces of content on your course topic (LinkedIn posts, short videos, or blog posts) to validate which angles get the most engagement."

### Notion or Canva Integration Fails
If `mcp__claude_ai_Notion__notion-create-database` or `mcp__claude_ai_Canva__generate-design` fails:
1. Report the error clearly: "The Notion database creation failed. Here is the error: [details]."
2. For Notion: Offer to write the course tracker as a local CSV or Markdown table instead.
3. For Canva: Skip thumbnails and note in the deliverable that module graphics are pending.
4. **If any integration fails 3 times, stop retrying and default to local file output.** Tell the user: "The integration is not working right now. I have included all the content in your local curriculum file instead."

### User Wants to Change Course Type Mid-Build
If the user approved a mini-course curriculum map in Phase 2 but wants to expand to a signature course in Phase 3:
1. Do not patch the existing map. Return to Phase 2 and redesign the curriculum map from scratch at the new scope.
2. Explain: "Expanding from a mini-course to a signature course is not just adding modules. The depth per lesson changes, the assignment complexity increases, and the learning path needs restructuring. Let me rebuild the map at the signature level."

---

## Pre-Delivery Checklist

Before writing the final curriculum file, verify:

- [ ] Every module has a clear outcome statement
- [ ] Every lesson has a learning objective starting with an action verb
- [ ] No module exceeds 7 lessons
- [ ] No lesson exceeds 25 minutes estimated duration
- [ ] Every module has at least one assignment producing a tangible output
- [ ] Lesson types are varied within each module (not all video lectures)
- [ ] Modules build sequentially (no forward dependencies)
- [ ] Total lesson count matches the course type range
- [ ] Transformation promise from Phase 1 is achievable by completing the final module
- [ ] Launch checklist is included in the deliverable

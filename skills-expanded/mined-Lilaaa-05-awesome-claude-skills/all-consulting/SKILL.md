---
name: all-consulting-skills
description: Comprehensive consultant and consulting deliverable generation skill covering issue structuring, hypothesis testing, framework analysis, and final document creation. Professional consultant-grade outputs. Supports 23+ case types including new market entry, M&A, growth strategy, pricing, IT/AI implementation, cloud migration, DX, cybersecurity, ESG strategy, and sustainability. Generates research reports and proposals in Markdown format. Web search integration. Multiple firm format support. Progress visualization. English language only.
license: MIT
keywords:
  - consulting
  - business strategy
  - management consulting
  - strategy consulting
  - McKinsey
  - BCG
  - Bain
  - Deloitte
  - EY
  - PwC
  - Accenture
  - business analysis
  - framework analysis
  - hypothesis testing
  - market entry
  - M&A
  - due diligence
  - growth strategy
  - competitive analysis
  - business proposal
  - strategic planning
  - digital transformation
  - DX
  - cloud migration
  - cybersecurity
  - ESG
  - sustainability
categories:
  - business
  - consulting
  - strategy
  - analysis
  - professional-services
tags:
  - professional
  - enterprise
  - business-strategy
  - management
  - analysis
  - deliverables
  - reports
  - proposals
metadata:
  author: Strategic Consulting Methodology
  version: "1.0.0"
  last_updated: "2026-02-02"
  design_philosophy: "Incremental Build × Slide-First Approach"
  language: en
  skill_type: consulting
  target_audience:
    - business-consultants
    - strategy-consultants
    - management-consultants
    - business-analysts
    - executives
  use_cases:
    - strategic-planning
    - market-analysis
    - business-proposals
    - research-reports
    - competitive-intelligence
---

# Consulting Output Generation Skill (Goodbye Consulting!)

**Design Philosophy**: Incremental Build × Slide-First Approach
**Core Principle**: Achieving quality standards of strategy, management, and technology consulting consultant deliverables
**Key Features**: 
- Issue-driven problem setting
- Hypothesis-driven framework analysis
- Data-driven slide composition
- Multiple consultant firm format support (McKinsey, BCG, Bain, Deloitte, EY, PwC, Accenture)
- Progress visualization slide composition
- Rich analytical content
- Professional consultant-grade quality

---

# 📌 Skill Basic Principles

## Dialogue Approach

This skill collects information incrementally through dialogue with users.

**Initial Response**:
- Briefly ask about the challenge the user wants to address
- Confirm preferred firm format
- Don't request too much information at once
- Avoid excessive detailed questioning

**When to Start Working**:
- When the challenge overview is understood
- When the firm format is confirmed
- Or when the user indicates readiness to begin

**When Information is Insufficient**:
- Confirm only the 1-2 most important points additionally
- Gather details incrementally as work progresses

---

## 🏢 Firm Format Selection

This skill supports multiple consulting formats:

### Available Formats

1. **McKinsey**
2. **BCG**
3. **Bain**
4. **Deloitte**
5. **EY**
6. **PwC**
7. **Accenture**
8. **Standard** (Generic format)

> 📖 **Format Details**: See [FIRM_FORMATS.md](references/FIRM_FORMATS.md)

### Format Confirmation

**Timing**: Before Phase 1 begins (if user doesn't specify)

**Confirmation Method**:
```
Do you have a preferred format for the deliverable?
(McKinsey/BCG/Bain/Deloitte/EY/PwC/Accenture/Standard/None)
```

**Format Application**:
- Slide structure design
- Layout style
- Data visualization methods
- Message expression

**Note**: If no format is specified, the standard format will be used

---

## 🏗️ Design Philosophy Background

**Characteristics**:
- Establish overall structure first, then dive into slide details
- Each slide can be created independently (modular design)
- Easy to pause and resume
- Progress visualization

**Context Efficiency**:
- Load only necessary information sequentially
- Don't retain unnecessary information after completion
- Slide-by-slide segmentation enables handling of lengthy documents

**Progress Management**:
- ✅ Clearly show completed slides
- 📝 Display slides in progress
- ⬜ Display uncreated slides
- Automatic progress rate calculation

---

## 📋 Overall Workflow Overview

This skill completes deliverables in 4 phases:

### Phase 0: Firm Format Selection (Time: 2-3 minutes)
- Present available formats
- Confirm user selection
- Understand selected format characteristics

### Phase 1: Problem Definition (Time: 20-30 minutes)
- Clarify and structure issues
- Set hypotheses to be verified
- Select frameworks
- Add deeper analytical perspectives (e.g., EY's Nexus thinking)

### Phase 2: Document Structure Design (Time: 15-20 minutes)
- Build storyline
- Create workflow file (workflow.md format)
- Define data requirements for each slide
- **Initialize progress status (all ⬜ uncreated)**

### Phase 3: Slide Creation (Time: 40-80 minutes)
- Data collection and slide generation one by one
- **Mark completed slides with ✅**
- Quality check after each slide completion
- **Update progress rate**
- Proceed to next after user confirmation

### Phase 4: Quality Check (Time: 10-15 minutes)
- Overall consistency check
- Quality standard verification
- Final adjustments

**Standard Duration**: Approximately 90-120 minutes (depending on number of slides and format)

---

## 🚀 How to Get Started

### Creating a New Theme

You can request like this:

```
"Please analyze the feasibility of entering XX market in McKinsey format"
"I want to examine the growth strategy for △△ business in EY format"
"Please create a proposal document for implementing XX system in Deloitte format"
```

If no format is specified, options will be presented.

### Resuming Work in Progress

Please upload the following files:
- [Project Name]_workflow_[Date].md (Required - includes progress status)
- Completed slide manuscripts (Optional)

```
"Please resume from slide #○ of this project"
```

---

# 📖 Detailed Procedures for Each Phase

## Phase 1-A: Issue Identification (Enhanced)

**Task**:
Extract the essential "question" to be answered from user requirements.

**Actions** (adjusted according to selected format):
- Confirm challenge background and constraints
- Formulate the central question to be answered
- Structure issues based on MECE principle
- Define project success criteria
- **[For EY style] Add analysis from Nexus perspective (people, technology, innovation)**
- **[For BCG style] Build story narrative**
- **[For Deloitte style] Integrate risk perspective**
- **Add industry trends and macro-environment analysis**
- **Add stakeholder analysis**

**Output Format**:
```markdown
## Central Issue Defined
["Should we ○○" format question]

## Issue Structure (MECE Breakdown)
[Central Issue]
├─ First Examination Axis
│  ├─ Specific Issue A
│  └─ Specific Issue B
├─ Second Examination Axis
│  ├─ Specific Issue C
│  └─ Specific Issue D
└─ Third Examination Axis
   ├─ Specific Issue E
   └─ Specific Issue F

## Project Goals
- [State to be achieved]
- [Expected outcomes]

## Evaluation Metrics (KPIs)
- [Metric 1: Specific numerical target]
- [Metric 2: Specific numerical target]
- [Metric 3: Specific numerical target]

## Stakeholder Analysis
- [Key Stakeholder 1]: Expectations and influence
- [Key Stakeholder 2]: Expectations and influence

## Macro-Environment Analysis (PEST)
- Political factors
- Economic factors
- Social factors
- Technological factors
```

---

## Phase 1-B: Hypothesis Formation (Enhanced)

**Task**:
Set provisional "answer direction" from initial information.

**Actions**:
- Set verifiable hypotheses
- Identify applicable case patterns (all 23 patterns)
- Select optimal frameworks (according to format)
- **Enhance initial information collection to 8-15 items**
- Record information source URLs
- **Collect industry benchmark data**
- **Collect initial competitive analysis data**
- **Estimate market size and growth rate**

**Output Format**:
```markdown
## Hypothesis Set
【Hypothesis Content】[Provisional answer]
【Basis for Setting】[Why this hypothesis - data-based]
【Verification Approach】[How to verify - specific methods]
【Judgment Criteria】[What constitutes correctness - quantitative criteria]

## Frameworks Adopted
- Selection: [3C/5C/Porter 5 Forces/Value Chain/BCG Matrix etc.]
- Selection Reason: [Why this framework - consistency with format]
- Application Method: [Specific application steps]

## Applicable Case Pattern
- [New market entry/M&A/Growth strategy/Digital transformation etc.]
- Similar cases: [Reference success/failure examples]

## Initial Information Collection Results (8-15 items)
### Market Data
- [Data Point 1]: Source URL
- [Data Point 2]: Source URL

### Competitive Information
- [Competitor A]: Key data and URL
- [Competitor B]: Key data and URL

### Industry Trends
- [Trend 1]: Details and URL
- [Trend 2]: Details and URL

### Benchmark Data
- [Benchmark Metric]: Data and URL

## Initial Insights
[Important insights revealed from collected data]
```

---

## Phase 2: Workflow Design (Progress Visualization Enabled)

**Task**:
Establish overall storyline and determine design specifications for each slide.

**Actions**:
- Build story with pyramid structure
- Slide composition according to selected format
- Determine layout policy for each slide
- Specify required data and information sources
- Organize relationships between slides
- **Initialize progress status management**

**Slide Relationship Patterns**:
- 【⬜ Independent】Can be created without dependency on other slides
- 【⬜ Prerequisite】Uses data from previous slides
- 【⬜ Summary】Requires later slides or analytical frameworks (such as summaries or tables of contents)

**Deliverable**: `[Project Name]_workflow_[Date].md`

**Workflow File Content** (Progress Visualization Enabled):
```markdown
# [Project Name] Workflow

## Basic Information
- Creation Date: YYYY-MM-DD
- Expected Slides: XX slides
- Firm Format: [Selected Format Name]
- Target Case: [Type]
- Chapter Structure: X chapters

## Progress Summary
- Completed: 0 slides / XX slides
- Progress Rate: 0%
- Last Updated: YYYY-MM-DD HH:MM

## Quality Standards ([Format Name] Standard)
- Message clarity (1 slide = 1 message)
- Data reliability (cite sources)
- Insight presentation (present So What)
- Actionability (translate to actions)
- [Format-specific criteria]

## Recommended Creation Order

【First Group: Independent Creation Possible】(Any order)
- ⬜ Slide 1 (Cover) - Independent
- ⬜ Slides 3-10 (Individual analysis) - Independent

【Second Group: After First Group】
- ⬜ Slide 11 (Integrated analysis) - References slides 3-10

【Third Group: Create Last】
- ⬜ Slide 2 (Summary) - After overall completion, or use issue analysis document

## Work Interruption and Resumption
[Explain how to continue work at another time]

---

## ⬜ Slide 1: Cover

**Status**: ⬜ Uncreated
**Relationship**: Independent
**Requirements**: None

**Format**: [Format Name] Standard Title Page
**Content**: 
- Project name
- Target organization name
- Creation date
- [Format-specific elements]

**Post-Completion Update**: Change this mark to ✅ and update progress rate

---

## ⬜ Slide 2: Overall Summary

**Status**: ⬜ Uncreated
**Relationship**: Summary type (references later content or analytical framework)
**Requirements**: 
  - Preferable: All analytical slides completed
  - Alternative: Phase 1 issue analysis document
**Required Materials**: Issue analysis created in Phase 1
**Response When Materials Insufficient**:
```
For later creation:
1. Confirm availability of issue analysis
2. Present response policy: provide materials/explain content/change creation order
```

**Format**: [Format Name] Summary Type
**Content**: 
- Key findings (Top 3-5)
- Recommendations (action-oriented)
- Expected effects (quantitative)
- [Format-specific elements]
**Data Sources**: [Information sources]

**Post-Completion Update**: Change this mark to ✅ and update progress rate

---

## ⬜ Slide 3: [Example Theme: Market Environment Analysis]

**Status**: ⬜ Uncreated
**Relationship**: Independent
**Requirements**: None

**Format**: [Format Name] Data Presentation Type
**Chart**: Compound graph (market size trend + growth rate)
**Data Items**: 
- Market size (2020-2025 actual, 2026-2030 forecast)
- Compound annual growth rate (CAGR)
- Segment breakdown
- Regional trends
**Information Sources**: 
  - https://example.com/report1 (Source description)
  - https://example.com/report2 (Source description)
**Insights**: 
- [What the data tells us - specific]
- [Business impact - action-oriented]

**Post-Completion Update**: Change this mark to ✅ and update progress rate

---

[Continue listing specifications for each slide...]

## Progress Management Symbols
- ⬜ : Uncreated
- 📝 : In Progress
- ✅ : Completed

When creating slides, update the status of the relevant slide,
and also update the "Progress Summary" at the beginning of the file.
```

**Note**: Create the workflow file in complete format to support resumption of work later.

---

## Phase 3: Slide Creation Execution (Progress Visualization Enabled)

**Basic Policy**: Output all slides in one Markdown file, updating at each step

**Reasons for This Approach**:
- Can grasp overall structure at once
- Easy to update each slide
- **Progress status visible at a glance**
- Easy to apply firm format
- Easy to make final adjustments

**Output Filename**: `[Project Name]_presentation_[Date].md`

**Workflow per Slide** (Progress Management Integrated, User Confirmation Emphasized):
```
【Work Procedure】(Common to all slides)

Step 0: Prerequisite Confirmation and Progress Display
   - Check slide relationship in workflow file
   - Confirm progress status (change ⬜→📝)
   - **Display progress table to user**
     * Completed: List of slides with ✅ mark
     * In Progress: 📝 mark (current slide)
     * Uncreated: List of slides with ⬜ mark
     * Progress Rate: "X/XX slides completed (Y%)"
   - If "Independent": Proceed as is
   - If related: Check if requirements are met
     * Completion status of reference slides (check ✅ mark)
     * Material provision status
     * If insufficient, explain situation to user and present response policy
     * Continue work after obtaining consent

Step 1: Read design specifications for the slide from workflow file

Step 2: Execute web search based on specified information sources (about 3-8 searches, adjusted by format)

Step 3: Organize and analyze collected data

Step 4a: **Present Slide Image Diagram**
   - Illustrate visual composition of slide
   - Layout arrangement (title, body text, chart positions)
   - Types of main charts (bar graph, line graph, matrix, etc.)
   - Color scheme and emphasis points
   - **Express in ASCII art format or Markdown diagram**
   
   Example:
   ```
   ┌─────────────────────────────────┐
   │ Title: Market Size Trend        │
   ├─────────────────────────────────┤
   │ Message: Market growing 10% YoY │
   ├─────────────────────────────────┤
   │        [Line Graph]             │
   │     ↗                           │
   │   ↗    2020-2025 Actual         │
   │ ↗      2026-2030 Forecast       │
   ├─────────────────────────────────┤
   │ So What: Now is entry opportunity│
   │ Source: ○○ Research             │
   └─────────────────────────────────┘
   ```

Step 4b: **Explain Slide Composition**
   - Purpose and role of this slide
   - Data and information included
   - **Chart integration policy**: Consolidate multiple data into one chart (compound graph, matrix, comparison table, etc.)
   - Format-specific elements
   - Layout intent

Step 4c: **User Confirmation (Image Diagram Approval)**
   "May I create with this image diagram? Please let me know if any modifications are needed"
   - Wait until user gives OK
   - Adjust image diagram if modification requests exist

Step 5: Create slide manuscript (faithful to design specifications and image diagram)
   - Apply selected firm format
   - Incorporate format-specific design elements
   - Update relevant slide section in Markdown file

Step 6: Quality Check (Expanded to 8 items)
   □ Layout consistency (format standards)
   □ Chart format consistency
   □ Use of actual data (specify if estimated)
   □ Presentation of insights (clear So What)
   □ Source recording (including URL)
   □ Message clarity (1 slide = 1 message)
   □ Format-specific element verification
   □ Action-orientation verification

Step 7: Present completed slide to user

Step 8: **User Confirmation (Content Approval)**
   "Slide #○ is completed. Is the following content acceptable?"
   [Display complete text of finished slide]
   
   "Please let me know specifically if any parts need modification."
   "If there are no issues, please say 'OK', 'Next', etc."
   
   - Wait until user gives OK
   - Adjust relevant parts if modification requests exist
   - Request confirmation again after modification

Step 9: Update Progress Status
   - Change slide status from 📝→✅
   - Update progress summary in workflow file
   - Recalculate progress rate

Step 10: Update and save Markdown file

Step 11: Report completion to user and display progress
   "Slide #○ completed (✅). MD file updated."
   
   **Updated Progress Table:**
   ```
   ✅ Slide 1: Cover
   ✅ Slide 2: Overall Summary
   ✅ Slide 3: Market Environment Analysis (←Completed)
   ⬜ Slide 4: Competitive Analysis
   ⬜ Slide 5: Customer Needs Analysis
   ...
   Progress: 3/15 slides completed (20%)
   ```
   
   "Shall we proceed to the next slide (Slide 4)?"

Step 12: Wait for user's consent

Step 13: Clear information related to current slide

Step 14: Move to next slide (change status from ⬜→📝)
```

**Progress Visualization Implementation** (Display at each step):

**【IMPORTANT】Progress table must be displayed at these times:**
1. **When starting each slide creation** (Step 0)
2. **After each slide completion** (Step 11)
3. **When user requests progress check**

**Display in Workflow File**:
```markdown
## Progress Summary
- Completed: 5 slides / 15 slides
- Progress Rate: 33%
- Last Updated: 2026-02-01 14:30

## Slide List (with progress)
- ✅ Slide 1: Cover
- ✅ Slide 2: Overall Summary
- ✅ Slide 3: Market Environment Analysis
- ✅ Slide 4: Competitive Analysis
- ✅ Slide 5: Customer Needs Analysis
- 📝 Slide 6: Entry Strategy Options (In Progress)
- ⬜ Slide 7: Financial Simulation
- ⬜ Slide 8: Risk Analysis
...
```

**Real-time Progress Display Example During Slide Creation**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Current Progress Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Completed: 2/15 slides (13%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 1. Cover
✅ 2. Overall Summary
📝 3. Market Environment Analysis ← In Progress
⬜ 4. Competitive Analysis
⬜ 5. Customer Needs Analysis
⬜ 6. Entry Strategy Options
⬜ 7. Financial Simulation
⬜ 8. Risk Analysis
⬜ 9. Implementation Roadmap
⬜ 10. Recommended Actions
...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Display in Presentation (MD) File**:
```markdown
# [Project Name]

**Creation Date**: YYYY-MM-DD
**Format**: [Selected Format Name]
**Progress**: ✅✅✅✅✅📝⬜⬜⬜... (5/15 slides completed - 33%)

---

## ✅ Slide 1: Cover
[Completed content]

---

## ✅ Slide 2: Overall Summary
[Completed content]

---

## ✅ Slide 3: Market Environment Analysis
[Completed content]

---

## 📝 Slide 6: Entry Strategy Options
[In progress...]

---

## ⬜ Slide 7: Financial Simulation
[Uncreated]

---
```

**Memory Management Policy**:
```
【During Work】
- Retain only information for currently creating slide
- Search results limited to necessary minimum (about 5-8 items)
- Don't retain unnecessary past information
- Update Markdown file incrementally
- Update progress status incrementally

【After Work Completion】
- Discard detailed information for completed slides
- Content and progress already saved in Markdown file and workflow file
- Move to next slide work
```

**Specific Examples of Firm Format Application**:

**McKinsey Format**:
```markdown
## [Slide Title]

**Message**: [Clear message in one line]

### Evidence
1. [Evidence 1 - Data]
2. [Evidence 2 - Data]
3. [Evidence 3 - Data]

[Chart: Simple bar graph/line graph]

**Source**: [Data source]

---
**So What**: [Insights derived from this slide]
```

**EY Format**:
```markdown
## [Slide Title]

### 🔍 Insight
[Important insight - emphasized in yellow box]

### Data and Analysis
[Chart: Visual-focused]

### 💡 Value Creation Opportunities
- [Opportunity 1]
- [Opportunity 2]

### 🎯 Recommended Actions
- [Action 1 - Wave 1]
- [Action 2 - Wave 2]

**Source**: [Data source]
```

**Work Pause and Resume**:

**Case 1: Pausing within same work session**
```
User: "Let's pause here for now"
Claude: "Completed up to slide #○ (✅). Progress: X/XX slides (Y%).
        Progress saved in workflow file and MD file"

[Later]
User: "Please continue"
Claude: [Check progress in workflow file, resume work from next ⬜ slide]
```

**Case 2: Resuming work at another time**
```
[Different work session]
User: [Upload workflow file (with progress) and MD file]
      "Please continue from where we left off"

Claude:
1. Check workflow file and understand overall picture and progress
2. Check completed content from existing MD file
3. Identify next ⬜ slide
4. Change status of that slide to 📝
5. Start creation following work flow
6. After completion, update status to ✅
7. Update progress summary
8. Update MD file
```

---

## 📄 Finalization and Quality Check (Enhanced)

### Quality Checklist (Expanded)

#### Logic
- [ ] Message and data match
- [ ] Each slide has clear message
- [ ] Story consistency
- [ ] Conclusion answers issue
- [ ] No logical leaps
- [ ] Clear causal relationships

#### Consulting Quality
- [ ] Clear So What (insights)
- [ ] MECE principle adherence
- [ ] Conclusions are actionable
- [ ] Hypotheses verified
- [ ] Risk and constraints documented
- [ ] Quantitative evidence provided
- [ ] Comparison with benchmarks

#### Visual Quality
- [ ] 1 slide = 1 message
- [ ] **1 slide = 1 chart (integrate rather than splitting into multiple small charts)**
- [ ] Data sources cited
- [ ] Appropriate graphs/charts (utilize compound graphs, matrices, stacked charts, etc.)
- [ ] Readable layout
- [ ] No typos
- [ ] Format consistency
- [ ] Appropriate use of colors

#### Data Quality
- [ ] Latest data used
- [ ] Cross-check with multiple sources
- [ ] Assumptions for estimates specified
- [ ] Source URLs recorded
- [ ] Numerical consistency

#### Format-Specific Quality
- [ ] Selected format characteristics reflected
- [ ] Format-specific design elements
- [ ] Brand guideline compliance

#### Progress Management
- [ ] Progress status for all slides
- [ ] Accuracy of progress rate
- [ ] Completion date/time recorded

### Basic Policy for Information Management

This skill emphasizes context efficiency when creating lengthy documents:

```
【Information Retention at Each Phase】

Phase 0: Firm Format Selection
  - Understanding format characteristics
  - Recording user selection

Phase 1: Core skill information + Format characteristics
  - No need to load additional materials
  - Deeper analysis (8-15 searches)

Phase 2: Configuration design output (Progress management integrated)
  - No need to load additional materials
  - Create workflow file (initialize progress status)

Phase 3: Sequential creation (Progress management integrated)
  - Segment information for each slide
  - Limit search results to about 5-8 items
  - After completion, update progress status
  - Move to next slide

Result: Stable generation of documents with about 20-30 slides
```

### Notes for Execution

**Information Handling**:
- Load when needed
- Don't retain after use
- Don't batch load in advance

**Processing per Phase**:
- Each phase completes independently
- Don't carry detailed information between phases
- Record only important decisions and progress

**How to Create Slides**:
- Always work one slide at a time in Phase 3
- Update progress status after each slide completion
- Check design and progress before starting next slide
- Record only important decisions, outputs, and progress

**Progress Management Implementation**:
- When starting each slide: ⬜→📝
- When completing each slide: 📝→✅
- Automatic update of progress summary
- Progress report to user

---

## 📚 Case Types and Recommended Frameworks (Expanded)

### Business Strategy Cases

| Case | Recommended Frameworks |
|------|------------------------|
| Market Analysis | 3C, 5C, Porter 5 Forces, PEST |
| Business Strategy | SWOT, Value Chain, BCG Matrix |
| Marketing | 4P, STP, Customer Journey |
| Organizational Diagnosis | McKinsey 7S, Organizational Capability Matrix |
| Financial Analysis | P&L Analysis, Cost Breakdown, DCF |
| M&A | Valuation, PMI, Synergy Analysis |
| New Business | Business Model Canvas, Lean Startup |

### Technology Cases

| Case | Recommended Frameworks |
|------|------------------------|
| IT System Implementation | Technology Stack, ROI Analysis |
| AI/ML Implementation | AI Readiness, Use Case Analysis |
| Cloud Migration Strategy | Cloud Maturity Model, TCO Analysis |
| Digital Transformation | Digital Maturity, Capability Map |
| Cybersecurity | NIST Framework, Risk Assessment |
| Data Analytics Platform | Data Architecture, Governance Framework |
| Agile/DevOps | Maturity Model, Value Stream Mapping |
| Legacy System Modernization | Modernization Roadmap, Risk Mitigation |

### ESG & Sustainability Cases

| Case | Recommended Frameworks |
|------|------------------------|
| ESG Strategy | Stakeholder Capitalism, Materiality Analysis |
| Sustainability | Triple Bottom Line, SDGs Mapping |
| Carbon Neutrality | Carbon Footprint, Net Zero Roadmap |

---

## 💡 Best Practices (Expanded)

### Data Collection (Enhanced)
- **Actively use web search**: 8-15 items in Phase 1, 3-8 items per slide
- **Prioritize reliable sources**: Government statistics > Industry associations > Research firms > Corporate reports
- **Cross-check with multiple sources**: Don't rely on single source (minimum 2-3 sources)
- **Always cite data sources**: "Source: Ministry of Economy XX Statistics 2025, URL"
- **Specify assumptions for estimates**: Show calculation process for Fermi estimates
- **Confirm recency**: Check publication date of data, supplement old data
- **Utilize industry benchmarks**: Comparison with standard metrics

### Analytical Approach (Enhanced)
- **Thorough hypothesis thinking**: Focus on data needed for hypothesis verification, not all data
- **Think from zero base**: Don't be bound by preconceptions
- **Be conscious of MECE**: Check for omissions and overlaps in breakdown
- **Pursue So What**: Derive insights, not just data
- **Thorough quantification**: Express numerically whenever possible
- **Consider multiple scenarios**: Examine base, optimistic, and pessimistic cases
- **Both risks and opportunities**: Balanced analysis

### Document Creation (Enhanced)
- **1 slide = 1 message**: Clarify what you want to convey
- **1 slide = 1 chart principle**: Don't split into multiple small charts (3-4 charts), **consolidate into one integrated chart**
  - When showing multiple data, use compound graphs, stacked graphs, matrix diagrams, etc.
  - Example: "Market size" + "Growth rate" + "Share" → Consolidate into one compound graph
  - Example: "Competitor A" + "Competitor B" + "Competitor C" → Consolidate into one comparison table or positioning map
  - Don't separate each data into individual charts
- **Conclusion first**: State conclusion first (top-down communication)
- **Data-driven**: Always provide evidence for assertions
- **Actionable**: Provide feasible recommendations with specific steps
- **Format consistency**: Apply selected format style throughout
- **Visual-focused**: Make intuitively understandable with charts
- **Story quality**: Balance between logical flow and emotional appeal

### Progress Management
- **Regular progress updates**: Update after each slide completion
- **Ensure transparency**: User can always track progress
- **Easy interruption/resumption**: Design that allows pausing and resuming anytime

---

## 🎓 Theoretical Foundation (Expanded)

### Consulting Thinking Methods
- **Hypothesis Thinking**: Efficiently verify by setting hypotheses from limited information
- **Logical Thinking**: Structuring methods like MECE, logic trees
- **Critical Thinking**: Always question premises and logic validity
- **Systems Thinking**: Grasp the whole picture and understand interrelationships
- **Design Thinking**: User-centered problem-solving approach

### Major Frameworks
**Strategy Analysis**:
- 3C Analysis (Customer, Company, Competitor)
- 5C Analysis (3C + Collaborator, Context)
- Porter's 5 Forces (Industry structure analysis)
- SWOT Analysis (Strengths, Weaknesses, Opportunities, Threats)
- PEST/PESTEL Analysis (Macro-environment analysis)
- Value Chain Analysis
- BCG Matrix (Business portfolio analysis)

**Marketing**:
- 4P (Product, Price, Place, Promotion)
- STP (Segmentation, Targeting, Positioning)
- Customer Journey Map
- Brand Positioning Map

**Organization & Operations**:
- McKinsey 7S (Strategy, Structure, Systems, Skills, Staff, Style, Shared Values)
- RACI Matrix (Role and responsibility clarification)
- Balanced Scorecard

**Finance & Investment**:
- DCF (Discounted Cash Flow) Analysis
- ROI (Return on Investment) Analysis
- Breakeven Analysis
- NPV/IRR (Net Present Value/Internal Rate of Return)

**Technology**:
- Technology Adoption Curve
- Cloud Maturity Model
- Data Governance Framework

**Change Management**:
- Kotter's 8-Step Change Model
- ADKAR Model (Awareness, Desire, Knowledge, Ability, Reinforcement)
- Wave Theory (EY wave theory - staged transformation)

---

## ✓ Execution Checklist (Expanded)

Items Claude should check when executing this skill:

**Dialogue Approach**:
- [ ] Initial: Confirm challenge with brief questions
- [ ] Initial: Present firm format options
- [ ] Initial: Don't present multiple options (except format)
- [ ] Questions: Focus only on important points
- [ ] Start: After obtaining user consent and format confirmation

**Information Handling**:
- [ ] Initial: Basic skill information only
- [ ] Additional information: Load when needed
- [ ] Format characteristics: Understand after selection

**Phase 0 Confirmation**:
- [ ] Present firm format options
- [ ] Confirm user selection
- [ ] Understand selected format characteristics

**Phase 1 Confirmation**:
- [ ] Executable with basic dialogue
- [ ] Add analysis according to format
- [ ] Deeper information collection (8-15 items)
- [ ] Collect industry trends and benchmarks

**Phase 2 Confirmation**:
- [ ] Output complete workflow file
- [ ] Specify relationship for each slide
- [ ] Initialize progress status (all ⬜)
- [ ] Set up progress summary
- [ ] Document work interruption and resumption methods
- [ ] Reflect format-specific elements

**Phase 3 Confirmation**:
- [ ] Consolidate all slides into one MD file
- [ ] Always process one at a time, update MD file after each completion
- [ ] **Display progress table when starting each slide**
- [ ] Change progress status from ⬜→📝 when starting each slide
- [ ] **Present image diagram before creating slide**
- [ ] **Obtain user confirmation for image diagram**
- [ ] **Provide image diagram and composition explanation**
- [ ] Apply selected firm format
- [ ] Incorporate format-specific design elements
- [ ] **Present completed slide to user**
- [ ] **Obtain user confirmation for content**
- [ ] **Address modification requests and reconfirm**
- [ ] Change progress status from 📝→✅ after user approval
- [ ] Update progress summary (completed slides, progress rate)
- [ ] **Display updated progress table after completion**
- [ ] Clear search information after each slide completion
- [ ] Reconfirm design and progress before starting next slide
- [ ] Check relationships

**Quality Check**:
- [ ] Execute expanded checklist (8 items)
- [ ] Verify format-specific quality
- [ ] Verify progress management accuracy

**Throughout Overall**:
- [ ] Update MD file incrementally, always maintain latest state
- [ ] Update workflow file progress incrementally
- [ ] Don't retain unnecessary information after completion
- [ ] Reference appropriate responses when problems occur
- [ ] Don't repeatedly load same materials
- [ ] Don't execute python-pptx related processing
- [ ] Implement regular progress reporting

---

## 🚀 Usage Examples

### New Project (Format Specified):
```
User: "Analyze the feasibility of entering the cloud kitchen market in McKinsey format with all-consulting"

Claude:
[Load: SKILL.md core only]
[Understand McKinsey format characteristics]
Phase 1: Issue identification (McKinsey approach)
Phase 1-B: Hypothesis formulation (collect 8-15 items)
Phase 2: Workflow design (McKinsey standard, initialize progress status)
[Output [Project Name]_workflow_[Date].md - all slides ⬜]
Phase 3: Generate by slide units
  Create [Project Name]_presentation_[Date].md file
  
  Slide 1: 
    →Display progress table (0/15 slides, 0%)
    →Status ⬜→📝
    →Present image diagram
    →Explain composition
    →User confirmation "Is this image OK?"
    →Obtain user OK
    →Search→Create in McKinsey style→Self-check
    →Present completed slide
    →User confirmation "Is this content acceptable?"
    →Obtain user OK (or address modifications)
    →Status 📝→✅
    →Update MD file
    →Display progress table (1/15 slides, 7%)
    →"Shall we proceed to next?"
    →Obtain user OK
  [Clear Slide 1 context]
  
  Slide 2: 
    →Display progress table (1/15 slides, 7%)
    →Status ⬜→📝
    →Present image diagram
    →Explain composition
    →User confirmation "Is this image OK?"
    →Obtain user OK
    →Search→Create in McKinsey style→Self-check
    →Present completed slide
    →User confirmation "Is this content acceptable?"
    →Obtain user OK (or address modifications)
    →Status 📝→✅
    →Update MD file
    →Display progress table (2/15 slides, 13%)
    →"Shall we proceed to next?"
    →Obtain user OK
  [Clear Slide 2 context]
  ...
```

### New Project (Format Not Specified):
```
User: "I want to create a DX strategy document for retail business"

Claude:
What challenge would you like to create a document about?

Also, do you have a preferred format for the document?
(McKinsey/BCG/Bain/Deloitte/EY/PwC/Accenture/Abeam/NRI/Standard/None)

User: "Please use Accenture format"

Claude:
[Understand Accenture format characteristics]
[Start from Phase 1...]
```

### Resuming Work at Another Time:
```
[Different work session]
User: [Upload workflow file (with progress) and MD file]
      "Please continue from where we left off"

Claude:
[Load workflow file]
Progress check: 10/20 slides completed (50%)
Next uncreated slide: Slide 11
Format: BCG

Check design requirements for Slide 11
Change status from ⬜→📝
Start Slide 11: Search→Create in BCG style→Quality check
→Update MD file→Status 📝→✅
→Update progress (11/20 slides, 55%)→Pause

Report: "Slide 11 completed (✅). Progress: 11/20 slides (55%). Shall we proceed?"
```

---

---

## 📞 Support and Troubleshooting

### Frequently Asked Questions

**Q: Can I change the format midway?**
A: Not recommended for consistency, but regenerating the entire document with a new format is possible.

**Q: Can I mix multiple formats?**
A: While we recommend unifying with one format,
   applying a different style to specific slides only is also possible.

**Q: What if progress status doesn't update correctly?**
A: Manually check/correct the configuration file and re-upload it.

**Q: Can I pause work and resume days later?**
A: Yes. If you upload the configuration file (with progress) and presentation file,
   you can resume from the exact position.

**Q: Can I create a custom format?**
A: Currently only 10 standard formats available, but
   you can customize by selecting "Standard" format and communicating specific requirements.

---

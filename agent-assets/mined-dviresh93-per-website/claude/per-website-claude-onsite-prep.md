# Casium On-Site Interview - Claude Context & Rules

**Last Updated:** October 7, 2025
**Interview Status:** Scheduled (pending date selection)
**Interview Type:** On-site at Seattle office

---

## 🎯 Quick Context Prompt

**Use this prompt to resume interview prep:**

```
I'm preparing for my Casium on-site interview. Review the context in:
interview-prep/companies/casium/onsite-prep/claude.md

Help me practice [live coding | system design | both].
```

---

## 📋 Interview Details

### Company: Casium
- **What they do:** AI-powered immigration services platform
- **Mission:** Help global talent navigate U.S. immigration (O-1, H-1B, EB-1A, EB-2 NIW)
- **Backed by:** AI2 Incubator (Allen Institute for AI)
- **Location:** Seattle, WA
- **Stage:** Early-stage startup, engineering-driven culture

### Role: AI Product Engineer
- **Salary Range:** $130K - $200K + equity
- **Focus:** Building LLM-powered agents for immigration workflows
- **Tech Stack:** Python, FastAPI, SQLAlchemy, Postgres, LLM platforms
- **Key Skills:** RAG pipelines, vector databases, prompt engineering, embeddings

### Interview Format (2 hours total)
1. **Live Coding (1 hour)** - Shared text editor + projector
2. **System Design (1 hour)** - Whiteboard or drawing tool + projector

---

## 🔍 What Casium is Building

### Product Context
- **Immigration automation platform** using AI + human expertise
- **LLM-powered agents** that autonomously reason through complex immigration workflows
- **Document processing** and case preparation systems
- **Client-facing tools** for visa strategy and application tracking

### Technical Challenges They Face
1. **Domain complexity:** Immigration law is intricate, rule-based, with many edge cases
2. **Document processing:** Extract structured data from unstructured legal documents
3. **Case reasoning:** AI agents must navigate multi-step workflows (eligibility → strategy → filing)
4. **Accuracy requirements:** Immigration has zero tolerance for errors
5. **Regulatory compliance:** USCIS requirements, data privacy (sensitive personal info)

### Why This Matters for Interview
Your problems will likely involve:
- **Business logic with complex rules** (like immigration eligibility criteria)
- **Data transformations** (extracting/structuring information)
- **Multi-step workflows** (agent-like reasoning through conditions)
- **Date/time calculations** (visa validity, filing deadlines)
- **Edge case handling** (incomplete data, special circumstances)

---

## 📝 Previous Assessment Pattern (Woven)

### Prorating Subscriptions Problem
**File:** `interview-prep/companies/casium/prorating_subscriptions.md`

**Key Patterns:**
- Date/time calculations (activation/deactivation dates)
- Cross-year boundary handling
- Business logic (pro-rating based on active days)
- Financial calculations (rounding to cents)
- Edge cases (leap years, mid-month changes, None values)
- Data aggregation (per-user charges, total revenue)

**What They Valued:**
- Clean code organization (helper functions)
- Comprehensive edge case handling
- Proper date boundary logic (`max()`, `min()` for ranges)
- Clear documentation
- Test cases

---

## 🧠 Interview Preparation Strategy

### Live Coding Round

**Expected Problem Types:**
1. **Business logic with complex rules**
   - Immigration eligibility checks (multiple criteria)
   - Document validation workflows
   - Multi-step decision trees

2. **Data transformations**
   - Parse structured data from text
   - Aggregate/group data by criteria
   - Format output for downstream systems

3. **Date/time calculations**
   - Visa validity periods
   - Filing deadlines
   - Time-based eligibility

4. **API response handling**
   - Process JSON responses
   - Filter/transform for frontend
   - Error handling

**Preparation Focus:**
- Practice problems similar to `prorating_subscriptions.md`
- Business logic problems (billing, eligibility, workflows)
- Date/time edge cases
- Dictionaries and list comprehensions
- Edge case thinking (None, empty, boundaries)

**Communication Strategy:**
1. **Clarify requirements** (5 min)
   - Ask about input format, edge cases, constraints
   - Confirm expected output structure

2. **Explain approach** (5 min)
   - Walk through high-level logic
   - Mention helper functions you'll create
   - Discuss edge cases you'll handle

3. **Code with narration** (35 min)
   - Explain as you write
   - Call out edge cases as you handle them
   - Use clear variable names

4. **Test and discuss** (15 min)
   - Walk through example inputs
   - Test edge cases
   - Discuss optimizations or alternative approaches

---

### System Design Round

**📘 DETAILED COACHING GUIDE:**
See `system_design_coaching.md` in this folder for comprehensive system design coaching methodology.

**Expected Problem Types:**
1. **Immigration-specific systems**
   - Visa application tracking system
   - Document management platform
   - Client-attorney collaboration tool
   - Case recommendation engine

2. **Core Components to Know:**
   - Database schema design (entities, relationships) - **30% weight**
   - REST API design (endpoints, request/response) - **30% weight**
   - Distributed components (load balancer, cache, queue, S3) - **40% weight**
   - LLM integration patterns (RAG, agents, prompt engineering)
   - Async processing (document parsing, agent reasoning)
   - File storage (S3 for documents)
   - Authentication/authorization (sensitive data access)

**Interview Approach (from system_design_coaching.md):**
1. **Clarifying questions** (5-10 min) - Understand requirements before designing
2. **High-level architecture** (10 min) - Draw boxes and arrows, explain components
3. **Database design deep dive** (15 min) - Tables, relationships, indexes
4. **API design** (10 min) - RESTful endpoints, async operations
5. **Scaling & trade-offs** (10 min) - Identify bottlenecks, propose solutions

**Database Design Patterns:**
```
Core entities for immigration platform:
- users (clients, attorneys, admins)
- cases (visa type, status, deadlines)
- documents (passports, diplomas, letters)
- workflows (steps, approvals, dependencies)
- eligibility_checks (rules, results)
- payments (invoices, subscriptions)
```

**API Design Patterns:**
```
RESTful endpoints:
POST   /api/cases                    # Create new case
GET    /api/cases/{id}               # Get case details
PUT    /api/cases/{id}               # Update case
GET    /api/cases/{id}/documents     # List case documents
POST   /api/cases/{id}/documents     # Upload document
GET    /api/cases/{id}/eligibility   # Check eligibility
POST   /api/cases/{id}/submit        # Submit to USCIS
```

**AI/LLM Integration:**
- RAG for legal document search
- Agents for case analysis workflow
- Vector databases for document similarity
- Prompt engineering for structured output
- Validation layers (like GridCOP dual validation)

**Scalability Considerations (moderate scale):**
- Load balancer → app servers (2-3 instances)
- Postgres with read replicas
- Redis cache for session/frequent queries
- Celery + RabbitMQ for async jobs (document processing, LLM calls)
- S3 for document storage
- External APIs: LLM providers (OpenAI/Anthropic), payment (Stripe)

---

## 🎓 Casium-Specific Knowledge

### Immigration Domain Basics (know enough to design systems)

**Visa Types They Handle:**
- **O-1:** Extraordinary ability (artists, scientists, athletes)
- **H-1B:** Specialty occupation (tech workers)
- **TN:** NAFTA professionals (Canada/Mexico)
- **EB-1A:** Employment-based green card (extraordinary ability)
- **EB-2 NIW:** National Interest Waiver

**Key Workflow Steps:**
1. Eligibility assessment
2. Strategy consultation
3. Document collection
4. Case preparation
5. USCIS filing
6. Case monitoring
7. Approval/RFE handling

**Data You Might See in Problems:**
- User profiles (education, work history, publications)
- Document metadata (type, upload date, verification status)
- Case timelines (filing dates, deadlines, status changes)
- Eligibility criteria (education level, salary thresholds, achievement metrics)

---

## 🛠️ Technical Preparation Checklist

### Python Patterns to Master
- [ ] Date/time handling (`datetime`, `calendar`, boundary calculations)
- [ ] Decimal for financial calculations
- [ ] Dictionary comprehensions and grouping
- [ ] List filtering and transformations
- [ ] Helper function extraction
- [ ] Edge case handling (None, empty, boundaries)
- [ ] Type hints and clear documentation

### System Design Topics
- [ ] Database schema design methodology
- [ ] REST API design patterns
- [ ] RAG architecture (retrieval → context → generation)
- [ ] AI agent workflows (reasoning, tool use, validation)
- [ ] Async job processing patterns
- [ ] File upload/storage systems
- [ ] Authentication and authorization
- [ ] Error handling and logging

### Casium-Specific Prep
- [ ] Review immigration workflow (eligibility → filing → approval)
- [ ] Understand visa types and their requirements
- [ ] Think about document processing challenges
- [ ] Consider LLM hallucination risks in legal context
- [ ] Practice explaining GridCOP validation approach (relevant!)

---

## 📚 Practice Materials

### From Your Existing Prep
1. **`prorating_subscriptions.md`** - MUST REVIEW (this is their style)
2. **`real_interview_question.py`** - Complexity reference
3. **`subscription_billing.py`** - Business logic practice
4. **`emergency_prep.py`** - Quick Python patterns review
5. **Database schema materials** - All files in casium folder
6. **`onsite_interview_prep.md`** - System design examples

### Practice Problems to Create
Create 3-5 Casium-themed practice problems:
1. **Visa eligibility checker** (business logic + rules)
2. **Document status tracker** (data transformation)
3. **Case deadline calculator** (date/time logic)
4. **Immigration case system design** (full system design)
5. **Document parsing API** (data extraction + validation)

---

## 🎯 Day-Of Strategy

### Morning Routine
1. Review this file (claude.md)
2. Skim `prorating_subscriptions.md` solution
3. Practice one coding problem OUT LOUD (30 min)
4. Review system design template (database + API + components)
5. **Leave early** - parking + train issues at Pier 70

### During Interview

**Live Coding:**
- Start with clarifying questions
- Explain approach before coding
- Think out loud
- Handle edge cases explicitly
- Test with examples
- Discuss trade-offs

**System Design:**
- Clarify requirements first (scale, features, constraints)
- Start with entities and relationships
- Design database schema (tables, keys, indexes)
- Design API endpoints (REST patterns)
- Add distributed components as needed
- Discuss AI/LLM integration carefully (they care about this!)
- Address edge cases and failure modes

### Key Differentiators
1. **Immigration domain knowledge** - show you understand the problem space
2. **AI safety mindset** - discuss hallucination risks, validation (like GridCOP)
3. **Production thinking** - error handling, logging, monitoring
4. **Clear communication** - they value collaborative problem solving

---

## 💡 Your Relevant Experience to Highlight

### GridCOP (Grid CoOperator) - HIGHLY RELEVANT
- Built LLM-powered agent for critical decision-making
- **Dual validation system** (schema + domain rules) → 60% to 90% accuracy
- Production deployment with zero-tolerance for errors
- Similar to immigration: complex rules, no room for mistakes

**Key Talking Points:**
- "At GridCOP, we faced similar challenges - LLMs generating valid queries that made no semantic sense. Like immigration, power grid data has strict domain rules."
- "We implemented dual validation: structural checks + business logic validation. Same approach would work for immigration eligibility - validate both data format AND legal requirements."
- "The key was making analysts trust the AI for critical decisions. In immigration, trust is even more important."

### Drone Log Analysis - Relevant for RAG
- Built RAG system with two-tier vector database
- Handled multi-product context (similar to multi-visa-type context)
- Reduced hallucinations by restructuring retrieval
- Local LLM for sensitive data

**Key Talking Points:**
- "In our drone tool, mixing up product names caused wrong recommendations - similar risk in immigration if AI confuses visa types."
- "Two-tier vector database: summaries + detailed content. Could work for immigration docs - index case summaries, fetch full documents only when needed."
- "Used local LLMs for customer data privacy - same concern with immigration data (SSNs, personal info)."

---

## 🚀 Success Metrics

**You'll know you're ready when:**
- [ ] Can solve `prorating_subscriptions.md` in 30 min with clean code
- [ ] Can design a complete system (DB + API + components) in 30 min
- [ ] Can explain GridCOP validation approach clearly
- [ ] Understand immigration workflow well enough to design for it
- [ ] Can discuss AI safety (hallucination, validation, privacy) confidently

**During interview, success looks like:**
- Clear communication of thought process
- Systematic approach (not jumping to code)
- Comprehensive edge case handling
- Production-quality thinking (not just working code)
- Relevant experience references (GridCOP, Drone tool)

---

## 📝 Questions to Ask Them

**Technical:**
- How do you handle LLM hallucinations in a zero-error domain like immigration?
- What's your RAG architecture for legal document retrieval?
- How do you validate agent outputs before they affect real cases?
- What's your approach to keeping immigration rules up-to-date in the system?

**Product:**
- How do clients interact with AI features vs attorney review?
- What's the balance between automation and human expertise?
- Which workflows have you successfully automated so far?

**Team:**
- How does the engineering team collaborate with immigration attorneys?
- What's your AI experimentation process?
- How do you approach technical debt vs new features?

---

## 🔄 Iteration & Improvement

**After practice sessions, track:**
- Problems solved successfully
- Patterns that caused difficulty
- Edge cases missed
- Communication clarity
- Time management

**This file should evolve as you practice. Update with:**
- New insights from practice problems
- Patterns you've mastered
- Areas needing more work
- Any new information about Casium or the interview

---

## 📌 Quick Reference Links

**Your Materials:**
- Main prep: `/interview-prep/companies/casium/onsite_interview_prep.md`
- Woven problem: `/interview-prep/companies/casium/prorating_subscriptions.md`
- Python practice: `/interview-prep/companies/casium/[python files]`
- Schema practice: `/interview-prep/companies/casium/[schema files]`
- This context: `/interview-prep/companies/casium/onsite-prep/claude.md`

**External:**
- Company: https://www.casium.com/
- Role: https://jobs.ashbyhq.com/casium/3b67ea29-f115-40e5-b516-f1c95701f6ce
- Your portfolio: https://vireshduvvuri.com

---

**Remember:** You've built production AI systems that handled critical decisions (GridCOP) and sensitive data (Drone tool). Casium's challenges are similar - just applied to immigration. You've got this! 🚀

---

## 📝 Coaching Session Format (Use This Pattern!)

**File Structure for Practice Sessions:**

Use `.txt` files (not `.md`) for practice sessions. Template:

```
================================================================================
PRACTICE SESSION [NUMBER]: [PROBLEM NAME]
================================================================================

Date: [DATE]
Problem: [Problem Name] (Difficulty, Time estimate)
Reference: [path to problem file]

Coach: Claude
Student: Viresh

================================================================================
PROBLEM STATEMENT
================================================================================

[Full problem description, inputs, outputs, examples]

================================================================================
7-STEP FRAMEWORK
================================================================================

✅ Step 1: Listen & Take Notes
✅ Step 2: Ask Clarifying Questions
✅ Step 3: Confirm Examples
⏸️ Step 4: Explain Approach (IN PLAIN ENGLISH - wait for approval!)
⏸️ Step 5: Write Pseudocode/Comments
⏸️ Step 6: Code + Narrate
⏸️ Step 7: Test Out Loud

================================================================================
STEP 1: LISTEN & TAKE NOTES
================================================================================

YOUR NOTES (write what you understand about the problem):

[Student writes here]


================================================================================
COACH FEEDBACK ON STEP 1
================================================================================

[Coach provides feedback here - IN THE CORRECT SECTION!]


================================================================================
STEP 2: ASK CLARIFYING QUESTIONS
================================================================================

YOUR QUESTIONS (ask about edge cases, assumptions, constraints):

[Student writes here]


================================================================================
COACH RESPONSES TO YOUR QUESTIONS
================================================================================

[Coach answers questions here - IN THE CORRECT SECTION!]


================================================================================
STEP 3: CONFIRM EXAMPLES
================================================================================

YOUR EXAMPLE WALKTHROUGH (pick one example and trace through it):

[Student writes here - MUST INCLUDE ACTUAL NUMBERS AND CALCULATIONS]


================================================================================
COACH FEEDBACK ON YOUR UNDERSTANDING
================================================================================

[Coach confirms if calculation is correct - IN THE CORRECT SECTION!]


================================================================================
STEP 4: EXPLAIN YOUR APPROACH (IN PLAIN ENGLISH!)
================================================================================

REMINDER: Do NOT write code yet. Explain in words:
- High-level approach
- Helper functions you'll need (if any)
- Edge cases you'll handle
- Why this approach makes sense

YOUR APPROACH:

[Student writes here]


================================================================================
COACH FEEDBACK & APPROVAL
================================================================================

[Coach reviews approach and gives green light to code - IN THE CORRECT SECTION!]


================================================================================
STEP 5: WRITE PSEUDOCODE/COMMENTS
================================================================================

YOUR PSEUDOCODE (outline the structure with comments):

[Student writes here]


================================================================================
STEP 6: CODE + NARRATE
================================================================================

YOUR CODE (write the implementation):

[Student writes here]


================================================================================
COACH FEEDBACK ON YOUR CODE
================================================================================

[Coach reviews for bugs, edge cases, code quality - IN THE CORRECT SECTION!]


================================================================================
STEP 7: TEST OUT LOUD
================================================================================

YOUR TEST CASES (walk through examples step-by-step):

[Student writes here]


================================================================================
FINAL COACH FEEDBACK
================================================================================

[Coach provides summary feedback on all 4 criteria - IN THE CORRECT SECTION!]


================================================================================
SESSION NOTES
================================================================================

[This section will be filled at the end]
```

---

## 🎓 Coaching Rules for Claude

**CRITICAL RULES:**

1. **ALWAYS write feedback in the CORRECT section** - not at the end of the file!
   - Step 1 feedback → "COACH FEEDBACK ON STEP 1" section
   - Step 2 answers → "COACH RESPONSES TO YOUR QUESTIONS" section
   - Step 3 feedback → "COACH FEEDBACK ON YOUR UNDERSTANDING" section
   - Step 4 approval → "COACH FEEDBACK & APPROVAL" section
   - Step 6 review → "COACH FEEDBACK ON YOUR CODE" section
   - Final feedback → "FINAL COACH FEEDBACK" section

2. **Step 3 MUST include actual calculations**
   - Not just "I'll validate and compute"
   - Must show: Input → Validation (with ✓/✗) → Calculation (with $) → Output

3. **Don't let student skip ahead**
   - If they jump to code in Step 4, redirect to explain in plain English first
   - If they skip Step 3 calculations, require them to redo with numbers

4. **Keep it simple**
   - For single-function problems: functions, not classes
   - Match solution complexity to problem scope

5. **Highlight missed edge cases**
   - After student asks questions, note what they missed
   - But let them discover some during coding/testing (realistic!)

---

## 📂 Practice Session Files

All practice sessions go in: `interview-prep/companies/casium/onsite-prep/`

Naming: `practice_session_[number][letter].txt`
- Example: `practice_session_1.txt`, `practice_session_1b.txt`

---

## 🎨 System Design Coaching Modes

**Reference:** `system_design_coaching.md` for full methodology

### Two Coaching Modes

**1. Teaching Mode (70% of time)**
Use when student asks questions or needs concept explained:
- Be conversational and helpful
- Show examples and comparisons
- Allow back-and-forth discussion
- Correct mistakes immediately
- "Let's think about it - Redis has more features..."

**2. Mock Interview Mode (30% of time)**
Use for full practice interviews:
- Simulate real interview conditions
- Stay in character as interviewer
- Let them struggle appropriately
- Only intervene if completely stuck
- Give comprehensive feedback at end
- "Interesting. What happens if two users upload at the same time?"

### System Design Interview Flow (60 minutes)

**Minutes 0-5: Present Problem**
Give Casium-themed problem (document processing, case tracking, workflow system)

**Minutes 5-10: Clarifying Questions**
- Let them ask questions
- Answer like real interviewer
- Evaluate question quality

**Minutes 10-20: High-Level Design**
- Let them draw architecture
- Ask follow-ups: "Why did you choose [component]?"
- Guide if they forget critical components

**Minutes 20-35: Database Design Deep Dive** ⭐ MOST IMPORTANT
- "Let's dive into your database schema"
- Look for: relationships, indexes, multi-tenancy, audit trail
- Ask probing questions about queries and edge cases

**Minutes 35-45: API Design**
- "Show me 2-3 key endpoints"
- Check: HTTP verbs, request/response, status codes, async handling
- Ask about error handling and pagination

**Minutes 45-55: Scaling & Trade-offs**
- "What if we grow 10x?"
- Expect specific bottleneck identification
- Look for concrete solutions, not vague "add more servers"

**Minutes 55-60: Feedback**
- Ask for self-reflection first
- Give structured feedback (strengths + improvements)
- Be specific and actionable

### Startup-Specific Focus (Not FAANG Scale)

**Scale Context:**
- 100-1000 companies
- 10K-100K users
- 500-5000 requests/day
- NOT billions of users

**What Matters:**
- ✅ Correct architectural choices
- ✅ Database design (tables, relationships, indexes)
- ✅ API patterns (REST, async, status codes)
- ✅ When to use cache/queue/S3
- ❌ NOT sharding across datacenters
- ❌ NOT handling billions of QPS

### Key Evaluation Criteria

**Database Design (30%):**
- [ ] Proper table structure and relationships
- [ ] Appropriate data types
- [ ] Indexes on frequently queried fields
- [ ] Multi-tenancy (company_id in all tables)
- [ ] Audit trail if required
- [ ] Files in S3, not DB

**API Design (30%):**
- [ ] RESTful conventions
- [ ] Proper HTTP verbs and status codes
- [ ] Async operations (202 Accepted)
- [ ] Pagination on list endpoints
- [ ] Clear request/response formats

**Distributed Components (40%):**
- [ ] Load balancer for multiple app servers
- [ ] Cache for read-heavy data
- [ ] Message queue for slow operations
- [ ] Object storage for files
- [ ] Clear explanation of WHY each component

### Common Mistakes to Catch

**Teaching Mode - Correct Immediately:**
- ❌ Storing files in database → "Let's think about storage costs..."
- ❌ No indexes → "How will you query by user_id at 1M records?"
- ❌ Synchronous slow operations → "Users wait 5 seconds. How else?"

**Mock Mode - Note for Feedback:**
- Take notes during interview
- Only redirect if going completely wrong
- Address all issues in final feedback

### Practice Problem Examples

**Easy:**
"Design a URL shortener supporting 1,000 URLs/day and 10,000 redirects/day"

**Medium (Casium-style):**
"Design a document processing system where users upload immigration documents, AI extracts data, lawyers review and edit, system tracks all changes. Support 100 companies, 10K users, 50 lawyers."

**Focus areas:** File storage, AI integration, audit logging, multi-tenancy, async processing

---

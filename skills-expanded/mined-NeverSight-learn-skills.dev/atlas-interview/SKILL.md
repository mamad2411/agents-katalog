---
name: atlas-interview
description: Generate tailored interview questions for a candidate with configurable pressure levels (supportive/standard/aggressive) and follow-up probing based on actual candidate answers. Use this skill whenever someone asks to generate interview questions, prepare for an interview, create behavioral or technical questions for a candidate, probe a candidate's answer, get follow-up questions, or do interview prep. Also use when someone mentions "what should I ask this candidate" or "interview this person". This is for question GENERATION — for scoring an interview transcript after the fact, use atlas_start_dialogue_assessment directly.
disable-model-invocation: true
argument-hint: "[candidate name]"
---

# Atlas Interview — Question Generation & Follow-Up Probing

Generate tailored interview questions based on a candidate's profile and optionally probe their answers with AI-generated follow-ups.

## Workflow

### Step 1: Identify the Candidate (FREE)

1. Call `atlas_list_contexts` to find the hiring context
2. Call `atlas_list_candidates` with `context_id` to find the candidate
3. Optionally call `atlas_list_jds` with `context_id` to get the JD (enriches question relevance)

If no context/candidates exist, direct user to `/atlas-onboard` first.

### Step 2: Configure Questions

Ask the user:
- **Pressure level:** `supportive` / `standard` / `aggressive` (default: standard)
  - Supportive: Best for early career or lateral moves
  - Standard: General-purpose behavioral + technical
  - Aggressive: Best for senior/leadership roles — harder probing questions
- **Number of questions:** 1-15 (default: 5)

### Step 3: Generate Interview Questions (8 credits)

Call `atlas_generate_interview` with:
- `context_id`
- `candidate_id`
- `jd_text` (optional but recommended — get from `atlas_list_jds`)
- `pressure_level`
- `num_questions`

This is synchronous — no polling needed.

Present each question with:
- **Question text**
- **Rationale** — Why this question matters for this candidate
- **What to look for** in the answer

### Step 4: Optional — Follow-Up Probing (1 credit each)

If the user has candidate answers from a real interview:

For each question-answer pair, call `atlas_interview_followup` with:
- `context_id`
- `candidate_id`
- `original_question` — The question text
- `candidate_answer` — What the candidate said
- `pressure_level`

Present the AI-generated follow-up probe with rationale for why this follow-up digs deeper.

### Step 5: Next Steps

After the interview prep, offer:
- **Competency scoring:** Run `/atlas-gem` to score the candidate
- **Role matching:** Run `/atlas-fit` to check JD alignment
- **Dialogue assessment:** If you have a full interview transcript, mention that `atlas_start_dialogue_assessment` can score the conversation (10 credits)

## Credit Cost

| Action | Cost |
|--------|------|
| Setup & identification | FREE |
| Generate questions | 8 credits |
| Each follow-up probe | 1 credit |

**Typical session:** 8 credits (questions) + 3-5 follow-ups = **11-13 credits**

## Tips

- Including JD text generates role-specific questions (vs generic behavioral) — always include it if available
- Aggressive pressure level generates harder probing questions — best for C-suite and VP roles
- Supportive mode works well for early career candidates or lateral moves
- Follow-up probes are powerful for real interview debriefs — feed actual candidate answers to get AI-generated probes
- Questions are tailored to the candidate's specific CV — they reference the candidate's experience and gaps

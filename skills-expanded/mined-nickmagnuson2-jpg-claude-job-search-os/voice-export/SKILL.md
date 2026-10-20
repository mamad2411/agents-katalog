---
name: voice-export
description: Generate a recruiter simulation prompt for the Claude App (voice mode) from a CV and job ad URL
argument-hint: <path-to-cv> <job-ad-url>
user-invocable: true
allowed-tools: Read(*), Glob(*), Grep(*), WebFetch
---

# Voice Export — Generate Recruiter Simulation Prompt

Generate a self-contained recruiter screening simulation prompt that can be pasted into the Claude App (voice mode). The recruiter stays in character for the entire call — no coaching, no interruptions. Coaching happens afterwards in Claude Code.

## Arguments

- `$ARGUMENTS` (required): Two arguments separated by space:
  1. Path to the CV file (e.g. `output/20260210-target-role-slug.md`)
  2. Job ad URL (e.g. `https://www.upwork.com/project/...`)

## Instructions

### Step 1: Parse Arguments

Extract the CV path and job ad URL from `$ARGUMENTS`. If only one argument is provided, ask the user for the missing one.

### Step 2: Load Sources

1. Read the CV file.
2. Fetch the job ad from the URL using WebFetch.
3. Auto-detect a deep review file: take the CV filename, append `-DEEP-REVIEW` before the extension.
   - Example: CV `output/20260210-target-role-slug.md` → look for `output/20260210-target-role-slug-DEEP-REVIEW.md`
   - If the file exists, read it. If not, skip — the question pool will rely on gap analysis only.
4. Auto-detect a cheat sheet file: take the CV filename, append `-cheatsheet` before the extension.
   - Example: CV `output/20260210-target-role-slug.md` → look for `output/20260210-target-role-slug-cheatsheet.md`
   - If the file exists, read **only the header section above the first `---`** for recruiter persona enrichment (name, company context, intermediary vs. end client). Do NOT read below the first `---` — that contains coached answers and candidate prep.
5. Read `framework/voice-export.md` for the export prompt structure and quality rules.

### Step 3: Detect Language

Determine the CV language by scanning section headers and body text. Common header patterns:
- English: "Summary", "Skills", "Certifications", "Projects" → **EN**
- German: "Kurzprofil", "Fachkenntnisse", "Zertifizierungen" → **DE**
- French: "Compétences", "Expérience", "Formation" → **FR**
- Dutch: "Vaardigheden", "Werkervaring", "Opleiding" → **NL**
- Spanish: "Habilidades", "Experiencia", "Formación" → **ES**
- Other languages → infer from content
- If uncertain → default to **EN**

All generated prompt text must match this language.

### Step 3b: Set the four persona axes (mandatory — do NOT default to a warm recruiter)

A warm-recruiter sim cannot rehearse the muscle a cold adversarial deep-dive tests. The most valuable reps recreate the pressure of the *actual next interviewer*. Before building the persona, read the pipeline **Next-Action** and the interviewer's `data/people/<slug>.md` dossier if one exists, then set all four axes explicitly:

| Axis | Options | How to set it |
|---|---|---|
| **1. Temperature** | adversarial / cold / skeptical ⟷ warm gatekeeper | From the round. Ask "adversarial or warm?" **only if genuinely ambiguous** — don't ask when the round type already answers it. |
| **2. Interviewer persona** | a named person, not a generic recruiter | Build from `data/people/<slug>.md`: background, fluency, what they screen for. An ex-consulting deep-dive interviewer behaves nothing like a warm phone screen. |
| **3. Round type** | recruiter screen / behavioral deep-dive / case / founder vibe-check | Drives question shape AND pacing, not just content. |
| **4. Scenario hold** | required whenever the sim carries a scenario | See Step 6 §8 below. |

**Seed the persona with current-week company facts** from the freshest dossier, so the sim interrogates from accurate present state rather than stale context.

**Length variant — offer it, don't wait to be asked:**
- **Full sim** (~15-20 min) — the complete loop. (Was "~25 min" here while Step 6 and `framework/voice-export.md` said 15-20; reconciled to 15-20 on 2026-10-06.)
- **Focused rep** (~10-12 min) — names the must-hit beats up front and **guarantees the run reaches them**. Use before a real call. This exists because an open-ended full sim ran out of time before the highest-value beat: the live-need bridge (hypothesis H4), which is the recurring miss. A focused rep that reaches the bridge beats a longer unfocused one.

### Step 4: Extract Recruiter Persona

Build from the Step 3b axes, the job ad, and the cheat sheet header if available:
- **Company name** and brief context (1-2 sentences) — cheat sheet may clarify intermediary vs. end client
- **Role title** / project description
- **Start date, duration, utilisation, remote/onsite**
- **Interviewer name and background** — prefer the real named interviewer from `data/people/<slug>.md`. Only generate a plausible recruiter name matching the job ad's market/language when no real interviewer is known.
- **Temperature and round-type behaviors** from Step 3b, written into the persona as concrete instructions ("you are skeptical and press for numbers; you do not offer encouragement"), not as an adjective.

### Step 5: Build Question Pool

Assemble the question pool from three sources:

#### A. Deep Review Questions (if file exists)
- Extract the "Top 10 Probing Interview Questions" section from the deep review file
- Include all questions verbatim — these are the highest-value probes

#### B. Gap-Derived Questions
- Compare job ad requirements against the CV
- Generate 3-5 questions targeting: technical gaps, experience depth mismatches, role-fit concerns
- Do NOT duplicate topics already covered by deep review questions

#### C. Standard Recruiter Topics
Always include these topics (the recruiter weaves them in naturally):
- Compensation expectations and flexibility (rate for freelance/contract roles, salary for permanent — derive from the CV and job ad context)
- Availability, notice period, or earliest start date
- Remote/onsite preferences and travel willingness
- Motivation for this specific role
- Current employment or engagement status
- Invoicing entity / contracting setup (for freelance/contract roles only, if relevant based on CV)

### Step 6: Assemble the Prompt

Build the prompt following this exact section order (use `##` headers):

1. **System Instruction** — Role assignment: realistic recruiter, no coaching, stay in character
2. **Recruiter Persona** — From Step 4
3. **Candidate CV** — Full CV text inlined (the recruiter "has it on their desk")
4. **Question Pool** — From Step 5. Mark this section as internal to the recruiter: "These are topics and questions for you to draw from during the call. Weave them into natural conversation — do not read them as a list."
5. **Call Flow Guidelines** — Natural pacing: intro → candidate pitch → technical/experience questions → compensation/logistics → closing with next steps. Target 15-20 minutes for a full sim, 10-12 for a focused rep. Go deeper on fewer questions rather than rushing through all.

   **For a focused rep**, replace the open flow with the named must-hit beats and instruct the persona to reach every one before closing — e.g. force a substance-first open, demand the numbers, and GUARANTEE the run reaches the live-need moment. A rep that ends before its target beat produced nothing.
6. **Session Rules** — Language match, stay in character, natural behaviour, ending instruction ("End of simulation. Take this conversation to Claude Code for a full debrief with your coaching files.")
7. **Opening and handshake** — match CV language. **Do NOT end the prompt with a start line such as `Say "Start" to begin the call`**: Step 7 property 1 fails exactly that. Instead put the persona's exact first words at the TOP of the prompt followed by "and nothing else" (property 1), and instruct the partner to reply with one word (`Ready.`), say nothing else, and deliver those first words only after the operator says `go` (property 8). This item prescribed the start line until 2026-10-06, which contradicted the Step 7 gate.

8. **Scenario Hold Clause** — **MANDATORY whenever the sim carries a scenario, case, prompt, or exercise.** "Open with Scenario 1" is not sufficient. A persona told only to open with a scenario will follow the candidate's first interesting tangent and never return to it, and the rep silently tests nothing. Write the recovery behavior explicitly:

   > *You are running Scenario X. If the candidate opens somewhere else or drifts, acknowledge briefly, then bring the conversation back to Scenario X before moving on. Do not proceed to any other topic until Scenario X has been worked. If the candidate resists twice, name it directly and return to it a third time.*

   Omit this section only when the sim genuinely has no scenario.

### Step 7: Structural pre-handover gate (MANDATORY - eight properties)

**Run this before Step 7b. A prompt that fails any property is not ready to hand over, however well
it reads.** The prose describing a role does almost none of the work; these eight structural
properties do, and each has to be BUILT rather than STATED. If the answer to any check is "it says so
in the prose," it is not built.

Origin: four consecutive failed sim attempts across two days, then two more structural defects a day
later. Every textual fix failed; the first structural fix held immediately. Full incident record:
`memory/feedback_persona_sim_prompts_need_structural_role_binding.md`.

| # | Property | The check | Fails when |
|---|---|---|---|
| 1 | **First words, literal** | The exact opening utterance appears at the top, followed by "and nothing else." | The prompt ends with a handshake line like "Say Start to begin" - ambiguous about who speaks, and a trailing instruction is the one most likely to be read as addressed to the model. |
| 2 | **Role bound to the speaker by name** | The prompt states *the person speaking to you is the candidate, his name is <Name>*, plus the corollary: if the candidate asks something the scenario should answer, **invent a plausible specific answer in character**. | "You are running a session with a candidate" - the model has no way to know the person talking to it IS that candidate. Produces mid-session role flips. |
| 3 | **Prohibition with a pre-send self-check** | The prohibition has its own section, enumerates the specific forbidden moves, and attaches a self-check: *if what you are about to say contains a suggested phrasing, an evaluation, or the word "better", delete it and ask a follow-up instead.* | Stated once in passing. Assistant-tuned models drift toward coaching over ~20 turns; a single mention loses to default helpfulness. |
| 4 | **Under ~6KB per paste** | Byte-count each paste. | One long document. Persona and rules at the top decay by mid-session. **Note: this ceiling is necessary, not sufficient - a 5,773-byte prompt still failed on task shape.** |
| 5 | **Each paste standalone** | Every paste repeats the role binding, the prohibition, and the first-words block. | A part-two prompt that says "same rules as before" inherits nothing when pasted into a fresh conversation. |
| 6 | **Position** | The durable half goes in the host's **persistent instructions field**, set once. The variable half is the **first message** of a new chat. | The persona is pasted as message one. It is then just message one of a conversation, carries no privileged status, and decays after roughly one turn. This defect survived three separate content rewrites before it was diagnosed. |
| 7 | **Task shape: one probe per chat** | Unless the prompt explicitly declares case mode, it carries exactly ONE probe. | A multi-probe prompt invites the partner to develop the opening question into a case. In the worst run, 7 of 8 scheduled probes never ran. **Drift is impossible when there is nothing to drift into.** |
| 8 | **Handshake** | The partner replies with one word (`Ready.`), says nothing else, and delivers the probe only after the operator says `go`. | The opening line arrives as text before the mic is live and gets read rather than heard, silently destroying a blind design. |

**Property 6 is the one to check first**, because a prompt can satisfy the other seven and still fail
completely. Properties 1-5 are all "state the rule more structurally." Property 6 is "put the rule
where it gets re-read," which is the same distinction as the CLAUDE.md enforcement-tier law: a rule
stated in a place that scrolls away is not built.

**Property 7 carries a diagnosis worth reusing.** When an instruction repeatedly loses to the model's
reading of the task, **change the task, not the wording.** The failing probe was itself case-shaped,
so telling a competent interviewer model to develop nothing fought the semantics of the question it
had just been handed.

**Operator setup steps are part of the prompt surface.** A setup step that lives only in the
operator's head silently costs the measurement - recording software left off made three probes nearly
unscoreable. If the rep depends on it, put it in the artifact.

**Output requirement:** print the eight-property verdict alongside the Step 8 summary, one line each,
`ok` or the property number plus what is missing. A silent pass is the `[[feedback_llm_self_policing_fails]]`
failure this gate exists to prevent.

### Step 7b: Quality Check

1. **Byte-count each paste.** Step 7 property 4 is the ceiling: under ~6KB per paste. If a paste is over, apply the compression strategies from `framework/voice-export.md` in priority order, or split it into standalone pastes (property 5). The earlier 8,000-word limit here was looser than the gate and is superseded.
2. **Scan for file references.** If any path-like string (`data/...`, `coaching/...`, `output/...`) appears in the prompt, remove it — everything must be inline.
3. **Check language consistency.** No mixing DE/EN within the prompt.
4. **Verify no coached answers leaked.** The prompt must NOT contain any prepared candidate answers.

### Step 8: Output

Output the prompt as **two fenced code blocks** (` ```markdown ... ``` `), per Step 7 property 6: (1) the **durable half** (role binding, prohibition with self-check, persona, session rules) to set once in the host app's persistent-instructions field; (2) the **variable half** (this rep's probe or call flow, opening with the first-words block and handshake) to paste as the first message of a new chat. Each block must stand alone (property 5). This step said "a single fenced code block" until 2026-10-06, which the Step 7 gate would have failed.

Before the code block, print a short summary:
- Role name
- Language (DE/EN)
- Word count
- Deep review questions included? (Yes/No) — if No, add: `💡 Run /review-cv-deep <cv-path> first for more substantial probing questions in the simulation.`

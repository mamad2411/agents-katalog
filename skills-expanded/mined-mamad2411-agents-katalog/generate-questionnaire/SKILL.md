---
name: generate-questionnaire
description: "Generates structured questionnaires for IT project management: a client
  requirements questionnaire (Phase 1 — Initiation) and a lessons-learned questionnaire
  for the team (Phase 6 — Closure). Also structures received answers for downstream
  skills. Triggers RU: «сформируй опросник», «подготовь опросник для заказчика»,
  «создай бриф заказчику», «подготовь анкету по урокам», «структурируй ответы заказчика».
  Triggers EN: 'generate questionnaire', 'create client brief', 'prepare lessons
  questionnaire', 'structure stakeholder answers', 'prepare project brief'."
---

# Skill: generate-questionnaire

Generates structured questionnaires for IT project management. Two types:
(1) client questionnaire — collects initial requirements at project start;
(2) team questionnaire — collects lessons learned at project closure.
Also structures received answers for downstream skills.

---

## Triggers

**Russian:** «сформируй опросник», «подготовь опросник для заказчика», «создай бриф заказчику», «подготовь анкету по урокам», «структурируй ответы заказчика», «нужен опросник», «подготовь вопросы для заказчика»
**English:** "generate questionnaire", "create client brief", "prepare lessons questionnaire", "structure stakeholder answers", "build client brief", "prepare project brief"

---

## Language Detection

Determine the language of the user's request:
- If the request is in Russian → use templates with the `-ru` suffix
- Otherwise → use templates with the `-en` suffix
- All output (headings, labels, agent messages) must match the detected language.

---

## Input

| Data | Required | Source | Notes |
|------|:--------:|--------|-------|
| Questionnaire type | yes | command or CLAUDE.md | `client` (phase 1) or `lessons` (phase 6) |
| Project name | yes | CLAUDE.md or command | Used in the file header |
| Recipient(s) | yes | command or CLAUDE.md | Name and email. For `client` — project sponsor; for `lessons` — team members |
| PM name | no | CLAUDE.md | Inserted into questionnaire metadata |
| Response deadline (`deadline`) | no | command | For `lessons` type only. If not provided — ask: "Specify the deadline by which the team should submit their responses." |

If the type is not explicitly specified — determine from the project phase (from CLAUDE.md):
- Phase 1 (initiation) → `client`
- Phase 6 (closure) → `lessons`
- Otherwise → ask one clarifying question:

```
Please clarify what you need:
A) Create a client questionnaire (Phase 1 — Initiation)
B) Create a team lessons-learned questionnaire (Phase 6 — Closure)
C) Structure received client answers
D) Structure received team answers
```

---

## Output

| Type | File | Project path | Mode |
|------|------|--------------|------|
| client | `questionnaire-client.md` | `{project}/01-initiation/` | generate |
| lessons | `questionnaire-lessons.md` | `{project}/04-closure/` | generate |
| any | Structured report in chat | — | structure |

---

## Instructions

### Step 1 — Determine Mode and Type

Check the request type first:
- If the request contains "evaluate", "analyze", "is it worth doing", "give a recommendation on the project" → this is an analysis request outside the skill's scope. Respond:
  "This skill structures questionnaire data but does not analyze answers or assess project viability. I can structure the answers and pass them to generate-charter, where the agent will flag ambiguities. Continue?"
  Wait for confirmation. Do not proceed until confirmed.

Determine the mode:
- Command to generate / prepare / create a questionnaire → `generate` mode
- Received answers ready to be structured → `structure` mode

If the mode is unclear — ask the clarifying question (see template above).

---

### Step 2 — `generate` Mode: Create Questionnaire

1. Determine language.
2. Read the template:
   - `client` → `questionnaire-client-{lang}.md`
   - `lessons` → `questionnaire-lessons-{lang}.md`
3. Fill in metadata placeholders:

| Placeholder | Source | Notes |
|-------------|--------|-------|
| `{{project_name}}` | CLAUDE.md or command | |
| `{{recipient_name}}` | command or CLAUDE.md | |
| `{{pm_name}}` | CLAUDE.md (if available) | |
| `{{date}}` | current date (YYYY-MM-DD) | |
| `{{deadline}}` | command | `lessons` type only. If not in command — ask before saving. |

4. Save the file according to the Output table.
4a. If type is `lessons` and only 1 recipient is specified — append to the confirmation message:
    "1 recipient specified. If you need to add more — let me know before sending."
5. Show in chat:
   - What was created: "Questionnaire saved as [filename] in [path]."
   - Next step: "Prepare an email draft for sending?"
6. After confirmation — proceed to Step 3.
7. Log to `logs/log.md`: date, skill, created file, recipient.

---

### Step 3 — Prepare Email and Call send-email

Determine parameters by type:

| Type | Email template | Attachment | Format | Level |
|------|---------------|-----------|--------|-------|
| client | `email-tpl-questionnaire-client-{lang}.md` | questionnaire-client.md | .docx | 3 (with confirmation) |
| lessons | `email-tpl-questionnaire-lessons-{lang}.md` | questionnaire-lessons.md | .md | 2 (PM in CC) |

Autonomy levels:
- **Level 2** — agent sends the email; PM added to CC automatically.
- **Level 3** — agent shows email draft; waits for human confirmation before sending.

Call send-email:
```
send-email(
  type          = "questionnaire-[client|lessons]",
  recipients    = [list of recipients with email],
  template      = [path to email template],
  attachment    = [path to questionnaire file],
  attach_format = [.docx | .md],
  level         = [3 | 2]
)
```

> **Stub:** send-email is not yet implemented. Until it is — display an email draft based on the email template and offer to send manually via Gmail.

---

### Step 4 — `structure` Mode: Structure Answers

1. Receive answers from chat or an attached file.
2. Determine the answer type:
   - Answers about project goals, scope, constraints → `client` type
   - Answers about lessons learned and retrospective → `lessons` type
3. Structure by blocks matching the corresponding questionnaire template.
4. Flag unanswered and ambiguous questions.
5. Show in chat:
   - Structured data by block
   - List of unanswered / ambiguous items (if any)
   - Recommendation: "Pass data to [generate-charter | generate-closure-report]?"
6. On confirmation — offer to launch the downstream skill.

---

## Dependencies

**Reads:**
- `CLAUDE.md` of the managed project — project name, PM, contacts
- Templates from `templates/`: questionnaires (4 files) + email templates (4 files)

**Passes data to:**
- `generate-charter` — after structuring `client` answers (phase 1)
- `generate-closure-report` — after structuring `lessons` answers (phase 6)

**Calls:**
- `send-email` — delivery module (stub until implemented)

---

## Constraints

- Questionnaire template is fixed — questions are not generated dynamically by project type
- Does not analyze answers or assess project viability
- Does not send email directly — calls send-email
- Does not create the project charter or close the project — only passes data downstream
- Handles one project per invocation

---

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-04-06 | 1.0 | Skill created. Two questionnaire types (client, lessons). Two modes (generate, structure). send-email stub. |
| 2026-04-06 | 1.1 | Post-eval fixes (4/6 → 6/6): added `{{deadline}}` to input and placeholder tables; added step 4a for single-recipient warning (lessons); added guard rail in Step 1 for analysis requests. |

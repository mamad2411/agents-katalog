# Skill Router

## Role
You are a Skill Navigator. You take the user's free-form intent in natural language and route
it to the most appropriate installed skill — printing a ranked list with confidence scores and
explicit reasoning to chat, never executing the skill itself until the user confirms.

## Context — Read First

Scan all plugin manifests before routing:
- `.claude/plugins/claude-skills-std/.claude-plugin/plugin.json`
- `.claude/plugins/global/.claude-plugin/plugin.json` (if it exists)

For each skill path listed, read only the SKILL.md frontmatter (name + description fields).

## Instructions

### Step 1: Discover All Installed Skills

Run:
```bash
find .claude/plugins -name "SKILL.md" | head -80
```

For each SKILL.md found, read lines 1–10 (frontmatter only). Extract `name:` and `description:`.
Build an internal registry: `{ name, description, filePath }[]`.
Do NOT load full skill bodies at this stage.

### Step 2: Build Topic Taxonomy (silent — do not print)

Group the registry into 2 levels using description keywords:

| Domain | Keyword signals |
|--------|----------------|
| `code` | commit, migration, refactor, scaffold, feature, test, endpoint |
| `docs` | documentation, markdown, ADR, standard, drift, style |
| `skills` | skill, build, convert, audit, export, router, categorize |
| `research` | research, industry, feasibility, prompt, plan, deep |
| `session` | session, handoff, compact, harvest, journal, context |
| `infra` | GCP, WIF, secret, bootstrap, deploy, terraform, cloud |

Assign each skill to its best-fit domain. If no domain signal → assign `other`.

### Step 3: Score the User's Intent

Given the user's free-form text, compute TF-IDF weighted relevance for each skill:

1. **Tokenize** user intent: lowercase, split on whitespace/punctuation, remove tokens ≤ 2 chars
2. **Per skill**: count overlapping tokens between user tokens and description tokens
3. **IDF weight**: tokens appearing in ≤ 20% of descriptions score 2×; tokens in > 60% of
   descriptions score 0.5×
4. **Domain boost**: if user intent contains a domain signal from Step 2, boost all skills in
   that domain by 1.2×
5. **Normalize** all scores to 0.0–1.0

Identify `top_score` (rank 1) and `second_score` (rank 2). Compute `margin = top_score − second_score`.

### Step 4: Apply Confidence Gate

**Case A — Clear winner** (`top_score ≥ 0.5` AND `margin > 0.15`):
Proceed directly to Step 5 with activation recommendation.

**Case B — Close match** (`top_score ≥ 0.5` AND `margin ≤ 0.15`):
Ask exactly one binary clarifying question:
> "שתי אפשרויות קרובות: האם הכוונה **[skill-1]** (מתאים כשרוצים [X]) או **[skill-2]**
> (מתאים כשרוצים [Y])?"

Wait for user response. Promote chosen skill to rank 1 and proceed to Step 5.

**Case C — Weak signal** (`top_score < 0.5`):
Ask exactly one domain-level clarifying question:
> "הכוונה קשורה ל-**[domain-A]** (לדוגמה: [skill-example-1], [skill-example-2]) או
> ל-**[domain-B]** (לדוגמה: [skill-example-3], [skill-example-4])?"

After response, re-score only within the identified domain. Proceed to Step 5.

**Case D — No match** (all scores < 0.05):
Print:
> "לא נמצאה התאמה ברורה. תחומים זמינים: [list level-1 domains with one example each].
> תאר מה אתה מנסה להשיג."
Stop.

**Clarifying question rules:**
- Maximum **one** question total per routing session — never ask a second.
- If user declines to answer → promote top-1 and state:
  "בוחר `[skill]` על סמך ההתאמה הגבוהה ביותר."

### Step 5: Present Results

Print to chat:

```
## סקיל מומלץ: `[skill-name]`

**ציון:** [top_score]  |  **מרווח מהבא:** +[margin]

**למה `[skill-name]` ולא `[second-name]`:**
[1–2 משפטים — מה בכוונת המשתמש מצביע על skill-name ולא על המתחרה הקרוב]

**Top 3:**
1. `[skill-name]`   [score]  — [one-line reason]
2. `[skill-name-2]` [score]  — [one-line reason]
3. `[skill-name-3]` [score]  — [one-line reason]

**להפעיל:** `/[skill-name]` — או אמור "כן" כדי שאטעין אותו עכשיו.
```

### Step 6: Activate on Confirmation

If the user says "כן", "yes", "הפעל", or any skill name from the top-3:
→ Read the full SKILL.md body of the chosen skill.
→ Print: "טוען `[skill-name]`..." then immediately begin that skill's instructions with
  the user's original intent as input.

If the user names a different skill not in top-3:
→ Confirm: "לא היה ב-top 3 — האם אתה בטוח שמדובר ב-`[named skill]`?" then activate if confirmed.

If the user rejects all suggestions:
→ Print: "מה אתה מנסה להשיג? תאר את הפעולה ואנסה שוב."

## Safety Rules

1. **NEVER execute the chosen skill** without explicit user confirmation (Step 6 requires "כן" /
   "yes" / skill name).
2. **NEVER write to any file** — all output goes to chat only.
3. **NEVER load full SKILL.md bodies** before Step 6 — frontmatter only in Steps 1–5.
4. **NEVER ask more than one clarifying question** per routing session regardless of confidence.
5. **NEVER hallucinate skill names** — only names discovered in Step 1 are valid candidates.

## Examples

**User:** "אני רוצה לעשות commit לשינויים שלי"

**Agent behaviour:**
Discovers installed skills. Scores: git-commit=0.84, safe-refactor=0.22, doc-updater=0.09.
Margin=0.62 — Case A (clear winner). Prints recommended block: "למה git-commit ולא
safe-refactor: הכוונה היא לשמירת שינויים (commit), לא לשינוי קוד קיים (refactor)."
User says "כן" → loads full git-commit SKILL.md and begins execution.

**User:** "רוצה לשפר את הקוד שלי"

**Agent behaviour:**
Scores: safe-refactor=0.51, scaffold-feature=0.44. Margin=0.07 — Case B (close match).
Asks: "שתי אפשרויות קרובות: האם הכוונה **safe-refactor** (שיפור קוד קיים תוך שמירה על
בדיקות) או **scaffold-feature** (יצירת feature חדש מאפס)?" User: "refactor" →
promotes safe-refactor to rank 1, displays top-3, activates on confirmation.

**User:** "משהו עם documentation"

**Agent behaviour:**
Scores: doc-updater=0.38, doc-standard=0.35, doc-research-planner=0.22. top_score=0.38 <
0.5 — Case C. Asks: "הכוונה לתיעוד **קיים** (עדכון drift, תיקון סגנון) או לתכנון
תיעוד **חדש** (מחקר, ADR, תכנון)?" After "קיים" → re-scores in docs domain →
doc-updater=0.71, clear winner, proceeds to activation.

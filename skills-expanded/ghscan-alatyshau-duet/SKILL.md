---
name: briefing
description: Deep one-by-one walkthrough of issues, decisions, or open questions. Builds index, then each issue gets full analytical depth sequentially.
---
# Skill: Briefing

## Purpose

Briefing's function: make an unresolved issue **understandable enough that the user can decide.** Nothing else in this skill matters if this fails — not analytical depth, not honesty about trade-offs, not elegant writing. A briefing the user doesn't fully understand produces a rubber-stamp, not a decision.

«Understandable» is specific. Imagine the reader as a CEO back from a month's vacation: no conversation context, no memory of prior discussions, no intent to open any document you reference. Your message IS the briefing — everything needed to decide lives inside it.

From your text alone, on one pass, without opening anything else, the reader must be able to state:

1. **What's the problem?**
2. **What's the proposed solution?**
3. **Why does the solution solve the problem?**
4. **Why is this solution better than the alternatives considered?**
5. **What makes this solution excellent — not just best-of-what-you-considered?**

Each question tests a distinct failure mode:

- Q1 — problem unstated → reader can't see what's being asked.
- Q2 — solution shape unstated (only actions listed) → reader has no mental picture of the result.
- Q3 — solution-to-problem link implicit → reader can't tell if mechanics actually address cause.
- Q4 — alternatives not named or not ruled out → reader can accept/reject the proposal but can't judge against other shapes.
- Q5 — excellence bar not applied → proposal may be best-of-weak-options, a band-aid that happens to beat two worse band-aids. If the answer to Q5 is just «it works» or «it's simpler» — the analyst settled.

All five answerable from the text = briefing works. Any one unanswerable = briefing broken, regardless of what's underneath.

Three process rules enforce this function:

- **One issue at a time.** N issues batched into one response give each ~1/N of thinking — no coherent analysis to be understood.
- **Explicit user approval per issue.** «Да» is the user's claim of understanding, not politeness. Agent cannot close what only the user can claim to have understood.
- **Fixation in a file per issue.** An understood decision kept only in chat is lost at compaction; next session reopens from scratch and the understanding is wasted.

Every rule below is in service of understandability. When applying the skill, the primary self-check is always: *can the reader, cold, answer all five questions from the text alone?* If no — stop and fix, whatever else is «right» about the work.

## Algorithm

### Phase 1: Build index + choose fixation strategy

The index is a dumb map — titles and pointers, not analysis. Deep thinking happens later, one issue at a time.

1. Scan source (file, conversation, agent reports) for issues needing resolution
2. Filter out already-resolved items (check by title only, don't deep-scan yet)
3. For each remaining issue: extract title + where to find context
4. **Choose fixation strategy** (see below). Assess whether issues are independent or interconnected. Write the strategy in the briefing file header.
5. Write `briefing_<case_name>.md` in the project folder
6. Link it from `plan.md` (so the next session knows there's an active briefing)
7. Show the index + chosen strategy. Agent owns the list and order. User approves the strategy — it's the only decision at this phase.

**Example output at this step:**

```
5 вопросов:

| # | Вопрос | Контекст |
|---|--------|----------|
| 1 | Glossary в system prompt — нужен или дублирует? | core_instructions.md:39-64 |
| 2 | "Be cautious about deletions" — паника без WHY | core_instructions.md:101 |
| 3 | Observable rules table — агент её использует? | core_instructions.md:123-138 |
| 4 | Spec gate — когда читать спеку? | review.md item 3 |
| 5 | Plan.md растёт — нужен ли лимит? | review.md item 6 |

Стратегия фиксации: **artifact → design_review.md** (вопросы связаны —
решения формируют документ для следующей сессии).
```

### Fixation strategy

Decisions made during briefing must survive compaction — if knowledge stays only in chat, it's lost. The strategy determines **where** decisions are materialized.

Choose one at index time. User approves the strategy. Record in briefing file header as `fixation: <strategy>`. The `target` field in header is mandatory for all strategies except `chat` — it names the file(s) where decisions ultimately land.

| Strategy | Where | When to use |
|----------|-------|-------------|
| `log` | In the briefing file itself — full decision + reasoning per issue | Issues are interconnected within one document/design. Fixing the target doc after each issue risks rework when a later issue changes context. All decisions first → one coherent pass on the target at the end |
| `artifact` | In a design doc or review document | Forming an intermediate artifact for another agent (or yourself in a new session) to execute. Typically: design doc for implementation, or review document for fixes |
| `final` | In code and specs directly | Issues are independent. Each can be fully closed on the spot without affecting others |
| `chat` | Nowhere — decisions stay in chat, index gets a status label only | **Anti-pattern by default.** Acceptable only for very small briefings (2-3 trivial issues) that fit in one short session with no compaction risk. If in doubt — use `log` instead |

**Why not always `final` or `artifact`?** When issues are interconnected, fixing the target after issue 2 may need to be redone after issue 5 changes the context. `log` collects all decisions first, then applies them in one pass.

**Why not always `log`?** When issues are independent, deferring creates unnecessary indirection. Fix it, close it, move on.

**Safety net:** `!упакуй` (checkpoint) walks every chat message and verifies that all decisions made it into files. If something slipped through during fixation — checkpoint catches it.

#### Briefing file header

```markdown
# Briefing: <case name>
source: <file(s) where issues come from>
target: <file(s) where decisions land — code, spec, design doc>
fixation: <strategy>

## Issues

### 1. Some issue title
- context: <pointers>
- status: **resolved** — <one-line summary>

### 2. Another issue
- context: <pointers>
- status: pending

## Solutions

### 1. Some issue title
**Decision:** <what we decided>
**User approved:** "<exact quote>"

<reasoning — free form, as long as needed. May use #### and #####
subsections to structure complex analysis. May include alternatives
considered, arguments for and against, nuances from discussion.
One paragraph or several pages — whatever captures the depth of the
conversation so a new session doesn't repeat the work.>
```

For `final` and `artifact` — the briefing file has only the Issues section (no Solutions). Decisions go directly into `target`.

### Phase 2: Walk through

Other sessions may have already fixed some issues. Re-scanning files on every step catches this — stale analysis is worse than no analysis.

For each issue:

1. **Re-scan** source through the lens of this issue. Two outputs:
   - Verify current state of files/code — may already be fixed by another session.
   - Pull explanatory material — excerpts, term definitions, relevant context — inline into your Problem block. The reader is cold; surfacing the context is your job, not theirs.

2. **Resolved?** — mark in index, move on.

3. **Alive?** — do the thinking, then present.

   **Analysis sequence** (apply before you write, in this order):
   `[bigpic]` → `[verify]` → `[think]` → `[propose]` → `[honest]`

   **Frame check — before Problem.** `[bigpic]` in a briefing is a concrete operation, not a nod. Before formulating «what's wrong», ask: *is this problem the right unit, or a symptom of something bigger?* The frame of the issue usually comes from the source document — and the source document wasn't written to question itself. Three outcomes:

   - **Problem dissolves under a wider frame** → reframe the briefing, don't patch. Example: issue titled «CORS * is unsafe in split mode» may actually be «split mode has no security boundary». Patching CORS answers the first, misses the second.
   - **Problem holds, but siblings emerge** (same root cause elsewhere in the system, or neighbouring decisions resting on the same faulty premise) → name the siblings inline in Problem; flag them for the index so they get their own briefings.
   - **Frame holds** → proceed to Problem block.

   A briefing that fixes a symptom leaves the root cause to generate more symptoms. The cheapest time to catch a misframed problem is before you've written about it.

   **Presentation structure.** Three mandatory blocks — each answers a specific question the reader has.

   - **Problem.** What is wrong. Include enough of the system context that the problem lands — processes, configs, components, whatever the reader needs. Define every term a cold reader would stumble on, on first use («In split mode» is not enough; «In split mode (two processes — HTTP and Workers — on separate ports) ...» is). No references to other documents expecting the reader to open them («см. `<doc>.md`», «как в §3.1») — pull the relevant excerpt inline. **End with the explicit question:** what needs to be decided, in one sentence. The Problem block isn't done until a reader can state in one sentence what you're asking them.

   - **Solution.** The shape of what you propose, not a list of actions. Describe the end state: «after this, the system looks like X». Make the link to Problem explicit: «this removes P because Q». Concrete actions (file edits, code diffs, renames) come after the shape, as a supporting list — they execute the solution, they don't substitute for it. A reader who sees only actions has no mental picture of the result and cannot judge whether it solves the problem.

   - **Why.** The reasoning behind choosing *this* solution — on two axes. **Comparative:** what alternatives you considered and why they lose (Q4). **Absolute:** what makes the chosen shape excellent — the positive property that sets it apart from a band-aid or best-of-weak-options (Q5). A Why block that only lists rejected alternatives passes Q4 but leaves Q5 unanswered; «beats everything I thought of» is not the same as «is the right shape». Depth lives here, not in Problem (that's framing) or Solution (that's the proposition).

   **Genuine fork — when analyst cannot resolve.** Replace **Solution** + **Why** with:
   - **Fork.** Two or more options with what happens in each case.
   - **Depends on.** Which priority of the user's settles the choice.

   Use only when you've done all the thinking an analyst can do and the remaining choice genuinely belongs to the human. Arriving at an answer is harder than listing options — default is to arrive.

   Fork swaps the Cold Reader Test: Q4/Q5 don't apply (no single solution to compare or assess), and Q1-Q3 adapt:
   - **Q1.** What's the problem?
   - **Q2-fork.** What are the options?
   - **Q3-fork.** What decides between them?

   If the reader can't state all three from your text, the fork is broken the same way a Solution briefing is broken when Q1-Q5 fail.

   **Cold Reader Test — mandatory before sending.** Reread what you've written as if you've never opened this codebase. From your text alone, answer:

   1. What's the problem? (one sentence)
   2. What's the proposed solution? (one sentence)
   3. Why does the solution solve the problem? (one sentence)
   4. Why is this solution better than the alternatives? (one sentence per alternative ruled out)
   5. What makes this solution excellent — not just adequate? (one sentence naming the positive property: architectural correctness, right-shape-not-band-aid, testability, extensibility, etc.)

   If any answer doesn't come from the text — block. Fix before sending, not after pushback.

   - Term that made you pause → missing inline definition.
   - «See X» / «как в Y» → missing inline excerpt.
   - Couldn't find solution shape, only actions → Solution block is describing actions, not result.
   - Couldn't connect solution to problem → link is implicit; make it explicit in Solution.
   - Couldn't name which alternatives were ruled out and why → Why block missing or thin; reader can accept/reject but can't judge against other shapes.
   - Couldn't name what makes the solution excellent beyond «it works» → Why block hasn't applied `[excellence]`; proposal may be best-of-weak-options. Find the positive property that makes this the right shape, or go back to first principles and look for a better shape.

   A briefing that fails this test delivers analytical depth the reader can't evaluate — which from the reader's seat is indistinguishable from no analysis at all.

4. **Wait** for decision. FULL STOP. Do not edit files, update index, or print ZERO LOOSE ENDS until the user explicitly approves or rejects. «Согласен?» from you is a question, not a decision. Only the user's reply is a decision.

5. **Act** based on fixation strategy:
   - **`final`** — fix immediately in target (code, spec, design doc). Context is hot — deferring means losing it.
   - **`log`** — write full decision + reasoning in the Decisions section of the briefing file. Target document is updated in one pass after all issues are resolved.
   - **`artifact`** — write into the intermediate document (design doc or review doc).

6. **Update index** — mark status, write one-line summary of decision.

7. **Zero loose ends gate** — before moving to next issue, print this checklist in chat:

   ```
   ✅ ZERO LOOSE ENDS:
   - User approved: "<exact user quote>"
   - Fixated: <where — briefing log / design doc / code+spec>
   - Index updated: <yes/no>
   - Decision recorded: <one-line summary>
   ```

   The «User approved» field is mandatory. You must quote the user's actual words that constitute approval. If you cannot fill this field — you skipped step 4. Stop, revert any changes, and go back to waiting.

   Do NOT present the next issue until this gate is printed and complete.

8. **Ask permission to move on.** After printing ZERO LOOSE ENDS — ask «Идём дальше?» and wait. This is `[review]` applied to briefing: agent cannot see the full picture and cannot mark an issue as closed — only the user can. Move to the next issue ONLY on explicit «да» or «дальше» (or user said «дальше» earlier, before the gate). Everything else means stay:
   - «Да» in response to «Согласен?» = approval of recommendation, NOT permission to move on.
   - User asks a question or makes a statement ignoring «Идём дальше?» = they're ignoring the question = we're not moving on.
   - User provides additional context, examples, corrections = still on current issue.

A single issue may take one message or fifty — don't move on until resolved or deferred.

**Example — clear answer:**

```
## [1/3] Glossary in system prompt — needed or redundant?

**Problem.** `core_instructions.md` (системный промпт, всегда в контексте
агента) содержит 25-строчный блок «Glossary»: дерево иерархии сущностей
и таблицу синонимов EN/RU. Параллельно агент получает `context.chain` из
`workspace_info` — breadcrumb вида «МетаЛаб / ТехноЛаб / Duet» с типом на
каждом уровне. Вопрос: даёт ли Glossary что-то сверх того, что уже приходит
в `context.chain`, или дублирует?

**Solution.** Оставить в `core_instructions.md` только таблицу синонимов
EN/RU, дерево иерархии удалить. После правки блок занимает 10 строк
вместо 25 и содержит только то, чего нет в `context.chain` — русские
синонимы для англоязычных терминов. Дублирование снимается, уникальное
знание остаётся.

Действия:
- Удалить строки 39-53 (дерево иерархии) из core_instructions.md.
- Оставить таблицу EN/RU (строки 55-64).

**Why.** *Альтернативы и почему они проигрывают (Q4).* Рассматривались
два варианта: (1) убрать весь Glossary — ломает работу с русскими
синонимами, агент перестаёт понимать «открой бизнес МетаЛаб»; (2) оставить
как есть — держит 15 строк дублирования с `context.chain` в промпте,
который всегда в контексте каждой сессии.

*Почему выбранная форма правильная, а не просто лучшая из трёх (Q5).*
`core_instructions.md` — дефицитный ресурс: он грузится в каждой сессии
и конкурирует за внимание агента на каждом запуске. Архитектурный
инвариант для always-loaded промпта: держим в нём **только то, чего нет
в `workspace_info`**. Решение приводит файл к этому инварианту — дерево
удаляется как дубликат `context.chain`, таблица остаётся как уникальное
знание. Альтернатива (2) оставляла бы инвариант нарушенным; альтернатива
(1) нарушала бы его в другую сторону (теряла бы уникальное). Выбранное
решение — единственное, которое соблюдает инвариант.
```

**Example — genuine fork (analyst can't resolve alone):**

```
## [2/3] Spec files — markdown or structured YAML?

**Problem.** Спецификации компонентов (архитектура, инварианты данных)
сейчас лежат в markdown-файлах. Появился запрос на машинное чтение спеков —
валидация (проверять, что код соответствует спеке) и генерация (создавать
из спеки скелеты). Markdown парсить ненадёжно — слишком свободная структура.
YAML парсить надёжно — машинно-читаемая схема, но человеку читать YAML
заметно тяжелее, чем markdown. Вопрос: на каком формате писать спеки
дальше?

**Fork.**

Если читаемость для человека важнее машинной обработки → оставить markdown.
Валидацию делать через LLM-парсинг (дороже, медленнее, но читаемость
сохраняется для 3 агентов и человека, которые читают спеки сейчас).

Если машинная обработка важнее → перейти на YAML. Допустимо добавить
markdown-комментарии внутри YAML для контекста, но основной формат —
структурированный.

**Depends on.** Кто основной потребитель спеков в ближайший год. Сейчас
читают 3 агента и человек напрямую. Если доля машинного потребления
растёт — YAML. Если основной потребитель остаётся человек — markdown.
Этот приоритет я не могу установить за тебя.
```

## Anti-patterns

| Don't | Why | Do instead |
|-------|-----|------------|
| Analyze during index phase | Wastes tokens on shallow pass you'll redo anyway | Index = titles + pointers only |
| Batch multiple issues in one response | Output tokens compete → shallow treatment | One issue, full depth |
| Skip re-scan before analysis | May already be fixed by another session | Check current file state first |
| Take the source's framing as given and go straight to Problem | Source document wasn't written to question itself — inherit its frame, inherit its blind spots. You fix a symptom and leave the root cause | Run the Frame check before Problem: is this the right unit, or a symptom of something bigger? |
| Describe how the system works instead of stating the problem | Reader sees «here's the setup» and asks «...and?» — the question is missing | End Problem block with the explicit decision to be made, in one sentence |
| List actions («переписать X, удалить Y») instead of describing solution shape | Reader gets a punch list but no mental picture of the result — can't evaluate whether it solves the problem | Describe end state first («after this, the system looks like X»), then list actions that produce it |
| Reasoning that doesn't connect problem to solution | Analysis floats unconnected — reader sees depth but can't tell what it's for | Every paragraph in Why earns its place by connecting to Solution or ruling out an alternative |
| Settle for best-of-considered without applying the excellence bar | «Beats the alternatives I thought of» may just be best-of-weak. The analyst defends the choice against a set they picked, not against first principles | After ruling out alternatives, name the positive property that makes the chosen shape right — architectural invariant, scarce-resource alignment, boundary placement. If nothing positive surfaces, the set you considered was too narrow — widen it |
| Reference a doc path expecting the reader to open it («см. `<doc>.md`», «как в §3.1») | Turns briefing into homework; reader can't judge proposal without context the reference hides | Pull the relevant excerpt inline; if long, summarise in one clause |
| Use project jargon without inline definition on first use (e.g. «split mode», an internal acronym, a codename) | Reader is cold — a term from the source document isn't automatically one they share | Define on first use in one clause; use freely afterwards |
| Skip the Cold Reader Test before sending | You ship a briefing that fails its own purpose; reader pushes back, round wasted | Reread as cold reader, verify all five questions are answerable from the text alone |
| Default to fork when arriving at an answer is hard | Listing options is easier than deciding — that's avoidance, not depth | Fork only when the answer genuinely depends on a user priority you can't know |
| Mark «resolved» without materializing | A status label is not fixation — «resolved» in index + nothing in files = lost knowledge | Fixate per chosen strategy, then mark |

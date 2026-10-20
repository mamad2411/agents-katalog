# Rule of plan execution

## Record all actions to `.tasklog/<taskid>.md`

- **After switching to ACT mode, append the plan to the `.tasklog/<taskid>.md`.**
- Always append data to the `.tasklog/<taskid>.md` file. The file may be modified by other tools, so it **needs to be re-read** each time new data is added.
- Until the work plan is finally approved and switched to ACT mode, only reading of the data for analysis and plan development is permitted; editing or changing the data is prohibited.
- Always append the results **of each step of the plan tasks** in the `.tasklog/<taskid>.md` file, including any negative results.
- After **several unsuccessful** attempts to solve a problem, **stop and analyze the problems**.
- If the problem persists and requires a change in the architecture or the solution is outside the scope of the approved plan, **stop task execution** and provide a report on the problem encountered with several proposed solutions to choose from.

## Structure your prompt for efficient LLM context caching.

- Place static content (`AGENTS.md`, `README.md`, etc.) first - they form a cacheable prefix.
- Place dynamic content (`.tasklog/<taskid>.md`, current file, command results) after static content.
- When updating `.tasklog/<taskid>.md`, send it at the start of a new turn, not mid-conversation.
- In long sessions, periodically re-send static blocks (`AGENTS.md`, `README.md`, etc.) to prevent cache eviction.

## Before plan complete and stop task execution

- Re-Read `.tasklog/<taskid>.md` and review the original plan for completeness and append any items not completed and the reasons why they were not completed.
- Systematize the errors that occurred during the tasks plan and suggest improvements to prevent them in the future.
- **Append all results** of the plan execution in the `.tasklog/<taskid>.md` file with a brief description of the results.

---

## Read structures before refactoring

**Do not refactor code without reading the full definition of every type involved.**

- Before modifying or replacing a type - read the complete header file and understand **all** fields, their semantics, and relationships.
- Do not assume which fields are "unnecessary". If you don't understand a field - ask.
- Pay special attention to types with semantics - they may carry ownership or lifetime constraints.
- When a task says "remove dependency on X" - first check what data from X is actually used in downstream code.

## Verify before completion

**Do not call `attempt_completion` until all verifications pass.**

After ANY change that removes types/fields/tokens, run:
1. `grep -rn` for the removed/changed name across the entire project - fix all remaining references. 
2. Do NOT skip test files - tests must also use the new code.
3. Call `cmake --build _build` - project must compile without errors.
4. Call `make run_tests` for all tests - must pass.
   - All test runs **MUST** use a timeout (e.g., `timeout 60 make run_tests`) to catch infinite loops or hangs.
5. If the change adds/moves a `.cpp`/`.hpp` or changes `#include` directives - additionally build and
   run the tests with the shared PCH **off** (`-DTRUST_USE_PCH=OFF`): the PCH is a dev-only optimization
   and must never mask a missing `#include`. Release builds must use `TRUST_USE_PCH=OFF` anyway
   (`ON` is a configuration error), so this configuration is the source of truth.

If build or tests fail - do NOT declare completion. Fix the underlying issue.

## Scope boundaries

**Do not expand the task without explicit agreement.**

- If architectural plan discussion exceeds 5-8 iterations - split into subtasks and agree separately.
- Do not mix adding functionality with API refactoring in a single task.
- Do not rework caller APIs if the task does not require it.
- If a simple task ("add an attribute") grows into an API redesign ("change substituteArgs to class") - stop and request a separate task.


## Component knowledge check

**Перед планированием задачи, затрагивающей компонент (ast, parser, diag, types, runtime и др.) - обязательно выполнить:**

1. Прочитать **`MEMORY.md` компонента** (корневой `MEMORY.md` и `include/<компонент>/MEMORY.md`) и учесть разделы «Architecture», «Facts and invariants», «Decisions», «Relations».
2. Если информация касается затрагиваемой области - учесть её в плане до передачи пользователю.

**Что сохраняется в `MEMORY.md` (критерии включения):**
- Только **семантические инварианты-ловушки**, которые:
  - вызвали **≥3 циклов доработок** (reopened задачи);
  - **не выводятся однозначно** из чтения исходного кода или описания MEMORY.md;
  - не являются описанием полей структур (состав полей - читать исходный код).
- Сохранять в `MEMORY.md` следует **только очень кратко** самые важные семантические инварианты-ловушки, которые сложно вывести из API/MEMORY.md/исходного кода.

**Что ЗАПРЕЩЕНО сохранять в `MEMORY.md`:**
- **запрещено сохранять любую информацию о багах или задачах** (в т.ч. статус/итоги выполнения, найденные проблемы, планы, «отдельные задачи», списки оставшихся работ) - всё это должно быть в `.tasklog`;
- информация о новой функциональности, которая уже выбрана пользователем и/или зафиксирована в коде или архитектуре;
- объяснения архитектуры пользователем на стадии планирования (они уже в `.tasklog`);
- состав и описание полей данных - для этого есть исходный код.

**Порядок пополнения `MEMORY.md`:**

- При каждом случае "ложного завершения" (≥3 TaskComplete) - если причина не покрыта существующими наблюдениями и не выводится из исходного кода - добавить наблюдение в `MEMORY.md` соответствующего компонента и обновить `last_reviewed` при ревизии.
- Если в ходе обычной задачи найден новый семантический инвариант-ловушка, отсутствующий в `MEMORY.md`, - дописать его в раздел «Facts and invariants» соответствующего компонента и обновить `last_reviewed`.
- Если `last_reviewed` в `MEMORY.md` затрагиваемого компонента старше `review_period` - предложить провести ревизию (сверить содержимое с кодом, обновить `last_reviewed`) как отдельный пункт плана.

---

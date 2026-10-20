# Solitaire — Claude Code Instructions

## Project
Unity 2D Solitaire prototype. Test assignment: "Undo Move" system using Command Pattern.
Senior Unity Tech Lead position. Architecture quality is the primary evaluation criterion.

## Navigation — read in this order
1. `AIDocs/PROGRESS.md` — current state, what's done, what's next ← **start here every session**
2. `AIDocs/PHASES.md` — phase index with status and links
3. `AIDocs/phases/phase-N.md` — current phase detail
4. `AIDocs/docs/` — system documentation (Obsidian knowledge base)

## Architecture

**Patterns:** Entry Point · Service Locator · LazySrv · EventBus · Command Pattern · IGameContext

**File structure:**
```
Assets/Scripts/
├── Core/           IService, ICommand, ServiceLocator, LazySrv, MoveHistoryService, CardSpriteRegistry, Constants
│   └── EventBus/   IEvent, EventBinding, EventBus<T>, EventBusUtil, PredefinedAssemblyUtil
├── Events/         InputReadyEvent, GameContextInitializedEvent
├── Context/        IGameContext, IInputContext, GameContext
├── Models/         Suit, CardColor, StackType, Card, CardStack, GameState
├── Rules/          IMoveValidator, TableauMoveValidator, FoundationMoveValidator
├── Commands/       MoveCommand, DrawCommand, RecycleWasteCommand
├── Services/       EntryPoint, CameraService, GameService, UIService
├── Controllers/    DragState, InputController, BoardRaycaster, CardDragController
└── Views/          CardView, StackView, HudPresenter
```

**Key rules:**
- `EntryPoint` — единственная точка входа, управляет lifecycle всех сервисов
- Сервисы инициализируются только в `Initialize()`, не в `Awake`/`OnEnable`
- UI работает только через `IGameContext` — никаких прямых ссылок на `GameService`
- Коммуникация между сервисами: `EventBus<T>` или `LazySrv<T>` через `ServiceLocator`
- Подписка на EventBus через `EventBinding<T>`, не через `Action` напрямую

## Phase Workflow (CRITICAL — follow exactly)

1. Прочитать `AIDocs/PROGRESS.md` — понять где остановились
2. Прочитать `AIDocs/phases/phase-N.md` — задачи фазы
3. Выполнить задачи
4. Создать/обновить системный документ в `AIDocs/docs/` по шаблону `AIDocs/docs/_template.md`
5. Запустить Gemini CLI ревью, показать результат пользователю
6. **Ждать команды пользователя** — не переходить к следующей фазе самостоятельно
7. После одобрения: обновить `AIDocs/PROGRESS.md` и статус в `AIDocs/PHASES.md`

## Documentation Rules

После каждой фазы создаётся **системная документация** в `AIDocs/docs/` — не отчёт о выполнении,
а техническое описание системы: что это, как работает, почему именно так.

Формат — Obsidian knowledge base (см. шаблон `AIDocs/docs/_template.md`):
- Frontmatter: `tags`, `related`, `doc_standard`
- TL;DR в одно предложение
- Таблица компонентов
- How it works (bullet points, только WHY)
- Key decisions
- See also с [[wiki-links]]

## Code Rules

**All comments in English only.**

**Naming:**
- Classes/Methods/Properties: PascalCase
- Private fields: `_camelCase`
- Local vars: camelCase
- Constants: `UPPER_SNAKE_CASE`
- Interfaces: `IPascalCase`

**Formatting:** Allman braces · 4 spaces · Explicit access modifiers · One class per file

**Unity:**
- `[SerializeField] private` — never public fields
- Cache `GetComponent` in `Awake`, never in `Update`
- No `GameObject.Find`, `FindObjectOfType`, `Transform.Find`
- `TextMeshPro` only — never `UnityEngine.UI.Text`
- Unsubscribe events in `Dispose()` / `OnDestroy()`
- Kill DOTween tweens in `Dispose()` / `OnDisable()`
- No magic numbers/strings — `Constants.cs`
- No `AddComponent` at runtime — configure prefabs in Editor

**Colliders:** `IsTrigger = true` на картах и стеках — Physics2D.Raycast попадает в триггеры.

## Unity Skills — when to use

| Task | Skill |
|---|---|
| Inspect scene before editing | `unity-scene-inspector` |
| Create/move GameObjects | `unity-scene-composer` |
| Read component values | `unity-component-readback` |
| Add/configure component | `unity-component-editor` |
| Inspect prefab | `unity-prefab-inspector` |
| Create/modify prefab | `unity-prefab-builder` |
| Console errors | `unity-console-error-triage` |

Always inspector/readback before composer/editor/builder.

## Git
- Conventional commits: `feat:`, `fix:`, `refactor:`, `docs:`
- No `.meta` files in `.gitignore` — Unity needs them
- Never commit without explicit user request

# Solitaire — AI Agent Instructions

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
- `EntryPoint` — single entry point, controls full service lifecycle
- Services initialize only in `Initialize()`, never in `Awake`/`OnEnable`
- UI works only through `IGameContext` — no direct references to `GameService`
- Cross-service communication: `EventBus<T>` or `LazySrv<T>` via `ServiceLocator`
- EventBus subscription via `EventBinding<T>` object, not raw `Action`

## Phase Workflow (CRITICAL — follow exactly)

1. Read `AIDocs/PROGRESS.md` — understand current state
2. Read `AIDocs/phases/phase-N.md` — phase tasks
3. Execute tasks
4. Create/update system document in `AIDocs/docs/` using template `AIDocs/docs/_template.md`
5. Run Gemini CLI review, show result to user
6. **Wait for user command** — do NOT proceed to next phase autonomously
7. After approval: update `AIDocs/PROGRESS.md` and status in `AIDocs/PHASES.md`

## Documentation Rules

After each phase — create **system documentation** in `AIDocs/docs/`.
NOT a completion report. A technical description: what the system is, how it works, why.

Format — Obsidian knowledge base (see template `AIDocs/docs/_template.md`):
- Frontmatter: `tags`, `related`, `doc_standard`
- TL;DR in one sentence
- Components table
- How it works (bullet points, WHY only — not WHAT)
- Key decisions
- See also with [[wiki-links]]

After writing — do NOT proceed, do NOT fix review findings autonomously.
Show Gemini result to user and wait for explicit command.

## Code Rules

**All code comments in English only.**

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
- Unsubscribe all events in `Dispose()` / `OnDestroy()`
- Kill DOTween tweens in `Dispose()` / `OnDisable()`
- No magic numbers/strings — use `Constants.cs`
- No `AddComponent` at runtime — configure prefabs in Editor
- Colliders: `IsTrigger = true` on cards and stacks

## Unity Skills — when to use

| Task | Skill |
|---|---|
| Inspect scene | `unity-scene-inspector` (read-only, always first) |
| Create/move GameObjects | `unity-scene-composer` |
| Read component values | `unity-component-readback` (read-only, always first) |
| Add/configure component | `unity-component-editor` |
| Inspect prefab | `unity-prefab-inspector` (read-only, always first) |
| Create/modify prefab | `unity-prefab-builder` |
| Console errors | `unity-console-error-triage` |

## Git
- Conventional commits: `feat:`, `fix:`, `refactor:`, `docs:`
- Do not commit without explicit user request
- No `.meta` files in `.gitignore`

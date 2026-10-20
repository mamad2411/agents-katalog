# Expert C# & Unity Development Rules — Solitaire Project

You are an expert in C#, Unity 2D, and game development.
Prioritize readability, performance, and modularity.

## Core Principles

- Write clear, technical C# and Unity responses with precise examples.
- Follow **Command Pattern** for undo system (`ICommand`: `Execute()`/`Undo()`).
- Use Unity's built-in features: ScriptableObjects, Prefabs, EventSystem, DOTween.
- Prioritize performance and memory management.
- Apply MVC separation: Model (plain C#) / Controller (logic) / View (visual only).

## Project Documentation

- Architecture decisions: `AIDocs/architecture.md`
- Code style rules:     `AIDocs/code_style.md`
- Available skills:     `AIDocs/skills/`

## C# & Unity Technical Standards

- Cache references in `Awake`. Use `TryGetComponent<T>(out var comp)`.
- **Forbidden:** `GameObject.Find`, `Transform.Find`, `FindObjectOfType`, `UnityEngine.UI.Text`.
- No allocations in `Update`/`FixedUpdate`. No LINQ/`foreach` in hot paths.
- Always unsubscribe events in `OnDisable`/`OnDestroy`.
- Use `TextMeshPro`. Explicit access modifiers. Allman braces. 4 spaces indent.
- `[SerializeField] private` over public fields. Default values inline.
- No magic strings/numbers → `Constants.cs`.
- DOTween: store `Tween` in field, kill before reassign, kill in `Dispose`.
- `TryGetComponent` instead of `GetComponent` + null check.

## Naming Conventions

- Classes/Methods: PascalCase
- Private fields: `_camelCase`
- Local variables: camelCase
- Constants: `UPPER_SNAKE_CASE`
- Interfaces: `I` prefix (`ICommand`, `ICardContainer`)
- Async methods: `Async` suffix

## Architecture (Solitaire-specific)

- Every card move = `ICommand` with `Execute()`/`Undo()`
- `UndoManager` holds `Stack<ICommand>`
- Model without MonoBehaviour: `Card` (struct), `CardStack`, `UndoManager`
- View without logic: `CardView`, `StackView` — only visual + event forwarding
- Drag-and-drop via `IBeginDragHandler`, `IDragHandler`, `IEndDragHandler`
- View subscribes to Model events — never polls in `Update`

## Error Handling

- Use `Debug.Assert` for logical assertions during development.
- `try-catch` only for I/O and external API calls.

## File Encoding

- **UTF-8 with BOM** for all text files (.cs, .json, .md, scripts).

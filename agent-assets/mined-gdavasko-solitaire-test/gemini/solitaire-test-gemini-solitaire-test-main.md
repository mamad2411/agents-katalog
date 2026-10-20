# Gemini CLI Rules — Solitaire Project

## 1. Core Principles

**Persona:** Senior Unity Architect. Prioritize readability, performance, and modularity.

**Project:** Unity 2D Solitaire prototype. Test assignment: "Undo Move" system.
Architecture: Command Pattern for undo, MVC-like separation.

**Documentation:**
- Architecture: `AIDocs/architecture.md`
- Code Style:   `AIDocs/code_style.md`
- Skills:       `AIDocs/skills/`

## 2. Architecture Rules

- **Command Pattern** — every move = `ICommand` with `Execute()` / `Undo()`
- **Stack-based Undo** — `UndoManager` holds `Stack<ICommand>`
- **MVC separation** — Model (no MonoBehaviour) / Controller / View
- **Events over polling** — View subscribes to Model events, no `Update` polling
- **Interface isolation** — components interact via interfaces, not concrete references
- **Full Dispose** — kill tweens, unsubscribe events, clear references

## 3. Unity & C# Technical Standards

- Cache references in `Awake`. Use `TryGetComponent<T>(out var comp)`.
- **Forbidden:** `GameObject.Find`, `Transform.Find`, `FindObjectOfType`, `UnityEngine.UI.Text`.
- No allocations in `Update`/`FixedUpdate`. No LINQ/`foreach` in hot paths.
- Always unsubscribe events in `OnDisable`/`OnDestroy`.
- Use `TextMeshPro`. Explicit access modifiers. Allman braces. 4 spaces.
- `[SerializeField] private` over public fields.
- No magic strings → `Constants.cs`.
- DOTween: store in field, kill before reassign, kill in `Dispose`.

**Naming:**
- Classes: PascalCase | Private fields: `_camelCase` | Constants: `UPPER_SNAKE_CASE`
- Async methods: `Async` suffix | Interfaces: `I` prefix

## 4. File Operations & Encoding

- **UTF-8 with BOM** for all text files: `.cs`, `.json`, `.md`, scripts.
- PowerShell write with BOM:
  ```powershell
  [System.IO.File]::WriteAllText($path, $content, (New-Object System.Text.UTF8Encoding($true)))
  ```

## 5. Skills

Available skills in `AIDocs/skills/` and `.gemini/skills/`:
- `unity-scene-inspector` — inspect scene before edits (read-only)
- `unity-scene-composer` — mutate scene after inspection
- `unity-component-readback` — read component fields (read-only)
- `unity-component-editor` — edit components after readback
- `unity-console-error-triage` — classify Unity errors
- `unity-playmode-validation` — validate changes before reporting complete

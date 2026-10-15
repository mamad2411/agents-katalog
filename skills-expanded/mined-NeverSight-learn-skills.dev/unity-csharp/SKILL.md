---
name: unity-csharp
description: >
  Unity C# scripting best practices and patterns. Use this skill when the user
  asks to write, review, or debug Unity scripts. Triggers on keywords like
  "MonoBehaviour", "coroutine", "Update", "Awake", "Start", "Instantiate",
  "ScriptableObject", "Unity script", "game object", "component", "prefab".
  Do NOT use for non-Unity C# (e.g. ASP.NET, console apps).
---

This skill provides best practices for writing clean, performant Unity C# scripts.

## When to load references

- MonoBehaviour lifecycle questions → read `references/monobehaviour.md`
- Coroutine or async questions → read `references/coroutines.md`
- Events, delegates, or callbacks → read `references/events.md`
- ScriptableObject questions → read `references/scriptableobjects.md`
- Performance or optimization → read `references/performance.md`
- Input, keyboard, mouse, controller, InputAction, PlayerInput → read `references/input.md`

## Core Rules

- NEVER use `new` to create MonoBehaviour — always use `Instantiate()` or `AddComponent()`
- NEVER call `GetComponent<>()` in `Update()` — cache in `Awake()` or `Start()`
- NEVER use `Find()` or `FindObjectOfType()` in hot paths — cache references
- Prefer `[SerializeField] private` over `public` for Inspector-exposed fields
- Use `CompareTag()` instead of `== tag` for tag comparison (avoids string allocation)
- Always null-check before using references obtained at runtime

## Project Structure Convention

```
Assets/
├── Scripts/
│   ├── Player/
│   ├── Enemies/
│   ├── UI/
│   ├── Managers/
│   └── ScriptableObjects/
├── Prefabs/
├── Scenes/
└── Art/
```

## Naming Conventions

- Classes: `PascalCase` (e.g. `PlayerController`)
- Private fields: `_camelCase` (e.g. `_moveSpeed`)
- Public properties: `PascalCase` (e.g. `MoveSpeed`)
- Constants: `ALL_CAPS` or `PascalCase` (e.g. `MaxHealth`)
- Coroutines: prefix with verb (e.g. `SpawnEnemies()`, `FadeOut()`)

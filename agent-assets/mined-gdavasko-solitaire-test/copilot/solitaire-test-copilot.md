# AI Assistant Instructions — Solitaire Project

Ты — ИИ-ассистент для разработки Unity 2D Solitaire прототипа.
Тестовое задание уровня **Senior Tech Lead**: система "Undo Move" с Command Pattern.

## ПРАВИЛО №1: ДОКУМЕНТАЦИЯ

Прежде чем писать код или предлагать архитектурные решения, ознакомься с документацией:

- **Архитектура:** `AIDocs/architecture.md` — Command Pattern, MVC, принципы
- **Code Style:** `AIDocs/code_style.md` — именование, форматирование, Unity-правила
- **Скиллы:** `AIDocs/skills/` — специализированные инструкции для работы с Unity Editor

## Ключевые правила (кратко)

**Архитектура:**
- Каждый ход = `ICommand` с `Execute()`/`Undo()`
- `UndoManager` хранит `Stack<ICommand>`
- Model (чистый C#, без MonoBehaviour) / Controller / View
- View подписывается на события Model — не polling в Update

**C# и Unity:**
- `[SerializeField] private` (не public поля)
- Кешировать GetComponent в Awake, не в Update
- `TryGetComponent` вместо GetComponent + null check
- Запрещено: `GameObject.Find`, `FindObjectOfType`, `UnityEngine.UI.Text`
- TextMeshPro для всего текста
- Allman braces, 4 пробела, explicit access modifiers
- `_camelCase` для private полей, PascalCase для классов/методов
- Никаких magic strings → `Constants.cs`
- События: всегда отписываться в OnDisable/OnDestroy
- DOTween: хранить в поле, убивать в Dispose

**Кодировка:** UTF-8 with BOM для всех текстовых файлов.

## Не изобретать велосипед

- DOTween уже в проекте — использовать для анимаций карт
- Unity Event System — для drag-and-drop (IBeginDragHandler и т.д.)
- TextMeshPro — уже подключён

## Структура папок

```
Assets/Scripts/
├── Models/       Card.cs, CardStack.cs, UndoManager.cs, MoveCommand.cs
├── Controllers/  GameManager.cs, DragController.cs
├── Views/        CardView.cs, StackView.cs
└── Data/         ScriptableObject конфиги
Constants.cs
```

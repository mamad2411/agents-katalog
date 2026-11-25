# AI Development Guidelines

**Проект:** Idle Tower Defense (3D)
**Стек:** TypeScript, SvelteKit, Svelte 5 Runes, Three.js, Miniplex (ECS)

---

## Критичные правила (СТРОГОЕ СОБЛЮДЕНИЕ)

### 1. Только TypeScript

- ЗАПРЕЩЕНЫ `.js` файлы
- ИСПОЛЬЗУЙ `.ts`, `.svelte.ts`, `.svelte`

### 2. Минимальные Svelte компоненты

- Только отображение UI
- Минимум кода в `onMount`
- Вся логика в `modules/*/systems/`

### 3. Минимум комментариев

- Код должен быть самодокументированным
- Комментарии допустимы для:
  - Сложных алгоритмов
  - Важных архитектурных решений
  - Контекста проекта (например, "одна башня", "единственная сущность X")

### 4. Импорты

- Все импорты в начале файла
- ЗАПРЕЩЕНЫ динамические `import()` внутри функций

### 5. Конфигурационные файлы

- ЗАПРЕЩЕНО менять любые конфиг файлы (tsconfig.json, eslint.config.js, package.json, и т.д.) без явного разрешения
- При необходимости изменить — спроси меня, указав: что именно хочешь поменять и зачем

### 6. Единые компоненты для статов

- Health, Damage, Speed — общие для всех сущностей
- НЕ создавать разные компоненты для одного и того же

### 7. Одна башня

- В игре **ОДНА** башня — циклы по башням не нужны, используй `.first`

---

## Codestyle Guide

### Функции

- Используй `function` вместо стрелочных функций:

```typescript
// ПРАВИЛЬНО
function createSystem(world: World) {
	return (dt: number) => { ... };
}

// НЕПРАВИЛЬНО
const createSystem = (world: World) => {
	return (dt: number) => { ... };
};
```

### Фабрики систем

- Все фабрики систем принимают `world` как первый аргумент:

```typescript
function createSystem(world: World<Entity>) {
	const query = world.with("component");
	return (dt: number) => { ... };
}
```

- НЕ использовать глобальный `world` внутри систем — всегда передавать через аргумент
- Canvas и другие внешние ресурсы также передавать аргументами, НЕ через `setCanvas`/модульный scope

### Enum-подобные типы

```typescript
// ПРАВИЛЬНО
export const EnemyState = {
	MOVING: "moving",
	ATTACKING: "attacking",
} as const;

export type EnemyStateType = (typeof EnemyState)[keyof typeof EnemyState];

// НЕПРАВИЛЬНО
export type EnemyState = "moving" | "attacking";
```

- Сразу после `const object` определяй тип через `typeof`
- Суффикс типа: `*Type` (например, `EnemyStateType`, `TowerStateType`)

### Именование variant-компонентов

- Если нужно определить тип/вариант сущности — используй суффикс `*Variant`: `enemyVariant`, `projectileVariant`
- НЕ используй `*Type` для типов сущностей — это создаёт `EnemyTypeType`, `ProjectileTypeType`
- `*Type` допустимо только для типов состояний: `TowerStateType`, `EnemyStateType`, `WaveStatusType`

### Именование компонентов-тегов

- Компоненты-теги (маркеры сущностей) именуются как `*Tag`: `enemyTag`, `towerTag`, `projectileTag`, `dyingTag`, `targetableTag`, `deadTag`
- НЕ использовать префикс `is`: `isEnemy`, `isTower` — запрещено
- Значение всегда `true`: `enemyTag: true`

### Импорты

- Все импорты в начале файла
- ЗАПРЕЩЕНЫ динамические `import()` внутри функций

### Типизация props в Svelte

Props всегда должны быть типизированы через `interface Props` или `type Props`:

```svelte
<script lang="ts">
	interface Props {
		label: string;
		onclick: () => void;
	}

	let { label, onclick }: Props = $props();
</script>
```

---

## Архитектура

### Структура модуля

```
modules/feature/
├── components.ts  # типы + компоненты
├── factory.ts     # фабрика сущностей
└── systems/       # системы
    ├── *.system.ts  # фабрики систем (принимают world, возвращают (dt) => void)
    └── *.ts         # вспомогательные файлы для фабрик/систем (хелперы, константы и т.д.)
```

### Модули общего назначения

```
modules/shared/
└── components/   # общие компоненты (hp-bar и т.д.)
```

### Структура папок (Screaming Architecture)

- Папки называть по тому, ЧТО делают (`enemies/`, `waves/`, `towers/`), а не по слою (`systems/`, `components/`)
- Внутри модуля могут быть любые папки с понятными названиями (`handlers/`, `ui/`, `physics/`)
- НЕ создавать: `components/`, `utils/`, `helpers/` (неинформативные названия)

### Анти-Overengineering

- НЕ использовать: классы-фабрики, Repository, Strategy паттерны
- НЕ использовать: интерфейсы с префиксом `I`
- ИСПОЛЬЗОВАТЬ: простые `type`, функции, плоские объекты данных

### Типизация Miniplex

Компоненты как объекты в едином типе Entity.

### Хранение констант

Все magic numbers должны быть вынесены в константы:

- `src/lib/core/constants.ts` — простые значения (FPS, тайминги, размеры)
- `src/lib/core/game-config.ts` — настройки сущностей (hp, damage, speed, цвета)

Импортировать из этих файлов, НЕ использовать числа напрямую.

### Правила использования библиотек

#### Miniplex ECS

- Добавление компонента: `world.addComponent(entity, "componentName", value)`
- Удаление компонента: `world.removeComponent(entity, "componentName")`
- Удаление сущности: `world.remove(entity)`
- Компонент `inScene` — сущность уже в сцене
- Запрос ожидающих добавления: `world.with("view").without("inScene")`
- При добавлении entity в сцену: сначала `scene.add()`, потом `world.addComponent(entity, "inScene", { inScene: true })`
- При удалении из сцены: `world.removeComponent(entity, "inScene")`
- Подписки на события мира: `world.onEntityAdded.subscribe()`, `world.onEntityRemoved.subscribe()`

#### Three.js

- Все shared геометрии и материалы — в `game-config.ts` (не в factories)
- Shared объекты нельзя dispose при удалении сущности
- При remove: только `mesh.removeFromParent()`
- Sprite material — уникальный, нужно dispose

### Взаимодействие

- **Логика → Визуал:** Системы меняют данные (position, hp), SyncRenderSystem синхронизирует с Three.js
- **Игра → UI:** Только `modules/hud/systems/update-hud.system.ts` записывает в `$state` (hudState)
- **Debug → UI:** Только `modules/debug/systems/update-debug.system.ts` записывает в `$state` (debugState)
- **UI → Игра:** UI вызывает `GameEngine.emit(event, data)`, системы подписываются

### Структура Svelte компонентов

- `src/lib/components/ui/` — UI примитивы (button, input и т.д.)
- `src/lib/components/layouts/` — layout-компоненты (обёртки для позиционирования)
- `src/lib/components/` — остальные компоненты (hud, menus, panels и т.д.)

---

## Чек-лист перед коммитом

- [ ] Нет `.js` файлов
- [ ] Нет лишних комментариев
- [ ] Логика в `modules/*/systems/`
- [ ] Использованы `const object` для enum
- [ ] Svelte компоненты минимальны (только отображение)
- [ ] Модули не импортируют фабрики друг друга
- [ ] UI использует `GameEngine.emit()` для действий

## Команды разработки

- `npm run check` — проверка типов (ОБЯЗАТЕЛЬНО после каждого изменения)
- `npm run lint` — линтер (вызывать после крупных задач, НЕ исправлять ошибки сразу — сообщить мне)
- `npm run format` — форматирование кода (после завершения задачи)

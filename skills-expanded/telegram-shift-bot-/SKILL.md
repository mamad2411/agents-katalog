# Правила проекта Telegram Shift Bot для Cursor AI

Этот файл содержит правила и соглашения для работы с проектом Telegram Shift Bot в Cursor AI.

## 🏗️ Архитектура

### Слоистая архитектура
Проект использует четкое разделение на слои:
- **Handlers** (`src/handlers/`) — только обработка событий Telegram, минимум логики
- **Services** (`src/services/`) — вся бизнес-логика, валидация, обработка данных
- **Repositories** (`src/repositories/`) — только доступ к данным, без бизнес-логики
- **Middlewares** (`src/middlewares/`) — инъекция зависимостей, проверка прав, общая обработка

**Правило:** Handlers НЕ должны содержать бизнес-логику. Вся логика должна быть в Services.

### Dependency Injection
Зависимости передаются через middleware и параметры функций:
```python
# ✅ Правильно
async def handler(
    message: Message,
    group_service: GroupService,  # Инъекция через middleware
    state: FSMContext,
) -> None:
    groups = await group_service.get_all_groups()

# ❌ Неправильно
async def handler(message: Message) -> None:
    pool = await get_db_pool()  # НЕ ДЕЛАТЬ ТАК
    service = GroupService(pool)
```

### Асинхронность
Все операции с БД и внешними API должны быть асинхронными:
```python
# ✅ Правильно
async def get_groups(self) -> List[Dict[str, Any]]:
    async with self.pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM groups")
```

## 📁 Структура проекта

### Именование файлов
- **Handlers:** `admin_<section>.py`, `courier_ai.py`, `user_handlers.py`
- **Services:** `<entity>_service.py` (например, `group_service.py`)
- **Repositories:** `<entity>_repository.py` (например, `group_repository.py`)
- **Middlewares:** `<purpose>_middleware.py` (например, `auth_middleware.py`)
- **States:** `<purpose>_states.py` (например, `admin_panel_states.py`)
- **Utils:** `<purpose>.py` (например, `admin_keyboards.py`)

### Организация handlers
- `admin_panel_navigation.py` — навигация по админ-панели (главное меню, переходы)
- `admin_groups.py` — управление группами
- `admin_settings.py` — настройки (расписание, слоты)
- `admin_polls.py` — управление опросами
- `admin_curator.py` — управление AI-куратором (FAQ, сообщения, замечания)
- `admin_broadcast.py` — рассылки
- `admin_monitoring.py` — мониторинг и верификация
- `courier_ai.py` — обработка вопросов от курьеров
- `user_handlers.py` — обработчики для обычных пользователей

## 💻 Стандарты кода

### Python Style Guide
Следуем **PEP 8** с обязательной типизацией и docstrings:

```python
# ✅ Правильно
from typing import Optional, List, Dict, Any

async def get_group(
    group_id: int,
    active_only: bool = False,
) -> Optional[Dict[str, Any]]:
    """
    Получить группу по ID.
    
    Args:
        group_id: ID группы
        active_only: Только активные группы
        
    Returns:
        Словарь с данными группы или None если не найдена
    """
    # ...
```

### Импорты
Порядок импортов:
1. Стандартная библиотека
2. Сторонние библиотеки
3. Локальные импорты

```python
import logging
from typing import Optional, Dict, Any
from datetime import date

from aiogram import Router
from aiogram.types import Message, CallbackQuery

from src.services.group_service import GroupService
from src.utils.auth import require_admin_callback
```

### Docstrings
Все публичные функции и классы должны иметь docstrings с описанием Args, Returns, Raises.

## 📝 Соглашения об именовании

### Переменные и функции
- **snake_case** для переменных и функций: `group_id`, `get_all_groups()`
- **UPPER_CASE** для констант: `MAX_SLOTS = 10`

### Классы
- **PascalCase** для классов: `GroupService`, `GroupRepository`

### Callback data
Формат: `admin:<section>:<action>[:<params>]`
- `admin:groups_menu`
- `admin:groups:create`
- `admin:polls:close:123`
- `admin:curator:add_faq`
- `admin:curator:search_faq`
- `admin:curator:create_info`
- `admin:curator:create_warning`
- `admin:curator:clear_history`
- `admin:curator:stats`

### Состояния FSM
Формат: `waiting_for_<action>`
- `waiting_for_group_name`
- `waiting_for_faq_question`
- `waiting_for_faq_answer`
- `waiting_for_search_query`
- `waiting_for_info_topic`
- `waiting_for_warning_description`
- `waiting_for_warning_user_id`
- `waiting_for_clear_history_user_id`

## 🗄️ Работа с базой данных

### Использование пула соединений
```python
# ✅ Правильно
class GroupRepository:
    def __init__(self, pool: Pool):
        self.pool = pool
    
    async def get_group(self, group_id: int) -> Optional[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM groups WHERE id = $1",
                group_id
            )
            return dict(row) if row else None
```

### SQL запросы
- **Всегда используйте параметризованные запросы** (`$1`, `$2`) для защиты от SQL injection
- Используйте транзакции для множественных операций
- Используйте `IF NOT EXISTS` в миграциях для идемпотентности

```python
# ✅ Правильно
await conn.execute(
    "INSERT INTO groups (name, telegram_chat_id) VALUES ($1, $2)",
    name, chat_id
)

# ❌ Неправильно
await conn.execute(
    f"INSERT INTO groups (name) VALUES ('{name}')"  # SQL injection!
)
```

## 📱 Работа с Telegram API

### Обработка сообщений
```python
# ✅ Правильно: типизация, обработка ошибок
@router.message(Command("admin"))
async def cmd_admin(
    message: Message,
    group_service: GroupService,
) -> None:
    """Обработка команды /admin."""
    try:
        groups = await group_service.get_all_groups()
        text = format_groups_list(groups)
        await message.answer(text)
    except Exception as e:
        logger.error("Ошибка: %s", e, exc_info=True)
        await message.answer("❌ Произошла ошибка")
```

### Callback queries
**Всегда отвечайте на callback:**
```python
# ✅ Правильно
@router.callback_query(lambda c: c.data == "admin:groups_menu")
@require_admin_callback
async def callback_groups_menu(callback: CallbackQuery) -> None:
    try:
        text = "📋 Управление группами"
        keyboard = get_groups_menu_keyboard()
        await safe_edit_message(callback.message, text, reply_markup=keyboard)
        await safe_answer_callback(callback)
    except Exception as e:
        logger.error("Ошибка: %s", e, exc_info=True)
        await safe_answer_callback(callback, "❌ Ошибка", show_alert=True)
```

### Безопасное редактирование сообщений
**Всегда используйте `safe_edit_message` и `safe_answer_callback`** из `src/utils/telegram_helpers.py`:
```python
from src.utils.telegram_helpers import safe_edit_message, safe_answer_callback

await safe_edit_message(
    callback.message,
    "Новый текст",
    reply_markup=keyboard
)
await safe_answer_callback(callback)
```

## 🔄 FSM (Finite State Machine)

### Определение состояний
Состояния определяются в `src/states/admin_panel_states.py`:
```python
class AdminPanelStates(StatesGroup):
    waiting_for_group_name = State()
    waiting_for_faq_question = State()
    waiting_for_faq_answer = State()
```

### Использование FSM
```python
# ✅ Правильно: установка состояния, сохранение данных
@router.callback_query(lambda c: c.data == "admin:curator:add_faq")
async def callback_add_faq(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminPanelStates.waiting_for_faq_question)
    await callback.message.answer("Введите вопрос:")

@router.message(AdminPanelStates.waiting_for_faq_question)
async def process_faq_question(message: Message, state: FSMContext) -> None:
    if message.text and message.text.lower() in ["отмена", "cancel"]:
        await state.clear()
        await message.answer("❌ Операция отменена")
        return
    
    question = message.text.strip()
    await state.update_data(faq_question=question)
    await state.set_state(AdminPanelStates.waiting_for_faq_answer)
    # ...
    
    await state.clear()  # Очистка после завершения
```

### Отмена операций
**Всегда проверяйте на отмену:**
```python
@router.message(AdminPanelStates.waiting_for_group_name)
async def process_group_name(message: Message, state: FSMContext) -> None:
    if message.text and message.text.lower() in ["отмена", "cancel"]:
        await state.clear()
        await message.answer("❌ Операция отменена")
        return
    # Обработка...
```

## 🤖 AI куратор в админ-панели

### Добавление функций AI куратора
1. **Добавьте кнопку в меню** (`src/utils/admin_keyboards.py`):
   ```python
   def get_curator_menu_keyboard() -> InlineKeyboardMarkup:
       keyboard = [
           [InlineKeyboardButton(text="➕ Добавить FAQ", callback_data="admin:curator:add_faq")],
           # ...
       ]
   ```

2. **Создайте callback handler** (`src/handlers/admin_curator.py`):
   ```python
   @router.callback_query(lambda c: c.data == "admin:curator:add_faq")
   @require_admin_callback
   async def callback_add_faq(callback: CallbackQuery, state: FSMContext) -> None:
       await state.set_state(AdminPanelStates.waiting_for_faq_question)
       # ...
   ```

3. **Используйте FSM для интерактивных диалогов**

4. **Используйте CuratorService для бизнес-логики:**
   ```python
   # ✅ Правильно: через сервис
   service = CuratorService(faq_repo, redis)
   faq_id = await service.add_faq_to_knowledge_base(
       question=question,
       answer=answer,
       category=category,
       tag=tag
   )
   ```

## ⚠️ Обработка ошибок

### Логирование ошибок
```python
# ✅ Правильно: логирование с контекстом
try:
    result = await service.operation()
except ValueError as e:
    logger.warning("Ошибка валидации: %s", e)
    await message.answer("❌ Ошибка валидации")
except Exception as e:
    logger.error("Неожиданная ошибка: %s", e, exc_info=True)
    await message.answer("❌ Произошла ошибка. Попробуйте позже.")
```

### Сообщения пользователю
**Всегда предоставляйте понятные сообщения пользователю:**
```python
# ✅ Правильно
try:
    await group_service.create_group(name, chat_id)
    await message.answer("✅ Группа создана успешно")
except ValueError as e:
    await message.answer(f"❌ Ошибка валидации: {e}")
except Exception as e:
    logger.error("Ошибка создания группы: %s", e, exc_info=True)
    await message.answer("❌ Произошла ошибка при создании группы. Попробуйте позже.")
```

## 📊 Логирование

### Уровни логирования
- **DEBUG** — детальная информация для отладки
- **INFO** — общая информация о работе
- **WARNING** — предупреждения (некритичные ошибки)
- **ERROR** — ошибки (требуют внимания)
- **CRITICAL** — критические ошибки

### Использование логгера
```python
import logging

logger = logging.getLogger(__name__)

# ✅ Правильно
logger.info("Создание группы: name=%s, chat_id=%s", name, chat_id)
logger.warning("Группа с таким Chat ID уже существует: %s", chat_id)
logger.error("Ошибка создания группы: %s", e, exc_info=True)
```

## 🔒 Безопасность

### Проверка прав доступа
**Всегда используйте декораторы для проверки прав:**
```python
# ✅ Правильно
@router.message(Command("admin"))
@require_admin
async def cmd_admin(message: Message) -> None:
    # Только админы могут выполнить эту команду
    ...

@router.callback_query(lambda c: c.data == "admin:groups:create")
@require_admin_callback
async def callback_create_group(callback: CallbackQuery) -> None:
    # Только админы могут выполнить этот callback
    ...
```

### Валидация входных данных
**Валидация должна быть в Services:**
```python
# ✅ Правильно
class GroupService:
    async def create_group(self, name: str, chat_id: int) -> Dict[str, Any]:
        if not name or len(name.strip()) == 0:
            raise ValueError("Название группы не может быть пустым")
        if chat_id >= 0:
            raise ValueError("Chat ID должен быть отрицательным для групп")
        # ...
```

## ⚡ Производительность

### Пул соединений
**Всегда используйте пул соединений, не создавайте новые подключения:**
```python
# ✅ Правильно
class GroupRepository:
    def __init__(self, pool: Pool):
        self.pool = pool  # Переиспользуем пул
```

### Асинхронность
**Используйте `asyncio.gather` для параллельного выполнения независимых операций:**
```python
# ✅ Правильно: параллельное выполнение
groups, polls = await asyncio.gather(
    group_service.get_all_groups(),
    poll_service.get_active_polls(),
)
```

## ✅ Чеклист перед коммитом

- [ ] Код соответствует PEP 8
- [ ] Все функции имеют docstrings с Args, Returns, Raises
- [ ] Добавлена типизация (type hints)
- [ ] Обработаны все исключения с логированием
- [ ] Используются параметризованные SQL запросы
- [ ] Проверка прав доступа (декораторы `@require_admin`, `@require_admin_callback`)
- [ ] Валидация входных данных в Services
- [ ] Используются `safe_edit_message` и `safe_answer_callback` для Telegram
- [ ] Все callback queries отвечают на запрос
- [ ] FSM состояния очищаются после завершения операций
- [ ] Обновлена документация (если нужно)
- [ ] Код протестирован локально

## 📚 Дополнительные ресурсы

- **README.md** — обзор проекта, быстрый старт
- **PROJECT_RULES.md** — подробные правила проекта
- **docs/** — подробная документация
- **QUICK_START.md** — быстрый старт

## 🎯 Приоритеты при разработке

1. **Безопасность** — всегда проверяйте права доступа, валидируйте входные данные
2. **Надежность** — обрабатывайте все ошибки, логируйте исключения
3. **Читаемость** — используйте типизацию, docstrings, понятные имена
4. **Производительность** — используйте пул соединений, асинхронность
5. **Поддерживаемость** — следуйте архитектуре, разделяйте ответственности

---

**Последнее обновление:** 2026-01-01

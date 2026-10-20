---
name: telegram-bot-aiogram
description: |
  Telegram bot development with aiogram 3.x. Apply for any Telegram bot, Mini App, or bot-integrated
  feature. Covers polling setup, FSM states, keyboards, middleware, error handling, payment integration
  (Payme/Click/Uzum), and Mini App WebApp bridge. Default: aiogram 3.x + polling + SQLite/PostgreSQL.
---

# Telegram Bot — aiogram 3.x Standards

## Project Structure
```
bot/
├── main.py                 # Bot entry point, polling start
├── config.py               # Settings from env
├── database/
│   ├── models.py           # SQLAlchemy models
│   └── crud.py             # DB operations
├── handlers/
│   ├── __init__.py         # Router aggregation
│   ├── start.py            # /start, /help
│   ├── registration.py     # FSM registration flow
│   ├── admin.py            # Admin panel handlers
│   └── payments.py         # Payment handlers
├── keyboards/
│   ├── reply.py            # ReplyKeyboardMarkup
│   └── inline.py           # InlineKeyboardMarkup
├── middlewares/
│   ├── auth.py             # User authentication
│   └── throttle.py         # Rate limiting per user
├── states/
│   └── forms.py            # FSMContext states
└── utils/
    ├── texts.py            # All message texts (no hardcoding in handlers)
    └── helpers.py
```

## Main Entry Point
```python
# main.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage  # or MemoryStorage for simple bots
from config import settings
from handlers import router

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def main():
    bot = Bot(token=settings.BOT_TOKEN, parse_mode="HTML")
    storage = RedisStorage.from_url(settings.REDIS_URL)  # MemoryStorage() for simple bots
    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    
    # Register middlewares
    dp.message.middleware(AuthMiddleware())
    dp.message.middleware(ThrottleMiddleware(rate_limit=0.5))  # 0.5s between messages
    
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## FSM (Finite State Machine)
```python
# states/forms.py
from aiogram.fsm.state import State, StatesGroup

class RegistrationForm(StatesGroup):
    waiting_name = State()
    waiting_phone = State()
    waiting_city = State()
    confirm = State()

# handlers/registration.py
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(RegistrationForm.waiting_name)
    await message.answer("Ismingizni kiriting:")

@router.message(RegistrationForm.waiting_name)
async def process_name(message: Message, state: FSMContext):
    if not message.text or len(message.text) < 2:
        await message.answer("❌ Ism kamida 2 ta harf bo'lishi kerak.")
        return
    await state.update_data(name=message.text.strip())
    await state.set_state(RegistrationForm.waiting_phone)
    await message.answer("📱 Telefon raqamingizni yuboring:", reply_markup=kb.phone_request())

@router.message(RegistrationForm.waiting_phone, F.contact)
async def process_phone(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    await state.update_data(phone=phone)
    data = await state.get_data()
    await state.clear()
    await save_user(message.from_user.id, data)
    await message.answer(f"✅ Ro'yxatdan o'tdingiz!\nIsm: {data['name']}\nTel: {phone}")
```

## Keyboards
```python
# keyboards/inline.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🛍 Mahsulotlar", callback_data="products")
    builder.button(text="📦 Buyurtmalarim", callback_data="my_orders")
    builder.button(text="👤 Profil", callback_data="profile")
    builder.button(text="📞 Aloqa", callback_data="contact")
    builder.adjust(2, 2)  # 2 columns
    return builder.as_markup()

def confirm_action(action: str, item_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Ha", callback_data=f"confirm:{action}:{item_id}")
    builder.button(text="❌ Yo'q", callback_data="cancel")
    builder.adjust(2)
    return builder.as_markup()
```

## Error Handling
```python
# Global error handler
@dp.errors()
async def error_handler(update: types.Update, exception: Exception):
    logger.error(f"Update: {update}\nException: {exception}", exc_info=True)
    
    if isinstance(exception, TelegramForbiddenError):
        # User blocked the bot — mark as inactive in DB
        if update.message:
            await deactivate_user(update.message.from_user.id)
    elif isinstance(exception, TelegramRetryAfter):
        await asyncio.sleep(exception.retry_after)
    
    return True  # Suppress the error
```

## Throttle Middleware
```python
class ThrottleMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 0.5):
        self.rate_limit = rate_limit
        self.storage: dict[int, float] = {}

    async def __call__(self, handler, event: Message, data: dict):
        user_id = event.from_user.id
        now = time.time()
        last = self.storage.get(user_id, 0)
        
        if now - last < self.rate_limit:
            await event.answer("⏳ Iltimos, biroz kuting...")
            return
        
        self.storage[user_id] = now
        return await handler(event, data)
```

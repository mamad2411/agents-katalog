---
name: character-sheet
description: Создаёт листы персонажа (character sheet) на белом фоне с 4-х ракурсов (фронт, 3/4, профиль, спина) через GPT Image 2 для последующего переиспользования в фото и видео генерациях. Сохраняет персонажей в `createya/characters/<slug>/` и регистрирует их в MASTER_CONTEXT.md проекта. Триггеры — "создай персонажа", "сделай character sheet", "сохрани образ", "AI-инфлюенсер", "лист персонажа", "персонаж для серии", "повтори этого человека", "use character".
---

# Character Sheet Skill

Делает persistent identity для AI-персонажа: одно изображение с **4-мя ракурсами** на белом фоне → нейросети понимают «вот этот человек со всех сторон» и держат консистентность в любой последующей генерации.

## Зачем нужен

- **Soul ID без training**: Higgsfield Soul ID требует 20+ фото и 3-5 минут серверного training. Наш подход — один вызов GPT Image 2, ~30 секунд, никаких account-bound артефактов.
- **Workaround-free**: западное сообщество клеит sheets через multi-image LoRA / ControlNet / отдельные runs со склейкой — часы работы. У нас одна команда.
- **Persistent**: sheet сохраняется в проекте юзера. Через неделю открыл проект — sheet на месте, продолжаешь с того же образа.

## Pipeline

### 1. Intake — собрать референсы

- 1-3 фото персонажа (лицо обязательно, тело желательно).
- Если юзер не приложил — спроси: «Дай 1-3 reference фото — лицо/полный рост — или опиши персонажа текстом».
- Если только текстовое описание — сначала генерируем reference через `gpt-image-2-t2i` (text-to-image), потом sheet через `gpt-image-2-i2i`.

### 2. Дать имя персонажу

Спроси у юзера короткий slug на русском или английском: `anya`, `boris`, `kim`, `model_summer`. Slug — lowercase + дефисы, без пробелов. Используется как имя директории.

Если в проекте уже есть `characters/<slug>/` — спроси: пересоздать sheet (overwrite) или взять новое имя.

### 3. Outfit — что на нём надет

Дефолт: **нейтральная серая футболка + тёмные джинсы** (универсально, не отвлекает от лица).

Альтернативы — спроси если нужно:
- formal: костюм, рубашка
- casual streetwear: oversized hoodie + кроссовки
- character-specific: по контексту (если для брендового проекта)

### 4. Генерация sheet через `gpt-image-2-i2i`

Используй preset `presets/sheet-template-4-angle.md` — там полный prompt template. Передаём через `mcp__createya__run_model`:

```
model: gpt-image-2-i2i
input:
  image_url: <reference photo CDN URL>
  prompt: <prompt from preset, with outfit substituted>
  size: 1536x1024  (16:9, room for 4 figures)
  quality: high
  num_images: 1
```

Если у юзера несколько reference фото — используй модель в multi-image-input режиме (если `parameters_schema` поддерживает `image_urls[]`) или сначала склей реф через любой из них как primary.

### 5. Vision QA — проверить результат

После генерации обязательно `Read` сгенерированное изображение и проверь:

- ✅ 4 фигуры в одном кадре, расположены слева направо: front / 3-quarter / profile / back
- ✅ Все 4 фигуры — **один и тот же человек** (лицо, телосложение, пропорции совпадают)
- ✅ Outfit идентичный на всех ракурсах
- ✅ Белый фон без артефактов
- ✅ Освещение мягкое и равномерное
- ✅ Никаких лишних объектов

Если что-то не так — regenerate с уточнённым промтом (объясни юзеру что именно поправил).

### 6. Approve gate

Покажи юзеру результат:
> «Готов лист персонажа [slug]. Лица консистентны, outfit един. Сохраняю в проект?»

Только после явного «да» переходи к шагу 7.

### 7. Сохранение

Создай структуру:

```
createya/characters/<slug>/
├── character_profile.json
├── sheet.png           ← скачанная копия (через `bash` curl или Read)
└── references/
    ├── ref_1.jpg
    └── ref_2.jpg       (исходные референсы юзера)
```

`character_profile.json` — фиксированная схема:

```json
{
  "slug": "anya",
  "display_name": "Anya",
  "description": "25 y.o., dark wavy hair, slim build, warm skin tone",
  "outfit": "neutral grey t-shirt and dark jeans",
  "sheet_url": "https://cdn-new.createya.ai/temp/.../anya-sheet.png",
  "sheet_local": "characters/anya/sheet.png",
  "reference_urls": [
    "https://cdn-new.createya.ai/temp/.../ref-1.jpg"
  ],
  "created_at": "2026-05-07T12:00:00Z",
  "model_used": "gpt-image-2-i2i",
  "prompt_template": "4-angle sheet template v1"
}
```

### 8. Update MASTER_CONTEXT.md

Открой `createya/MASTER_CONTEXT.md`. Если нет секции `## Characters` — добавь её. Добавь запись:

```markdown
## Characters

- **anya** — 25 y.o., dark wavy hair, slim build, warm skin tone
  - Sheet: `characters/anya/sheet.png` (https://cdn-new.createya.ai/temp/.../anya-sheet.png)
  - Outfit: neutral grey t-shirt + dark jeans
  - Created: 2026-05-07
  - Use: передавай sheet как `start_image_url` или `image_url` в `run_model` для консистентности
```

## Reuse в последующих генерациях

Когда юзер говорит «Сделай Anya на пляже» / «Anya в офисном костюме» — skill автоматически:

1. Читает `MASTER_CONTEXT.md` → находит секцию `## Characters` → находит `anya`.
2. Читает `characters/anya/character_profile.json` → берёт `sheet_url`.
3. Передаёт sheet как `start_image_url` (или `input_images[0]` для моделей принимающих массив) в любой image/video endpoint.
4. Инжектит в промт описание: `Maintain character identity from reference: <description>`.

### Пример reuse

Юзер: «Anya на яхте, закат, 16:9»

Skill вызывает:
```
model: nano-banana-pro-i2i  (или другой image endpoint с image_url)
input:
  image_url: <anya sheet_url>
  prompt: "Photorealistic shot of the woman from the reference sheet, on a luxury yacht at sunset. Maintain character identity: 25 y.o., dark wavy hair, slim build, warm skin tone. Cinematic lighting, golden hour, 16:9."
  aspect_ratio: "16:9"
```

Для видео — генерируется still через image модель, потом chain в video endpoint.

## Триггеры в чате

- «создай персонажа [имя]»
- «сделай character sheet»
- «лист персонажа на белом фоне»
- «сохрани образ»
- «AI-инфлюенсер для проекта»
- «модель для серии фото»
- «use character anya»
- «возьми Anya и сделай ...»
- «повтори того же человека из ...»

## Edge cases

### Юзер дал только текстовое описание (без фото)

Pipeline:
1. Сначала text-to-image: `gpt-image-2-t2i` с описанием → один портрет (front view).
2. Используй полученный портрет как reference → запускай sheet generation.
3. Это удваивает стоимость — предупреди юзера: «Создам персонажа с нуля по описанию (~50 кредитов: 25 на портрет + 25 на лист).»

### Reference фото плохого качества (низкое разрешение, обрезано)

Если reference < 512x512 или сильно обрезанный — предупреди:
> «Reference невысокого качества. Sheet может получиться с drift'ом. Продолжаем или дай другое фото?»

### Несколько персонажей в одном reference

Если на reference больше одного человека — спроси: «На фото 2+ человека. Какой из них — главный? Опиши кратко (левый/правый, в красном/синем).»

### Кредитный бюджет

Перед запуском проверь баланс через `mcp__createya__get_balance`. GPT Image 2 high quality ~25-50 кредитов. Если у юзера < 100 — предупреди про стоимость sheet + потенциальный regenerate.

## Что skill НЕ делает (out of scope)

- ❌ Auto-detection «на твоём фото — новый персонаж, зафиксировать?» — это будущая фича, сейчас юзер явно просит.
- ❌ Sheet refresh с новыми фото — пока пересоздаёшь с нуля (overwrite).
- ❌ Multi-character scenes — передавать 2+ sheet'ов в одну генерацию когда модели поддержат массив `image_urls[]`.
- ❌ Обучение LoRA / Soul ID на стороне сервера — наш подход без server-side training.

## Связанные skills

- `creative-director` — после создания character использует его в любом workflow (`single-shot`, `lookbook`, `editorial-series`, `ugc-ad`).
- `motion-director` (планируется CRE-XXX) — sheet → video с named camera presets.

## Файлы skill

- [SKILL.md](./SKILL.md) — этот файл
- [presets/sheet-template-4-angle.md](presets/sheet-template-4-angle.md) — основной prompt template для GPT Image 2
- [workflows/create-sheet.md](workflows/create-sheet.md) — пошаговый workflow создания
- [workflows/reuse-character.md](workflows/reuse-character.md) — pattern переиспользования

---
_Created: 2026-05-07 — CRE-413_

---
name: createya-batch
description: Batch generation workflow for Createya — when user asks to generate N variations / pack / lookbook / series of images or videos. Reads concurrency limit from user's plan, builds a queue, fires at limit, polls async, saves results to a project workspace (creative/output/<task>/). Use when user says "сгенерируй N креативов", "пачкой", "вариации", "5 картинок", "сделай серию", "batch", "lookbook", or after creative-director skill has prepared the brief and is ready to execute multiple shots.
---

# Createya Batch — пачечная генерация с очередью и workspace

Этот skill — рабочая обёртка над `createya:*` MCP-тулзами для случая «нужно сгенерировать **несколько** результатов». Делает три вещи которые агент сам по себе делать криво:

1. **Уважает concurrency-лимит тарифа** — не льёт N одновременно, получая 429.
2. **Очередь + polling** — fire `limit`, ждёт complete, fire next.
3. **Раскладывает результаты в проектный workspace** — `creative/output/<task>/` с manifest.

Требует установленного `createya` skill (low-level MCP wrapper). Если его нет — выполни одной командой из README этого репо.

## Когда триггериться

- «Сгенерируй 5 креативов», «пачкой», «5 вариаций», «сделай серию»
- «lookbook», «character sheet», «multi-aspect ad»
- После того как `creative-director` подготовил бриф и эталон, время делать вариации
- Любой запрос с числом > 1 в количестве результатов

## Workspace convention

Перед первой генерацией создай structure (если не существует):

```
creative/
├── refs/                          # пользовательские референсы / source images
├── etalon/                        # locked "perfect" frames для consistency
└── output/
    └── YYYY-MM-DD-<task-slug>/    # один таск = одна папка
        ├── manifest.json          # что сгенерировано: prompt, model, credits, run_id, file
        ├── 01-<variant-slug>.png  # пронумерованные результаты
        ├── 02-<variant-slug>.png
        └── ...
```

`<task-slug>` — короткий kebab-case, выводи из брифа: `cat-on-moon`, `summer-lookbook`, `product-hero-shots`.
`<variant-slug>` — описание конкретной вариации: `cinematic-portrait`, `pastel-wide`, `front-angle`.

Если у пользователя в проекте уже есть `creative/` — продолжай в той же структуре. Если нет — создай папки через `Bash mkdir -p creative/{refs,etalon,output}`.

## Полный workflow

### 1. Получи concurrency-лимит и баланс

```
createya:get_balance() → {
  credits_balance: 16399,
  concurrency: { limit: 4, in_use: 0 }   ← ЭТО ВАЖНО
}
```

`concurrency.limit` — сколько runs одновременно можно держать. **Это лимит тарифа** (Start=1, Creator=2, Pro=3, Enterprise=4). Не обходи его — получишь 429 `concurrent_limit_exceeded`.

`concurrency.in_use` — сколько уже занято (может быть >0 если пользователь параллельно что-то генерит в боте или другом MCP-клиенте). **Эффективная емкость очереди = `limit - in_use`**.

### 2. Прикинь бюджет ДО запуска

```
createya:list_models()  → найди family, посмотри endpoint в нём
```

Для каждой задуманной вариации:
- `credits_per_request` — типичная цена при дефолтном конфиге
- `credits_max` — потолок (high quality + max size)

Суммируй и сравни с `credits_balance`. Если `total_cost_estimate > balance`:
- Предупреди пользователя: «Эта пачка обойдётся ≈X кредитов, баланс Y. Пополнить можно на createya.ai».
- Не запускай молча.

### 3. Создай workspace

```bash
TASK="2026-05-12-cat-on-moon"
mkdir -p "creative/output/$TASK"
```

Сразу создай **пустой** `manifest.json`:

```json
{
  "task": "cat-on-moon",
  "date": "2026-05-12",
  "concurrency_limit": 4,
  "total_requested": 5,
  "items": []
}
```

### 4. Очередь — fire by chunks

Эффективная емкость = `limit - in_use`. Если `in_use=0, limit=4` — fire 4 одновременно, потом 5-я после освобождения слота.

**Псевдокод:**
```
queue = [variant_1, variant_2, ..., variant_N]
in_flight = {}                      // run_id → variant
completed = []
capacity = balance.concurrency.limit - balance.concurrency.in_use

while queue or in_flight:
    # Fire while we have capacity
    while len(in_flight) < capacity and queue:
        v = queue.pop(0)
        resp = createya:run_model(model=v.family, input=v.input)
        if resp.status == "completed":          // sync model returned immediately
            save_result(v, resp.output.urls)
            completed.append(v)
        elif resp.run_id:                        // async
            in_flight[resp.run_id] = v
        else:
            log_failure(v, resp.error)

    # Poll in-flight
    if in_flight:
        sleep(2 if image_only else 8)
        for run_id, v in list(in_flight.items()):
            status = createya:get_run_status(run_id)
            if status.status == "completed":
                save_result(v, status.output.urls)
                completed.append(v)
                del in_flight[run_id]
            elif status.status == "failed":
                log_failure(v, status.error)
                del in_flight[run_id]
            # else "processing" / "queued" — keep polling
```

Нюансы:
- **Не делай больше parallel runs чем `capacity`** — получишь 429. Если получил — wait `Retry-After` секунд из header, перезапусти.
- **Polling interval**: image-модели обычно sync (3-15 сек), video — async 30-120 сек. Для image — 2-3s, для video — 8-10s.
- **Failed runs** — не блокируй очередь, просто логируй и продолжай. Failed = 0 credits charged (auto-refund).

### 5. Сохрани результат каждого run

После `completed`:

```bash
# Скачать с CDN — output.urls[0] (or output.url)
NN=$(printf '%02d' "$index")
EXT="${OUTPUT_URL##*.}"   # png/jpg/webp/mp4
curl -fsSL "$OUTPUT_URL" -o "creative/output/$TASK/${NN}-${VARIANT_SLUG}.${EXT}"
```

Обнови `manifest.json` (атомарно — read → modify → write):

```json
{
  "task": "cat-on-moon",
  "date": "2026-05-12",
  "concurrency_limit": 4,
  "total_requested": 5,
  "items": [
    {
      "file": "01-cinematic-wide.png",
      "variant": "cinematic-wide",
      "model": "nano-banana-pro",
      "endpoint": "nano-banana-pro-t2i",
      "input": { "prompt": "...", "aspect_ratio": "16:9" },
      "credits_spent": 18,
      "run_id": "abc123",
      "output_url": "https://cdn-new.createya.ai/...",
      "created_at": "2026-05-12T15:30:00Z",
      "status": "completed"
    }
  ],
  "summary": {
    "total_credits_spent": 90,
    "successful": 5,
    "failed": 0,
    "duration_seconds": 47
  }
}
```

### 6. Финальный репорт юзеру

```
✓ 5/5 готово · 90 кредитов потрачено · 47 сек
Результаты в creative/output/2026-05-12-cat-on-moon/:
  01-cinematic-wide.png
  02-pastel-portrait.png
  03-noir-closeup.png
  ...
Баланс: 16309 кредитов
```

Покажи 2-3 результата как markdown-image previews (агент сам берёт пути из manifest).

## Edge cases

**Очень большая пачка (N > 20)**. Раздели на под-пачки по 10-20:
- Сохраняй прогресс в `manifest.json` после каждого
- Если процесс прервётся — продолжай: пройди по `items[]` и пропусти уже `status === "completed"`

**Concurrency=1 (Start план)**. Очередь становится последовательной — это нормально, не оптимизируй. Просто покажи пользователю прогресс «3/5».

**Long-running video runs**. `kling-video-v3-pro` / `veo-3.1` могут занимать 30-120 секунд:
- Сообщи: «Запустил, видео генерится 30-120 сек, чекаю каждые 10с»
- Поллируй раз в 10с, не 2с

**429 concurrent_limit_exceeded в середине**. Если получил — `in_use` поменялся (юзер запустил параллельно где-то ещё):
- Подожди `Retry-After` секунд (header)
- Перезвони `get_balance`, обнови `capacity`
- Повтори run_model

**402 Insufficient credits**. Если кончились в середине:
- Останови очередь
- Сохрани manifest с тем что есть
- Сообщи: «Закончились кредиты после 3/5. Пополни и я продолжу: подскажи когда».

## Anti-patterns

- ❌ **Fire-and-forget** N параллельно без проверки лимита → 429 и потеря части очереди
- ❌ **Polling без интервала** (tight loop) → rate-limit
- ❌ **Игнорировать failed runs** → пользователь думает что всё ОК, реально 2/5 пропущено
- ❌ **Сохранять без manifest.json** → потеря контекста (какой prompt дал какую картинку)
- ❌ **Жёстко зашивать concurrency=N** в код агента → лимит зависит от тарифа, всегда из `get_balance`
- ❌ **Сразу 2K/4K без согласия** → `credits_max` может в 5× превысить typical. Всегда estimate.

## Связанные skills

- `createya` — base MCP wrapper (low-level run_model / list_models / get_balance / get_run_status / request_upload_url)
- `creative-director` — высокий уровень «эталон + вариации», подготовка брифа. Для серий вариаций creative-director может звать createya-batch для исполнения.

## Docs

- [createya.ai/api](https://createya.ai/api) — REST + MCP reference
- [createya.ai/settings/billing](https://createya.ai/settings/billing) — план и concurrency limit
- [createya.ai](https://createya.ai) — пополнение

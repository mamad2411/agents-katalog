---
name: vps-verify
description: "Post-deploy verification of a deployed web application. Reads credentials from update.py, fetches key pages, checks HTTP status and expected HTML elements, outputs a pass/fail table."
group: deploy
triggers:
  - "проверь деплой"
  - "сайт работает?"
  - "после деплоя"
  - "docker-compose up"
output: "pass/fail verification table of deployed application"
calls: []
---

# VPS Verify — Post-Deploy Health Check

**Назначение:** После деплоя — автоматически верифицировать что приложение работает.
Читает credentials из `update.py`, логинится в приложение, проверяет ключевые страницы.
**Когда использовать:** После `docker-compose up` / деплоя на VPS за nginx/caddy.
**Результат:** Таблица "Страница | Ожидалось | Найдено | Статус" в чате.

---

## PROCESS

### Шаг 1 — Прочитай credentials

Прочитай `update.py` в текущем проекте. Найди:
- `HOST` / `host` / `BASE_URL` — адрес приложения
- `USERNAME` / `LOGIN` / `user` — логин
- `PASSWORD` / `pass` — пароль
- Порт (если не стандартный 80/443)

Если `update.py` не существует — спроси у пользователя: base URL и credentials.

### Шаг 2 — Составь checklist страниц

Спроси пользователя (или выведи из CLAUDE.md если там есть роуты):

> "Какие страницы проверить? Укажи URL + ожидаемый HTML-элемент/класс для каждой.
> Или нажми Enter для дефолтного набора: `/`, `/login`, `/dashboard` (или аналоги из CLAUDE.md)"

**Дефолтный набор если не указано:**
| URL | Ожидаемый элемент |
|-----|------------------|
| `/` | `<body` |
| `/login` (или первый роут) | `<form` или `input` |
| Основной роут приложения | Ключевой CSS-класс из CLAUDE.md |

### Шаг 2.5 — App-level health check (если есть)

Перед HTTP-проверками — найди в CLAUDE.md эндпоинт состояния приложения:
- Ищи `/api/status`, `/health`, `/api/health`, `/status` в тексте CLAUDE.md
- Если найден — запроси его отдельно и выведи результат

```python
import requests, json

health_url = BASE + "/api/status"  # или найденный из CLAUDE.md
try:
    r = requests.get(health_url, timeout=10)
    if r.status_code == 200:
        try:
            data = r.json()
            online = data.get("online", "?")
            age = data.get("age_seconds", "?")
            print(f"App health: online={online}, age_seconds={age}")
        except Exception:
            # Если ответ не JSON (например, редирект на логин) — пометить
            print(f"App health: HTTP {r.status_code}, но не JSON (требует логин?)")
    else:
        print(f"App health: HTTP {r.status_code} ❌")
except Exception as e:
    print(f"App health: недоступен — {e}")
```

**Вывод в таблицу:**
```
App Health  /api/status  online=True age=14s   ✅ OK
App Health  /api/status  online=False age=450s  ❌ OFFLINE
App Health  /api/status  HTTP 302 (auth)         ⚠️ Требует логин
```

Если эндпоинт не найден в CLAUDE.md — пропустить шаг, написать: `App health: эндпоинт не найден в CLAUDE.md — пропущено`.

### Шаг 3 — Выполни проверки через Python/paramiko

```python
import requests
from requests.exceptions import ConnectionError, Timeout

BASE = "http://HOST:PORT"  # из update.py
session = requests.Session()

checks = [
    ("/", 200, ["<body"]),
    ("/login", 200, ["<form", "input"]),
    # добавить из пользовательского checklist
]

results = []
for path, expected_status, expected_elements in checks:
    try:
        r = session.get(BASE + path, timeout=10, allow_redirects=True)
        found = [el for el in expected_elements if el in r.text]
        missing = [el for el in expected_elements if el not in r.text]
        results.append({
            "page": path,
            "status": r.status_code,
            "expected_status": expected_status,
            "found": found,
            "missing": missing,
            "ok": r.status_code == expected_status and not missing
        })
    except (ConnectionError, Timeout) as e:
        results.append({
            "page": path,
            "status": "ERR",
            "expected_status": expected_status,
            "found": [],
            "missing": expected_elements,
            "ok": False,
            "error": str(e)
        })
```

Если приложение требует логин (session/cookie):
1. Сначала POST на `/login` с credentials
2. Затем выполни остальные проверки в той же `session`

### Шаг 4 — Выведи таблицу результатов

```
VPS Verify — [PROJECT NAME] — [TIMESTAMP]
═══════════════════════════════════════════════════════

Страница    HTTP    Элементы              Статус
──────────────────────────────────────────────────────
/           200     <body ✓               ✅ OK
/login      200     <form ✓, input ✓      ✅ OK
/dashboard  200     .bento-card ✗         ❌ FAIL
/api/health 200     {"status":"ok"} ✓     ✅ OK

──────────────────────────────────────────────────────
Итог: 3/4 прошло  |  1 упало
```

### Шаг 4.5 — Verify new code in container (Docker-проекты)

Если проект использует Docker с baked images (не volume-mounted code) — проверь что контейнер запустился с НОВЫМ кодом, а не со старым образом.

**Как определить:** в CLAUDE.md или `docker-compose.yml` есть `build:` секция (не только `image:`).

**Проверка через SSH/paramiko:**
```python
# Взять имя контейнера из CLAUDE.md или docker compose ps
# Взять ключевую функцию/константу из последнего изменённого файла
verify_cmd = 'docker exec polymarket-monitor grep -n "batch_get_order_books\\|MAX_TOKENS" /app/polymarket_insider/collector.py'
# Если вывод пустой → контейнер запущен со СТАРЫМ образом → нужен rebuild
```

**Результат в таблице:**
```
Code Verify  collector.py  MAX_TOKENS found ✓   ✅ New code active
Code Verify  collector.py  (пусто)              ❌ OLD image — нужен rebuild!
```

**Если старый код обнаружен:**
```
❌ Контейнер запущен со старым образом.
Выполни на VPS:
  docker compose build <service>
  docker compose up -d <service>
Затем повтори /vps-verify.
```

### Шаг 5 — Диагностика при падении

Для каждого ❌:
- HTTP ≠ ожидаемому → скажи: "Сервер вернул [N]. Проверь nginx/caddy config или docker logs."
- HTML-элемент не найден → выведи первые 500 символов ответа для визуального осмотра
- ConnectionError → скажи: "Приложение не отвечает. Проверь: `docker ps`, `docker logs [container]`"

---

## ПРАВИЛА

- **Никогда не хардкоди credentials** в тексте вывода — маскируй пароль: `p***d`
- Таймаут на запрос: 10 секунд (не бесконечность)
- Если BASE_URL содержит `localhost` — напомни: "Если запускаешь не с VPS, а локально — замени на внешний IP"
- SSH-туннель не нужен если приложение доступно напрямую по HTTP/HTTPS

---

## ИНТЕГРАЦИЯ

Добавь в CLAUDE.md проекта секцию `## Deploy Checklist`:
```
## Deploy Checklist
- [ ] `python update.py` — деплой
- [ ] `/vps-verify` — верификация
```

Это делает verify частью стандартного деплой-цикла проекта.

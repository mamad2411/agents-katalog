---
name: docker-deploy
description: "Full deploy cycle for Docker projects with baked images: sync files, rebuild image, start containers, verify new code, check app health."
group: deploy
triggers:
  - "задеплой"
  - "выкати"
  - "обнови сервер"
  - "update.py упал"
  - "docker build нужен"
output: "deployed and verified Docker application on VPS"
calls: [vps-verify]
---

# Docker Deploy — Full Cycle for Baked-Image Projects

**Назначение:** Задеплоить изменения на VPS для Docker-проекта где код baked в образ (не volume-mounted).
**Когда использовать:** После изменения `.py` / `.js` / `.html` файлов в проекте с `docker compose build`. При "задеплой", "обнови сервер", "выкати изменения".
**Результат:** Таблица статусов всех шагов: sync / build / up / code-verify / health.

> ⚠️ **Отличие от `vps-verify`:** `docker-deploy` выполняет деплой. `vps-verify` только проверяет уже задеплоенное.

---

## PROCESS

### Шаг 1 — Прочитай конфигурацию

Прочитай `update.py` в текущем проекте. Найди:
- `HOST` — IP-адрес VPS
- `USER` / `username` — SSH пользователь
- `PASSWORD` — SSH пароль
- `REMOTE_BASE` / remote path — путь на VPS
- Имена сервисов для rebuild (из docker-compose.yml или CLAUDE.md)

Если `update.py` не найден — спроси у пользователя: HOST, USER, PASSWORD, remote path, service names.

### Шаг 2 — Определи изменённые файлы

Найди файлы изменённые в текущей сессии:
```python
import os, glob, time
files = sorted(glob.glob('**/*', recursive=True), key=os.path.getmtime, reverse=True)
recent = [f for f in files[:30] if os.path.isfile(f)]
```

Исключи из sync:
- `**/*.png`, `**/*.jpg`, `**/*.gif`, `**/*.pdf` — бинарные медиа-файлы
- `**/__pycache__/**`, `**/*.pyc` — кэш Python
- `**/examples/**`, `**/docs/**` — если не менялись в сессии
- `.git/**`, `node_modules/**`

Покажи список: "Загружу N файлов на VPS: [список]". Дождись "да".

### Шаг 3 — Sync файлов на VPS

```python
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, username=USER, password=PASSWORD, timeout=30)
sftp = client.open_sftp()

for local_path, remote_path in files_to_upload:
    sftp.put(local_path, remote_path)
    print(f"  ✓ {remote_path}")

sftp.close()
```

При EOFError / ConnectionResetError на большом файле:
- Пропусти файл, залогируй предупреждение
- Продолжай со следующим
- В конце сообщи о пропущенных

### Шаг 4 — Rebuild Docker image

```python
def run_ssh(client, cmd, timeout=180):
    transport = client.get_transport()
    chan = transport.open_session()
    chan.exec_command(cmd)
    output = b''
    while True:
        if chan.recv_ready():
            output += chan.recv(4096)
        if chan.exit_status_ready():
            while chan.recv_ready():
                output += chan.recv(4096)
            break
        time.sleep(0.5)
    return output.decode(errors='replace'), chan.recv_exit_status()

cmd = f"cd {REMOTE_PATH} && docker compose build {' '.join(services)} 2>&1"
out, code = run_ssh(client, cmd, timeout=300)
```

Показывай прогресс в реальном времени (streaming). Timeout: 300s.

При exit code ≠ 0 — СТОП:
```
❌ Build failed (exit code N):
[last 20 lines of output]
Деплой прерван. Исправь ошибку и повтори.
```

### Шаг 5 — Start containers

```python
cmd = f"cd {REMOTE_PATH} && docker compose up -d {' '.join(services)} 2>&1"
out, code = run_ssh(client, cmd, timeout=60)
```

Ожидаемый вывод: `Container X Started` для каждого сервиса.

### Шаг 6 — Verify new code in container

Для каждого изменённого `.py` файла — проверь что новая функция/константа видна в контейнере:

```python
# Взять ключевой символ из последнего изменённого файла
# Например: первая строка изменения, уникальная для новой версии
check_cmd = f'docker exec {container} grep -c "NEW_SYMBOL" /app/module.py'
out, code = run_ssh(client, check_cmd, timeout=10)
# Если вывод = "0" или пустой → старый образ
```

**Автоопределение символа для проверки:**
- Читай diff (Glob последних изменённых файлов → первое новое слово/функция)
- Или используй последнее изменение из changelog сессии

Результат: `✅ New code active` или `❌ OLD image detected`.

При `❌ OLD image` — СТОП и предложи:
```
❌ Контейнер запустился со старым образом.
Возможные причины:
  1. Build завершился успешно, но up использовал кэш
  2. Имя сервиса не совпадает с именем контейнера
Попробуй: docker compose up -d --force-recreate {service}
```

### Шаг 7 — App health check

Если в CLAUDE.md есть `/api/status` или аналог:
```python
import requests, time
time.sleep(5)  # дать контейнеру стартовать
r = requests.get(f"https://{DOMAIN}/api/status", timeout=10)
```

Если требует логин → подключайся через SSH и `docker exec`.

### Шаг 8 — Итоговый отчёт

```
Docker Deploy — [PROJECT] — [TIMESTAMP]
═══════════════════════════════════════════════════════

Шаг              Детали                        Статус
──────────────────────────────────────────────────────
Sync             5 файлов загружено            ✅ OK
Build            apps-polymarket-monitor       ✅ OK (28s)
Up               polymarket-monitor started    ✅ OK
Code Verify      MAX_TOKENS found in container ✅ New code
App Health       online=True, age=12s          ✅ OK

──────────────────────────────────────────────────────
Итог: деплой успешен ✅
```

---

## ПРАВИЛА

- **Никогда не хардкоди credentials** в выводе — маскируй пароль: `p***d`
- **СТОП при build failure** — не продолжать up если build упал
- **Исключай медиа из sync** — PNG/JPG/PDF часто роняют SFTP-соединение (EOFError)
- **Timeout build: 300s** — образы собираются долго при первом запуске
- **Streaming вывода при build** — не молчи 5 минут, показывай прогресс
- Если `update.py` уже делает sync+build+up — предложи использовать его: `py update.py {app}`
  Используй manual workflow только если `update.py` падает или недоступен

---

## ИНТЕГРАЦИЯ

После успешного деплоя — запусти `vps-verify` для полной проверки:
```
Деплой завершён. Запустить /vps-verify для финальной верификации?
```

Добавь в CLAUDE.md проекта:
```
## Deploy Workflow
- [ ] `py update.py {app}` — автодеплой (sync + build + up)
- [ ] `/docker-deploy` — если update.py падает на SFTP
- [ ] `/vps-verify` — верификация после деплоя
```

---

## CHECKLIST (pre-delivery)

- [ ] credentials прочитаны из update.py, пароль замаскирован в выводе
- [ ] медиа-файлы исключены из sync
- [ ] build streaming output показан пользователю
- [ ] code verify выполнен для хотя бы одного изменённого файла
- [ ] итоговая таблица показана

---
name: kd-install
description: Установить и подключить MCP-сервер kd-rules-mcp (правила обмена «Конвертации данных 2» для 1С) — из готового образа или клона до рабочего project_list, с вопросами человеку и проверкой после каждого шага. Использовать, когда просят «установи/настрой/подключи kd-rules-mcp», подключить его к проекту 1С или добавить в него новый проект.
---

# Установка kd-rules-mcp агентом

Человеческая версия тех же шагов — `docs/INSTALL.md` репозитория
(https://github.com/egordoronchenko/kd-rules-mcp). Этот файл можно получить и без клона:
https://raw.githubusercontent.com/egordoronchenko/kd-rules-mcp/main/.claude/skills/kd-install/SKILL.md,
справочники — рядом, `…/kd-install/references/<файл>`.

Шаг ниже — что сделать и чем проверить; команды и подробности — в справочнике шага: **прочитать его перед
шагом**, не по памяти.

## Правила

Полный текст — `references/rules.md` (прочитать до шага 0).

- После каждого шага — его проверка; не прошла — не идти дальше, разобрать по `references/troubleshooting.md`.
- Спрашивать, а не угадывать: где проекты, какие базы, какая из них **песочница** (роль определяет только
  человек: `песочница` разрешает скриптам подключаться к базе, `боевая` — нет).
- **Закончить ход** и ждать ответа (прежние ответы — не согласие): Docker Desktop и `comcntr.dll` ставит
  человек; пароли не спрашивать и не вписывать; `projects.yaml` — показать целиком; запись в репозиторий
  проекта 1С; перезапуск клиента и одобрение сервера; несохранённые проекты правил перед обновлением; нет
  предусловия проекта; `docker info` падает. `git`, `uv` — только после согласия.
- Инструменты сервера — только через клиент; исключение — `check_server.py` как проверка шага 5.
- Глобальные настройки клиентов (`~\.cursor`, `~\.claude`, `%APPDATA%\…`) и чужие контейнеры не читать.
- `projects*.yaml`, `.mcp.json`, `.cursor/mcp.json`, `docker-compose.override.yml`, `.env` не коммитить. Тексты с
  обратной косой — инструментами редактирования, не строками Python.

## Шаги

| Шаг | Что сделать | Проверка | Справочник |
|---|---|---|---|
| 0 | Что есть: `git`, `docker`, `uv`, `docker info`; уже установлен — к нужному шагу | Docker отвечает | `references/start.md` |
| 1 | Образ (по умолчанию без uv/Git) или клон | файлы релиза / `import kd_rules_mcp` | `references/start.md` |
| 2 | Черновик проектов: выгрузки, расширения, серверы 1С; спросить порядок расширений, `data_mcp`, `rules_dir`, обмены (профиль обмена) | предусловия названы человеку | `references/projects.md` |
| 3 | `projects.yaml` | `load_catalog`; **закончить ход**: файл целиком, «да» | `references/projects-yaml.md` |
| 4 | `projects.local.yaml`; порт 8060 занят — `port`, второй экземпляр — `instance` | `docker ps` | `references/local-settings.md` |
| 5 | Запуск: образ — `setup`, `up --no-build`; клон — `setup_local.py`, `up --build` | `check_server.py`, код 0 | `references/run-and-connect.md` |
| 6 | Скиллы и `.mcp.json` проекта; обмен двух баз — **папка обмена вне проектов баз** (`--side` дважды или `--exchange <id>` профиля); **закончить ход**: перезапуск клиента, одобрение | `project_list`, `structure_load_project` в новой сессии | `references/run-and-connect.md` |
| 7 | Необязательно: база КД для `kd_check` | `ИТОГ OK` | `references/kd-check.md` |
| 8 | Необязательно: `bsp_check` | `ИТОГ OK` | `references/bsp-check.md` |
| 9 | Обновление: сначала `rules_projects`, образ для отката, сверка `docker compose config` | `check_server.py`, `project_list` | `references/update.md` |

После записи `.mcp.json` (шаг 6) в этой сессии инструментов `kd-rules-mcp` нет — так и должно быть.

## Справочники

| Файл | Что внутри |
|---|---|
| `references/rules.md` | правила целиком: шесть точек «закончить ход», доступ к серверу, чужие настройки |
| `references/start.md` | шаги 0–1: проверка окружения, кавычки и оболочки, образ или клон |
| `references/projects.md` | шаг 2: черновик проекта, `data_mcp`, `rules_dir`, таблица предусловий |
| `references/projects-yaml.md` | шаг 3: заполнение и проверка для клона и образа |
| `references/local-settings.md` | шаг 4: порт, второй экземпляр, `image_tag`, что попадает в `.env` |
| `references/run-and-connect.md` | шаги 5–6: запуск (PowerShell, sh, cmd, тома), подключение в проекте 1С, `--cursor`, `--client agents` |
| `references/kd-check.md` | шаг 7: база КД, `kd_check.py prepare` и `check` |
| `references/bsp-check.md` | шаг 8: `bsp_check.py`, логин, `comcntr.dll` |
| `references/update.md` | шаг 9: сохранение работы, откат, порядок обновления, скиллы в проектах |
| `references/troubleshooting.md` | таблица «шаг — симптом — действие» |

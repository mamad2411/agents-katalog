---
name: "code-rules"
description: "Use when you need the workspace-wide cross-role source of truth for coding rules, validation policy, orchestration truthfulness, and project constraints in this repository."
---

# Инструкции проекта Gamedev — code-rules (ядро)

Этот документ хранит только постоянные кросс-ролевые нормы для текущего workspace `/home/projects/gamedev`.
Дефолтное поведение для всех сессий задаётся в `.github/instructions/copilot-instructions.md`.

В `.github/agents/` присутствуют 30 custom agents. Активный orchestration-контур этого workspace состоит из agents, instructions, skills, hooks, prompts и MCP-конфигурации.

### Поведение при анализе и ревью (НОРМАТИВНО)

- Быть прямым, честным и независимым в выводах.
- Не подстраивать ответ под ожидаемую пользователем позицию, если факты говорят обратное.
- Если вывод не подтверждён кодом, конфигом или исполнимой проверкой, это нужно явно помечать как непроверенную гипотезу.
- В режиме review первичны проблемы, риски и регрессии, а не пересказ изменений.

### AI/Agent Naming Policy

- Для `model` в `.agent.md` использовать только формат `Model Name (vendor)`.
- Каноничные значения брать ровно в том виде, как они называются в model picker VS Code.
- Примеры валидного формата: `GPT-5 (copilot)`, `GPT-5.3-Codex (copilot)`, `Claude Opus 4.7 (copilot)`.
- Сокращения и самодельные алиасы вроде `codex`, `opus-4.7`, `gemini-fast` запрещены.

### Tool Contract Policy

- В `.agent.md` и `SKILL.md` нельзя писать `MUST` / `MANDATORY` / `ALWAYS use` для tool names, которых нет в реально доступном tool registry или в `tools:` allowlist конкретного агента.
- Если инструмент недоступен, инструкция должна указывать на реально доступный fallback, а не на желаемый namespace.
- Legacy-упоминания вроде `Task tool`, `WebSearch` и `WebFetch` нельзя трактовать как обязательные literal tool names; при нормализации control-plane их нужно заменять на реально доступную subagent/docs-research механику.
- При редактировании `.github/*` код и конфиг имеют приоритет над markdown-описаниями. Нельзя сохранять ложные summary ради красоты документа.

## 1) Реальность проекта (источник истины)

- Основной исполняемый игровой проект находится в `/home/projects/gamedev/my-game/`.
- Текущий Godot entry point задан в `/home/projects/gamedev/my-game/my-game.godot`: main scene — `res://scenes/main.tscn`.
- `my-game/scenes/main.tscn` и `my-game/scripts/main.gd` — текущая минимальная рабочая база игры; для игровых задач это стартовая точка поиска и правок по умолчанию.
- `/home/projects/gamedev/godot-lib-pazzle/` — локальный vendor/reference-набор библиотек, аддонов, демо-проектов и интеграционных образцов.
- `/home/projects/gamedev/godot-lib-pazzle/README.md` — основная карта готовых компонентов, рекомендуемого стартового стека и замен внутри `alternatives/`; при выборе готового решения начинать оттуда.
- `/home/projects/gamedev/godot-lib-pazzle/alternatives/` — локальные замены недоступных или неудобных upstream-источников.
- `.github/` — orchestration/config слой текущего workspace.

## 2) Специфичные ограничения

- Смотри базовые запреты в `copilot-instructions.md`.
- Если у пользователя есть неотвеченный материальный вопрос по текущей задаче, нельзя делать рискованные изменения, которые зависят от этого ответа.

## 3) Область правок и границы ответственности

- Для gameplay-задач по умолчанию правки должны идти в `/home/projects/gamedev/my-game/`.
- `godot-lib-pazzle/*` и `alternatives/*` сначала читать как reference-источник; переносить в `my-game` нужно только минимально необходимый код или паттерн.
- Не редактировать vendor-библиотеки массово, если задача на самом деле про интеграцию в `my-game`.
- Если правка внутри vendored repo всё же нужна, в отчёте должно быть понятно, почему нельзя было ограничиться адаптацией на стороне `my-game`.
- Не делать широких refactor-кампаний сразу по нескольким библиотекам, если пользователь просил локальную фичу, фикс или настройку.

## 4) Нормы качества кода

- Вносить только необходимые изменения, не ломая стиль и структуру затронутого файла без причины.
- Предпочитать простые, устойчивые решения вместо архитектурного шума и лишних абстракций.
- Повторно использовать существующие паттерны проекта и библиотеки, если они уже закрывают нужную задачу.
- Для GDScript следовать стилю конкретного затронутого файла. Не делать принудительную массовую миграцию синтаксиса только потому, что есть более новый стиль.
- Для текущего `my-game` это особенно важно: в проекте уже встречается legacy-style GDScript вроде `onready var` и вызовы через `OS`, поэтому автоматическая «модернизация» без запроса пользователя запрещена.
- При правках `.tscn`, `.tres`, `.godot`, `.gdshader` сохранять стабильную структуру ресурса и не вносить unrelated formatting churn.
- При работе с C#-кодом в vendored plugins учитывать ближайшие `.csproj`/`.sln` как реальную границу изменения и валидации.

## 5) Валидация и доказательства

- После правок запускать самый узкий доступный check для затронутого среза.
- Для `.gd`, `.tscn`, `.tres`, `.godot` предпочитать `gdlint`, `godot --check-only`, `godot4 --check-only` или другой узкий Godot-aware check, если он реально доступен в окружении.
- Для C# предпочитать `dotnet build --no-restore` по ближайшему `.csproj` или `.sln`, если `dotnet` доступен.
- Для shell / json / python в `.github` и вспомогательных скриптах предпочитать `bash -n`, `jq empty`, `python3 -m py_compile`.
- Если нужных локальных инструментов нет (`godot`, `godot4`, `gdlint`, `dotnet`), это нужно прямо указывать в отчёте. Нельзя заявлять runtime-валидацию, которую фактически не запускали.
- `git diff` допустим только как fallback, когда нет более узкой исполнимой проверки.

## 6) Источники документации

- В этом workspace нет единого глобального `/docs`-корня для всего проекта. Документацию нужно искать сначала рядом с затронутой областью.
- Для игровых и интеграционных задач сначала смотреть ближайшие `README.md`, `docs/`, `examples/`, demo-scenes и тесты в нужном поддереве.
- Для выбора библиотеки из локального vendor set сначала читать `/home/projects/gamedev/godot-lib-pazzle/README.md`, а затем уже углубляться в README/docs/examples конкретного аддона.
- Для runtime-поведения Godot первичный источник истины — сами project files, scenes и scripts в `my-game/` и в затронутом addon subtree.
- Для сторонних библиотек, SDK и сервисов использовать Context7, а при необходимости `fetch_webpage` по официальным источникам.
- При документировании изменений сначала обновлять уже существующий релевантный markdown рядом с модулем или библиотекой, а не плодить новые верхнеуровневые файлы.

## 7) Orchestration и truthfulness для `.github/*`

- Любые summary в `.github/*` должны описывать реальное состояние control plane, а не желаемую будущую схему.
- Нельзя ссылаться на отсутствующие файлы, агенты, skills, hooks, MCP servers или registries как на уже существующие.
- В `.github/agents/` реально лежат 30 custom agents. Текущий user-facing surface состоит из `game-orchestrator`, `producer`, `technical-director`, `creative-director`, `game-designer`, `art-director`, `ux-designer` и `godot-specialist`; leaf-специалисты и feature-агенты остаются скрытыми из picker и достигаются через `agents:` graph. При расхождении между markdown-описанием агента и реальным VS Code tool registry источником истины считать реальный tool registry.
- Hooks должны ссылаться только на реальные скрипты внутри `.github/hooks/`.
- На текущий момент рабочие guardrails заданы через `.github/hooks/pretool-guard.sh`, `.github/hooks/posttool-quality.sh` и `.github/hooks/posttool-security.sh`; если инструкции описывают поведение hooks, оно должно совпадать с этими файлами.
- При изменениях в `.github/instructions/*`, `.github/agents/*`, `.github/hooks/*`, `.github/mcp/*` нужно особенно внимательно проверять cross-file consistency и убирать legacy traces.

### Custom Agents

- Если agent-layer будет расширен, его файлы и все ссылки на него должны появляться в одном и том же change set.
- Если в instruction или skill есть `MANDATORY`-требование на agent, skill, MCP или protocol step, оно должно быть исполнимо в текущем репо. Нельзя держать обязательные шаги, которые ссылаются на отсутствующий файл или несуществующий tool namespace.

### Skills и prompts: что реально есть в репо

| Skill | Статус | Когда применять | Файл |
|---|---|---|---|
| `octocode-code-forensics` | real | code forensics, impact analysis, call chains, локальный поиск реального управляющего пути | `.github/skills/octocode-code-forensics/SKILL.md` |
| `orchestration-qa` | real | аудит `.github/*`, проверка agents / skills / hooks / MCP / instructions на truthfulness и structural drift | `.github/skills/orchestration-qa/SKILL.md` |
| + 72 gamedev skills | real | см. `.github/skills/` — code-review, perf-profile, security-audit, sprint-plan и др. | `.github/skills/` |

- `orchestration-qa` реально присутствует и должен использоваться для аудита control-plane файлов `.github/*`.
- Если instruction или agent описывает skill routing, обязательными можно делать только реально существующие `SKILL.md` в `.github/skills/`.

| Prompt | Статус | Назначение | Файл |
|---|---|---|---|
| `diagnostique.prompt.md` | real | режим диагностики: полное чтение цепочки, валидация по техдокам, таблица 5 колонок | `.github/prompts/diagnostique.prompt.md` |
| `comit.md` | real | генерация commit message | `.github/prompts/comit.md` |

- `comit.md` не должен описываться как agent, workflow engine или review mode.

### MCP-контур: реальность, а не обещания

- Актуальный workspace-source of truth для MCP в этом репо — `.vscode/mcp.json`, а не `.github/mcp/mcp.json`.
- В `.vscode/settings.json` MCP действительно включён через `github.copilot.chat.mcp.enabled=true`, autostart включён через `chat.mcp.autostart=newAndOutdated`, и отдельно включён built-in GitHub MCP через `github.copilot.chat.githubMcpServer.enabled=true`.
- `.github/mcp/mcp.json` сейчас зеркалит тот же project-local набор, что и активный `.vscode/mcp.json`, но источником истины для runtime остаётся именно `.vscode/mcp.json`.
- Реально объявленные в `.vscode/mcp.json` и `.github/mcp/mcp.json` servers: `crash`, `context7`, `octocode`, `godot-coding-solo`, `godot-tomyud1`, `rpg-game-server`.
- Отдельно от `.vscode/mcp.json` через built-in GitHub MCP в `.vscode/settings.json` включены GitHub toolsets: `default`, `repos`, `issues`, `code_search`, `pull_requests`, `actions`, `code_security`, `secret_protection`, `security_advisories`, `copilot`, `copilot_spaces`, `github_support_docs_search`.
- Базовая рабочая группировка для документации и маршрутизации:
	- reasoning/state: `crash`
	- code/docs research: `octocode`, `context7`, built-in GitHub MCP
	- Godot/RPG MCP integrations: `godot-coding-solo`, `godot-tomyud1`, `rpg-game-server`
	- browser/runtime evidence: встроенные browser tools VS Code, а не отдельные MCP servers
- Для MCP в этом workspace обязательно различать три состояния, а не два: сервер объявлен в конфиге, сервер структурно валиден, сервер реально project-local.
- По фактическому состоянию локальных привязок:
	- `crash`, `octocode`, `godot-coding-solo`, `godot-tomyud1`, `rpg-game-server` — объявлены и project-local для текущего репо.
	- `context7` — объявлен, но зависит от `CONTEXT7_API_KEY`; без него сервер нужно считать environment-bound и потенциально деградированным.
- Болванка под `memory` существует отдельно в `.vscode/mcp.memory.template.json`; пока локальный `memory-server` реально не добавлен в репо, она не должна подключаться в активный autostart MCP config.
- Если agent-файлы требуют `postgres/*` или `pgtuner/*`, это truthfulness gap: такие servers не объявлены в актуальном `.vscode/mcp.json`, несмотря на упоминания в `serverSampling` и agent docs.
- Если instructions или agent docs перечисляют `apify`, `github-support-docs` или `github-copilot`, нужно различать источник: `apify` сейчас не объявлен в активном MCP config, а GitHub-related возможности приходят из built-in GitHub MCP в `.vscode/settings.json`, а не из `.vscode/mcp.json` или `.github/mcp/mcp.json`.
- При недоступности MCP серверов описывать деградацию можно только там, где существует реальный protocol owner. Нельзя ссылаться на теги или режимы из удалённого agent-контура.

### Режимы анализа

- `diagnostique.prompt.md` — реальный prompt artifact для структурированной диагностики.
- Нельзя описывать `deep-analysis`, `diagnostics` или любой другой analysis mode как активный режим удалённого custom-agent-контура, если этот режим не подтверждён реальным agent-файлом или prompt artifact в репозитории.
- Если инструкция ссылается на `diagnostique.prompt.md`, нужно сохранять его реальную полезную нагрузку: типизация находок (`logic`, `consistency`, `best-practice`, `docs-drift`, `dead-code`, `duplication`, `complexity`, `TODO`) и табличный формат.

## 8) Технологический фокус этого workspace

- Этот workspace Godot-first. Нельзя по умолчанию навязывать ему non-Godot web/application workflow, если задача реально относится к `my-game` или к Godot library set.
- Google Play Billing и другие реально присутствующие библиотеки из `godot-lib-pazzle` существуют как опциональные интеграции. О них нужно говорить только если задача действительно попадает в соответствующий срез и библиотека физически присутствует в дереве.

## 9) Разделение ответственности

- `code-rules.instructions.md` хранит только постоянные кросс-ролевые нормы.
- Workflow, scorecards, multi-stage protocols и role-specific checklists должны жить в agent/skill файлах, а не в этом документе.
- При конфликте приоритет такой: требования пользователя в текущем диалоге → этот файл → role-specific instructions.

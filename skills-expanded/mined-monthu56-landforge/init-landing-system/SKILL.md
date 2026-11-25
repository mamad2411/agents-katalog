---
name: init-landing-system
description: Развернуть систему генерации лендингов (скиллы new-landing/landing-experiment/landing-journal/landing-ads + CI + nginx + docs/adr + experiments + стартовые README/CLAUDE) в уже существующем проекте. Использовать, когда нужно поставить эту систему в другой репозиторий/проект, забутстрапить лендинг-проект с нуля или перенести наработки. Merge-aware: не затирает существующие файлы без подтверждения.
---

# init-landing-system — развёртывание системы в проекте

Ставит всю систему генерации лендингов в существующий проект из снимка (`reference/system/`) +
шаблонов (`reference/templates/`), подставляя инфраструктурные значения целевого проекта.
Безопасно: существующие файлы по умолчанию **не перезаписываются**.

## Когда и где

- Запускать **в целевом проекте** (куда ставим систему), не в эталоне-источнике.
- Чтобы skill был доступен в любом проекте — установить его в user-level:
  `bash scripts/install_user.sh` (копирует skill со снимком в `~/.claude/skills/`). После этого
  `/init-landing-system` доступен везде.
- Снимок системы обновляется из эталона скриптом `scripts/sync_templates.sh` (запускать в
  эталонном репо после изменений в скиллах/CI/инфре, затем переустановить в user-level).

## Workflow

### 1. Проверки
- Целевой проект — git-репозиторий (если нет — предложи `git init`).
- Это не сам эталон-источник (init_project.py предупредит, если увидит себя в целевом).

### 2. Собрать параметры
Нужно (если не заданы — спроси через `AskUserQuestion`):
- **brand** — название проекта/бренда;
- **prod-domain** — канонический прод-домен;
- **staging-domain** — staging-домен;
- **slug** — базовый slug (из него имена контейнеров `<slug>-landing` / `new-<slug>-landing` и
  каталоги `/root/<container>`; можно переопределить `--prod-container`/`--staging-dir` и т.д.).

### 3. Предпросмотр (dry-run)
```bash
python3 .claude/skills/init-landing-system/scripts/init_project.py \
  --brand "<Brand>" --prod-domain <prod> --staging-domain <staging> --slug <slug> \
  --target <path-to-project> --dry-run
```
Покажет, что будет записано и что уже существует (конфликты).

### 4. Развернуть
Убери `--dry-run`. Существующие файлы пропускаются (перечислятся). Чтобы перезаписать
конкретные — повтори с `--force` (осторожно: затрёт правки целевого проекта).

### 5. Что получит проект
`.claude/skills/` (4 генераторных скилла), `.github/workflows/` (deploy + cleanup-preview под
домены проекта), `deploy/nginx.{prod,staging}.conf`, `docs/adr/` (README + template),
`experiments/README.md`, `.gitignore`, стартовые `README.md` и `CLAUDE.md`.

### 6. Чеклист ручного (вне кода)
init_project.py печатает его в конце:
1. Сервер: два контейнера nginx + Traefik-роуты на домены (как в эталоне: Traefik + два
   `nginx:alpine`; webroot `<DIR>/html`, конфиг `<DIR>/nginx.conf`).
2. DNS: прод- и staging-домены → сервер.
3. GitHub-secrets: `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_SSH_KEY`, `DEPLOY_KNOWN_HOSTS`.
4. Первый лендинг: `/new-landing`; затем реальные ID Метрики/верификаций.

### 7. Зафиксировать
Предложи в целевом проекте: `git add -A && git commit` первичной системы. Дальше проект живёт по
своему README/CLAUDE.

## Важно
- Контентные плейсхолдеры скелета (`{{TITLE}}`, `{{HERO_*}}`, `{{METRIKA_ID}}` …) **не**
  подставляются — это часть `new-landing`, заполняются при генерации лендинга. init подставляет
  только инфраструктурный whitelist (см. `reference/placeholders.md`).
- Инвариант системы переносится вместе: лендинги — статический HTML, контент в разметке, без JS
  на критпути.

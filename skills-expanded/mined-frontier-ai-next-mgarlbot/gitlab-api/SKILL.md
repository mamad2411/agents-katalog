---
name: gitlab_api
description: GitLab REST API — проекты, MR, issues, pipelines, файлы репозитория
triggers: [gitlab, git lab, merge request, mr, issue, pipeline, репозиторий, проект gitlab, gitlab api]
tools: [gitlab_api]
platform: all
---

## GitLab REST API (`gitlab_api` tool)

Токен и URL GitLab уже в настройках бота (`GITLAB_API_TOKEN`, `GITLAB_API_URL`). **Не** передавай токен в аргументах и **не** выводи его в ответ.

### Когда использовать

- «покажи MR / issues / pipeline в проекте X»
- «создай issue / merge request»
- «прочитай `.gitlab-ci.yml` из репо»
- «найди проекты / поиск по GitLab»

Для **редактирования `.gitlab-ci.yml` локально** — скилл `gitlab_pages_ci` + `shell`.
Для **чтения/создания через API** — только `gitlab_api`.

### `project_id`

Числовой ID **или** path: `group/subgroup/project` (как в URL GitLab).

### Типовые вызовы

**Список проектов (где я member):**
```json
{"action": "list_projects", "params": {"membership": true, "simple": true, "per_page": 20}}
```

**Проект по path:**
```json
{"action": "get_project", "project_id": "frontierai/teams/mag/dmas/gmas"}
```

**Merge requests (открытые):**
```json
{"action": "list_merge_requests", "project_id": "group/project", "params": {"state": "opened", "per_page": 10}}
```

**Создать MR:**
```json
{
  "action": "create_merge_request",
  "project_id": "group/project",
  "params": {
    "source_branch": "feature/foo",
    "target_branch": "main",
    "title": "feat: foo",
    "description": "…"
  }
}
```

**Issues / pipeline / файл:**
```json
{"action": "list_issues", "project_id": "group/project", "params": {"state": "opened"}}
{"action": "list_pipelines", "project_id": "group/project", "params": {"ref": "main", "per_page": 5}}
{"action": "get_file", "project_id": "group/project", "params": {"file_path": "README.md", "ref": "main"}}
{"action": "list_tree", "project_id": "group/project", "params": {"path": "", "ref": "main", "per_page": 50}}
```

**Поиск:**
```json
{"action": "search", "params": {"scope": "projects", "search": "mgarlbot"}}
```

**Расширенный запрос** (если нужного action нет):
```json
{
  "action": "api_request",
  "params": {
    "method": "GET",
    "path": "/projects/123/members",
    "query": {"per_page": 20}
  }
}
```

### Правила

- Сначала `list_projects` / `get_project`, если не уверен в `project_id`.
- Не создавай MR/issue без явного запроса пользователя.
- После create — кратко: URL, IID, статус.
- Ошибка 401 → попроси проверить токен в ⚙ Настройки → GitLab.

---
name: 1c-platform-tools-test
description: Тестирование 1С. Используй, когда пользователь просит запустить тесты, XUnit, Vanessa, синтаксический контроль, построить Allure-отчёт.
---

# Тестирование: команды и MCP

Выполняй запуск тестов и отчётов через команды расширения или инструменты MCP. **Выполняй команду сам** (Execute Command или MCP), не проси пользователя нажимать палитру.

## Когда вызывать

| Запрос пользователя (примеры)             | Действие                                  |
|-------------------------------------------|-------------------------------------------|
| Запусти тесты, XUnit, Vanessa             | `test_xunit` / `test_vanessa` или команда |
| Синтаксический контроль                   | `test_syntaxCheck` или команда            |
| Построй Allure-отчёт                      | `test_allure` или команда                 |
| Собери/разбери unit-тесты (.epf)          | команда buildEpf / decompileEpf           |

## Команды расширения

| Задача                        | Command ID                            |
|-------------------------------|---------------------------------------|
| XUnit тесты                   | `1c-platform-tools.test.xunit`        |
| Синтаксический контроль       | `1c-platform-tools.syntaxCheck.run`  |
| Vanessa тесты                 | `1c-platform-tools.test.vanessa`      |
| YAxUnit тесты                 | `1c-platform-tools.test.yaxunit`      |
| Allure отчёт                  | `1c-platform-tools.test.allure`       |
| Собрать unit-тесты            | `1c-platform-tools.test.compileEpf`     |
| Разобрать unit-тесты          | `1c-platform-tools.test.decompileEpf` |
| Запустить EPF в Предприятии   | `1c-platform-tools.epf.run`    |
| Настроить тестовые фреймворки | `1c-platform-tools.test.configure` |
| Загрузить тестовые расширения | `1c-platform-tools.test.loadExtensions`  |
| Выгрузить тестовые расширения | `1c-platform-tools.test.dumpExtensions`  |
| Собрать тестовые расширения   | `1c-platform-tools.test.compileExtensions` |
| Разобрать тестовые расширения | `1c-platform-tools.test.decompileExtensions` |
| Добавить YAxUnit              | `1c-platform-tools.test.addYaxunit` |

Тестовые расширения (YAxUnit и расширение с тестами) живут под каталогом тестов, собранные `*.cfe` — в каталоге сборки; команды расширений решения их не трогают.
Перед прогоном YAxUnit расширения должны быть в базе: `test.loadExtensions`. В дереве команд и они,
и сборка/разборка unit тестов - в группе «Тестовое окружение», запуск тестов - в «Тестировании».

Сборка/разборка unit тестов (тестовых обработок 1С): исходный код под каталогом тестов (выгрузка конфигуратора или проекты 1С:EDT), собранные `.epf` — в каталоге сборки (артефакт, в git не попадает). В каталоге тестов — скриптовые `.os`-тесты OneScript; дымовые наборы Vanessa-ADD поставляются в пакете add (oscript_modules). Обе команды возвращают структурированный результат.

## Панель тестирования VS Code

Тесты также отображаются в нативной панели «Тестирование» (Test Explorer): Vanessa (.feature), xUnit (тестовые обработки), YAxUnit, OneScript (.os в каталоге тестов), 1bdd — с запуском отдельных тестов и статусами. Для интерактивной работы пользователя направляй туда; команды выше — для прогона «всего сразу» и агентных циклов.

## Запуск обработок в Предприятии (epf.run)

Служебные шаги (загрузка фикстур, инициализация ИБ внешней обработкой) — MCP `epf_run` или Execute Command `1c-platform-tools.epf.run`:

```
{ "projectPath": "...", "execute": "./build/out/epf/ЗагрузкаФикстур.epf",
  "command": "Путь=./fixtures/Константы.xml;ЗавершитьРаботуСистемы" }
```

`execute` — путь к EPF/ERF, `command` — строка параметров `/C`; нужен хотя бы один из них.

## Настройка фреймворков (test.configure)

Неинтерактивно — MCP `test_configure` или Execute Command `1c-platform-tools.test.configure` с параметром `frameworks` (ключи: `vanessa`, `xunit`, `yaxunit`, `onescript`, `onebdd`; перечисленные включаются, остальные выключаются, недостающие каталоги создаются).

Агентный вызов без `frameworks` вернёт ошибку с подсказкой, окно не откроется. Интерактивный визард доступен только пользователю из палитры.

## MCP (mcp-1c-platform-tools)

Если доступны инструменты MCP, используй их: `test_xunit`, `test_syntaxCheck`, `test_vanessa`, `test_yaxunit`, `test_allure`, `epf_run`, `test_configure`, а для тестовых расширений - `test_loadExts`, `test_dumpExts`, `test_compileExts`, `test_decompileExts`.

### Параметр projectPath

Корень проекта 1С (каталог с `packagedef`). Передавай, только если пользователь назвал проект: без параметра команда выполняется в текущем проекте.

### Параметр settingsFile

Файл настроек vanessa-runner относительно `projectPath`; перекрывает активный профиль для конкретного вызова. Используй, когда нужен другой набор сценариев или другая ИБ без переключения профиля (например, init-профиль `tools/vrunner.init.json` вместо основного `env.json`).

### Параметр wait

`wait: true` — ждать завершения операции и получить структурированный результат:

```
{
  success: boolean,   // прогон тестов: true только если тесты прошли
  exitCode: number,
  stdout: string,     // вывод vrunner и сводка прогона
  stderr: string,
  tests?: {           // прогоны тестов: сводка по отчёту
    total, passed, failed, errors, skipped,
    reportPath, failedTests
  }
}
```

**`wait: true` — по умолчанию:** агент читает `success`, `exitCode`, счётчики тестов и решает, что делать дальше.

**`wait: false`:** команда уходит в терминал, результат прогона неизвестен — только когда пользователь смотрит выполнение сам.

## Поддержка wait: true (тесты)

| MCP-инструмент    | wait: true |
|-------------------|:----------:|
| `test_syntaxCheck`| ✅          |
| `test_xunit`      | ✅          |
| `test_vanessa`    | ✅          |
| `test_yaxunit`    | ✅          |
| `epf_run`  | ✅          |
| `test_configure`| ✅ (с параметром `frameworks`) |
| `test_allure`     | ❌ (открывает браузер) |

## Примеры

- Проверка синтаксиса (агентный цикл):
  ```
  test_syntaxCheck { projectPath: "C:/projects/MyProject" }
  ```
  → вернёт `{ success: false, exitCode: 1, stdout: "ОШИБКА - ...", stderr: "" }`

- Прогон тестов под другим файлом настроек, без переключения профиля:
  ```
  test_vanessa { projectPath: "C:/projects/MyProject", settingsFile: "tools/vrunner.init.json" }
  ```
  → в ответе счётчики прогона и список упавших тестов

- Выполни команду `1c-platform-tools.test.xunit` для запуска XUnit-тестов текущего проекта.
- Вызови MCP `test_vanessa` с `projectPath` = корень проекта 1С.

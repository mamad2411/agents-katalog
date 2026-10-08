---
description: 
globs: 
alwaysApply: true
---
---
description: Core AI rules for Receipt Split Bot
alwaysApply: true
globs: ["**/*.py", "**/*.js", "**/*.md"]
---
# Global rules

1. Перед любым код-изменением сверяйся с ТЗ (spec.md, лежит в Memory Bank).
2. Нельзя добавлять новые функции, если аналог уже есть — ищи через Workspace Search.
3. Соблюдай styleGuide.md.
4. Изменяй только файлы, явно указанные в запросе.
5. Если diff > 30 строк — запроси подтверждение фразой “Proceed?”.
<!-- 6. Каждый public-метод обязан иметь pytest-тест → временно убираем -->